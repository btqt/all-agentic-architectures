# 📘 Agentic Architectures 4: Planning - Quy trình Lập kế hoạch

Trong notebook này, chúng ta sẽ khám phá kiến trúc **Planning**. Pattern này giới thiệu một lớp dự phòng (foresight) quan trọng vào quy trình suy luận của Agent. Thay vì phản ứng với thông tin theo từng bước như trong mô hình ReAct, một Planning Agent trước tiên sẽ phân tách một nhiệm vụ phức tạp thành một chuỗi các mục tiêu phụ (sub-goals) nhỏ hơn, có thể quản lý được. Nó tạo ra một "kế hoạch tác chiến" (battle plan) đầy đủ _trước khi_ thực hiện bất kỳ hành động nào.

Cách tiếp cận chủ động này mang lại sự cấu trúc, khả năng dự đoán và hiệu quả cho các nhiệm vụ gồm nhiều bước. Để làm nổi bật các lợi ích của nó, chúng ta sẽ so sánh trực tiếp hiệu suất của một **Reactive Agent (ReAct)** với **Planning Agent** mới của chúng ta. Chúng ta sẽ giao cho cả hai một nhiệm vụ yêu cầu thu thập nhiều mẩu thông tin trước khi thực hiện tính toán cuối cùng, minh chứng cách một kế hoạch được tính toán trước có thể dẫn đến một giải pháp mạnh mẽ và trực tiếp hơn.

### Definition: Định nghĩa

Kiến trúc **Planning** bao gồm một Agent thực hiện việc chia nhỏ một mục tiêu phức tạp thành một chuỗi các Sub-task chi tiết một cách rõ ràng _trước khi_ bắt đầu thực thi. Đầu ra của giai đoạn lập kế hoạch ban đầu này là một bản kế hoạch cụ thể, từng bước một mà Agent sau đó sẽ tuân thủ một cách có phương pháp để đạt được giải pháp.

### High-level Workflow: Quy trình cấp cao

1.  **Receive Goal (Nhận mục tiêu):** Agent được giao một nhiệm vụ phức tạp.
2.  **Plan (Lập kế hoạch):** Một thành phần 'Planner' chuyên dụng phân tích mục tiêu và tạo ra một danh sách các Sub-task có thứ tự cần thiết để đạt được mục tiêu đó. Ví dụ: `["Tìm dữ kiện A", "Tìm dữ kiện B", "Tính toán C bằng A và B"]`.
3.  **Execute (Thực thi):** Một thành phần 'Executor' nhận kế hoạch và thực hiện từng Sub-task theo thứ tự, sử dụng các công cụ khi cần thiết.
4.  **Synthesize (Tổng hợp):** Sau khi tất cả các bước trong kế hoạch hoàn tất, một thành phần cuối cùng sẽ tổng hợp các kết quả từ các bước đã thực thi thành một câu trả lời cuối cùng mạch lạc.

### When to Use / Applications: Khi nào nên sử dụng / Ứng dụng

- **Multi-Step Workflows (Quy trình nhiều bước):** Lý tưởng cho các nhiệm vụ mà trình tự hoạt động đã được biết trước và mang tính quyết định, chẳng hạn như tạo báo cáo yêu cầu lấy dữ liệu, xử lý dữ liệu và sau đó tóm tắt dữ liệu đó.
- **Project Management Assistants (Trợ lý quản lý dự án):** Phân tách một mục tiêu lớn như "ra mắt tính năng mới" thành các Sub-task cho các nhóm khác nhau.
- **Educational Tutoring (Gia sư giáo dục):** Tạo kế hoạch bài giảng để dạy học sinh một khái niệm cụ thể, từ các nguyên lý cơ bản đến ứng dụng nâng cao.

### Strengths & Weaknesses: Điểm mạnh & Điểm yếu

- **Strengths (Điểm mạnh):**
  - **Structured & Traceable (Có cấu trúc & Có thể truy vết):** Toàn bộ quy trình được vạch ra trước, giúp quy trình của Agent trở nên minh bạch và dễ dàng debug.
  - **Efficient (Hiệu quả):** Có thể hiệu quả hơn ReAct đối với các nhiệm vụ có thể dự đoán được, vì nó tránh được các vòng lặp suy luận không cần thiết giữa các bước.
