# 📘 Agentic Architectures 14: Observability + Dry-Run Harness

Chào mừng bạn đến với một notebook quan trọng trong loạt bài của chúng ta, tập trung vào việc triển khai và an toàn vận hành của các AI agent. Chúng ta sẽ triển khai một **Observability and Dry-Run Harness** (Cơ chế Quan sát và Chạy thử), một pattern thiết yếu để kiểm thử, gỡ lỗi và quản lý an toàn các agent tương tác với các hệ thống trong thế giới thực.

Nguyên tắc cốt lõi rất đơn giản nhưng mạnh mẽ: **không bao giờ chạy một hành động của agent trong môi trường thực tế (live) mà không biết chính xác nó định làm gì.** Kiến trúc này chính thức hóa quy trình "nhìn kỹ trước khi nhảy". Một agent trước tiên thực thi kế hoạch của mình ở chế độ `dry_run`, chế độ này không thay đổi thế giới thực nhưng tạo ra các bản nhật ký (logs) chi tiết và một kế hoạch hành động rõ ràng. Kế hoạch này sau đó được trình bày cho con người (hoặc một bộ kiểm tra tự động) để phê duyệt trước khi cho phép thực thi chính thức, thực tế.

Để chứng minh điều này, chúng ta sẽ xây dựng một **Corporate Social Media Agent**. Agent này có nhiệm vụ tạo và xuất bản các bài đăng. Chúng ta sẽ thấy cơ chế chạy thử cho phép chúng ta:
1.  **Generate a Proposed Post (Tạo bài đăng đề xuất):** AI sẽ soạn thảo một bài đăng một cách sáng tạo dựa trên một câu lệnh.
2.  **Perform a Dry Run (Thực hiện chạy thử):** Agent sẽ gọi hàm `publish` ở chế độ hộp cát `dry_run=True`, tạo ra các bản nhật ký về những gì *sẽ* xảy ra.
3.  **Human-in-the-Loop Review (Đánh giá có sự tham gia của con người):** Một người vận hành sẽ được xem nội dung bài đăng chính xác và dấu vết chạy thử (dry-run trace). Họ phải nhập `approve` để tiếp tục.
4.  **Execute Live Action (Thực thi hành động thực tế):** Chỉ sau khi được phê duyệt, hàm `publish` mới được gọi lại, lần này với `dry_run=False`, để thực hiện hành động thực.

Pattern này là nền tảng của việc triển khai agent có trách nhiệm, cung cấp sự minh bạch và khả năng kiểm soát cần thiết để vận hành AI an toàn trong môi trường production.

### Definition
Một **Observability and Dry-Run Harness** là một kiến trúc kiểm thử và triển khai giúp đánh chặn các hành động của agent. Trước tiên, nó thực thi chúng ở chế độ "dry run" hoặc "hộp cát" (sandboxed) giúp mô phỏng hành động mà không gây ra tác động thực tế. Kế hoạch và các bản nhật ký kết quả sau đó được đưa ra để đánh giá, và chỉ sau khi có sự chấp thuận rõ ràng, hành động mới được thực thi trong môi trường thực.

### High-level Workflow
1.  **Agent Proposes Action:** Agent xác định một kế hoạch hoặc một cuộc gọi công cụ (tool call) cụ thể để thực thi (ví dụ: `api.post_update(...)`).
2.  **Dry Run Execution:** Cơ chế này gọi kế hoạch của agent với cờ `dry_run=True`. Các công cụ bên dưới được thiết kế để nhận diện cờ này và chỉ đưa ra những gì chúng *sẽ* làm, cùng với các bản nhật ký và dấu vết (traces).
3.  **Collect Observability Data:** Cơ chế này thu thập hành động đề xuất, các bản nhật ký chạy thử và bất kỳ dữ liệu dấu vết liên quan nào khác từ mô phỏng.
4.  **Human/Automated Review:** Dữ liệu quan sát này được trình bày cho người đánh giá. Con người có thể kiểm tra tính chính xác, an toàn và sự phù hợp với mục tiêu. Một hệ thống tự động có thể chạy các bài kiểm tra vi phạm chính sách hoặc các pattern xấu đã biết.
5.  **Go/No-Go Decision:** Người đánh giá đưa ra quyết định `approve` (phê duyệt) hoặc `reject` (từ chối).
6.  **Live Execution (on 'Go'):** Nếu được phê duyệt, cơ chế này thực thi lại hành động của agent, lần này với `dry_run=False`, gây ra tác động thực tế.

