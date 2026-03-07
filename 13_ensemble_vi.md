# 📘 Agentic Architectures 13: Parallel Exploration + Ensemble Decision

Chào mừng bạn đến với bài tìm hiểu sâu về một trong những kiến trúc lập luận mạnh mẽ và đáng tin cậy nhất: **Parallel Exploration with Ensemble Decision-Making** (Khám phá song song với ra quyết định theo nhóm). Pattern này giải quyết tính phi định hình vốn có và các định kiến tiềm ẩn của một LLM đơn lẻ bằng cách tận dụng nguyên lý "trí tuệ tập thể" (wisdom of the crowd) áp dụng cho các AI agent.

Thay vì dựa vào một dòng lập luận duy nhất, kiến trúc này sinh ra nhiều agent độc lập để phân tích một vấn đề từ các góc nhìn khác nhau cùng một lúc. Mỗi agent đi theo con đường lập luận riêng của mình, giống như các chuyên gia khác nhau trong một ủy ban. Các kết luận cá nhân của họ sau đó được thu thập và tổng hợp bởi một agent "aggregator" (người tổng hợp) cuối cùng. Agent này sẽ cân nhắc các quan điểm khác nhau, xác định sự đồng thuận và xung đột, và đưa ra một câu trả lời cuối cùng sắc sảo và đáng tin cậy hơn.

Để xây dựng một triển khai phức tạp và mạnh mẽ, chúng ta sẽ tạo ra một **Hội đồng Đầu tư AI giả lập** với nhiệm vụ trả lời một câu hỏi khó và mở: **"NVIDIA (NVDA) có phải là một khoản đầu tư dài hạn tốt vào giữa năm 2024 không?"**

Hội đồng của chúng ta sẽ bao gồm ba agent song song, riêng biệt:
1.  **The Bullish Growth Analyst (Nhà phân tích tăng trưởng lạc quan):** Một người lạc quan tập trung vào sự đổi mới, sự thống trị thị trường và tiềm năng tương lai.
2.  **The Cautious Value Analyst (Nhà phân tích giá trị thận trọng):** Một người hoài nghi, xem xét kỹ lưỡng các số liệu tài chính, định giá, cạnh tranh và các rủi ro tiềm ẩn.
3.  **The Quantitative Analyst (Quant - Nhà phân tích định lượng):** Một chuyên gia dựa trên dữ liệu, chỉ nhìn vào các chỉ số tài chính và các chỉ báo kỹ thuật của cổ phiếu.

Cuối cùng, một agent **Chief Investment Officer (CIO - Giám đốc đầu tư)** sẽ tổng hợp các báo cáo mâu thuẫn của họ thành một luận điểm đầu tư cuối cùng, cân bằng, cung cấp một câu trả lời mạnh mẽ hơn nhiều so với bất kỳ agent đơn lẻ nào có thể làm được.

### Definition
**Parallel Exploration + Ensemble Decision** là một kiến trúc agentic nơi một vấn đề được xử lý đồng thời bởi nhiều agent hoặc các con đường lập luận độc lập. Các kết quả đầu ra cá nhân sau đó được tập hợp lại, thường là bởi một agent riêng biệt, thông qua một phương pháp như bỏ phiếu (voting), xây dựng sự đồng thuận (consensus-building), hoặc tổng hợp (synthesis) để đi đến một kết luận cuối cùng mạnh mẽ hơn.

