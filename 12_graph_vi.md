# 📘 Agentic Architectures 12: Graph / World-Model Memory

Chào mừng bạn đến với bài tìm hiểu chi tiết về một trong những cấu trúc bộ nhớ mạnh mẽ nhất cho các AI agent: **Graph-based World Model**. Kiến trúc này vượt xa việc truy xuất tài liệu đơn giản hoặc lịch sử trò chuyện để xây dựng một sự hiểu biết có cấu trúc, kết nối lẫn nhau về thế giới, giống như bộ nhớ ngữ nghĩa (semantic memory) của con người.

Thay vì lưu trữ thông tin dưới dạng các đoạn văn bản (chunks) bị cô lập, một graph-based agent sẽ phân tích dữ liệu đầu vào thành các **thực thể (nodes)** và **mối quan hệ (edges)**. Điều này tạo ra một đồ thị tri thức (knowledge graph) phong phú, có thể truy vấn được. Sau đó, agent có thể trả lời các câu hỏi phức tạp bằng cách duyệt qua đồ thị này, khám phá ra những hiểu biết vốn bị ẩn giấu trong văn bản phi cấu trúc.

Để trình bày chi tiết điều này, chúng ta sẽ xây dựng một **Corporate Intelligence Agent**. Agent này sẽ:
1.  **Ingest Unstructured Reports (Hấp thụ báo cáo phi cấu trúc):** Đọc các tài liệu văn bản về các công ty, con người và sản phẩm.
2.  **Construct a Knowledge Graph (Xây dựng đồ thị tri thức):** Sử dụng một LLM để trích xuất các thực thể (ví dụ: `Company`, `Person`) và các mối quan hệ (ví dụ: `ACQUIRED`, `WORKS_FOR`, `COMPETES_WITH`) và đổ vào cơ sở dữ liệu đồ thị Neo4j.
3.  **Answer Complex, Multi-Hop Questions (Trả lời câu hỏi đa bước phức tạp):** Sử dụng đồ thị để trả lời các câu hỏi yêu cầu kết nối nhiều mẩu thông tin, chẳng hạn như "*Ai làm việc cho công ty đã mua lại BetaSolutions?*"—một loại truy vấn cực kỳ khó đối với vector search tiêu chuẩn.

### Definition
Một kiến trúc **Graph / World-Model Memory** là nơi tri thức được lưu trữ trong một cơ sở dữ liệu đồ thị có cấu trúc. Thông tin được đại diện dưới dạng các node (thực thể như con người, địa điểm, khái niệm) và các edge (mối quan hệ giữa chúng). Điều này tạo ra một "mô hình thế giới" (world model) năng động mà agent có thể thực hiện lập luận trên đó.

### High-level Workflow
1.  **Information Ingestion (Hấp thụ thông tin):** Agent nhận dữ liệu phi cấu trúc hoặc bán cấu trúc (văn bản, tài liệu, phản hồi API).
2.  **Knowledge Extraction (Trích xuất tri thức):** Một quy trình được hỗ trợ bởi LLM giúp phân tích thông tin, xác định các thực thể chính và các mối quan hệ kết nối chúng.
3.  **Graph Update (Cập nhật đồ thị):** Các node và edge được trích xuất sẽ được thêm vào hoặc cập nhật trong một cơ sở dữ liệu đồ thị bền vững (như Neo4j).
4.  **Question Answering / Reasoning (Trả lời câu hỏi / Lập luận):** Khi được đặt câu hỏi, agent sẽ:
    a. Chuyển đổi câu hỏi ngôn ngữ tự nhiên thành một ngôn ngữ truy vấn đồ thị chính thức (ví dụ: Cypher cho Neo4j).
    b. Thực thi truy vấn đối với đồ thị để truy xuất các đồ thị con (subgraphs) hoặc các sự kiện liên quan.
    c. Tổng hợp kết quả truy vấn thành một câu trả lời bằng ngôn ngữ tự nhiên.

### When to Use / Applications
*   **Trợ lý tri thức doanh nghiệp:** Xây dựng một mô hình có thể truy vấn về các dự án, nhân viên và khách hàng của công ty từ các tài liệu nội bộ.
*   **Trợ lý nghiên cứu nâng cao:** Tạo một cơ sở tri thức năng động về một lĩnh vực khoa học bằng cách hấp thụ các bài báo nghiên cứu.
*   **Chẩn đoán hệ thống phức tạp:** Mô hình hóa các thành phần của hệ thống và sự phụ thuộc của chúng để chẩn đoán lỗi.

