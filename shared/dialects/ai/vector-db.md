---
type: pattern
family: ai
---

# Vector Database Contract

Attaches to any work using **vector databases** for similarity search, nearest neighbor retrieval, or semantic indexing. This contract establishes **standard vector database specifications, selection criteria, and deployment patterns** across providers. Loads alongside the embedding model dialect and any RAG system contracts.

Vector databases **store and index embedding vectors** for efficient similarity search. The choice of vector database directly impacts retrieval quality, system performance, operational costs, and scalability. A well-chosen vector database can handle millions of vectors with millisecond latency; a poorly chosen one can become the bottleneck of your entire system.

## The Discipline

Vector database selection is **not just picking the most popular option** — it's a **system design decision** that must consider your specific use case, scale, performance requirements, and compliance constraints. The discipline requires:

- **Search is the bottleneck**: Vector search latency directly impacts user experience
- **Scale compounds**: 1M vectors is easy; 100M vectors requires careful design
- **Accuracy vs speed**: Exact search is accurate but slow; approximate search is fast but may miss results
- **Hybrid search matters**: Combining vector + keyword search improves recall
- **Filtering is essential**: Metadata filtering reduces search space and improves relevance
- **Memory is finite**: Vector dimensions and count determine hardware requirements

- **Indexing is an art**: The right index for your data can be 100x faster
- **Hardware matters**: GPUs accelerate vector search dramatically
- **Cloud vs self-hosted**: Managed services reduce ops overhead but may limit flexibility
- **Compliance is mandatory**: European deployments must respect data residency

## Vector Database Providers

### 1. Pinecone
**Contract**: Managed vector database service

**Specifications**:
```
Provider: Pinecone Systems
Deployment: Managed cloud service
Supported Indexes:
  - Approximate Nearest Neighbor (ANN): HNSW, Pod-based
  - Hybrid: Vector + metadata filtering
Vector Dimensions: Up to 20,000
Max Vectors: Billions (scale with pods)
Latency: ~10-100ms (p99)
Throughput: 100-1000+ QPS (depending on pod type)
```

**Pod Types**:
```
┌─────────────┬─────────────┬──────────────┬─────────────┐
│ Pod Type     │ Vectors/Pod │ Memory (GB)   │ Price/Month  │
├─────────────┼─────────────┼──────────────┼─────────────┤
│ p1.x1 (free) │ 100K        │ 0.5           │ Free         │
│ p1.x1        │ 100K        │ 0.5           │ $15          │
│ p1.x2        │ 500K        │ 2             │ $70          │
│ p1.x4        │ 1M          │ 4             │ $140         │
│ p1.x8        │ 2M          │ 8             │ $280         │
│ p2.x1        │ 100K        │ 1             │ $29          │
│ p2.x2        │ 500K        │ 4             │ $135         │
│ p2.x4        │ 1M          │ 8             │ $270         │
│ p2.x8        │ 2M          │ 16            │ $540         │
│ p2.x16       │ 4M          │ 32            │ $1080        │
└─────────────┴─────────────┴──────────────┴─────────────┘
```

**Capability Profile**:
| Capability | Score | Notes |
|-----------|-------|-------|
| ANN Search Quality | ★★★★★ | Excellent recall with HNSW |
| Filtering | ★★★★★ | Full metadata filtering |
| Hybrid Search | ★★★★★ | Vector + keyword + metadata |
| Scalability | ★★★★★ | Horizontal scaling with pods |
| Managed Service | ★★★★★ | Fully managed, no ops |
| Latency | ★★★★☆ | ~50-100ms typical |
| Cost Efficiency | ★★★☆☆ | Expensive at scale |
| EU Deployment | ❌ | US-based only (no EU data centers) |
| Self-Hosting | ❌ | Managed only |

**Strengths**:
- Fully managed service (no infrastructure to manage)
- Excellent search quality with HNSW
- Strong filtering capabilities
- Horizontal scaling (add pods as needed)
- Hybrid search (vector + keyword)
- Free tier for development
- Good documentation and SDKs

**Weaknesses**:
- ❌ **Non-EU deployment**: All Pinecone services are US-based
- Expensive at scale (pod-based pricing)
- Limited customization
- No self-hosting option
- Vendor lock-in

**European Data Residency**: ❌ **Not compliant** - All data stored and processed in US data centers. For EU data, must use alternative providers.

**Use Cases**:
- ✅ US-based applications
- ✅ Rapid prototyping
- ✅ Production systems where EU compliance is not required
- ❌ European applications with GDPR requirements

---

### 2. Weaviate
**Contract**: Open-source and managed vector database

**Specifications**:
```
Provider: Weaviate BV (SeMI Technologies)
Deployment: Open-source (self-hosted) or managed cloud
Supported Indexes:
  - HNSW (default)
  - Brute Force (exact)
  - Dynamic indexing (auto-selects based on data)
Vector Dimensions: Up to 16,384
Max Vectors: Billions (sharded)
Latency: ~10-50ms (p99, with filtering)
Throughput: 100-1000+ QPS (depending on hardware)
```

**Managed Service (Weaviate Cloud)**:
```
┌──────────────┬─────────────┬──────────────┬─────────────┐
│ Plan          │ Vectors      │ Price/Month   │ Region       │
├──────────────┼─────────────┼──────────────┼─────────────┤
│ Sandbox       │ 100K        │ Free          │ US/EU        │
│ Startup       │ 1M          │ $49           │ US/EU        │
│ Growth        │ 10M         │ $199          │ US/EU        │
│ Scale         │ 100M        │ $999          │ US/EU        │
│ Enterprise    │ Custom      │ Custom        │ US/EU/Other  │
└──────────────┴─────────────┴──────────────┴─────────────┘
```

**Capability Profile**:
| Capability | Score | Notes |
|-----------|-------|-------|
| ANN Search Quality | ★★★★★ | Excellent HNSW implementation |
| Filtering | ★★★★★ | Full metadata filtering with operators |
| Hybrid Search | ★★★★★ | Vector + BM25 + metadata |
| Scalability | ★★★★☆ | Sharding support |
| Managed Service | ★★★★☆ | Weaviate Cloud available |
| Latency | ★★★★★ | Optimized C++ backend, ~10-50ms |
| Cost Efficiency | ★★★★☆ | Good value, especially self-hosted |
| EU Deployment | ✅ | Both self-hosted and managed EU |
| Self-Hosting | ✅ | Open-source, easy to deploy |

**Strengths**:
- Open-source (Apache 2.0 license)
- **EU compliance**: Both self-hosted and managed EU options
- Excellent search quality
- Very fast (C++ backend)
- Strong filtering with complex operators (AND, OR, NOT, >, <, etc.)
- Hybrid search (vector + BM25 keyword)
- GraphQL API (flexible querying)
- Multi-tenancy support
- Automatic indexing (chooses best index type)

