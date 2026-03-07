# 📘 Agentic Architectures 2: Tool Use

Notebook này đề cập đến kiến trúc agentic thứ hai, và có thể nói là một trong những kiến trúc mang tính thay đổi nhất: **Tool Use**. Pattern này là cầu nối liên kết khả năng suy luận của Large Language Model (LLM) với thế giới thực đầy biến động.

Nếu không có tool, một LLM là một hệ thống khép kín, bị giới hạn bởi kiến thức đã được "đóng băng" trong dữ liệu training của nó. Nó không thể biết thời tiết hôm nay thế nào, giá cổ phiếu hiện tại là bao nhiêu, hay trạng thái của một đơn hàng trong Database của công ty bạn. Bằng cách cung cấp cho agent khả năng sử dụng tool, chúng ta trao quyền cho nó vượt qua giới hạn cơ bản này, cho phép nó truy vấn các API, tìm kiếm Database, và truy cập thông tin trực tiếp để đưa ra các câu trả lời không chỉ dựa trên suy luận mà còn dựa trên dữ liệu thực tế, kịp thời và phù hợp.

### Definition
Kiến trúc **Tool Use** trang bị cho một agent chạy bằng LLM khả năng gọi các hàm hoặc API bên ngoài (gọi là "tools"). Agent sẽ tự chủ quyết định khi nào một truy vấn của người dùng không thể được trả lời chỉ bằng kiến thức nội bộ của nó và xác định tool nào là phù hợp để gọi nhằm tìm kiếm thông tin cần thiết.

### High-level Workflow
1.  **Receive Query:** Agent nhận một request từ người dùng.
2.  **Decision:** Agent phân tích truy vấn và các tool hiện có. Nó quyết định xem có cần một tool để trả lời câu hỏi một cách chính xác hay không.
3.  **Action:** Nếu cần một tool, agent sẽ định dạng một lời gọi đến tool đó (ví dụ: một hàm cụ thể với các đối số phù hợp).
4.  **Observation:** Hệ thống thực thi lời gọi tool, và kết quả (gọi là "observation") được trả về cho agent.
5.  **Synthesis:** Agent tích hợp kết quả đầu ra của tool vào quá trình suy luận của mình để tạo ra câu trả lời cuối cùng, có căn cứ cho người dùng.

### When to Use / Applications
*   **Research Assistants:** Trả lời các câu hỏi yêu cầu thông tin cập nhật từng phút bằng cách sử dụng một web search API.
*   **Enterprise Assistants:** Truy vấn các Database nội bộ của công ty để trả lời các câu hỏi như "Có bao nhiêu người dùng mới đã đăng ký vào tuần trước?"
*   **Scientific & Mathematical Tasks:** Sử dụng máy tính hoặc một computational engine như WolframAlpha cho các phép tính chính xác mà các LLM thường gặp khó khăn.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Factual Grounding:** Giảm đáng kể tình trạng ảo giác (hallucination) bằng cách truy xuất dữ liệu thực tế, trực tiếp.
    *   **Extensibility:** Khả năng của agent có thể được mở rộng liên tục bằng cách thêm các tool mới.
*   **Weaknesses:**
    *   **Integration Overhead:** Yêu cầu việc thiết lập hệ thống ("plumbing") cẩn thận để định nghĩa các tool, xử lý API keys, và quản lý các lỗi tiềm ẩn của tool.
    *   **Tool Trust:** Chất lượng câu trả lời của agent phụ thuộc vào độ tin cậy và tính chính xác của các tool mà nó sử dụng. Agent phải tin tưởng rằng các tool của nó cung cấp thông tin chính xác.

## Phase 0: Foundation & Setup

Như trước đây, chúng ta bắt đầu bằng việc thiết lập môi trường. Việc này bao gồm cài đặt các thư viện cần thiết và cấu hình API keys cho Nebius, LangSmith, và tool cụ thể mà chúng ta sẽ sử dụng.

