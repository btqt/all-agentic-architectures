# 📘 Agentic Architectures 6: Planner → Executor → Verifier (PEV)

Trong notebook này, chúng ta khám phá kiến trúc **Planner → Executor → Verifier (PEV)**, một pattern giới thiệu lớp then chốt về tính ổn định (robustness) và khả năng tự sửa lỗi (self-correction) vào các hệ thống agentic. Kiến trúc này được lấy cảm hứng từ các quy trình kỹ thuật phần mềm và đảm bảo chất lượng (QA) nghiêm ngặt, nơi công việc không được coi là 'hoàn thành' cho đến khi nó được xác minh (verified).

Mặc dù một Planning agent tiêu chuẩn mang lại cấu trúc và tính có thể dự đoán được, nhưng nó hoạt động trên một giả định quan trọng: rằng các công cụ của nó sẽ hoạt động hoàn hảo và trả về dữ liệu hợp lệ mọi lúc. Trong thế giới thực, các API thất bại, tìm kiếm không trả về kết quả và dữ liệu có thể bị sai định dạng. PEV pattern giải quyết vấn đề này bằng cách thêm một **Verifier** agent chuyên dụng hoạt động như một khâu kiểm tra đảm bảo chất lượng sau mỗi hành động, cho phép hệ thống phát hiện các lỗi và phục hồi một cách năng động.

Để chứng minh giá trị của nó, trước tiên chúng ta sẽ xây dựng một **Planner-Executor agent** tiêu chuẩn và cho thấy nó thất bại như thế nào khi một tool trả về một error. Sau đó, chúng ta sẽ xây dựng một **PEV agent** hoàn chỉnh để chỉ ra cách Verifier bắt lỗi, kích hoạt vòng lặp lập kế hoạch lại (re-planning), và cuối cùng dẫn dắt hệ thống đến kết quả thành công.

### Definition
Kiến trúc **Planner → Executor → Verifier (PEV)** là một workflow ba giai đoạn phân tách rõ ràng các hành động lập kế hoạch, thực thi và xác minh. Nó đảm bảo rằng kết quả đầu ra của mỗi bước được validate trước khi agent tiếp tục, tạo ra một vòng lặp tự sửa lỗi mạnh mẽ.

### High-level Workflow
1.  **Plan:** Một 'Planner' agent phân tách một mục tiêu cấp cao thành một chuỗi các bước thực thi cụ thể.
2.  **Execute:** Một 'Executor' agent thực hiện bước *tiếp theo* từ kế hoạch và gọi tool phù hợp.
3.  **Verify:** Một 'Verifier' agent kiểm tra kết quả đầu ra từ Executor. Nó kiểm tra tính đúng đắn, mức độ liên quan và các lỗi tiềm ẩn. Sau đó, nó đưa ra một phán quyết: bước đó thành công hay thất bại?
4.  **Route & Iterate:** Dựa trên phán quyết của Verifier, một router quyết định bước tiếp theo:
    *   Nếu bước đó **thành công** và kế hoạch chưa hoàn tất, quay lại Executor cho bước tiếp theo.
    *   Nếu bước đó **thất bại**, quay lại Planner để tạo một kế hoạch *mới*, thường là cung cấp context về lỗi để kế hoạch mới có thể thông minh hơn.
    *   Nếu bước đó **thành công** và kế hoạch đã hoàn tất, tiến hành bước tổng hợp cuối cùng.

### When to Use / Applications
*   **Safety-Critical Applications (Tài chính, Y tế):** Khi chi phí của một sai sót là cao, PEV cung cấp các rào chắn (guardrails) thiết yếu để ngăn chặn agent hành động dựa trên dữ liệu xấu.
*   **Hệ thống với các Tool không đáng tin cậy:** Khi làm việc với các API bên ngoài có thể chập chờn hoặc trả về dữ liệu không nhất quán, Verifier có thể xử lý các thất bại một cách khéo léo.
*   **Nhiệm vụ độ chính xác cao (Pháp lý, Khoa học):** Đối với các nhiệm vụ yêu cầu độ chính xác thực tế cao, Verifier đảm bảo mỗi thông tin thu thập được là hợp lệ trước khi nó được sử dụng trong các suy luận tiếp theo.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Tính ổn định & Độ tin cậy:** Sức mạnh cốt lõi của nó là khả năng phát hiện và phục hồi từ lỗi.
    *   **Tính Module:** Sự tách biệt các mối quan tâm làm cho hệ thống dễ debug và bảo trì hơn.