**Weaknesses**:
- Self-hosting requires infrastructure management
- Sharding can be complex at scale
- Managed service still maturing
- Smaller community than some alternatives

**European Data Residency**: ✅ **Fully compliant**
- **Self-hosted**: Deploy on any EU cloud provider
- **Managed**: Weaviate Cloud EU regions available (AWS Frankfurt, GCP Netherlands)
- **Certifications**: SOC 2 Type II, ISO 27001

**Use Cases**:
- ✅ European applications requiring GDPR compliance
- ✅ Production systems with filtering requirements
- ✅ Hybrid search applications
- ✅ Self-hosted deployments
- ✅ Multi-tenant applications

---

### 3. Qdrant
**Contract**: Open-source vector similarity search engine

**Specifications**:
```
Provider: Qdrant (by Zilliz)
Deployment: Open-source (self-hosted) or managed (Qdrant Cloud)
Supported Indexes:
  - HNSW (default)
  - Brute Force
  - Product quantization (PQ)
  - Locality-Sensitive Hashing (LSH)
Vector Dimensions: Up to 65,535
Max Vectors: Trillions (distributed)
Latency: ~10-100ms (p99)
Throughput: 100-10000+ QPS (depending on hardware)
```

**Managed Service (Qdrant Cloud)**:
```
┌──────────────┬─────────────┬──────────────┬─────────────┐
│ Plan          │ Vectors      │ Price/Month   │ Region       │
├──────────────┼─────────────┼──────────────┼─────────────┤
│ Free          │ 100K        │ Free          │ US/EU        │
│ Starter       │ 1M          │ $25           │ US/EU        │
│ Professional  │ 10M         │ $250          │ US/EU        │
│ Enterprise    │ 100M+       │ Custom        │ US/EU/Other  │
└──────────────┴─────────────┴──────────────┴─────────────┘
```

**Capability Profile**:
| Capability | Score | Notes |
|-----------|-------|-------|
| ANN Search Quality | ★★★★★ | Excellent HNSW + PQ + LSH |
| Filtering | ★★★★★ | Full metadata filtering |
| Hybrid Search | ★★★★☆ | Vector + keyword (with payload) |
| Scalability | ★★★★★ | Distributed architecture |
| Managed Service | ★★★★☆ | Qdrant Cloud available |
| Latency | ★★★★☆ | ~10-100ms typical |
| Cost Efficiency | ★★★★★ | Very cost-effective |
| EU Deployment | ✅ | Both self-hosted and managed EU |
| Self-Hosting | ✅ | Open-source, Rust-based |

**Strengths**:
- Open-source (Apache 2.0 license)
- **EU compliance**: Both self-hosted and managed EU options
- Rust-based (memory-safe, fast, efficient)
- Multiple index types (HNSW, PQ, LSH)
- Distributed architecture (scales to trillions of vectors)
- Excellent filtering
- Product quantization for compression
- Very active development and community
- Good for high-dimensional vectors

**Weaknesses**:
- Self-hosting requires infrastructure
- Smaller ecosystem than some alternatives
- Managed service still maturing

**European Data Residency**: ✅ **Fully compliant**
- **Self-hosted**: Deploy on any EU cloud provider
- **Managed**: Qdrant Cloud EU regions available
- **Performance**: Optimized for EU deployments

**Use Cases**:
- ✅ European applications requiring GDPR compliance
- ✅ High-scale applications (billions of vectors)
- ✅ Production systems with advanced indexing needs
- ✅ Self-hosted deployments
- ✅ High-dimensional embeddings

---

### 4. Milvus / Zilliz Cloud
**Contract**: Open-source vector database (Milvus) with managed service (Zilliz Cloud)

**Specifications**:
```
Provider: Zilliz
Deployment: Open-source (Milvus) or managed (Zilliz Cloud)
Supported Indexes:
  - HNSW
  - IVF (Inverted File Index)
  - IVF_PQ (IVF + Product Quantization)
  - IVF_SQ8 (IVF + Scalar Quantization)
  - Rhs (Random Projection Hashing)
  - ANNOY (Approximate Nearest Neighbors Oh Yeah)
  - FAISS (by Facebook)
Vector Dimensions: Up to 32,768
Max Vectors: Trillions (distributed)
Latency: ~10-200ms (p99, depending on index)
Throughput: 100-10000+ QPS
```

**Managed Service (Zilliz Cloud)**:
```
┌──────────────┬─────────────┬──────────────┬─────────────┐
│ Plan          │ Vectors      │ Price/Month   │ Region       │
├──────────────┼─────────────┼──────────────┼─────────────┤
│ Free          │ 10GB storage │ Free          │ US/EU/APAC   │
│ Standard      │ Custom       │ $0.10/GB      │ US/EU/APAC   │
│ Enterprise    │ Custom       │ Custom        │ All regions  │
└──────────────┴─────────────┴──────────────┴─────────────┘
```

**Capability Profile**:
| Capability | Score | Notes |
|-----------|-------|-------|
| ANN Search Quality | ★★★★★ | Multiple index types, including FAISS |
| Filtering | ★★★★☆ | Good filtering with some limitations |
| Hybrid Search | ★★★★☆ | Vector + keyword (with plugins) |
| Scalability | ★★★★★ | Distributed, cloud-native |
| Managed Service | ★★★★☆ | Zilliz Cloud available |
| Latency | ★★★★☆ | ~50-200ms typical |
| Cost Efficiency | ★★★★☆ | Storage-based pricing |
| EU Deployment | ✅ | Both self-hosted and managed EU |
| Self-Hosting | ✅ | Open-source Milvus |

**Strengths**:
- Open-source (Apache 2.0 license)
- **EU compliance**: Both self-hosted and managed EU options
- Multiple index types (FAISS, HNSW, IVF, etc.)
- Distributed architecture (scales to trillions)
- Cloud-native design
- Strong ecosystem and community
- Integration with many frameworks
- High availability features

**Weaknesses**:
- Complex setup and configuration
- Steeper learning curve
- Filtering not as mature as Weaviate/Qdrant
- Higher resource requirements
- Managed service pricing can be complex

**European Data Residency**: ✅ **Fully compliant**
- **Self-hosted**: Milvus can be deployed on any EU cloud
- **Managed**: Zilliz Cloud EU regions available (AWS Frankfurt, GCP Netherlands, etc.)
- **Certifications**: SOC 2 Type II, ISO 27001

**Use Cases**:
- ✅ European applications requiring GDPR compliance
- ✅ Large-scale applications (trillions of vectors)
- ✅ Advanced indexing requirements
- ✅ Cloud-native deployments
- ✅ Integration with existing cloud infrastructure

---

### 5. Chroma
**Contract**: Open-source embedding database

**Specifications**:
```
Provider: Chroma
Deployment: Open-source (self-hosted only)
Supported Indexes:
  - HNSW (default)
  - Brute Force
Vector Dimensions: Unlimited
Max Vectors: Millions to billions (single node)
Latency: ~50-200ms (p99)
Throughput: 100-1000 QPS (single node)
```

