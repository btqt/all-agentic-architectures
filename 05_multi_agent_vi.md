# 📘 Agentic Architectures 5: Multi-Agent Systems

Trong notebook này, chúng ta tiến tới một trong những kiến trúc mạnh mẽ và linh hoạt nhất: **Multi-Agent System**. Pattern này vượt qua khái niệm về một agent đơn lẻ, bất kể nó phức tạp đến đâu, và thay vào đó mô hình hóa một nhóm gồm các specialized agents cộng tác với nhau để giải quyết một vấn đề. Mỗi agent có một vai trò, persona và bộ kỹ năng riêng biệt, mô phỏng cách làm việc của các nhóm chuyên gia con người.

Cách tiếp cận này cho phép thực hiện "phân công lao động" (division of labor) một cách sâu sắc, nơi các vấn đề phức tạp được chia nhỏ thành các nhiệm vụ phụ và giao cho agent phù hợp nhất với công việc đó. Để giới thiệu sức mạnh của nó, chúng ta sẽ thực hiện một so sánh trực tiếp. Đầu tiên, chúng ta sẽ giao cho một **monolithic 'generalist' agent** duy nhất nhiệm vụ tạo ra một báo cáo phân tích thị trường toàn diện. Sau đó, chúng ta sẽ tập hợp một **specialist team**—bao gồm một Technical Analyst, một News Analyst và một Financial Analyst—và để agent 'Manager' thứ tư tổng hợp các thông tin đầu vào chuyên môn của họ thành một báo cáo cuối cùng. Sự khác biệt về chất lượng, cấu trúc và chiều sâu sẽ hiển hiện ngay lập tức.

### Definition
Một **Multi-Agent System** là một kiến trúc nơi một nhóm các specialized agents riêng biệt, chuyên môn hóa cộng tác (hoặc đôi khi cạnh tranh) để đạt được một mục tiêu chung. Một bộ điều khiển trung tâm hoặc một giao thức workflow đã được định nghĩa được sử dụng để quản lý giao tiếp và route các nhiệm vụ giữa các agent.

### High-level Workflow
1.  **Decomposition:** Một bộ điều khiển chính hoặc người dùng cung cấp một nhiệm vụ phức tạp.
2.  **Role Definition:** Hệ thống giao các nhiệm vụ phụ cho các specialized agents dựa trên vai trò đã định nghĩa của họ (ví dụ: 'Researcher', 'Coder', 'Critic', 'Writer').
3.  **Collaboration:** Các agent thực thi các nhiệm vụ của mình, thường là song song hoặc tuần tự. Họ chuyển kết quả đầu ra cho nhau hoặc cho một 'blackboard' trung tâm.
4.  **Synthesis:** Một agent 'manager' hoặc 'synthesizer' cuối cùng thu thập các kết quả đầu ra từ các chuyên gia và lắp ráp thành một phản hồi cuối cùng, hợp nhất.

### When to Use / Applications
*   **Complex Report Generation:** Tạo ra các báo cáo chi tiết yêu cầu kiến thức chuyên môn từ nhiều lĩnh vực (ví dụ: phân tích tài chính, nghiên cứu khoa học).
*   **Software Development Pipelines:** Mô phỏng một nhóm phát triển với một lập trình viên, một người review code, một tester và một quản lý dự án.
*   **Creative Brainstorming:** Một nhóm các agent với các 'personalities' khác nhau (ví dụ: một người lạc quan, một người thận trọng, một người cực kỳ sáng tạo) có thể tạo ra một bộ ý tưởng đa dạng hơn.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Specialization & Depth:** Mỗi agent có thể được tinh chỉnh với một persona và tool cụ thể, dẫn đến công việc chất lượng cao hơn trong lĩnh vực của nó.
    *   **Tính module & Khả năng mở rộng:** Dễ dàng thêm, xóa hoặc nâng cấp các agent riêng lẻ mà không cần thiết kế lại toàn bộ hệ thống.
    *   **Tính song song (Parallelism):** Nhiều agent có thể làm việc trên các nhiệm vụ phụ của mình cùng một lúc, tiềm năng giảm tổng thời gian thực hiện nhiệm vụ.
