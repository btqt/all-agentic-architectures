
import os
import json

from typing import Annotated, TypedDict

# LangChain
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage
from langchain.tools import tool
from pydantic import BaseModel, Field


# LangGraph
from langgraph.graph import StateGraph, END
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# pretty printing
from rich.console import Console

from logger_utils import get_logger

from dotenv import load_dotenv

logger = get_logger("react")

load_dotenv()

console = Console()

# Định nghĩa state
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Định nghĩa tool và llm
@tool("web_search", description="A tool that can be used to search the internet for up-to-date information on any topic, including news, events, and current affairs.")
def search_internet(query: str) -> str:
    """Search the internet for up-to-date information on any topic, including news, events, and current affairs."""
    search_tool = DuckDuckGoSearchResults(output_format="list")    
    return search_tool.invoke(query)

tools = [search_internet]

llm = ChatOllama(model="qwen2.5-coder:3b", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Định nghĩa basic agent, có thể sử dụng tool nhưng chỉ dùng 1 lần duy nhất
def basic_agent_node(state: AgentState):
    console.print("--- BASIC AGENT: Thinking... ---")
    # Note: Cung cấp 1 system prompt khuyến khích agent chỉ gọi tool 1 lần duy nhất
    system_prompt = f"""You are a helpful assistant. You have access to a web search tool. Answer the user's question based on the tool's results. You must provide a final answer after one tool call."""
    
    messages = [("system", system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# Định nghĩa basic linear graph
basic_graph_builder = StateGraph(AgentState)
basic_graph_builder.add_node("agent", basic_agent_node)
basic_graph_builder.add_node("tools", ToolNode(tools))

basic_graph_builder.set_entry_point("agent")

# Sau agent, nó chỉ có thể đi tới tools, và sau tools, nó BẮT BUỘC phải kết thúc.
basic_graph_builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", "__end__": END})
basic_graph_builder.add_edge("tools", END)

basic_tool_agent_app = basic_graph_builder.compile()

multi_step_query = "Who is the current CEO of the company that created the sci-fi movie 'Dune', and what was the budget for that company's most recent film?"

console.print(f"[bold yellow]Testing BASIC agent on a multi-step query:[/bold yellow] '{multi_step_query}'\n")

basic_agent_output = basic_tool_agent_app.invoke({"messages": [("user", multi_step_query)]})

console.print("\n--- [bold red]Final Output from Basic Agent[/bold red] ---")
console.print(Markdown(basic_agent_output['messages'][-1].content))