**Capability Profile**:
| Capability | Score | Notes |
|-----------|-------|-------|
| ANN Search Quality | ★★★★☆ | Good HNSW implementation |
| Filtering | ★★★☆☆ | Basic filtering support |
| Hybrid Search | ❌ | Not available |
| Scalability | ★★★☆☆ | Single node only (no distributed) |
| Managed Service | ❌ | Self-hosted only |
| Latency | ★★★☆☆ | ~50-200ms typical |
| Cost Efficiency | ★★★★★ | Free and open-source |
| EU Deployment | ✅ | Self-hosted on EU infrastructure |
| Self-Hosting | ✅ | Open-source, Python-based |

**Strengths**:
- Open-source (Apache 2.0 license)
- **EU compliance**: Can be self-hosted on EU infrastructure
- Very easy to use (Python-first API)
- Lightweight and simple
- Good for prototyping and small-scale
- Built-in document storage
- Active development

**Weaknesses**:
- No managed service option
- No distributed mode (single node only)
- Limited filtering capabilities
- No hybrid search
- Smaller community than alternatives
- Performance not as optimized as Rust/C++ alternatives

**European Data Residency**: ✅ **Fully compliant when self-hosted in EU**

**Use Cases**:
- ✅ Prototyping and development
- ✅ Small-scale production (<10M vectors)
- ✅ Python-based applications
- ✅ Simple deployments
- ❌ Large-scale applications (no distributed mode)

---

### 6. Postgres (pgvector)
**Contract**: PostgreSQL extension for vector search

**Specifications**:
```
Provider: Neon Labs / Supabase / Self-hosted PostgreSQL
Deployment: Extension on PostgreSQL 11+
Supported Indexes:
  - HNSW (via pgvector)
  - IVF (via pgvector)
  - Brute Force
Vector Dimensions: Up to 2000 (HNSW), unlimited (brute force)
Max Vectors: Limited by PostgreSQL storage
Latency: ~10-100ms (p99)
Throughput: 100-1000+ QPS
```

**Managed Services**:
```
┌──────────────┬─────────────┬──────────────┬─────────────┐
│ Provider       │ Plan          │ Price/Month   │ Region       │
├──────────────┼─────────────┼──────────────┼─────────────┤
│ Neon          │ Free          │ Free          │ US/EU        │
│ Neon          │ Pro           │ $19+          │ US/EU        │
│ Supabase      │ Free          │ Free          │ US/EU        │
│ Supabase      │ Pro           │ $25+          │ US/EU        │
│ AWS RDS       │ Custom        │ Custom        │ All regions  │
└──────────────┴─────────────┴──────────────┴─────────────┘
```

**Capability Profile**:
| Capability | Score | Notes |
|-----------|-------|-------|
| ANN Search Quality | ★★★★☆ | Good HNSW implementation |
| Filtering | ★★★★★ | Full SQL filtering (WHERE clauses) |
| Hybrid Search | ★★★★☆ | Vector + full SQL capabilities |
| Scalability | ★★★☆☆ | Limited by PostgreSQL scaling |
| Managed Service | ★★★★☆ | Multiple providers |
| Latency | ★★★★☆ | ~10-100ms typical |
| Cost Efficiency | ★★★★★ | Uses existing Postgres infrastructure |
| EU Deployment | ✅ | Multiple EU hosting options |
| Self-Hosting | ✅ | Self-hosted PostgreSQL + pgvector |

**Strengths**:
- **EU compliance**: Multiple EU hosting options (Neon EU, Supabase EU, self-hosted)
- Uses existing PostgreSQL infrastructure
- Full SQL capabilities for filtering
- ACID transactions
- Strong consistency guarantees
- Mature ecosystem and tooling
- Easy integration with existing apps
- Backups and point-in-time recovery

**Weaknesses**:
- Limited by PostgreSQL scaling (vertical scaling only)
- HNSW index limited to 2000 dimensions
- Higher memory usage
- Requires PostgreSQL expertise
- Not optimized for pure vector workloads

**European Data Residency**: ✅ **Fully compliant**
- **Neon**: EU regions available (AWS Frankfurt)
- **Supabase**: EU regions available
- **Self-hosted**: Can deploy on any EU infrastructure

**Use Cases**:
- ✅ European applications with existing Postgres infrastructure
- ✅ Applications needing ACID transactions
- ✅ Small to medium scale (<100M vectors)
- ✅ Applications needing strong filtering (SQL WHERE clauses)
- ✅ Integration with existing data pipelines

---

### 7. Redis (Redis Stack)
**Contract**: In-memory data store with vector search capabilities

**Specifications**:
```
Provider: Redis / Redis Stack
Deployment: Self-hosted or managed (Redis Cloud)
Supported Indexes:
  - HNSW (via RediSearch module)
  - Flat (brute force)
Vector Dimensions: Up to 1000 (HNSW)
Max Vectors: Limited by memory (millions to billions)
Latency: ~1-10ms (p99, in-memory)
Throughput: 10,000-100,000+ QPS
```

**Managed Service (Redis Cloud)**:
```
┌──────────────┬─────────────┬──────────────┬─────────────┐
│ Plan          │ Memory       │ Price/Month   │ Region       │
├──────────────┼─────────────┼──────────────┼─────────────┤
│ Free          │ 30MB         │ Free          │ US/EU        │
│ Standard      │ 1GB-12GB     │ $50-$600      │ US/EU        │
│ Pro           │ 12GB-1TB     │ Custom        │ US/EU        │
└──────────────┴─────────────┴──────────────┴─────────────┘
```

**Capability Profile**:
| Capability | Score | Notes |
|-----------|-------|-------|
| ANN Search Quality | ★★★★☆ | Good for in-memory use cases |
| Filtering | ★★★★☆ | Good filtering with RediSearch |
| Hybrid Search | ★★★☆☆ | Vector + text (with RediSearch) |
| Scalability | ★★★★☆ | Horizontal scaling with Redis Cluster |
| Managed Service | ★★★★☆ | Redis Cloud available |
| Latency | ★★★★★ | Sub-millisecond (in-memory) |
| Cost Efficiency | ★★★☆☆ | Memory-intensive |
| EU Deployment | ✅ | Managed and self-hosted EU options |
| Self-Hosting | ✅ | Self-hosted Redis Stack |

**Strengths**:
- **Ultra-low latency**: Sub-millisecond response times
- **EU compliance**: Redis Cloud EU regions available, self-hosted EU possible
- In-memory performance
- Full Redis capabilities (caching, pub/sub, etc.)
- Horizontal scaling with Redis Cluster
- Mature ecosystem and tooling

