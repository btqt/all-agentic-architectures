import os
import operator
import re
from typing import Annotated, TypedDict, List, Optional

# LangChain
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage, ToolMessage
from langchain_community.tools import DuckDuckGoSearchResults
from pydantic import BaseModel, Field
from langchain.tools import tool

# LangGraph
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from rich.console import Console
from rich.markdown import Markdown

from logger_utils import get_logger
from dotenv import load_dotenv

logger = get_logger("planning")
load_dotenv()
console = Console()

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
llm = ChatOllama(model=LLM_MODEL_NAME, temperature=0)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# 1. Định nghĩa tool và llm
@tool("web_search", description="A tool that can be used to search the internet for up-to-date information on any topic, including news, events, and current affairs.")
def search_internet(query: str) -> str:
    """Search the internet for up-to-date information on any topic, including news, events, and current affairs."""
    logger.info(f"\n--- TOOL: Searching for [bold green]{query}[/bold green] ---")
    search_tool = DuckDuckGoSearchResults(output_format="list")    
    return search_tool.invoke(query)

tools = [search_internet]

# 3. Định nghĩa LLM và bind nó vào custom tool của chúng ta
llm_with_tools = llm.bind_tools(tools)

# 4. Agent node với một system prompt để ép buộc một cuộc gọi tool tại một thời điểm
def react_agent_node(state: AgentState):
    logger.info("--- REACTIVE Agent: Thinking... ---")
    messages_with_system_prompt = []
    # [
    #     SystemMessage(content="You are helpful research assistant. You must call one and only one tool at a time. Do not call multiple tools in a single turn. After receiving the result from a tool, you will decide on the next step.")
    # ]

    messages_with_system_prompt += state["messages"]

    response = llm_with_tools.invoke(messages_with_system_prompt)

    return {"messages": [response]}

# 5. Sử dụng custom tool đã được chỉnh sửa của chúng ta trong ToolNode
tool_node = ToolNode(tools)

react_graph_builder = StateGraph(AgentState)
react_graph_builder.add_node("agent", react_agent_node)
react_graph_builder.add_node("tools", tool_node)
react_graph_builder.set_entry_point("agent")
react_graph_builder.add_conditional_edges("agent", tools_condition)
react_graph_builder.add_edge("tools", "agent")

react_agent_app = react_graph_builder.compile()

plan_centric_query = """
Find the population of the capital cities of France, Germany, and Italy. 
Then calculate their combined total. 
Finally, compare that combined total to the population of the United States, and say which is larger.
"""

logger.info(f"""[bold yellow]Testing REACTIVE agent on a plan-centric query:[/bold yellow] '{plan_centric_query}'\n""")

final_react_output = None

for chunk in react_agent_app.stream({"messages": [("user", plan_centric_query)]}, stream_mode="values"):
    final_react_output = chunk
    logger.info(f"--- [bold purple]Current State:[/bold purple] ---")
    chunk["messages"][-1].pretty_print()
    logger.info("\n---\n")

logger.info("\n--- [bold red]Final Output from ReAct Agent[/bold red] ---")
console.print(Markdown(final_react_output['messages'][-1].content))





# Pydantic model để đảm bảo kết quả đầu ra của planner là danh sách các bước có cấu trúc
class Plan(BaseModel):
    """Một kế hoạch gồm các cuộc gọi tool cần thực thi để trả lời truy vấn của người dùng."""
    steps: List[str] = Field(description="A list of tool calls that, when executed, will answer the query.")

# Định nghĩa state cho planning agent
class PlanningState(TypedDict):
    user_request: str
    plan: Optional[List[str]]
    intermediate_steps: List[ToolMessage]
    final_answer: Optional[str]

