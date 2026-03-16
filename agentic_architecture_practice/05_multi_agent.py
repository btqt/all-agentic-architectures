import os
from typing import List, Annotated, TypedDict, Optional
from dotenv import load_dotenv

# LangChain components
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# LangGraph components
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages, AnyMessage
from langgraph.prebuilt import ToolNode, tools_condition

# For pretty printing
from rich.console import Console
from rich.markdown import Markdown

console = Console()

load_dotenv()

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
llm = ChatOllama(model=LLM_MODEL_NAME, temperature=0)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Định nghĩa tool và llm
@tool("web_search", description="A tool that can be used to search the internet for up-to-date information on any topic, including news, events, and current affairs.")
def search_internet(query: str) -> str:
    """Search the internet for up-to-date information on any topic, including news, events, and current affairs."""
    console.print(f"\n--- Searching for: [bold green]{query}[/bold green] ---")
    search_tool = DuckDuckGoSearchResults(output_format="list")    
    return search_tool.invoke(query)

tools = [search_internet]
llm_with_tools = llm.bind_tools(tools)

# Định nghĩa monilithic agent node
def monolithic_agent_node(state: AgentState):
    console.print("--- MONOLITHIC AGENT: Thinking... ---")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# Xây dựng ReAct graph cho monolithic agent
mono_graph_builder = StateGraph(AgentState)
mono_graph_builder.add_node("agent_node", monolithic_agent_node)
mono_graph_builder.add_node("tool_node", ToolNode(tools))
mono_graph_builder.set_entry_point("agent_node")













