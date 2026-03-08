from dotenv import load_dotenv
from logger_utils import get_logger

logger = get_logger("tool_use")

from langchain_ollama import ChatOllama

from langchain_tavily import TavilySearch

load_dotenv()

llm = ChatOllama(model="llama3.1:8b", temperature=0.2)


search_tool = TavilySearch(max_results=2)
logger.info("Tavily search tool initialized.")

search_tool.name = "web_search"
search_tool.description = "A tool that can be used to search the internet for up-to-date information on any topic, including news, events, and current affairs."

tools = [search_tool]
logger.info(f"Tool '{search_tool.name}' created with description '{search_tool.description}'")