### Strengths & Weaknesses
*   **Strengths:**
    *   **Có cấu trúc & Có thể giải thích được:** Tri thức được tổ chức cao. Một câu trả lời có thể được giải thích bằng cách chỉ ra con đường chính xác trong đồ thị đã dẫn đến nó.
    *   **Cho phép lập luận phức tạp:** Xuất sắc trong việc trả lời các câu hỏi "đa bước" (multi-hop) yêu cầu kết nối các mẩu thông tin rời rạc thông qua các mối quan hệ.
*   **Weaknesses:**
    *   **Độ phức tạp ban đầu:** Yêu cầu một schema được định nghĩa rõ ràng và một quy trình trích xuất mạnh mẽ.
    *   **Cập nhật đồ thị:** Có thể gặp thử thách trong việc quản lý các cập nhật, giải quyết thông tin mâu thuẫn và loại bỏ các sự kiện lỗi thời theo thời gian (quản lý vòng đời tri thức).

## Phase 0: Foundation & Setup
Chúng ta sẽ cài đặt các thư viện, bao gồm Neo4j driver, và cấu hình môi trường. **Quan trọng là bạn phải có một instance Neo4j đang chạy và một file `.env` với các thông tin đăng nhập.**

```python
# !pip install -q -U langchain-nebius langchain langgraph rich python-dotenv langchain_community neo4j
```

```python
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Pydantic for data modeling
from pydantic import BaseModel, Field

# LangChain components
from langchain_nebius import ChatNebius
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel as V1BaseModel

# For pretty printing
from rich.console import Console
from rich.markdown import Markdown

# --- API Key and Tracing Setup ---
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agentic Architecture - Graph Memory (Nebius)"

required_vars = ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD"]
for var in required_vars:
    if var not in os.environ:
        print(f"Warning: Environment variable {var} not set.")

print("Environment variables loaded and tracing is set up.")
```

## Phase 1: Building the Graph Construction Agent
Đây là trái tim của pipeline hấp thụ thông tin. Chúng ta cần một agent có thể đọc văn bản phi cấu trúc và trích xuất các thực thể cũng như các mối quan hệ dưới một định dạng có cấu trúc. Chúng ta sẽ sử dụng một LLM với khả năng đầu ra có cấu trúc (Pydantic) để đóng vai trò là bộ trích xuất tri thức.

```python
console = Console()
llm = ChatNebius(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0)

# Kết nối tới cơ sở dữ liệu Neo4j
try:
    graph = Neo4jGraph()
    # Xóa đồ thị để có một lượt chạy sạch sẽ
    graph.query("MATCH (n) DETACH DELETE n")
except Exception as e:
    console.print(f"[bold red]Failed to connect to Neo4j: {e}. Please check your credentials and connection.[/bold red]")
    graph = None

# Pydantic models cho trích xuất có cấu trúc (sử dụng LangChain v1 BaseModel để tương thích với các phương thức đầu ra có cấu trúc cũ hơn)
class Node(V1BaseModel):
    id: str = Field(description="Unique name or identifier for the entity.")
    type: str = Field(description="The type or label of the entity (e.g., Person, Company, Product).")

class Relationship(V1BaseModel):
    source: Node
    target: Node
    type: str = Field(description="The type of relationship (e.g., WORKS_FOR, ACQUIRED).")

class KnowledgeGraph(V1BaseModel):
    """Một đồ thị gồm các node và relationship."""
    relationships: List[Relationship]

# Graph Maker Agent
def get_graph_maker_chain():
    extractor_llm = llm.with_structured_output(KnowledgeGraph)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at extracting information from text and building a knowledge graph. Extract all entities (nodes) and relationships from the provided text. The relationship type should be a verb in all caps, like 'WORKS_FOR' or 'ACQUIRED'."),
        ("human", "Extract a knowledge graph from the following text:\n\n{text}")
    ])
    return prompt | extractor_llm

graph_maker_agent = get_graph_maker_chain()
print("Successfully connected to Neo4j and defined the Graph Maker Agent.")
```

