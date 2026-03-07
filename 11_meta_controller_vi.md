# 📘 Agentic Architectures 11: Meta-Controller

Chào mừng bạn đến với notebook thứ mười một trong loạt bài của chúng ta. Hôm nay, chúng ta sẽ xây dựng một **Meta-Controller**, một kiến trúc agent giám sát điều phối một nhóm các sub-agents chuyên biệt. Pattern này là nền tảng để tạo ra các hệ thống AI đa tài, mạnh mẽ.

Thay vì xây dựng một agent đơn lẻ, nguyên khối (monolithic) cố gắng làm mọi thứ, Meta-Controller đóng vai trò như một bộ điều phối thông minh. Nó nhận một yêu cầu đầu vào, phân tích bản chất của nó và chuyển hướng (route) nó đến specialist phù hợp nhất từ một nhóm các agent có sẵn. Điều này cho phép mỗi sub-agent được tối ưu hóa cao độ cho nhiệm vụ cụ thể của nó, dẫn đến hiệu suất và tính module tốt hơn.

Chúng ta sẽ chứng minh điều này bằng cách xây dựng một hệ thống với ba specialist riêng biệt:
1.  **Generalist Agent:** Xử lý các cuộc hội thoại thông thường và các câu hỏi đơn giản.
2.  **Research Agent:** Được trang bị search tool để trả lời các câu hỏi về các sự kiện gần đây hoặc các chủ đề phức tạp.
3.  **Coding Agent:** Một specialist tập trung vào việc tạo các đoạn mã Python.

Meta-Controller sẽ là "bộ não" của hoạt động, kiểm tra từng truy vấn của người dùng và quyết định agent nào phù hợp nhất để phản hồi. Điều này tạo ra một hệ thống linh hoạt và dễ dàng mở rộng, nơi các khả năng mới có thể được thêm vào đơn giản bằng cách tạo một specialist agent mới và dạy cho controller về nó.

### Definition
Một **Meta-Controller** (hoặc Router) là một agent giám sát trong một hệ thống đa tác vụ (multi-agent system), chịu trách nhiệm phân tích các nhiệm vụ đầu vào và gửi chúng đến sub-agent chuyên biệt hoặc workflow phù hợp. Nó hoạt động như một lớp định tuyến thông minh, quyết định công cụ hoặc chuyên gia nào phù hợp nhất cho công việc hiện tại.

### High-level Workflow
1.  **Receive Input:** Hệ thống nhận yêu cầu từ người dùng.
2.  **Meta-Controller Analysis:** Agent Meta-Controller kiểm tra ý định, độ phức tạp và nội dung của yêu cầu.
3.  **Dispatch to Specialist:** Dựa trên phân tích của mình, Meta-Controller chọn specialist agent tốt nhất (ví dụ: 'Researcher', 'Coder', 'Chatbot') từ một nhóm được định nghĩa trước.
4.  **Execute Task:** Specialist agent được chọn sẽ thực thi nhiệm vụ và tạo ra kết quả.
5.  **Return Result:** Kết quả từ specialist được trả về cho người dùng. Trong các workflow phức tạp hơn, quyền kiểm soát có thể quay lại Meta-Controller để thực hiện các bước tiếp theo hoặc giám sát.

### When to Use / Applications
*   **Nền tảng AI đa dịch vụ:** Một điểm truy cập duy nhất cho một nền tảng cung cấp các dịch vụ đa dạng như phân tích tài liệu, trực quan hóa dữ liệu và sáng tác nội dung.
*   **Trợ lý cá nhân thích ứng:** Một trợ lý có thể chuyển đổi giữa các chế độ hoặc công cụ khác nhau, chẳng hạn như quản lý lịch của bạn, tìm kiếm trên web hoặc điều khiển các thiết bị nhà thông minh.
*   **Workflow doanh nghiệp:** Định tuyến các ticket hỗ trợ khách hàng đến đúng bộ phận (kỹ thuật, thanh toán, bán hàng) dựa trên nội dung của ticket.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Tính linh hoạt & Tính module:** Cực kỳ dễ dàng để thêm các khả năng mới bằng cách chỉ cần thêm một specialist agent mới và cập nhật logic định tuyến của controller.
    *   **Hiệu suất:** Cho phép sử dụng các agent chuyên gia, được tối ưu hóa cao thay vì một mô hình "vạn năng" nhưng có thể chỉ đạt mức trung bình ở mọi thứ.
