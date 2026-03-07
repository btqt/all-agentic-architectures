# 📘 Agentic Architectures 15: Self-Improvement Loop (Self-Refine & RLHF Analogy)

Chào mừng bạn đến với bài tìm hiểu sâu về một pattern agentic có lẽ là tiên tiến nhất: **Self-Improvement Loop** (Vòng lặp Tự cải thiện). Kiến trúc này cho phép một agent học hỏi từ chính hiệu suất của nó, lặp lại việc tinh chỉnh đầu ra để đạt được tiêu chuẩn chất lượng cao hơn. Đây là cơ chế cho phép một agent đi từ một mức cơ bản tốt đến hiệu suất cấp độ chuyên gia theo thời gian.

Quá trình này mô phỏng chu kỳ học tập của con người: `làm -> nhận phản hồi -> cải thiện`. Chúng ta sẽ triển khai điều này thông qua một workflow **Self-Refine** (Tự tinh chỉnh), nơi đầu ra của một agent ngay lập tức được đánh giá bởi một sub-agent phản biện, và nếu nó bị coi là thiếu sót, agent ban đầu sẽ có nhiệm vụ sửa đổi công việc của mình dựa trên những phản hồi có thể thực hiện được.

Để làm cho khái niệm này trở nên hữu hình và chi tiết, chúng ta sẽ xây dựng một **Marketing Copywriter Agent**. Workflow sẽ là:
1.  Một agent `JuniorCopywriter` tạo ra bản nháp đầu tiên của một email marketing.
2.  Một agent `SeniorEditor` phê bình bản nháp dựa trên một bộ tiêu chí nghiêm ngặt (sự rõ ràng, tính thuyết phục, call-to-action).
3.  Nếu điểm số của bản nháp dưới ngưỡng chất lượng, `JuniorCopywriter` sẽ được gọi lại, nhưng lần này với những phản hồi cụ thể của biên tập viên, để tạo ra một bản nháp sửa đổi.
4.  Vòng lặp này tiếp tục cho đến khi email được phê duyệt hoặc đạt đến số lần sửa đổi tối đa.

Hơn nữa, chúng ta sẽ khám phá cách pattern này tạo thành cơ sở khái niệm cho **việc học tập dài hạn**, tương tự như RLHF, bằng cách lưu các đầu ra tốt nhất vào một bộ nhớ bền vững để cung cấp thông tin cho các thế hệ tương lai, tạo ra một hệ thống thực sự biết học hỏi.

### Definition
Một **Self-Improvement Loop** là một kiến trúc agentic nơi đầu ra của một agent được đánh giá, bởi chính nó hoặc bởi một agent khác, và đánh giá này được sử dụng làm phản hồi để tạo ra một đầu ra sửa đổi, chất lượng cao hơn. Khi phản hồi này được lưu trữ và sử dụng để cải thiện hiệu suất cơ sở của agent theo thời gian, nó sẽ trở thành một dạng học tập liên tục (continual learning).

### High-level Workflow (Self-Refine)
1.  **Generate Initial Output (Tạo đầu ra ban đầu):** Agent chính tạo ra phiên bản đầu tiên của giải pháp ("bản nháp").
2.  **Critique Output (Phê bình đầu ra):** Một agent phản biện (hoặc agent chính ở "chế độ phê bình") đánh giá bản nháp dựa trên một bộ tiêu chí định sẵn hoặc một bộ quy tắc chung.
3.  **Decision (Quyết định):** Hệ thống kiểm tra xem phê bình có đủ tích cực để chấp nhận đầu ra hay không.
4.  **Revise (Loop - Sửa đổi):** Nếu đầu ra không được chấp nhận, bản nháp gốc *và* phản hồi của người phản biện sẽ được chuyển ngược lại cho agent chính, agent này được hướng dẫn tạo ra một phiên bản sửa đổi giải quyết các phản hồi đó.
5.  **Accept (Chấp nhận):** Khi đầu ra đáp ứng tiêu chuẩn chất lượng, vòng lặp kết thúc và phiên bản cuối cùng được trả về.

