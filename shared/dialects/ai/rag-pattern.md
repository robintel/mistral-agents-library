---
type: pattern
family: ai
---

# RAG Pattern Contract

Attaches to any work building or using **Retrieval-Augmented Generation (RAG)** systems. This contract establishes the **standard patterns, architectures, and best practices** for implementing RAG applications effectively. Loads alongside the rag-engineer agent and any AI/ML framework contracts.

RAG is **not just adding a vector database to an LLM** — it's a **system design discipline** that requires careful consideration of document processing, retrieval strategies, prompt engineering, and evaluation. A well-designed RAG system can transform an LLM from a general-purpose tool into a domain-specific expert, but a poorly designed one can be worse than no retrieval at all.

## The Discipline

RAG transforms static LLMs into **dynamic knowledge systems** by grounding responses in external data. The discipline requires:

- **Document-first thinking**: The quality of your RAG is limited by the quality of your documents
- **Retrieval is the bottleneck**: A great LLM with poor retrieval is useless
- **Context matters**: How you present retrieved information to the LLM dramatically affects output quality
- **Measurement is mandatory**: You cannot improve what you cannot measure
- **Latency compounds**: Each component adds latency; optimize aggressively
- **Cost scales**: Token costs, vector database costs, and infrastructure costs must be managed

The RAG pattern contract provides:
- **Architecture patterns** for different use cases and complexity levels
- **Component contracts** for each part of the RAG pipeline
- **Best practices** learned from production deployments
- **Anti-patterns** to avoid common pitfalls
- **Evaluation frameworks** to measure and improve quality

## RAG Architecture Patterns

### 1. Naive RAG (Baseline Pattern)
**Pattern**: Document → Chunk → Embed → Store → Retrieve → Generate

**Structure**:
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │────▶│   Input      │────▶│   Embed     │
│   Query      │     │   Processing │     │   Query     │
└─────────────┘     └─────────────┘     └──────────┬───┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────┐
│                   Vector Database                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   Chunk     │    │   Chunk     │    │   Chunk     │  │
│  │   Embedding │    │   Embedding │    │   Embedding │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
               ┌─────────────┐
               │   LLM       │
               │   with      │
               │   Context   │
               └─────────────┘
                          │
                          ▼
                 ┌─────────────┐
                 │   Output    │
                 │   Response  │
                 └─────────────┘