**Weaknesses**:
- Memory-intensive (all data in memory)
- Limited to 1000 dimensions for HNSW
- Higher cost at scale
- Complexity in distributed mode
- Data persistence trade-offs (memory vs disk)

**European Data Residency**: ✅ **Fully compliant**
- **Redis Cloud**: EU regions available
- **Self-hosted**: Can deploy on any EU infrastructure

**Use Cases**:
- ✅ Applications requiring ultra-low latency (<10ms)
- ✅ Caching layer for vector search
- ✅ Real-time applications
- ✅ Applications already using Redis
- ✅ High-throughput scenarios

---

### 8. Elasticsearch (Vector Search)
**Contract**: Distributed search engine with vector search capabilities

**Specifications**:
```
Provider: Elastic
Deployment: Self-hosted or managed (Elastic Cloud)
Supported Indexes:
  - HNSW (default)
  - Brute Force
Vector Dimensions: Up to 32,768
Max Vectors: Limited by cluster storage
Latency: ~10-100ms (p99)
Throughput: 100-10000+ QPS
```

**Managed Service (Elastic Cloud)**:
```
┌──────────────┬─────────────┬──────────────┬─────────────┐
│ Plan          │ Storage      │ Price/Month   │ Region       │
├──────────────┼─────────────┼──────────────┼─────────────┤
│ Trial         │ 5GB          │ Free          │ US/EU        │
│ Standard      │ 10GB-1TB     │ $95-$9600     │ US/EU        │
│ Gold          │ 1TB+         │ Custom        │ US/EU        │
└──────────────┴─────────────┴──────────────┴─────────────┘
```

**Capability Profile**:
| Capability | Score | Notes |
|-----------|-------|-------|
| ANN Search Quality | ★★★★☆ | Good HNSW implementation |
| Filtering | ★★★★★ | Full Elasticsearch query DSL |
| Hybrid Search | ★★★★★ | Vector + full-text + structured |
| Scalability | ★★★★★ | Distributed, cloud-native |
| Managed Service | ★★★★☆ | Elastic Cloud available |
| Latency | ★★★★☆ | ~10-100ms typical |
| Cost Efficiency | ★★★☆☆ | Resource-intensive |
| EU Deployment | ✅ | Managed and self-hosted EU options |
| Self-Hosting | ✅ | Self-hosted Elasticsearch |

**Strengths**:
- **EU compliance**: Elastic Cloud EU regions available, self-hosted EU possible
- Full-text search capabilities
- Strong filtering (Elasticsearch query DSL)
- Distributed architecture
- Mature ecosystem and tooling
- Strong analytics capabilities
- Kibana integration for visualization

**Weaknesses**:
- Resource-intensive (requires significant CPU/RAM)
- Complex setup and configuration
- Steeper learning curve
- Higher operational overhead
- Expensive at scale

**European Data Residency**: ✅ **Fully compliant**
- **Elastic Cloud**: EU regions available (multiple EU data centers)
- **Self-hosted**: Can deploy on any EU infrastructure
- **Certifications**: SOC 2, ISO 27001, etc.

**Use Cases**:
- ✅ Applications needing both vector and full-text search
- ✅ Analytics and visualization (Kibana)
- ✅ Large-scale distributed deployments
- ✅ Applications already using Elasticsearch
- ✅ Complex filtering requirements

## Selection Criteria

### Decision Framework

Use this **weighted scoring matrix** to select the optimal vector database:

```
Score each provider (1-5) on each criterion:
1 = Poor, 2 = Below Average, 3 = Average, 4 = Above Average, 5 = Excellent

Criteria:
┌─────────────────────────┬──────────┬─────────────────────────────────────┐
│ Criterion                │ Weight   │ Description                             │
├─────────────────────────┼──────────┼─────────────────────────────────────┤
│ Search Quality           │ 25%      │ Retrieval accuracy and recall         │
│ EU Compliance            │ 25%      │ Data residency and privacy            │
│ Latency                  │ 20%      │ End-to-end search time                │
│ Scalability               │ 15%      │ Ability to handle growth              │
│ Filtering                │ 10%      │ Metadata filtering capabilities        │
│ Cost                     │ 5%       │ Total cost of ownership               │
└─────────────────────────┴──────────┴─────────────────────────────────────┘

Weighted Score = Σ(score × weight)
```

### Quick Selection Guide

| Use Case | Recommended | Alternative | Notes |
|----------|-------------|-------------|-------|
| **Production RAG (EU, <10M vectors)** | Weaviate | Qdrant | Best balance of quality, compliance, features |
| **Production RAG (EU, >10M vectors)** | Qdrant | Milvus | Best scalability for EU |
| **Production RAG (US, <10M vectors)** | Pinecone | Weaviate | Managed service with good features |
| **Production RAG (US, >10M vectors)** | Pinecone | Weaviate | Scalable managed service |
| **Ultra-low Latency** | Redis | Qdrant | Sub-millisecond response times |
| **Full-text + Vector** | Elasticsearch | Postgres | Best hybrid search |
| **Existing Postgres** | Postgres (pgvector) | Weaviate | Leverage existing infrastructure |
| **Existing Elasticsearch** | Elasticsearch | Qdrant | Use what you already have |
| **Prototyping** | Chroma | Weaviate | Easy to start, Python-first |
| **Self-hosted Only** | Qdrant | Milvus | Best open-source options |
| **Managed Only** | Pinecone | Weaviate Cloud | No infrastructure management |
| **Cost-Sensitive** | Qdrant | Postgres | Most cost-effective options |
| **Maximum Scalability** | Milvus | Qdrant | Scales to trillions of vectors |

### EU-Compliant Recommendations

For **European deployments requiring GDPR compliance**, these are the top recommendations:

#### 1. Weaviate (Best Overall for EU)
**Why**:
- Open-source with managed EU option
- Excellent search quality and filtering
- Fast (C++ backend)
- Strong EU presence
- Hybrid search capabilities

**Deployment Options**:
- Self-hosted on OVHcloud, T-Systems, Scaleway
- Weaviate Cloud EU (AWS Frankfurt, GCP Netherlands)

**Pricing**:
- Self-hosted: Only infrastructure costs
- Managed: $49-$999/month (1M-100M vectors)

#### 2. Qdrant (Best for Scale)
**Why**:
- Open-source with managed EU option
- Excellent scalability (trillions of vectors)
- Multiple index types (HNSW, PQ, LSH)
- Rust-based (fast, memory-efficient)

**Deployment Options**:
- Self-hosted on any EU cloud
- Qdrant Cloud EU

**Pricing**:
- Self-hosted: Only infrastructure costs
- Managed: $25-$250/month (1M-10M vectors)

#### 3. Milvus / Zilliz Cloud (Best for Advanced Indexing)
**Why**:
- Open-source with managed EU option
- Multiple index types (FAISS, HNSW, IVF, etc.)
- Distributed architecture
- Cloud-native design

