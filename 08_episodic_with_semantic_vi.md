# 📘 Agentic Architectures 8: Episodic + Semantic Memory Stack

Chào mừng bạn đến với notebook thứ tám trong loạt bài của chúng ta. Hôm nay, chúng ta sẽ giải quyết một trong những thách thức quan trọng nhất trong việc tạo ra các trợ lý thông minh thực thụ, dài hạn: **bộ nhớ bền vững (persistent memory)**. Bộ nhớ chatbot tiêu chuẩn có tính chất tạm thời (ephemeral), chỉ tồn tại trong một phiên làm việc duy nhất. Để xây dựng một agent cá nhân hóa có khả năng học hỏi và phát triển cùng người dùng, chúng ta cần một giải pháp mạnh mẽ hơn.

Chúng ta sẽ triển khai một kiến trúc bộ nhớ có cấu trúc mô phỏng nhận thức của con người, kết hợp hai loại bộ nhớ riêng biệt:

1.  **Episodic Memory (Bộ nhớ tình tiết):** Đây là bộ nhớ về các sự kiện cụ thể hoặc các tương tác trong quá khứ. Nó trả lời cho câu hỏi "Điều gì đã xảy ra?" (ví dụ: "Tuần trước, người dùng đã hỏi tôi về giá cổ phiếu của NVIDIA."). Chúng ta sẽ sử dụng một **vector database** cho việc này để tìm các cuộc hội thoại trong quá khứ có liên quan đến chủ đề hiện tại.
2.  **Semantic Memory (Bộ nhớ ngữ nghĩa):** Đây là bộ nhớ về các sự kiện có cấu trúc, khái niệm và mối quan hệ được trích xuất từ các sự kiện đó. Nó trả lời cho câu hỏi "Tôi biết những gì?" (ví dụ: "Người dùng Alex là một nhà đầu tư thận trọng.", "Alex quan tâm đến Cổ phiếu Công nghệ."). Chúng ta sẽ sử dụng một **graph database (Neo4j)** cho việc này, vì nó xuất sắc trong việc quản lý và truy vấn các mối quan hệ phức tạp.

Bằng cách kết hợp hai loại bộ nhớ này, agent của chúng ta không chỉ có thể nhớ lại các cuộc hội thoại trong quá khứ mà còn xây dựng được một cơ sở tri thức phong phú, liên kết chặt chẽ về người dùng và thế giới, dẫn đến các tương tác mang tính cá nhân hóa sâu sắc và nhận thức ngữ cảnh tốt.

### Definition
Một **Episodic + Semantic Memory Stack** là một kiến trúc agent duy trì hai loại bộ nhớ dài hạn. **Episodic memory** lưu trữ nhật ký trình tự thời gian của các trải nghiệm (ví dụ: các bản tóm tắt lịch sử chat) và thường được tìm kiếm dựa trên sự tương đương về ngữ nghĩa (semantic similarity). **Semantic memory** lưu trữ kiến thức có cấu trúc, đã được trích xuất (sự thật, thực thể, mối quan hệ) trong một cơ sở tri thức, thường là một đồ thị (graph).

### High-level Workflow
1.  **Interaction:** Agent thực hiện hội thoại với người dùng.
2.  **Memory Retrieval (Recall):** Đối với một truy vấn mới của người dùng, trước tiên agent sẽ truy vấn cả hai hệ thống bộ nhớ.
3.  **Augmented Generation:** Các bộ nhớ được truy xuất sẽ được thêm vào context của prompt, cho phép LLM tạo ra phản hồi có nhận thức về các tương tác trong quá khứ và các sự thật đã học được.
4.  **Memory Creation (Encoding):** Sau khi tương tác hoàn tất, một quy trình ngầm sẽ phân tích cuộc hội thoại.
    *   Nó tạo ra một bản tóm tắt ngắn gọn về lượt hội thoại (đó là **episodic** memory mới).
    *   Nó trích xuất các thực thể và mối quan hệ chính (đó là **semantic** memory mới).
5.  **Memory Storage:** Bản tóm tắt episodic mới được nhúng (embedded) và lưu vào vector store. Các sự thật semantic mới được ghi dưới dạng các node và edge trong graph database.

### When to Use / Applications
*   **Trợ lý cá nhân dài hạn:** Một trợ lý ghi nhớ các sở thích, dự án và thông tin cá nhân của bạn qua nhiều tuần hoặc nhiều tháng.
*   **Hệ thống cá nhân hóa:** Bot thương mại điện tử ghi nhớ phong cách của bạn, hoặc gia sư giáo dục ghi nhớ tiến trình học tập và các lỗ hổng kiến thức của bạn.
*   **Agent nghiên cứu phức tạp:** Một agent xây dựng một knowledge graph về một chủ đề khi nó khám phá các tài liệu, cho phép nó trả lời các câu hỏi phức tạp, đa bước (multi-hop).

