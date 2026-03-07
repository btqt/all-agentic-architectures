# 📘 Agentic Architectures 10: Simulator / Mental-Model-in-the-Loop

Chào mừng bạn đến với notebook thứ mười trong loạt bài của chúng ta. Hôm nay, chúng ta khám phá một kiến trúc tinh vi được thiết kế cho sự an toàn và ra quyết định mạnh mẽ trong các môi trường có rủi ro cao: **Simulator**, còn được gọi là **Mental-Model-in-the-Loop**.

Ý tưởng cốt lõi là cung cấp cho agent khả năng "suy nghĩ trước khi hành động" theo một cách rất cụ thể. Thay vì thực hiện một hành động trong thế giới thực ngay lập tức, trước hết agent sẽ kiểm tra hành động dự kiến của mình trong một phiên bản mô phỏng nội bộ của môi trường. Bằng cách quan sát các hệ quả có khả năng xảy ra trong "hộp cát" (sandbox) an toàn này, nó có thể đánh giá rủi ro, tinh chỉnh chiến lược của mình và chỉ sau đó mới thực thi một hành động đã được cân nhắc kỹ lưỡng hơn trong thực tế.

Chúng ta sẽ xây dựng một **stock trading agent** đơn giản để chứng minh điều này. "Thế giới thực" sẽ là một market simulator tiến triển từng bước một. Trước khi thực hiện một giao dịch, agent của chúng ta sẽ:
1. Đề xuất một chiến lược chung (ví dụ: "mua quyết đoán").
2. Chạy chiến lược đó qua một phiên bản *fork* (tách nhánh) của market simulator cho nhiều bước trong tương lai để xem các kết quả tiềm năng.
3. Phân tích kết quả mô phỏng để đánh giá rủi ro và lợi nhuận.
4. Đưa ra quyết định cuối cùng, đã được tinh chỉnh (ví dụ: "Mô phỏng cho thấy độ biến động cao; hãy mua một lượng nhỏ hơn.").
5. Thực thi giao dịch đã tinh chỉnh đó trong thị trường thực.

Pattern này là cực kỳ quan trọng để chuyển đổi các agent từ các nhiệm vụ thông tin sang thực hiện các hành động trong thế giới thực, nơi những sai lầm có thể gây ra hậu quả thực tế.

### Definition
Một kiến trúc **Simulator** hoặc **Mental-Model-in-the-Loop** bao gồm một agent sử dụng một mô hình nội bộ về môi trường của nó để mô phỏng các kết quả của các hành động tiềm năng trước khi thực thi bất kỳ hành động nào trong số đó. Điều này cho phép agent thực hiện phân tích 'what-if' (điều gì xảy ra nếu), dự đoán các hệ quả và tinh chỉnh kế hoạch của mình để đảm bảo an toàn và hiệu quả.

### High-level Workflow
1.  **Observe (Quan sát):** Agent quan sát trạng thái hiện tại của môi trường thực.
2.  **Propose Action (Đề xuất hành động):** Dựa trên các mục tiêu và trạng thái hiện tại, module lập kế hoạch của agent tạo ra một hành động hoặc chiến lược đề xuất ở mức độ cao.
3.  **Simulate (Mô phỏng):** Agent tách (fork) trạng thái hiện tại của môi trường vào một mô phỏng trong hộp cát. Nó áp dụng hành động đề xuất và chạy mô phỏng về phía trước để quan sát một loạt các kết quả có thể xảy ra.
4.  **Assess & Refine (Đánh giá & Tinh chỉnh):** Agent phân tích kết quả từ mô phỏng. Hành động đó có dẫn đến kết quả mong muốn không? Có những hệ quả tiêu cực không lường trước được không? Dựa trên đánh giá này, nó tinh chỉnh đề xuất ban đầu thành một hành động cụ thể, cuối cùng.
5.  **Execute (Thực thi):** Agent thực thi hành động cuối cùng, đã tinh chỉnh trong môi trường *thực*.
6.  **Repeat (Lặp lại):** Vòng lặp bắt đầu lại từ trạng thái mới của môi trường thực.

