# 📘 Agentic Architectures 9: Tree-of-Thoughts Planning

Chào mừng bạn đến với notebook thứ chín trong loạt bài của chúng ta. Hôm nay, chúng ta khám phá một kiến trúc lập luận và lập kế hoạch mạnh mẽ: **Tree-of-Thoughts (ToT)**. Pattern này nâng tầm khả năng giải quyết vấn đề của agent từ một chuỗi suy nghĩ tuyến tính (linear chain of thought) lên một cuộc tìm kiếm khám phá đa con đường.

Thay vì tạo ra một dòng lập luận tuần tự, duy nhất, một ToT agent sẽ tạo ra nhiều "suy nghĩ" (thoughts) ứng viên hoặc các bước tiếp theo tại mỗi giai đoạn của một vấn đề. Sau đó, nó đánh giá những suy nghĩ này, cắt tỉa (pruning) các nhánh không hợp lệ hoặc không hứa hẹn và mở rộng những nhánh hứa hẹn nhất. Điều này tạo ra một cây tìm kiếm (search tree) nơi agent có thể quay lui (backtrack), khám phá các lựa chọn thay thế và điều hướng một không gian vấn đề phức tạp một cách có hệ thống.

Để chứng minh điều này, chúng ta sẽ giao cho agent của mình một câu đố logic cổ điển: **Bài toán Sói, Dê và Bắp cải**. Câu đố này nổi tiếng vì nó yêu cầu các bước không hiển nhiên (như mang một vật *quay trở lại*) và có một vài trạng thái không hợp lệ có thể làm "bẫy" một người lập luận đơn giản. Chúng ta sẽ chỉ ra cách một Chain-of-Thought agent đơn giản có thể thất bại, trong khi ToT agent xây dựng một kế hoạch hợp lệ một cách có phương pháp bằng cách khám phá và đánh giá một cây các khả năng.

### Definition
**Tree-of-Thoughts (ToT)** là một framework lập luận agentic, nơi việc giải quyết vấn đề được mô hình hóa như một cuộc tìm kiếm qua một cái cây. Agent khám phá nhiều con đường lập luận (các nhánh) đồng thời. Tại mỗi bước, nó tạo ra các bước tiếp theo tiềm năng ("suy nghĩ"), đánh giá tính khả thi của chúng và quyết định con đường nào nên tiếp tục khám phá, qua đó cắt tỉa không gian tìm kiếm một cách hiệu quả.

### High-level Workflow
1.  **Decomposition (Phân rã):** Vấn đề được chia nhỏ thành một loạt các bước hoặc suy nghĩ.
2.  **Thought Generation (Tạo suy nghĩ):** Đối với trạng thái hiện tại của vấn đề, agent tạo ra nhiều bước tiếp theo tiềm năng hoặc các suy nghĩ. Điều này tạo ra các nhánh trong cây tìm kiếm.
3.  **State Evaluation (Đánh giá trạng thái):** Mỗi suy nghĩ mới (dẫn đến một trạng thái mới) được đánh giá bởi một "critic" hoặc một hàm thẩm định (validation function). Đánh giá này có thể xem xét:
    *   **Tính hợp lệ (Validity):** Bước đi này có được phép theo quy tắc của bài toán không?
    *   **Tiến độ (Progress):** Bước đi này có đưa chúng ta đến gần giải pháp hơn không?
    *   **Heuristics (Cảm tính):** Con đường này có khả năng thành công cao không?
4.  **Pruning & Expansion (Cắt tỉa & Mở rộng):** Các nhánh không hợp lệ hoặc không khả quan sẽ bị cắt tỉa. Agent sau đó tiếp tục từ những nhánh hoạt động hứa hẹn nhất, lặp lại quá trình tạo suy nghĩ.
5.  **Solution (Giải pháp):** Quá trình tiếp tục cho đến khi đạt được trạng thái mục tiêu. Giải pháp là con đường chứa các suy nghĩ từ gốc (root) đến mục tiêu (goal).

