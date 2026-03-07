# 📘 Agentic Architectures 3: ReAct (Reason + Act)

Chào mừng bạn đến với notebook thứ ba trong loạt bài này. Bây giờ chúng ta sẽ khám phá **ReAct**, một kiến trúc then chốt thu hẹp khoảng cách giữa việc sử dụng tool đơn giản và việc giải quyết các vấn đề phức tạp, nhiều bước. ReAct là viết tắt của **Reason + Act**, và sự đổi mới cốt lõi của nó là cách nó cho phép một agent suy luận (reason) về một vấn đề một cách năng động, hành động (act) dựa trên suy luận đó, quan sát kết quả, và sau đó suy luận lại.

Pattern này biến một agent từ một bộ gọi tool tĩnh thành một bộ giải quyết vấn đề thích ứng. Để làm nổi bật sức mạnh của nó, trước tiên chúng ta sẽ xây dựng một **basic, single-shot tool-using agent** và chỉ ra những hạn chế của nó đối với một nhiệm vụ phức tạp. Sau đó, chúng ta sẽ xây dựng một ReAct agent hoàn chỉnh và chứng minh cách vòng lặp `think -> act -> observe` của nó giúp nó thành công ở những nơi mà basic agent thất bại.

### Definition
Kiến trúc **ReAct** là một design pattern nơi một agent xen kẽ các bước reasoning với các action. Thay vì lập kế hoạch cho tất cả các bước ngay từ đầu, agent tạo ra một suy nghĩ (thought) về bước tiếp theo ngay lập tức, thực hiện một action (như gọi một tool), quan sát kết quả, và sau đó sử dụng thông tin mới đó để tạo ra suy nghĩ và action tiếp theo. Điều này tạo ra một vòng lặp năng động và có khả năng thích ứng.

### High-level Workflow
1.  **Receive Goal:** Agent nhận một nhiệm vụ phức tạp.
2.  **Think (Reason):** Agent tạo ra một suy nghĩ nội bộ, chẳng hạn như: *"Để trả lời điều này, trước tiên tôi cần tìm thông tin X."*
3.  **Act:** Dựa trên suy nghĩ của mình, agent thực hiện một action, thường là gọi một tool (ví dụ: `search_api('X')`).
4.  **Observe:** Agent nhận kết quả từ tool.
5.  **Repeat:** Agent tích hợp observation vào context của nó và quay lại bước 2, tạo ra một suy nghĩ mới (ví dụ: *"Được rồi, bây giờ tôi đã có X, tôi cần sử dụng nó để tìm Y."*). Vòng lặp này tiếp tục cho đến khi mục tiêu tổng thể được thỏa mãn.

### When to Use / Applications
*   **Multi-hop Question Answering:** Khi việc trả lời một câu hỏi yêu cầu tìm kiếm nhiều mẩu thông tin theo trình tự (ví dụ: "Ai là CEO của công ty sản xuất iPhone?").
*   **Web Navigation & Research:** Một agent có thể tìm kiếm một điểm bắt đầu, đọc kết quả, và sau đó quyết định một search query mới dựa trên những gì nó đã học được.
*   **Interactive Workflows:** Bất kỳ nhiệm vụ nào mà môi trường năng động và đường dẫn đầy đủ đến giải pháp không thể được biết trước.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Thích ứng & Năng động:** Có thể điều chỉnh kế hoạch của mình ngay lập tức dựa trên thông tin mới.
    *   **Xử lý sự phức tạp:** Vượt trội ở các vấn đề yêu cầu xâu chuỗi nhiều bước phụ thuộc.
*   **Weaknesses:**
    *   **Latency & Cost cao hơn:** Bao gồm nhiều lần gọi LLM tuần tự, làm cho nó chậm hơn và đắt hơn so với các phương pháp tiếp cận single-shot.
    *   **Rủi ro vòng lặp:** Một agent không được hướng dẫn tốt có thể bị mắc kẹt trong các vòng lặp suy nghĩ và hành động lặp đi lặp lại, không hiệu quả.