```

**When to Use**:
- Proof of concept or MVP
- Simple Q&A applications
- Internal knowledge bases with straightforward queries
- Low-complexity use cases

**Pros**:
- Simple to implement
- Fast to deploy
- Good for getting started

**Cons**:
- No query understanding
- No retrieval feedback loop
- No document re-ranking
- Poor handling of complex queries
- Susceptible to context overflow

**Pitfalls**:
- **Garbage in, garbage out**: Poor documents = poor answers
- **Lost in translation**: Embedding may not capture document meaning
- **Needle in haystack**: Important info buried in long documents
- **Context explosion**: Retrieving too much irrelevant context

**Mitigations**:
- Use high-quality, well-structured documents
- Implement proper chunking with overlap
- Set appropriate top-k limits
- Add basic filtering by metadata

---

### 2. Query Expansion RAG
**Pattern**: User Query → Expand → Retrieve → Generate

**Structure**:
```
┌─────────────┐
│   User      │
│   Query      │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│   Query Expansion            │
│  ┌─────────────┐  ┌─────────┐  │
│  │ HyDE        │  │ Sub-Q    │  │
│  │ (Hypothetical│  │ (Sub-    │  │
│  │  Document   │  │  Questions│  │
│  │  Embedding) │  │          │  │
│  └─────────────┘  └─────────┘  │
│  ┌─────────────┐  ┌─────────┐  │
│  │ Query       │  │ Synonym  │  │
│  │  Rewriting   │  │ Injection│  │
│  └─────────────┘  └─────────┘  │
└─────────────┬────────────────┘
              │
              ▼
      ┌─────────────────┐
      │   Embed &       │
      │   Retrieve       │
      └────────┬────────┘
               │
               ▼
        ┌─────────────┐
        │   LLM       │
        │   with      │
        │   Context   │
        └─────────────┘
```

**When to Use**:
- Complex queries that need better understanding
- Domain-specific terminology that may not match document language
- Queries where simple similarity search performs poorly
- Technical or specialized domains

**Expansion Techniques**:

#### HyDE (Hypothetical Document Embeddings)
**Concept**: Generate a hypothetical answer to the query, embed it, and retrieve documents similar to this hypothetical answer.

**Implementation**:
```python
# Step 1: Generate hypothetical answer
hypothetical_answer = llm.generate(
    prompt=f"Generate a hypothetical answer to: {user_query}"
)

# Step 2: Embed the hypothetical answer
hypothetical_embedding = embedding_model.embed(hypothetical_answer)

# Step 3: Retrieve documents similar to the hypothetical answer
results = vector_db.search(hypothetical_embedding, k=5)
```

**Pros**:
- Captures semantic intent, not just keyword matching
- Works well for complex, multi-faceted queries
- Can retrieve documents that don't share keywords with the query

**Cons**:
- Additional latency from generating hypothetical answer
- Additional cost from extra LLM call
- May introduce bias from the hypothetical answer

#### Query Rewriting
**Concept**: Use an LLM to rewrite the user's query to be more effective for retrieval.

**Implementation**:
```python
rewritten_query = llm.generate(
    prompt=f"""
    Rewrite the following query to improve search results.
    Keep the meaning the same but make it more likely to match
    relevant documents in a vector database.
    
    Original query: {user_query}
    Rewritten query:
    """
)
```

**Pros**:
- Improves query quality without changing user experience
- Can add domain-specific terms
- Can expand abbreviations and jargon

**Cons**:
- Additional latency and cost
- May change query intent
- Requires careful prompt engineering

#### Sub-Questions
**Concept**: Break a complex query into multiple sub-questions, retrieve for each, then combine results.

**Implementation**:
```python
# Step 1: Generate sub-questions
sub_questions = llm.generate(
    prompt=f"""
    Break the following complex query into 2-4 simpler sub-questions
    that can be answered independently and then combined.
    
    Query: {user_query}
    Sub-questions:
    """
)

# Step 2: Retrieve for each sub-question
all_results = []
for question in sub_questions:
    results = retrieve(question, k=3)
    all_results.extend(results)

# Step 3: Deduplicate and rerank
final_results = deduplicate_and_rerank(all_results, k=5)
```

**Pros**:
- Handles complex, multi-part queries well
- Can capture different aspects of a complex question
- More likely to retrieve all relevant information

**Cons**:
- Multiple retrieval operations increase latency
- Requires deduplication logic
- May retrieve redundant information

#### Synonym Injection
**Concept**: Add synonyms and related terms to the query to improve recall.

**Implementation**:
```python
# Step 1: Get synonyms for query terms
synonyms = synonym_db.get_synonyms(user_query)

# Step 2: Create expanded query
expanded_query = f"{user_query} {synonyms}"

# Step 3: Embed and retrieve
results = retrieve(expanded_query, k=5)
```

**Pros**:
- Improves recall for queries with multiple valid terms
- Works well for technical domains with established synonyms
- Low computational overhead

**Cons**:
- Requires domain-specific synonym database
- May introduce noise if synonyms aren't precise
- Limited effectiveness for complex queries

---

### 3. Multi-Hop RAG
**Pattern**: Query → Retrieve → Generate Intermediate → Retrieve Again → Final Generate

**Structure**:
```
┌─────────────┐
│   User      │
│   Query      │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   First Retrieval    │
│   (Initial context)  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Intermediate Generation    │
│   (Decomposition, sub-queries,│
│    reasoning, next steps)     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────┐
│   Second Retrieval   │
│   (With new queries) │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Final Generation   │
│   (With all context) │
└─────────────────────┘
```

**When to Use**:
- Complex, multi-step reasoning tasks
- Research questions requiring multiple information sources
- Questions that benefit from iterative refinement
- Situations where initial retrieval is insufficient

**Implementation Patterns**:

#### Sequential Multi-Hop
```python
# Hop 1: Initial retrieval
context_1 = retrieve(user_query, k=5)

# Generate intermediate reasoning
hop_1_thoughts = llm.generate(
    prompt=f"""
    Based on the context below, what additional information do we need
    to fully answer the user's question?
    
    Context: {context_1}
    User question: {user_query}
    
    Additional queries needed:
    """
)

# Hop 2: Retrieve with new queries
context_2 = retrieve(hop_1_thoughts, k=5)

# Final generation
final_answer = llm.generate(
    prompt=f"""
    Answer the user's question using all the context below.
    
    Context from first retrieval: {context_1}
    Context from second retrieval: {context_2}
    
    User question: {user_query}
    """
)
```

#### Parallel Multi-Hop
```python
# Generate multiple parallel queries
parallel_queries = llm.generate(
    prompt=f"""
    Generate 3-5 parallel queries that would help answer the user's question.
    Each query should retrieve different but complementary information.
    
    User question: {user_query}
    Parallel queries:
    """
)

# Retrieve for all queries in parallel
parallel_results = [retrieve(q, k=3) for q in parallel_queries]

# Combine and generate final answer
final_answer = llm.generate(
    prompt=f"""
    Answer the user's question using all the retrieved context below.
    
    Retrieved contexts:
    {parallel_results}
    
    User question: {user_query}
    """
)
```

**Pros**:
- Can handle very complex queries
- Iterative improvement of results
- More comprehensive information gathering

**Cons**:
- Significantly higher latency
- Higher computational cost
- More complex implementation
- Requires careful query generation

---

### 4. Graph RAG
**Pattern**: Document → Extract Entities/Relationships → Build Knowledge Graph → Retrieve + Reason

**Structure**:
```
┌─────────────┐
│   Documents  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│   Entity & Relationship       │
│   Extraction                  │
│  ┌─────────────┐  ┌─────────┐  │
│  │ Entity      │  │ Relationship│  │
│  │  Recognition │  │  Extraction │  │
│  └─────────────┘  └─────────┘  │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Knowledge Graph             │
│  ┌───────────┐              │
│  │   Node    │◄─────────────┤
│  │ (Entity)  │              │
│  └─────┬─────┘              │
│        │                    │
│  ┌─────▼─────┐              │
│  │   Edge    │              │
│  │ (Relation)│              │
│  └───────────┘              │
└─────────────┬────────────────┘
              │
              ▼
      ┌─────────────────┐
      │   Hybrid         │
      │   Retrieval      │
      │  (Vector + Graph)│
      └────────┬────────┘
               │
               ▼
        ┌─────────────┐
        │   LLM       │
        │   with      │
        │   Context   │
        └─────────────┘
```

**When to Use**:
- Structured knowledge domains (technical, scientific, organizational)
- Queries involving relationships between entities
- Reasoning that benefits from understanding connections
- Situations where graph structure provides additional signal

**Implementation**:

```python
# Step 1: Entity and relationship extraction
entities = []
relationships = []

for document in documents:
    # Extract entities
    entity_result = llm.generate(
        prompt=f"""
        Extract all entities from the following document.
        Entities can be: people, organizations, locations, dates,
        technical terms, product names, etc.
        
        Document: {document}
        
        Entities:
        """
    )
    entities.extend(entity_result)
    
    # Extract relationships
    relationship_result = llm.generate(
        prompt=f"""
        Extract all relationships between entities in the following document.
        Relationships should be: verb phrases, connections, dependencies,
        hierarchies, etc.
        
        Document: {document}
        Entities: {entity_result}
        
        Relationships (source -> relation -> target):
        """
    )
    relationships.extend(relationship_result)

# Step 2: Build knowledge graph
kg = KnowledgeGraph()
kg.add_entities(entities)
kg.add_relationships(relationships)

# Step 3: Store in graph database
kg.store(graph_db)

# Step 4: Hybrid retrieval
# Vector retrieval
top_k_vector = vector_db.search(query_embedding, k=10)

# Graph retrieval (find related entities)
top_k_graph = kg.search_related(query_entities, k=10)

# Combine results
combined_results = combine(top_k_vector, top_k_graph)
```

**Pros**:
- Captures relationships between entities
- Enables reasoning over connections
- Can answer relationship-based queries ("Who reports to X?", "What causes Y?")
- Provides additional signal beyond semantic similarity

**Cons**:
- Complex implementation
- Entity/relationship extraction can be error-prone
- Requires graph database
- Higher infrastructure complexity

---

### 5. Agentic RAG
**Pattern**: Query → Plan → Execute Tools → Synthesize

**Structure**:
```
┌─────────────┐
│   User      │
│   Query      │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│   Query Understanding         │
│   & Decomposition             │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Planning                   │
│   (What tools/data needed?)  │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Tool Selection &           │
│   Execution Planning          │
│  ┌─────────────┐  ┌─────────┐  │
│  │ Vector      │  │ Web      │  │
│  │  Search     │  │ Search   │  │
│  └─────────────┘  └─────────┘  │
│  ┌─────────────┐  ┌─────────┐  │
│  │ Database    │  │ API      │  │
│  │  Query      │  │ Call     │  │
│  └─────────────┘  └─────────┘  │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Tool Execution              │
│   (Retrieve data)             │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Synthesis                   │
│   (Combine results, answer)   │
└─────────────────────────────┘
```

**When to Use**:
- Tasks requiring external tool use (web search, API calls, database queries)
- Complex information gathering across multiple sources
- Dynamic environments where data sources change
- Situations requiring real-time information

**Implementation**:

```python
class AgenticRAG:
    def __init__(self):
        self.tools = {
            "vector_search": VectorSearchTool(),
            "web_search": WebSearchTool(),
            "database_query": DatabaseQueryTool(),
            "api_call": APICallTool(),
        }
    
    def query(self, user_query):
        # Step 1: Understand the query and plan
        plan = self.llm.generate(
            prompt=f"""
            Analyze the following user query and determine:
            1. What information is needed to answer it?
            2. What tools should be used?
            3. What are the sub-queries for each tool?
            
            Available tools: {list(self.tools.keys())}
            
            User query: {user_query}
            
            Plan:
            """
        )
        
        # Step 2: Execute tools based on plan
        results = []
        for tool_name, sub_query in plan.tool_calls:
            tool = self.tools[tool_name]
            result = tool.execute(sub_query)
            results.append((tool_name, sub_query, result))
        
        # Step 3: Synthesize results
        final_answer = self.llm.generate(
            prompt=f"""
            Synthesize the following results to answer the user's query.
            Include citations for each source.
            
            Tool results:
            {results}
            
            User query: {user_query}
            """
        )
        
        return final_answer
```

**Pros**:
- Can gather information from multiple, diverse sources
- Flexible and adaptable to different query types
- Can incorporate real-time information
- More powerful than static RAG

**Cons**:
- Very complex implementation
- Tool selection and orchestration is challenging
- Higher latency due to multiple tool calls
- More failure modes (any tool can fail)
- Security considerations for tool access

---

### 6. Modular RAG
**Pattern**: Decompose RAG into independent, swappable modules

**Structure**:
```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline                              │
├─────────────────┬─────────────────┬─────────────────┬────────┤
│  Document        │  Retrieval        │  Generation       │  User   │
│  Processing      │  Pipeline         │  Pipeline         │  Interface│
│  Pipeline        │                  │                  │         │
└────────┬────────┴────────┬────────┴────────┬────────┴─────────┘
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Loaders         │ │  Retrievers      │ │  LLM Provider    │
│  (PDF, HTML, etc)│ │  (Vector, Keyword│ │  (Mistral, OpenAI│
│  ┌─────────────┐│ │   Hybrid)       │ │   etc.)          │
│  │ Text         ││ │  ┌─────────────┐│ │  ┌─────────────┐│
│  │ Chunking     ││ │  │ Reranker    ││ │  │ Prompt      ││
│  │ Embedding    ││ │  └─────────────┘│ │  │  Engine     ││
│  │ Storage      ││ └─────────────────┘│ │  └─────────────┘│
│  └─────────────┘                    │ └─────────────────┘
└─────────────────┘                  └───────────────────┘
```

**When to Use**:
- Production systems requiring flexibility and maintainability
- Systems that may need to swap components (different LLMs, vector DBs)
- Multi-team development where different teams own different modules
- Situations requiring A/B testing of different approaches

**Module Contracts**:

```python
# Document Processing Module Contract
class DocumentProcessor:
    def load(self, source) -> List[Document]: ...
    def chunk(self, document: Document) -> List[Chunk]: ...
    def embed(self, chunk: Chunk) -> Embedding: ...
    def store(self, chunk: Chunk, embedding: Embedding) -> str: ...

# Retrieval Module Contract
class Retriever:
    def retrieve(self, query: str, k: int = 5) -> List[Chunk]: ...
    def retrieve_with_metadata(self, query: str, k: int = 5) -> List[Tuple[Chunk, Metadata]]: ...

# Generation Module Contract
class Generator:
    def generate(self, prompt: str, context: List[Chunk], **kwargs) -> str: ...
    def stream(self, prompt: str, context: List[Chunk], **kwargs) -> Iterator[str]: ...

# Evaluation Module Contract
class Evaluator:
    def evaluate(self, query: str, answer: str, context: List[Chunk]) -> EvaluationResult: ...
```

**Pros**:
- Highly maintainable and testable
- Modules can be developed and tested independently
- Easy to swap out components (e.g., different LLMs)
- Enables experimentation and A/B testing
- Clear interfaces between components

**Cons**:
- More complex architecture
- Requires careful interface design
- May have performance overhead from modularity
- More integration testing needed

## Component Patterns

### Document Processing Patterns

#### 1. Hierarchical Chunking
**Pattern**: Split documents into hierarchical chunks (document → section → paragraph → sentence)

**Implementation**:
```python
def hierarchical_chunk(document, max_tokens=512):
    """
    Chunk document hierarchically:
    1. Try to split by sections (if document has clear structure)
    2. Try to split by paragraphs
    3. Split by sentences
    4. Ensure no chunk exceeds max_tokens
    """
    chunks = []
    
    # Split by sections if available
    if document.has_sections:
        for section in document.sections:
            section_chunks = hierarchical_chunk(section, max_tokens)
            chunks.extend(section_chunks)
    
    # Split by paragraphs
    elif document.has_paragraphs:
        for paragraph in document.paragraphs:
            paragraph_chunks = hierarchical_chunk(paragraph, max_tokens)
            chunks.extend(paragraph_chunks)
    
    # Split by sentences
    else:
        sentences = split_into_sentences(document.text)
        for sentence in sentences:
            if len(sentence) <= max_tokens:
                chunks.append(Chunk(text=sentence))
            else:
                # Split long sentences
                sub_chunks = split_into_tokens(sentence, max_tokens)
                chunks.extend(sub_chunks)
    
    return chunks
```

**When to Use**:
- Structured documents (reports, manuals, articles)
- Documents with natural hierarchical organization
- When you want to preserve document structure in chunks

---

#### 2. Semantic Chunking
**Pattern**: Split documents at semantic boundaries (topics, ideas) rather than fixed sizes

**Implementation**:
```python
def semantic_chunk(document, model):
    """
    Split document at semantic boundaries using LLM.
    """
    chunks = []
    current_chunk = ""
    
    # Process document in sections
    for section in document.sections:
        # Check if adding this section would exceed semantic coherence
        test_chunk = current_chunk + section.text
        
        coherence_score = model.evaluate_coherence(test_chunk)
        
        if coherence_score < THRESHOLD or len(test_chunk) > MAX_TOKENS:
            if current_chunk:
                chunks.append(Chunk(text=current_chunk))
                current_chunk = section.text
            else:
                # Section itself is too large, split it
                sub_chunks = semantic_chunk(section, model)
                chunks.extend(sub_chunks)
        else:
            current_chunk = test_chunk
    
    if current_chunk:
        chunks.append(Chunk(text=current_chunk))
    
    return chunks
```

**When to Use**:
- Documents where semantic coherence is critical
- Technical documents with complex concepts
- When fixed-size chunking breaks meaning

---

#### 3. Overlapping Chunks
**Pattern**: Create chunks with overlap to preserve context across boundaries

**Implementation**:
```python
def create_overlapping_chunks(document, chunk_size=512, overlap_size=100):
    """
    Create chunks with overlap to preserve context.
    """
    tokens = document.tokens
    chunks = []
    
    for i in range(0, len(tokens), chunk_size - overlap_size):
        chunk_tokens = tokens[i:i + chunk_size]
        chunks.append(Chunk(tokens=chunk_tokens, 
                           start_idx=i, 
                           end_idx=i + len(chunk_tokens)))
    
    return chunks
```

**When to Use**:
- Almost always (recommended default)
- Prevents information loss at chunk boundaries
- Helps with retrieval of partial information

**Overlap Sizes**:
- 10-20% of chunk size for general text
- 25-50% for technical documents with dense information
- Consider semantic overlap (repeat key sentences) instead of token overlap

---

### Retrieval Patterns

#### 1. Hybrid Search
**Pattern**: Combine vector similarity with keyword/BM25 search for better results

**Implementation**:
```python
def hybrid_retrieve(query, vector_db, keyword_db, k=5, alpha=0.5):
    """
    Retrieve using hybrid vector + keyword search.
    
    alpha: Weight for vector search (0 = pure keyword, 1 = pure vector)
    """
    # Vector search
    vector_results = vector_db.search(query, k=k)
    
    # Keyword search
    keyword_results = keyword_db.search(query, k=k)
    
    # Combine and rerank
    combined = []
    for i, (vec_result, kw_result) in enumerate(zip(vector_results, keyword_results)):
        combined_score = alpha * vec_result.score + (1 - alpha) * kw_result.score
        combined.append((vec_result, kw_result, combined_score))
    
    # Sort by combined score
    combined.sort(key=lambda x: x[2], reverse=True)
    
    # Return top k
    return [x[0] for x in combined[:k]]
```

**When to Use**:
- General-purpose RAG (recommended default)
- When you need both semantic and keyword matching
- Balances recall and precision

**Alpha Tuning**:
- alpha = 0.5: Balanced (recommended starting point)
- alpha > 0.5: More weight on semantic similarity
- alpha < 0.5: More weight on keyword matching

---

#### 2. Multi-Vector Retrieval
**Pattern**: Use multiple embedding vectors per chunk for different aspects

**Implementation**:
```python
def multi_vector_retrieve(query, vector_db, k=5):
    """
    Retrieve using multiple vectors per document.
    """
    # Query embedding
    query_embedding = embed(query)
    
    # Retrieve
    results = vector_db.search(query_embedding, k=k*3)  # Get more candidates
    
    # Rerank using all vectors
    reranked = []
    for doc in results:
        # Score using all of the document's vectors
        max_score = max([
            cosine_similarity(query_embedding, vec) 
            for vec in doc.vectors
        ])
        reranked.append((doc, max_score))
    
    # Sort and return top k
    reranked.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in reranked[:k]]
