# 📘 Agentic Architectures 16: Cellular Automata / Grid-Based Systems

Chào mừng bạn đến với bài khám phá một kiến trúc agentic hoàn toàn khác biệt: **Cellular Automata** (Tế bào tự động) và **Grid-Based Agent Systems** (Hệ thống Agent dựa trên lưới). Pattern này được truyền cảm hứng từ các hệ thống phức tạp trong tự nhiên và các khái niệm như Trò chơi Cuộc sống (Game of Life) của Conway. Nó chuyển đổi paradigm từ một vài agent phức tạp, tập trung sang một số lượng lớn các agent đơn giản, phi tập trung hoạt động trên một lưới (grid).

Trong mô hình này, chính môi trường trở thành agent. Mỗi ô (cell) trong một lưới là một mini-agent với trạng thái riêng và một bộ quy tắc đơn giản để cập nhật trạng thái đó dựa trên các láng giềng (neighbors) trực tiếp của nó. Không có bộ điều khiển trung tâm hay thuật toán tìm đường (pathfinding) phức tạp. Thay vào đó, hành vi thông minh mang tính toàn cục **nảy sinh** (emerge) từ việc áp dụng đồng bộ, lặp đi lặp lại các quy tắc cục bộ đơn giản này. Hệ thống trở thành một "computational fabric" (mạng lưới tính toán) giải quyết các vấn đề thông qua sự lan truyền thông tin dạng sóng.

Để chứng minh điều này trong một triển khai chi tiết và phức tạp, chúng ta sẽ xây dựng một **Warehouse Logistics Simulator** (Giả lập Logicstic kho hàng). Mục tiêu của chúng ta là hoàn thành một đơn hàng bằng cách di chuyển các mặt hàng từ kệ đến trạm đóng gói. Chúng ta sẽ giải quyết nhiệm vụ lập luận không gian phức tạp này không phải bằng một agent "robot" duy nhất, mà bằng cách lập trình chính các ô lưới để chúng cùng nhau tính toán con đường tối ưu.

### Definition
Một **Grid-Based Agent System** là một kiến trúc nơi một số lượng lớn các agent đơn giản (hoặc các "ô") được sắp xếp trong một lưới không gian. Mỗi agent có một trạng thái và cập nhật nó một cách đồng bộ dựa trên một bộ quy tắc chỉ xem xét trạng thái của các láng giềng trực tiếp. Các pattern cấp cao phức tạp và khả năng giải quyết vấn đề nảy sinh từ những tương tác cục bộ này.

### High-level Workflow
1.  **Grid Initialization (Khởi tạo lưới):** Một lưới gồm các cell-agent được tạo ra, mỗi cell được khởi tạo với một loại (ví dụ: vật cản, trống) và một trạng thái (ví dụ: một giá trị).
2.  **Set Boundary Conditions (Thiết lập điều kiện biên):** Một hoặc nhiều ô được cấp một trạng thái đặc biệt để bắt đầu tính toán (ví dụ: giá trị của ô "mục tiêu" được đặt thành 0).
3.  **Synchronous Tick (Nhịp đồng bộ):** Hệ thống "tích tắc" (tick) tiến về phía trước. Trong mỗi nhịp, mọi ô đồng thời tính toán trạng thái tiếp theo của nó dựa trên trạng thái hiện tại của các láng giềng của nó.
4.  **Emergence (Sự nảy sinh):** Khi hệ thống tích tắc, thông tin lan truyền khắp lưới giống như một làn sóng. Điều này có thể tạo ra các độ dốc (gradients), các con đường và các cấu trúc phức tạp khác.
5.  **State Stabilization (Ổn định trạng thái):** Hệ thống chạy cho đến khi trạng thái lưới ổn định (không còn thay đổi nào xảy ra), cho thấy quá trình tính toán đã hoàn tất.
6.  **Readout (Đọc kết quả):** Giải pháp cho vấn đề sau đó được đọc trực tiếp từ trạng thái cuối cùng của lưới (ví dụ: bằng cách đi theo một độ dốc đã được tính toán).