*   **Weaknesses:**
    *   **Controller là điểm gây lỗi duy nhất (Single Point of Failure):** Chất lượng của toàn bộ hệ thống phụ thuộc vào khả năng định tuyến chính xác của controller. Một quyết định định tuyến sai lầm sẽ dẫn đến kết quả dưới mức tối ưu hoặc không chính xác.
    *   **Khả năng tăng độ trễ:** Bước định tuyến bổ sung có thể làm tăng một chút độ trễ so với việc gọi trực tiếp đến một agent duy nhất.

## Phase 0: Foundation & Setup
Chúng ta sẽ cài đặt các thư viện và thiết lập môi trường. Chúng ta sẽ cần `langchain-tavily` cho search tool của Research Agent.

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv langchain-tavily
```

```python
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Pydantic for data modeling
from pydantic import BaseModel, Field

# LangChain components
from langchain_nebius import ChatNebius
from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate

# LangGraph components
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

# For pretty printing
from rich.console import Console
from rich.markdown import Markdown

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Meta-Controller (Nebius)"

required_vars = ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]
for var in required_vars:
    if var not in os.environ:
        print(f"Warning: Environment variable {var} not set.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Building the Specialist Agents
Đầu tiên, chúng ta sẽ tạo ra nhóm các agent chuyên gia. Mỗi agent sẽ là một chuỗi (chain) đơn giản với một persona cụ thể và trong trường hợp của Researcher là một công cụ (tool). Chúng ta sẽ bao bọc chúng trong một hàm node để sử dụng trong LangGraph.

```python
console = Console()
llm = ChatNebius(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0)
search_tool = TavilySearch(max_results=3)

# Định nghĩa state cho toàn bộ graph
class MetaAgentState(TypedDict):
    user_request: str
    next_agent_to_call: Optional[str]
    generation: str

# Một hàm factory hỗ trợ để tạo các specialist agent nodes
def create_specialist_node(persona: str, tools: list = None):
    """Factory để tạo một specialist agent node."""
    system_prompt = f"You are a specialist agent with the following persona: {persona}. Respond directly and concisely to the user's request based on your role."
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{user_request}")
    ])
    
    if tools:
        chain = prompt | llm.bind_tools(tools)
    else:
        chain = prompt | llm
        
    def specialist_node(state: MetaAgentState) -> Dict[str, Any]:
        result = chain.invoke({"user_request": state['user_request']})
        return {"generation": result.content}
    
    return specialist_node

# 1. Generalist Agent Node
generalist_node = create_specialist_node(
    "You are a friendly and helpful generalist AI assistant. You handle casual conversation and simple questions."
)

# 2. Research Agent Node
research_agent_node = create_specialist_node(
    "You are an expert researcher. You must use your search tool to find information to answer the user's question.",
    tools=[search_tool]
)

# 3. Coding Agent Node
coding_agent_node = create_specialist_node(
    "You are an expert Python programmer. Your task is to write clean, efficient Python code based on the user's request. Provide only the code, wrapped in markdown code blocks, with minimal explanation."
)

print("Specialist agents defined successfully.")
```

## Phase 2: Building the Meta-Controller
Đây là bộ não của hệ thống. Meta-Controller là một node được hỗ trợ bởi LLM, công việc duy nhất của nó là quyết định nên định tuyến yêu cầu tới specialist nào. Chất lượng của prompt là yếu tố quyết định hiệu suất của hệ thống.

```python
# Pydantic model cho quyết định định tuyến của controller
class ControllerDecision(BaseModel):
    next_agent: str = Field(description="The name of the specialist agent to call next. Must be one of ['Generalist', 'Researcher', 'Coder'].")
    reasoning: str = Field(description="A brief reason for choosing the next agent.")

def meta_controller_node(state: MetaAgentState) -> Dict[str, Any]:
    """Controller trung tâm quyết định specialist nào sẽ được gọi."""
    console.print("--- 🧠 Meta-Controller Analyzing Request ---")
    
    # Định nghĩa các specialist và mô tả của chúng cho controller
    specialists = {
        "Generalist": "Handles casual conversation, greetings, and simple questions.",
        "Researcher": "Answers questions about recent events, complex topics, or anything requiring up-to-date information from the web.",
        "Coder": "Writes Python code based on a user's specification."
    }
    
    specialist_descriptions = "\n".join([f"- {name}: {desc}" for name, desc in specialists.items()])
    
    prompt = ChatPromptTemplate.from_template(
        f"""You are the meta-controller for a multi-agent AI system. Your job is to analyze the user's request and route it to the most appropriate specialist agent.

Here are the available specialists:
{specialist_descriptions}

Analyze the following user request and choose the best specialist to handle it. Provide your decision in the required format.

User Request: "{{user_request}}" """
    )
    
    controller_llm = llm.with_structured_output(ControllerDecision)
    chain = prompt | controller_llm
    
    decision = chain.invoke({"user_request": state['user_request']})
    console.print(f"[yellow]Routing decision:[/yellow] Send to [bold]{decision.next_agent}[/bold]. [italic]Reason: {decision.reasoning}[/italic]")
    
    return {"next_agent_to_call": decision.next_agent}

print("Meta-Controller node defined successfully.")
```

## Phase 3: Assembling and Running the Graph
Bây giờ chúng ta sẽ dùng LangGraph để kết nối mọi thứ lại với nhau. Graph sẽ bắt đầu với Meta-Controller, sau đó dựa trên quyết định của nó, một conditional edge sẽ định tuyến state tới specialist node chính xác. Sau khi specialist chạy, graph sẽ kết thúc.

```python
# Xây dựng graph
workflow = StateGraph(MetaAgentState)

# Thêm các node cho controller và mỗi specialist
workflow.add_node("meta_controller", meta_controller_node)
workflow.add_node("Generalist", generalist_node)
workflow.add_node("Researcher", research_agent_node)
workflow.add_node("Coder", coding_agent_node)

# Thiết lập entry point
workflow.set_entry_point("meta_controller")

# Định nghĩa logic định tuyến có điều kiện
def route_to_specialist(state: MetaAgentState) -> str:
    """Đọc quyết định của controller và trả về tên của node cần định tuyến tới."""
    return state["next_agent_to_call"]

workflow.add_conditional_edges(
    "meta_controller",
    route_to_specialist,
    {
        "Generalist": "Generalist",
        "Researcher": "Researcher",
        "Coder": "Coder"
    }
)

# Sau khi bất kỳ specialist nào chạy, quy trình kết thúc
workflow.add_edge("Generalist", END)
workflow.add_edge("Researcher", END)
workflow.add_edge("Coder", END)

meta_agent = workflow.compile()
print("Meta-Controller agent graph compiled successfully.")
```

## Phase 4: Demonstration
Hãy kiểm tra Meta-Controller của chúng ta với một loạt các câu lệnh để xem liệu nó có gửi chúng đến đúng specialist hay không.

```python
def run_agent(query: str):
    result = meta_agent.invoke({"user_request": query})
    console.print("\n[bold]Final Response:[/bold]")
    console.print(Markdown(result['generation']))

# Test 1: Nên được định tuyến tới Generalist
console.print("--- 💬 Test 1: General Conversation ---")
run_agent("Hello, how are you today?")

# Test 2: Nên được định tuyến tới Researcher
console.print("\n--- 🔬 Test 2: Research Question ---")
run_agent("What were NVIDIA's latest financial results?")

# Test 3: Nên được định tuyến tới Coder
console.print("\n--- 💻 Test 3: Coding Request ---")
run_agent("Can you write me a python function to calculate the nth fibonacci number?")
```

## Conclusion
Trong notebook này, chúng ta đã triển khai thành công một kiến trúc **Meta-Controller**. Các bài kiểm tra của chúng ta đã chứng minh rõ ràng chức năng chính của nó: hoạt động như một bộ định tuyến thông minh và năng động.

1.  Lời chào đơn giản được xác định chính xác và gửi tới **Generalist**.
2.  Truy vấn về tin tức tài chính gần đây được gửi tới **Researcher**, agent này đã sử dụng search tool để lấy thông tin cập nhật.
3.  Yêu cầu về một đoạn mã đã được định tuyến tới **Coder**, agent này đã cung cấp một hàm được định dạng tốt và chính xác.

Pattern này đặc biệt mạnh mẽ để xây dựng các hệ thống AI có khả năng mở rộng và bảo trì. Bằng cách tách biệt các mối quan tâm, mỗi specialist có thể được cải thiện độc lập mà không ảnh hưởng đến những agent khác. Trí thông minh tổng thể của hệ thống có thể được nâng cao đơn giản bằng cách thêm các specialist mới, có năng lực hơn và làm cho Meta-Controller nhận thức được chúng. Mặc thân bản thân controller đại diện cho một điểm thắt nút tiềm năng, nhưng vai trò của nó như một bộ điều phối linh hoạt là nền tảng của thiết kế agentic tiên tiến.
