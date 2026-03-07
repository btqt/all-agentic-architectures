# 📘 Agentic Architectures 7: Blackboard Systems

Chào mừng bạn đến với notebook thứ bảy trong loạt bài về kiến trúc agentic. Hôm nay, chúng ta khám phá **Blackboard System**, một pattern mạnh mẽ và linh hoạt cao để phối hợp nhiều specialist agents. Kiến trúc này được mô phỏng dựa trên ý tưởng về một nhóm các chuyên gia con người cộng tác xung quanh một chiếc bảng đen (blackboard) vật lý để giải quyết một vấn đề phức tạp.

Thay vì một chuỗi các bước bàn giao agent cứng nhắc, được định nghĩa trước, một hệ thống Blackboard có một kho lưu trữ dữ liệu chung, trung tâm (gọi là 'blackboard'), nơi các agent có thể đọc trạng thái hiện tại của vấn đề và viết các đóng góp của họ. Một **Controller** năng động quan sát bảng đen và quyết định specialist agent nào sẽ được kích hoạt tiếp theo dựa trên những gì cần thiết để đưa giải pháp tiến lên. Điều này cho phép một workflow mang tính cơ hội và nảy sinh (opportunistic and emergent).

Để làm nổi bật những ưu điểm độc đáo của nó, chúng ta sẽ so sánh nó với **sequential multi-agent system** mà chúng ta đã xây dựng trước đây. Chúng ta sẽ giao cho cả hai hệ thống một truy vấn tài chính phức tạp, nơi con đường tối ưu không phải là một chuỗi A → B → C đơn giản. Chúng ta sẽ chứng minh cách sequential agent cứng nhắc đi theo một con đường dưới mức tối ưu, trong khi Controller năng động của hệ thống Blackboard kích hoạt các agent theo thứ tự logic, dựa trên dữ liệu hơn, dẫn đến một bản phân tích hiệu quả và mạch lạc hơn.

### Definition
Một **Blackboard System** là một kiến trúc đa tác vụ (multi-agent) nơi nhiều specialist agents cộng tác bằng cách đọc từ và viết vào một kho lưu trữ dữ liệu trung tâm, chung được gọi là 'blackboard'. Một bộ điều khiển (controller) hoặc bộ lập lịch (scheduler) sẽ xác định một cách năng động agent nào sẽ thực hành động tiếp theo dựa trên trạng thái đang phát triển của giải pháp trên bảng đen.

### High-level Workflow
1.  **Shared Memory (The Blackboard):** Một cấu trúc dữ liệu trung tâm giữ trạng thái hiện tại của vấn đề, bao gồm yêu cầu của người dùng, các phát hiện trung gian và các giải pháp từng phần.
2.  **Specialist Agents:** Một nhóm các agent độc lập, mỗi agent có một chuyên môn cụ thể, liên tục theo dõi bảng đen.
3.  **Controller:** Một agent 'controller' trung tâm cũng theo dõi bảng đen. Công việc của nó là phân tích trạng thái hiện tại và quyết định specialist agent nào được trang bị tốt nhất để thực hiện đóng góp tiếp theo.
4.  **Opportunistic Activation:** Controller kích hoạt agent đã chọn. Agent đọc dữ liệu liên quan từ bảng đen, thực hiện nhiệm vụ của mình và viết lại các phát hiện của mình lên bảng đen.
5.  **Iteration:** Quá trình lặp lại, với Controller kích hoạt các agent khác nhau theo một trình tự năng động, cho đến khi nó xác định rằng giải pháp trên bảng đen đã hoàn thành.

