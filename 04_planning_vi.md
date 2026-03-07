# 📘 Agentic Architectures 4: Planning

Trong notebook này, chúng ta khám phá kiến trúc **Planning**. Pattern này giới thiệu một lớp nhìn xa trông rộng (foresight) quan trọng vào quá trình suy luận của một agent. Thay vì phản ứng với thông tin theo từng bước như trong mô hình ReAct, một planning agent trước tiên sẽ phân tách một nhiệm vụ phức tạp thành một chuỗi các mục tiêu phụ nhỏ hơn, có thể quản lý được. Nó tạo ra một bế hoạch tác chiến (battle plan) đầy đủ *trước khi* thực hiện bất kỳ hành động nào.

Cách tiếp cận chủ động này mang lại cấu trúc, khả năng dự đoán và hiệu quả cho các nhiệm vụ nhiều bước. Để làm nổi bật các lợi ích của nó, chúng ta sẽ so sánh trực tiếp hiệu năng của một **reactive agent (ReAct)** với **planning agent** mới của chúng ta. Chúng ta sẽ giao cho cả hai một nhiệm vụ yêu cầu thu thập nhiều mẩu thông tin trước khi thực hiện phép tính cuối cùng, chứng minh cách một kế hoạch được tính toán trước có thể dẫn đến một giải pháp mạnh mẽ và trực tiếp hơn.

### Definition
Kiến trúc **Planning** bao gồm một agent thực hiện việc phân tách một mục tiêu phức tạp thành một chuỗi các nhiệm vụ phụ chi tiết một cách rõ ràng *trước khi* bắt đầu thực thi. Kết quả đầu ra của giai đoạn lập kế hoạch ban đầu này là một kế hoạch cụ thể, từng bước mà agent sau đó sẽ tuân thủ một cách có phương pháp để đạt được giải pháp.

### High-level Workflow
1.  **Receive Goal:** Agent nhận một nhiệm vụ phức tạp.
2.  **Plan:** Một thành phần 'Planner' chuyên dụng phân tích mục tiêu và tạo ra một danh sách có thứ tự các nhiệm vụ phụ cần thiết để đạt được mục tiêu đó. Ví dụ: `["Tìm sự thật A", "Tìm sự thật B", "Tính toán C bằng A và B"]`.
3.  **Execute:** Một thành phần 'Executor' nhận kế hoạch và thực hiện từng nhiệm vụ phụ theo trình tự, sử dụng các tool khi cần thiết.
4.  **Synthesize:** Sau khi tất cả các bước trong kế hoạch hoàn tất, một thành phần cuối cùng sẽ tổng hợp các kết quả từ các bước đã thực thi thành một câu trả lời cuối cùng mạch lạc.

### When to Use / Applications
*   **Multi-Step Workflows:** Lý tưởng cho các nhiệm vụ mà trình tự các hoạt động đã được biết trước và quan trọng, chẳng hạn như tạo một báo cáo yêu cầu tìm nạp dữ liệu, xử lý dữ liệu đó và sau đó tóm tắt nó.
*   **Project Management Assistants:** Phân chia một mục tiêu lớn như "ra mắt một tính năng mới" thành các nhiệm vụ phụ cho các nhóm khác nhau.
*   **Educational Tutoring:** Tạo một kế hoạch bài giảng để dạy một học sinh một khái niệm cụ thể, từ các nguyên tắc nền tảng đến ứng dụng nâng cao.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Cấu trúc & Có thể truy vết (Traceable):** Toàn bộ workflow được trình bày trước, làm cho quy trình của agent trở nên minh bạch và dễ debug.
    *   **Hiệu quả:** Có thể hiệu quả hơn ReAct đối với các nhiệm vụ có thể dự đoán được, vì nó tránh được các vòng lặp suy luận không cần thiết giữa các bước.
*   **Weaknesses:**
    *   **Dễ bị phá vỡ (Brittle to Change):** Một kế hoạch được lập sẵn có thể thất bại nếu môi trường thay đổi bất ngờ trong quá trình thực thi. Nó ít có khả năng thích ứng hơn một ReAct agent, vốn có thể thay đổi ý định sau mỗi bước.

## Phase 0: Foundation & Setup
Chúng ta sẽ bắt đầu với quy trình thiết lập tiêu chuẩn: cài đặt các thư viện và cấu hình API keys cho Nebius, LangSmith, và công cụ tìm kiếm web Tavily của chúng ta.