```

**When to Use**:
- Documents with multiple topics or aspects
- Complex documents where single embedding isn't sufficient
- When different parts of document need different embeddings

---

#### 3. Query Expansion with History
**Pattern**: Use conversation history to expand and improve queries

**Implementation**:
```python
def retrieve_with_history(query, conversation_history, vector_db, k=5):
    """
    Expand query using conversation history.
    """
    # Generate expanded query based on history
    expanded_query = llm.generate(
        prompt=f"""
        Given the conversation history below and the current query,
        generate an improved query that incorporates relevant context
        from the history.
        
        History: {conversation_history}
        Current query: {query}
        
        Expanded query:
        """
    )
    
    # Embed and retrieve
    results = vector_db.search(expanded_query, k=k)
    
    return results
```

**When to Use**:
- Chat-based RAG systems
- Multi-turn conversations
- When queries build on previous context

---

#### 4. Time-Aware Retrieval
**Pattern**: Incorporate temporal information into retrieval for time-sensitive queries

**Implementation**:
```python
def time_aware_retrieve(query, vector_db, k=5, time_range=None):
    """
    Retrieve with time awareness.
    """
    # Extract time from query if not provided
    if time_range is None:
        time_range = extract_time_range(query)
    
    # Filter by time range
    if time_range:
        results = vector_db.search_with_filter(
            query, 
            k=k,
            filters={"timestamp": time_range}
        )
    else:
        results = vector_db.search(query, k=k)
    
    return results