- **Weaknesses (Điểm yếu):**
  - **Brittle to Change (Dễ gãy trước sự thay đổi):** Một kế hoạch được chuẩn bị trước có thể thất bại nếu môi trường thay đổi bất ngờ trong khi thực thi. Nó ít có khả năng thích ứng hơn so với một ReAct Agent - vốn có thể thay đổi quyết định sau mỗi bước.

---

## Phase 0: Foundation & Setup - Nền tảng & Cài đặt

Chúng ta sẽ bắt đầu với quy trình thiết lập tiêu chuẩn: cài đặt các thư viện và cấu hình API key cho Nebius, LangSmith và công cụ tìm kiếm web Tavily của chúng ta.

### Step 0.1: Installing Core Libraries - Cài đặt các thư viện cốt lõi

**Chúng ta sẽ làm gì:**
Chúng ta sẽ cài đặt bộ thư viện tiêu chuẩn, bao gồm gói `langchain-tavily` đã cập nhật để giải quyết cảnh báo lỗi thời (deprecation warning).

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv langchain-tavily
```

### Step 0.2: Importing Libraries and Setting Up Keys - Nhập thư viện và thiết lập Key

**Chúng ta sẽ làm gì:**
Chúng ta sẽ nhập các module cần thiết và tải các API key từ file `.env`.

**Yêu cầu hành động:** Tạo một file `.env` trong thư mục này với các key của bạn:

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

# --- Thiết lập API Key và Tracing ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Planning (Nebius)"

# Kiểm tra xem các key đã được thiết lập chưa
for key in ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]:
    if not os.environ.get(key):
        print(f"{key} không tìm thấy. Vui lòng tạo file .env và thiết lập nó.")

print("Các biến môi trường đã được tải và tracing đã được thiết lập.")
```

---

## Phase 1: The Baseline - Một Agent 'Phản ứng' (ReAct)

Để đánh giá đúng giá trị của Planning, trước tiên chúng ta cần một mức cơ sở (baseline). Chúng ta sẽ sử dụng ReAct Agent mà chúng ta đã xây dựng trong notebook trước. Agent này thông minh nhưng có tầm nhìn hẹp - nó tìm ra lộ trình của mình theo từng bước một.

### Step 1.1: Re-building the ReAct Agent - Xây dựng lại ReAct Agent

**Chúng ta sẽ làm gì:**
Chúng ta sẽ nhanh chóng tái cấu trúc ReAct Agent. Tính năng cốt lõi của nó là một vòng lặp nơi đầu ra của Agent được định tuyến quay lại chính nó sau mỗi lần gọi công cụ, cho phép nó đánh giá lại và quyết định bước tiếp theo dựa trên thông tin mới nhất.

```python
console = Console()

# Định nghĩa trạng thái cho các graph của chúng ta
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# 1. Định nghĩa công cụ cơ sở từ gói tavily
tavily_search_tool = TavilySearch(max_results=2)

# 2. GIẢI PHÁP: Đơn giản hóa công cụ tùy chỉnh.
#    Phương thức .invoke() đã trả về một chuỗi sạch, vì vậy chúng ta chỉ cần chuyển tiếp nó.
@tool
def web_search(query: str) -> str:
    """Thực hiện tìm kiếm web bằng Tavily và trả về kết quả dưới dạng chuỗi."""
    console.print(f"--- TOOL: Đang tìm kiếm cho '{query}'...")
    results = tavily_search_tool.invoke(query)
    return results

# 3. Định nghĩa LLM và liên kết nó với công cụ tùy chỉnh của chúng ta
llm = ChatNebius(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)
llm_with_tools = llm.bind_tools([web_search])

# 4. Agent node với một system prompt để buộc thực hiện mỗi lần một lệnh gọi công cụ
def react_agent_node(state: AgentState):
    console.print("--- REACTIVE AGENT: Đang suy nghĩ... ---")

    messages_with_system_prompt = [
        SystemMessage(content="Bạn là một trợ lý nghiên cứu hữu ích. Bạn phải gọi một và chỉ một công cụ tại một thời điểm. Không gọi nhiều công cụ trong một lượt duy nhất. Sau khi nhận được kết quả từ một công cụ, bạn sẽ quyết định bước tiếp theo.")
    ] + state["messages"]

    response = llm_with_tools.invoke(messages_with_system_prompt)

    return {"messages": [response]}

# 5. Sử dụng công cụ tùy chỉnh đã sửa lỗi trong ToolNode
tool_node = ToolNode([web_search])

# ReAct graph với vòng lặp đặc trưng của nó
react_graph_builder = StateGraph(AgentState)
react_graph_builder.add_node("agent", react_agent_node)
react_graph_builder.add_node("tools", tool_node)
react_graph_builder.set_entry_point("agent")
react_graph_builder.add_conditional_edges("agent", tools_condition)
react_graph_builder.add_edge("tools", "agent")

react_agent_app = react_graph_builder.compile()
print("Reactive (ReAct) agent đã được biên dịch thành công.")
```