### When to Use / Applications
*   **Gỡ lỗi và Kiểm thử:** Trong quá trình phát triển, để hiểu chính xác cách một agent đang diễn giải một nhiệm vụ và những hành động nào nó đang thực hiện mà không gây ra tác dụng phụ.
*   **Xác thực & An toàn trong Production:** Như một tính năng vĩnh viễn trong production cho bất kỳ agent nào có thể sửa đổi trạng thái, chi tiêu tiền, gửi thông tin liên lạc hoặc thực hiện bất kỳ hành động không thể đảo ngược nào khác.
*   **CI/CD cho Agent:** Tích hợp cơ chế chạy thử vào một pipeline kiểm thử tự động để xác thực hành vi của agent trước khi triển khai các phiên bản mới.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Tính minh bạch & An toàn tối đa:** Cung cấp bản xem trước rõ ràng, có thể kiểm tra được về các hành động của agent, ngăn chặn những sai lầm tốn kém hoặc gây bối rối.
    *   **Tuyệt vời cho việc gỡ lỗi:** Giúp dễ dàng truy vết logic và các cuộc gọi công cụ của agent mà không phải hoàn tác các thay đổi thực tế.
*   **Weaknesses:**
    *   **Làm chậm việc triển khai/thực thi:** Bước đánh giá bắt buộc (đặc biệt nếu là con người) gây ra độ trễ, khiến nó không phù hợp cho các ứng dụng thời gian thực.
    *   **Yêu cầu sự hỗ trợ từ công cụ:** Các công cụ và API mà agent sử dụng phải được thiết kế để hỗ trợ chế độ `dry_run`.

## Phase 0: Foundation & Setup
Thiết lập tiêu chuẩn các thư viện và biến môi trường.

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv
```

```python
import os
import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Pydantic for data modeling
from pydantic import BaseModel, Field

# LangChain components
from langchain_nebius import ChatNebius
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
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Dry-Run Harness (Nebius)"