### When to Use / Applications
*   **Câu đố Logic & Bài toán Toán học:** Các vấn đề có quy tắc và trạng thái mục tiêu rõ ràng, yêu cầu lập luận đa bước, phi tuyến tính (ví dụ: Sudoku, các bài toán qua sông).
*   **Lập kế hoạch phức tạp:** Khi một nhiệm vụ yêu cầu một kế hoạch chi tiết, nơi thứ tự các hoạt động là quan trọng và các ràng buộc phải được tôn trọng (ví dụ: lập kế hoạch cho một chuyến đi phức tạp với nhiều chặng và ràng buộc ngân sách).
*   **Sáng tác nội dung hoặc Tạo mã nguồn:** Khám phá nhiều nhánh câu chuyện hoặc chiến lược triển khai trước khi quyết định chọn một cái.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Tính ổn định (Robustness):** Khám phá không gian vấn đề một cách có hệ thống, khiến nó ít có khả năng bị kẹt hoặc đưa ra câu trả lời sai so với phương pháp chạy một lượt (single-pass).
    *   **Xử lý độ phức tạp tổ hợp:** Rất phù hợp cho các vấn đề mà số lượng các chuỗi khả thi là khổng lồ.
*   **Weaknesses:**
    *   **Tốn kém tài nguyên tính toán:** Đòi hỏi nhiều lượt gọi LLM và quản lý trạng thái hơn đáng kể so với một Chain-of-Thought prompt đơn giản, khiến nó chậm hơn và đắt hơn.
    *   **Yêu cầu bộ đánh giá (Evaluator) tốt:** Hiệu quả của cuộc tìm kiếm phụ thuộc rất nhiều vào chất lượng của logic đánh giá trạng thái.

## Phase 0: Foundation & Setup
Chúng ta sẽ cài đặt các thư viện và cấu hình các API keys như thường lệ.

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv
```

```python
import os
import re
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from collections import defaultdict

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
from rich.tree import Tree

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Tree-of-Thoughts (Nebius)"