### Step 0.1: Installing Core Libraries
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ cài đặt bộ thư viện tiêu chuẩn để thực hiện orchestration (`langchain-nebius`, `langgraph`), quản lý môi trường (`python-dotenv`), và in ấn (`rich`). Quan trọng nhất, chúng ta cũng sẽ cài đặt `tavily-python`, thư viện cung cấp một API dễ sử dụng cho một công cụ tìm kiếm web mạnh mẽ mà chúng ta sẽ cung cấp cho agent của mình.

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv tavily-python
```

### Step 0.2: Importing Libraries and Setting Up Keys
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ import các module cần thiết và sử dụng `python-dotenv` để load các API keys. Đối với notebook này, chúng ta cần các key cho Nebius (cho LLM), LangSmith (để thực hiện tracing), và Tavily (cho công cụ tìm kiếm web).

**Action Required:** Tạo một file `.env` trong thư mục này với các key của bạn:
```
NEBIUS_API_KEY="your_nebius_api_key_here"
LANGCHAIN_API_KEY="your_langsmith_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"
```

```python
import os
import json
from typing import List, Annotated, TypedDict, Optional
from dotenv import load_dotenv

# LangChain components
from langchain_nebius import ChatNebius
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage, ToolMessage
from pydantic import BaseModel, Field

# LangGraph components
from langgraph.graph import StateGraph, END
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode

# For pretty printing
from rich.console import Console
from rich.markdown import Markdown

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Tool Use (Nebius)"