*   **Weaknesses:**
    *   **Chi phí điều phối (Coordination Overhead):** Việc quản lý giao tiếp và workflow giữa các agent làm tăng thêm sự phức tạp cho việc thiết kế hệ thống.
    *   **Tăng chi phí & Độ trễ:** Việc chạy nhiều agent liên quan đến nhiều cuộc gọi LLM hơn, có thể đắt hơn và chậm hơn so với cách tiếp cận single-agent.

## Phase 0: Foundation & Setup
Chúng ta sẽ bắt đầu bằng việc cài đặt các thư viện và cấu hình các API keys cho Nebius, LangSmith và Tavily.

### Step 0.1: Installing Core Libraries
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ cài đặt bộ thư viện tiêu chuẩn cho loạt dự án này.

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
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# For pretty printing
from rich.console import Console
from rich.markdown import Markdown

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Multi-Agent (Nebius)"

for key in ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]:
    if not os.environ.get(key):
        print(f"{key} not found. Please create a .env file and set it.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: The Baseline - A Monolithic 'Generalist' Agent
Để giới thiệu giá trị của một specialist team, trước tiên chúng ta cần xem một agent đơn lẻ thực hiện một nhiệm vụ phức tạp như thế nào. Chúng ta sẽ xây dựng một ReAct agent và cung cấp cho nó một prompt rộng yêu cầu nó thực hiện nhiều loại phân tích cùng một lúc.

### Step 1.1: Building the Monolithic Agent
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ xây dựng một ReAct agent tiêu chuẩn. Chúng ta sẽ cung cấp cho nó một công cụ tìm kiếm web và một system prompt rất chung chung yêu cầu nó trở thành một chuyên gia phân tích tài chính toàn diện.

```python
console = Console()

# Định nghĩa state chung cho cả hai agent
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Định nghĩa tool và LLM
search_tool = TavilySearch(max_results=3, name="web_search")
llm = ChatNebius(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)
llm_with_tools = llm.bind_tools([search_tool])

# Định nghĩa monolithic agent node
def monolithic_agent_node(state: AgentState):
    console.print("--- MONOLITHIC AGENT: Thinking... ---")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode([search_tool])

# Xây dựng ReAct graph cho monolithic agent
mono_graph_builder = StateGraph(AgentState)
mono_graph_builder.add_node("agent", monolithic_agent_node)
mono_graph_builder.add_node("tools", tool_node)
mono_graph_builder.set_entry_point("agent")

def tools_condition_with_end(state):
    result = tools_condition(state)
    if isinstance(result, str):
        # Các phiên bản cũ chỉ trả về "tools" hoặc "agent"
        return {result: "tools", "__default__": END}
    elif isinstance(result, dict):
        # Các phiên bản mới trả về một mapping
        result["__default__"] = END
        return result
    else:
        raise TypeError(f"Unexpected type from tools_condition: {type(result)}")

mono_graph_builder.add_conditional_edges("agent", tools_condition_with_end)
mono_graph_builder.add_edge("tools", "agent")

monolithic_agent_app = mono_graph_builder.compile()

print("Monolithic 'generalist' agent compiled successfully.")
```

### Step 1.2: Testing the Monolithic Agent
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ giao cho generalist agent một nhiệm vụ phức tạp: tạo một báo cáo phân tích thị trường đầy đủ cho một công ty, bao gồm ba lĩnh vực riêng biệt.

```python
company = "NVIDIA (NVDA)"
monolithic_query = f"Create a brief but comprehensive market analysis report for {company}. The report should include three sections: 1. A summary of recent news and market sentiment. 2. A basic technical analysis of the stock's price trend. 3. A look at the company's recent financial performance."

console.print(f"[bold yellow]Testing MONOLITHIC agent on a multi-faceted task:[/bold yellow]\n'{monolithic_query}'\n")

final_mono_output = monolithic_agent_app.invoke({
    "messages": [
        SystemMessage(content="You are a single, expert financial analyst. You must create a comprehensive report covering all aspects of the user's request."),
        HumanMessage(content=monolithic_query)
    ]
})

console.print("\n--- [bold red]Final Report from Monolithic Agent[/bold red] ---")
console.print(Markdown(final_mono_output['messages'][-1].content))
```

**Discussion of the Output:**
Monolithic agent đã tạo ra một báo cáo. Nó có khả năng đã thực hiện vài cuộc tìm kiếm web và cố gắng hết sức để tổng hợp thông tin. Tuy nhiên, kết quả đầu ra có thể có một số điểm yếu:
- **Thiếu cấu trúc:** Các phần có thể bị trộn lẫn với nhau, không có tiêu đề rõ ràng hoặc định dạng chuyên nghiệp.
- **Phân tích hời hợt:** Việc cố gắng trở thành chuyên gia trong ba lĩnh vực cùng một lúc có thể khiến agent chỉ cung cấp các tóm tắt cấp cao mà không đi sâu vào bất kỳ lĩnh vực đơn lẻ nào.
- **Giọng văn chung chung:** Ngôn ngữ có thể chung chung, thiếu các thuật ngữ chuyên môn và sự tập trung của một chuyên gia thực thụ trong mỗi lĩnh vực.

Kết quả này là baseline của chúng ta. Nó hoạt động được, nhưng không xuất sắc. Bây giờ, chúng ta sẽ xây dựng một specialist team để xem liệu chúng ta có thể làm tốt hơn không.

## Phase 2: The Advanced Approach - A Multi-Agent Specialist Team
Bây giờ chúng ta sẽ xây dựng nhóm của mình: một News Analyst, một Technical Analyst và một Financial Analyst. Mỗi người sẽ là một agent node riêng với một persona cụ thể. Một Report Writer cuối cùng sẽ đóng vai trò manager, biên soạn công việc của họ.

### Step 2.1: Defining the Specialist Agent Nodes
**Những gì chúng ta sẽ làm:**
Chúng ta sẽ tạo ra ba agent nodes riêng biệt. Sự khác biệt chính là system prompt có tính cụ thể cao mà chúng ta cung cấp cho mỗi node. Prompt này định nghĩa persona của họ, lĩnh vực chuyên môn của họ và định dạng chính xác mà kết quả đầu ra của họ nên có. Đây là cách chúng ta thực thi sự chuyên môn hóa (specialization).

```python
# State cho hệ thống đa tác vụ của chúng ta sẽ giữ kết quả đầu ra của mỗi chuyên gia
class MultiAgentState(TypedDict):
    user_request: str
    news_report: Optional[str]
    technical_report: Optional[str]
    financial_report: Optional[str]
    final_report: Optional[str]

def create_specialist_node(persona: str, output_key: str):
    """Factory function để tạo một specialist agent node."""
    system_prompt = persona + "\n\nYou have access to a web search tool. Your output MUST be a concise report section, formatted in markdown, focusing only on your area of expertise."

    # Xây dựng ChatPromptTemplate
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{user_request}")
    ])

    agent = prompt_template | llm_with_tools

    def specialist_node(state: MultiAgentState):
        console.print(f"--- CALLING {output_key.replace('_report','').upper()} ANALYST ---")
        result = agent.invoke({"user_request": state["user_request"]})
        content = result.content if result.content else f"No direct content, tool calls: {result.tool_calls}"
        return {output_key: content}

    return specialist_node


# Tạo các specialist nodes
news_analyst_node = create_specialist_node(
    "You are an expert News Analyst. Your specialty is scouring the web for the latest news, articles, and social media sentiment about a company.",
    "news_report"
)
technical_analyst_node = create_specialist_node(
    "You are an expert Technical Analyst. You specialize in analyzing stock price charts, trends, and technical indicators.",
    "technical_report"
)
financial_analyst_node = create_specialist_node(
    "You are an expert Financial Analyst. You specialize in interpreting financial statements and performance metrics.",
    "financial_report"
)

def report_writer_node(state: MultiAgentState):
    """Agent quản lý thực hiện tổng hợp các báo cáo từ các chuyên gia."""
    console.print("--- CALLING REPORT WRITER ---")
    prompt = f"""You are an expert financial editor. Your task is to combine the following specialist reports into a single, professional, and cohesive market analysis report. Add a brief introductory and concluding paragraph.
    
    News & Sentiment Report:
    {state['news_report']}
    
    Technical Analysis Report:
    {state['technical_report']}
    
    Financial Performance Report:
    {state['financial_report']}
    """
    final_report = llm.invoke(prompt).content
    return {"final_report": final_report}

print("Specialist agent nodes and Report Writer node defined.")
```

### Step 2.2: Building the Multi-Agent Graph
**Những gì chúng ta sẽ làm:**
Bây giờ chúng ta sẽ kết nối các chuyên gia và quản lý vào một graph. Đối với nhiệm vụ này, các chuyên gia có thể làm việc độc lập, vì vậy chúng ta có thể chạy chúng theo một trình tự đơn giản (trong một ứng dụng thực tế, những việc này có thể được chạy song song). Bước cuối cùng luôn là report writer.

```python
multi_agent_graph_builder = StateGraph(MultiAgentState)

# Thêm tất cả các nodes
multi_agent_graph_builder.add_node("news_analyst", news_analyst_node)
multi_agent_graph_builder.add_node("technical_analyst", technical_analyst_node)
multi_agent_graph_builder.add_node("financial_analyst", financial_analyst_node)
multi_agent_graph_builder.add_node("report_writer", report_writer_node)

# Định nghĩa trình tự workflow
multi_agent_graph_builder.set_entry_point("news_analyst")
multi_agent_graph_builder.add_edge("news_analyst", "technical_analyst")
multi_agent_graph_builder.add_edge("technical_analyst", "financial_analyst")
multi_agent_graph_builder.add_edge("financial_analyst", "report_writer")
multi_agent_graph_builder.add_edge("report_writer", END)

multi_agent_app = multi_agent_graph_builder.compile()
print("Multi-agent specialist team compiled successfully.")
```

## Phase 3: Head-to-Head Comparison
Bây giờ chúng ta sẽ chạy specialist team cho cùng một nhiệm vụ như monolithic agent và so sánh các báo cáo cuối cùng.

```python
multi_agent_query = f"Create a brief but comprehensive market analysis report for {company}."
initial_multi_agent_input = {"user_request": multi_agent_query}

console.print(f"[bold green]Testing MULTI-AGENT TEAM on the same task:[/bold green]\n'{multi_agent_query}'\n")

final_multi_agent_output = multi_agent_app.invoke(initial_multi_agent_input)

console.print("\n--- [bold green]Final Report from Multi-Agent Team[/bold green] ---")
console.print(Markdown(final_multi_agent_output['final_report']))
```

**Discussion of the Output:**
Sự khác biệt trong báo cáo cuối cùng là rất lớn. Kết quả đầu ra từ multi-agent team mang những đặc điểm:
- **Tính cấu trúc cao:** Nó có các phần rõ ràng, riêng biệt cho từng lĩnh vực phân tích bởi vì mỗi phần được tạo ra bởi một chuyên gia với hướng dẫn định dạng cụ thể.
- **Phân tích sâu hơn:** Mỗi phần chứa ngôn ngữ và thông tin chi tiết cụ thể hơn cho từng lĩnh vực chuyên môn. Technical Analyst nói về các đường trung bình động (moving averages), News Analyst thảo luận về sentiment, và Financial Analyst tập trung vào doanh thu và lợi nhuận.
- **Chuyên nghiệp hơn:** Báo cáo cuối cùng, được lắp ráp bởi Report Writer, đọc giống như một tài liệu chuyên nghiệp, với phần mở đầu, nội dung chính và kết luận rõ ràng.

Sự so sánh định định tính này cho thấy bằng cách phân chia lao động giữa một nhóm các chuyên gia, chúng ta đạt được một kết quả vượt trội mà một generalist agent đơn lẻ khó có thể tái hiện được.

## Phase 4: Quantitative Evaluation
Để chính thức hóa việc so sánh, chúng ta sẽ sử dụng một LLM-as-a-Judge để chấm điểm cả hai báo cáo. Các tiêu chí sẽ tập trung vào các phẩm chất mà chúng ta mong đợi sẽ tốt hơn trong cách tiếp cận multi-agent, chẳng hạn như cấu trúc và chiều sâu phân tích.

```python
class Evaluation(BaseModel):
    """Schema cho việc chấm điểm báo cáo."""
    clarity_and_structure_score: int = Field(description="Score từ 1-10 về độ rõ nét và cấu trúc.")
    analytical_depth_score: int = Field(description="Score từ 1-10 về chiều sâu phân tích.")
    completeness_score: int = Field(description="Score từ 1-10 về tính đầy đủ.")
    justification: str = Field(description="Giải thích ngắn gọn cho các điểm số.")

judge_llm = llm.with_structured_output(Evaluation)

def evaluate_report(report_content: str):
    prompt = f"""You are an expert judge of financial reports. Evaluate the following market analysis report based on its clarity, analytical depth, and completeness.
    
    Report Content:
    {report_content}
    """
    return judge_llm.invoke(prompt)

if final_mono_output and final_multi_agent_output:
    console.print("--- Evaluating Monolithic Agent's Report ---")
    mono_eval = evaluate_report(final_mono_output['messages'][-1].content)
    console.print(mono_eval.model_dump())

    console.print("\n--- Evaluating Multi-Agent Team's Report ---")
    multi_eval = evaluate_report(final_multi_agent_output['final_report'])
    console.print(multi_eval.model_dump())
```

**Discussion of the Output:**
Giám khảo định lượng xác nhận sự ưu việt của Multi-Agent System cho các nhiệm vụ đòi hỏi sự đa dạng về kiến thức chuyên môn. specialist team liên tục đạt điểm cao hơn về cấu trúc và chiều sâu phân tích. Bằng cách cho phép mỗi chuyên gia hoạt động trong phạm vi năng lực cốt lõi của họ và có một manager chuyên trách thực hiện việc tổng hợp cuối cùng, chúng ta tạo ra một bản phân tích sắc bén hơn, chi tiết hơn và nhìn chuyên nghiệp hơn so với bất kỳ điều gì mà một tác nhân đơn lẻ, "đa năng" có thể đạt được.

## Conclusion
Kiến trúc **Multi-Agent System** phản ánh sức mạnh của sự chuyên môn hóa của con người trong thế giới AI. Bằng cách chuyển đổi từ một mô hình agent đơn lẻ sang một nhóm các specialized agents cộng tác, chúng ta mở khóa các mức độ sâu, độ chính xác và tính chuyên nghiệp mới cho các nhiệm vụ phức tạp. Mặc dù việc điều phối một nhóm như vậy làm tăng thêm sự phức tạp cho hệ thống, nhưng kết quả—vốn vượt trội đáng kể về chất lượng và độ tinh tế—thường biện minh hoàn toàn cho nỗ lực đó. Pattern này là một nền tảng cho việc xây dựng các hệ thống AI cấp doanh nghiệp, thực sự mang lại kết quả chất lượng cao cho các vấn đề phức tạp.