## Phase 2: Ingesting Knowledge and Building the World Model
Bây giờ, chúng ta sẽ cung cấp cho agent một loạt các tài liệu liên quan nhưng riêng biệt. Agent sẽ xử lý từng tài liệu và dần dần xây dựng đồ thị tri thức doanh nghiệp. Điều này mô phỏng cách một hệ thống thực tế sẽ học hỏi theo thời gian khi có thông tin mới.

```python
unstructured_documents = [
    "On May 15, 2023, global tech giant AlphaCorp announced its acquisition of startup BetaSolutions, a leader in cloud-native database technology.",
    "Dr. Evelyn Reed, a renowned AI researcher, has been the Chief Science Officer at AlphaCorp since 2021. She leads the team responsible for the QuantumLeap AI platform.",
    "Innovate Inc.'s flagship product, NeuraGen, is seen as a direct competitor to AlphaCorp's QuantumLeap AI. Meanwhile, Innovate Inc. recently hired Johnathan Miles as their new CTO."
]
for i, doc in enumerate(unstructured_documents):
    console.print(f"--- Ingesting Document {i+1} ---")
    try:
        kg_data = graph_maker_agent.invoke({"text": doc})
        if kg_data.relationships:
            graph.add_graph_documents(graph_documents=kg_data.relationships, include_source=False)
            console.print(f"[green]Successfully added {len(kg_data.relationships)} relationships to the graph.[/green]")
        else:
             console.print("[yellow]No relationships extracted.[/yellow]")
    except Exception as e:
        console.print(f"[red]Failed to process document: {e}[/red]")

console.print("--- ✅ Knowledge Graph Ingestion Complete ---")
console.print("\n--- Graph Schema ---")
console.print(graph.schema)
```

## Phase 3: Building the Graph-Querying Agent
Với đồ thị tri thức đã có dữ liệu, chúng ta cần một agent có thể sử dụng nó. Điều này bao gồm một quy trình **Text-to-Cypher**. Agent sẽ nhận một câu hỏi ngôn ngữ tự nhiên từ người dùng, chuyển đổi nó thành một truy vấn Cypher sử dụng schema của đồ thị làm ngữ cảnh, thực thi truy vấn, và sau đó tổng hợp các kết quả thành một câu trả lời mà con người có thể đọc được.

```python
# LangChain có một chain tích hợp cho việc này, nhưng chúng ta sẽ kiểm tra các thành phần
# để hiểu cách nó hoạt động.
cypher_generation_prompt = ChatPromptTemplate.from_template(
    """You are an expert Neo4j Cypher query developer. Your task is to convert a user's natural language question into a valid Cypher query.
You must use the provided graph schema to construct the query. Do not use any node labels or relationship types that are not in the schema.
Return ONLY the Cypher query, with no additional text or explanations.

Graph Schema:
{schema}

User Question:
{question}
"""
)

cypher_response_prompt = ChatPromptTemplate.from_template(
    """You are an assistant that provides clear, natural language answers based on query results from a knowledge graph.
Use the context from the graph query result to answer the user's original question.

User Question: {question}
Query Result: {context}
"""
)

def query_graph(question: str) -> Dict[str, Any]:
    """Toàn bộ pipeline Text-to-Cypher và synthesis."""
    console.print(f"\n[bold]Question:[/bold] {question}")
    
    # 1. Tạo Cypher Query
    console.print("--- ➡️ Generating Cypher Query ---")
    cypher_chain = cypher_generation_prompt | llm
    generated_cypher = cypher_chain.invoke({"schema": graph.schema, "question": question}).content
    console.print(f"[cyan]Generated Cypher:\n{generated_cypher}[/cyan]")
    
    # 2. Thực thi Cypher Query
    console.print("--- ⚡ Executing Query ---")
    try:
        context = graph.query(generated_cypher)
        console.print(f"[yellow]Query Result:\n{context}[/yellow]")
    except Exception as e:
        console.print(f"[red]Cypher Query Failed: {e}[/red]")
        return {"answer": "I was unable to execute a query to find the answer to your question."}
    
    # 3. Tổng hợp câu trả lời cuối cùng
    console.print("--- 🗣️ Synthesizing Final Answer ---")
    synthesis_chain = cypher_response_prompt | llm
    answer = synthesis_chain.invoke({"question": question, "context": context}).content
    
    return {"answer": answer}

print("Graph-Querying Agent defined successfully.")
```