### When to Use / Applications
*   **Robotics:** Mô phỏng một thao tác cầm nắm hoặc một con đường trước khi di chuyển một cánh tay vật lý để tránh va chạm hoặc hư hỏng.
*   **Ra quyết định rủi ro cao:** Trong tài chính, mô phỏng tác động của một giao dịch đối với danh mục đầu tư dưới các điều kiện thị trường khác nhau. Trong y tế, mô phỏng tác động tiềm năng của một kế hoạch điều trị.
*   **AI trong trò chơi phức tạp:** Một AI trong một trò chơi chiến thuật mô phỏng vài bước đi trước để chọn ra bước đi tối ưu.

### Strengths & Weaknesses
*   **Strengths:**
    *   **An toàn & Giảm thiểu rủi ro:** Giảm đáng kể khả năng xảy ra các sai lầm có hại hoặc tốn kém bằng cách kiểm tra các hành động trong một môi trường an toàn trước.
    *   **Cải thiện hiệu năng:** Dẫn đến các quyết định mạnh mẽ và được cân nhắc kỹ lưỡng hơn bằng cách cho phép nhìn xa và lập kế hoạch.
*   **Weaknesses:**
    *   **Khoảng cách Mô phỏng-Thực tế (Simulation-Reality Gap):** Hiệu quả phụ thuộc hoàn toàn vào độ trung thực của simulator. Nếu mô hình thế giới không chính xác, các kế hoạch của agent có thể dựa trên các giả định sai lầm.
    *   **Chi phí tính toán:** Việc chạy các mô phỏng, đặc biệt là nhiều kịch bản, rất tốn kém tài nguyên tính toán và chậm hơn so với việc hành động trực tiếp.

## Phase 0: Foundation & Setup
Chúng ta sẽ cài đặt các thư viện và thiết lập môi trường.

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv numpy
```

```python
import os
import random
import numpy as np
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
from rich.table import Table

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Simulator (Nebius)"