def extract_time_range(query):
    """
    Extract time range from query.
    """
    time_patterns = [
        (r"in (\d{4})", "year"),
        (r"between (\d{4}) and (\d{4})", "year range"),
        (r"last (\d+) (day|week|month|year)s?", "relative"),
        (r"since (\d{4}-\d{2}-\d{2})", "since date"),
    ]
    
    for pattern, time_type in time_patterns:
        match = re.search(pattern, query)
        if match:
            return create_time_filter(match.groups(), time_type)
    
    return None
```

**When to Use**:
- News, financial, or other time-sensitive data
- When documents have timestamps
- Queries with explicit time references

---

### Generation Patterns

#### 1. Structured Output Generation
**Pattern**: Generate output in a structured format (JSON, YAML, etc.) for easier processing

**Implementation**:
```python
def generate_structured(prompt, context, output_schema):
    """
    Generate structured output.
    """
    structured_prompt = f"""
    Answer the user's question using the context below.
    Format your answer as {output_schema}.
    
    Context: {context}
    Question: {prompt}
    
    Answer:
    """
    
    return llm.generate(structured_prompt)

# Example usage
output_schema = """
{
    "answer": "string",
    "confidence": "number (0-1)",
    "sources": ["string"]
}
"""

result = generate_structured(user_query, context, output_schema)
```

**When to Use**:
- API responses
- Automated processing pipelines
- When you need machine-readable output
- Structured data extraction

---

#### 2. Citation-Aware Generation
**Pattern**: Generate answers with explicit citations to source documents

**Implementation**:
```python
def generate_with_citations(prompt, context_chunks):
    """
    Generate answer with citations.
    """
    context_with_metadata = "\n\n".join(
        [f"[Source: {chunk.source}, Page: {chunk.page}]\n{chunk.text}" 
         for chunk in context_chunks]
    )
    
    generation_prompt = f"""
    Answer the question using ONLY the context below.
    For each statement in your answer, include a citation in [Source: ..., Page: ...] format.
    If you cannot answer from the context, say so.
    
    Context:
    {context_with_metadata}
    
    Question: {prompt}
    
    Answer with citations:
    """
    
    return llm.generate(generation_prompt)