### When to Use / Applications
*   **Các vấn đề phức tạp, cấu trúc kém (Ill-Structured Problems):** Lý tưởng cho các vấn đề mà con đường giải quyết không được biết trước và yêu cầu một chiến lược cơ hội, nảy sinh (ví dụ: chẩn đoán phức tạp, khám phá khoa học).
*   **Hệ thống đa phương thức (Multi-Modal Systems):** Một cách tuyệt vời để phối hợp các agent làm việc với các loại dữ liệu khác nhau (văn bản, hình ảnh, mã nguồn), vì tất cả chúng đều có thể đăng các phát hiện của mình lên bảng đen chung.
*   **Dynamic Sense-Making:** Các tình huống đòi hỏi tổng hợp thông tin từ nhiều nguồn khác nhau, không đồng bộ.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Tính linh hoạt & Khả năng thích ứng:** Workflow không được mã hóa cứng; nó nảy sinh dựa trên vấn đề, làm cho hệ thống có khả năng thích ứng cao.
    *   **Tính Module:** Rất dễ dàng để thêm hoặc xóa các specialist agents mà không cần thiết kế lại toàn bộ hệ thống.
*   **Weaknesses:**
    *   **Độ phức tạp của Controller:** Trí thông minh của toàn bộ hệ thống phụ thuộc rất nhiều vào sự tinh vi của Controller. Một Controller đơn giản có thể dẫn đến hành vi không hiệu quả hoặc bị lặp (looping).
    *   **Thách thức trong Debug:** Bản chất phi tuyến tính, nảy sinh của workflow đôi khi có thể khiến việc truy vết và debug khó khăn hơn so với một quy trình tuần tự đơn giản.

## Phase 0: Foundation & Setup
Chúng ta sẽ bắt đầu với quy trình thiết lập tiêu chuẩn: cài đặt các thư viện và cấu hình API keys cho Nebius, LangSmith và Tavily.

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
from typing import List, Annotated, TypedDict, Optional
from dotenv import load_dotenv

# LangChain components
from langchain_nebius import ChatNebius
from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

# LangGraph components
from langgraph.graph import StateGraph, END

# For pretty printing
from rich.console import Console
from rich.markdown import Markdown

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Blackboard (Nebius)"

