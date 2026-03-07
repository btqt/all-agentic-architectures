# 📘 Agentic Architectures 17: Reflexive Metacognitive Agents

Chào mừng bạn đến với phần triển khai chi tiết về một trong những pattern agentic tinh vi nhất: **Reflexive Metacognitive Agent** (Agent siêu nhận thức phản xạ). Kiến trúc này ban tặng cho agent một dạng khả năng tự nhận thức, cho phép nó lập luận về các khả năng, sự tự tin và các hạn chế của chính mình trước khi hành động.

Điều này đi xa hơn một bước so với sự tự phản chiếu (self-reflection) đơn giản. Một agent siêu nhận thức duy trì một **"self-model"** (mô hình bản thân) rõ ràng—một sự đại diện có cấu trúc về kiến thức, công cụ và ranh giới của chính nó. Khi đối mặt với một nhiệm vụ, bước đầu tiên của nó không phải là giải quyết vấn đề, mà là *phân tích vấn đề trong bối cảnh mô hình bản thân của nó*. Nó đặt ra các câu hỏi nội bộ như:
- "Tôi có đủ kiến thức để trả lời câu này một cách tự tin không?"
- "Chủ đề này có nằm trong lĩnh vực chuyên môn được chỉ định của tôi không?"
- "Tôi có công cụ cụ thể nào cần thiết để trả lời câu này một cách an toàn và chính xác không?"
- "Truy vấn của người dùng có thuộc về một chủ đề rủi ro cao, nơi mà một sai sót có thể gây nguy hiểm không?"

Dựa trên các câu trả lời, nó chọn một chiến lược: lập luận trực tiếp, sử dụng một công cụ chuyên dụng, hoặc—quan trọng nhất—**chuyển lên cho con người (escalate)** khi nhiệm vụ vượt quá giới hạn đã biết của nó.

Để xây dựng một bản trình diễn phức tạp và mạnh mẽ, chúng ta sẽ tạo ra một **Medical Triage & Information Assistant** (Trợ lý thông tin & Sàng lọc y tế). Đây là một kịch bản rủi ro cao điển hình, nơi khả năng nhận biết các giới hạn của chính agent không chỉ là một tính năng, mà là một yêu cầu an toàn sống còn.

### Definition
Một **Reflexive Metacognitive Agent** là một agent duy trì và sử dụng một mô hình rõ ràng về các khả năng, ranh giới kiến thức và mức độ tự tin của chính nó để lựa chọn chiến lược phù hợp nhất cho một nhiệm vụ nhất định. Việc tự mô hình hóa này cho phép nó hành xử an toàn và đáng tin cậy hơn, đặc biệt là trong các lĩnh vực mà thông tin sai lệch có thể gây hại.

### High-level Workflow
1.  **Perceive Task (Nhận thức nhiệm vụ):** Agent nhận được yêu cầu từ người dùng.
2.  **Metacognitive Analysis (Self-Reflection - Phân tích siêu nhận thức):** Công cụ lập luận cốt lõi của agent phân tích yêu cầu *so với mô hình bản thân của chính nó*. Nó đánh giá sự tự tin, mức độ liên quan của các công cụ và liệu truy vấn có nằm trong phạm vi hoạt động đã định trước hay không.
3.  **Strategy Selection (Lựa chọn chiến lược):** Dựa trên phân tích, agent chọn một trong các chiến lược sau:
    *   **Reason Directly (Lập luận trực tiếp):** Cho các truy vấn có độ tự tin cao, rủi ro thấp trong cơ sở kiến thức của nó.
    *   **Use Tool (Sử dụng công cụ):** Khi truy vấn yêu cầu một khả năng cụ thể mà agent sở hữu thông qua một công cụ.
    *   **Escalate/Refuse (Chuyển tiếp/Từ chối):** Cho các truy vấn có độ tự tin thấp, rủi ro cao hoặc nằm ngoài phạm vi.