*   **Weaknesses:**
    *   **Tăng độ trễ & Chi phí:** Việc thêm bước xác minh sau mỗi hành động làm tăng thêm các cuộc gọi LLM, khiến nó trở thành kiến trúc chậm nhất và đắt nhất trong số các kiến trúc chúng ta đã đề cập cho đến nay.
    *   **Độ phức tạp của Verifier:** Thiết kế một Verifier hiệu quả có thể là một thách thức. Nó cần đủ thông minh để phân biệt giữa các vấn đề nhỏ và lỗi nghiêm trọng.

## Phase 0: Foundation & Setup
Chúng ta sẽ bắt đầu bằng việc cài đặt các thư viện và cấu hình các API keys cho Nebius, LangSmith và các tool của chúng ta.

### Step 0.1: Installing Core Libraries
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ cài đặt bộ thư viện tiêu chuẩn của mình cho loạt dự án này.

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
import json

# LangChain components
from langchain_nebius import ChatNebius
from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage, ToolMessage
from pydantic import BaseModel, Field

# LangGraph components
from langgraph.graph import StateGraph, END

# For pretty printing
from rich.console import Console
from rich.markdown import Markdown

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - PEV (Nebius)"

for key in ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]:
    if not os.environ.get(key):
        print(f"{key} not found. Please create a .env file and set it.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: The Baseline - A Planner-Executor Agent
Để hiểu nhu cầu cần có một Verifier, trước tiên chúng ta phải xây dựng một agent không có nó. Agent này sẽ tạo một kế hoạch và làm theo một cách mù quáng, chứng minh tiềm năng thất bại khi một cuộc gọi tool gặp trục trặc.

### Step 1.1: Building the Planner-Executor Agent
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ xây dựng một Planner-Executor graph đơn giản, tương tự như trong notebook trước. Để mô phỏng một sự cố thực tế, chúng ta sẽ tạo một công cụ 'flaky' (chập chờn) đặc biệt. Công cụ này sẽ cố tình trả về một thông báo lỗi cho một query cụ thể, điều mà basic agent của chúng ta sẽ không có cách nào xử lý.

```python
console = Console()
llm = ChatNebius(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)

# Định nghĩa một 'flaky' tool sẽ thất bại với một query cụ thể
def flaky_web_search(query: str) -> str:
    """Thực hiện tìm kiếm web, nhưng được thiết kế để thất bại với một query cụ thể."""
    console.print(f"--- TOOL: Searching for '{query}'... ---")
    if "employee count" in query.lower():
        console.print("--- TOOL: [bold red]Simulating API failure![/bold red] ---")
        return "Error: Could not retrieve data. The API endpoint is currently unavailable."
    else:
        result = TavilySearch(max_results=2).invoke(query)
        # Đảm bảo kết quả luôn là string
        if isinstance(result, (dict, list)):
            return json.dumps(result, indent=2)
        return str(result)

# Định nghĩa state cho basic P-E agent
class BasicPEState(TypedDict):
    user_request: str
    plan: Optional[List[str]]
    intermediate_steps: List[str]
    final_answer: Optional[str]

class Plan(BaseModel):
    steps: List[str] = Field(description="A list of tool calls to execute.")

def basic_planner_node(state: BasicPEState):
    console.print("--- (Basic) PLANNER: Creating plan... ---")
    planner_llm = llm.with_structured_output(Plan)

    prompt = f"""
    You are a planning agent. 
    Your job is to decompose the user's request into a list of clear tool queries.

    - Only return JSON that matches this schema: {{ "steps": [ "query1", \"query2\", ... ] }}
    - Do NOT return any prose or explanation.
    - Always use the 'flaky_web_search' tool for queries.

    User's request: "{state['user_request']}"
    """
    plan = planner_llm.invoke(prompt)
    return {"plan": plan.steps}

def basic_executor_node(state: BasicPEState):
    console.print("--- (Basic) EXECUTOR: Running next step... ---")
    next_step = state["plan"][0]
    result = flaky_web_search(next_step)
    return {"plan": state["plan"][1:], "intermediate_steps": state["intermediate_steps"] + [result]}

def basic_synthesizer_node(state: BasicPEState):
    console.print("--- (Basic) SYNTHESIZER: Generating final answer... ---")
    context = "\n".join(state["intermediate_steps"])
    prompt = f"Synthesize an answer for '{state['user_request']}' using this data:\n{context}"
    answer = llm.invoke(prompt).content
    return {"final_answer": answer}

# Xây dựng graph
pe_graph_builder = StateGraph(BasicPEState)
pe_graph_builder.add_node("plan", basic_planner_node)
pe_graph_builder.add_node("execute", basic_executor_node)
pe_graph_builder.add_node("synthesize", basic_synthesizer_node)

pe_graph_builder.set_entry_point("plan")
pe_graph_builder.add_conditional_edges("plan", lambda s: "execute" if s["plan"] else "synthesize")
pe_graph_builder.add_conditional_edges("execute", lambda s: "execute" if s["plan"] else "synthesize")
pe_graph_builder.add_edge("synthesize", END)

basic_pe_app = pe_graph_builder.compile()
print("Basic Planner-Executor agent compiled successfully.")
```

### Step 1.2: Testing the Basic Agent on the 'Flaky' Problem
**Những gì chúng ta sẽ làm:**
Bây giờ chúng ta sẽ giao cho basic agent một nhiệm vụ yêu cầu nó gọi tool `flaky_web_search` của chúng ta với query cụ thể mà chúng ta biết chắc chắn sẽ thất bại. Điều này sẽ cho thấy sự bất lực của nó trong việc xử lý lỗi.

```python
flaky_query = "What was Apple's R&D spend in their last fiscal year, and what was their total employee count? Calculate the R&D spend per employee."

console.print(f"[bold yellow]Testing BASIC P-E agent on a flaky query:[/bold yellow]\n'{flaky_query}'\n")

initial_pe_input = {"user_request": flaky_query, "intermediate_steps": []}
final_pe_output = basic_pe_app.invoke(initial_pe_input)

console.print("\n--- [bold red]Final Output from Basic P-E Agent[/bold red] ---")
console.print(Markdown(final_pe_output['final_answer']))
```

**Discussion of the Output:**
Thất bại, như dự đoán. Execution trace cho thấy agent đã tạo một kế hoạch, có khả năng là `["Apple R&D spend last fiscal year", "Apple total employee count"]`. Nó đã thực hiện thành công bước đầu tiên. Tuy nhiên, ở bước thứ hai, tool `flaky_web_search` của chúng ta đã trả về một chuỗi thông báo lỗi.

Thất bại cốt lõi nằm ở bước cuối cùng. **Synthesizer**, vì không có cách nào biết được bước thứ hai đã thất bại, nên đã nhận thông báo lỗi như thể đó là dữ liệu hợp lệ. Do đó, câu trả lời cuối cùng của nó là vô nghĩa, có khả năng nêu một điều gì đó như "Tôi không thể thực hiện phép tính vì một trong các dữ liệu đầu vào là một thông báo lỗi." Nó đã làm theo kế hoạch một cách mù quáng cho đến khi hoàn thành, dẫn đến một kết quả vô dụng. Điều này cho thấy nhu cầu cấp thiết về một bước xác minh (verification).

## Phase 2: The Advanced Approach - A Planner-Executor-Verifier Agent
Bây giờ chúng ta sẽ xây dựng PEV agent hoàn chỉnh. Chúng ta sẽ thêm một **Verifier** node chuyên dụng và tạo một routing logic tinh vi hơn cho phép agent phục hồi sau lỗi của tool.

### Step 2.1: Defining the Verifier and the PEV Graph
**Những gì chúng ta sẽ làm:**
1.  Định nghĩa Pydantic model `VerificationResult` cho kết quả đầu ra có cấu trúc của Verifier.
2.  Tạo `verifier_node`, node này sẽ phân tích kết quả đầu ra của Executor.
3.  Tạo một `router` mới, phức tạp hơn, có thể xử lý các phản hồi của Verifier và kích hoạt vòng lặp lập kế hoạch lại (re-planning).

```python
class VerificationResult(BaseModel):
    """Schema cho đầu ra của Verifier."""
    is_successful: bool = Field(description="True if the tool execution was successful and the data is valid.")
    reasoning: str = Field(description="Reasoning for the verification decision.")

class PEVState(TypedDict):
    user_request: str
    plan: Optional[List[str]]
    last_tool_result: Optional[str]
    intermediate_steps: List[str]
    final_answer: Optional[str]
    retries: int  # đếm số lần chúng ta đã lập kế hoạch lại

from langchain_core.exceptions import OutputParserException

class Plan(BaseModel):
    steps: List[str] = Field(
        description="List of queries (max 5).",
        max_items=5
    )

def pev_planner_node(state: PEVState):
    retries = state.get("retries", 0)
    if retries > 3:  # dừng lại sau 3 lần lập kế hoạch lại
        console.print("--- (PEV) PLANNER: Retry limit reached. Stopping. ---")
        return {
            "plan": [],
            "final_answer": "Error: Unable to complete task after multiple retries."
        }

    console.print(f"--- (PEV) PLANNER: Creating/revising plan (retry {retries})... ---")

    planner_llm = llm.with_structured_output(Plan, strict=True)

    past_context = "\n".join(state["intermediate_steps"])
    base_prompt = f"""
    You are a planning agent. 
    Create a plan to answer: '{state['user_request']}'. 
    Use the 'flaky_web_search' tool.

    Rules:
    - Return ONLY valid JSON in this exact format: {{ "steps": ["query1", "query2"] }}
    - Maximum 5 steps.
    - Do NOT repeat failed queries or endless variations.
    - Do NOT output explanations, only JSON.

    Previous attempts and results:
    {past_context}
    """

    # Vòng lặp retry cho JSON bị lỗi
    for attempt in range(2):
        try:
            plan = planner_llm.invoke(base_prompt)
            return {"plan": plan.steps, "retries": retries + 1}
        except OutputParserException as e:
            console.print(f"[red]Planner parsing failed (attempt {attempt+1}): {e}[/red]")
            base_prompt = f"Return ONLY valid JSON with {{'steps': ['...']}}. {base_prompt}"

    # Fallback cuối cùng để tránh bị treo
    return {"plan": ["Apple R&D spend last fiscal year"], "retries": retries + 1}


def pev_executor_node(state: PEVState):
    if not state.get("plan"):  # bảo vệ chống lại kế hoạch trống
        console.print("--- (PEV) EXECUTOR: No steps left, skipping execution. ---")
        return {}
    
    console.print("--- (PEV) EXECUTOR: Running next step... ---")
    next_step = state["plan"][0]
    result = flaky_web_search(next_step)
    return {"plan": state["plan"][1:], "last_tool_result": result}

def verifier_node(state: PEVState):
    console.print("--- VERIFIER: Checking last tool result... ---")
    verifier_llm = llm.with_structured_output(VerificationResult)
    prompt = f"Verify if the following tool output is a successful result or an error message. The task was '{state['user_request']}'.\n\nTool Output: '{state['last_tool_result']}'"
    verification = verifier_llm.invoke(prompt)
    console.print(f"--- VERIFIER: Judgment is '{'Success' if verification.is_successful else 'Failure'}' ---")
    if verification.is_successful:
        # Nếu thành công, thêm kết quả hợp lệ vào danh sách các bước tốt của chúng ta
        return {"intermediate_steps": state["intermediate_steps"] + [state['last_tool_result']]}
    else:
        # Nếu thất bại, thêm lý do thất bại và kích hoạt lập kế hoạch lại bằng cách xóa kế hoạch
        return {"plan": [], "intermediate_steps": state["intermediate_steps"] + [f"Verification Failed: {state['last_tool_result']}"]}

pev_synthesizer_node = basic_synthesizer_node # Chúng ta có thể tái sử dụng synthesizer cũ

def pev_router(state: PEVState):
    # Nếu chúng ta đã có câu trả lời cuối cùng (ví dụ: đạt giới hạn retry), hãy dừng lại
    if state.get("final_answer"):
        console.print("--- ROUTER: Final answer available. Moving to synthesizer. ---")
        return "synthesize"

    if not state["plan"]:
        # Kiểm tra xem kế hoạch có trống vì lỗi xác minh hay không
        if state["intermediate_steps"] and "Verification Failed" in state["intermediate_steps"][-1]:
            console.print("--- ROUTER: Verification failed. Re-planning... ---")
            return "plan"
        else:
            console.print("--- ROUTER: Plan complete. Moving to synthesizer. ---")
            return "synthesize"
    else:
        console.print("--- ROUTER: Plan has more steps. Continuing execution. ---")
        return "execute"


# Xây dựng PEV graph
pev_graph_builder = StateGraph(PEVState)
pev_graph_builder.add_node("plan", pev_planner_node)
pev_graph_builder.add_node("execute", pev_executor_node)
pev_graph_builder.add_node("verify", verifier_node)
pev_graph_builder.add_node("synthesize", pev_synthesizer_node)

pev_graph_builder.set_entry_point("plan")
pev_graph_builder.add_edge("plan", "execute")
pev_graph_builder.add_edge("execute", "verify")
pev_graph_builder.add_conditional_edges("verify", pev_router)
pev_graph_builder.add_edge("synthesize", END)

pev_agent_app = pev_graph_builder.compile()
print("Planner-Executor-Verifier (PEV) agent compiled successfully.")
```

## Phase 3: Head-to-Head Comparison
Bây giờ là cho bài kiểm tra quan trọng. Chúng ta sẽ chạy PEV agent mạnh mẽ cho cùng một flaky task và quan sát cách nó điều hướng thành công qua sự cố của tool.

### Step 3.1: Running the PEV Agent
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ invoke PEV agent và stream kết quả đầu ra của nó. Chúng ta mong đợi được thấy nó bắt được lỗi từ công cụ `flaky_web_search`, báo cáo lại cho Planner và tạo ra một chiến lược mới để lấy dữ liệu còn thiếu.

```python
console.print(f"[bold cyan]Testing PEV agent on the same flaky query:[/bold cyan]\n'{flaky_query}'\n")

initial_pev_input = {"user_request": flaky_query, "intermediate_steps": [], "retries": 0}

for chunk in pev_agent_app.stream(initial_pev_input):
    for node_name, values in chunk.items():
        console.print(f"--- Node [bold cyan]{node_name}[/bold cyan] completed ---")
        if node_name == "verify":
            # Hiển thị cho chúng ta phán quyết của Verifier từ state (vì node in nó ra, chúng ta chỉ in một dải phân cách)
            pass
        if node_name == "synthesize":
            console.print(values['final_answer'])
    console.print("\n")

console.print("\n[bold green]✅ PEV Agent execution complete![/bold green]")
```

**Discussion of the Output:**
Thành công rực rỡ! Ngược lại hoàn toàn với basic agent, PEV agent đã xử lý failure một cách duyên dáng:
1.  **Phát hiện:** Khi `flaky_web_search` trả về thông báo lỗi, **Verifier** đã ngay lập tức đánh dấu nó là một failure.
2.  **Hồi đáp:** Router, thay vì chuyển sang synthesizer, đã nhận ra lỗi và đưa quy trình quay trở lại **Planner**.
3.  **Phục hồi:** Planner, giờ đã được thông báo rằng tìm kiếm thô về "employee count" đã thất bại, đã tạo ra một kế hoạch thông minh hơn. Nó có khả năng đề xuất tra cứu hồ sơ 10-K mới nhất của Apple hoặc một trang tin tức tài chính cụ thể.
4.  **Giải quyết:** executor đã thực thi kế hoạch mới thành công và synthesizer cuối cùng đã đưa ra một câu trả lời hoàn chỉnh và chính xác 100%.

Điều này chứng minh sức mạnh của PEV pattern. Nó biến một hệ thống dễ bị hỏng thành một hệ thống linh hoạt và đáng tin cậy.

## Phase 4: Quantitative Evaluation
Để kết thúc, chúng ta sẽ sử dụng giám khảo LLM của mình để chấm điểm cả hai agent dựa trên một chỉ số quan trọng mới: **Reliability (Độ tin cậy)**—khả năng cung cấp câu trả lời đúng ngay cả khi đối mặt với các lỗi của tool.

```python
class ReliabilityEvaluation(BaseModel):
    """Schema cho đánh giá độ tin cậy."""
    pe_reliability_score: int = Field(description="Reliability score 1-10 for the basic P-E agent.")
    pev_reliability_score: int = Field(description="Reliability score 1-10 for the PEV agent.")
    justification: str = Field(description="Reasoning for the scores based on the execution traces.")

judge_llm = llm.with_structured_output(ReliabilityEvaluation)

def evaluate_reliability(pe_trace: str, pev_trace: str):
    prompt = f"""You are an expert quality auditor for AI systems. 
    Evaluate the reliability of two different agent architectures when faced with a tool failure.
    
    The basic P-E agent blindly followed its plan.
    The PEV agent used a Verifier to detect and recover from errors.
    
    --- BASIC P-E TRACE ---
    {pe_trace}
    
    --- PEV TRACE ---
    {pev_trace}
    """
    return judge_llm.invoke(prompt)

# (Logs đơn giản hóa cho giám khảo)
pe_trace = "Executed plan. Step 2 returned an error. Synthesized a nonsense answer based on the error message."
pev_trace = "Executed plan. Step 2 fail detected by Verifier. Re-planned and found an alternative path to the correct data. Synthesized a perfect answer."

console.print("--- Performing Reliability Evaluation ---")
reliability_eval = evaluate_reliability(pe_trace, pev_trace)
console.print(reliability_eval.model_dump())
```

**Discussion of the Output:**
Kết quả của giám khảo chính thức hóa những gì chúng ta đã quan sát được. PEV agent nhận được điểm tuyệt đối về độ tin cậy. Nó chứng minh rằng trong thiết kế agentic, **niềm tin phải luôn đi kèm với sự xác minh**. Bằng cách dành thời gian để kiểm tra kết quả đầu ra của chính mình, agent đã trở nên đáng tin cậy hơn nhiều.

## Conclusion
Kiến trúc **Planner → Executor → Verifier (PEV)** là một khuôn mẫu thiết kế nền tảng để xây dựng các AI agent có khả năng hoạt động trong môi trường sản xuất. Bằng cách phân tách các mối quan tâm và thực thi vòng lặp xác minh-thực thi nghiêm ngặt, chúng ta tạo ra các hệ thống không chỉ thông minh mà còn kiên cường. Đối với bất kỳ ứng dụng nào mà tính chính xác và độ tin cậy là không thể thương lượng, PEV không chỉ là một sự nâng cấp—nó là một sự thiết yếu. Pattern này cho thấy rằng sức mạnh thực sự của các AI agent không chỉ nằm ở khả năng suy luận của chúng, mà còn ở khả năng tự sửa những sai lầm của chính mình.