### When to Use / Applications
*   **Lập luận không gian & Logistics:** Tìm đường tối ưu trong môi trường năng động (giống như ví dụ kho hàng của chúng ta).
*   **Giả lập hệ thống phức tạp:** Mô hình hóa các hiện tượng có hành vi nảy sinh như cháy rừng, sự lây lan của dịch bệnh hoặc sự phát triển đô thị.
*   **Tính toán song song:** Một số thuật toán có thể được ánh xạ vào mô hình cellular automata để thực thi trên phần cứng song song cao (như GPU).

### Strengths & Weaknesses
*   **Strengths:**
    *   **Tính song song cao:** Logic vốn dĩ là song song, làm cho nó cực kỳ nhanh trên phần cứng thích hợp.
    *   **Khả năng thích ứng:** Hệ thống có thể phản ứng linh hoạt với những thay đổi trong môi trường (ví dụ: một vật cản mới) bằng cách đơn giản là lan truyền lại các làn sóng của nó.
    *   **Sự phức tạp nảy sinh:** Có thể giải quyết các vấn đề rất phức tạp với các quy tắc cực kỳ đơn giản.
*   **Weaknesses:**
    *   **Độ phức tạp trong thiết kế:** Thiết kế các quy tắc cục bộ để tạo ra hành vi toàn cục mong muốn có thể đầy thử thách và không mang tính trực quan.
    *   **Kém tính nội soi:** Khó có thể hỏi một ô duy nhất "tại sao" nó có một trạng thái nhất định; việc lập luận được phân phối trên toàn bộ hệ thống.

## Phase 0: Foundation & Setup
Chúng ta cần `numpy` cho các thao tác lưới hiệu quả và `rich` cho các hiển thị đầu cuối chất lượng cao.

```python
# !pip install -q -U langchain-nebius rich python-dotenv numpy
```

```python
import os
import numpy as np
import time
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from IPython.display import clear_output

# LangChain for optional final summary
from langchain_nebius import ChatNebius
from langchain_core.prompts import ChatPromptTemplate

# For pretty printing and visualization
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Cellular Automata (Nebius)"

required_vars = ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY"]
for var in required_vars:
    if var not in os.environ:
        print(f"Warning: Environment variable {var} not set.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Building the Cellular Automata Environment
Đây là giai đoạn quan trọng nhất. Chúng ta sẽ định nghĩa hai class cốt lõi cho phần giả lập của mình:
1.  `CellAgent`: Đại diện cho một ô duy nhất trong lưới. Nó chứa loại của nó (type), trạng thái của nó (một giá trị tìm đường), và quy tắc cục bộ để cập nhật trạng thái đó.
2.  `WarehouseGrid`: Container cho toàn bộ hệ thống. Nó sẽ quản lý mảng 2D gồm các `CellAgent`, điều phối các cập nhật đồng bộ `tick` và xử lý việc hiển thị.

```python
console = Console()

class CellAgent:
    """Một agent duy nhất trong lưới của chúng ta. Công việc duy nhất của nó là cập nhật giá trị của mình dựa trên các láng giềng."""
    def __init__(self, cell_type: str, item: Optional[str] = None):
        self.type = cell_type # 'EMPTY', 'OBSTACLE', 'SHELF', 'PACKING_STATION'
        self.item = item
        self.pathfinding_value = float('inf')

    def update_value(self, neighbors: List['CellAgent']):
        """Quy tắc cục bộ cốt lõi: giá trị mới của tôi là 1 + giá trị tối thiểu của các láng giềng không phải vật cản."""
        if self.type == 'OBSTACLE':
            return float('inf')
        
        min_neighbor_value = float('inf')
        for neighbor in neighbors:
            if neighbor.pathfinding_value < min_neighbor_value:
                min_neighbor_value = neighbor.pathfinding_value
        
        # +1 đại diện cho chi phí di chuyển từ một láng giềng đến ô này
        return min(self.pathfinding_value, min_neighbor_value + 1)