### High-level Workflow
1.  **Fan-Out (Khám phá song song):** Truy vấn của người dùng được phân phối tới N specialist agent độc lập. Quan trọng là các agent này thường được cung cấp các hướng dẫn, persona (hình mẫu nhân vật) hoặc công cụ khác nhau để khuyến khích các phương pháp phân tích đa dạng.
2.  **Independent Processing (Xử lý độc lập):** Mỗi agent làm việc trên vấn đề một cách cô lập, tạo ra phân tích, kết luận hoặc câu trả lời hoàn chỉnh của riêng mình.
3.  **Fan-In (Tập hợp):** Kết quả đầu ra từ tất cả N agent được thu thập lại.
4.  **Synthesize (Ra quyết định theo nhóm):** Một agent "aggregator" (người tổng hợp) hoặc "judge" (thẩm phán) cuối cùng nhận tất cả các kết quả đầu ra cá nhân. Nhiệm vụ của nó là phân tích các góc nhìn này, xác định điểm chung, cân đối các bằng chứng mâu thuẫn và tổng hợp thành một câu trả lời cuối cùng toàn diện.

### When to Use / Applications
*   **Q&A Lập luận khó:** Đối với các câu hỏi phức tạp, mơ hồ mà một dòng lập luận duy nhất có thể dễ dàng bỏ lỡ các sắc thái (ví dụ: "Nguyên nhân chính của cuộc khủng hoảng tài chính năm 2008 là gì?").
*   **Kiểm chứng sự thật & Xác minh:** Việc có nhiều agent tìm kiếm và xác minh một sự thật từ các nguồn khác nhau có thể giảm thiểu đáng kể tình trạng ảo giác (hallucinations).
*   **Hỗ trợ ra quyết định rủi ro cao:** Trong các lĩnh vực như y tế hoặc tài chính, việc lấy "ý kiến thứ hai" (hoặc thứ ba, thứ tư) từ các persona AI khác nhau trước khi đưa ra khuyến nghị.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Tăng cường độ tin cậy & độ chính xác:** Trung hòa các lỗi ngẫu nhiên hoặc định kiến của một agent đơn lẻ, làm cho câu trả lời cuối cùng có khả năng chính xác và toàn diện hơn nhiều.
    *   **Giảm thiểu ảo giác:** Nếu một agent ảo giác về một sự thật, những agent khác ít có khả năng làm điều tương tự, và người tổng hợp có thể dễ dàng phát hiện ra điểm bất thường.
*   **Weaknesses:**
    *   **Chi phí rất cao:** Đây là một trong những kiến trúc tốn kém nhất, vì nó nhân số lượng lượt gọi LLM với số lượng agent trong nhóm (cộng với lượt gọi tổng hợp cuối cùng).
    *   **Tăng độ trễ:** Hệ thống phải chờ tất cả các con đường song song hoàn thành trước khi quá trình tổng hợp cuối cùng có thể bắt đầu.

## Phase 0: Foundation & Setup
Chúng ta sẽ cài đặt các thư viện và thiết lập môi trường. Chúng ta sẽ cần `langchain-tavily` cho các công cụ nghiên cứu của các nhà phân tích.

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
from rich.panel import Panel

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Parallel Ensemble (Nebius)"