```

**When to Use**:
- Knowledge base Q&A
- When traceability is important
- Legal, medical, or other high-stakes domains
- RAG systems where sources matter

---

#### 3. Confidence-Aware Generation
**Pattern**: Generate answers with confidence scores and uncertainty indication

**Implementation**:
```python
def generate_with_confidence(prompt, context):
    """
    Generate answer with confidence assessment.
    """
    confidence_prompt = f"""
    Answer the question using the context below.
    For each part of your answer, assess your confidence (0-1) based on:
    - How well the context supports the answer
    - How certain you are in your understanding
    
    Format your answer with confidence scores:
    [Confidence: 0.95] The answer is...
    [Confidence: 0.7] This part is less certain because...
    
    If you cannot answer confidently, state the uncertainty.
    
    Context: {context}
    Question: {prompt}
    
    Answer with confidence:
    """
    
    return llm.generate(confidence_prompt)
```

**When to Use**:
- High-stakes applications
- When uncertainty needs to be communicated
- Decision support systems
- Expert systems

---

#### 4. Multi-Persona Generation
**Pattern**: Generate answers from different perspectives or personas

**Implementation**:
```python
def generate_multi_persona(prompt, context, personas):
    """
    Generate answers from multiple personas.
    """
    results = {}
    for persona in personas:
        persona_prompt = f"""
        Answer the question from the perspective of {persona['name']}.
        Persona description: {persona['description']}
        
        Context: {context}
        Question: {prompt}
        
        Answer:
        """
        results[persona['name']] = llm.generate(persona_prompt)
    
    return results