4.  **Execute Strategy (Thực thi chiến lược):** Con đường đã chọn được thực hiện.
5.  **Respond (Phản hồi):** Agent cung cấp kết quả, có thể là câu trả lời trực tiếp, câu trả lời được hỗ trợ bởi công cụ hoặc lời từ chối an toàn kèm theo hướng dẫn tham khảo ý kiến chuyên gia.

### When to Use / Applications
*   **Hệ thống tư vấn rủi ro cao:** Bất kỳ hệ thống nào cung cấp thông tin trong các lĩnh vực như y tế, luật pháp hoặc tài chính, nơi agent phải có khả năng nói "Tôi không biết" hoặc "Bạn nên tham khảo ý kiến chuyên gia".
*   **Hệ thống tự trị:** Một robot phải đánh giá khả năng thực hiện một nhiệm vụ vật lý một cách an toàn trước khi thử thực hiện nó.
*   **Điều phối công cụ phức tạp:** Một agent phải chọn đúng API từ một thư viện khổng lồ, hiểu rằng một số API nguy hiểm hoặc tốn kém hơn những API khác.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Tăng cường an toàn và tin cậy:** Lợi ích chính. Agent được thiết kế rõ ràng để tránh đưa ra các khẳng định chắc chắn trong những lĩnh vực mà nó không phải là chuyên gia.
    *   **Cải thiện việc ra quyết định:** Dẫn đến hành vi mạnh mẽ hơn bằng cách buộc phải lựa chọn chiến lược có tính toán thay vì thử nghiệm trực tiếp một cách ngây thơ.
*   **Weaknesses:**
    *   **Độ phức tạp của mô hình bản thân:** Việc định nghĩa và duy trì một mô hình bản thân chính xác có thể rất phức tạp.
    *   **Chi phí siêu nhận thức:** Bước phân tích ban đầu làm tăng độ trễ và chi phí tính toán cho mọi yêu cầu.

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
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Metacognitive Agent (Nebius)"