**Deployment Options**:
- Self-hosted (Milvus) on any EU cloud
- Zilliz Cloud EU (AWS Frankfurt, GCP Netherlands, etc.)

**Pricing**:
- Self-hosted: Only infrastructure costs
- Managed: $0.10/GB/month (storage-based)

#### 4. Postgres + pgvector (Best for Existing Postgres)
**Why**:
- Uses existing Postgres infrastructure
- Full SQL capabilities
- ACID transactions
- Multiple EU hosting options

**Deployment Options**:
- Neon EU (AWS Frankfurt)
- Supabase EU
- Self-hosted Postgres on EU cloud

**Pricing**:
- Managed: $19-$25+/month
- Self-hosted: Only infrastructure costs

## Index Types Explained

### 1. Brute Force (Exact Search)
**Algorithm**: Compare query vector against all database vectors
**Accuracy**: 100% (guaranteed to find exact nearest neighbors)
**Performance**: O(n) - Linear time, slow for large datasets
**Memory**: High (stores all vectors)
**When to Use**: Small datasets (<10K vectors), need 100% accuracy

```
Pros:
- Guaranteed accuracy
- Simple implementation
- No index maintenance

Cons:
- Slow for large datasets
- High memory usage
- Doesn't scale
```

### 2. HNSW (Hierarchical Navigable Small World)
**Algorithm**: Graph-based approximate nearest neighbor search
**Accuracy**: 95-99% (configurable)
**Performance**: O(log n) - Very fast, even for large datasets
**Memory**: Medium (graph structure overhead)
**When to Use**: Most applications (default choice)

```
Parameters:
- M: Number of bidirectional links (higher = more accurate, more memory)
- efConstruction: Construction time parameter (higher = better quality, slower build)
- efSearch: Search time parameter (higher = better recall, slower search)

Typical Values:
- M = 16-64 (default: 16)
- efConstruction = 100-500 (default: 200)
- efSearch = 10-100 (default: 50)
```

**Pros**:
- Excellent accuracy/performance trade-off
- Works well for most use cases
- Memory-efficient
- Fast construction

**Cons**:
- Approximate (not exact)
- Graph construction time for large datasets
- Memory overhead for graph structure

### 3. IVF (Inverted File Index)
**Algorithm**: Partitions vectors into clusters, search only relevant clusters
**Accuracy**: 80-95% (configurable via nprobe)
**Performance**: O(nprobe) - Very fast for appropriate nprobe
**Memory**: Low (only stores cluster centers + inverted lists)
**When to Use**: Large datasets with natural clustering

```
Parameters:
- nlist: Number of clusters (higher = more clusters, more memory, better accuracy)
- nprobe: Number of clusters to search (higher = better recall, slower)

Typical Values:
- nlist = 100-1000 (based on dataset size)
- nprobe = 10-100 (default: 50)
```

**Pros**:
- Very memory-efficient
- Fast search
- Good for large datasets

**Cons**:
- Lower accuracy than HNSW
- Sensitive to cluster quality
- Requires tuning nlist and nprobe

### 4. IVF_PQ (IVF + Product Quantization)
**Algorithm**: IVF with product quantization for compression
**Accuracy**: 70-90% (configurable)
**Performance**: O(nprobe) - Very fast
**Memory**: Very Low (compressed vectors)
**When to Use**: Very large datasets (100M+ vectors), limited memory

```
Parameters:
- nlist: Number of clusters
- m: Number of sub-vectors (PQ dimension)
- nprobe: Number of clusters to search

Typical Values:
- nlist = 100-1000
- m = 8-64 (divides vector into m sub-vectors)
- nprobe = 10-100
```

**Pros**:
- Extremely memory-efficient (10-100x compression)
- Fast search
- Good for very large datasets

**Cons**:
- Lower accuracy (quantization loss)
- Complex tuning
- Slower index construction

### 5. LSH (Locality-Sensitive Hashing)
**Algorithm**: Hashes vectors into buckets, compares within buckets
**Accuracy**: 60-80% (configurable)
**Performance**: O(1) - Constant time, extremely fast
**Memory**: Low
**When to Use**: Very high-speed requirements, lower accuracy acceptable

```
Parameters:
- ntables: Number of hash tables (higher = better recall, more memory)
- nbits: Number of bits per hash (higher = more buckets, lower recall per table)

Typical Values:
- ntables = 10-100
- nbits = 8-16
```

**Pros**:
- Extremely fast (constant time)
- Low memory usage
- Good for real-time applications

**Cons**:
- Lower accuracy
- Requires tuning
- Not suitable for high-accuracy applications

### 6. ANNOY (Approximate Nearest Neighbors Oh Yeah)
**Algorithm**: Tree-based partitioning with random projections
**Accuracy**: 85-95%
**Performance**: O(log n) - Fast
**Memory**: Medium
**When to Use**: Alternative to HNSW, good for some datasets

```
Parameters:
- n_trees: Number of trees (higher = better accuracy, more memory)
- search_k: Number of nodes to examine (higher = better recall, slower)

Typical Values:
- n_trees = 10-1000
- search_k = 10-1000
```

**Pros**:
- Good accuracy/performance trade-off
- Memory-efficient
- Fast construction

**Cons**:
- Not as widely adopted as HNSW
- Construction can be slow for large datasets

### 7. FAISS (Facebook AI Similarity Search)
**Algorithm**: Multiple implementations (IVF, PQ, HNSW, etc.)
**Accuracy**: 80-99% (depending on configuration)
**Performance**: Very fast (C++ implementation)
**Memory**: Configurable
**When to Use**: Advanced users, specific accuracy/performance needs

**Pros**:
- Multiple index types available
- Highly optimized (C++)
- Good for very large datasets
- GPU acceleration available

**Cons**:
- Complex configuration
- Steeper learning curve
- Limited to FAISS-supported indexes

## Index Selection Guide

```
┌─────────────────────┬─────────────┬─────────────┬──────────────┐
│ Dataset Size         │ Accuracy     │ Speed        │ Recommended   │
├─────────────────────┼─────────────┼─────────────┼──────────────┤
│ < 10K vectors        │ 100%         │ Any          │ Brute Force   │
│ 10K - 100K vectors    │ 99%+         │ Fast         │ HNSW          │
│ 100K - 1M vectors     │ 95-99%       │ Fast         │ HNSW          │
│ 1M - 10M vectors      │ 90-95%       │ Very Fast    │ HNSW          │
│ 10M - 100M vectors    │ 85-95%       │ Very Fast    │ HNSW or IVF_PQ│
│ 100M - 1B vectors     │ 80-90%       │ Extremely Fast│ IVF_PQ        │
│ > 1B vectors          │ 70-85%       │ Extremely Fast│ IVF_PQ or LSH  │
└─────────────────────┴─────────────┴─────────────┴──────────────┘
```

## Performance Optimization

### 1. Index Parameter Tuning

