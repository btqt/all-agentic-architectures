
import os
import json

from typing import Annotated, TypedDict

# LangChain
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from pydantic import BaseModel, Field


# LangGraph
from langgraph.graph import StateGraph, END
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# pretty printing
from rich.console import Console
from rich.markdown import Markdown

from logger_utils import get_logger

from dotenv import load_dotenv

logger = get_logger("react")

load_dotenv()

console = Console()

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

llm = ChatOllama(model=LLM_MODEL_NAME, temperature=0)

# Định nghĩa state
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Định nghĩa tool và llm
@tool("web_search", description="A tool that can be used to search the internet for up-to-date information on any topic, including news, events, and current affairs.")
def search_internet(query: str) -> str:
    """Search the internet for up-to-date information on any topic, including news, events, and current affairs."""
    logger.info(f"\n--- Searching for: [bold green]{query}[/bold green] ---")
    search_tool = DuckDuckGoSearchResults(output_format="list")    
    return search_tool.invoke(query)

tools = [search_internet]

llm_with_tools = llm.bind_tools(tools)

# Định nghĩa basic agent, có thể sử dụng tool nhưng chỉ dùng 1 lần duy nhất
def basic_agent_node(state: AgentState):
    logger.info("--- BASIC AGENT: Thinking... ---")
    # Note: Cung cấp 1 system prompt khuyến khích agent chỉ gọi tool 1 lần duy nhất
    system_prompt = f"""You are a helpful assistant. You have access to a web search tool. Answer the user's question based on the tool's results."""
    
    messages = [("system", system_prompt)] + state["messages"]
    response = llm_with_tools.invoke(messages)
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

logger.info(f"[bold yellow]Testing BASIC agent on a multi-step query:[/bold yellow] '{multi_step_query}'\n")

basic_agent_output = basic_tool_agent_app.invoke({"messages": [("user", multi_step_query)]})

logger.info("\n--- [bold green]Final Output from Basic Agent[/bold green] ---")
console.print(Markdown(basic_agent_output['messages'][-1].content))
logger.info("\n---\n")

def react_agent_node(state: AgentState):
    logger.info("--- REACT AGENT: Thinking... ---")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# ToolNode giống như trước
react_tool_node = ToolNode(tools)

# Router function
def react_router(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        logger.info("--- ROUTER: Decision is to call a tool. ---")
        return "tools"
    else:
        logger.info("--- ROUTER: Decision is to finish. ---")
        return "__end__"

# Bây giờ chúng ta định nghĩa graph với vòng lặp quan trọng
react_graph_builder = StateGraph(AgentState)
react_graph_builder.add_node("agent", react_agent_node)
react_graph_builder.add_node("tools", react_tool_node)
react_graph_builder.add_conditional_edges("agent", react_router, {"tools": "tools", "__end__": END})

react_graph_builder.set_entry_point("agent")

# Đây là sự khác biệt chính: edge đi từ tools QUAY LẠI agent
react_graph_builder.add_edge("tools", "agent")

react_agent_app = react_graph_builder.compile()

logger.info(f"Testing ReAct agent on the same multi-step query: [bold green]'{multi_step_query}'[/bold green]\n")

final_react_output = None

for chunk in react_agent_app.stream({"messages": [("user", multi_step_query)]}, stream_mode="values"):
    final_react_output = chunk
    logger.info(f"--- [bold purple]Current State:[/bold purple] ---")
    chunk["messages"][-1].pretty_print()
    logger.info("\n---\n")

logger.info("\n--- [bold green]Final Output from ReAct Agent[/bold green] ---")
console.print(Markdown(final_react_output['messages'][-1].content))
class AgentEvaluation(BaseModel):
    """Schema để đánh giá agent"""
    task_completion_score: int = Field(description="Score từ 1-10 về mức độ hoàn thành nhiệm vụ.")
    reasoning_quality_score: int = Field(description="Score từ 1-10 về chất lượng suy luận.")
    justification: str = Field(description="Giải thích ngắn gọn cho các điểm số.")

judge_llm = llm.with_structured_output(AgentEvaluation)

def evaluate_agent(output_content: str):
    prompt = f"""You are an expert judge of AI agents. Evaluate the following final answer provided by an agent based on a complex, multi-step user requset. Provide a brief justification written in Vietnamese.
    
    User Request: {multi_step_query}

    Agent Final Answer:
    {output_content}

    Evaluate the answer from 1-10 for task completion and reasoning quality. Provide a brief justification.
    """

    return judge_llm.invoke(prompt)

if basic_agent_output and final_react_output:
    logger.info("--- Evaluating Basic Agent's output ---")
    basic_eval = evaluate_agent(basic_agent_output['messages'][-1].content)
    logger.info(basic_eval.model_dump())

    logger.info("\n--- Evaluating ReAct Agent's output ---")
    react_eval = evaluate_agent(final_react_output['messages'][-1].content)
    logger.info(react_eval.model_dump())