required_vars = ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY"]
for var in required_vars:
    if var not in os.environ:
        print(f"Warning: Environment variable {var} not set.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Defining the Agent's Self-Model and Tools
Đây là nền tảng cho khả năng tự nhận thức của agent. Chúng ta sẽ tạo ra một `AgentSelfModel` có cấu trúc và một công cụ chuyên dụng. Mô hình này không chỉ là một câu lệnh (prompt); nó là một đối tượng cấu hình sẽ được chuyển vào vòng lặp lập luận của agent.

```python
console = Console()

# --- The Agent's Self-Model ---
class AgentSelfModel(BaseModel):
    """Một sự đại diện có cấu trúc về các khả năng và hạn chế của agent."""
    name: str
    role: str
    # Các ranh giới kiến thức rõ ràng của agent
    knowledge_domain: List[str] = Field(description="List of topics the agent is knowledgeable about.")
    # Các công cụ có sẵn của agent
    available_tools: List[str] = Field(description="List of tools the agent can use.")
    confidence_threshold: float = Field(description="The confidence level (0-1) below which the agent must escalate.", default=0.6)

# Khởi tạo mô hình bản thân cho Triage Agent y tế của chúng ta
medical_agent_model = AgentSelfModel(
    name="TriageBot-3000",
    role="A helpful AI assistant for providing preliminary medical information.",
    knowledge_domain=["common_cold", "influenza", "allergies", "headaches", "basic_first_aid"],
    available_tools=["drug_interaction_checker"]
)

# --- Specialist Tools ---
class DrugInteractionChecker:
    """Một công cụ giả lập để kiểm tra tương tác thuốc."""
    def check(self, drug_a: str, drug_b: str) -> str:
        """Kiểm tra tương tác giữa hai loại thuốc."""
        # Trong một hệ thống thực, việc này sẽ truy vấn một cơ sở dữ liệu y tế.
        known_interactions = {
            frozenset(["ibuprofen", "lisinopril"]): "Moderate risk: Ibuprofen may reduce the blood pressure-lowering effects of lisinopril. Monitor blood pressure.",
            frozenset(["aspirin", "warfarin"]): "High risk: Increased risk of bleeding. This combination should be avoided unless directed by a doctor."
        }
        interaction = known_interactions.get(frozenset([drug_a.lower(), drug_b.lower()]))
        if interaction:
            return f"Interaction Found: {interaction}"
        return "No known significant interactions found. However, always consult a pharmacist or doctor."

drug_tool = DrugInteractionChecker()
print("Agent Self-Model and Tools defined successfully.")
```

## Phase 2: Building the Metacognitive Agent with LangGraph
Đây là nơi điều kỳ diệu xảy ra. Chúng ta sẽ xây dựng một graph trong đó bước đầu tiên chính là **phân tích siêu nhận thức**. Node này sẽ sử dụng một prompt mạnh mẽ, chi tiết để khiến agent lập luận về chính nó. Một router có điều kiện sau đó sẽ hướng dòng chảy dựa trên chiến lược đã chọn.

```python
llm = ChatNebius(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0)

# Pydantic Models cho đầu ra có cấu trúc
class MetacognitiveAnalysis(BaseModel):
    """Tự phân tích của agent về một truy vấn."""
    confidence: float = Field(description="A score from 0.0 to 1.0 representing the agent's confidence in its ability to answer safely and accurately.")
    strategy: str = Field(description="The chosen strategy. Must be one of: 'reason_directly', 'use_tool', 'escalate'.")
    reasoning: str = Field(description="A brief justification for the chosen confidence and strategy.")
    tool_to_use: Optional[str] = Field(description="If strategy is 'use_tool', the name of the tool to use.", default=None)
    tool_args: Optional[Dict[str, Any]] = Field(description="If strategy is 'use_tool', the arguments for the tool.", default=None)

# LangGraph State
class AgentState(TypedDict):
    user_query: str
    self_model: AgentSelfModel
    metacognitive_analysis: Optional[MetacognitiveAnalysis]
    tool_output: Optional[str]
    final_response: str

# Graph Nodes
def metacognitive_analysis_node(state: AgentState) -> Dict[str, Any]:
    console.print(Panel("🤔 Agent is performing metacognitive analysis...", title="[yellow]Step: Self-Reflection[/yellow]"))
    prompt = ChatPromptTemplate.from_template(
        """You are a metacognitive reasoning engine for an AI assistant. Your task is to analyze a user's query in the context of the agent's own capabilities and limitations (its 'self-model').
        Your primary directive is **SAFETY**. You must determine the safest and most appropriate strategy for handling the query.

        **Agent's Self-Model:**
        - Name: {agent_name}
        - Role: {agent_role}
        - Knowledge Domain: {knowledge_domain}
        - Available Tools: {available_tools}

        **Strategy Rules:**
        1.  **escalate:** Choose this strategy if the query involves a potential medical emergency (e.g., chest pain, difficulty breathing, severe injury, broken bones), is outside the agent's knowledge domain, or if you have any doubt about providing a safe answer. **WHEN IN DOUBT, ESCALATE.**
        2.  **use_tool:** Choose this strategy if the query explicitly or implicitly requires one of the available tools. For example, a question about drug interactions requires the 'drug_interaction_checker'.
        3.  **reason_directly:** Choose this strategy ONLY if you are highly confident the query is a simple, low-risk question that falls squarely within the agent's knowledge domain.

        Analyze the user query below and provide your metacognitive analysis in the required format.

        **User Query:** "{query}""""
    )
    chain = prompt | llm.with_structured_output(MetacognitiveAnalysis)
    analysis = chain.invoke({
        "query": state['user_query'],
        "agent_name": state['self_model'].name,
        "agent_role": state['self_model'].role,
        "knowledge_domain": ", ".join(state['self_model'].knowledge_domain),
        "available_tools": ", ".join(state['self_model'].available_tools),
    })
    console.print(Panel(f"[bold]Confidence:[/bold] {analysis.confidence:.2f}\n[bold]Strategy:[/bold] {analysis.strategy}\n[bold]Reasoning:[/bold] {analysis.reasoning}", title="Metacognitive Analysis Result"))
    return {"metacognitive_analysis": analysis}

def reason_directly_node(state: AgentState) -> Dict[str, Any]:
    console.print(Panel("✅ Confident in direct answer. Generating response...", title="[green]Strategy: Reason Directly[/green]"))
    prompt = ChatPromptTemplate.from_template("You are {agent_role}. Provide a helpful, non-prescriptive answer to the user's query. Remind the user that you are not a doctor.\n\nQuery: {query}")
    chain = prompt | llm
    response = chain.invoke({"agent_role": state['self_model'].role, "query": state['user_query']}).content
    return {"final_response": response}

def call_tool_node(state: AgentState) -> Dict[str, Any]:
    console.print(Panel(f"🛠️ Confidence requires tool use. Calling `{state['metacognitive_analysis'].tool_to_use}`...", title="[cyan]Strategy: Use Tool[/cyan]"))
    analysis = state['metacognitive_analysis']
    if analysis.tool_to_use == 'drug_interaction_checker':
        tool_output = drug_tool.check(**analysis.tool_args)
        return {"tool_output": tool_output}
    return {"tool_output": "Error: Tool not found."}

def synthesize_tool_response_node(state: AgentState) -> Dict[str, Any]:
    console.print(Panel("📝 Synthesizing final response from tool output...", title="[cyan]Step: Synthesize[/cyan]"))
    prompt = ChatPromptTemplate.from_template("You are {agent_role}. You have used a tool to get specific information. Now, present this information to the user in a clear and helpful way. ALWAYS include a disclaimer to consult a healthcare professional.\n\nOriginal Query: {query}\nTool Output: {tool_output}")
    chain = prompt | llm
    response = chain.invoke({"agent_role": state['self_model'].role, "query": state['user_query'], "tool_output": state['tool_output']}).content
    return {"final_response": response}

def escalate_to_human_node(state: AgentState) -> Dict[str, Any]:
    console.print(Panel("🚨 Low confidence or high risk detected. Escalating to human.", title="[bold red]Strategy: Escalate[/bold red]"))
    response = "I am an AI assistant and not qualified to provide information on this topic. This query is outside my knowledge domain or involves potentially serious symptoms. **Please consult a qualified medical professional immediately.**"
    return {"final_response": response}

# Conditional Edge
def route_strategy(state: AgentState) -> str:
    return state["metacognitive_analysis"].strategy

# Xây dựng graph
workflow = StateGraph(AgentState)
workflow.add_node("analyze", metacognitive_analysis_node)
workflow.add_node("reason", reason_directly_node)
workflow.add_node("call_tool", call_tool_node)
workflow.add_node("synthesize", synthesize_tool_response_node)
workflow.add_node("escalate", escalate_to_human_node)

workflow.set_entry_point("analyze")
workflow.add_conditional_edges("analyze", route_strategy, {
    "reason_directly": "reason",
    "use_tool": "call_tool",
    "escalate": "escalate"
})
workflow.add_edge("call_tool", "synthesize")
workflow.add_edge("reason", END)
workflow.add_edge("synthesize", END)
workflow.add_edge("escalate", END)

metacognitive_agent = workflow.compile()
print("Reflexive Metacognitive Agent graph compiled successfully.")
```

## Phase 3: Demonstration & Analysis
Bây giờ chúng ta sẽ kiểm tra agent với một loạt các truy vấn ngày càng khó và rủi ro cao. Chúng ta sẽ quan sát cách phân tích siêu nhận thức điều phối chính xác từng truy vấn đi theo con đường thích hợp, chứng minh sự an toàn và khả năng tự nhận thức của hệ thống.

```python
def run_agent(query: str):
    initial_state = {"user_query": query, "self_model": medical_agent_model}
    result = metacognitive_agent.invoke(initial_state)
    console.print(Markdown(result['final_response']))

# Test 1: Đơn giản, nên được trả lời trực tiếp
console.print("--- Test 1: Simple, In-Scope, Low-Risk Query ---")
run_agent("What are the symptoms of a common cold?")

# Test 2: Yêu cầu công cụ cụ thể
console.print("\n--- Test 2: Specific Query Requiring a Tool ---")
run_agent("Is it safe to take Ibuprofen if I am also taking Lisinopril?")

# Test 3: Rủi ro cao, nên được chuyển tiếp ngay lập tức
console.print("\n--- Test 3: High-Stakes, Emergency Query ---")
run_agent("I have a crushing pain in my chest and my left arm feels numb, what should I do?")
```

### Analysis of the Results
Bản trình diễn là một ví dụ minh họa mạnh mẽ về tính an toàn và độ tin cậy mà kiến trúc này mang lại:

1.  **Câu trả lời nằm trong phạm vi chính xác:** Đối với truy vấn 'cảm lạnh thông thường', phân tích siêu nhận thức đã xác định chính xác đây là một chủ đề rủi ro thấp trong phạm vi kiến thức của nó. Nó đặt điểm tự tin cao và chọn chiến lược `reason_directly`, cung cấp câu trả lời hữu ích nhưng có cảnh báo thích hợp.

2.  **Sử dụng công cụ chính xác:** Đối với câu hỏi về tương tác thuốc, phân tích đã nhận ra nhu cầu về một khả năng cụ thể. Nó xác định chính xác rằng cần có công cụ `drug_interaction_checker`, đặt độ tự tin cao *trong khả năng sử dụng công cụ*, và chọn chiến lược `use_tool`. Phản hồi cuối cùng là một bản tóm tắt an toàn, tổng hợp từ đầu ra của công cụ.

3.  **Chuyển tiếp cho an toàn sống còn:** Đây là kết quả quan trọng nhất. Một agent ngây thơ có thể đã cố gắng trả lời truy vấn 'đau ngực' bằng cách tìm kiếm nguyên nhân trên web, có thể cung cấp thông tin nguy hiểm và gây hiểu lầm. Agent siêu nhận thức của chúng ta, được hướng dẫn bởi tiêu chuẩn an toàn hàng đầu, đã ngay lập tức nhận ra các dấu hiệu của một trường hợp cấp cứu y tế. Phân tích siêu nhận thức gán điểm tự tin rất thấp và chọn chính xác chiến lược `escalate`. Đầu ra cuối cùng không phải là một câu trả lời, mà là lời từ chối có trách nhiệm, an toàn và hướng dẫn tìm kiếm sự trợ giúp chuyên nghiệp. Nó đã xác định chính xác các giới hạn về năng lực của chính mình.

Workflow này chứng minh rằng bằng cách buộc agent lập luận về chính nó *trước khi* lập luận về vấn đề, chúng ta có thể xây dựng một lớp an toàn và tin cậy mạnh mẽ vào hoạt động của nó.

## Conclusion
Trong notebook chi tiết này, chúng ta đã triển khai một **Reflexive Metacognitive Agent**, một kiến trúc tinh vi ưu tiên sự an toàn và tin cậy bằng cách ban tặng cho agent khả năng tự nhận thức. Bằng cách xây dựng một `self-model` rõ ràng và buộc phải thực hiện phân tích siêu nhận thức như bước đầu tiên của bất kỳ nhiệm vụ nào, chúng ta đã tạo ra một hệ thống hiểu được ranh giới của chính mình.

Đổi mới quan trọng là sự chuyển dịch trong mục tiêu ban đầu của agent từ "Làm thế nào để tôi trả lời câu này?" sang "*Có nên* trả lời câu này không, và nếu có thì bằng cách nào?" Bước nội soi này cho phép agent linh hoạt chọn chiến lược an toàn và phù hợp nhất—cho dù đó là lập luận trực tiếp, sử dụng công cụ chuyên dụng hay chuyển tiếp quan trọng cho chuyên gia là con người.

Kiến trúc này không chỉ là một kỹ thuật; nó là một triết lý thiết kế. Nó hoàn toàn thiết yếu để tạo ra các agent AI có trách nhiệm, những agent có thể được tin cậy để hoạt động trong các lĩnh vực rủi ro cao, thế giới thực, nơi việc biết những gì bạn *không* biết cũng quan trọng như những gì bạn biết.