### Step 1.2: Testing the Reactive Agent on a Plan-Centric Problem - Kiểm tra Reactive Agent trên một bài toán tập trung vào lập kế hoạch

**Chúng ta sẽ làm gì:**
Chúng ta sẽ giao cho ReAct Agent một nhiệm vụ yêu cầu hai bước thu thập dữ liệu riêng biệt, theo sau là một phép tính cuối cùng. Điều này sẽ kiểm tra khả năng quản lý một quy trình nhiều bước mà không có kế hoạch trả trước của nó.

```python
plan_centric_query = """
Tìm dân số của các thành phố thủ đô của Pháp, Đức và Ý.
Sau đó tính tổng dân số kết hợp của chúng.
Cuối cùng, so sánh tổng đó với dân số của Hoa Kỳ và cho biết cái nào lớn hơn.
"""

console.print(f"[bold yellow]Đang kiểm tra REACTIVE agent với truy vấn tập trung vào lập kế hoạch:[/bold yellow] '{plan_centric_query}'\n")

final_react_output = None
for chunk in react_agent_app.stream({"messages": [("user", plan_centric_query)]}, stream_mode="values"):
    final_react_output = chunk
    console.print(f"--- [bold purple]Cập nhật trạng thái hiện tại[/bold purple] ---")
    chunk['messages'][-1].pretty_print()
    console.print("\n")

console.print("\n--- [bold red]Đầu ra cuối cùng từ Reactive Agent[/bold red] ---")
console.print(Markdown(final_react_output['messages'][-1].content))
```

**Discussion of the Output: Thảo luận về kết quả**
ReAct Agent đã hoàn thành thành công nhiệm vụ. Bằng cách quan sát đầu ra được stream, chúng ta có thể truy vết quy trình suy luận từng bước của nó:

1. Đầu tiên, nó quyết định tìm kiếm dân số của Paris.
2. Sau khi nhận kết quả đó, nó đưa thông tin vào bộ nhớ và sau đó quyết định bước tiếp theo là tìm kiếm dân số của Berlin.
3. Cuối cùng, với cả hai mẩu thông tin đã thu thập được, nó thực hiện tính toán và đưa ra câu trả lời cuối cùng.

Mặc dù nó hoạt động, quy trình khám phá lặp lại này không phải lúc nào cũng hiệu quả nhất. Đối với một nhiệm vụ có thể đoán trước như thế này, Agent đang thực hiện thêm các lệnh gọi LLM để suy luận giữa mỗi bước. Điều này tạo tiền đề cho việc trình diễn giá trị của một Planning Agent.

---

## Phase 2: The Advanced Approach - Một Agent Lập kế hoạch (Planning Agent)

Bây giờ, hãy xây dựng một Agent biết suy nghĩ trước khi hành động. Agent này sẽ có một **Planner** chuyên dụng để tạo danh sách nhiệm vụ hoàn chỉnh, một **Executor** để thực hiện kế hoạch và một **Synthesizer** để lắp ráp kết quả cuối cùng.

### Step 2.1: Defining the Planner, Executor, and Synthesizer Nodes - Định nghĩa các Node Planner, Executor và Synthesizer

**Chúng ta sẽ làm gì:**
Chúng ta sẽ tạo các thành phần cốt lõi cho Agent mới của mình:

1.  **`Planner`:** Một Node dựa trên LLM nhận yêu cầu của người dùng và xuất ra một bản kế hoạch có cấu trúc.
2.  **`Executor`:** Một Node nhận kế hoạch, thực hiện bước _tiếp theo_ bằng một công cụ và ghi lại kết quả.
3.  **`Synthesizer`:** Một Node dựa trên LLM cuối cùng nhận tất cả các kết quả đã thu thập và tạo ra câu trả lời cuối cùng.

```python
# Pydantic model để đảm bảo đầu ra của planner là một danh sách các bước có cấu trúc
class Plan(BaseModel):
    """Một kế hoạch gồm các lệnh gọi công cụ để thực thi nhằm trả lời truy vấn của người dùng."""
    steps: List[str] = Field(description="Một danh sách các lệnh gọi công cụ mà khi thực hiện sẽ trả lời được truy vấn.")

# Định nghĩa trạng thái cho planning agent
class PlanningState(TypedDict):
    user_request: str
    plan: Optional[List[str]]
    intermediate_steps: List[ToolMessage]
    final_answer: Optional[str]

def planner_node(state: PlanningState):
    """Tạo ra một bản kế hoạch hành động để trả lời yêu cầu của người dùng."""
    console.print("--- PLANNER: Đang phân tách nhiệm vụ... ---")
    planner_llm = llm.with_structured_output(Plan)

    # GIẢI PHÁP: Một prompt rõ ràng hơn nhiều với ví dụ cụ thể (few-shot prompting)
    prompt = f"""Bạn là một chuyên gia lập kế hoạch. Công việc của bạn là tạo ra một kế hoạch từng bước để trả lời yêu cầu của người dùng.
        Mỗi bước trong kế hoạch phải là một lệnh gọi duy nhất đến công cụ `web_search`.

        **Hướng dẫn:**
        1. Phân tích yêu cầu của người dùng.
        2. Chia nhỏ nó thành một chuỗi các truy vấn tìm kiếm đơn giản, logic.
        3. Định dạng đầu ra dưới dạng một danh sách các chuỗi, trong đó mỗi chuỗi là một lệnh gọi công cụ hợp lệ duy nhất.

        **Ví dụ:**
        Yêu cầu: "Thủ đô của Pháp là gì và dân số của nó là bao nhiêu?"
        Đầu ra kế hoạch đúng:
        [
            "web_search('thủ đô của Pháp')",
            "web_search('dân số của Paris')"
        ]

        **Yêu cầu của người dùng:**
        {state['user_request']}
    """

    plan_result = planner_llm.invoke(prompt)
    # Sử dụng plan_result.steps để tránh nhầm lẫn với tên biến 'plan'
    console.print(f"--- PLANNER: Kế hoạch đã tạo: {plan_result.steps} ---")
    return {"plan": plan_result.steps}

def executor_node(state: PlanningState):
    """Thực hiện bước tiếp theo trong kế hoạch."""
    console.print("--- EXECUTOR: Đang chạy bước tiếp theo... ---")
    plan = state["plan"]
    next_step = plan[0]

    # Regex mạnh mẽ để xử lý cả dấu ngoặc đơn và ngoặc kép
    match = re.search(r"(\w+)\((?:\"|\')(.*?)(?:\"|\')\)", next_step)
    if not match:
        tool_name = "web_search"
        query = next_step
    else:
        tool_name, query = match.groups()[0], match.groups()[1]

    console.print(f"--- EXECUTOR: Đang gọi công cụ '{tool_name}' với truy vấn '{query}' ---")

    result = tavily_search_tool.invoke(query)

    # Chúng ta vẫn tạo ToolMessage, nhưng bản thân lệnh gọi công cụ hiện đã an toàn.
    tool_message = ToolMessage(
    content=str(result),
    name=tool_name,
    tool_call_id=f"manual-{hash(query)}"
    )

    return {
        "plan": plan[1:], # Lấy bước đã thực thi ra khỏi kế hoạch
        "intermediate_steps": state["intermediate_steps"] + [tool_message]
    }

def synthesizer_node(state: PlanningState):
    """Tổng hợp câu trả lời cuối cùng từ các bước trung gian."""
    console.print("--- SYNTHESIZER: Đang tạo câu trả lời cuối cùng... ---")

    context = "\n".join([f"Tool {msg.name} trả về: {msg.content}" for msg in state["intermediate_steps"]])

    prompt = f"""Bạn là một chuyên gia tổng hợp. Dựa trên yêu cầu của người dùng và dữ liệu đã thu thập, hãy cung cấp một câu trả lời cuối cùng toàn diện.

    Yêu cầu: {state['user_request']}
    Dữ liệu đã thu thập:
    {context}
    """
    final_answer = llm.invoke(prompt).content
    return {"final_answer": final_answer}

print("Các Node Planner, Executor và Synthesizer đã được định nghĩa.")
```