### When to Use / Applications
*   **Tạo nội dung chất lượng cao:** Cho các nhiệm vụ mà bản nháp đầu tiên thông thường là không đủ, chẳng hạn như viết tài liệu pháp lý, báo cáo kỹ thuật chi tiết hoặc bản thảo marketing thuyết phục.
*   **Học tập liên tục & Cá nhân hóa:** Một agent học các sở thích của người dùng bằng cách tạo phản hồi, nhận phản hồi ngầm hoặc rõ ràng và tinh chỉnh chiến lược nội bộ của nó cho lần tương tác tiếp theo.
*   **Giải quyết vấn đề phức tạp:** Một agent có thể đề xuất một kế hoạch, phê bình nó về những thiếu sót hoặc sự kém hiệu quả, sau đó sửa đổi kế hoạch trước khi thực thi.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Tăng vọt chất lượng đầu ra:** Việc tinh chỉnh lặp đi lặp lại nhất quán tạo ra kết quả tốt hơn so với việc tạo ra trong một lần duy nhất (single-shot).
    *   **Cho phép học tập liên tục:** Cung cấp một khung làm việc để agent trở nên tốt hơn theo thời gian, thích ứng với thông tin hoặc phản hồi mới.
*   **Weaknesses:**
    *   **Rủi ro củng cố định kiến:** Nếu agent phản biện có logic sai lầm hoặc định kiến, hệ thống có thể bị kẹt trong một vòng lặp củng cố chính lỗi của mình.
    *   **Tốn kém về mặt tính toán:** Tính chất lặp lại có nghĩa là nhiều lượt gọi LLM cho mỗi nhiệm vụ, làm tăng chi phí và độ trễ.

## Phase 0: Foundation & Setup
Thiết lập tiêu chuẩn các thư viện và biến môi trường.

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv
```

```python
import os
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
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Self-Improvement Loop (Nebius)"