required_vars = ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]
for var in required_vars:
    if var not in os.environ:
        print(f"Warning: Environment variable {var} not set.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Creating the Diverse Specialist Analysts
Chìa khóa của một nhóm (ensemble) thành công là sự đa dạng về nhận thức. Chúng ta sẽ tạo ra ba agent nhà phân tích riêng biệt, mỗi agent có một persona chi tiết được thiết kế để tạo ra một loại phân tích khác nhau. Tất cả đều có quyền truy cập vào search tool.

```python
console = Console()
# Cần một model mạnh mẽ cho nhiệm vụ phức tạp này
llm = ChatNebius(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0.3)
search_tool = TavilySearch(max_results=5)

# LangGraph State
class EnsembleState(TypedDict):
    query: str
    # Dict 'analyses' sẽ lưu trữ đầu ra từ mỗi agent song song
    analyses: Dict[str, str]
    final_recommendation: Optional[Any] # Sẽ lưu trữ đầu ra có cấu trúc từ CIO

# Helper factory để tạo các analyst nodes của chúng ta
def create_analyst_node(persona: str, agent_name: str):
    """Factory để tạo một specialist analyst node với persona độc nhất."""
    system_prompt = f"You are an expert financial analyst. Your persona is '{persona}'. You must use your search tool to gather up-to-date information. Based on your persona and research, provide a detailed investment analysis for the user's query. Conclude with a clear 'Recommendation' (e.g., Buy, Hold, Sell) and a 'Confidence Score' (1-10)."
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{query}")
    ])
    chain = prompt | llm.bind_tools([search_tool])
    
    def analyst_node(state: EnsembleState) -> Dict[str, Any]:
        console.print(f"--- 👨‍💻 Calling {agent_name} --- ")
        result = chain.invoke({"query": state['query']})
        # Việc cập nhật state được thiết kế cẩn thận để thêm vào dict 'analyses'
        # mà không ghi đè lên các bản khác. Đây là chìa khóa cho việc thực thi song song.
        current_analyses = state.get('analyses', {})
        current_analyses[agent_name] = result.content
        return {"analyses": current_analyses}
    
    return analyst_node

# 1. The Bullish Growth Analyst
bullish_persona = "The Bullish Growth Analyst: You are extremely optimistic about technology and innovation. You focus on Total Addressable Market (TAM), visionary leadership, technological moats, and future growth potential. Downplay short-term volatility and valuation concerns in favor of the long-term disruptive story."
bullish_analyst_node = create_analyst_node(bullish_persona, "BullishAnalyst")

# 2. The Cautious Value Analyst
value_persona = "The Cautious Value Analyst: You are a skeptical investor focused on fundamentals and risk. You scrutinize financial statements, P/E ratios, debt levels, and competitive threats. You are wary of hype and market bubbles. Highlight potential risks, downside scenarios, and reasons for caution."
value_analyst_node = create_analyst_node(value_persona, "ValueAnalyst")

# 3. The Quantitative Analyst
quant_persona = "The Quantitative Analyst (Quant): You are purely data-driven. You ignore narratives and focus on hard numbers. Report on key financial metrics (YoY revenue growth, EPS, margins), valuation multiples (P/E, P/S), and technical indicators (RSI, moving averages). Your analysis must be objective and based on the data you find."
quant_analyst_node = create_analyst_node(quant_persona, "QuantAnalyst")

print("Specialist analyst agents defined successfully.")
```

## Phase 2: Building the CIO Aggregator Agent
Đây là bước **Ensemble Decision**. Chúng ta sẽ tạo ra một agent cuối cùng, Chief Investment Officer (CIO), người có nhiệm vụ tổng hợp các báo cáo từ ba nhà phân tích. Agent này cần một prompt tinh vi và một model đầu ra có cấu trúc để đảm bảo nó tạo ra một luận điểm đầu tư cuối cùng chất lượng cao và cân bằng.

```python
# Pydantic model cho khuyến nghị cuối cùng có cấu trúc
class FinalRecommendation(BaseModel):
    """Luận điểm đầu tư cuối cùng, được tổng hợp từ CIO."""
    final_recommendation: str = Field(description="The final investment decision, must be one of 'Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell'.")
    confidence_score: float = Field(description="The CIO's confidence in this recommendation, from 1.0 to 10.0.")
    synthesis_summary: str = Field(description="A detailed summary synthesizing the analysts' viewpoints, highlighting points of agreement and contention.")
    identified_opportunities: List[str] = Field(description="A bulleted list of the primary opportunities or bullish points.")
    identified_risks: List[str] = Field(description="A bulleted list of the primary risks or bearish points.")

def cio_synthesizer_node(state: EnsembleState) -> Dict[str, Any]:
    """Node cuối cùng tổng hợp tất cả các phân tích thành một khuyến nghị duy nhất."""
    console.print("--- 🏛️ Calling Chief Investment Officer for Final Decision ---")
    
    # Kết hợp tất cả các phân tích cá nhân thành một chuỗi duy nhất cho prompt
    all_analyses = "\n\n---\n\n".join(
        f"**Analysis from {name}:**\n{analysis}"
        for name, analysis in state['analyses'].items()
    )
    
    cio_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Chief Investment Officer (CIO) of a major investment fund. You have received reports from your team of specialist analysts. Your task is to synthesize these diverse and often conflicting viewpoints into a single, final, and actionable investment thesis. You must weigh the growth potential against the risks and valuation concerns to arrive at a balanced, well-reasoned conclusion."),
        ("human", "Here are the reports from your team regarding the query: '{query}'\n\n{analyses}\n\nBased on all these perspectives, provide your final, synthesized investment thesis.")
    ])
    
    cio_llm = llm.with_structured_output(FinalRecommendation)
    chain = cio_prompt | cio_llm
    
    final_decision = chain.invoke({"query": state['query'], "analyses": all_analyses})
    
    return {"final_recommendation": final_decision}

print("CIO Aggregator agent defined successfully.")
```

## Phase 3: Assembling the LangGraph Workflow
Bây giờ chúng ta kết nối mọi thứ lại với nhau. Graph sẽ có một entry point duy nhất rẽ nhánh (fan-out) tới ba analyst node song song của chúng ta. Khi tất cả các nhà phân tích đã hoàn thành công việc, graph sẽ tụ lại (fan-in) tới node cio_synthesizer duy nhất để tạo ra kết quả cuối cùng.

```python
# Node bắt đầu đơn giản là nhận truy vấn và chuẩn bị state.
def start_analysis_node(state: EnsembleState) -> Dict[str, Any]:
    # Khởi tạo dictionary analyses
    return {"analyses": {}}

# Xây dựng graph
workflow = StateGraph(EnsembleState)

workflow.add_node("start_analysis", start_analysis_node)

# Thêm các analyst node song song
workflow.add_node("bullish_analyst", bullish_analyst_node)
workflow.add_node("value_analyst", value_analyst_node)
workflow.add_node("quant_analyst", quant_analyst_node)

# Thêm node synthesizer cuối cùng
workflow.add_node("cio_synthesizer", cio_synthesizer_node)

# Thiết lập entry point
workflow.set_entry_point("start_analysis")

# FAN-OUT: Từ lúc bắt đầu, chạy cả ba analyst song song
workflow.add_edge("start_analysis", ["bullish_analyst", "value_analyst", "quant_analyst"])

# FAN-IN: Sau khi tất cả analyst xong, gọi CIO synthesizer
workflow.add_edge(["bullish_analyst", "value_analyst", "quant_analyst"], "cio_synthesizer")

workflow.add_edge("cio_synthesizer", END)

ensemble_agent = workflow.compile()
print("Parallel Ensemble agent graph compiled successfully.")
```

## Phase 3: Demonstration & Analysis
Hãy chạy toàn bộ hội đồng đầu tư cho câu hỏi phức tạp của chúng ta. Chúng ta sẽ in các báo cáo cá nhân trước để thấy sự đa dạng của các ý kiến, sau đó là khuyến nghị tổng hợp cuối cùng của CIO.

```python
query = "Based on recent news, financial performance, and future outlook, is NVIDIA (NVDA) a good long-term investment in mid-2024?"
console.print(f"--- 📈 Running Investment Committee for: {query} ---")

result = ensemble_agent.invoke({"query": query})

# Hiển thị các báo cáo cá nhân
console.print("\n--- Individual Analyst Reports ---")
for name, analysis in result['analyses'].items():
    console.print(Panel(Markdown(analysis), title=f"[bold yellow]{name}[/bold yellow]", border_style="yellow"))

# Hiển thị khuyến nghị tổng hợp cuối cùng
console.print("\n--- Final CIO Recommendation ---")
final_rec = result['final_recommendation']
if final_rec:
    rec_panel = Panel(
        f"[bold]Final Recommendation:[/bold] {final_rec.final_recommendation}\n"
        f"[bold]Confidence Score:[/bold] {final_rec.confidence_score}/10\n\n"
        f"[bold]Synthesis Summary:[/bold]\n{final_rec.synthesis_summary}\n\n"
        f"[bold]Identified Opportunities:[/bold]\n* {'\n* '.join(final_rec.identified_opportunities)}\n\n"
        f"[bold]Identified Risks:[/bold]\n* {'\n* '.join(final_rec.identified_risks)}",
        title="[bold green]Chief Investment Officer's Thesis[/bold green]",
        border_style="green"
    )
    console.print(rec_panel)
```

### Analysis of the Results
Phần trình diễn minh họa mạnh mẽ giá trị của kiến trúc phức tạp này:

1.  **Sự đa dạng về nhận thức:** Ba nhà phân tích đã đưa ra các báo cáo rất khác nhau, nhưng mỗi báo cáo đều có giá trị riêng. Nhà phân tích Bull tập trung vào tầm nhìn vĩ đại, nhà phân tích Value tập trung vào rủi ro, và nhà phân tích Quant cung cấp các dữ liệu thô. Một agent đơn lẻ, ngay cả với một prompt trung lập, cũng có khả năng nghiêng về một trong những hướng này, mang lại một bức tranh không đầy đủ.

2.  **Sự tổng hợp mạnh mẽ:** Agent CIO không chỉ đơn thuần "lấy trung bình" các khuyến nghị ('Buy', 'Hold', 'Hold'). Thay vào đó, nó thực hiện một sự tổng hợp thực sự. Nó thừa nhận tính hợp lệ của trường hợp lạc quan nhưng chế ngự nó bằng những lo ngại của các nhà phân tích giá trị và định lượng về định giá. Khuyến nghị cuối cùng là 'Buy' với mức độ tự tin 7.5 phản ánh sắc thái này, thực tế là: "Đây là một công ty tuyệt vời, nhưng cổ phiếu đắt, vì vậy hãy tiến hành thận trọng."

3.  **Insight có thể thực hiện và giải thích được:** Kết quả đầu ra có cấu trúc cuối cùng, với danh sách rõ ràng các cơ hội và rủi ro, hữu ích hơn nhiều cho một người ra quyết định so với một khối văn bản đơn lẻ, nguyên khối. Nó giải thích *tại sao* khuyến nghị cuối cùng được đưa ra bằng cách chỉ ra cách các ý kiến chuyên gia khác nhau được cân bằng như thế nào.

Phương pháp hội đồng này đã chuyển đổi thành công một câu hỏi chủ quan và phức tạp thành một phân tích đa chiều, có lập luận chặt chẽ, làm tăng đáng kể tính tin cậy của kết quả cuối cùng so với bất kỳ agent đơn lẻ nào.

## Conclusion
Trong notebook này, chúng ta đã triển khai một agent **Parallel Exploration + Ensemble Decision** toàn diện và phức tạp. Bằng cách giả lập một hội đồng gồm các chuyên gia đa dạng và một người ra quyết định cuối cùng, chúng ta đã xây dựng một hệ thống xuất sắc trong việc giải quyết các vấn đề mơ hồ, có rủi ro cao.

Các nguyên tắc cốt lõi—**sinh ra các nhà lập luận độc lập, đa dạng** và sau đó **tổng hợp kết quả của họ**—tạo ra một cơ chế mạnh mẽ để giảm thiểu định kiến, giảm sai sót và tăng chiều sâu phân tích. Mặc dù đây là một trong những kiến trúc agentic tốn kém nhất về mặt tính toán, nhưng khả năng đưa ra các kết luận mạnh mẽ, đáng tin cậy và sắc sảo khiến nó trở thành một công cụ không thể thiếu cho bất kỳ ứng dụng nào mà chất lượng và tính tin cậy của quyết định cuối cùng là tối quan trọng.