## Phase 0: Foundation & Setup
Chúng ta sẽ bắt đầu với quy trình thiết lập tiêu chuẩn: cài đặt các thư viện và cấu hình API keys cho Nebius, LangSmith, và công cụ tìm kiếm web Tavily của chúng ta.

### Step 0.1: Installing Core Libraries
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ cài đặt bộ thư viện tiêu chuẩn cho loạt dự án này.

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv tavily-python
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
from typing import Annotated
from dotenv import load_dotenv

# LangChain components
from langchain_nebius import ChatNebius
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

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
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - ReAct (Nebius)"

# Kiểm tra xem các key đã được thiết lập chưa
for key in ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]:
    if not os.environ.get(key):
        print(f"{key} not found. Please create a .env file and set it.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: The Basic Approach - A Single-Shot Tool User
Để hiểu tại sao ReAct lại mạnh mẽ đến vậy, trước tiên chúng ta phải xem điều gì sẽ xảy ra nếu không có nó. Chúng ta sẽ xây dựng một agent "basic" có thể sử dụng các tool, nhưng chỉ một lần duy nhất. Nó sẽ phân tích truy vấn của người dùng, thực hiện một cuộc gọi tool duy nhất, và sau đó cố gắng đưa ra câu trả lời cuối cùng dựa trên mẩu thông tin duy nhất đó.

### Step 1.1: Building the Basic Agent
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ định nghĩa cùng một tool và LLM như trước đây, nhưng chúng ta sẽ kết nối chúng thành một graph đơn giản, tuyến tính. Agent có một cơ hội để gọi một tool, và sau đó workflow kết thúc. Không có vòng lặp (loop).

```python
from typing import TypedDict

console = Console()

# Định nghĩa state cho các graph của chúng ta
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Định nghĩa tool và LLM
search_tool = TavilySearchResults(max_results=2, name="web_search")
llm = ChatNebius(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)
llm_with_tools = llm.bind_tools([search_tool])

# Định nghĩa agent node cho basic agent
def basic_agent_node(state: AgentState):
    console.print("--- BASIC AGENT: Thinking... ---")
    # Lưu ý: Chúng tôi cung cấp một system prompt để khuyến khích nó trả lời trực tiếp sau một lần gọi tool
    system_prompt = "You are a helpful assistant. You have access to a web search tool. Answer the user's question based on the tool's results. You must provide a final answer after one tool call."
    messages = [("system", system_prompt)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Định nghĩa basic, linear graph
basic_graph_builder = StateGraph(AgentState)
basic_graph_builder.add_node("agent", basic_agent_node)
basic_graph_builder.add_node("tools", ToolNode([search_tool]))

basic_graph_builder.set_entry_point("agent")
# Sau agent, nó chỉ có thể đi tới tools, và sau tools, nó BẮT BUỘC phải kết thúc.
basic_graph_builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", "__end__": "__end__"})
basic_graph_builder.add_edge("tools", END)

basic_tool_agent_app = basic_graph_builder.compile()

print("Basic single-shot tool-using agent compiled successfully.")
```

### Step 1.2: Testing the Basic Agent on a Multi-Step Problem
**Những gì chúng ta sẽ làm:**
Bây giờ chúng ta sẽ giao cho basic agent một vấn đề yêu cầu nhiều bước phụ thuộc để giải quyết. Điều này sẽ phơi bày điểm yếu cơ bản của nó.

```python
multi_step_query = "Who is the current CEO of the company that created the sci-fi movie 'Dune', and what was the budget for that company's most recent film?"

console.print(f"[bold yellow]Testing BASIC agent on a multi-step query:[/bold yellow] '{multi_step_query}'\n")

basic_agent_output = basic_tool_agent_app.invoke({"messages": [("user", multi_step_query)]})

console.print("\n--- [bold red]Final Output from Basic Agent[/bold red] ---")
console.print(Markdown(basic_agent_output['messages'][-1].content))
```

**Discussion of the Output:**
Đúng như dự đoán, basic agent đã thất bại. Cuộc gọi tool duy nhất của nó có lẽ là một tìm kiếm cho toàn bộ truy vấn dài. Kết quả tìm kiếm cho một truy vấn phức tạp, mang tính kết hợp như vậy thường lộn xộn và không chứa tất cả các mẩu thông tin cần thiết ở một nơi duy nhất.

Câu trả lời cuối cùng của agent có thể không đầy đủ, không chính xác hoặc là một tuyên bố rằng nó không thể tìm thấy thông tin. Nó đã không thể chia nhỏ vấn đề:
1.  Tìm công ty đã sản xuất 'Dune' (Legendary Entertainment).
2.  Tìm CEO của công ty đó (Joshua Grode).
3.  Tìm bộ phim gần đây nhất của công ty đó và ngân sách của nó.

Sự thất bại này minh họa hoàn hảo cho sự cần thiết của một cách tiếp cận năng động hơn. Agent cần một cách để **phản ứng (react)** lại thông tin mà nó tìm thấy ở một bước để cung cấp thông tin cho bước tiếp theo.

## Phase 2: The Advanced Approach - Implementing ReAct
Bây giờ, chúng ta sẽ xây dựng ReAct agent thực sự. Sự khác biệt cốt lõi nằm ở cấu trúc của graph: chúng ta sẽ giới thiệu một vòng lặp cho phép agent lặp đi lặp lại việc suy nghĩ, hành động và quan sát.

### Step 2.1: Building the ReAct Agent Graph
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ định nghĩa các node và hàm router quan trọng để tạo ra vòng lặp `think -> act`. Thay đổi kiến trúc then chốt là edge route kết quả đầu ra từ `tool_node` *quay lại* `agent_node`, cho phép agent xem kết quả và quyết định bước tiếp theo của nó.

```python
def react_agent_node(state: AgentState):
    console.print("--- REACT AGENT: Thinking... ---")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# ToolNode giống như trước
react_tool_node = ToolNode([search_tool])

# Router cũng cùng một logic
def react_router(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        console.print("--- ROUTER: Decision is to call a tool. ---")
        return "tools"
    console.print("--- ROUTER: Decision is to finish. ---")
    return "__end__"

# Bây giờ chúng ta định nghĩa graph với vòng lặp quan trọng
react_graph_builder = StateGraph(AgentState)
react_graph_builder.add_node("agent", react_agent_node)
react_graph_builder.add_node("tools", react_tool_node)

react_graph_builder.set_entry_point("agent")
react_graph_builder.add_conditional_edges("agent", react_router, {"tools": "tools", "__end__": "__end__"})

# Đây là sự khác biệt chính: edge đi từ tools QUAY LẠI agent
react_graph_builder.add_edge("tools", "agent")

react_agent_app = react_graph_builder.compile()
print("ReAct agent compiled successfully with a reasoning loop.")
```

## Phase 3: Head-to-Head Comparison
Bây giờ chúng ta sẽ chạy cùng một truy vấn phức tạp với ReAct agent mới của mình và quan sát sự khác biệt trong quy trình và kết quả cuối cùng.

### Step 3.1: Testing the ReAct Agent on the Multi-Step Problem
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ invoke ReAct agent với cùng một truy vấn nhiều bước và stream kết quả đầu ra để xem quá trình suy luận lặp lại của nó.

```python
console.print(f"[bold green]Testing ReAct agent on the same multi-step query:[/bold green] '{multi_step_query}'\n")

final_react_output = None
for chunk in react_agent_app.stream({"messages": [("user", multi_step_query)]}, stream_mode="values"):
    final_react_output = chunk
    console.print(f"--- [bold purple]Current State[/bold purple] ---")
    chunk['messages'][-1].pretty_print()
    console.print("\n")

console.print("\n--- [bold green]Final Output from ReAct Agent[/bold green] ---")
console.print(Markdown(final_react_output['messages'][-1].content))
```

**Discussion of the Output:**
Thành công! Execution trace cho thấy một quy trình hoàn toàn khác biệt và thông minh hơn nhiều. Bạn có thể thấy suy luận từng bước của agent:
1.  **Thought 1:** Trước tiên, nó suy luận rằng nó cần xác định công ty sản xuất bộ phim 'Dune'.
2.  **Action 1:** Nó gọi tool `web_search` với một truy vấn như "production company for Dune movie".
3.  **Observation 1:** Nó nhận được kết quả: "Legendary Entertainment".
4.  **Thought 2:** Bây giờ, tích hợp thông tin mới, nó suy luận rằng nó cần tìm CEO của Legendary Entertainment.
5.  **Action 2:** Nó gọi `web_search` một lần nữa với truy vấn như "CEO of Legendary Entertainment".
6.  ...và cứ tiếp tục như vậy, cho đến khi nó thu thập được tất cả các mẩu thông tin cần thiết.
7.  **Synthesis:** Cuối cùng, nó tập hợp tất cả các sự thật đã thu thập được thành một câu trả lời hoàn chỉnh và chính xác.

Điều này chứng minh rõ ràng sự vượt trội của ReAct pattern đối với bất kỳ nhiệm vụ nào không phải là một bước tra cứu đơn giản.

## Phase 4: Quantitative Evaluation
Để chính thức hóa việc so sánh, chúng ta sẽ sử dụng một LLM-as-a-Judge để chấm điểm kết quả cuối cùng từ cả basic agent và ReAct agent dựa trên khả năng giải quyết nhiệm vụ của chúng.

```python
class AgentEvaluation(BaseModel):
    """Schema cho việc đánh giá kết quả của agent."""
    task_completion_score: int = Field(description="Score từ 1-10 về mức độ hoàn thành nhiệm vụ.")
    reasoning_quality_score: int = Field(description="Score từ 1-10 về chất lượng suy luận.")
    justification: str = Field(description="Giải thích ngắn gọn cho các điểm số.")

judge_llm = llm.with_structured_output(AgentEvaluation)

def evaluate_agent(output_content: str):
    prompt = f"""You are an expert judge of AI agents. Evaluate the following final answer provided by an agent based on a complex, multi-step user request.
    
    User Request: {multi_step_query}
    
    Agent's Final Answer:
    {output_content}
    
    Evaluate the answer from 1-10 for task completion and reasoning quality. Provide a brief justification.
    """
    return judge_llm.invoke(prompt)

if basic_agent_output and final_react_output:
    console.print("--- Evaluating Basic Agent's Output ---")
    basic_eval = evaluate_agent(basic_agent_output['messages'][-1].content)
    console.print(basic_eval.model_dump())

    console.print("\n--- Evaluating ReAct Agent's Output ---")
    react_eval = evaluate_agent(final_react_output['messages'][-1].content)
    console.print(react_eval.model_dump())
```

**Discussion of the Output:**
Bản đánh giá định lượng xác nhận điều mà execution trace đã gợi ý: ReAct agent vượt trội hơn hẳn basic agent. Nó có khả năng hoàn thành nhiệm vụ và chất lượng suy luận cao hơn đáng kể. Thay vì đưa ra câu trả lời phỏng đoán hoặc không đầy đủ sau một lần thử, ReAct agent đã thể hiện khả năng kiên trì trong việc tìm kiếm các sự thật cụ thể cần thiết để đưa ra câu trả lời chính xác 100%.

## Conclusion
Kiến trúc **ReAct** là một bước nhảy vọt cơ sở trong khả năng của các agent. Bằng cách cho phép một tác nhân xen kẽ việc suy nghĩ và thực hiện action thông qua một vòng lặp lặp đi lặp lại năng động, chúng ta giải phóng tiềm năng của LLM để giải quyết các vấn đề phức tạp, đa dạng của thế giới thực. ReAct không chỉ là về việc sử dụng các tool; đó là về việc sử dụng chúng một cách có chiến lược và có suy luận. Mẫu kiến trúc này tạo thành trái tim của nhiều ứng dụng agentic tiên tiến nhất hiện nay.