**HNSW Tuning**:
```
# For better accuracy (at cost of memory and speed)
M = 64              # More connections in graph
EFConstruction = 500 # More thorough construction
EFSearch = 100      # More thorough search

# For better speed (at cost of accuracy)
M = 16              # Fewer connections
EFConstruction = 100 # Faster construction
EFSearch = 10       # Faster search
```

**IVF_PQ Tuning**:
```
# For better accuracy (at cost of memory and speed)
nlist = 1000        # More clusters
m = 8              # Fewer sub-vectors (less compression)
nprobe = 100       # Search more clusters

# For better memory efficiency (at cost of accuracy)
nlist = 100         # Fewer clusters
m = 64             # More sub-vectors (more compression)
nprobe = 10        # Search fewer clusters
```

### 2. Hardware Optimization

**Memory Requirements**:
```
# Storage per vector (approximate)
┌─────────────────┬────────────┬────────────┐
│ Dimensions       │ Float32     │ Float16     │
├─────────────────┼────────────┼────────────┤
│ 384              │ 1.5 KB      │ 768 bytes   │
│ 768              │ 3 KB        │ 1.5 KB      │
│ 1024             │ 4 KB        │ 2 KB        │
│ 1536             │ 6 KB        │ 3 KB        │
│ 2048             │ 8 KB        │ 4 KB        │
└─────────────────┴────────────┴────────────┘

# Total memory for 1M vectors:
1M × 1536d × 4 bytes = 6 GB (float32)
1M × 1536d × 2 bytes = 3 GB (float16)
```

**Hardware Recommendations**:
```
┌─────────────────┬─────────────┬─────────────┬─────────────────┐
│ Vectors          │ Dimensions   │ RAM Required │ Recommended      │
├─────────────────┼─────────────┼─────────────┼─────────────────┤
│ 1M               │ 1536         │ 6 GB         │ 8 GB RAM         │
│ 10M              │ 1536         │ 60 GB        │ 64 GB RAM        │
│ 100M             │ 1536         │ 600 GB       │ 1 TB RAM or disk │
│ 1B               │ 1536         │ 6 TB         │ Distributed      │
└─────────────────┴─────────────┴─────────────┴─────────────────┘
```

**GPU Acceleration**:
- **FAISS**: Supports GPU acceleration (NVIDIA CUDA)
- **Milvus**: Supports GPU acceleration
- **Weaviate**: GPU support in development
- **Qdrant**: GPU support via plugins

**GPU Requirements**:
```
# For FAISS GPU:
- NVIDIA GPU with CUDA support
- CUDA 11.0+
- cuDNN
- Minimum 8GB VRAM for 1M vectors
- Minimum 32GB VRAM for 10M vectors
```

### 3. Query Optimization

**Filter Pushdown**:
```python
# Bad: Filter after search
results = db.search(query, k=100)
filtered = [r for r in results if r.metadata['category'] == 'engineering']
final = filtered[:10]

# Good: Filter before/during search
results = db.search(
    query,
    k=10,
    filter={'category': 'engineering'}  # Filter pushdown
)
```

**Pre-filtering**:
```python
# Bad: Search all vectors, then filter
results = db.search(query, k=100)

# Good: Pre-filter by metadata first
doc_ids = db.filter_metadata(category='engineering', timestamp > start_date)
results = db.search(query, k=10, doc_ids=doc_ids)
```

**Limit Result Count**:
```python
# Bad: Retrieve too many results
results = db.search(query, k=1000)

# Good: Retrieve only what you need
results = db.search(query, k=10)  # or k=20 for re-ranking
```

### 4. Caching

**Query Caching**:
```python
# Cache frequent queries
query_cache = {}

def search(query, k=10):
    cache_key = hash(query)
    if cache_key in query_cache:
        return query_cache[cache_key]
    
    results = db.search(query, k=k)
    query_cache[cache_key] = results
    return results
```

**Embedding Caching**:
- Cache embeddings for repeated queries
- Cache embeddings for documents (if not already stored)
- Use TTL (time-to-live) for cache entries

### 5. Sharding

**Problem**: Single node can't handle all data

**Solution**: Split data across multiple nodes

```
# Sharding strategies:
1. Random sharding: Distribute vectors randomly
   - Pros: Even distribution
   - Cons: Every query must search all shards

2. Metadata-based sharding: Distribute by metadata value
   - Pros: Queries can target specific shards
   - Cons: Uneven distribution possible

3. Hybrid sharding: Random + metadata
   - Pros: Balance of both approaches
   - Cons: More complex
```

**Sharding in Practice**:
```python
# Query with sharding
results = []
for shard in shards:
    shard_results = shard.search(query, k=local_k)
    results.extend(shard_results)

# Re-rank and deduplicate
final_results = rerank_and_dedup(results, k=10)
```

### 6. Replication

**Problem**: Single point of failure

**Solution**: Replicate data across multiple nodes

```
# Replication strategies:
1. Leader-Follower: One leader handles writes, followers replicate
   - Pros: Simple, consistent
   - Cons: Leader is bottleneck

2. Multi-Leader: Multiple leaders handle writes
   - Pros: Higher write throughput
   - Cons: Conflict resolution needed

3. Full Replication: All nodes have all data
   - Pros: High availability, fast reads
   - Cons: High memory usage
```

## Cost Optimization

### Cost Comparison (1M vectors, 1536d, 10K queries/day)

```
┌─────────────────────────┬──────────────┬──────────────┬──────────────┐
│ Provider                 │ Ingestion    │ Query        │ Monthly Total │
├─────────────────────────┼──────────────┼──────────────┼──────────────┤
│ Pinecone (p1.x2)         │ $70          │ $70          │ $140          │
│ Weaviate Cloud (1M)      │ $49          │ Included     │ $49           │
│ Qdrant Cloud (1M)        │ $25          │ Included     │ $25           │
│ Zilliz Cloud (10GB)      │ ~$10         │ ~$10         │ ~$20          │
│ Self-hosted (8GB RAM)     │ $0*          │ $0*          │ $15-30*       │
│ Self-hosted (32GB RAM)    │ $0*          │ $0*          │ $60-120*      │
└─────────────────────────┴──────────────┴──────────────┴──────────────┘

*Infrastructure costs only (cloud VM pricing)
**Break-even points**:
- Self-hosted vs Managed: ~5M vectors (for typical use)
- Cloud VM vs Managed: Varies by provider and usage
```

### Cost-Saving Checklist