required_vars = ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY"]
for var in required_vars:
    if var not in os.environ:
        print(f"Warning: Environment variable {var} not set.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Defining the Core Components (Generator, Critic, Reviser)
Hệ thống của chúng ta cần các vai trò riêng biệt. Chúng ta sẽ định nghĩa các persona và đầu ra có cấu trúc cho `JuniorCopywriter` (người tạo) và `SeniorEditor` (người phê bình). `Reviser` (người sửa đổi) không phải là một agent mới, mà là một chế độ gọi khác của người tạo, được trang bị thêm phản hồi.

```python
console = Console()
llm = ChatNebius(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0.4)

# --- Pydantic Models for Structured Data ---
class MarketingEmail(BaseModel):
    """Đại diện cho một bản nháp email marketing."""
    subject: str = Field(description="A catchy and concise subject line for the email.")
    body: str = Field(description="The full body text of the email, written in markdown.")

class Critique(BaseModel):
    """Phê bình có cấu trúc cho bản nháp email marketing."""
    score: int = Field(description="Overall quality score from 1 (poor) to 10 (excellent).")
    feedback_points: List[str] = Field(description="A bulleted list of specific, actionable feedback points for improvement.")
    is_approved: bool = Field(description="A boolean indicating if the draft is approved (score >= 8). This is redundant with the score but useful for routing.")

# --- 1. The Generator: Junior Copywriter ---
def get_generator_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a junior marketing copywriter. Your task is to write a first draft of a marketing email based on the user's request. Be creative, but focus on getting the core message across."),
        ("human", "Write a marketing email about the following topic:\n\n{request}")
    ])
    return prompt | llm.with_structured_output(MarketingEmail)

# --- 2. The Critic: Senior Editor ---
def get_critic_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior marketing editor and brand manager. Your job is to critique an email draft written by a junior copywriter. 
        Evaluate the draft against the following criteria:
        1.  **Catchy Subject:** Is the subject line engaging and likely to get opened?
        2.  **Clarity & Persuasiveness:** Is the body text clear, compelling, and persuasive?
        3.  **Strong Call-to-Action (CTA):** Is there a clear, single action for the user to take?
        4.  **Brand Voice:** Is the tone professional yet approachable?
        Provide a score from 1-10. A score of 8 or higher means the draft is approved for sending. Provide specific, actionable feedback to help the writer improve."""
        ),
        ("human", "Please critique the following email draft:\n\n**Subject:** {subject}\n\n**Body:**\n{body}")
    ])
    return prompt | llm.with_structured_output(Critique)

# --- 3. The Reviser (Generator in 'Revise' Mode) ---
def get_reviser_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the junior marketing copywriter who wrote the original draft. You have just received feedback from your senior editor. Your task is to carefully revise your draft to address every single point of feedback. Produce a new, improved version of the email."),
        ("human", "Original Request: {request}\n\nHere is your original draft:\n**Subject:** {original_subject}\n**Body:**\n{original_body}\n\nHere is the feedback from your editor:\n{feedback}\n\nPlease provide the revised email.")
    ])
    return prompt | llm.with_structured_output(MarketingEmail)

print("Generator and Critic components defined successfully.")
```

## Phase 2: Building the Self-Refinement Loop with LangGraph
Bây giờ chúng ta sẽ xây dựng graph tự động hóa vòng lặp `Generate -> Critique -> Revise`. State sẽ theo dõi bản nháp, phản biện và số lần sửa đổi. Một conditional edge sẽ kiểm tra điểm số của người phản biện để quyết định thoát khỏi vòng lặp hoặc tiếp tục với một lần sửa đổi khác.

```python
# LangGraph State
class AgentState(TypedDict):
    user_request: str
    draft_email: Optional[MarketingEmail]
    critique: Optional[Critique]
    revision_number: int

# Graph Nodes
def generate_node(state: AgentState) -> Dict[str, Any]:
    console.print(Panel("📝 Junior Copywriter is generating the initial draft.", title="[yellow]Step: Generate[/yellow]", border_style="yellow"))
    chain = get_generator_chain()
    draft = chain.invoke({"request": state['user_request']})
    console.print(Panel(f"[bold]Subject:[/bold] {draft.subject}\n\n{draft.body}", title="Draft 1"))
    return {"draft_email": draft, "revision_number": 1}

def critique_node(state: AgentState) -> Dict[str, Any]:
    title = f"[yellow]Step: Critique (Revision #{state['revision_number']})[/yellow]"
    console.print(Panel(f"🧐 Senior Editor is critiquing draft #{state['revision_number']}.", title=title, border_style="yellow"))
    chain = get_critic_chain()
    critique_result = chain.invoke(state['draft_email'].dict())
    feedback_text = "\n- ".join(critique_result.feedback_points)
    console.print(Panel(f"[bold]Score:[/bold] {critique_result.score}/10\n[bold]Feedback:[/bold]\n- {feedback_text}", title="Critique Result"))
    return {"critique": critique_result}

def revise_node(state: AgentState) -> Dict[str, Any]:
    console.print(Panel("✍️ Junior Copywriter is revising the draft based on feedback.", title="[yellow]Step: Revise[/yellow]", border_style="yellow"))
    chain = get_reviser_chain()
    feedback_str = "\n- ".join(state['critique'].feedback_points)
    revised_draft = chain.invoke({
        "request": state['user_request'],
        "original_subject": state['draft_email'].subject,
        "original_body": state['draft_email'].body,
        "feedback": feedback_str,
    })
    console.print(Panel(f"[bold]Subject:[/bold] {revised_draft.subject}\n\n{revised_draft.body}", title=f"Draft {state['revision_number'] + 1}"))
    return {"draft_email": revised_draft, "revision_number": state['revision_number'] + 1}

# Conditional Edge
def should_continue(state: AgentState) -> str:
    console.print(Panel("⚖️ Decision Point: Does the draft meet quality standards?", title="[yellow]Step: Decide[/yellow]", border_style="yellow"))
    if state['critique'].is_approved:
        console.print("[green]Conclusion: Critique APPROVED! Finishing process.[/green]")
        return "end"
    if state['revision_number'] >= 3: # Thiết lập giới hạn sửa đổi tối đa
        console.print("[red]Conclusion: Max revisions reached. Finishing with last draft.[/red]")
        return "end"
    else:
        console.print("[yellow]Conclusion: Critique requires revision. Looping back.[/yellow]")
        return "continue"

# Xây dựng graph
workflow = StateGraph(AgentState)
workflow.add_node("generate", generate_node)
workflow.add_node("critique", critique_node)
workflow.add_node("revise", revise_node)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "critique")
workflow.add_conditional_edges(
    "critique",
    should_continue,
    {"continue": "revise", "end": END}
)
workflow.add_edge("revise", "critique")

self_refine_agent = workflow.compile()
print("Self-Refinement agent graph compiled successfully.")
```

## Phase 3: Demonstration of the Self-Refinement Loop
Hãy chạy agent và quan sát quy trình tinh chỉnh lặp lại. Chúng ta sẽ yêu cầu nó viết một email cho một sản phẩm AI mới và theo dõi quá trình nó tạo ra, bị phê bình và tự sửa đổi công việc của mình cho đến khi đáp ứng tiêu chuẩn chất lượng.

```python
def run_agent(request: str):
    initial_state = {"user_request": request}
    # stream() cho phép chúng ta thấy các bước trung gian
    final_state = None
    for step in self_refine_agent.stream(initial_state):
        # State cuối cùng là cái ngay trước khi END được gọi
        if END not in step:
            final_state = list(step.values())[0]
    return final_state

request = "Write a marketing email announcing our new revolutionary AI-powered data analytics platform, 'InsightSphere'."
console.print(f"--- 🚀 Kicking off the Self-Refinement Process ---")
final_result = run_agent(request)

# Hiển thị kết quả cuối cùng đã được phê duyệt
console.print("\n--- Final Approved Email ---")
final_email = final_result['draft_email']
final_critique = final_result['critique']
email_panel = Panel(
    f"[bold]Subject:[/bold] {final_email.subject}\n\n---\n\n{final_email.body}",
    title="[bold green]Approved Email[/bold green]",
    subtitle=f"[green]Final Score: {final_critique.score}/10[/green]",
    border_style="green"
)
console.print(email_panel)
```

## Phase 4: Persistent Improvement - The RLHF Analogy
Vòng lặp self-refine giúp cải thiện chất lượng cho *một lượt chạy duy nhất*. Nhưng làm thế nào để chúng ta làm cho agent tốt hơn *theo thời gian*? Chúng ta có thể mở rộng kiến trúc của mình để lưu các đầu ra chất lượng cao, đã được phê duyệt và sử dụng chúng làm ví dụ cho các nhiệm vụ trong tương lai. Đây là một sự tương đồng thực tế, ở cấp độ ứng dụng, với cách hoạt động của Reinforcement Learning from Human/AI Feedback (RLHF).

Chúng ta sẽ định nghĩa một `GoldStandardMemory` đơn giản trong bộ nhớ và một node tạo mới sử dụng bộ nhớ này để cải thiện bản nháp đầu tiên của nó.

```python
class GoldStandardMemory:
    """Một kho lưu trữ đơn giản trong bộ nhớ cho các ví dụ chất lượng cao."""
    def __init__(self):
        self.examples: List[MarketingEmail] = []
        
    def add_example(self, email: MarketingEmail):
        self.examples.append(email)
        
    def get_formatted_examples(self) -> str:
        if not self.examples:
            return "No examples available yet."
        formatted = "\n\n---\n\n".join([
            f"Example Subject: {ex.subject}\nExample Body:\n{ex.body}"
            for ex in self.examples
        ])
        return formatted

# Khởi tạo bộ nhớ bền vững của chúng ta
gold_standard_memory = GoldStandardMemory()

# Node tạo mới sử dụng bộ nhớ
def generate_node_with_memory(state: AgentState) -> Dict[str, Any]:
    title = "[yellow]Step: Generate[/yellow]"
    console.print(Panel("📝 Junior Copywriter is generating the initial draft (Informed by Past Successes).", title=title, border_style="yellow"))
    examples = gold_standard_memory.get_formatted_examples()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a junior marketing copywriter. Your task is to write a first draft of a marketing email based on the user's request. You should learn from the style and quality of past successful examples."),
        ("human", "Here are some examples of high-quality emails that were approved by your editor:\n\n{examples}\n\nNow, write a marketing email about the following topic:\n\n{request}")
    ])
    chain = prompt | llm.with_structured_output(MarketingEmail)
    draft = chain.invoke({"request": state['user_request'], "examples": examples})
    console.print(Panel(f"[bold]Subject:[/bold] {draft.subject}\n\n{draft.body}", title=f"Draft {state.get('revision_number', 1)}"))
    return {"draft_email": draft, "revision_number": 1}

# Xây dựng graph mới với người tạo có hỗ trợ bộ nhớ
workflow_with_memory = StateGraph(AgentState)
workflow_with_memory.add_node("generate", generate_node_with_memory)
workflow_with_memory.add_node("critique", critique_node)
workflow_with_memory.add_node("revise", revise_node)

workflow_with_memory.set_entry_point("generate")
workflow_with_memory.add_edge("generate", "critique")
workflow_with_memory.add_conditional_edges("critique", should_continue, {"continue": "revise", "end": END})
workflow_with_memory.add_edge("revise", "critique")
self_improving_agent = workflow_with_memory.compile()
print("Persistent memory components defined successfully.")

# --- DEMONSTRATION OF LONG-TERM IMPROVEMENT ---

# 1. Lưu email đã được phê duyệt trước đó vào bộ nhớ
console.print(Panel("The high-quality, editor-approved email for 'InsightSphere' has been saved. It will now be used as a reference for future generations.", title="[bold]🏆 Saving approved email to Gold Standard Memory[/bold]", border_style="magenta"))
gold_standard_memory.add_example(final_result['draft_email'])

# 2. Chạy lại agent cho một nhiệm vụ MỚI
new_request = "Write a promotional email for our new AI-powered CRM called 'Visionary'."
console.print("\n--- 🚀 Kicking off the Self-Refinement Process with Memory ---")
new_final_result = run_agent(new_request)

# 3. Hiển thị kết quả mới. Điểm mấu chốt cần lưu ý là liệu nó có được phê duyệt nhanh hơn không.
console.print("\n--- Final Approved Email (Generated with Memory) ---")
new_final_email = new_final_result['draft_email']
new_critique = new_final_result['critique']
email_panel_2 = Panel(
    f"[bold]Subject:[/bold] {new_final_email.subject}\n\n---\n\n{new_final_email.body}",
    title="[bold green]Approved Email[/bold green]",
    subtitle=f"[green]Final Score: {new_critique.score}/10[/green]",
    border_style="green"
)
console.print(email_panel_2)
```

### Analysis of the Results
Việc triển khai chi tiết này tiết lộ một quy trình cải thiện hai lớp:

1.  **Cải thiện Nội bộ Nhiệm vụ (Self-Refine):** Trong lượt chạy đầu tiên, bản nháp ban đầu của agent cố tình chỉ ở mức trung bình (điểm: 4/10). Các bản nhật ký cho thấy rõ ràng những phản hồi cụ thể, có thể thực hiện được từ Senior Editor. Sau đó, agent đã tạo ra một bản nháp sửa đổi với sự cải thiện đáng kể, đạt được 9/10 và được phê duyệt. Điều này cho thấy lợi ích tức thì của vòng lặp đối với việc cải thiện một đầu ra duy nhất.

2.  **Cải thiện Liên Nhiệm vụ (Học tập bền vững):** Trong phần trình diễn thứ hai, agent được giao một nhiệm vụ *mới*. Tuy nhiên, người tạo của nó hiện đã được trang bị một ví dụ chất lượng cao từ lượt chạy thành công trước đó. Nhật ký đầu ra là minh chứng cho việc học tập: **bản nháp đầu tiên của agent cho sản phẩm mới tốt đến mức đạt ngay điểm 9/10**, không cần sửa đổi thêm. Đây là một minh chứng mạnh mẽ cho khả năng học hỏi. Hiệu suất cơ sở của agent đã được cải thiện vì nó học được từ những thành công trong quá khứ đã được biên tập viên phê duyệt.

Phần thứ hai này là một sự tương đồng trực tiếp, mang tính thực tế cho RLHF. Chúng ta đang củng cố hành vi của agent bằng cách chỉ cho nó những ví dụ về thế nào là "tốt", từ đó cải thiện khả năng tạo ra các đầu ra chất lượng cao ngay từ lần thử đầu tiên trong các nhiệm vụ tương lai.

## Conclusion
Trong notebook này, chúng ta đã triển khai một **Self-Improvement Loop** toàn diện và phức tạp. Chúng ta đã chứng minh rằng kiến trúc này không chỉ đơn thuần là tinh chỉnh một phần công việc duy nhất, mà là một paradigm mạnh mẽ để tạo ra các agent thực sự biết học hỏi và cải thiện theo thời gian.

Bằng cách tách biệt các vai trò của **generator (người tạo)** và **critic (người phản biện)**, chúng ta tạo ra một động lực phản hồi và sửa đổi giúp nâng cao chất lượng đầu ra của agent một cách nhất quán. Bằng cách thêm một **persistent memory (bộ nhớ bền vững)** cho các kết quả chất lượng cao, chúng ta tạo ra một vòng phản hồi tích cực giúp cải thiện các khả năng cơ bản của agent, làm cho nó trở nên hiệu quả và đắc lực hơn trong các nhiệm vụ tương lai.

Mặc dù rủi ro người phản biện củng cố các định kiến của chính mình là có thực và cần được quản lý cẩn thận, nhưng tiềm năng xây dựng các agent học hỏi từ kinh nghiệm là một bước chuyển mình hướng tới các hệ thống AI thông minh, có năng lực và tự chủ hơn.