# Kiểm tra xem các key đã được thiết lập chưa
for key in ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]:
    if not os.environ.get(key):
        print(f"{key} not found. Please create a .env file and set it.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Defining the Agent's Toolkit
Một agent chỉ có năng lực tương đương với các tool mà nó có quyền truy cập. Trong Phase này, chúng ta sẽ định nghĩa và kiểm thử tool cụ thể mà chúng ta sẽ cung cấp cho agent: tính năng tìm kiếm web trực tiếp.

### Step 1.1: Creating and Testing the Web Search Tool
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ khởi tạo tool `TavilySearchResults`. Phần quan trọng nhất của việc định nghĩa một tool là **mô tả (description)** của nó. LLM sử dụng mô tả bằng ngôn ngữ tự nhiên này để hiểu tool đó làm gì và khi nào nên sử dụng nó. Một bản mô tả rõ ràng, chính xác là điều thiết yếu để agent đưa ra các quyết định đúng đắn. Sau đó, chúng ta sẽ kiểm thử tool trực tiếp để xem kết quả đầu ra thô của nó trông như thế nào.

```python
# Khởi tạo tool. Chúng ta có thể đặt số lượng kết quả tối đa để giữ cho context ngắn gọn.
search_tool = TavilySearchResults(max_results=2)

# Việc đặt tên và mô tả rõ ràng cho tool là cực kỳ quan trọng đối với agent
search_tool.name = "web_search"
search_tool.description = "A tool that can be used to search the internet for up-to-date information on any topic, including news, events, and current affairs."

tools = [search_tool]
print(f"Tool '{search_tool.name}' created with description: '{search_tool.description}'")

console = Console()

# Hãy thử kiểm thử tool trực tiếp để xem format kết quả đầu ra của nó
print("\n--- Testing the tool directly ---")
test_query = "What was the score of the last Super Bowl?"
test_result = search_tool.invoke({"query": test_query})
console.print(f"[bold green]Query:[/bold green] {test_query}")
console.print("\n[bold green]Result:[/bold green]")
console.print(test_result)
```

**Discussion of the Output:**
Bài kiểm thử cho thấy kết quả thô của tool `web_search` của chúng ta. Nó trả về một danh sách các dictionary, trong đó mỗi dictionary chứa URL và đoạn snippet nội dung của một kết quả tìm kiếm. Thông tin có cấu trúc này chính là những gì agent sẽ nhận được dưới dạng "observation" sau khi nó quyết định sử dụng tool. Bây giờ khi đã có một tool hoạt động tốt, chúng ta có thể xây dựng agent sẽ học cách sử dụng nó.

## Phase 2: Building the Tool-Using Agent with LangGraph
Bây giờ chúng ta sẽ xây dựng agentic workflow. Việc này bao gồm làm cho LLM nhận thức được các tool và tạo ra một graph cho phép nó lặp lại qua chu kỳ "think-act-observe" (suy nghĩ-hành động-quan sát), vốn là bản chất của việc sử dụng tool.

### Step 2.1: Defining the Graph State
**Những gì chúng ta sẽ làm:**
State cho một agent sử dụng tool thường là một danh sách các message đại diện cho lịch sử hội thoại. Lịch sử này bao gồm các câu hỏi của người dùng, suy nghĩ của agent và các lời gọi tool, cùng với kết quả từ các tool đó. Chúng ta sẽ sử dụng một `TypedDict` có thể chứa bất kỳ loại LangChain message nào.

```python
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

print("AgentState TypedDict defined to manage conversation history.")
```

### Step 2.2: Binding the Tools to the LLM
**Những gì chúng ta sẽ làm:**
Đây là bước quan trọng nơi chúng ta làm cho LLM "nhận thức" được về các tool. Chúng ta sử dụng phương thức `.bind_tools()`, phương thức này truyền tên và mô tả của các tool vào system prompt của LLM. Điều này cho phép logic nội bộ của model quyết định khi nào nên gọi một tool dựa trên mô tả của nó.

```python
llm = ChatNebius(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)

# Bind các tool vào LLM, giúp nó nhận thức được các tool
llm_with_tools = llm.bind_tools(tools)

print("LLM has been bound with the provided tools.")
```

### Step 2.3: Defining the Agent Nodes
**Những gì chúng ta sẽ làm:**
Graph của chúng ta sẽ có hai node chính:
1.  **`agent_node`:** Đây là "bộ não". Nó gọi LLM với lịch sử hội thoại hiện tại. Phản hồi của LLM sẽ là câu trả lời cuối cùng hoặc một yêu cầu gọi một tool.
2.  **`tool_node`:** Đây là "đôi tay". Nó tiếp nhận yêu cầu gọi tool từ `agent_node`, thực thi tool tương ứng, và trả về kết quả đầu ra. Chúng ta sẽ sử dụng `ToolNode` có sẵn của LangGraph cho việc này.

```python
def agent_node(state: AgentState):
    """Node chính thực hiện gọi LLM để quyết định hành động tiếp theo."""
    console.print("--- AGENT: Thinking... ---")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# ToolNode là một node có sẵn từ LangGraph thực hiện việc chạy các tool
tool_node = ToolNode(tools)

print("Agent node and Tool node have been defined.")
```

### Step 2.4: Defining the Conditional Router
**Những gì chúng ta sẽ làm:**
Sau khi `agent_node` chạy, chúng ta cần quyết định đi đâu tiếp theo. Hàm router kiểm tra message cuối cùng từ agent. Nếu message đó chứa attribute `tool_calls`, điều đó có nghĩa là agent muốn sử dụng một tool, vì vậy chúng ta route đến `tool_node`. Nếu không, điều đó có nghĩa là agent đã có câu trả lời cuối cùng, và chúng ta có thể kết thúc workflow.

```python
def router_function(state: AgentState) -> str:
    """Kiểm tra message cuối cùng của agent để quyết định bước tiếp theo."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        # Agent đã yêu cầu một cuộc gọi tool
        console.print("--- ROUTER: Decision is to call a tool. ---")
        return "call_tool"
    else:
        # Agent đã cung cấp câu trả lời cuối cùng
        console.print("--- ROUTER: Decision is to finish. ---")
        return "__end__"

print("Router function defined.")
```

## Phase 3: Assembling and Running the Workflow
Bây giờ chúng ta sẽ kết nối tất cả các thành phần lại với nhau thành một graph hoàn chỉnh, có thể thực thi và chạy nó trên một truy vấn buộc agent phải sử dụng khả năng tìm kiếm web mới của mình.

### Step 3.1: Building and Visualizing the Graph
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ tạo `StateGraph` và thêm các node cùng các edge của mình. Phần then chốt là conditional edge sử dụng `router_function` của chúng ta để tạo ra vòng lặp suy luận chính của agent: `agent -> router -> tool -> agent`.

```python
graph_builder = StateGraph(AgentState)

# Thêm các node
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("call_tool", tool_node)

# Thiết lập điểm bắt đầu
graph_builder.set_entry_point("agent")

# Thêm conditional router
graph_builder.add_conditional_edges(
    "agent",
    router_function,
)

# Thêm edge từ tool node quay lại agent để hoàn tất vòng lặp
graph_builder.add_edge("call_tool", "agent")

# Compile graph
tool_agent_app = graph_builder.compile()

print("Tool-using agent graph compiled successfully!")

# Hình ảnh hóa graph
try:
    from IPython.display import Image, display
    png_image = tool_agent_app.get_graph().draw_png()
    display(Image(png_image))
except Exception as e:
    print(f"Graph visualization failed: {e}. Please ensure pygraphviz is installed.")
```

**Discussion of the Output:**
Graph đã hoàn tất việc compile và sẵn sàng hoạt động. Hình ảnh hóa cho thấy rõ ràng vòng lặp suy luận của agent. Quy trình bắt đầu tại node `agent`. Conditional edge (được đại diện bởi hình thoi) sau đó sẽ route luồng công việc. Nếu cần một tool, nó sẽ đi đến node `call_tool`, và kết quả đầu ra được đưa ngược lại node `agent` để tổng hợp. Nếu không cần tool nào, quy trình sẽ đi tới `__end__`. Cấu trúc này triển khai hoàn hảo pattern Tool Use.

### Step 3.2: End-to-End Execution
**Những gì chúng ta sẽ làm:**
Hãy chạy agent với một câu hỏi mà nó không thể biết được từ dữ liệu training của mình, buộc nó phải sử dụng tool tìm kiếm web. Chúng ta sẽ stream các bước trung gian để theo dõi quá trình suy luận của nó diễn ra.

```python
user_query = "What were the main announcements from Apple's latest WWDC event?"
initial_input = {"messages": [("user", user_query)]}

console.print(f"[bold cyan]🚀 Kicking off Tool Use workflow for request:[/bold cyan] '{user_query}'\n")

for chunk in tool_agent_app.stream(initial_input, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
    console.print("\n---\n")

console.print("\n[bold green]✅ Tool Use workflow complete![/bold green]")
```

## Phase 4: Evaluation
Bây giờ agent đã chạy xong, chúng ta có thể evaluate hiệu năng của nó. Đối với một agent sử dụng tool, chúng ta quan tâm đến hai điều: liệu nó có sử dụng các tool của mình một cách chính xác không, và câu trả lời cuối cùng – vốn được tổng hợp từ kết quả đầu ra của tool – có đạt chất lượng cao không?

### Step 4.1: Analyzing the Execution Trace
**Những gì chúng ta sẽ làm:**
Bằng cách xem kết quả được stream ở bước trước, chúng ta có thể trace chính xác quá trình tư duy của agent. Kết quả cho thấy các loại message khác nhau (`AIMessage` với `tool_calls`, `ToolMessage` với các kết quả) luân chuyển qua graph state.

**Discussion of the Output:**
Execution trace cho thấy rõ ràng pattern Tool Use đang hoạt động:
1.  Message đầu tiên được in ra là từ node `agent`. Đó là một `AIMessage` chứa attribute `tool_calls`, cho thấy LLM đã quyết định chính xác việc sử dụng tool `web_search`.
2.  Message tiếp theo là một `ToolMessage`. Đây là kết quả đầu ra từ `tool_node` sau khi nó thực hiện tìm kiếm và trả về các kết quả thô.
3.  Message cuối cùng là một `AIMessage` khác, nhưng lần này không có `tool_calls`. Đây là lúc agent tổng hợp thông tin từ `ToolMessage` thành một câu trả lời cuối cùng, mạch lạc cho người dùng.
Trace này xác nhận rằng logic của agent và việc routing của graph đã hoạt động hoàn hảo.

### Step 4.2: Evaluating with LLM-as-a-Judge
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ tạo một LLM 'Judge' (Giám khảo) để cung cấp một bản evaluation có cấu trúc, mang tính định lượng về hiệu năng của agent. Các tiêu chí evaluation sẽ được điều chỉnh cụ thể để đánh giá chất lượng của việc sử dụng tool.

```python
class ToolUseEvaluation(BaseModel):
    """Schema để đánh giá việc sử dụng tool của agent và câu trả lời cuối cùng."""
    tool_selection_score: int = Field(description="Score 1-5 on whether the agent chose the correct tool for the task.")
    tool_input_score: int = Field(description="Score 1-5 on how well-formed and relevant the input to the tool was.")
    synthesis_quality_score: int = Field(description="Score 1-5 on how well the agent integrated the tool's output into its final answer.")
    justification: str = Field(description="A brief justification for the scores.")

judge_llm = llm.with_structured_output(ToolUseEvaluation)

# Để đánh giá, chúng ta cần tái lập conversation trace đầy đủ
final_answer = tool_agent_app.invoke(initial_input)
conversation_trace = "\n".join([f"{m.type}: {m.content or ''} {getattr(m, 'tool_calls', '')}" for m in final_answer['messages']])

def evaluate_tool_use(trace: str):
    prompt = f"""You are an expert judge of AI agents. Evaluate the following conversation trace based on the agent's tool use on a scale of 1-5. Provide a brief justification.
    
    Conversation Trace:
    ```
    {trace}
    ```
    """
    return judge_llm.invoke(prompt)

console.print("--- Evaluating Tool Use Performance ---")
evaluation = evaluate_tool_use(conversation_trace)
console.print(evaluation.model_dump())
```

**Discussion of the Output:**
LLM-as-a-Judge cung cấp một bản đánh giá có cấu trúc và có lý lẽ về hiệu năng của agent của chúng ta. Các điểm số cao trên cả ba danh mục—`tool_selection_score`, `tool_input_score`, và `synthesis_quality_score`—xác nhận rằng agent của chúng ta không chỉ đang sử dụng các tool, mà còn sử dụng chúng một cách *hiệu quả*. Nó đã xác định chính xác nhu cầu tìm kiếm web, xây dựng một truy vấn phù hợp, và tổng hợp thành công các sự thật đã truy xuất được thành một câu trả lời cuối cùng hữu ích và chính xác. Bản evaluation tự động này giúp chúng ta tin tưởng vào mức độ mạnh mẽ của việc triển khai.

## Conclusion
Trong notebook này, chúng ta đã xây dựng một agent hoàn chỉnh, đang hoạt động dựa trên kiến trúc **Tool Use**. Chúng ta đã trang bị thành công cho một LLM chạy trên Nebius một tool tìm kiếm web và sử dụng LangGraph để tạo ra một vòng lặp suy luận mạnh mẽ, cho phép agent quyết định khi nào và làm thế nào để sử dụng nó.

Việc thực thi từ đầu đến cuối và quá trình đánh giá sau đó chứng minh giá trị to lớn của pattern này. Bằng cách kết nối agent của mình với thông tin thực tế bên ngoài, chúng ta đã vượt qua được giới hạn của dữ liệu training tĩnh một cách cơ bản. Agent giờ đây không còn chỉ là một bộ máy suy luận; nó là một nhà nghiên cứu, có khả năng đưa ra những câu trả lời có cơ sở, thực tế và cập nhật. Kiến trúc này là một khối xây dựng nền tảng để tạo ra hầu hết mọi AI assistant thực tiễn trong thế giới thực.