### Strengths & Weaknesses
*   **Strengths:**
    *   **Cá nhân hóa thực sự:** Cho phép duy trì context và việc học tập kéo dài vô hạn, vượt xa cửa sổ ngữ cảnh (context window) của một phiên làm việc duy nhất.
    *   **Sự hiểu biết phong phú:** Graph database cho phép agent hiểu và suy luận về các mối quan hệ phức tạp giữa các thực thể.
*   **Weaknesses:**
    *   **Độ phức tạp:** Đây là một kiến trúc phức tạp hơn đáng kể để xây dựng và bảo trì so với một stateless agent đơn giản.
    *   **Sự phình to của bộ nhớ & Cắt tỉa (Pruning):** Theo thời gian, các kho lưu trữ bộ nhớ có thể trở nên khổng lồ. Các chiến lược tóm tắt, hợp nhất hoặc cắt tỉa các bộ nhớ cũ/không liên quan là rất thiết yếu cho hiệu năng dài hạn.

## Phase 0: Foundation & Setup
Chúng ta sẽ cài đặt tất cả các thư viện cần thiết, bao gồm driver cho các vector và graph databases, đồng thời cấu hình các API keys của mình.

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv langchain_community langchain-openai neo4j faiss-cpu tiktoken
```

```python
import os
import uuid
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

# Pydantic for data modeling
from pydantic import BaseModel, Field

# LangChain components
from langchain_nebius import ChatNebius, NebiusEmbeddings
from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_core.prompts import ChatPromptTemplate

# LangGraph components
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

# For pretty printing
from rich.console import Console
from rich.markdown import Markdown

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Memory Stack (Nebius)"