### Step 2.2: Building the Planning Agent Graph - Xây dựng Graph cho Planning Agent

**Chúng ta sẽ làm gì:**
Bây giờ chúng ta sẽ lắp ráp các Node mới vào một Graph. Luồng sẽ là: `Planner` -> `Executor` (looped) -> `Synthesizer`.

```python
def planning_router(state: PlanningState):
    if not state["plan"]:
        console.print("--- ROUTER: Kế hoạch hoàn tất. Chuyển sang synthesizer. ---")
        return "synthesize"
    else:
        console.print("--- ROUTER: Kế hoạch còn các bước khác. Tiếp tục thực thi. ---")
        return "execute"

planning_graph_builder = StateGraph(PlanningState)
planning_graph_builder.add_node("plan", planner_node)
planning_graph_builder.add_node("execute", executor_node)
planning_graph_builder.add_node("synthesize", synthesizer_node)

planning_graph_builder.set_entry_point("plan")
planning_graph_builder.add_conditional_edges("plan", planning_router, {"execute": "execute", "synthesize": "synthesize"}) # Định tuyến sau khi lập kế hoạch
planning_graph_builder.add_conditional_edges("execute", planning_router, {"execute": "execute", "synthesize": "synthesize"})
planning_graph_builder.add_edge("synthesize", END)

planning_agent_app = planning_graph_builder.compile()
print("Planning agent đã được biên dịch thành công.")
```

---

## Phase 3: Head-to-Head Comparison - So sánh đối đầu

Hãy chạy Planning Agent mới của chúng ta trên cùng một nhiệm vụ và so sánh luồng thực thi cũng như đầu ra cuối cùng của nó với Reactive Agent.

```python
console.print(f"[bold green]Đang kiểm tra PLANNING agent trên cùng một truy vấn tập trung vào lập kế hoạch:[/bold green] '{plan_centric_query}'\n")

# Nhớ khởi tạo trạng thái chính xác, đặc biệt là danh sách cho các bước trung gian
initial_planning_input = {"user_request": plan_centric_query, "intermediate_steps": []}

final_planning_output = planning_agent_app.invoke(initial_planning_input)

console.print("\n--- [bold green]Đầu ra cuối cùng từ Planning Agent[/bold green] ---")
console.print(Markdown(final_planning_output['final_answer']))
```

**Discussion of the Output: Thảo luận về kết quả**
Sự khác biệt trong quy trình là rõ ràng ngay lập tức. Bước đầu tiên chính là `Planner` tạo ra một bản kế hoạch hoàn chỉnh, rõ ràng: `['web_search("dân số Paris")', 'web_search("dân số Berlin")']`.

Agent sau đó thực hiện kế hoạch này một cách có phương pháp mà không cần dừng lại để suy nghĩ giữa các bước. Quy trình này:

- **More Transparent (Minh bạch hơn):** Chúng ta có thể thấy toàn bộ chiến lược của Agent trước khi nó bắt đầu.
- **More Robust (Mạnh mẽ hơn):** Nó ít có khả năng bị lạc hướng vì nó đang tuân theo một bộ chỉ dẫn rõ ràng.
- **Potentially More Efficient (Tiềm năng hiệu quả hơn):** Nó tránh được các lệnh gọi LLM bổ sung để suy luận giữa các bước.

Điều này chứng minh sức mạnh của việc lập kế hoạch cho các nhiệm vụ mà các bước yêu cầu có thể được xác định trước.

---

## Phase 4: Quantitative Evaluation - Đánh giá định lượng

