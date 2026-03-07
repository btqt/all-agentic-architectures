# 📘 Agentic Architectures 1: Reflection

Chào mừng bạn đến với notebook đầu tiên trong chuỗi tìm hiểu sâu về 21 agentic architectures chính. Chúng ta bắt đầu với một trong những pattern cơ bản và mạnh mẽ nhất: **Reflection**.

Pattern này nâng tầm một Large Language Model (LLM) từ một bộ tạo (generator) đơn tầng, đơn giản thành một bộ suy luận (reasoner) mạnh mẽ và thận trọng hơn. Thay vì chỉ cung cấp câu trả lời đầu tiên mà nó nghĩ ra, một reflective agent sẽ lùi lại một bước để critique, và refine kết quả của chính mình. Quá trình tự cải thiện theo vòng lặp này là nền tảng để xây dựng các hệ thống AI đáng tin cậy và chất lượng cao hơn.

### Definition
Kiến trúc **Reflection** bao gồm việc một agent tự critique và revise kết quả đầu ra của chính mình trước khi trả về câu trả lời cuối cùng. Thay vì tạo ra kết quả trong một lần duy nhất (single-pass generation), nó thực hiện một cuộc độc thoại nội bộ nhiều bước: tạo ra (produce), evaluate, và cải thiện (improve). Điều này mô phỏng quá trình của con người khi soạn thảo, review, và chỉnh sửa để phát hiện lỗi và nâng cao chất lượng.

### High-level Workflow
1.  **Generate:** Agent tạo ra bản draft hoặc giải pháp đầu tiên dựa trên prompt của người dùng.
2.  **Critique:** Agent chuyển đổi vai trò thành một critic. Nó tự vấn các câu hỏi như: *"Có gì sai với câu trả lời này không?"*, *"Còn thiếu sót gì không?"*, *"Giải pháp này đã tối ưu chưa?"*, hoặc *"Có lỗi logic hay bug nào không?"*.
3.  **Refine:** Sử dụng các insight từ quá trình tự critique, agent tạo ra phiên bản cuối cùng đã được cải thiện của kết quả đầu ra.

### When to Use / Applications
*   **Code Generation:** Code ban đầu có thể có bug, chưa hiệu quả hoặc thiếu comment. Reflection cho phép agent đóng vai trò như một code reviewer của chính nó, phát hiện lỗi và cải thiện style trước khi trình bày script cuối cùng.
*   **Complex Summarization:** Khi tóm tắt các tài liệu dày đặc, lần tóm tắt đầu tiên có thể bỏ sót các sắc thái hoặc chi tiết quan trọng. Bước reflection giúp đảm bảo bản tóm tắt đầy đủ và chính xác.
*   **Creative Writing & Content Creation:** Bản draft đầu tiên của một email, bài blog hoặc câu chuyện luôn có thể được cải thiện. Reflection cho phép agent tinh chỉnh tone, sự rõ ràng và tác động của nội dung.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Cải thiện chất lượng:** Trực tiếp giải quyết và sửa lỗi, dẫn đến kết quả chính xác, mạnh mẽ và được suy luận tốt hơn.
    *   **Low Overhead:** Đây là một pattern đơn giản về mặt khái niệm, có thể triển khai với một LLM duy nhất và không yêu cầu các tool bên ngoài phức tạp.
*   **Weaknesses:**
    *   **Self-Bias:** Agent vẫn bị giới hạn bởi kiến thức và bias của chính nó. Nếu nó không biết cách tốt hơn để giải quyết vấn đề, nó không thể critique để ra được giải pháp tốt hơn. Nó có thể sửa các lỗi mà nó nhận ra nhưng không thể tự tạo ra kiến thức mà nó còn thiếu.
    *   **Tăng Latency & Cost:** Quá trình này bao gồm ít nhất hai lần gọi LLM (generation + critique/refinement), làm cho nó chậm hơn và đắt hơn so với cách tiếp cận single-pass.