# Example usage
personas = [
    {"name": "Technical Expert", "description": "Deep technical knowledge, precise"},
    {"name": "Business Analyst", "description": "Focuses on business impact and ROI"},
    {"name": "End User", "description": "Simple, practical explanation"}
]

answers = generate_multi_persona(user_query, context, personas)
```

**When to Use**:
- Executive briefings (different stakeholder views)
- Technical vs. non-technical audiences
- Comprehensive analysis from multiple angles
- Educational applications

---

## Evaluation Patterns

### 1. RAGAS Evaluation
**Pattern**: Use the RAGAS framework to evaluate RAG quality across multiple dimensions

**Metrics**:
```
RAGAS Metrics:
1. Faithfulness: Does the answer contain hallucinations? (0-1)
2. Answer Relevance: Does the answer directly address the question? (0-1)
3. Context Relevance: Are the retrieved contexts relevant to the question? (0-1)
4. Context Recall: Does the context contain all necessary information? (0-1)
5. Context Precision: Are all retrieved contexts relevant? (0-1)
6. Answer Correctness: Is the answer factually correct? (0-1)
7. Answer Semantic Similarity: Is the answer semantically similar to reference? (0-1)
```

**Implementation**:
```python
def evaluate_ragas(question, answer, context, reference_answer=None):
    """
    Evaluate RAG response using RAGAS metrics.
    """
    # Faithfulness: Check for hallucinations
    faithfulness = evaluator.llm.evaluate(
        prompt=f"""
        Determine if the following answer contains any information that
        is NOT supported by the provided context.
        
        Context: {context}
        Answer: {answer}
        
        Faithfulness score (0-1, where 1 means no hallucinations):
        """
    )
    
    # Answer Relevance: Does answer address the question?
    answer_relevance = evaluator.llm.evaluate(
        prompt=f"""
        Determine if the following answer directly addresses the question.
        
        Question: {question}
        Answer: {answer}
        
        Answer Relevance score (0-1):
        """
    )
    
    # Context Relevance: Are contexts relevant to question?
    context_relevance = evaluator.llm.evaluate(
        prompt=f"""
        For each retrieved context, determine if it is relevant to the question.
        Calculate the average relevance score.
        
        Question: {question}
        Contexts: {context}
        
        Context Relevance score (0-1):
        """
    )
    
    # Context Recall: Does context contain all needed info?
    if reference_answer:
        context_recall = evaluator.llm.evaluate(
            prompt=f"""
            Determine if the retrieved context contains all information needed
            to generate the reference answer.
            
            Question: {question}
            Context: {context}
            Reference Answer: {reference_answer}
            
            Context Recall score (0-1):
            """
        )
    
    # Combine into final score
    ragas_score = {
        "faithfulness": faithfulness,
        "answer_relevance": answer_relevance,
        "context_relevance": context_relevance,
        "context_recall": context_recall if reference_answer else None,
        "overall": (faithfulness + answer_relevance + context_relevance + 
                   (context_recall if reference_answer else 0)) / 
                  (4 if reference_answer else 3)
    }
    
    return ragas_score
