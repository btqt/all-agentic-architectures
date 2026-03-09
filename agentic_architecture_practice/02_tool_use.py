import os

from typing import TypedDict, Annotated

from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage

from duckduckgo_search import DDGS

from dotenv import load_dotenv

from logger_utils import get_logger

logger = get_logger("tool_use")

load_dotenv()

search_tool = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "A tool that can be used to search the internet for up-to-date information on any topic, including news, events, and current affairs.",
        "parameters": {
            "type": "object",
            "properties": {} 
        }
    }
}

tools = [search_tool]


LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL")

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]