required_vars = ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY"]
for var in required_vars:
    if var not in os.environ:
        print(f"Warning: Environment variable {var} not set.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Building the Environment and Tools
Cốt lõi của kiến trúc này là một công cụ hỗ trợ chế độ `dry_run`. Chúng ta sẽ tạo một class `SocialMediaAPI` đơn giản. Phương thức `publish_post` của nó sẽ hành xử khác nhau tùy thuộc vào cờ `dry_run`, cung cấp khả năng quan sát mà chúng ta cần.

```python
console = Console()

# Model có cấu trúc cho bài đăng đề xuất của agent
class SocialMediaPost(BaseModel):
    content: str = Field(description="The full text content of the social media post.")
    hashtags: List[str] = Field(description="A list of relevant hashtags, without the '#'.")

# Thành phần mấu chốt: Một công cụ với cờ dry_run
class SocialMediaAPI:
    """Một API mạng xã hội giả lập hỗ trợ chế độ dry-run."""
    
    def publish_post(self, post: SocialMediaPost, dry_run: bool = True) -> Dict[str, Any]:
        """Xuất bản một bài đăng lên bảng tin mạng xã hội."""
        timestamp = datetime.datetime.now().isoformat()
        hashtags_str = ' '.join([f'#{h}' for h in post.hashtags])
        full_post_text = f"{post.content}\n\n{hashtags_str}"
        
        if dry_run:
            # Trong chế độ dry-run, chúng ta không thực thi, chúng ta chỉ trả về kế hoạch và logs
            log_message = f"[DRY RUN] At {timestamp}, would publish the following post:\n--- PREVIEW ---\n{full_post_text}\n--- END PREVIEW ---"
            console.print(Panel(log_message, title="[yellow]Dry Run Log[/yellow]", border_style="yellow"))
            return {"status": "DRY_RUN_SUCCESS", "log": log_message, "proposed_post": full_post_text}
        else:
            # Trong chế độ live, chúng ta thực thi hành động
            log_message = f"[LIVE] At {timestamp}, successfully published post!"
            console.print(Panel(log_message, title="[green]Live Execution Log[/green]", border_style="green"))
            # Tại đây bạn sẽ thực hiện cuộc gọi API thực tế, ví dụ: twitter_client.create_tweet(...)
            return {"status": "LIVE_SUCCESS", "log": log_message, "post_id": f"post_{hash(full_post_text)}"}

social_media_tool = SocialMediaAPI()
print("Dry-run capable SocialMediaAPI tool defined successfully.")
```

## Phase 2: Building the Dry-Run Harness with LangGraph
Bây giờ chúng ta sẽ xây dựng toàn bộ workflow. Graph sẽ quản lý trạng thái của quy trình, chuyển từ việc đề xuất một hành động, đến bước chạy thử và đánh giá, và cuối cùng là thực thi có điều kiện dựa trên sự phê duyệt của con người.

```python
llm = ChatNebius(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0.5)

# LangGraph State
class AgentState(TypedDict):
    user_request: str
    proposed_post: Optional[SocialMediaPost]
    dry_run_log: Optional[str]
    review_decision: Optional[str] # 'approve' hoặc 'reject'
    final_status: str

# Graph Nodes
def propose_post_node(state: AgentState) -> Dict[str, Any]:
    """Agent sáng tạo thực hiện soạn thảo bài đăng mạng xã hội."""
    console.print("--- 📝 Social Media Agent Drafting Post ---")
    prompt = ChatPromptTemplate.from_template(
        "You are a creative and engaging social media manager for a major AI company. Based on the user's request, draft a compelling social media post, including relevant hashtags.\n\nRequest: {request}"
    )
    post_generator_llm = llm.with_structured_output(SocialMediaPost)
    chain = prompt | post_generator_llm
    proposed_post = chain.invoke({"request": state['user_request']})
    return {"proposed_post": proposed_post}

def dry_run_review_node(state: AgentState) -> Dict[str, Any]:
    """Thực hiện chạy thử và yêu cầu con người đánh giá."""
    console.print("--- 🧐 Performing Dry Run & Awaiting Human Review ---")
    dry_run_result = social_media_tool.publish_post(state['proposed_post'], dry_run=True)
    
    # Trình bày kế hoạch để đánh giá
    review_panel = Panel(
        f"[bold]Proposed Post:[/bold]\n{dry_run_result['proposed_post']}",
        title="[bold yellow]Human-in-the-Loop: Review Required[/bold yellow]",
        border_style="yellow"
    )
    console.print(review_panel)
    
    # Lấy phê duyệt từ con người
    decision = ""
    while decision.lower() not in ["approve", "reject"]:
        decision = console.input("Type 'approve' to publish or 'reject' to cancel: ")
        
    return {"dry_run_log": dry_run_result['log'], "review_decision": decision.lower()}

def execute_live_post_node(state: AgentState) -> Dict[str, Any]:
    """Thực thi bài đăng live sau khi được phê duyệt."""
    console.print("--- ✅ Post Approved, Executing Live ---")
    live_result = social_media_tool.publish_post(state['proposed_post'], dry_run=False)
    return {"final_status": f"Post successfully published! ID: {live_result.get('post_id')}"}

def post_rejected_node(state: AgentState) -> Dict[str, Any]:
    """Xử lý trường hợp bài đăng bị từ chối."""
    console.print("--- ❌ Post Rejected by Human Reviewer ---")
    return {"final_status": "Action was rejected by the reviewer and not executed."}

# Conditional Edge
def route_after_review(state: AgentState) -> str:
    """Định tuyến tới thực thi hoặc từ chối dựa trên đánh giá của con người."""
    return "execute_live" if state["review_decision"] == "approve" else "reject"

# Xây dựng graph
workflow = StateGraph(AgentState)
workflow.add_node("propose_post", propose_post_node)
workflow.add_node("dry_run_review", dry_run_review_node)
workflow.add_node("execute_live", execute_live_post_node)
workflow.add_node("reject", post_rejected_node)

workflow.set_entry_point("propose_post")
workflow.add_edge("propose_post", "dry_run_review")
workflow.add_conditional_edges("dry_run_review", route_after_review, {"execute_live": "execute_live", "reject": "reject"})
workflow.add_edge("execute_live", END)
workflow.add_edge("reject", END)

dry_run_agent = workflow.compile()
print("Dry-Run Harness agent graph compiled successfully.")
```

## Phase 3: Demonstration
Hãy kiểm tra toàn bộ hệ thống. Đầu tiên, với một yêu cầu an toàn, tiêu chuẩn mà chúng ta sẽ phê duyệt. Thứ hai, với một yêu cầu mơ hồ hơn có thể tạo ra một bài đăng rủi ro, mà chúng ta sẽ từ chối.

```python
def run_agent_with_harness(request: str):
    initial_state = {"user_request": request}
    # Lưu ý: Bạn sẽ được yêu cầu nhập vào console bên dưới cell.
    result = dry_run_agent.invoke(initial_state)
    console.print(f"\n[bold]Final Status:[/bold] {result['final_status']}")

# Test 1: Một bài đăng an toàn mà chúng ta sẽ phê duyệt.
console.print("--- ✅ Test 1: Safe Post (Approve) ---")
run_agent_with_harness("Draft a positive launch announcement for our new AI model, 'Nebula'.")

# Test 2: Một bài đăng rủi ro mà chúng ta sẽ từ chối.
console.print("\n--- ❌ Test 2: Risky Post (Reject) ---")
run_agent_with_harness("Draft a post that emphasizes how much better our new 'Nebula' model is than the competition.")
```

### Analysis of the Results
Phần trình diễn là một minh chứng hoàn hảo cho giá trị của cơ chế này:

1.  **Bài đăng an toàn:** Yêu cầu đầu tiên rất rõ ràng. Agent đã tạo ra một bài đăng chuyên nghiệp và nhiệt huyết. Chạy thử đã cho xem trước chính xác những gì sẽ được xuất bản. Chúng ta đã phê duyệt nó, và nhật ký `[LIVE]` xác nhận rằng hành động thực tế đã được thực hiện. Quy trình hoạt động đúng như mong đợi.

2.  **Bài đăng rủi ro:** Yêu cầu thứ hai mơ hồ hơn và có thể được diễn giải một cách quyết liệt. Agent, được yêu cầu nhấn mạnh sự vượt trội, đã soạn thảo một bài đăng mang tính kiêu ngạo và thiếu chuyên nghiệp (`làm cho tất cả các đối thủ của chúng ta trở nên lỗi thời`). Mặc dù agent đã đáp ứng được câu lệnh sáng tạo của nó, nhưng đây không phải là thông điệp mà một công ty thực thụ muốn xuất bản.

Đây là lúc cơ chế chạy thử chứng minh giá trị của mình. Việc chạy thử đã phơi bày nội dung rủi ro này *trước khi* nó có thể được xuất bản. Người đánh giá là con người đã dễ dàng xác định giọng điệu không phù hợp và nhập `reject`. Graph đã định tuyến chính xác tới `post_rejected_node`, và trạng thái cuối cùng xác nhận rằng **không có hành động live nào được thực hiện.** Một cuộc khủng hoảng PR tiềm tàng đã được ngăn chặn bằng một workflow đơn giản, có cấu trúc.

Điều này phân tách rõ ràng việc tạo ra nội dung sáng tạo nhưng khó đoán của agent với việc thực thi có kiểm soát, mang tính định hình, cung cấp một lớp an toàn quan trọng.

## Conclusion
Trong notebook này, chúng ta đã xây dựng một **Observability and Dry-Run Harness** hoàn chỉnh. Kiến trúc này không chỉ là một tính năng mà là một triết lý nền tảng để triển khai các agent tương tác với thế giới thực. Bằng cách thực thi chu kỳ `propose -> review -> execute` (đề xuất -> đánh giá -> thực thi), chúng ta đạt được những lợi ích then chốt:

- **Sự minh bạch:** Chúng ta biết chính xác những gì agent định làm trước khi nó thực hiện.
- **Khả năng kiểm soát:** Chúng ta có con người tham gia (hoặc một công cụ quy tắc tự động) với quyền phủ quyết tối cao đối với bất kỳ hành động nào.
- **An toàn:** Chúng ta ngăn chặn các hành động không mong muốn, tốn kém hoặc có hại, chuyển từ việc thực thi một cách đầy hy vọng sang triển khai một cách đầy tự tin.

Mặc dù pattern này gây ra độ trễ, nhưng sự an toàn và độ tin cậy mà nó cung cấp là không thể thương lượng đối với hầu hết các ứng dụng thực tế. Nó là một công cụ thiết yếu cho bất kỳ nhà phát triển nào muốn xây dựng các hệ thống agentic mạnh mẽ, đáng tin cậy và sẵn sàng cho môi trường production.