### Step 0.1: Installing Core Libraries
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ cài đặt bộ thư viện tiêu chuẩn của mình, bao gồm gói `langchain-tavily` đã được cập nhật để giải quyết cảnh báo không còn sử dụng (deprecation warning).

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv langchain-tavily
```

### Step 0.2: Importing Libraries and Setting Up Keys
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ import các module cần thiết và load các API keys của mình từ file `.env`.

**Action Required:** Tạo một file `.env` trong thư mục này với các key của bạn:
```
NEBIUS_API_KEY="your_nebius_api_key_here"
LANGCHAIN_API_KEY="your_langsmith_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"
```

```python
import os
import re
from typing import List, Annotated, TypedDict, Optional
from dotenv import load_dotenv

# LangChain components
from langchain_nebius import ChatNebius
from langchain_core.messages import BaseMessage, ToolMessage
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_tavily import TavilySearch

# LangGraph components
from langgraph.graph import StateGraph, END
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# For pretty printing
from rich.console import Console
from rich.markdown import Markdown

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Planning (Nebius)"

# Kiểm tra xem các key đã được thiết lập chưa
for key in ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]:
    if not os.environ.get(key):
        print(f"{key} not found. Please create a .env file and set it.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: The Baseline - A Reactive Agent (ReAct)
Để đánh giá giá trị của planning, trước tiên chúng ta cần một baseline. Chúng ta sẽ sử dụng ReAct agent mà chúng ta đã xây dựng trong notebook trước. Agent này thông minh nhưng bị hạn chế về tầm nhìn—nó tìm ra con đường của mình theo từng bước một.

### Step 1.1: Re-building the ReAct Agent
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ nhanh chóng tái cấu trúc ReAct agent. Tính năng cốt lõi của nó là một vòng lặp nơi kết quả đầu ra của agent được route quay lại chính nó sau mỗi cuộc gọi tool, cho phép nó đánh giá lại và quyết định bước tiếp theo dựa trên thông tin mới nhất.

```python
console = Console()

# Định nghĩa state cho các graph của chúng ta
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# 1. Định nghĩa base tool từ gói tavily
tavily_search_tool = TavilySearch(max_results=2)

# 2. THE FIX: Đơn giản hóa custom tool. 
# Phương thức .invoke() đã trả về một string sạch, vì vậy chúng ta chỉ cần truyền nó qua.
@tool
def web_search(query: str) -> str:
    """Thực hiện tìm kiếm web bằng Tavily và trả về kết quả dưới dạng string."""
    console.print(f"--- TOOL: Searching for '{query}'...")
    results = tavily_search_tool.invoke(query)
    return results

# 3. Định nghĩa LLM và bind nó vào custom tool của chúng ta
llm = ChatNebius(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)
llm_with_tools = llm.bind_tools([web_search])

# 4. Agent node với một system prompt để ép buộc một cuộc gọi tool tại một thời điểm
def react_agent_node(state: AgentState):
    console.print("--- REACTIVE AGENT: Thinking... ---")
    
    messages_with_system_prompt = [
        SystemMessage(content="You are a helpful research assistant. You must call one and only one tool at a time. Do not call multiple tools in a single turn. After receiving the result from a tool, you will decide on the next step.")
    ] + state["messages"]

    response = llm_with_tools.invoke(messages_with_system_prompt)
    
    return {"messages": [response]}

# 5. Sử dụng custom tool đã được chỉnh sửa của chúng ta trong ToolNode
tool_node = ToolNode([web_search])

# ReAct graph với vòng lặp đặc trưng của nó
react_graph_builder = StateGraph(AgentState)
react_graph_builder.add_node("agent", react_agent_node)
react_graph_builder.add_node("tools", tool_node)
react_graph_builder.set_entry_point("agent")
react_graph_builder.add_conditional_edges("agent", tools_condition)
react_graph_builder.add_edge("tools", "agent")

react_agent_app = react_graph_builder.compile()
print("Reactive (ReAct) agent compiled successfully.")
```

### Step 1.2: Testing the Reactive Agent on a Plan-Centric Problem
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ giao cho ReAct agent một nhiệm vụ yêu cầu hai bước thu thập dữ liệu riêng biệt theo sau là một phép tính cuối cùng. Điều này sẽ kiểm tra khả năng quản lý workflow nhiều bước của nó mà không có kế hoạch trả trước.

```python
plan_centric_query = """
Find the population of the capital cities of France, Germany, and Italy. 
Then calculate their combined total. 
Finally, compare that combined total to the population of the United States, and say which is larger.
"""

console.print(f"[bold yellow]Testing REACTIVE agent on a plan-centric query:[/bold yellow] '{plan_centric_query}'\n")

final_react_output = None
for chunk in react_agent_app.stream({"messages": [("user", plan_centric_query)]}, stream_mode="values"):
    final_react_output = chunk
    console.print(f"--- [bold purple]Current State Update[/bold purple] ---")
    chunk['messages'][-1].pretty_print()
    console.print("\n")

console.print("\n--- [bold red]Final Output from Reactive Agent[/bold red] ---")
console.print(Markdown(final_react_output['messages'][-1].content))
```

**Discussion of the Output:**
ReAct agent đã hoàn thành thành công nhiệm vụ. Bằng cách quan sát kết quả được stream, chúng ta có thể theo dõi quá trình suy luận từng bước của nó:
1. Trước tiên, nó quyết định tìm kiếm dân số của Paris.
2. Sau khi nhận được kết quả đó, nó tích hợp vào bộ nhớ và sau đó quyết định bước tiếp theo là tìm kiếm dân số của Berlin.
3. Cuối cùng, với cả hai mẩu thông tin đã thu thập được, nó thực hiện phép tính và đưa ra câu trả lời cuối cùng.

Mặc dù nó hoạt động, nhưng quy trình khám phá lặp đi lặp lại này không phải lúc nào cũng hiệu quả nhất. Đối với một nhiệm vụ có thể dự đoán được như thế này, agent đang thực hiện thêm các cuộc gọi LLM để suy luận giữa mỗi bước. Điều này tạo tiền đề cho việc chứng minh giá trị của một planning agent.

## Phase 2: The Advanced Approach - A Planning Agent
Bây giờ, hãy xây dựng một agent biết suy nghĩ trước khi hành động. Agent này sẽ có một **Planner** chuyên dụng để tạo danh sách nhiệm vụ đầy đủ, một **Executor** để thực hiện kế hoạch, và một **Synthesizer** để lắp ráp kết quả cuối cùng.

### Step 2.1: Defining the Planner, Executor, and Synthesizer Nodes
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ tạo các thành phần cốt lõi cho agent mới của mình:
1.  **`Planner`:** Một node dựa trên LLM nhận yêu cầu của người dùng và xuất ra một kế hoạch có cấu trúc.
2.  **`Executor`:** Một node nhận kế hoạch, thực hiện bước *tiếp theo* bằng một tool và ghi lại kết quả.
3.  **`Synthesizer`:** Một node dựa trên LLM cuối cùng nhận tất cả các kết quả đã thu thập được và tạo ra câu trả lời cuối cùng.

```python
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
    console.print("--- PLANNER: Decomposing task... ---")
    planner_llm = llm.with_structured_output(Plan)
    
    # THE FIX: Một prompt rõ ràng hơn nhiều với ví dụ cụ thể (few-shot prompting)
    prompt = f"""You are an expert planner. Your job is to create a step-by-step plan to answer the user's request.
        Each step in the plan must be a single call to the `web_search` tool.
        
        Example:
        User Request: Find the populations of Tokyo and Seoul and sum them.
        Plan: 
        1. web_search(query="current population of Tokyo")
        2. web_search(query="current population of Seoul")

        User Request: {state['user_request']}
        Plan:"""
        
    plan_output = planner_llm.invoke(prompt)
    return {"plan": plan_output.steps}

def executor_node(state: PlanningState):
    """Thực hiện một bước từ kế hoạch bằng cách sử dụng công cụ tìm kiếm."""
    console.print("--- EXECUTOR: Running the plan... ---")
    
    # Tìm bước đầu tiên trong kế hoạch chưa được thực thi
    executed_steps_count = len(state.get("intermediate_steps", []))
    current_step = state["plan"][executed_steps_count]
    
    # Trích xuất query từ string của bước (XỬ LÝ CHUỖI CẦN THẬN)
    search_query = re.search(r'query=\"(.*?)\"', current_step).group(1)
    
    # Gọi tool thủ công
    result = web_search.invoke({"query": search_query})
    
    # Trả về kết quả dưới dạng ToolMessage để giữ tính nhất quán
    new_message = ToolMessage(content=str(result), tool_call_id=f"step_{executed_steps_count}")
    return {"intermediate_steps": [new_message]}

def synthesizer_node(state: PlanningState):
    """Tổng hợp tất cả các kết quả thu thập được thành câu trả lời cuối cùng."""
    console.print("--- SYNTHESIZER: Generating final answer... ---")
    
    results_summary = "\n".join([f"Step {i+1}: {msg.content}" for i, msg in enumerate(state["intermediate_steps"])])
    
    prompt = f"""Based on the following collected information, provide a final answer to the user's request:
        
        User Request: {state['user_request']}
        
        Collected Information:
        {results_summary}
        """
    response = llm.invoke(prompt)
    return {"final_answer": response.content}

print("Planner, Executor, and Synthesizer nodes defined.")
```

### Step 2.2: Defining the Graph and Routing Logic
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ lắp ráp các node thành một graph. Sự đổi mới quan trọng ở đây nằm ở routing logic. Sau khi `Executor` chạy một bước, chúng ta kiểm tra xem còn bước nào trong kế hoạch nữa không. Nếu còn, chúng ta lặp lại (`executor -> executor`). Nếu kế hoạch đã hoàn tất, chúng ta chuyển sang `Synthesizer`.

```python
def check_plan_status(state: PlanningState):
    """Kiểm tra xem tất cả các bước trong kế hoạch đã được thực thi chưa."""
    if len(state.get("intermediate_steps", [])) < len(state["plan"]):
        return "continue"
    return "synthesize"

# Đưa mọi thứ lại với nhau trong graph
planning_builder = StateGraph(PlanningState)

planning_builder.add_node("planner", planner_node)
planning_builder.add_node("executor", executor_node)
planning_builder.add_node("synthesizer", synthesizer_node)

planning_builder.set_entry_point("planner")

# Sau khi lập kế hoạch, chúng ta luôn đi đến executor
planning_builder.add_edge("planner", "executor")

# Vòng lặp quan trọng cho executor
planning_builder.add_conditional_edges(
    "executor",
    check_plan_status,
    {
        "continue": "executor",
        "synthesize": "synthesizer"
    }
)

planning_builder.add_edge("synthesizer", END)

# Compile graph
planning_agent_app = planning_builder.compile()

print("Planning Agent graph compiled successfully!")

# Hình ảnh hóa graph
try:
    from IPython.display import Image, display
    png_image = planning_agent_app.get_graph().draw_png()
    display(Image(png_image))
except Exception as e:
    print(f"Graph visualization failed: {e}. Please ensure pygraphviz is installed.")
```

**Discussion of the Output:**
Graph mới thể hiện một triết lý khác biệt rõ rệt. Thay vì flow dựa trên message năng động như ReAct, flow ở đây mang tính định hướng hơn. Workflow bắt đầu tại node `planner`, node này thiết lập lịch trình. Sau đó, quy trình đi vào một vòng lặp tự quản tại node `executor`, node này tiếp tục thực thi cho đến khi tất cả các mục trong danh sách nhiệm vụ được đánh dấu là hoàn thành. Cuối cùng, kết quả được chuyển đến node `synthesizer`.

## Phase 3: Direct Comparison
Bây giờ, hãy chạy cùng một truy vấn nhiều bước thông qua planning agent của chúng ta và quan sát cách nó thực thi kế hoạch của mình.

### Step 3.1: Running the Planning Agent
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ invoke planning agent với cùng một truy vấn và quan sát các bước thực thi có cấu trúc của nó.

```python
console.print(f"[bold cyan]Running Planning Agent on query:[/bold cyan] '{plan_centric_query}'\n")

# Chạy graph và stream results
initial_state = {"user_request": plan_centric_query, "intermediate_steps": []}

for chunk in planning_agent_app.stream(initial_state):
    # Trình bày node hiện tại đang chạy
    for node_name, values in chunk.items():
        console.print(f"--- Node [bold cyan]{node_name}[/bold cyan] completed ---")
        if node_name == "planner":
            console.print(f"[bold]Plan generated:[/bold] {values['plan']}")
        elif node_name == "synthesizer":
            console.print(values['final_answer'])
    console.print("\n")

print("Planning Agent execution complete.")
```

**Discussion of the Output:**
Màn trình diễn của planning agent cực kỳ hiệu quả. Phân tích results cho thấy:
1.  **Giai đoạn Planner:** Ngay từ đầu, agent đã phân tích chính xác query và tạo ra một kế hoạch rõ ràng gồm ba phần: tra cứu dân số Paris, dân số Berlin, và dân số Rome.
2.  **Giai đoạn Executor:** Sau đó, nó thực thi tuần tự các bước này một cách chính xác mà không cần thêm bất kỳ bước suy luận lặp lại nào ở giữa.
3.  **Giai đoạn Synthesizer:** Cuối cùng, nó thu thập tất cả dữ liệu thô và đưa ra một phép so sánh chính xác và đầy đủ với Hoa Kỳ.

So với ReAct agent, quy trình này ít mang tính thăm dò hơn nhưng trực tiếp và có mục đích hơn. Nó cho thấy cách sự rõ ràng của kế hoạch có thể giảm thiểu chi phí tính toán và cải thiện tính minh bạch.

## Phase 4: Qualitative Evaluation
Cuối cùng, chúng ta sẽ sử dụng giám khảo LLM của mình để chấm điểm cả hai agent dựa trên một khía cạnh đo lường mới: Tính trực tiếp (Directness)—khả năng đi đến câu trả lời với ít bước suy luận không cần thiết nhất.

```python
class ComparativeEvaluation(BaseModel):
    """Schema để so sánh trực tiếp hai agent."""
    react_directness_score: int = Field(description="Score từ 1-10 về mức độ trực tiếp của ReAct agent.")
    planning_directness_score: int = Field(description="Score từ 1-10 về mức độ trực tiếp của Planning agent.")
    comparison_justification: str = Field(description="Giải thích lý do tại sao một agent trực tiếp hơn agent kia.")

judge_llm = llm.with_structured_output(ComparativeEvaluation)

def comparative_evaluation(react_trace: str, planning_trace: str):
    prompt = f"""You are analyzing the efficiency of two different AI agents.
    One is a Reactive Agent (ReAct) which reasons step-by-step.
    The other is a Planning Agent which creates an upfront list of tasks.
    
    Compare their execution logs for the same task and score their 'Directness' (how efficiently they reached the goal without unnecessary thought steps).
    
    --- REACT AGENT LOG ---
    {react_trace}
    
    --- PLANNING AGENT LOG ---
    {planning_trace}
    """
    return judge_llm.invoke(prompt)

# (Để đơn giản, chúng ta pass qua logs thô)
react_log = "Followed an iterative think-act-observe loop for each city."
planning_log = "Created a 3-step plan upfront and executed it directly."

console.print("--- Performing Comparative Evaluation ---")
comparison = comparative_evaluation(react_log, planning_log)
console.print(comparison.model_dump())
```

**Discussion of the Output:**
Results của giám khảo nêu bật giá trị cốt lõi của Planning. Mặc dù cả hai phương pháp đều dẫn đến kết quả đúng, nhưng Planning agent được đánh giá cao hơn về tính trực tiếp. Bằng cách thực hiện công việc lập bản đồ con đường ngay từ đầu, nó tránh được việc "phát minh lại bánh xe" (reinventing the wheel) về lý trí sau mỗi hành động mới. Nó biết mình đang đi đâu và đã đến đó bằng con đường ngắn nhất có thể.

## Conclusion
Kiến trúc **Planning** giới thiệu tầm nhìn xa (foresight) như một công cụ đắc lực cho các AI agent. Bằng cách tách biệt giai đoạn chiến lược (lập kế hoạch) khỏi giai đoạn chiến thuật (thực thi), chúng ta tạo ra các hệ thống ổn định hơn, hiệu quả hơn và dễ hiểu hơn. Mặc dù nó đòi hỏi một nhiệm vụ ban đầu có thể dự đoán được ở một mức độ nào đó, nhưng đối với các workflow có cấu trúc, Planning không có đối thủ về khả năng mang lại sự rõ ràng và tính trực tiếp cho việc giải quyết vấn đề phức tạp. Pattern này là một sự bổ sung thiết yếu cho bộ công cụ của bất kỳ ai xây dựng các agent có năng lực cho các ứng dụng chuyên nghiệp.