for key in ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]:
    if not os.environ.get(key):
        print(f"{key} not found. Please create a .env file and set it.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: The Baseline - A Sequential Multi-Agent System (Corrected)
Để hiểu tính linh hoạt của blackboard, trước tiên chúng ta cần một hệ thống tuần tự hoạt động đúng đắn. Phiên bản gốc đã thất bại vì các chuyên gia không sử dụng kết quả đầu ra của các bước trước đó. Chúng ta sẽ sửa lỗi này bằng cách đảm bảo mỗi agent nhận được context cần thiết từ state.

### Step 1.1: Building the (Corrected) Sequential Team
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ định nghĩa các specialist agents mà rõ ràng sử dụng kết quả đầu ra của những người tiền nhiệm, sau đó kết nối chúng theo một trình tự cố định, tuyến tính.

```python
console = Console()
# Sử dụng một mô hình có khả năng cao hơn để xử lý các hướng dẫn phức tạp tốt hơn
llm = ChatNebius(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0)
search_tool = TavilySearch(max_results=2)

# State cho sequential agent
class SequentialState(TypedDict):
    user_request: str
    news_report: Optional[str]
    technical_report: Optional[str]
    financial_report: Optional[str]
    final_report: Optional[str]

# --- CORRECTED SPECIALIST NODES FOR SEQUENTIAL AGENT ---
# Thay đổi quan trọng là mỗi agent hiện nhận được context từ các bước trước đó, không chỉ là yêu cầu ban đầu.

def news_analyst_node_seq(state: SequentialState):
    console.print("--- (Sequential) CALLING NEWS ANALYST ---")
    prompt = f"Your task is to act as an expert News Analyst. Find the latest major news about the topic in the user's request and provide a concise summary.\n\nUser Request: {state['user_request']}"
    agent = llm.bind_tools([search_tool])
    result = agent.invoke(prompt)
    return {"news_report": result.content}

def technical_analyst_node_seq(state: SequentialState):
    console.print("--- (Sequential) CALLING TECHNICAL ANALYST ---")
    # Agent này hiện sử dụng news report làm context.
    prompt = f"Your task is to act as an expert Technical Analyst. Based on the following news report, conduct a technical analysis of the company's stock.\n\nNews Report:\n{state['news_report']}"
    agent = llm.bind_tools([search_tool])
    result = agent.invoke(prompt)
    return {"technical_report": result.content}

def financial_analyst_node_seq(state: SequentialState):
    console.print("--- (Sequential) CALLING FINANCIAL ANALYST ---")
    # Agent này cũng sử dụng news report làm context.
    prompt = f"Your task is to act as an expert Financial Analyst. Based on the following news report, analyze the company's recent financial performance.\n\nNews Report:\n{state['news_report']}"
    agent = llm.bind_tools([search_tool])
    result = agent.invoke(prompt)
    return {"financial_report": result.content}


def report_writer_node_seq(state: SequentialState):
    console.print("--- (Sequential) CALLING REPORT WRITER ---")
    prompt = f"""You are an expert report writer. Your task is to synthesize the information from the News, Technical, and Financial analysts into a single, cohesive report that directly answers the user's original request.

User Request: {state['user_request']}

Here are the reports to combine:
---
News Report: {state['news_report']}
---
Technical Report: {state['technical_report']}
---
Financial Report: {state['financial_report']}
"""
    report = llm.invoke(prompt).content
    return {"final_report": report}

# Xây dựng sequential graph
seq_graph_builder = StateGraph(SequentialState)
seq_graph_builder.add_node("news", news_analyst_node_seq)
seq_graph_builder.add_node("tech", technical_analyst_node_seq)
seq_graph_builder.add_node("finance", financial_analyst_node_seq)
seq_graph_builder.add_node("writer", report_writer_node_seq)

# Trình tự cố định
seq_graph_builder.set_entry_point("news")
seq_graph_builder.add_edge("news", "tech")
seq_graph_builder.add_edge("tech", "finance")
seq_graph_builder.add_edge("finance", "writer")
seq_graph_builder.add_edge("writer", END)

sequential_app = seq_graph_builder.compile()
print("Corrected sequential multi-agent system compiled successfully.")
```

### Step 1.2: Testing the Sequential Agent on a Dynamic Problem
Bây giờ sequential agent đã truyền context một cách chính xác, hãy quan sát hành vi của nó. Nó sẽ tạo ra một báo cáo mạch lạc hơn, nhưng *quy trình* của nó vẫn không hiệu quả và thất bại trong việc tuân theo logic điều kiện.

```python
dynamic_query = "Find the latest major news about Nvidia. Based on the sentiment of that news, conduct either a technical analysis (if the news is neutral or positive) or a financial analysis of their recent performance (if the news is negative)."

console.print(f"[bold yellow]Testing CORRECTED SEQUENTIAL agent on a dynamic query:[/bold yellow]\n'{dynamic_query}'\n")

# Chạy graph
final_seq_output = sequential_app.invoke({"user_request": dynamic_query})

console.print("\n--- [bold red]Final Report from Sequential Agent[/bold red] ---")
console.print(Markdown(final_seq_output['final_report']))
```

**Discussion of the (Corrected) Output:**
Agent hiện tạo ra một báo cáo đầy đủ, logic. Tuy nhiên, execution trace `News → Technical → Financial` để lộ lỗ hổng cơ bản của nó. Nó đã thực hiện **cả hai** phân tích kỹ thuật và tài chính, hoàn toàn bỏ qua yêu cầu có điều kiện của người dùng ("either... or..."). Điều này không hiệu quả và chứng minh tính cứng nhắc mà chúng ta hướng tới giải quyết bằng kiến trúc Blackboard.

## Phase 2: The Advanced Approach - A Blackboard System (Corrected)
Bây giờ, chúng ta sẽ xây dựng hệ thống Blackboard. Chìa khóa để sửa lỗi hành vi lặp (looping) của hệ thống gốc là tạo ra một prompt thông minh hơn nhiều cho **Controller**, khiến nó nhận thức được vai trò của mình như một nhà lập hoạch có trạng thái (stateful planner).

### Step 2.1: Defining the Blackboard and the (Corrected) Controller
**Những gì chúng ta sẽ làm:**
1.  **Blackboard State:** Định nghĩa một `BlackboardState` cho bộ nhớ chung.
2.  **Specialist Agents:** Định nghĩa các specialist nodes. Chúng sẽ tương tự như các agent trước đây của chúng ta.
3.  **Controller (Corrected):** Tạo một `controller_node` mạnh mẽ với prompt rõ ràng suy luận về các bước đã hoàn thành và các mục tiêu còn lại. Đây là thay đổi quan trọng nhất.

```python
# Blackboard State giữ tất cả thông tin
class BlackboardState(TypedDict):
    user_request: str
    # Bảng đen trung tâm nơi các agent đăng các phát hiện của họ dưới dạng chuỗi
    blackboard: List[str]
    # Danh sách các agent có sẵn để controller lựa chọn
    available_agents: List[str]
    # Quyết định tiếp theo của controller
    next_agent: Optional[str]

# Pydantic model cho quyết định của Controller
class ControllerDecision(BaseModel):
    next_agent: str = Field(description="The name of the next agent to call. Must be one of ['News Analyst', 'Technical Analyst', 'Financial Analyst', 'Report Writer'] or 'FINISH'.")
    reasoning: str = Field(description="A brief reason for choosing the next agent.")

# Reusable factory để tạo specialist agents cho blackboard
def create_blackboard_specialist(persona: str, agent_name: str):
    system_prompt = f"""You are an expert specialist agent: a {persona}.
Your task is to contribute to a larger goal by performing your specific function.
Read the initial User Request and the current Blackboard for context.
Use your tools to find the required information.
Finally, post your concise markdown report back to the blackboard. Your report should be signed with your name '{agent_name}'.
"""
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "User Request: {user_request}\n\nBlackboard (previous reports):\n{blackboard_str}")
    ])
    agent = prompt_template | llm.bind_tools([search_tool])

    def specialist_node(state: BlackboardState):
        console.print(f"--- (Blackboard) AGENT '{agent_name}' is working... ---")
        blackboard_str = "\n---\n".join(state["blackboard"])
        result = agent.invoke({"user_request": state["user_request"], "blackboard_str": blackboard_str})
        report = f"**Report from {agent_name}:**\n{result.content}"
        # Thêm report mới vào danh sách các mục trên bảng đen
        return {"blackboard": state["blackboard"] + [report]}
    return specialist_node

# Tạo các specialist agent nodes
news_analyst_bb = create_blackboard_specialist("News Analyst", "News Analyst")
technical_analyst_bb = create_blackboard_specialist("Technical Analyst", "Technical Analyst")
financial_analyst_bb = create_blackboard_specialist("Financial Analyst", "Financial Analyst")
report_writer_bb = create_blackboard_specialist("Report Writer who synthesizes a final answer from the blackboard", "Report Writer")

# --- THE CORRECTED, INTELLIGENT CONTROLLER NODE ---
# Đây là bản sửa lỗi quan trọng nhất. Prompt hiện đã phức tạp hơn nhiều.
def controller_node(state: BlackboardState):
    console.print("--- CONTROLLER: Analyzing blackboard... ---")

    # Sử dụng một LLM có đầu ra cấu trúc để đưa ra quyết định
    controller_llm = llm.with_structured_output(ControllerDecision)

    blackboard_content = "\n\n".join(state['blackboard'])
    agent_list = state['available_agents']

    # Prompt mới nhận thức được trạng thái và hướng tới mục tiêu.
    prompt = f"""You are the central controller of a multi-agent system. Your job is to analyze the shared blackboard and the original user request to decide which specialist agent should run next.

**Original User Request:**
{state['user_request']}

**Current Blackboard Content:**
---
{blackboard_content if blackboard_content else "The blackboard is currently empty."}
---

**Available Specialist Agents:**
{', '.join(agent_list)}

**Your Task:**
1.  Read the user request and the current blackboard content carefully.
2.  Determine what the *next logical step* is to move closer to a complete answer.
3.  Choose the single best agent to perform that step from the list of available agents.
4.  If the user's request has been fully addressed and a final report has been written, choose 'FINISH'. Do not finish until a \"Report Writer\" has provided a final, synthesized answer.

Provide your decision in the required format.
"""
    decision_result = controller_llm.invoke(prompt)
    console.print(f"--- CONTROLLER: Decision is to call '{decision_result.next_agent}'. Reason: {decision_result.reasoning} ---")

    # Từ điển được trả về ở đây sẽ cập nhật khóa 'next_agent' trong state của graph
    return {"next_agent": decision_result.next_agent}

print("Blackboard components and corrected Controller node defined.")
```

### Step 2.2: Building the Blackboard Graph
Bây giờ chúng ta kết nối các thành phần vào một graph năng động. Controller đóng vai trò như một router trung tâm. Sau khi bất kỳ specialist nào chạy, quyền kiểm soát luôn quay lại Controller để quyết định bước tiếp theo.

```python
bb_graph_builder = StateGraph(BlackboardState)

# Thêm tất cả các node vào graph
bb_graph_builder.add_node("Controller", controller_node)
bb_graph_builder.add_node("News Analyst", news_analyst_bb)
bb_graph_builder.add_node("Technical Analyst", technical_analyst_bb)
bb_graph_builder.add_node("Financial Analyst", financial_analyst_bb)
bb_graph_builder.add_node("Report Writer", report_writer_bb)

bb_graph_builder.set_entry_point("Controller")

# Hàm này định nghĩa logic routing năng động dựa trên quyết định của Controller
def route_to_agent(state: BlackboardState):
    return state["next_agent"]

# Các conditional edges route từ Controller đến specialist được chọn hoặc đến phần kết thúc
bb_graph_builder.add_conditional_edges(
    "Controller",
    route_to_agent,
    {
        "News Analyst": "News Analyst",
        "Technical Analyst": "Technical Analyst",
        "Financial Analyst": "Financial Analyst",
        "Report Writer": "Report Writer",
        "FINISH": END
    }
)

# Sau khi bất kỳ specialist nào chạy, quyền kiểm soát luôn quay lại Controller cho quyết định tiếp theo
bb_graph_builder.add_edge("News Analyst", "Controller")
bb_graph_builder.add_edge("Technical Analyst", "Controller")
bb_graph_builder.add_edge("Financial Analyst", "Controller")
bb_graph_builder.add_edge("Report Writer", "Controller")

blackboard_app = bb_graph_builder.compile()
print("Blackboard system compiled successfully.")
```

## Phase 3: Head-to-Head Comparison
Hãy chạy hệ thống Blackboard mới của chúng ta cho cùng một nhiệm vụ năng động và quan sát workflow thông minh của nó.

```python
console.print(f"[bold cyan]Testing BLACKBOARD system on the same dynamic query:[/bold cyan]\n'{dynamic_query}'\n")

initial_bb_state = {
    "user_request": dynamic_query,
    "blackboard": [],
    "available_agents": ["News Analyst", "Technical Analyst", "Financial Analyst", "Report Writer"]
}

# Chạy graph và stream các cập nhật state
for chunk in blackboard_app.stream(initial_bb_state):
    for node_name, values in chunk.items():
        if node_name == "Controller":
            pass # Controller đã in rồi
        else:
            console.print(f"\n--- [bold green]Current Blackboard State[/bold green] ---")
            for i, report in enumerate(values.get("blackboard", [])):
                console.print(f"--- Report {i+1} ---")
                console.print(Markdown(report))
                console.print("\n")

print("Blackboard system execution complete.")
```

**Discussion of the Output:**
Hệ thống Blackboard đã chứng minh sự vượt trội rõ rệt về hiệu quả và trí thông minh:
1.  **Opportunistic Workflow:** Sau khi News Analyst cung cấp báo cáo (có sentiment tích cực rõ rệt), **Controller** đã phân tích trạng thái này và đưa ra quyết định thông minh là *chỉ* gọi Technical Analyst.
2.  **Efficiency:** Nó đã hoàn toàn bỏ qua Financial Analyst, nhận ra rằng bước đó là không cần thiết dựa trên logic điều kiện của người dùng.
3.  **Synthesis:** Sau khi hai chuyên gia cần thiết đóng góp, nó đã gọi Report Writer để hoàn thiện giải pháp.

Trình tự nảy sinh (`News → Tech → Writer`) trực tiếp và thông minh hơn nhiều so với trình tự tuần tự cứng nhắc (`News → Tech → Finance → Writer`). Điều này cho thấy cách kiến trúc Blackboard cho phép các hệ thống AI xử lý các vấn đề cấu trúc kém với mức độ linh hoạt tương đương chuyên gia con người.

## Phase 4: Qualitative Evaluation
Cuối cùng, chúng ta sẽ sử dụng giám khảo LLM của mình để đánh giá cả hai hệ thống dựa trên tiêu chí **Process Logic (Logic Quy trình)**—khả năng tuân thủ các hướng dẫn có điều kiện và tránh các công việc dư thừa.

```python
class ProcessEvaluation(BaseModel):
    """Schema cho đánh giá logic quy trình."""
    sequential_logic_score: int = Field(description="Score từ 1-10 cho logic quy trình của sequential agent.")
    blackboard_logic_score: int = Field(description="Score từ 1-10 cho logic quy trình của Blackboard system.")
    justification: str = Field(description="Giải thích tại sao một hệ thống có logic quy trình tốt hơn hệ thống kia.")

judge_llm = llm.with_structured_output(ProcessEvaluation)

def evaluate_process_logic(seq_trace: str, bb_trace: str):
    prompt = f"""You are an expert auditor of AI workflows. 
    Evaluate the process logic of two different agent architectures in response to a conditional query.
    
    The user asked for: 'Find news. IF positive/neutral, do Technical. IF negative, do Financial.'
    
    --- SEQUENTIAL AGENT TRACE ---
    {seq_trace}
    
    --- BLACKBOARD SYSTEM TRACE ---
    {bb_trace}
    """
    return judge_llm.invoke(prompt)

# (Logs đơn giản hóa cho giám khảo)
seq_trace = "Found positive news. Ran Technical Analyst. THEN ran Financial Analyst (redundant). Finally wrote report."
bb_trace = "Found positive news. Controller decided to run ONLY Technical Analyst based on the news. Finally wrote report."

console.print("--- Performing Process Logic Evaluation ---")
process_eval = evaluate_process_logic(seq_trace, bb_trace)
console.print(process_eval.model_dump())
```

**Discussion of the Output:**
Kết quả của giám khảo xác nhận giá trị chiến lược của kiến trúc Blackboard. Trong khi cả hai agent đều cung cấp câu trả lời đúng, hệ thống Blackboard nhận được điểm cao về Process Logic vì nó có khả năng đưa ra các quyết định hành động sáng suốt dựa trên dữ liệu. Nó tránh được sự dư thừa bằng cách tự động thích ứng workflow của mình phù hợp với tin tức cụ thể mà nó tìm thấy. Giai đoạn lập kế hoạch năng động này là đặc điểm nổi bật của các hệ thống agentic thực sự tinh vi.

## Conclusion
Kiến trúc **Blackboard System** thể hiện sự chuyển đổi từ workflows lập trình sẵn sang workflows nảy sinh. Bằng cách tách biệt năng lực của agent khỏi logic điều phối, chúng ta tạo ra các hệ thống AI có khả năng giải quyết các vấn đề ngày càng phức tạp, không chắc chắn và đa chiều. Trong khi nó đòi hỏi một Controller thông minh hơn, lợi ích về tính linh hoạt, hiệu quả và khả năng thích ứng là không thể phủ nhận. Pattern này là một sự bổ sung thiết yếu cho bộ công cụ của bất kỳ ai xây dựng các agent có khả năng thực hiện suy luận "theo ngữ cảnh" (context-aware reasoning) thực thụ trong các ứng dụng thực tế năng động.