# Kiểm tra các biến môi trường bắt buộc
required_vars = ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD"]
for var in required_vars:
    if var not in os.environ:
        print(f"Warning: Environment variable {var} not set.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Building the Memory Components
Đây là cốt lõi trong kiến trúc của chúng ta. Chúng ta sẽ định nghĩa các cấu trúc cho bộ nhớ và thiết lập kết nối tới các database. Chúng ta cũng sẽ tạo agent "Memory Maker" chịu trách nhiệm xử lý các cuộc hội thoại và tạo ra các bộ nhớ mới.

```python
console = Console()
llm = ChatNebius(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0)
embeddings = NebiusEmbeddings()

# --- 1. Vector Store cho Episodic Memory ---
# Trong một ứng dụng thực tế, bạn sẽ cần lưu trữ lâu dài cái này. Trong ví dụ này, nó nằm trong bộ nhớ (in-memory).
try:
    episodic_vector_store = FAISS.from_texts(["Initial document to bootstrap the store"], embeddings)
except ImportError:
    console.print("[bold red]FAISS not installed. Please run `pip install faiss-cpu`.[/bold red]")
    episodic_vector_store = None

# --- 2. Graph DB cho Semantic Memory ---
try:
    graph = Neo4jGraph(
        url=os.environ.get("NEO4J_URI"),
        username=os.environ.get("NEO4J_USERNAME"),
        password=os.environ.get("NEO4J_PASSWORD")
    )
    # Xóa graph để bắt đầu một lượt chạy sạch
    graph.query("MATCH (n) DETACH DELETE n")
except Exception as e:
    console.print(f"[bold red]Failed to connect to Neo4j: {e}. Please check your credentials and connection.[/bold red]")
    graph = None

# --- 3. Pydantic Models cho \"Memory Maker\" ---
# Định nghĩa cấu trúc kiến thức chúng ta muốn trích xuất.
class Node(BaseModel):
    id: str = Field(description="Unique identifier for the node, which can be a person's name, a company ticker, or a concept.")
    type: str = Field(description="The type of the node (e.g., 'User', 'Company', 'InvestmentPhilosophy').")
    properties: Dict[str, Any] = Field(description="A dictionary of properties for the node.")

class Relationship(BaseModel):
    source: Node = Field(description="The source node of the relationship.")
    target: Node = Field(description="The target node of the relationship.")
    type: str = Field(description="The type of the relationship (e.g., 'IS_A', 'INTERESTED_IN').")
    properties: Dict[str, Any] = Field(description="A dictionary of properties for the relationship.")

class KnowledgeGraph(BaseModel):
    """Đại diện cho kiến thức có cấu trúc được trích xuất từ một cuộc hội thoại."""
    relationships: List[Relationship] = Field(description="A list of relationships to be added to the knowledge graph.")

# --- 4. The \"Memory Maker\" Agent ---
def create_memories(user_input: str, assistant_output: str):
    conversation = f"User: {user_input}\nAssistant: {assistant_output}"
    
    # 4a. Tạo Episodic Memory (Tóm tắt)
    console.print("--- Creating Episodic Memory (Summary) ---")
    summary_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a summarization expert. Create a concise, one-sentence summary of the following user-assistant interaction. This summary will be used as a memory for future recall."),
        ("human", "Interaction:\n{interaction}")
    ])
    summarizer = summary_prompt | llm
    episodic_summary = summarizer.invoke({"interaction": conversation}).content
    
    new_doc = Document(page_content=episodic_summary, metadata={"created_at": uuid.uuid4().hex})
    episodic_vector_store.add_documents([new_doc])
    console.print(f"[green]Episodic memory created:[/green] '{episodic_summary}'")
    
    # 4b. Tạo Semantic Memory (Trích xuất sự thật)
    console.print("--- Creating Semantic Memory (Graph) ---")
    extraction_llm = llm.with_structured_output(KnowledgeGraph)
    extraction_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a knowledge extraction expert. Your task is to identify key entities and their relationships from a conversation and model them as a graph. Focus on user preferences, goals, and stated facts."),
        ("human", "Extract all relationships from this interaction:\n{interaction}")
    ])
    extractor = extraction_prompt | extraction_llm
    try:
        kg_data = extractor.invoke({"interaction": conversation})
        if kg_data.relationships:
            for rel in kg_data.relationships:
                graph.add_graph_documents([rel], include_source=True)
            console.print(f"[green]Semantic memory created:[/green] Added {len(kg_data.relationships)} relationships to the graph.")
        else:
            console.print("[yellow]No new semantic memories identified in this interaction.[/yellow]")
    except Exception as e:
        console.print(f"[red]Could not extract or save semantic memory: {e}[/red]")

if episodic_vector_store and graph:
    print("Memory components initialized successfully.")
```

## Phase 2: The Memory-Augmented Agent
Bây giờ chúng ta sẽ xây dựng agent sử dụng hệ thống bộ nhớ này. Chúng ta sẽ sử dụng LangGraph để định nghĩa một workflow có trạng thái, rõ ràng: truy xuất bộ nhớ, tạo một phản hồi sử dụng các bộ nhớ đó và cuối cùng là cập nhật bộ nhớ với tương tác mới nhất.

```python
# Định nghĩa state cho LangGraph agent của chúng ta
class AgentState(TypedDict):
    user_input: str
    retrieved_memories: Optional[str]
    generation: str

# Định nghĩa các node trong graph

def retrieve_memory(state: AgentState) -> Dict[str, Any]:
    """Node truy xuất bộ nhớ từ cả episodic store và semantic store."""
    console.print("--- Retrieving Memories ---")
    user_input = state['user_input']
    
    # Truy xuất từ episodic memory
    retrieved_docs = episodic_vector_store.similarity_search(user_input, k=2)
    episodic_memories = "\n".join([doc.page_content for doc in retrieved_docs])
    
    # Truy xuất từ semantic memory
    try:
        graph_schema = graph.get_schema
        semantic_memories = str(graph.query("""
            UNWIND $keywords AS keyword
            CALL db.index.fulltext.queryNodes("entity", keyword) YIELD node, score
            MATCH (node)-[r]-(related_node)
            RETURN node, r, related_node LIMIT 5
            """, {'keywords': user_input.split()}))
    except Exception as e:
        semantic_memories = f"Could not query graph: {e}"
        
    retrieved_content = f"Relevant Past Conversations (Episodic Memory):\n{episodic_memories}\n\nRelevant Facts (Semantic Memory):\n{semantic_memories}"
    console.print(f"[cyan]Retrieved Context:\n{retrieved_content}[/cyan]")
    
    return {"retrieved_memories": retrieved_content}

def generate_response(state: AgentState) -> Dict[str, Any]:
    """Node tạo phản hồi sử dụng các bộ nhớ đã truy xuất."""
    console.print("--- Generating Response ---")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful and personalized financial assistant. Use the retrieved memories to inform your response and tailor it to the user. If the memories indicate a user's preference (e.g., they are a conservative investor), you MUST respect it."),
        ("human", "My question is: {user_input}\n\nHere are some memories that might be relevant:\n{retrieved_memories}")
    ])
    generator = prompt | llm
    generation = generator.invoke(state).content
    console.print(f"[green]Generated Response:\n{generation}[/green]")
    return {"generation": generation}

def update_memory(state: AgentState) -> Dict[str, Any]:
    """Node cập nhật bộ nhớ với tương tác mới nhất."""
    console.print("--- Updating Memory ---")
    create_memories(state['user_input'], state['generation'])
    return {}

# Xây dựng graph
workflow = StateGraph(AgentState)

workflow.add_node("retrieve", retrieve_memory)
workflow.add_node("generate", generate_response)
workflow.add_node("update", update_memory)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", "update")
workflow.add_edge("update", END)

memory_agent = workflow.compile()
print("Memory-augmented agent graph compiled successfully.")
```

## Phase 3: Demonstration & Inspection
Hãy cùng xem agent hoạt động. Chúng ta sẽ mô phỏng một cuộc hội thoại nhiều lượt. Hai lượt đầu tiên sẽ gieo mầm cho bộ nhớ. Lượt thứ ba sẽ kiểm tra xem agent có thể sử dụng bộ nhớ đó để đưa ra phản hồi cá nhân hóa hay không. Cuối cùng, chúng ta sẽ trực tiếp kiểm tra các database để xem các bộ nhớ đã được tạo ra.

```python
def run_interaction(query: str):
    result = memory_agent.invoke({"user_input": query})
    return result['generation']

console.print("\n--- 💬 INTERACTION 1: Seeding Memory ---")
run_interaction("Hi, my name is Alex. I'm a conservative investor, and I'm mainly interested in established tech companies.")

console.print("\n--- 💬 INTERACTION 2: Asking a specific question ---")
run_interaction("What do you think about Apple (AAPL)?")

console.print("\n--- 🧠 INTERACTION 3: THE MEMORY TEST ---")
run_interaction("Based on my goals, what's a good alternative to that stock?")
```

### Inspecting the Memory Stores
Chúng ta hãy cùng nhìn sâu hơn. Chúng ta có thể truy vấn trực tiếp database để xem các bộ nhớ mà agent đã tạo ra.

```python
console.print("--- 🔍 Inspecting Episodic Memory (Vector Store) ---")
# Thực hiện tìm kiếm theo sự tương đồng cho một khái niệm chung để xem kết quả trả về
retrieved_docs = episodic_vector_store.similarity_search("User's investment strategy", k=3)
for i, doc in enumerate(retrieved_docs):
    print(f"{i+1}. {doc.page_content}")

console.print("\n--- 🕸️ Inspecting Semantic Memory (Graph Database) ---")
print(f"Graph Schema:\n{graph.get_schema}")

# Truy vấn Cypher để xem ai quan tâm đến cái gì
query_result = graph.query("MATCH (n:User)-[r:INTERESTED_IN|HAS_GOAL]->(m) RETURN n, r, m")
print(f"Relationships in Graph:\n{query_result}")
```

## Conclusion
Trong notebook này, chúng ta đã xây dựng thành công một agent với hệ thống bộ nhớ dài hạn, tinh vi. Bản demo đã cho thấy rõ sức mạnh của kiến trúc này:

- **Stateless Failure (Thất bại khi không có trạng thái):** Một agent tiêu chuẩn, khi được hỏi "Dựa trên các mục tiêu của tôi, lựa chọn thay thế tốt cho cổ phiếu đó là gì?", sẽ thất bại vì nó không có bộ nhớ về các mục tiêu của người dùng.
- **Memory-Augmented Success (Thành công khi được tăng cường bộ nhớ):** Agent của chúng ta đã thành công vì nó có thể:
    1.  **Nhớ lại Episodic:** Nó truy xuất bản tóm tắt của cuộc hội thoại đầu tiên: "Alex giới thiệu mình là một nhà đầu tư thận trọng..."
    2.  **Nhớ lại Semantic:** Nó truy vấn đồ thị và tìm thấy sự thật có cấu trúc: `(User: Alex) -[HAS_GOAL]-> (InvestmentPhilosophy: Conservative)`.
    3.  **Tổng hợp:** Nó sử dụng bối cảnh kết hợp này để đưa ra đề xuất có độ liên quan cao và mang tính cá nhân hóa (Microsoft), đề cập một cách rõ ràng đến các mục tiêu thận trọng của người dùng.

Sự kết hợp giữa việc nhớ lại *điều gì đã xảy ra* (episodic) và *điều gì đã biết* (semantic) là một paradigm mạnh mẽ để tiến xa hơn các agent giao dịch đơn giản, tiến tới tạo ra những người bạn đồng hành có khả năng học hỏi thực sự. Mặc dù việc quản lý bộ nhớ ở quy mô lớn mang lại các thách thức như việc cắt tỉa và hợp nhất, nhưng kiến trúc nền tảng mà chúng ta đã xây dựng ở đây là một bước tiến quan trọng hướng tới các hệ thống AI thông minh và cá nhân hóa hơn.