## Phase 0: Foundation & Setup
Trước khi xây dựng reflective agent, chúng ta cần thiết lập môi trường. Việc này bao gồm cài đặt các thư viện cần thiết, import các module và cấu hình API keys.

### Step 0.1: Installing Core Libraries
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ cài đặt các thư viện Python thiết yếu cho project này. Package `langchain-nebius` cung cấp quyền truy cập vào các model của Nebius AI Studio, `langchain` và `langgraph` sẽ cung cấp orchestration framework cốt lõi, `python-dotenv` sẽ quản lý API keys, và `rich` sẽ giúp chúng ta in kết quả đầu ra một cách đẹp mắt.

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv
```

### Step 0.2: Importing Libraries and Setting Up Keys
**Những gì chúng ta sẽ làm:**
Bây giờ chúng ta sẽ import tất cả các thành phần cần thiết từ các thư viện đã cài đặt. Chúng ta sẽ sử dụng thư viện `python-dotenv` để load Nebius API key từ file `.env` cục bộ một cách an toàn. Chúng ta cũng sẽ thiết lập LangSmith để thực hiện tracing, điều này cực kỳ giá trị để debug các agentic workflows nhiều bước.

**Action Required:** Bạn phải tạo một file tên là `.env` trong cùng thư mục với notebook này và thêm các key của bạn vào đó, như sau:
```
NEBIUS_API_KEY="your_nebius_api_key_here"
LANGCHAIN_API_KEY="your_langsmith_api_key_here"
```

```python
import os
import json
from typing import List, TypedDict, Optional
from dotenv import load_dotenv

# Nebius and LangChain components
from langchain_nebius import ChatNebius
from pydantic import BaseModel, Field # Corrected import for Pydantic v2
from langgraph.graph import StateGraph, END

# For pretty printing
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

# --- API Key and Tracing Setup ---
load_dotenv()

# Set up LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Reflection (Nebius)"

# Check that the keys are set
if not os.environ.get("NEBIUS_API_KEY"):
    print("NEBIUS_API_KEY not found. Please create a .env file and set it.")