```

**When to Use**:
- Production RAG systems
- Continuous improvement
- Quality assurance
- Benchmarking different configurations

---

### 2. Human-in-the-Loop Evaluation
**Pattern**: Incorporate human feedback to improve evaluation and RAG quality

**Implementation**:
```python
class HumanInTheLoopEvaluator:
    def __init__(self):
        self.feedback_log = []
    
    def evaluate_with_human(self, question, answer, context):
        """
        Evaluate with human feedback.
        """
        # First, get automated evaluation
        auto_score = self.auto_evaluate(question, answer, context)
        
        # Request human feedback
        human_feedback = self.request_human_feedback(
            question, answer, context, auto_score
        )
        
        # Log feedback
        self.feedback_log.append({
            "question": question,
            "answer": answer,
            "context": context,
            "auto_score": auto_score,
            "human_feedback": human_feedback
        })
        
        # Use feedback to improve future evaluations
        self.update_evaluator(human_feedback)
        
        return {"auto": auto_score, "human": human_feedback}
    
    def request_human_feedback(self, question, answer, context, auto_score):
        """
        Request human feedback on RAG response.
        """
        # Present to human evaluator
        feedback = {
            "correctness": input("Is the answer correct? (1-5)"),
            "relevance": input("Is the answer relevant? (1-5)"),
            "completeness": input("Is the answer complete? (1-5)"),
            "clarity": input("Is the answer clear? (1-5)"),
            "sources": input("Are the sources appropriate? (1-5)"),
            "comments": input("Additional comments:")
        }
        
        return feedback
```

**When to Use**:
- High-stakes applications
- When automated evaluation isn't sufficient
- Continuous learning from human feedback
- Quality improvement iterations

---

### 3. A/B Testing Pattern
**Pattern**: Compare two different RAG configurations to determine which performs better

**Implementation**:
```python
class ABTester:
    def __init__(self, config_a, config_b):
        self.config_a = config_a  # First RAG configuration
        self.config_b = config_b  # Second RAG configuration
    
    def run_test(self, test_queries, metric="overall"):
        """
        Run A/B test on a set of queries.
        """
        results = {"a": [], "b": []}
        
        for query in test_queries:
            # Get answer from config A
            answer_a = self.config_a.query(query)
            score_a = self.evaluate(query, answer_a)
            results["a"].append(score_a)
            
            # Get answer from config B
            answer_b = self.config_b.query(query)
            score_b = self.evaluate(query, answer_b)
            results["b"].append(score_b)
        
        # Calculate average scores
        avg_a = sum(results["a"]) / len(results["a"])
        avg_b = sum(results["b"]) / len(results["b"])
        
        # Determine winner
        if avg_a > avg_b:
            winner = "a"
        else:
            winner = "b"
        
        return {
            "config_a_avg": avg_a,
            "config_b_avg": avg_b,
            "winner": winner,
            "all_results": results
        }