required_vars = ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY"]
for var in required_vars:
    if var not in os.environ:
        print(f"Warning: Environment variable {var} not set.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Building the Simulator Environment
Đầu tiên, chúng ta cần tạo ra "thế giới" mà agent sẽ tương tác. Chúng ta sẽ xây dựng một class `MarketSimulator` quản lý trạng thái của một cổ phiếu, một danh mục đầu tư và bao gồm một hàm `step` để tiến triển thời gian. Đây sẽ đóng vai trò là cả "thế giới thực" và hộp cát cho các mô phỏng của agent.

```python
console = Console()

class Portfolio(BaseModel):
    cash: float = 10000.0
    shares: int = 0
    
    def value(self, current_price: float) -> float:
        return self.cash + self.shares * current_price

class MarketSimulator(BaseModel):
    """Một mô phỏng đơn giản về thị trường chứng khoán cho một tài sản."""
    day: int = 0
    price: float = 100.0
    volatility: float = 0.1 # Độ lệch chuẩn cho thay đổi giá
    drift: float = 0.01 # Xu hướng chung
    market_news: str = "Market is stable."
    portfolio: Portfolio = Field(default_factory=Portfolio)

    def step(self, action: str, amount: float = 0.0):
        """Tiến triển mô phỏng thêm một ngày, thực hiện giao dịch trước."""
        # 1. Thực thi giao dịch
        if action == "buy": # amount là số lượng cổ phiếu
            shares_to_buy = int(amount)
            cost = shares_to_buy * self.price
            if self.portfolio.cash >= cost:
                self.portfolio.shares += shares_to_buy
                self.portfolio.cash -= cost
        elif action == "sell": # amount là số lượng cổ phiếu
            shares_to_sell = int(amount)
            if self.portfolio.shares >= shares_to_sell:
                self.portfolio.shares -= shares_to_sell
                self.portfolio.cash += shares_to_sell * self.price
        
        # 2. Cập nhật giá thị trường (Geometric Brownian Motion)
        daily_return = np.random.normal(self.drift, self.volatility)
        self.price *= (1 + daily_return)
        
        # 3. Tiến triển thời gian
        self.day += 1
        
        # 4. Có khả năng cập nhật tin tức
        if random.random() < 0.1: # 10% cơ hội có tin tức mới
            self.market_news = random.choice(["Positive earnings report expected.", "New competitor enters the market.", "Macroeconomic outlook is strong.", "Regulatory concerns are growing."])
            # Tin tức ảnh hưởng đến drift
            if "Positive" in self.market_news or "strong" in self.market_news:
                self.drift = 0.05
            else:
                self.drift = -0.05
        else:
             self.drift = 0.01 # Trở lại drift bình thường

    def get_state_string(self) -> str:
        return f"Day {self.day}: Price=${self.price:.2f}, News: {self.market_news}\nPortfolio: ${self.portfolio.value(self.price):.2f} ({self.portfolio.shares} shares, ${self.portfolio.cash:.2f} cash)"

print("Market simulator environment defined successfully.")
```

## Phase 2: Building the Simulator Agent
Bây giờ chúng ta sẽ dùng LangGraph để điều phối workflow `Observe -> Propose -> Simulate -> Refine -> Execute`. Chúng ta sẽ định nghĩa các Pydantic models cho kết quả đầu ra của LLM để đảm bảo giao tiếp có cấu trúc giữa các bước.

```python
llm = ChatNebius(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0.4)

# Pydantic models cho structured LLM outputs
class ProposedAction(BaseModel):
    """Chiến lược cấp cao được đề xuất bởi nhà phân tích.""" 
    strategy: str = Field(description="A high-level trading strategy, e.g., 'buy aggressively', 'sell cautiously', 'hold'.")
    reasoning: str = Field(description="Brief reasoning for the proposed strategy.")

class FinalDecision(BaseModel):
    """Hành động cụ thể, cuối cùng được thực thi."""
    action: str = Field(description="The final action to take: 'buy', 'sell', or 'hold'.")
    amount: float = Field(description="The number of shares to buy or sell. Should be 0 if holding.")
    reasoning: str = Field(description="Final reasoning, referencing the simulation results.")

# LangGraph State
class AgentState(TypedDict):
    real_market: MarketSimulator
    proposed_action: Optional[ProposedAction]
    simulation_results: Optional[List[Dict]]
    final_decision: Optional[FinalDecision]

# Graph Nodes
def propose_action_node(state: AgentState) -> Dict[str, Any]:
    """Quan sát thị trường và đề xuất một chiến lược cấp cao."""
    console.print("--- 🧐 Analyst Proposing Action ---")
    prompt = ChatPromptTemplate.from_template(
        "You are a sharp financial analyst. Based on the current market state, propose a trading strategy.\n\nMarket State:\n{market_state}"
    )
    proposer_llm = llm.with_structured_output(ProposedAction)
    chain = prompt | proposer_llm
    proposal = chain.invoke({"market_state": state['real_market'].get_state_string()})
    console.print(f"[yellow]Proposal:[/yellow] {proposal.strategy}. [italic]Reason: {proposal.reasoning}[/italic]")
    return {"proposed_action": proposal}

def run_simulation_node(state: AgentState) -> Dict[str, Any]:
    """Chạy chiến lược đề xuất trong một mô phỏng hộp cát."""
    console.print("--- 🤖 Running Simulations ---")
    strategy = state['proposed_action'].strategy
    num_simulations = 5
    simulation_horizon = 10 # ngày
    results = []

    for i in range(num_simulations):
        # QUAN TRỌNG: Tạo một bản copy sâu để không ảnh hưởng đến trạng thái thị trường thực
        simulated_market = state['real_market'].model_copy(deep=True)
        initial_value = simulated_market.portfolio.value(simulated_market.price)

        # Chuyển đổi chiến lược thành một hành động cụ thể cho mô phỏng
        if "buy" in strategy:
            action = "buy"
            # Quyết đoán = 25% tiền mặt, Thận trọng = 10%
            amount = (simulated_market.portfolio.cash * (0.25 if "aggressively" in strategy else 0.1)) / simulated_market.price
        elif "sell" in strategy:
            action = "sell"
            # Quyết đoán = 25% số lượng cổ phiếu, Thận trọng = 10%
            amount = simulated_market.portfolio.shares * (0.25 if "aggressively" in strategy else 0.1)
        else:
            action = "hold"
            amount = 0
        
        # Chạy mô phỏng về phía trước
        simulated_market.step(action, amount)
        for _ in range(simulation_horizon - 1):
            simulated_market.step("hold") # Chỉ giữ sau hành động ban đầu
        
        final_value = simulated_market.portfolio.value(simulated_market.price)
        results.append({"sim_num": i+1, "initial_value": initial_value, "final_value": final_value, "return_pct": (final_value - initial_value) / initial_value * 100})
    
    console.print("[cyan]Simulation complete. Results will be passed to the risk manager.[/cyan]")
    return {"simulation_results": results}

def refine_and_decide_node(state: AgentState) -> Dict[str, Any]:
    """Phân tích kết quả mô phỏng và đưa ra quyết định cuối cùng, đã được tinh chỉnh."""
    console.print("--- 🧠 Risk Manager Refining Decision ---")
    results_summary = "\n".join([f"Sim {r['sim_num']}: Initial=${r['initial_value']:.2f}, Final=${r['final_value']:.2f}, Return={r['return_pct']:.2f}%" for r in state['simulation_results']])
    
    prompt = ChatPromptTemplate.from_template(
        "You are a cautious risk manager. Your analyst proposed a strategy. You have run simulations to test it. Based on the potential outcomes, make a final, concrete decision. If results are highly variable or negative, reduce risk (e.g., buy/sell fewer shares, or hold).\n\nInitial Proposal: {proposal}\n\nSimulation Results:\n{results}\n\nReal Market State:\n{market_state}"
    )
    decider_llm = llm.with_structured_output(FinalDecision)
    chain = prompt | decider_llm
    final_decision = chain.invoke({
        "proposal": state['proposed_action'].strategy,
        "results": results_summary,
        "market_state": state['real_market'].get_state_string()
    })
    console.print(f"[green]Final Decision:[/green] {final_decision.action} {final_decision.amount:.0f} shares. [italic]Reason: {final_decision.reasoning}[/italic]")
    return {"final_decision": final_decision}

def execute_in_real_world_node(state: AgentState) -> Dict[str, Any]:
    """Thực thi quyết định cuối cùng trong môi trường thị trường thực."""
    console.print("--- 🚀 Executing in Real World ---")
    decision = state['final_decision']
    real_market = state['real_market']
    real_market.step(decision.action, decision.amount)
    console.print(f"[bold]Execution complete. New market state:[/bold]\n{real_market.get_state_string()}")
    return {"real_market": real_market}

# Xây dựng graph
workflow = StateGraph(AgentState)
workflow.add_node("propose", propose_action_node)
workflow.add_node("simulate", run_simulation_node)
workflow.add_node("refine", refine_and_decide_node)
workflow.add_node("execute", execute_in_real_world_node)

workflow.set_entry_point("propose")
workflow.add_edge("propose", "simulate")
workflow.add_edge("simulate", "refine")
workflow.add_edge("refine", "execute")
workflow.add_edge("execute", END)

simulator_agent = workflow.compile()
print("Simulator-in-the-loop agent graph compiled successfully.")
```

## Phase 3: Demonstration
Hãy để agent của chúng ta chạy vài ngày trên thị trường. Chúng ta sẽ bắt đầu với một số tin tốt và xem nó phản ứng thế nào, sau đó đưa vào một số tin xấu.

```python
real_market = MarketSimulator()
console.print("--- Initial Market State ---")
console.print(real_market.get_state_string())

# --- Chạy Ngày 1 ---
console.print("\n--- Day 1: Good News Hits! ---")
real_market.market_news = "Positive earnings report expected."
real_market.drift = 0.05
initial_state = {"real_market": real_market}
final_state = simulator_agent.invoke(initial_state)
real_market = final_state['real_market']

# --- Chạy Ngày 2 ---
console.print("\n--- Day 2: Bad News Hits! ---")
real_market.market_news = "New competitor enters the market."
real_market.drift = -0.05
initial_state = {"real_market": real_market}
final_state = simulator_agent.invoke(initial_state)
real_market = final_state['real_market']
```

### Analysis of the Results
Hành vi của agent chứng minh giá trị của vòng lặp mô phỏng:

- **Vào Ngày 1 (Tin tốt):**
    - *Analyst* đề xuất mua quyết đoán khi nhận thấy cơ hội.
    - *Simulator* xác nhận khả năng cao có kết quả tích cực.
    - *Risk Manager* chuyển chiến lược mua quyết đoán thành một giao dịch mua cụ thể, số lượng lớn (20 cổ phiếu) nhưng không mạo hiểm toàn bộ số dư tiền mặt.

- **Vào Ngày 2 (Tin xấu):**
    - *Analyst* xác định chính xác rủi ro mới và đề xuất bán thận trọng.
    - *Simulator* có khả năng đưa ra một loạt kết quả hỗn hợp, với một số kịch bản cho thấy sự sụt giảm mạnh và một số khác là sự phục hồi, xác nhận sự không chắc chắn.
    - *Risk Manager*, nhận thấy sự biến động và tỷ lệ sinh lời trung bình âm trong các mô phỏng, đã đưa ra quyết định thận trọng là giảm vị thế (bán 5 cổ phiếu) thay vì bán tháo toàn bộ trong hoảng loạn. Đây là một hành động sắc sảo hơn nhiều so với những gì một agent đơn giản dựa trên quy tắc có thể thực hiện.

Một agent đơn giản không có vòng lặp mô phỏng có thể đã mua quá nhiều vào ngày 1 và sau đó bán hết sạch vào ngày 2, làm tăng chi phí giao dịch và có khả năng bỏ lỡ cơ hội phục hồi. Agent mô phỏng của chúng ta hành động giống như một nhà giao dịch thực tế, thực hiện một vụ đặt cược theo xác suất và sau đó phòng vệ cho vụ đặt cược đó khi thông tin mới thay đổi hồ sơ rủi ro.

## Conclusion
Trong notebook này, chúng ta đã xây dựng một kiến trúc agent mạnh mẽ sử dụng một **simulator** nội bộ để kiểm tra và tinh chỉnh các hành động trước khi thực hiện chúng. Bằng cách tạo ra một vòng lặp `Propose -> Simulate -> Refine -> Execute`, chúng ta cho phép agent của mình thực hiện phân tích rủi ro tinh vi và đưa ra các quyết định sắc sảo, an toàn hơn trong một môi trường năng động.

Pattern này là nền tảng để xây dựng các agent có thể hoạt động an toàn và hiệu quả trong thế giới thực. Khả năng thực hiện phân tích 'what-if' trên một "mô hình trí tuệ" (mental model) nội bộ cho phép agent dự đoán các hệ quả, tránh các sai lầm tốn kém và phát triển các chiến lược mạnh mẽ hơn. Mặc dù độ trung thực của simulator là một yếu điểm quan trọng ("khoảng cách mô phỏng-thực tế"), kiến trúc này cung cấp một framework rõ ràng và có thể mở rộng để xây dựng các AI có trách nhiệm và có khả năng hành động.