class WarehouseGrid:
    """Quản lý toàn bộ lưới các CellAgents và vòng lặp giả lập."""
    def __init__(self, layout: List[str]):
        self.height = len(layout)
        self.width = len(layout[0])
        self.grid = self._create_grid_from_layout(layout)
        self.item_locations = self._get_item_locations()

    def _create_grid_from_layout(self, layout):
        grid = np.empty((self.height, self.width), dtype=object)
        for r, row_str in enumerate(layout):
            for c, char in enumerate(row_str):
                if char == ' ':
                    grid[r, c] = CellAgent('EMPTY')
                elif char == '#':
                    grid[r, c] = CellAgent('OBSTACLE')
                elif char == 'P':
                    grid[r, c] = CellAgent('PACKING_STATION')
                else: # Đó là một mặt hàng
                    grid[r, c] = CellAgent('SHELF', item=char)
        return grid

    def _get_item_locations(self) -> Dict[str, Tuple[int, int]]:
        locations = {}
        for r in range(self.height):
            for c in range(self.width):
                if self.grid[r, c].type == 'SHELF':
                    locations[self.grid[r, c].item] = (r, c)
                if self.grid[r, c].type == 'PACKING_STATION':
                    locations['P'] = (r, c)
        return locations

    def get_neighbors(self, r: int, c: int) -> List[CellAgent]:
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # N, S, E, W
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.height and 0 <= nc < self.width:
                neighbors.append(self.grid[nr, nc])
        return neighbors

    def tick(self) -> bool:
        """Thực hiện một bản cập nhật đồng bộ của tất cả các ô. Trả về True nếu có bất kỳ giá trị nào thay đổi."""
        changed = False
        # Đầu tiên, tính toán tất cả các giá trị mới dựa trên trạng thái hiện tại
        new_values = np.empty((self.height, self.width))
        for r in range(self.height):
            for c in range(self.width):
                neighbors = self.get_neighbors(r, c)
                new_values[r, c] = self.grid[r, c].update_value(neighbors)
        
        # Sau đó, áp dụng tất cả các giá trị mới
        for r in range(self.height):
            for c in range(self.width):
                if self.grid[r, c].pathfinding_value != new_values[r, c]:
                    self.grid[r, c].pathfinding_value = new_values[r, c]
                    changed = True
        return changed

    def visualize(self, show_values: bool = False, title: str = "Warehouse Grid"):
        """Hiển thị trạng thái lưới bằng Rich."""
        table = Table(title=title, show_header=False, show_edge=True, padding=0)
        for _ in range(self.width):
            table.add_column(justify="center")
        
        for r in range(self.height):
            row_renderables = []
            for c in range(self.width):
                cell = self.grid[r, c]
                val = cell.pathfinding_value
                display_char = ''
                if cell.type == 'EMPTY': display_char = '[grey70]·[/grey70]'
                elif cell.type == 'OBSTACLE': display_char = '[red]█[/red]'
                elif cell.type == 'PACKING_STATION': display_char = '[bold green]P[/bold green]'
                elif cell.type == 'SHELF': display_char = f'[bold blue]{cell.item}[/bold blue]'

                if show_values and val != float('inf'):
                    # Mã hóa màu cho các giá trị đường đi
                    color = int(255 - (val * 5) % 255)
                    row_renderables.append(f"[rgb({color},{color},{color}) on rgb(30,30,60)]{int(val):^3}[/]")
                else:
                    row_renderables.append(f" {display_char} ")
            table.add_row(*row_renderables)
        console.print(table)

print("Cellular Automata environment defined successfully.")
```

## Phase 2: Implementing the Emergent Behaviors
Bản thân lưới chỉ là một framework. Chúng ta cần triển khai logic cấp cao sử dụng cellular automata để giải quyết vấn đề của mình. Điều này bao gồm hai hành vi nảy sinh chính:

1.  **Path Wave Propagation (Lan truyền sóng đường đi):** Một hàm thiết lập mục tiêu và để lưới `tick` cho đến khi một độ dốc tìm đường hoàn chỉnh được hình thành trên toàn bộ sàn kho.
2.  **Gradient Descent Traversal (Duyệt theo độ dốc giảm dần):** Một hàm mô phỏng một agent "người vận chuyển" bắt đầu tại kệ của mặt hàng và đơn giản là đi theo con đường dốc nhất (giá trị `pathfinding_value` thấp nhất) cho đến khi đạt được mục tiêu.

```python
def propagate_path_wave(grid: WarehouseGrid, target_pos: Tuple[int, int], visualize_steps: bool = False):
    """Đặt lại và sau đó chạy giả lập cho đến khi các giá trị tìm đường ổn định."""
    # Đặt lại tất cả các giá trị tìm đường
    for r in range(grid.height):
        for c in range(grid.width):
            grid.grid[r, c].pathfinding_value = float('inf')
            
    # Đặt giá trị của mục tiêu là 0 để bắt đầu làn sóng
    grid.grid[target_pos].pathfinding_value = 0
    
    tick_count = 0
    while True:
        tick_count += 1
        if visualize_steps:
            clear_output(wait=True)
            grid.visualize(show_values=True, title=f"Path Wave Propagation (Tick #{tick_count})")
            time.sleep(0.1)
        
        changed = grid.tick()
        if not changed:
            break
    if visualize_steps:
        clear_output(wait=True)
        grid.visualize(show_values=True, title=f"Path Wave Propagation (Stabilized at Tick #{tick_count})")