```

**When to Use**:
- Comparing different RAG architectures
- Tuning parameters (chunk size, top-k, etc.)
- Testing different models or embedding approaches
- Continuous improvement through experimentation

---

## Anti-Patterns to Avoid

### 1. Dump-and-Generate
**Anti-Pattern**: Retrieving massive amounts of context and hoping the LLM will figure it out.

**Why It's Bad**:
- Exceeds context window limits
- Confuses the LLM with irrelevant information
- Increases latency and cost
- Poor quality answers

**Better Approach**:
- Retrieve only the most relevant chunks
- Use reranking to select top results
- Filter by metadata (date, source, etc.)
- Implement context trimming

---

### 2. One-Size-Fits-All Chunking
**Anti-Pattern**: Using the same chunking strategy for all document types.

**Why It's Bad**:
- Different documents have different structures
- Technical docs need different handling than natural text
- Code needs different handling than prose

**Better Approach**:
- Use document-type-specific chunking strategies
- Experiment with different chunk sizes and overlaps
- Consider hierarchical or semantic chunking

---

### 3. Ignoring Evaluation
**Anti-Pattern**: Deploying RAG without measuring quality.

**Why It's Bad**:
- No way to know if RAG is actually helping
- No way to detect when RAG degrades
- No way to improve the system

**Better Approach**:
- Implement evaluation from day one
- Track key metrics (accuracy, relevance, latency, cost)
- Set up continuous evaluation
- Use both automated and human evaluation

---

### 4. Static RAG
**Anti-Pattern**: Building a RAG system that doesn't update or learn.

**Why It's Bad**:
- Documents become outdated
- Knowledge doesn't evolve with new information
- Misses opportunity to improve over time

**Better Approach**:
- Implement document update mechanisms
- Set up periodic re-indexing
- Capture user feedback for improvement
- Monitor for document freshness

---

### 5. No Security Considerations
**Anti-Pattern**: Building RAG without security protections.

**Why It's Bad**:
- Vulnerable to prompt injection
- May leak sensitive information
- Can be used for malicious purposes
- Compliance violations

**Better Approach**:
- Implement input sanitization
- Validate retrieved documents
- Filter outputs for sensitive information
- Set up monitoring for abuse

---

### 6. Over-Engineering
**Anti-Pattern**: Building unnecessarily complex RAG when simple would suffice.

**Why It's Bad**:
- Increased development time
- Higher maintenance burden
- More failure modes
- Unnecessary cost and latency

**Better Approach**:
- Start with Naive RAG for proof of concept
- Only add complexity when needed
- Measure the value of each added component
- Keep it simple until complexity is justified

---

## Best Practices

### Document Processing Best Practices
1. **Start with clean documents**: Garbage in, garbage out
2. **Preserve structure**: Maintain document hierarchy where possible
3. **Use overlapping chunks**: Prevents information loss at boundaries
4. **Add meaningful metadata**: Source, date, author, document type
5. **Filter out noise**: Remove headers, footers, boilerplate text
6. **Handle multi-modal**: Text is just the beginning (images, tables, diagrams)
7. **Track provenance**: Know where each chunk came from

### Retrieval Best Practices
1. **Use hybrid search**: Combine vector + keyword for best results
2. **Implement reranking**: Retrieve many, rank the best
3. **Filter by metadata**: Use date, source, type filters
4. **Handle no results**: Provide graceful degradation
5. **Deduplicate**: Remove redundant or near-duplicate chunks
6. **Diversify**: Ensure result diversity
7. **Cache frequent queries**: Improve performance and reduce cost

### Generation Best Practices
1. **Always cite sources**: Traceability is critical
2. **Indicate confidence**: Be honest about uncertainty
3. **Handle missing info**: Don't hallucinate; say when you don't know
4. **Format consistently**: Use templates for predictable output
5. **Limit length**: Stay within context windows
6. **Use personas**: Adapt to different user types
7. **Provide explanations**: Help users understand the reasoning

### Evaluation Best Practices
1. **Start with evaluation**: Build it in from the beginning
2. **Use multiple metrics**: No single metric tells the whole story
3. **Track over time**: Monitor for degradation or improvement
4. **Compare configurations**: A/B test different approaches
5. **Incorporate humans**: Use human feedback for continuous learning
6. **Set targets**: Define what "good" looks like
7. **Alert on degradation**: Get notified when quality drops

### Deployment Best Practices
1. **Start small**: Proof of concept before production
2. **Monitor everything**: Latency, quality, cost, errors
3. **Set budgets**: Token usage, API costs, infrastructure costs
4. **Implement caching**: Reduce redundant computations
5. **Plan for updates**: Document update procedures
6. **Have rollback**: Be able to revert to previous version
7. **Document everything**: Architecture, configurations, decisions

## Tooling Integration

- **Vector Databases**: Pinecone, Weaviate, Qdrant, Milvus, Chroma, FAISS, pgvector
- **Embedding Models**: OpenAI text-embedding, Mistral embeddings, Hugging Face, local models
- **LLMs**: Mistral, OpenAI, Anthropic, local models (vLLM, Ollama)
- **Evaluation**: RAGAS, TruLens, custom evaluation suites
- **Monitoring**: Prometheus, Grafana, custom dashboards
- **Document Processing**: Unstructured, LangChain, LlamaIndex, custom parsers

## Verbosity

verbosity: V2
