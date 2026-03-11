import os
import json

from typing import Annotated, TypedDict

# LangChain
from langchain_ollama import ChatOllama
from langchain.core.messages import BaseMessage
from pydantic import BaseModel, Field


# LangGraph
from langgraph.graph import StateGraph, END
from langgraph.graph.message import AnyMessage, add_messages

# pretty printing
from rich.console import Console

from logger_utils import get_logger

from dotenv import load_dotenv

logger = get_logger("react")

load_dotenv()