- [ ] Use appropriate index type (IVF_PQ for large datasets)
- [ ] Compress vectors (float16 instead of float32)
- [ ] Use product quantization for storage efficiency
- [ ] Implement query caching
- [ ] Use filtering to reduce search space
- [ ] Right-size your hardware (don't over-provision)
- [ ] Use spot instances for batch operations
- [ ] Archive old/infrequently accessed vectors
- [ ] Monitor usage and set budgets/alerts
- [ ] Consider self-hosting for large-scale deployments

## European Compliance

### GDPR Requirements for Vector Databases

**Key Considerations**:

1. **Personal Data in Vectors**
   - Vectors can contain PII (even if not human-readable)
   - **Mitigation**: Remove PII before embedding or use PII-safe embedding models
   - **Detection**: Regular audits of source data

2. **Data Residency**
   - Vectors must be stored in EU for EU citizens' data
   - **Mitigation**: Use EU-based vector database providers or self-host in EU
   - **Verification**: Audit data center locations regularly

3. **Data Subject Rights**
   - Right to access: Provide vector representations on request
   - Right to erasure: Delete vectors when requested
   - Right to portability: Export vectors in standard format
   - **Mitigation**: Implement robust data management policies

4. **Data Minimization**
   - Only store vectors necessary for the task
   - **Mitigation**: Implement data retention policies
   - **Verification**: Regular audits of stored vectors

5. **Purpose Limitation**
   - Vectors must be used only for stated purposes
   - **Mitigation**: Document vector use cases
   - **Verification**: Access controls and audit logging

6. **Security**
   - Vectors must be protected from unauthorized access
   - **Mitigation**: Encryption at rest and in transit, access controls
   - **Verification**: Regular security audits

### EU-Compliant Vector Database Stack

```
┌─────────────────────────────────────────────────────────────┐
│                        Application Layer                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   User      │  │   RAG        │  │   LLM               │  │
│  │   Interface │  │   System     │  │   (EU-hosted)       │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Vector Database                            │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  EU-Compliant Options:                                       │  │
│  │  - Weaviate (self-hosted on OVHcloud/T-Systems)             │  │
│  │  - Qdrant (self-hosted on any EU cloud)                     │  │
│  │  - Milvus (self-hosted on any EU cloud)                     │  │
│  │  - Postgres + pgvector (Neon EU, Supabase EU, self-hosted)  │  │
│  │  - Weaviate Cloud EU / Qdrant Cloud EU / Zilliz Cloud EU   │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Infrastructure                            │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  EU-Based Cloud Providers:                                  │  │
│  │  - OVHcloud (France, Germany, UK)                           │  │
│  │  - T-Systems (Germany)                                      │  │
│  │  - Scaleway (France, Netherlands, Poland)                   │  │
│  │  - AWS (Frankfurt, Ireland, Stockholm, Paris, Milan)       │  │
│  │  - GCP (Belgium, Netherlands, Germany, UK, Switzerland)   │  │
│  │  - Azure (Germany, Netherlands, UK, France, Switzerland)  │  │
│  │                                                                │  │
│  │  Certifications: ISO 27001, SOC 2, Gaia-X, C5              │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Compliance Checklist

**Provider Selection**:
- [ ] Verify provider has EU data centers
- [ ] Confirm data never leaves EU jurisdiction
- [ ] Check provider certifications (ISO 27001, SOC 2, etc.)
- [ ] Review data processing agreements
- [ ] Verify compliance with Gaia-X principles (if applicable)

**Data Management**:
- [ ] Implement data classification (identify PII)
- [ ] Remove or anonymize PII before embedding
- [ ] Implement data retention policies
- [ ] Enable encryption at rest and in transit
- [ ] Use EU-based key management service
- [ ] Implement access controls (RBAC)

**Operational Controls**:
- [ ] Enable audit logging for all operations
- [ ] Implement backup and disaster recovery
- [ ] Regular security audits
- [ ] Data Protection Impact Assessment (DPIA) for high-risk deployments
- [ ] Appoint Data Protection Officer (DPO) if required

**User Rights**:
- [ ] Implement data subject access request (DSAR) process
- [ ] Enable right to erasure (delete vectors on request)
- [ ] Support data portability (export in standard format)
- [ ] Provide privacy notices

## Deployment Patterns

### 1. Managed Cloud (Recommended for Most)

**Architecture**:
```
User → Application → Weaviate Cloud EU → EU Data Center → Vector Database
```

**Pros**:
- No infrastructure management
- Automatic scaling
- EU compliance built-in
- Regular updates and maintenance
- High availability

**Cons**:
- Ongoing service costs
- Limited customization
- Vendor lock-in risk

**When to Use**:
- Production systems with <100M vectors
- Need EU compliance without infrastructure overhead
- Want to start quickly
- Limited DevOps resources

### 2. Self-Hosted Single Node (Development/Small Scale)

**Architecture**:
```
User → Application → Vector Database (Single Node on EU Cloud)
```

**Pros**:
- Full data control
- No service costs (only infrastructure)
- Complete customization
- Offline capability

**Cons**:
- Infrastructure management overhead
- Limited scalability
- Single point of failure
- Need to handle backups, updates, etc.

**When to Use**:
- Development and testing
- Small-scale production (<10M vectors)
- Air-gapped environments
- Custom requirements

### 3. Self-Hosted Distributed (High Volume)

**Architecture**:
```
User → Load Balancer → [Vector DB Node 1] → Shard 1
                        │
                        ├─ [Vector DB Node 2] → Shard 2
                        │
                        └─ [Vector DB Node 3] → Shard 3
```

**Pros**:
- Horizontal scalability
- High throughput
- Fault tolerance
- Full data control

**Cons**:
- Complex infrastructure
- Higher costs
- Need orchestration (Kubernetes, etc.)
- Operational overhead

**When to Use**:
- High-volume production (>100M vectors)
- Need to process millions of queries/day
- Require low latency at scale
- Mission-critical applications

### 4. Hybrid (Best of Both Worlds)

**Architecture**:
```
User → Application → [Managed for Production] → Vectors
                       │
                       └─ [Self-hosted for Development] → Vectors
```

**Pros**:
- Production-grade managed service
- Development flexibility with self-hosted
- Cost optimization

**Cons**:
- Complex architecture
- Need to manage two systems
- Data synchronization between environments

**When to Use**:
- Mature production systems
- Active development and experimentation
- Cost-conscious organizations

### 5. Multi-Cloud (High Availability)

**Architecture**:
```
User → Load Balancer → [Weaviate on AWS Frankfurt] → Primary
                        │
                        └─ [Qdrant on OVHcloud] → Replica
```

**Pros**:
- High availability across providers
- Disaster recovery
- Avoid vendor lock-in

**Cons**:
- Very complex
- Expensive
- Data synchronization challenges

**When to Use**:
- Mission-critical applications
- Cannot tolerate downtime
- Multi-cloud strategy

## Monitoring and Maintenance

### Key Metrics to Monitor

```
┌─────────────────────────┬──────────────┬─────────────────────────┐
│ Metric                    │ Target        │ Alert Threshold         │
├─────────────────────────┼──────────────┼─────────────────────────┤
│ Search Latency (p95)      │ <50ms         │ >200ms                  │
│ Search Latency (p99)      │ <100ms        │ >500ms                  │
│ Throughput (queries/sec)  │ >100          │ <50                     │
│ Index Build Time          │ <1 hour       │ >4 hours                │
│ Memory Usage              │ <80%          │ >90%                    │
│ Disk Usage                │ <70%          │ >85%                    │
│ Error Rate                │ <0.1%         │ >1%                     │
│ Cache Hit Rate            │ >50%          │ <30%                    │
│ Replication Lag           │ <1s           │ >10s                    │
└─────────────────────────┴──────────────┴─────────────────────────┘
```

### Alerting Rules

```yaml
# Example Prometheus alerting rules
- alert: HighSearchLatency
  expr: histogram_quantile(0.95, vector_search_latency_seconds) > 0.2
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High search latency (p95 > 200ms)"

- alert: CriticalSearchLatency
  expr: histogram_quantile(0.99, vector_search_latency_seconds) > 0.5
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "Critical search latency (p99 > 500ms)"

- alert: HighErrorRate
  expr: rate(vector_search_errors_total[5m]) > 0.01
  labels:
    severity: warning
  annotations:
    summary: "High error rate (>1%)"

- alert: HighMemoryUsage
  expr: vector_db_memory_usage_percent > 90
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "High memory usage (>90%)"

- alert: ReplicationLag
  expr: vector_db_replication_lag_seconds > 10
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High replication lag (>10s)"
```

### Index Maintenance

**Regular Index Optimization**:
```python
# Rebuild index periodically for better performance
if index_quality_score < 0.8:
    db.rebuild_index()

# Optimize index parameters based on data distribution
if data_has_changed_significantly():
    db.optimize_index()
```

**Index Rebuilding Schedule**:
```
┌─────────────────┬─────────────┬─────────────────────────┐
│ Data Size        │ Frequency    │ Notes                    │
├─────────────────┼─────────────┼─────────────────────────┤
│ < 100K vectors    │ Weekly       │ Low overhead             │
│ 100K - 1M vectors │ Bi-weekly    │ Medium overhead           │
│ 1M - 10M vectors  │ Monthly      │ Higher overhead          │
│ > 10M vectors     │ Quarterly    │ Very high overhead       │
└─────────────────┴─────────────┴─────────────────────────┘
```

## Migration Strategies

### From One Database to Another

**Challenges**:
- Different index formats
- Different query APIs
- Need to re-index all vectors
- Potential downtime during migration

**Migration Process**:

```
Phase 1: Preparation (1-2 weeks)
├── Select new vector database
├── Set up new infrastructure
├── Create migration plan
└── Test migration with sample data

Phase 2: Dual Running (2-4 weeks)
├── Run both databases in parallel
├── Write to both databases
├── Compare search results
├── A/B test with users
└── Monitor performance and quality

Phase 3: Cutover (1 week)
├── Migrate all data to new database
├── Update application to use new database
├── Full regression testing
└── Gradual rollout to users

Phase 4: Cleanup (1 week)
├── Verify all data migrated correctly
├── Delete old database
├── Monitor new database performance
└── Update documentation
```

**Migration Tools**:

```python
# Batch migration script
async def migrate_vectors(old_db, new_db, batch_size=10000):
    offset = 0
    while True:
        vectors = old_db.get_vectors(offset, batch_size)
        if not vectors:
            break
        
        # Transform if needed (different dimensions, etc.)
        transformed = [transform(v) for v in vectors]
        
        # Insert into new database
        new_db.insert_vectors(transformed)
        
        offset += batch_size
        print(f"Migrated {offset} vectors")
```

### Index Type Migration

**Problem**: Changing index type requires re-indexing all data

**Solution**: Use blue-green deployment

```python
# Blue-Green migration
# 1. Create new index with new type
new_index = db.create_index(index_type='IVF_PQ', params=params)

# 2. Copy all vectors to new index
for batch in old_index.get_all_vectors():
    new_index.insert(batch)

# 3. Validate new index
if validate_index(new_index):
    # 4. Switch to new index (atomic operation)
    db.switch_index(old_index, new_index)
    
    # 5. Delete old index
    db.delete_index(old_index)
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No filtering | Retrieves irrelevant documents | Always use metadata filtering |
| Retrieving too many results | High latency, high cost | Limit k to what you need |
| Not using index | Brute force search is slow | Always create index for large datasets |
| Wrong index type | Suboptimal performance | Choose index based on data size |
| No monitoring | Can't detect issues | Monitor latency, throughput, errors |
| No backups | Data loss risk | Regular backups and validation |
| No encryption | Security risk | Enable encryption at rest and in transit |
| Hardcoding database in app | Can't change database | Use configuration |
| Not testing with real queries | Synthetic ≠ real | Test with actual user queries |
| Ignoring EU compliance | GDPR violations | Use EU-compliant providers |

## Best Practices

### Pre-Insertion
- [ ] Clean and normalize text before embedding
- [ ] Chunk long documents appropriately
- [ ] Remove PII and sensitive data
- [ ] Generate and store metadata
- [ ] Deduplicate near-identical documents
- [ ] Validate vector dimensions match index

### Insertion
- [ ] Use batching (100-1000 vectors per batch)
- [ ] Handle errors and retries gracefully
- [ ] Implement rate limiting
- [ ] Use async for better throughput
- [ ] Monitor and log all operations
- [ ] Version your vector database

### Querying
- [ ] Always use filtering to reduce search space
- [ ] Limit result count (k=10-20 typically sufficient)
- [ ] Use appropriate index parameters (efSearch, nprobe, etc.)
- [ ] Cache frequent queries
- [ ] Monitor query performance
- [ ] Implement query timeouts

### Operations
- [ ] Set up monitoring and alerting
- [ ] Regularly optimize indexes
- [ ] Monitor storage usage and growth
- [ ] Plan for index rebuilding
- [ ] Test backup and restore procedures
- [ ] Document your vector database configuration
- [ ] Implement disaster recovery plan

## Summary

Vector databases are the **engine of RAG and semantic applications**. The choice of database impacts retrieval quality, performance, scalability, and compliance. For European deployments, **Weaviate, Qdrant, Milvus, or Postgres + pgvector** provide the best combinations of performance, features, and EU compliance.

**Key Takeaways**:

1. **Quality First**: Choose a database with excellent search quality (HNSW-based)
2. **EU Compliance**: Use EU-based providers or self-host in EU data centers
3. **Right-Size**: Match database to your scale and requirements
4. **Optimize**: Use appropriate indexes, filtering, and caching
5. **Monitor**: Track latency, throughput, errors, and resource usage
6. **Plan for Scale**: Design for growth from the beginning

For most European industrial applications, **Weaviate (self-hosted on OVHcloud or managed EU)** provides the optimal combination of search quality, performance, features, and EU compliance. For the highest scalability requirements, **Qdrant or Milvus (self-hosted on EU cloud)** offer excellent alternatives.