## Phase 4: Demonstration & Analysis
Bây giờ là bài kiểm tra cuối cùng. Chúng ta sẽ đặt cho agent các câu hỏi từ việc truy xuất sự thật đơn giản đến lập luận đa bước phức tạp, yêu cầu kết nối thông tin từ cả ba tài liệu nguồn của chúng ta.

```python
# Test 1: Truy xuất sự thật đơn giản (yêu cầu thông tin từ doc 2)
result1 = query_graph("Who works for AlphaCorp?")
console.print("\n--- Final Answer ---")
console.print(Markdown(result1['answer']))

# Test 2: Một truy xuất sự thật đơn giản khác (yêu cầu thông tin từ doc 1)
result2 = query_graph("What company did AlphaCorp acquire?")
console.print("\n--- Final Answer ---")
console.print(Markdown(result2['answer']))

# Test 3: Câu hỏi lập luận đa bước (yêu cầu thông tin từ cả 3 tài liệu)
result3 = query_graph("What companies compete with the products made by the company that acquired BetaSolutions?")
console.print("\n--- Final Answer ---")
console.print(Markdown(result3['answer']))
```

### Analysis of the Results
Phần trình diễn làm nổi bật lợi thế sâu sắc của một graph-based world model:

- Hai câu hỏi đầu tiên là các lần tra cứu đơn giản. Agent đã chuyển đổi thành công câu hỏi thành Cypher, truy vấn đồ thị và tìm thấy các mối quan hệ trực tiếp.

- Câu hỏi thứ ba là câu hỏi then chốt. Một RAG agent tiêu chuẩn sẽ thất bại ở đây. Nó có thể tìm thấy tài liệu về việc mua lại và tài liệu về đối thủ cạnh tranh, nhưng nó sẽ gặp khó khăn để kết nối chúng. Nó thiếu cấu trúc quan hệ rõ ràng để hiểu rằng "AlphaCorp" trong tài liệu 1 là cùng một thực thể với "AlphaCorp" trong tài liệu 2 và 3.

- Agent dựa trên đồ thị của chúng ta đã giải quyết nó một cách dễ dàng. Chúng ta có thể theo dõi logic của nó trực tiếp từ truy vấn Cypher được tạo ra:
    1.  `MATCH (acquirer:Company)-[:ACQUIRED]->(:Company {id: 'BetaSolutions'})`: Đầu tiên, tìm công ty đã mua lại BetaSolutions (Kết quả: AlphaCorp).
    2.  `MATCH (acquirer)-[:PRODUCES]->(product:Product)`: Tiếp theo, tìm các sản phẩm do công ty đó sản xuất (Kết quả: QuantumLeap AI).
    3.  `MATCH (product)-[:COMPETES_WITH]->(competitor_product:Product)`: Sau đó, tìm các sản phẩm cạnh tranh với sản phẩm đó (Kết quả: NeuraGen).
    4.  `MATCH (competitor_company:Company)-[:PRODUCES]->(competitor_product)`: Cuối cùng, tìm công ty sản xuất sản phẩm cạnh tranh đó (Kết quả: Innovate Inc.).

Khả năng duyệt qua các mối quan hệ và tổng hợp thông tin từ các nguồn khác nhau là "siêu năng lực" của kiến trúc Graph / World-Model. Câu trả lời không chỉ được truy xuất; nó được lập luận ra.

## Conclusion
Trong notebook này, chúng ta đã xây dựng một hệ thống agentic hoàn chỉnh xoay quanh một **Graph / World-Model Memory**. Chúng ta đã chứng minh toàn bộ vòng đời: hấp thụ dữ liệu phi cấu trúc, sử dụng một LLM để xây dựng một đồ thị tri thức có cấu trúc, và sau đó sử dụng đồ thị đó để trả lời các câu hỏi đa bước phức tạp đòi hỏi lập luận thực sự.

Kiến trúc này đại diện cho một bước tiến đáng kể về khả năng so với các hệ thống bộ nhớ đơn giản hơn. Bằng cách tạo ra một mô hình thế giới rõ ràng, có thể truy vấn được, chúng ta cung cấp cho agent khả năng kết nối các sự thật rời rạc và khám phá ra những hiểu biết tiềm ẩn. Mặc dù các thử thách trong việc duy trì đồ thị này theo thời gian là có thực, nhưng tiềm năng xây dựng các trợ lý AI có kiến thức sâu rộng và có thể giải thích được khiến đây trở thành một trong những pattern thú vị và mạnh mẽ nhất trong thiết kế agentic hiện đại.