if not os.environ.get("LANGCHAIN_API_KEY"):
    print("LANGCHAIN_API_KEY not found. Please create a .env file and set it for tracing.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Building the Core Components of Reflection
Một kiến trúc reflection mạnh mẽ không chỉ đơn thuần là một prompt đơn giản. Chúng ta sẽ xây dựng nó như một hệ thống gồm ba phần có cấu trúc: một **Generator**, một **Critic**, và một **Refiner**. Để đảm bảo sự tin cậy, chúng ta sẽ sử dụng các Pydantic model để định nghĩa output schemas mong đợi cho mỗi bước.

### Step 1.1: Defining the Data Schemas with Pydantic
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ định nghĩa các Pydantic model đóng vai trò như một bản hợp đồng cho LLM. Điều này cho LLM biết chính xác cấu trúc mà kết quả đầu ra của nó nên có, điều này rất quan trọng cho một quy trình nhiều bước nơi kết quả đầu ra của bước này trở thành đầu vào cho bước tiếp theo.

```python
class DraftCode(BaseModel):
    """Schema for the initial code draft generated by the agent."""
    code: str = Field(description="The Python code generated to solve the user's request.")
    explanation: str = Field(description="A brief explanation of how the code works.")

class Critique(BaseModel):
    """Schema for the self-critique of the generated code."""
    has_errors: bool = Field(description="Does the code have any potential bugs or logical errors?")
    is_efficient: bool = Field(description="Is the code written in an efficient and optimal way?")
    suggested_improvements: List[str] = Field(description="Specific, actionable suggestions for improving the code.")
    critique_summary: str = Field(description="A summary of the critique.")

class RefinedCode(BaseModel):
    """Schema for the final, refined code after incorporating the critique."""
    refined_code: str = Field(description="The final, improved Python code.")
    refinement_summary: str = Field(description="A summary of the changes made based on the critique.")

print("Pydantic models for Draft, Critique, and RefinedCode have been defined.")
```

**Discussion of the Output:**
Chúng ta đã định nghĩa thành công các cấu trúc dữ liệu của mình. Model `Critique` đặc biệt quan trọng; bằng cách yêu cầu các field cụ thể như `has_errors` và `is_efficient`, chúng ta hướng dẫn LLM thực hiện một quá trình evaluation có cấu trúc và hữu ích hơn là chỉ yêu cầu nó "review code".

### Step 1.2: Initializing the Nebius LLM and the Console
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ khởi tạo Nebius language model, thành phần sẽ cung cấp sức mạnh cho cả ba vai trò (Generator, Critic, và Refiner). Chúng ta sẽ sử dụng một model mạnh mẽ như `meta-llama/Meta-Llama-3.1-8B-Instruct` để đảm bảo khả năng suy luận chất lượng cao cho tất cả các bước. Chúng ta cũng sẽ thiết lập `rich` console để có kết quả đầu ra được format rõ ràng.

```python
# Use a powerful Nebius model for generation and critique
llm = ChatNebius(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0.2)

# Initialize console for pretty printing
console = Console()

print("Nebius LLM and Console are initialized.")
```

### Step 1.3: Creating the Generator Node
**Những gì chúng ta sẽ làm:**
Nhiệm vụ duy nhất của node này là tiếp nhận request của người dùng và tạo ra bản draft đầu tiên. Chúng ta sẽ bind Pydantic model `DraftCode` vào Nebius LLM để đảm bảo kết quả đầu ra của nó được cấu trúc chính xác.

```python
def generator_node(state):
    """Generates the initial draft of the code."""
    console.print("--- 1. Generating Initial Draft ---")
    generator_llm = llm.with_structured_output(DraftCode)
    
    prompt = f"""You are an expert Python programmer. Write a Python function to solve the following request.
    Provide a simple, clear implementation and an explanation.
    
    Request: {state['user_request']}
    """
    
    draft = generator_llm.invoke(prompt)
    return {"draft": draft.model_dump()} # Corrected: use .model_dump()
```

### Step 1.4: Creating the Critic Node
**Những gì chúng ta sẽ làm:**
Đây là phần cốt lõi của quá trình reflection. Node Critic tiếp nhận bản draft ban đầu, phân tích các điểm yếu, và tạo ra một bản critique có cấu trúc bằng cách sử dụng Pydantic model `Critique` của chúng ta.

```python
def critic_node(state):
    """Critiques the generated code for errors and inefficiencies."""
    console.print("--- 2. Critiquing Draft ---")
    critic_llm = llm.with_structured_output(Critique)
    
    code_to_critique = state['draft']['code']
    
    prompt = f"""You are an expert code reviewer and senior Python developer. Your task is to perform a thorough critique of the following code.
    
    Analyze the code for:
    1.  **Bugs and Errors:** Are there any potential runtime errors, logical flaws, or edge cases that are not handled?
    2.  **Efficiency and Best Practices:** Is this the most efficient way to solve the problem? Does it follow standard Python conventions (PEP 8)?
    
    Provide a structured critique with specific, actionable suggestions.
    
    Code to Review:
    ```python
    {code_to_critique}
    ```
    """
    
    critique = critic_llm.invoke(prompt)
    return {"critique": critique.model_dump()} # Corrected: use .model_dump()
```

### Step 1.5: Creating the Refiner Node
**Những gì chúng ta sẽ làm:**
Bước cuối cùng trong logic của chúng ta là Refiner. Node này nhận cả bản draft gốc và bản critique có cấu trúc, với nhiệm vụ viết phiên bản code cuối cùng đã được cải thiện.

```python
def refiner_node(state):
    """Refines the code based on the critique."""
    console.print("--- 3. Refining Code ---")
    refiner_llm = llm.with_structured_output(RefinedCode)
    
    draft_code = state['draft']['code']
    critique_suggestions = json.dumps(state['critique'], indent=2)
    
    prompt = f"""You are an expert Python programmer tasked with refining a piece of code based on a critique.
    
    Your goal is to rewrite the original code, implementing all the suggested improvements from the critique.
    
    **Original Code:**
    ```python
    {draft_code}
    ```
    
    **Critique and Suggestions:**
    {critique_suggestions}
    
    Please provide the final, refined code and a summary of the changes you made.
    """
    
    refined_code = refiner_llm.invoke(prompt)
    return {"refined_code": refined_code.model_dump()} # Corrected: use .model_dump()
```

**Discussion of Phase 1:**
Hiện tại, chúng ta đã tạo ra ba thành phần logic cốt lõi cho reflective agent của mình. Mỗi thành phần là một hàm độc lập (hoặc 'node') thực hiện một nhiệm vụ duy nhất và được định nghĩa rõ ràng. Việc sử dụng structured output ở mỗi giai đoạn đảm bảo dữ liệu truyền đi một cách đáng tin cậy từ node này sang node tiếp theo. Bây giờ, chúng ta đã sẵn sàng để orchestrate workflow này bằng LangGraph.

## Phase 2: Orchestrating the Reflection Workflow with LangGraph

### Step 2.1: Defining the Graph State
**Những gì chúng ta sẽ làm:**
'State' là bộ nhớ của graph của chúng ta. Nó là một object trung tâm được truyền giữa các node, và mỗi node có thể đọc từ đó hoặc ghi vào đó. Chúng ta sẽ định nghĩa một `ReflectionState` sử dụng `TypedDict` của Python để chứa tất cả các phần trong workflow của mình.

```python
class ReflectionState(TypedDict):
    """Represents the state of our reflection graph."""
    user_request: str
    draft: Optional[dict]
    critique: Optional[dict]
    refined_code: Optional[dict]

print("ReflectionState TypedDict defined.")
```

### Step 2.2: Building and Visualizing the Graph
**Những gì chúng ta sẽ làm:**
Bây giờ chúng ta sẽ lắp ráp các node của mình thành một workflow mạch lạc bằng cách sử dụng `StateGraph`. Đối với reflection pattern này, workflow là một chuỗi tuần tự đơn giản: **Generate → Critique → Refine**. Chúng ta sẽ định nghĩa luồng này, sau đó compile và hình ảnh hóa graph để xác nhận cấu trúc của nó.

```python
graph_builder = StateGraph(ReflectionState)

# Add the nodes to the graph
graph_builder.add_node("generator", generator_node)
graph_builder.add_node("critic", critic_node)
graph_builder.add_node("refiner", refiner_node)

# Define the workflow edges
graph_builder.set_entry_point("generator")
graph_builder.add_edge("generator", "critic")
graph_builder.add_edge("critic", "refiner")
graph_builder.add_edge("refiner", END)

# Compile the graph
reflection_app = graph_builder.compile()

print("Reflection graph compiled successfully!")

# Visualize the graph
try:
    from IPython.display import Image, display
    png_image = reflection_app.get_graph().draw_png()
    display(Image(png_image))
except Exception as e:
    print(f"Graph visualization failed: {e}. Please ensure pygraphviz is installed.")
```

**Discussion of the Output:**
Hệ thống graph đã được compile thành công. Hình ảnh hóa xác nhận workflow tuần tự đúng như dự định. Bạn có thể thấy rõ ràng state truyền từ điểm bắt đầu (`generator`), đi qua các node `critic` và `refiner`, và cuối cùng kết thúc ở trạng thái `__end__`. Cấu trúc đơn giản nhưng mạnh mẽ này hiện đã sẵn sàng để thực thi.

## Phase 3: End-to-End Execution and Evaluation
Với graph đã được compile, đã đến lúc xem reflection pattern hoạt động trên thực tế. Chúng ta sẽ giao cho nó một nhiệm vụ lập trình mà nỗ lực đầu tiên sơ sài có khả năng không tối ưu, khiến nó trở thành một test case hoàn hảo cho quá trình tự critique và refinement.

### Step 3.1: Running the Full Reflection Workflow
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ invoke ứng dụng LangGraph đã được compile của mình với một request yêu cầu viết một hàm tìm số Fibonacci thứ n. Chúng ta sẽ stream các kết quả và tích lũy đầy đủ state để có thể kiểm tra tất cả các bước trung gian ở cuối quy trình.

```python
user_request = "Write a Python function to find the nth Fibonacci number."
initial_input = {"user_request": user_request}

console.print(f"[bold cyan]🚀 Kicking off Reflection workflow for request:[/bold cyan] '{user_request}'\n")

# Corrected: This loop correctly captures the final, fully-populated state
final_state = None
for state_update in reflection_app.stream(initial_input, stream_mode="values"):
    final_state = state_update

console.print("\n[bold green]✅ Reflection workflow complete![/bold green]")
```

### Step 3.2: Analyzing the 'Before and After'
**Những gì chúng ta sẽ làm:**
Đây là thời điểm quyết định. Bây giờ chúng ta sẽ kiểm tra kết quả từ mỗi giai đoạn của workflow, được lưu trữ trong `final_state`. Chúng ta sẽ in bản draft đầu tiên, bản critique mà nó nhận được, và code cuối cùng đã được tinh chỉnh để thấy rõ giá trị gia tăng được tạo ra bởi quá trình reflection.

```python
# Check if final_state is available and has the expected keys
if final_state and 'draft' in final_state and 'critique' in final_state and 'refined_code' in final_state:
    console.print(Markdown("--- ### Initial Draft ---"))
    console.print(Markdown(f"**Explanation:** {final_state['draft']['explanation']}"))
    # Use rich's Syntax for proper code highlighting
    console.print(Syntax(final_state['draft']['code'], "python", theme="monokai", line_numbers=True))

    console.print(Markdown("\n--- ### Critique ---"))
    console.print(Markdown(f"**Summary:** {final_state['critique']['critique_summary']}"))
    console.print(Markdown(f"**Improvements Suggested:**"))
    for improvement in final_state['critique']['suggested_improvements']:
        console.print(Markdown(f"- {improvement}"))

    console.print(Markdown("\n--- ### Final Refined Code ---"))
    console.print(Markdown(f"**Refinement Summary:** {final_state['refined_code']['refinement_summary']}"))
    console.print(Syntax(final_state['refined_code']['refined_code'], "python", theme="monokai", line_numbers=True))
else:
    console.print("[bold red]Error: The `final_state` is not available or is incomplete. Please check the execution of the previous cells.[/bold red]")
```

**Discussion of the Output:**
Các kết quả là một minh họa hoàn hảo cho sức mạnh của reflection.

1.  **Bản Draft đầu tiên** có khả năng tạo ra một giải pháp recursive đơn giản. Mặc dù đúng, nhưng cách tiếp cận này nổi tiếng là kém hiệu quả do tính toán lặp lại các giá trị giống nhau nhiều lần, dẫn đến độ phức tạp thời gian (time complexity) theo hàm mũ.
2.  Bản **Critique** đã xác định chính xác thiếu sót lớn này. LLM, trong vai trò 'critic', đã chỉ ra sự kém hiệu quả và gợi ý một phương pháp iterative tối ưu hơn để tránh các tính toán dư thừa.
3.  **Code cuối cùng đã được tinh chỉnh** đã triển khai thành công bản critique. Nó thay thế hàm recursive chậm chạp bằng một giải pháp iterative nhanh hơn nhiều, sử dụng một loop và hai biến để theo dõi chuỗi số.

Đây là một sự cải thiện không hề nhỏ. Agent không chỉ sửa một lỗi đánh máy; nó đã thay đổi hoàn toàn thuật toán của mình để hướng tới một giải pháp mạnh mẽ và có khả năng mở rộng tốt hơn. Đây chính là giá trị của reflection pattern.

### Step 3.3: Quantitative Evaluation (LLM-as-a-Judge)
**Những gì chúng ta sẽ làm:**
Để chính thức hóa việc phân tích, chúng ta sẽ sử dụng một LLM khác làm 'judge' khách quan để chấm điểm chất lượng của bản draft đầu tiên so với code cuối cùng. Điều này cung cấp một thước đo khách quan hơn về sự cải thiện đạt được thông qua reflection.

```python
class CodeEvaluation(BaseModel):
    """Schema for evaluating a piece of code."""
    correctness_score: int = Field(description="Score from 1-10 on whether the code is logically correct.")
    efficiency_score: int = Field(description="Score from 1-10 on the code's algorithmic efficiency.")
    style_score: int = Field(description="Score from 1-10 on code style and readability (PEP 8). ")
    justification: str = Field(description="A brief justification for the scores.")

judge_llm = llm.with_structured_output(CodeEvaluation)

def evaluate_code(code_to_evaluate: str):
    prompt = f"""You are an expert judge of Python code. Evaluate the following function on a scale of 1-10 for correctness, efficiency, and style. Provide a brief justification.
    
    Code:
    ```python
    {code_to_evaluate}
    ```
    """
    return judge_llm.invoke(prompt)

if final_state and 'draft' in final_state and 'refined_code' in final_state:
    console.print("--- Evaluating Initial Draft ---")
    initial_draft_evaluation = evaluate_code(final_state['draft']['code'])
    console.print(initial_draft_evaluation.model_dump()) # Corrected: use .model_dump()

    console.print("\n--- Evaluating Refined Code ---")
    refined_code_evaluation = evaluate_code(final_state['refined_code']['refined_code'])
    console.print(refined_code_evaluation.model_dump()) # Corrected: use .model_dump()
else:
    console.print("[bold red]Error: Cannot perform evaluation because the `final_state` is incomplete.[/bold red]")
```

**Discussion of the Output:**
Quá trình evaluation theo kiểu LLM-as-a-Judge cung cấp bằng chứng định lượng về sự thành công của reflection pattern. Bản draft đầu tiên có lẽ đã nhận được điểm cao về tính chính xác nhưng điểm rất thấp về hiệu quả. Ngược lại, code đã tinh chỉnh sẽ đạt điểm cao ở cả tính chính xác và hiệu quả. Quá trình evaluation tự động, có chấm điểm này xác nhận rằng quy trình reflection không chỉ làm thay đổi code—nó còn cải thiện code một cách rõ rệt có thể đo lường được.

## Conclusion
Trong notebook này, chúng ta đã xây dựng, thực hiện, và evaluate thành công một agent hoàn chỉnh từ đầu đến cuối sử dụng kiến trúc **Reflection** với các model của Nebius AI Studio. Chúng ta đã trực tiếp thấy cách pattern đơn giản nhưng mạnh mẽ này có thể biến một bộ tạo LLM cơ bản thành một công cụ giải quyết vấn đề phức tạp và đáng tin cậy hơn.

Bằng cách cấu trúc quy trình thành các bước **Generate**, **Critique**, và **Refine** riêng biệt và orchestrate chúng bằng LangGraph, chúng ta đã tạo ra một hệ thống mạnh mẽ có thể tự nhận diện và sửa các lỗi nghiêm trọng của chính mình. Sự cải thiện hữu hình—từ một giải pháp recursive kém hiệu quả sang một giải pháp iterative tối ưu—chứng minh rằng reflection là một kỹ thuật nền tảng để tiến xa hơn các tác vụ agentic tầm thường và xây dựng các hệ thống AI thể hiện sự chất lượng và suy luận sâu sắc hơn.