def trace_and_move_item(grid: WarehouseGrid, start_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Đi theo độ dốc từ vị trí bắt đầu ngược về mục tiêu (giá trị 0)."""
    path = [start_pos]
    r, c = start_pos
    
    while grid.grid[r, c].pathfinding_value > 0:
        neighbors = grid.get_neighbors(r, c)
        best_neighbor_pos = None
        min_val = grid.grid[r, c].pathfinding_value
        
        # Tìm láng giềng có giá trị tìm đường thấp nhất
        for neighbor_cell in neighbors:
            # Tìm vị trí của ô láng giềng
            pos_list = np.where(grid.grid == neighbor_cell)
            if len(pos_list[0]) > 0:
                nr, nc = pos_list[0][0], pos_list[1][0]
                if neighbor_cell.pathfinding_value < min_val:
                    min_val = neighbor_cell.pathfinding_value
                    best_neighbor_pos = (nr, nc)
        
        if best_neighbor_pos:
            path.append(best_neighbor_pos)
            r, c = best_neighbor_pos
        else:
            console.print("[red]Error: Path tracing got stuck. No downhill neighbor found.[/red]")
            break
            
    return path

print("Emergent behavior functions defined successfully.")
```

## Phase 3: The Full Orchestration Workflow
Bây giờ chúng ta sẽ tạo hàm cấp cao nhất để mô phỏng toàn bộ quy trình hoàn thành đơn hàng. Điều này sẽ chứng minh cách các hành vi nảy sinh có thể được kết hợp để giải quyết một vấn đề nhiều bước.

```python
def fulfill_order(layout: List[str], order: List[str], visualize_waves: bool = False):
    """Hàm điều phối chính."""
    grid = WarehouseGrid(layout)
    console.print("--- Initial Warehouse State ---")
    grid.visualize()
    
    packing_station_pos = grid.item_locations['P']
    
    for i, item_id in enumerate(order):
        panel_title = f"[bold]Step {i+1}: Fulfill Item '{item_id}'[/bold]"
        log_messages = []
        
        item_pos = grid.item_locations.get(item_id)
        if not item_pos:
            console.print(Panel(f"[red]Error: Item '{item_id}' not found in warehouse.[/red]", title=panel_title))
            continue
            
        # 1. Tính toán sóng đường đi từ trạm đóng gói
        log_messages.append("🌊 Computing path wave from Packing Station...")
        propagate_path_wave(grid, packing_station_pos, visualize_steps=visualize_waves)
        
        # 2. Truy vết con đường cho mặt hàng hiện tại
        log_messages.append(f"🚚 Found path for item {item_id}. Moving along gradient...")
        path = trace_and_move_item(grid, item_pos)
        path_str = ' -> '.join(map(str, path))
        log_messages.append(f"Path: {path_str}")

        # 3. Cập nhật trạng thái lưới (mặt hàng hiện đã ở trạm đóng gói)
        grid.grid[item_pos].type = 'EMPTY'
        grid.grid[item_pos].item = None
        log_messages.append(f"✅ Item '{item_id}' has been moved to the packing station.")
        console.print(Panel('\n'.join(log_messages), title=panel_title, border_style="blue"))
        
    console.print(Panel(f"The system successfully fulfilled the order for items {order} by emergently computing paths through local cell interactions.", title="[bold green]🎉 Order Fulfillment Complete![/bold green]", border_style="green"))
    return grid

# --- Main Execution ---
warehouse_layout = [
    "#######",
    "# D   #",
    "# ### #",
    "#A#C# #",
    "# # #B#",
    "#  P  #",
    "#######",
]
order_to_fulfill = ['A', 'B']
final_grid = fulfill_order(warehouse_layout, order_to_fulfill, visualize_waves=True)

# --- Tùy chọn: LLM Interpretation ---
console.print("\n--- 🤖 LLM Interpretation of the Final State ---")
llm = ChatNebius(model="mistralai/Mixtral-8x22B-Instruct-v0.1")
summary_prompt = ChatPromptTemplate.from_template("You are a logistics manager. Briefly summarize the outcome of the following order fulfillment report.\n\nOrder: {order}\nFinal Warehouse State: All items from the order have been moved to the packing station. Items A and B were retrieved. Original locations were {loc_A} and {loc_B}. The floor is now clear.")
summary_chain = summary_prompt | llm
final_summary = summary_chain.invoke({
    "order": order_to_fulfill, 
    "loc_A": WarehouseGrid(warehouse_layout).item_locations['A'],
    "loc_B": WarehouseGrid(warehouse_layout).item_locations['B']
}).content
console.print(Markdown(final_summary))
```

### Analysis of the Results
Triển khai chi tiết này thể hiện hoàn hảo bản chất độc đáo của Cellular Automata trong việc giải quyết vấn đề:

1.  **Không có người lập kế hoạch trung tâm:** Chúng ta không sử dụng thuật toán tìm đường toàn cục như A* vào bất kỳ lúc nào. Chúng ta chưa bao giờ tính toán đường đi theo cách từ trên xuống (top-down). Con đường tối ưu là một *đặc tính nảy sinh* của chính lưới đó.

2.  **Thông tin dưới dạng Sóng:** Hàm `propagate_path_wave` là chìa khóa. Phần hình ảnh cho thấy 'khoảng cách' từ trạm đóng gói lan tỏa khắp các ô lưới qua từng nhịp tích tắc, uốn lượn quanh các vật cản một cách tự nhiên. Đây chính là "mạng lưới tính toán" đang vận hành. Lưới thực chất đã tính toán đường ngắn nhất từ *mọi ô trống* đến trạm đóng gói cùng một lúc.

3.  **Agent đơn giản, Hành vi phức tạp:** "Người vận chuyển" di chuyển mặt hàng cực kỳ đơn giản. Logic duy nhất của nó là "tìm láng giềng nào có con số thấp nhất và di chuyển đến đó." Tất cả các lập luận phức tạp về môi trường đã được mã hóa vào trạng thái của lưới bằng sóng đường đi.

4.  **Khả năng thích ứng:** Nếu chúng ta thay đổi bố cục nhà kho bằng cách thêm một vật cản mới, chúng ta sẽ không cần viết lại một thuật toán tìm đường phức tạp. Chúng ta chỉ đơn giản là chạy lại quá trình lan truyền sóng, và các giá trị đường đi sẽ tự động và chính xác uốn quanh vật cản mới, minh chứng cho khả năng thích ứng vốn có của hệ thống.

Đây là một sự chuyển dịch cơ bản so với thiết kế agent truyền thống. Thay vì xây dựng một agent thông minh điều hướng trong một môi trường thụ động, chúng ta xây dựng một môi trường thông minh bao gồm nhiều agent đơn giản, cùng nhau giải quyết vấn đề.

## Conclusion
Trong notebook này, chúng ta đã xây dựng một **Cellular Automata / Grid-Based Agent System** hoàn chỉnh. Chúng ta đã đi xa hơn lý thuyết và triển khai một giải pháp thực tế cho một vấn đề lập luận không gian phức tạp: logistics kho hàng.

Chúng ta đã tận mắt chứng kiến hành vi phức tạp, định hướng mục tiêu có thể nảy sinh như thế nào từ việc thực thi đồng bộ các quy tắc cục bộ đơn giản trên một lưới các mini-agent. Các khái niệm về **lan truyền sóng** và **gradient descent** không được lập trình rõ ràng theo cách từ trên xuống mà là kết quả tự nhiên từ sự tiến hóa của cellular automata.

Kiến trúc này, mặc dù không phù hợp cho mọi vấn đề, nhưng cực kỳ mạnh mẽ cho các nhiệm vụ liên quan đến lập luận không gian, giả lập và tối ưu hóa trong môi trường năng động. Nó khuyến khích chúng ta nghĩ về các hệ thống agentic ít hơn như những "con bot" riêng lẻ và nhiều hơn như một **môi trường tính toán có thể lập trình**, có thể cấu hình để giải quyết các vấn đề theo cách song song hóa và thích ứng cao.