def planner_node(state: PlanningState):
    """Tạo một kế hoạch hành động để trả lời yêu cầu của người dùng."""
    logger.info("--- PLANNER: Decomposing task... ---")
    planner_llm = llm.with_structured_output(Plan)

    # THE FIX: Một prompt rõ ràng hơn nhiều với ví dụ cụ thể (few-shot prompting)
    prompt = f"""You are an expert planner. Your job is to create a step-by-step plan to answer the user's request. Each step in the plan must be a single call to the `web_search` tool.
        **Instructions:**
        1. Analyze the user's request.
        2. Break it down into a sequence of simple, logical search queries.
        3. Format the output as a list of strings, where each string is a single valid tool call.
        
        **Example:**
        User Request: What is the capital of France and what is its population?
        Plan:
        1. web_search("capital of France")
        2. web_search("population of Paris")
        
        **User's Request:**
        {state["user_request"]}
        """

    plan_result = planner_llm.invoke(prompt)

    # Use plan_result.steps, not plan.steps to avoid confusion with the variable name 'plan'
    logger.info(f"--- PLANNER: Generated Plan: {plan_result.steps} ---")
    return {"plan": plan_result.steps}

def executor_node(state: PlanningState):
    """Executes bước tiếp theo trong plan"""
    logger.info("--- EXECUTOR: Running next step... ---")
    
    plan = state["plan"]
    next_step = plan[0]

    # Robust regex to handle both single and double quotes
    match = re.match(r'(\w+)\((?:\"|\')(.*?)(?:\"|\')\)', next_step)
    if not match:
        tool_name = "web_search"
        query = next_step
    else:
        tool_name, query = match.groups()[0], match.groups()[1]

    logger.info(f"--- EXECUTOR: Calling tool: '{tool_name}' with query '{query}' ---")

    result = search_internet(query)

    # We still create a ToolMessage, but the tool call itself is now safe
    tool_message = ToolMessage(content=str(result),
                               name=tool_name,
                               tool_call_id=f"manual-{hash(query)}")
    
    return {
        "plan": plan[1:],  # Pop the executed step from the plan
        "intermediate_steps": state["intermediate_steps"] + [tool_message]
    }

def synthesizer_node(state: PlanningState):
    """Tổng hợp final answer từ các intermidiate steps."""
    logger.info("--- SYNTHESIZER: Generating final answer... ---")
    context = "\n".join(f"Tool {msg.name} returned: {msg.content}" for msg in state["intermediate_steps"])

    prompt = f"""You are an expert synthesizer. Based on the user's request and the collected data, provide a comprehensive final answer.
    
    Request: {state['user_request']}
    Collected Data:
    {context}
    """
    final_answer = llm.invoke(prompt)
    return {"final_answer": final_answer}

def planning_router(state: PlanningState):
    if not state["plan"]:
        logger.info("--- ROUTER: Plan complete. Moving to synthesizer ---")
        return "synthesize"
    else:
        logger.info("--- ROUTER: Plan has more steps. Continuing execution in executor ---")
        return "execute"

planning_graph_builder = StateGraph(PlanningState)
planning_graph_builder.add_node("plan", planner_node)
planning_graph_builder.add_node("execute", executor_node)
planning_graph_builder.add_node("synthesize", synthesizer_node) 

planning_graph_builder.set_entry_point("plan")
planning_graph_builder.add_conditional_edges("plan", planning_router, {"execute": "execute", "synthesize": "synthesize"}) # Route after planning
planning_graph_builder.add_conditional_edges("execute", planning_router, {"execute": "execute", "synthesize": "synthesize"})
planning_graph_builder.add_edge("synthesize", END)

planning_agent_app = planning_graph_builder.compile()
print("Planning agent compiled successfully.")

logger.info(f"""[bold green]Testing PLANNING agent on the same plan-centric query:[/bold green] '{plan_centric_query}'\n""")

# Remember to initialize the state correctly, especially the list for intermediate steps
initial_planning_input = {"user_request": plan_centric_query, "intermediate_steps": []}
final_planning_output = planning_agent_app.invoke(initial_planning_input)

logger.info("\n--- [bold green]Final Output from Planning Agent[/bold green] ---")
console.print(Markdown(final_planning_output['final_answer']))
