# Kiểm tra các biến môi trường bắt buộc
required_vars = ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY"]
for var in required_vars:
    if var not in os.environ:
        print(f"Warning: Environment variable {var} not set.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Defining the Problem Environment
Một hệ thống Tree-of-Thoughts yêu cầu một môi trường được định nghĩa rõ ràng để hoạt động. Đối với câu đố Sói, Dê và Bắp cải, điều này có nghĩa là chúng ta cần định nghĩa bằng lập trình:

1.  **State Representation (Đại diện trạng thái):** Một cách để mô tả vị trí của tất cả các vật phẩm.
2.  **Validation Rules (Quy tắc thẩm định):** Một hàm để kiểm tra xem một trạng thái có không hợp lệ hay không (ví dụ: dê và bắp cải bị bỏ lại cùng nhau).
3.  **Goal State (Trạng thái mục tiêu):** Một cách để kiểm tra xem câu đố đã được giải xong chưa.
4.  **Possible Moves (Các bước đi khả thi):** Một hàm để xác định tất cả các bước đi hợp lệ từ một trạng thái cho trước.

```python
console = Console()

class PuzzleState(BaseModel):
    "Đại diện cho trạng thái của câu đố Sói, Dê và Bắp cải."
    # Sử dụng các set cho các tập hợp vật phẩm không có thứ tự trên mỗi bờ
    left_bank: set[str] = Field(default_factory=lambda: {"wolf", "goat", "cabbage"})
    right_bank: set[str] = Field(default_factory=set)
    boat_location: str = "left"
    move_description: str = "Initial state."

    def is_valid(self) -> bool:
        """Kiểm tra xem trạng thái hiện tại có hợp lệ không (không ai bị ăn thịt)."""
        # Kiểm tra bờ bên trái
        if self.boat_location == "right":
            if "wolf" in self.left_bank and "goat" in self.left_bank:
                return False
            if "goat" in self.left_bank and "cabbage" in self.left_bank:
                return False
        # Kiểm tra bờ bên phải
        if self.boat_location == "left":
            if "wolf" in self.right_bank and "goat" in self.right_bank:
                return False
            if "goat" in self.right_bank and "cabbage" in self.right_bank:
                return False
        return True

    def is_goal(self) -> bool:
        """Kiểm tra xem đã đạt đến trạng thái mục tiêu chưa."""
        return self.right_bank == {"wolf", "goat", "cabbage"}
    
    def __hash__(self):
        # Làm cho trạng thái có thể hash được để kiểm tra các trạng thái đã ghé thăm
        return hash((frozenset(self.left_bank), frozenset(self.right_bank), self.boat_location))
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

def get_possible_moves(state: PuzzleState) -> list[PuzzleState]:
    """Tạo ra tất cả các trạng thái tiếp theo hợp lệ khả thi từ trạng thái hiện tại."""
    moves = []
    current_bank = state.left_bank if state.boat_location == "left" else state.right_bank
    
    # Lựa chọn 1: Di chuyển một vật phẩm trong thuyền
    for item in current_bank:
        new_state = state.model_copy(deep=True)
        if state.boat_location == "left":
            new_state.left_bank.remove(item)
            new_state.right_bank.add(item)
            new_state.boat_location = "right"
            new_state.move_description = f"Move {item} to the right bank."
        else:
            new_state.right_bank.remove(item)
            new_state.left_bank.add(item)
            new_state.boat_location = "left"
            new_state.move_description = f"Move {item} to the left bank."
        if new_state.is_valid():
            moves.append(new_state)
            
    # Lựa chọn 2: Di chuyển thuyền trống
    empty_move_state = state.model_copy(deep=True)
    if state.boat_location == "left":
        empty_move_state.boat_location = "right"
        empty_move_state.move_description = "Move the boat empty to the right bank."
    else:
        empty_move_state.boat_location = "left"
        empty_move_state.move_description = "Move the boat empty to the left bank."
    if empty_move_state.is_valid():
        moves.append(empty_move_state)
        
    return moves

print("Puzzle environment defined successfully.")
```

## Phase 2: Implementing the ToT Agent with LangGraph
Bây giờ chúng ta sẽ xây dựng bản thân agent. State của graph sẽ theo dõi tất cả các con đường (các nhánh) đang hoạt động trong cây suy nghĩ của mình. Các node sẽ thực hiện các hành động ToT chính:

1.  **Expand Paths (Thought Generator):** Một node được hỗ trợ bởi LLM giúp xem xét trạng thái cuối cùng của mỗi con đường đang hoạt động và đề xuất một bước đi tiếp theo đầy hứa hẹn từ danh sách các khả năng hợp lệ.
2.  **Prune Paths (State Evaluator):** Node này dọn dẹp sau khi tạo. Nó sẽ loại bỏ bất kỳ con đường nào đã rơi vào trạng thái không hợp lệ hoặc bị lặp (ghé thăm lại một trạng thái trước đó).
3.  **Check for Solution (Goal Check):** Một node điều kiện giúp kiểm tra xem có con đường nào đang hoạt động đã đạt được trạng thái mục tiêu chưa. Nếu có, nó sẽ kết thúc vòng lặp.

```python
llm = ChatNebius(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0.4)

# Pydantic model cho lựa chọn bước đi của LLM
class MoveChoice(BaseModel):
    best_move_index: int = Field(description="The index of the best move from the provided list of possible moves.")
    reasoning: str = Field(description="Brief reasoning for why this is the most promising move.")

# LangGraph State
class ToTState(TypedDict):
    problem_description: str
    # Mỗi con đường là một danh sách các đối tượng PuzzleState
    active_paths: List[List[PuzzleState]]
    # Chúng ta sẽ lưu trữ giải pháp cuối cùng tại đây
    solution: Optional[List[PuzzleState]]

# Graph Nodes
def initialize_search(state: ToTState) -> Dict[str, Any]:
    """Node để thiết lập trạng thái ban đầu cho cuộc tìm kiếm."""
    initial_puzzle_state = PuzzleState()
    return {"active_paths": [[initial_puzzle_state]]}

def expand_paths(state: ToTState) -> Dict[str, Any]:
    """'Thought Generator'. Mở rộng mỗi con đường đang hoạt động bằng một bước đi tiếp theo hứa hẹn."""
    console.print("--- Expanding Paths ---")
    new_paths = []
    choice_llm = llm.with_structured_output(MoveChoice)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert logic puzzle solver. Your goal is to solve the Wolf, Goat, and Cabbage problem. Analyze the current path and choose the most promising next move from the list of options to reach the goal."),
        ("human", "Problem: {problem}\n\nCurrent Path History:\n{path_history}\n\nFrom the final state, choose the best next move from this list:\n{possible_moves}")
    ])
    
    for path in state['active_paths']:
        last_state = path[-1]
        possible_next_states = get_possible_moves(last_state)
        
        if not possible_next_states:
            continue # Con đường này đi vào ngõ cụt
            
        path_history_str = " -> ".join([s.move_description for s in path])
        possible_moves_str = "\n".join([f"{i}: {s.move_description}" for i, s in enumerate(possible_next_states)])
        
        # Để đơn giản và để hiển thị chiều rộng, chúng ta có thể khám phá nhiều bước đi.
        # Một ToT tiên tiến hơn có thể sử dụng LLM để chỉ chọn ra một cái tốt nhất duy nhất.
        # Ở đây, chúng ta sẽ để tất cả các bước đi hợp lệ rẽ nhánh ra để chứng minh cấu trúc cây.
        for next_state in possible_next_states:
            new_paths.append(path + [next_state])

    console.print(f"[cyan]Expanded to {len(new_paths)} potential paths.[/cyan]")
    return {"active_paths": new_paths}

def prune_paths(state: ToTState) -> Dict[str, Any]:
    """'State Evaluator'. Cắt tỉa các con đường không hợp lệ hoặc chứa các vòng lặp (cycles)."""
    console.print("--- Pruning Paths ---")
    pruned_paths = []
    for path in state['active_paths']:
        # Kiểm tra các vòng lặp: nếu trạng thái cuối cùng đã xuất hiện trước đó trong con đường này
        if path[-1] in path[:-1]:
            continue # Đã thấy vòng lặp, cắt tỉa con đường này
        
        # Hàm get_possible_moves đã đảm bảo tính hợp lệ rồi, nhưng đây là nơi tốt để thêm các kiểm tra phụ.
        pruned_paths.append(path)
        
    console.print(f"[green]Pruned down to {len(pruned_paths)} valid, non-cyclical paths.[/green]")
    return {"active_paths": pruned_paths}

# Conditional Node
def check_for_solution(state: ToTState) -> str:
    """Kiểm tra xem có con đường nào đã đạt được mục tiêu chưa và điều hướng thực thi."""
    for path in state['active_paths']:
        if path[-1].is_goal():
            console.print("[bold green]Solution Found![/bold green]")
            # Side effect: cập nhật giải pháp trong state. LangGraph sẽ copy nó ra.
            state['solution'] = path
            return "solution_found"
    return "continue_search"

# Xây dựng graph
workflow = StateGraph(ToTState)

workflow.add_node("initialize", initialize_search)
workflow.add_node("expand", expand_paths)
workflow.add_node("prune", prune_paths)

workflow.set_entry_point("initialize")
workflow.add_edge("initialize", "expand")
workflow.add_edge("expand", "prune")

workflow.add_conditional_edges(
    "prune",
    check_for_solution,
    {
        "solution_found": END,
        "continue_search": "expand"
    }
)

tot_agent = workflow.compile()
print("Tree-of-Thoughts agent graph compiled successfully.")
```

## Phase 3: Demonstration & Analysis
Bây giờ, hãy chạy ToT agent của chúng ta cho câu đố. Chúng ta sẽ so sánh cách tiếp cận có hệ thống của nó với một yêu cầu Chain-of-Thought đơn lẻ, chạy một lượt (single-pass) để làm nổi bật sự khác biệt về tính ổn định.

```python
problem = "A farmer wants to cross a river with a wolf, a goat, and a cabbage. The boat can only carry the farmer and one other item. The farmer cannot leave the wolf alone with the goat, nor the goat alone with the cabbage. How can the farmer get everyone across safely?"

console.print("--- 🌳 Running Tree-of-Thoughts Agent ---")
# Giới hạn đệ quy ngăn chặn các vòng lặp vô hạn trong graph của chúng ta
config = {"recursion_limit": 15}
final_state = tot_agent.invoke({"problem_description": problem}, config=config)

console.print("\n--- ✅ ToT Agent Solution ---")
if final_state.get('solution'):
    solution_path = final_state['solution']
    # Sử dụng rich.Tree cho đầu ra trực quan đẹp mắt
    tree = Tree("[bold magenta]Wolf, Goat, and Cabbage Solution Path[/bold magenta]")
    for i, state in enumerate(solution_path):
        tree.add(f"[green]{i+1}.[/green] {state.move_description}")
    console.print(tree)
else:
    console.print("[bold red]No solution found within the step limit.[/bold red]")

console.print("\n--- 🤔 Running Simple Chain-of-Thought Agent ---")
cot_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world-class logic puzzle solver. Provide a step-by-step solution to the user's puzzle."),
    ("human", "{problem}")
])
cot_chain = cot_prompt | llm
cot_result = cot_chain.invoke({"problem": problem}).content
console.print(Markdown(cot_result))
```

### Analysis of the Results
Sự khác biệt giữa hai phương pháp là rất sâu sắc:

- **Chain-of-Thought (CoT):** Cách tiếp cận này dựa trên kiến thức đã được huấn luyện trước của LLM để nhớ lại giải pháp. Đối với một vấn đề cổ điển, nổi tiếng như thế này, một LLM mạnh mẽ thường có thể đưa ra câu trả lời đúng ngay trong một lượt. Tuy nhiên, nếu nó mắc một lỗi duy nhất, nó không có cơ chế để tự sửa chữa. Đối với một vấn đề mới lạ hoặc phức tạp hơn, khả năng thất bại cao hơn nhiều. Tính đúng đắn của nó là vấn đề của việc ghi nhớ, không phải là lập luận có thể xác minh.

- **Tree-of-Thoughts (ToT):** Agent này *khám phá ra* giải pháp thông qua cuộc tìm kiếm có hệ thống, có thể xác minh. Nó không chỉ nhớ lại một câu trả lời; nó xây dựng một cái. Chúng ta có thể thấy quy trình trong nhật ký: mở rộng các con đường, sau đó cắt tỉa những con đường rơi vào ngõ cụt hoặc vòng lặp. Ngay cả khi LLM hướng dẫn việc mở rộng đưa ra một lựa chọn không tối ưu trên một nhánh, agent vẫn có thể tiếp tục khám phá các nhánh khác đầy hứa hẹn hơn. Phương pháp này ổn định và đáng tin cậy hơn nhiều vì giải pháp cuối cùng của nó được đảm bảo là hợp lệ theo các quy tắc của môi trường mà chúng ta đã định nghĩa.

Thành công của ToT agent không dựa trên sự may mắn hay việc học thuộc lòng, mà dựa trên sự vững chãi của thuật toán tìm kiếm của nó. Điều này khiến nó trở thành một cách tiếp cận vượt trội hơn hẳn cho các nhiệm vụ đòi hỏi độ tin cậy và lập kế hoạch cao.

## Conclusion
Trong notebook này, chúng ta đã triển khai một **Tree-of-Thoughts** agent để giải một câu đố logic cổ điển. Chúng ta đã chứng minh rằng bằng cách chuyển đổi một vấn đề thành một không gian trạng thái (state space) và tìm kiếm qua đó một cách có hệ thống, một agent có thể đạt được mức độ ổn định và chính xác mà các phương pháp lập luận đơn giản, chạy một lượt không thể làm được.

Các thành phần cốt lõi của ToT—**tạo suy nghĩ (thought generation - expansion)**, **đánh giá trạng thái (state evaluation - pruning)**, và **tìm kiếm (search)**—tạo ra một framework mạnh mẽ để giải quyết các nhiệm vụ lập kế hoạch và lập luận phức tạp. Mặc dù nó đi kèm với chi phí tính toán cao hơn, nhưng sự đánh đổi lại là sự gia tăng đáng kể về tính tin cậy và khả năng giải quyết vấn đề. Kiến trúc này là một bước đi then chốt hướng tới việc xây dựng các agent có thể lập luận một cách chủ động (reason deliberately) và tìm ra giải pháp cho các vấn đề đa bước, đầy thách thức.