Để chính thức hóa việc so sánh của chúng ta, chúng ta sẽ sử dụng một LLM-as-a-Judge (LLM làm giám khảo) để chấm điểm cả hai Agent, tập trung vào chất lượng và hiệu quả của quy trình giải quyết vấn đề của chúng.

````python
class ProcessEvaluation(BaseModel):
    """Schema để đánh giá quy trình giải quyết vấn đề của một Agent."""
    task_completion_score: int = Field(description="Điểm 1-10 về việc liệu Agent có hoàn thành nhiệm vụ thành công hay không.")
    process_efficiency_score: int = Field(description="Điểm 1-10 về hiệu quả và tính trực tiếp của quy trình của Agent. Điểm cao hơn có nghĩa là lộ trình logic hơn và ít vòng vo hơn.")
    justification: str = Field(description="Một lời giải thích ngắn gọn cho các điểm số.")

judge_llm = llm.with_structured_output(ProcessEvaluation)

def evaluate_agent_process(query: str, final_state: dict):
    # Đối với ReAct agent, dấu vết nằm trong 'messages'. Đối với Planning, nó nằm trong 'intermediate_steps'.
    if 'messages' in final_state:
        trace = "\n".join([f"{m.type}: {str(m.content)}" for m in final_state['messages']])
    else:
        trace = f"Plan: {final_state.get('plan', [])}\nSteps: {final_state.get('intermediate_steps', [])}"

    prompt = f"""Bạn là một giám khảo chuyên gia về các AI agent. Hãy đánh giá quy trình giải quyết nhiệm vụ của Agent trên thang điểm 1-10.
    Tập trung vào việc liệu quy trình có logic và hiệu quả hay không.

    **Nhiệm vụ của người dùng:** {query}
    **Dấu vết đầy đủ của Agent:**\n```\n{trace}\n```
    """
    return judge_llm.invoke(prompt)

console.print("--- Đang đánh giá quy trình của Reactive Agent ---")
react_agent_evaluation = evaluate_agent_process(plan_centric_query, final_react_output)
console.print(react_agent_evaluation.model_dump())

console.print("\n--- Đang đánh giá quy trình của Planning Agent ---")
planning_agent_evaluation = evaluate_agent_process(plan_centric_query, final_planning_output)
console.print(planning_agent_evaluation.model_dump())
````

**Discussion of the Output: Thảo luận về kết quả**
Điểm số của giám khảo định lượng sự khác biệt trong hai cách tiếp cận. Cả hai Agent có khả năng nhận được `task_completion_score` cao vì cả hai cuối cùng đều tìm ra câu trả lời. Tuy nhiên, **Planning Agent** sẽ nhận được `process_efficiency_score` cao hơn đáng kể. Lời giải thích của giám khảo sẽ nêu bật rằng kế hoạch trả trước của nó là một cách trực tiếp và logic hơn để giải quyết vấn đề so với quy trình khám phá từng bước của ReAct Agent.

Đánh giá này xác nhận giả thuyết của chúng ta: đối với các bài toán có con đường giải quyết có thể dự đoán được, kiến trúc Planning cung cấp một cách tiếp cận có cấu trúc, minh bạch và hiệu quả hơn.

---

## Conclusion: Kết luận

Trong notebook này, chúng ta đã triển khai kiến trúc **Planning** và đối chiếu nó trực tiếp với mẫu **ReAct**. Bằng cách buộc một Agent trước tiên phải xây dựng một kế hoạch toàn diện trước khi thực thi, chúng ta thu được những lợi ích đáng kể về tính minh bạch, tính mạnh mẽ và hiệu quả cho các nhiệm vụ gồm nhiều bước đã được xác định rõ ràng.

Trong khi ReAct xuất sắc trong các kịch bản khám phá nơi bước tiếp theo chưa được biết rõ, thì Planning tỏa sáng khi con đường đi tới giải pháp có thể được vạch ra trước. Hiểu được sự đánh đổi này là rất quan trọng đối với một nhà thiết kế hệ thống. Chọn lựa đúng kiến trúc cho đúng vấn đề là một kỹ năng then chốt trong việc xây dựng các AI Agent hiệu quả và thông minh. Pattern Planning là một công cụ thiết yếu trong bộ công cụ đó, cung cấp cấu trúc cần thiết cho các quy trình phức tạp và có thể dự đoán được.
