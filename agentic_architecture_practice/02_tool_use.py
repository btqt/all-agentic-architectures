import os

from typing import TypedDict, Annotated
from pprint import pprint

from langchain_ollama import ChatOllama

from langgraph.graph import StateGraph, END
from langgraph.graph.message import AnyMessage, add_messages

from langchain.tools import tool

from langgraph.prebuilt import ToolNode

from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults

from dotenv import load_dotenv

from rich.console import Console

from logger_utils import get_logger

logger = get_logger("tool_use")

load_dotenv()

@tool("web_search", description="A tool that can be used to search the internet for up-to-date information on any topic, including news, events, and current affairs.")
def search_internet(query: str) -> str:
    """Search the internet for up-to-date information on any topic, including news, events, and current affairs."""
    search_tool = DuckDuckGoSearchResults(output_format="list")    
    return search_tool.invoke(query)

tools = [search_internet]

console = Console()

# Let's test the tool directly to see its output format
print("\n--- Testing the tool directly ---")
test_query = "What was the score of the last Super Bowl?"
test_result = search_internet.invoke({"query": test_query})
console.print(f"[bold green]Query:[/bold green] {test_query}")
console.print("\n[bold green]Result:[/bold green]")
console.print(test_result)

LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL")

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

llm = ChatOllama(model=LLM_MODEL_NAME, temperature=0)

llm_with_tools = llm.bind_tools(tools)

def agent_node(state: AgentState):
    """Node chính thực hiện gọi LLM để quyết định hành động tiếp theo."""
    console.print("--- AGENT: Thinking... ---")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

tools_node = ToolNode(tools)

def router_function(state: AgentState) -> str:
    """Kiểm tra message cuối cùng của agent để quyết định bước tiếp theo."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        # Agent đã yêu cầu một cuộc gọi tool
        console.print("--- ROUTER: Decision is to call a tool. ---")
        return "call_tool"
    else:
        # Agent đã cung cấp câu trả lời cuối cùng
        console.print("--- ROUTER: Decision is to finish. ---")
        return "__end__"


graph_builder = StateGraph(AgentState)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("call_tool", tools_node)

graph_builder.set_entry_point("agent")

# Thêm conditional router
graph_builder.add_conditional_edges("agent", router_function)

# Thêm edge từ tool node quay lại agent để hoàn tất vòng lặp
graph_builder.add_edge("call_tool", "agent")

tool_agent_app = graph_builder.compile()

try:
    png_image = tool_agent_app.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(png_image)
    console.print("\n--- Graph visualization saved to [bold green]graph.png[/bold green] ---")
except Exception as e:
    logger.error(f"Graph visualization failed: {e}")


user_query = "What were the main announcements from Apple's latest WWDC event?"
initial_input = {"messages": [("user", user_query)]}

console.print(f"[bold cyan]🚀 Kicking off Tool Use workflow for request:[/bold cyan] '{user_query}'\n")

for chunk in tool_agent_app.stream(initial_input, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
    console.print("\n---\n")

console.print("\n[bold green]✅ Tool Use workflow complete![/bold green]")



