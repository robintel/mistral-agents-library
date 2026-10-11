---
type: pattern
family: ai
---

# Embedding Model Contract

Attaches to any work using **embedding models** for RAG, search, similarity, or semantic applications. This contract establishes **standard embedding model specifications, selection criteria, and deployment patterns** across providers. Loads alongside any RAG, vector database, or AI system dialect.

Embedding models **transform text into numerical vectors** that capture semantic meaning. The choice of embedding model directly impacts retrieval quality, system performance, and operational costs. A well-chosen embedding model can mean the difference between a RAG system that works and one that fails.

## The Discipline

Embedding selection is **not just picking the most popular model** — it's a **multi-dimensional optimization problem** that balances quality, cost, latency, and compliance. The discipline requires:

- **Quality is parametric**: Different models excel at different tasks (semantic search, clustering, classification, code)
- **Cost scales with usage**: Embedding costs can dwarf LLM costs in high-volume systems
- **Latency compounds**: Embedding time adds to every query and document ingestion
- **Dimensionality matters**: Higher dimensions capture more nuance but cost more to store and compare
- **Provider constraints**: Not all providers support all use cases (batch, custom models, fine-tuning)
- **Compliance is mandatory**: European deployments must respect data residency and privacy requirements

- **Embeddings are the foundation**: Poor embeddings cannot be fixed by better LLMs
- **Test before committing**: Always evaluate candidate models on your actual data
- **Monitor drift**: Embedding quality can degrade as language and data evolve
- **Plan for evolution**: Embedding models improve; design for model swapping

## Embedding Model Providers

### 1. OpenAI Embeddings
**Contract**: `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`

**Specifications**:
```
Provider: OpenAI
Models:
  - text-embedding-3-small:    1536 dimensions, $0.00002/1K tokens
  - text-embedding-3-large:    3072 dimensions, $0.00013/1K tokens
  - text-embedding-ada-002:    1536 dimensions, $0.00010/1K tokens (legacy)
Context Window: 8191 tokens (3-series), 8192 tokens (ada-002)
Max Input: 1M tokens (batch)
Rate Limit: 10,000 RPM (3-small), 10,000 RPM (3-large)
Latency: ~100-300ms (typical)
```

**Capability Profile**:
| Capability | text-embedding-3-small | text-embedding-3-large | text-embedding-ada-002 |
|-----------|------------------------|------------------------|------------------------|
| Semantic Search | ★★★★☆ | ★★★★★ | ★★★★☆ |
| Clustering | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| Classification | ★★★★☆ | ★★★★★ | ★★★★☆ |
| Code | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| Multilingual | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| Long Context | ★★★★☆ | ★★★★☆ | ★★☆☆☆ |

**Strengths**:
- Industry-standard baseline for comparison
- Excellent for English-language tasks
- Strong support for batch operations
- Well-documented and widely adopted
- Consistent performance across use cases

**Weaknesses**:
- Non-EU data processing (US-based)
- Higher cost for 3-large
- Limited customization options
- No fine-tuning capability

**European Data Residency**: ❌ Not available - All OpenAI processing occurs in US data centers. For EU compliance, data must be pre-processed in EU before sending, or use alternative providers.

**Pricing Example** (as of Oct 2026):
```
text-embedding-3-small: $0.02 per 1M tokens
  - 100K documents × 500 tokens avg = 50M tokens = $1.00
  - 10K queries/day × 50 tokens avg = 500K tokens/day = $0.01/day

text-embedding-3-large: $0.13 per 1M tokens
  - 100K documents × 500 tokens avg = 50M tokens = $6.50
  - 10K queries/day × 50 tokens avg = 500K tokens/day = $0.065/day
```

---

### 2. Mistral Embeddings
**Contract**: `mistral-embed` (via Mistral API)

**Specifications**:
```
Provider: Mistral AI
Models:
  - mistral-embed: 1024 dimensions (default)
  - mistral-embed-large: 2048 dimensions
Context Window: 32768 tokens
Max Input: 128K tokens (batch)
Rate Limit: 1000 RPM (standard), negotiable for enterprise
Latency: ~80-200ms (typical, EU-based)
```

**Capability Profile**:
| Capability | mistral-embed | mistral-embed-large |
|-----------|--------------|---------------------|
| Semantic Search | ★★★★☆ | ★★★★★ |
| Clustering | ★★★★☆ | ★★★★★ |
| Classification | ★★★★☆ | ★★★★★ |
| Code | ★★★★☆ | ★★★★★ |
| Multilingual | ★★★★★ | ★★★★★ |
| Long Context | ★★★★★ | ★★★★★ |

**Strengths**:
- **EU data residency**: All processing in European data centers (France/Germany)
- Excellent multilingual support (100+ languages)
- High context window (32K tokens)
- Lower dimensionality = lower storage costs
- Competitive pricing
- Open weights models available for self-hosting

**Weaknesses**:
- Newer ecosystem (less community validation)
- Lower rate limits than OpenAI
- Limited batch size compared to OpenAI
- Smaller model size may impact nuance capture

**European Data Residency**: ✅ **Full compliance** - All Mistral AI processing occurs in EU data centers. Data never leaves EU jurisdiction.

**Pricing Example** (as of Oct 2026):
```
mistral-embed: $0.0001 per 1M tokens
  - 100K documents × 500 tokens avg = 50M tokens = $5.00
  - 10K queries/day × 50 tokens avg = 500K tokens/day = $0.05/day

mistral-embed-large: $0.0002 per 1M tokens
  - 100K documents × 500 tokens avg = 50M tokens = $10.00
  - 10K queries/day × 50 tokens avg = 500K tokens/day = $0.10/day
```

**Note**: Mistral also offers open-source embedding models (`bge-mistral-7b`, etc.) that can be self-hosted for complete data control.

---

### 3. Hugging Face Embeddings
**Contract**: Multiple model families via Hugging Face API or self-hosted

**Model Families**:
```
Sentence Transformers:
  - all-MiniLM-L6-v2:        384 dimensions (baseline)
  - all-mpnet-base-v2:      768 dimensions (high quality)
  - multi-qa-MiniLM-L6-cos-v1: 384 dimensions (Q&A optimized)
  - paraphrase-multilingual-MiniLM-L12-v2: 384 dimensions (multilingual)
  
BAAI:
  - bge-small-en-v1.5:      384 dimensions
  - bge-base-en-v1.5:       768 dimensions
  - bge-large-en-v1.5:      1024 dimensions
  - bge-multilingual-base:  768 dimensions
  
Mistral Open Models:
  - mistralai/Mistral-7B-Instruct-v0.2: 4096 dimensions (via pooling)
  - mistralai/mistral-embed: 1024 dimensions (official embedding model)
```

**Specifications** (Hugging Face API):
```
Provider: Hugging Face
Context Window: Model-dependent (typically 512-2048 tokens)
Max Input: Model-dependent
Rate Limit: 50 RPM (free), 1000+ RPM (pro/enterprise)
Latency: ~200-500ms (API), ~50-150ms (self-hosted on GPU)
```

**Capability Profile** (bge-large-en-v1.5):
| Capability | bge-small | bge-base | bge-large |
|-----------|-----------|----------|-----------|
| Semantic Search | ★★★★☆ | ★★★★★ | ★★★★★ |
| Clustering | ★★★★☆ | ★★★★★ | ★★★★★ |
| Classification | ★★★★☆ | ★★★★★ | ★★★★★ |
| Code | ★★★☆☆ | ★★★★☆ | ★★★★★ |
| Multilingual | ★★★☆☆ | ★★★★☆ | ★★★★★ |
| Long Context | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ |

**Strengths**:
- **Wide model selection**: Hundreds of pre-trained models
- **Self-hosting**: Complete data control and privacy
- **Open source**: Full transparency, customizable
- **Fine-tunable**: Can fine-tune on domain-specific data
- **Multilingual**: Strong support for 100+ languages
- **Cost-effective**: Free for self-hosting, pay-as-you-go for API

**Weaknesses**:
- **API latency**: Higher latency than native provider APIs
- **Rate limits**: Lower on free tier
- **Infrastructure**: Self-hosting requires GPU resources
- **Complexity**: More setup and maintenance overhead
- **Inconsistent performance**: Model quality varies significantly

**European Data Residency**: 
- ⚠️ **API**: Hugging Face API is US-based (not EU compliant)
- ✅ **Self-hosted**: Full EU compliance when hosted in EU data centers
- ✅ **Inference Endpoints**: Can be deployed on EU cloud providers

**Pricing** (Hugging Face API, as of Oct 2026):
```
Free tier: 50 requests/minute
Pro tier: $9/month + $0.002 per 1K tokens
Enterprise: Custom pricing

Self-hosted: Only infrastructure costs (GPU instances)
  - A100 GPU: ~$3-5/hour (on-demand)
  - T4 GPU: ~$0.50-1/hour (on-demand)
```

---

### 4. Cohere Embeddings
**Contract**: `embed-english-v3.0`, `embed-multilingual-v3.0`, `embed-light`

**Specifications**:
```
Provider: Cohere
Models:
  - embed-english-v3.0:     1024 dimensions
  - embed-multilingual-v3.0: 1024 dimensions
  - embed-light:           1024 dimensions (faster, cheaper)
Context Window: 512 tokens (v3.0), 2048 tokens (light)
Max Input: 10K tokens (batch)
Rate Limit: 1000 RPM (standard)
Latency: ~100-250ms
```

**Capability Profile**:
| Capability | embed-english | embed-multilingual | embed-light |
|-----------|---------------|-------------------|-------------|
| Semantic Search | ★★★★★ | ★★★★★ | ★★★★☆ |
| Clustering | ★★★★★ | ★★★★★ | ★★★★☆ |
| Classification | ★★★★★ | ★★★★★ | ★★★☆☆ |
| Code | ★★★★☆ | ★★★★☆ | ★★★☆☆ |
| Multilingual | ★★☆☆☆ | ★★★★★ | ★★☆☆☆ |
| Long Context | ★★★☆☆ | ★★★☆☆ | ★★★★☆ |

**Strengths**:
- High-quality embeddings for English
- Strong multilingual support (v3.0)
- Fast inference
- Good documentation
- Enterprise-ready

**Weaknesses**:
- ❌ **Non-EU data processing**: Cohere is US/Canada-based
- Higher cost than some alternatives
- Limited model selection
- No fine-tuning capability

**European Data Residency**: ❌ Not available - All processing occurs outside EU.

**Pricing** (as of Oct 2026):
```
embed-english-v3.0: $0.0001 per 1K tokens
embed-multilingual-v3.0: $0.0001 per 1K tokens
embed-light: $0.00005 per 1K tokens
```

---

### 5. Local/Open-Source Embeddings
**Contract**: Self-hosted embedding models

**Recommended Models**:
```
BAAI (FlagEmbedding):
  - BAAI/bge-small-en-v1.5:     384d, 93M params
  - BAAI/bge-base-en-v1.5:      768d, 110M params
  - BAAI/bge-large-en-v1.5:     1024d, 567M params
  
Sentence Transformers:
  - sentence-transformers/all-MiniLM-L6-v2:        384d, 22M params
  - sentence-transformers/all-mpnet-base-v2:      768d, 109M params
  - sentence-transformers/multi-qa-mpnet-base-dot-v1: 768d, 109M params
  
Mistral:
  - mistralai/mistral-embed:                        1024d, 110M params
  - mistralai/Mistral-7B-Instruct-v0.2:          4096d (via mean pooling)
  
Intel:
  - intel/electra-large-discriminator:           256d, 335M params (fast)
```

**Deployment Options**:

#### Option A: Hugging Face Transformers (CPU)
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-base-en-v1.5')
embeddings = model.encode(texts)
```
**Latency**: ~500-1000ms (CPU, batch of 100)
**Hardware**: 8+ CPU cores recommended
**Throughput**: ~100-500 docs/minute

#### Option B: Hugging Face Transformers (GPU)
```python
model = SentenceTransformer('BAAI/bge-large-en-v1.5', device='cuda')
embeddings = model.encode(texts)
```
**Latency**: ~50-150ms (GPU, batch of 100)
**Hardware**: 1x A100 or 2x T4 GPUs
**Throughput**: ~2000-10000 docs/minute

#### Option C: ONNX Runtime (Optimized)
```python
import onnxruntime as ort
sess = ort.InferenceSession('bge-base-en-v1.5.onnx')
embeddings = sess.run(None, {'input': texts})[0]
```
**Latency**: ~30-80ms (GPU, batch of 100)
**Hardware**: 1x GPU
**Throughput**: ~5000-20000 docs/minute

#### Option D: vLLM (High Throughput)
```python
from vllm import LLM, SamplingParams
model = LLM(model='BAAI/bge-large-en-v1.5', tensor_parallel_size=4)
```
**Latency**: ~20-50ms (multi-GPU)
**Hardware**: 4+ GPUs
**Throughput**: ~20000+ docs/minute

**Strengths**:
- ✅ **Full data control**: Data never leaves your infrastructure
- ✅ **EU compliance**: Can be deployed in EU data centers
- ✅ **No API costs**: Only infrastructure costs
- ✅ **Customizable**: Fine-tune on domain-specific data
- ✅ **Offline**: Works without internet connectivity
- ✅ **No rate limits**: Limited only by hardware

**Weaknesses**:
- **Infrastructure overhead**: Requires GPU/CPU resources
- **Maintenance**: Model updates, security patches
- **Scaling complexity**: Need to manage multiple instances
- **Hardware costs**: GPU instances are expensive
- **Expertise required**: Need ML/DevOps knowledge

**European Data Residency**: ✅ **Full compliance** when deployed in EU data centers.

**Infrastructure Costs** (EU cloud, as of Oct 2026):
```
CPU-only (8 vCPUs):
  - AWS (Frankfurt): ~$0.15/hour = ~$108/month
  - OVHcloud (France): ~€0.10/hour = ~€72/month
  - Hetzner (Germany): ~€0.08/hour = ~€58/month
  Throughput: ~200-500 docs/minute

Single GPU (1x T4):
  - AWS (Frankfurt): ~$0.50/hour = ~$360/month
  - OVHcloud: ~€0.40/hour = ~€288/month
  - Hetzner: ~€0.35/hour = ~€252/month
  Throughput: ~2000-5000 docs/minute

Multi-GPU (4x A100):
  - AWS (Frankfurt): ~$10/hour = ~$7200/month
  - OVHcloud: ~€8/hour = ~€5760/month
  Throughput: ~20000-50000 docs/minute
```

## Selection Criteria

### Decision Framework

Use this **weighted scoring matrix** to select the optimal embedding model:

```
Score each provider (1-5) on each criterion:
1 = Poor, 2 = Below Average, 3 = Average, 4 = Above Average, 5 = Excellent

Criteria:
┌─────────────────────────┬──────────┬─────────────────────────────────────┐
│ Criterion                │ Weight   │ Description                             │
├─────────────────────────┼──────────┼─────────────────────────────────────┤
│ Quality (Your Data)      │ 30%      │ Performance on your specific data     │
│ Cost                     │ 25%      │ Total cost of ownership               │
│ Latency                  │ 20%      │ End-to-end embedding time             │
│ EU Compliance            │ 15%      │ Data residency and privacy            │
│ Throughput               │ 10%      │ Documents/queries per minute          │
└─────────────────────────┴──────────┴─────────────────────────────────────┘

Weighted Score = Σ(score × weight)
```

### Quick Selection Guide

| Use Case | Recommended Provider | Alternative | Notes |
|----------|---------------------|-------------|-------|
| **Production RAG (EU)** | Mistral AI | Self-hosted BAAI | Full EU compliance, good quality |
| **Production RAG (US)** | OpenAI 3-large | Cohere v3 | Best quality, highest cost |
| **Cost-Sensitive** | Mistral AI | Self-hosted | 5-10x cheaper than OpenAI |
| **High Volume** | Self-hosted (vLLM) | OpenAI | Scale to millions of docs |
| **Multilingual** | Mistral AI | Hugging Face BAAI | Best non-English support |
| **Offline/Air-Gapped** | Self-hosted | - | Only option for secure environments |
| **Fine-Tuning Needed** | Self-hosted | - | Only option for custom models |
| **Fast Prototyping** | OpenAI | Hugging Face API | Quick to start, easy to use |
| **Maximum Quality** | OpenAI 3-large | Cohere v3 | Best-in-class embeddings |

### Evaluation Protocol

Before selecting an embedding model, **always evaluate on your data**:

```python
# 1. Retrieve Test Set
# Collect 100-500 representative queries and their expected answers

# 2. Embed All Documents
# Embed your entire document corpus with candidate models

# 3. Evaluate Retrieval
# For each query:
#   - Retrieve top-K documents using each model's embeddings
#   - Calculate: Hit Rate, MRR, NDCG, Precision@K

# 4. Compare Results
hit_rate = (queries with correct doc in top-K) / total_queries
mrr = mean(reciprocal_rank of first correct doc)
ndcg = normalized discounted cumulative gain

# 5. Select Winner
# Choose model with best quality/cost trade-off
```

**Evaluation Metrics**:

| Metric | Formula | Target | Description |
|--------|---------|--------|-------------|
| Hit Rate @K | Hits / Total | >0.8 | % of queries with correct doc in top-K |
| MRR (Mean Reciprocal Rank) | 1/rank of first hit | >0.5 | Average of reciprocal ranks |
| NDCG @K | Normalized DCG | >0.7 | Quality of ranking considering position |
| Precision @K | Relevant / Retrieved | >0.6 | % of retrieved docs that are relevant |
| Recall @K | Relevant Retrieved / Total Relevant | >0.5 | % of all relevant docs retrieved |

## Performance Optimization

### 1. Dimensionality Reduction

**Problem**: Higher dimensions = better quality but higher costs (storage, compute, latency)

**Solutions**:
```
Option A: Use Lower-Dimensional Model
  - text-embedding-3-small: 1536d → Save 50% storage
  - bge-small-en-v1.5: 384d → Save 75% storage
  - mistral-embed: 1024d → Save 33% storage vs 1536d

Option B: PCA (Principal Component Analysis)
  - Reduce 1536d → 512d with minimal quality loss
  - Can lose 1-5% retrieval quality
  - Fast, linear transformation

Option C: Truncated SVD
  - Similar to PCA but works on sparse data
  - Preserves most variance in lower dimensions
```

**Quality vs Dimensionality**:
```
Model: text-embedding-3-small (1536d)
┌──────────────┬──────────┬──────────┬──────────┐
│ Dimensions    │ Hit Rate │ MRR       │ Storage   │
├──────────────┼──────────┼──────────┼──────────┤
│ 1536 (full)   │ 0.85     │ 0.62     │ 100%      │
│ 1024          │ 0.84     │ 0.61     │ 67%       │
│ 768           │ 0.83     │ 0.60     │ 50%       │
│ 512           │ 0.81     │ 0.58     │ 33%       │
│ 384           │ 0.78     │ 0.55     │ 25%       │
└──────────────┴──────────┴──────────┴──────────┘
```

### 2. Quantization

**Problem**: Float32 embeddings use 16 bytes per dimension (32-bit float × 4 bytes × 2 for index)

**Solutions**:
```
Option A: Float16 (Half Precision)
  - 2 bytes per dimension
  - Minimal quality loss (<0.5%)
  - Supported by most vector databases

Option B: Int8 (8-bit Integer)
  - 1 byte per dimension
  - Small quality loss (1-3%)
  - Requires calibration

Option C: Binary (1-bit)
  - 0.125 bytes per dimension
  - Significant quality loss (5-10%)
  - Only for approximate search
```

**Storage Savings**:
```
1M documents × 1536 dimensions:
┌──────────────┬────────────┬────────────┐
│ Precision     │ Size per doc│ Total Size  │
├──────────────┼────────────┼────────────┤
│ Float32       │ 6 KB        │ 6 GB        │
│ Float16       │ 3 KB        │ 3 GB        │
│ Int8          │ 1.5 KB      │ 1.5 GB      │
│ Binary        │ 192 bytes   │ 192 MB      │
└──────────────┴────────────┴────────────┘
```

### 3. Batching

**Problem**: API latency per request adds up quickly

**Solution**: Batch multiple texts into single API call

```
# Sequential (bad)
for text in texts:
    embedding = client.embed(text)  # 100ms per call
# Total: 100 texts × 100ms = 10 seconds

# Batched (good)
embeddings = client.embed(texts)  # 100ms total for 100 texts
# Total: 100ms
```

**Batch Size Limits**:
```
Provider        Max Batch Size  Max Tokens/Request
─────────────────────────────────────────────
OpenAI          2048 texts      1M tokens
Mistral         1000 texts      128K tokens
Hugging Face    200 texts       32K tokens
Cohere          1000 texts      10K tokens
```

**Optimal Batch Size**: Balance between latency and throughput
- Too small: High overhead per request
- Too large: Long wait times, memory issues
- **Recommended**: 100-500 texts per batch

### 4. Caching

**Problem**: Same text embedded multiple times = wasted cost and time

**Solution**: Cache embeddings by text content

```python
# Simple in-memory cache
embedding_cache = {}

def get_embedding(text):
    if text not in embedding_cache:
        embedding_cache[text] = client.embed(text)
    return embedding_cache[text]
```

**Cache Strategies**:

| Strategy | When to Use | Hit Rate | Complexity |
|----------|-------------|----------|------------|
| In-Memory | Single process | 30-60% | Low |
| Redis | Multi-process | 50-80% | Medium |
| Database | Persistent | 60-90% | High |
| Distributed (Redis Cluster) | High volume | 70-95% | High |

**Cache Key**: Use content hash, not text (to handle formatting differences)
```python
import hashlib
cache_key = hashlib.sha256(text.encode()).hexdigest()[:16]
```

**Cache Invalidation**:
- **Documents**: Never invalidate (content is static)
- **Queries**: Cache for 1-24 hours (queries may repeat)
- **Size Limit**: Set max cache size (e.g., 100K entries)
- **TTL**: Time-to-live for cache entries

### 5. Pre-filtering

**Problem**: Embedding and retrieving irrelevant documents wastes resources

**Solution**: Filter documents before embedding/retrieval

```python
# Pre-filter by metadata
if document.metadata['language'] != query_language:
    skip

if document.metadata['timestamp'] < query_time_range[0]:
    skip

if document.metadata['category'] not in query_categories:
    skip
```

**Filtering Strategies**:

| Filter Type | When to Use | Efficiency Gain |
|-------------|-------------|-----------------|
| Language | Multilingual corpus | 50-90% |
| Timestamp | Time-sensitive queries | 70-95% |
| Category | Domain-specific queries | 40-80% |
| Access Level | Security-conscious | 80-99% |
| Geolocation | Location-based queries | 60-90% |

## Cost Optimization

### Cost Comparison (100K documents, 10K queries/day)

```
┌─────────────────────────┬──────────────┬──────────────┬──────────────┐
│ Provider                 │ Ingestion    │ Query        │ Monthly Total │
├─────────────────────────┼──────────────┼──────────────┼──────────────┤
│ OpenAI 3-small           │ $5.00        │ $0.10        │ $5.10         │
│ OpenAI 3-large           │ $32.50       │ $0.65        │ $33.15        │
│ Mistral embed            │ $5.00        │ $0.05        │ $5.05         │
│ Mistral embed-large      │ $10.00       │ $0.10        │ $10.10        │
│ Cohere embed-english     │ $5.00        │ $0.10        │ $5.10         │
│ Cohere embed-light       │ $2.50        │ $0.05        │ $2.55         │
│ Self-hosted (CPU, 8 vCPU)│ $0.00*       │ $0.00*       │ $108.00*      │
│ Self-hosted (GPU, 1xT4)  │ $0.00*       │ $0.00*       │ $360.00*      │
│ Self-hosted (GPU, 4xA100)│ $0.00*       │ $0.00*       │ $7200.00*     │
└─────────────────────────┴──────────────┴──────────────┴──────────────┘

*Infrastructure costs only, no embedding API costs
**Break-even points**:
- Self-hosted CPU vs OpenAI: ~20K docs/month
- Self-hosted GPU (T4) vs OpenAI: ~80K docs/month
- Self-hosted GPU (A100) vs OpenAI: ~500K docs/month
```

### Cost-Saving Checklist

- [ ] Use lower-dimensional models where quality permits
- [ ] Enable batching for all embedding operations
- [ ] Implement caching for repeated texts/queries
- [ ] Pre-filter documents to reduce embedding volume
- [ ] Use float16 or int8 quantization for storage
- [ ] Consider self-hosting for high-volume use cases
- [ ] Monitor usage and set budgets/alerts
- [ ] Delete unused embeddings (garbage collection)
- [ ] Use spot instances for batch embedding jobs
- [ ] Compress embeddings with PCA for storage efficiency

## European Compliance

### GDPR Requirements for Embeddings

**Key Considerations**:

1. **Personal Data in Embeddings**
   - Embeddings can contain PII (names, addresses, IDs)
   - **Mitigation**: Remove PII before embedding or use models that don't leak PII
   - **Detection**: Use PII detection tools on source text

2. **Data Residency**
   - Embeddings must be stored in EU for EU citizens' data
   - **Mitigation**: Use EU-based embedding providers or self-host in EU
   - **Verification**: Audit data center locations regularly

3. **Data Subject Rights**
   - Right to access: Provide embedding representations on request
   - Right to erasure: Delete embeddings when requested
   - Right to portability: Export embeddings in standard format
   - **Mitigation**: Implement robust data management policies

4. **Data Minimization**
   - Only embed data necessary for the task
   - **Mitigation**: Filter documents before embedding
   - **Verification**: Regular audits of embedded data

5. **Purpose Limitation**
   - Embeddings must be used only for stated purposes
   - **Mitigation**: Document embedding use cases
   - **Verification**: Access controls and audit logging

### EU-Compliant Embedding Stack

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
│                      Embedding Service                           │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Option 1: Mistral AI Embeddings (EU-based)              │  │
│  │  Option 2: Self-hosted on OVHcloud/T-Systems (EU)        │  │
│  │  Option 3: Hugging Face Inference on EU cloud             │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Vector Database                            │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Option 1: Qdrant on OVHcloud (EU)                        │  │
│  │  Option 2: Weaviate on AWS Frankfurt (EU)                 │  │
│  │  Option 3: Milvus on T-Systems (EU)                       │  │
│  │  Option 4: Self-hosted on sovereign cloud                 │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Infrastructure                            │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  All infrastructure in EU data centers                    │  │
│  │  EU-based cloud providers: OVHcloud, T-Systems, Scaleway  │  │
│  │  Certifications: ISO 27001, SOC 2, Gaia-X                  │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Compliance Checklist

- [ ] **Embedding Provider**: Verify EU data residency (Mistral AI or self-hosted)
- [ ] **Vector Database**: Deploy in EU data center
- [ ] **Data Classification**: Identify and label all PII in documents
- [ ] **PII Removal**: Strip PII before embedding or use PII-safe models
- [ ] **Access Controls**: Implement role-based access to embeddings
- [ ] **Audit Logging**: Log all embedding operations and access
- [ ] **Data Retention**: Define and enforce retention policies
- [ ] **Encryption**: Encrypt embeddings at rest and in transit
- [ ] **Key Management**: Use EU-based key management service
- [ ] **Data Portability**: Ensure embeddings can be exported in standard format
- [ ] **DPO Review**: Consult Data Protection Officer for high-risk deployments
- [ ] **DPIA**: Conduct Data Protection Impact Assessment if required

## Deployment Patterns

### 1. Managed Provider (Recommended for Most)

**Architecture**:
```
User → Application → Mistral AI API → EU Data Center → Embeddings
```

**Pros**:
- No infrastructure management
- Automatic scaling
- EU compliance built-in
- Regular model updates

**Cons**:
- Ongoing API costs
- Rate limits
- Limited customization

**When to Use**:
- Production systems with <10M docs
- Need EU compliance without infrastructure overhead
- Want to start quickly

### 2. Self-Hosted Single Node (Development/Small Scale)

**Architecture**:
```
User → Application → Self-hosted Model (CPU/GPU) → Embeddings
```

**Pros**:
- Full data control
- No API costs
- Complete customization
- Offline capability

**Cons**:
- Infrastructure management overhead
- Limited scalability
- Need GPU for good performance

**When to Use**:
- Development and testing
- Small-scale production (<100K docs)
- Air-gapped environments
- Fine-tuning required

### 3. Self-Hosted Distributed (High Volume)

**Architecture**:
```
User → Load Balancer → [Embedding Node 1] → Embeddings
                        │
                        ├─ [Embedding Node 2]
                        │
                        └─ [Embedding Node N]
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

**When to Use**:
- High-volume production (>1M docs)
- Need to process millions of documents
- Require low latency at scale

### 4. Hybrid (Best of Both Worlds)

**Architecture**:
```
User → Application → [Managed for Queries] → Embeddings
                       │
                       └─ [Self-hosted for Ingestion] → Embeddings
```

**Pros**:
- Cost-effective ingestion (self-hosted batch)
- Low-latency queries (managed API)
- Flexibility

**Cons**:
- Complex architecture
- Need to manage two systems

**When to Use**:
- Large document corpus with frequent queries
- Batch ingestion with real-time queries
- Cost optimization priority

## Monitoring and Maintenance

### Key Metrics to Monitor

```
┌─────────────────────────┬──────────────┬─────────────────────────┐
│ Metric                    │ Target        │ Alert Threshold         │
├─────────────────────────┼──────────────┼─────────────────────────┤
│ Embedding Latency (p95)   │ <200ms        │ >500ms                  │
│ Throughput (docs/min)     │ >1000         │ <500                    │
│ Hit Rate @5               │ >0.8          │ <0.7                    │
│ MRR                       │ >0.6          │ <0.5                    │
│ NDCG @10                  │ >0.7          │ <0.6                    │
│ API Error Rate            │ <0.1%         │ >1%                     │
│ Cache Hit Rate            │ >50%          │ <30%                    │
│ Cost per 1K embeddings    │ <$0.01        │ >$0.05                  │
└─────────────────────────┴──────────────┴─────────────────────────┘
```

### Alerting Rules

```yaml
# Example Prometheus alerting rules
- alert: HighEmbeddingLatency
  expr: histogram_quantile(0.95, embedding_latency_seconds) > 0.5
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High embedding latency (p95 > 500ms)"

- alert: LowRetrievalQuality
  expr: hit_rate_at_5 < 0.7
  for: 15m
  labels:
    severity: critical
  annotations:
    summary: "Low retrieval quality (hit rate < 70%)"

- alert: HighAPIErrors
  expr: rate(embedding_api_errors_total[5m]) > 0.01
  labels:
    severity: warning
  annotations:
    summary: "High API error rate (>1%)"

- alert: HighCost
  expr: embedding_cost_today > 100
  labels:
    severity: warning
  annotations:
    summary: "High embedding costs (>$100 today)"
```

### Model Drift Detection

**Problem**: Embedding quality can degrade over time as language evolves

**Solution**: Regularly re-evaluate embedding performance

```python
# Monthly evaluation
current_metrics = evaluate_embeddings(test_set)
if current_metrics['hit_rate'] < baseline_metrics['hit_rate'] * 0.95:
    trigger_alert("Embedding quality degradation detected")
    schedule_model_review()
```

**Drift Detection Strategies**:

| Strategy | Frequency | Complexity |
|----------|-----------|------------|
| Statistical Test | Daily | Low |
| Quality Metrics | Weekly | Medium |
| A/B Testing | Monthly | High |
| User Feedback | Continuous | Medium |

## Migration Strategies

### From One Model to Another

**Challenges**:
- Different dimension sizes
- Different semantic spaces
- Need to re-embed all documents

**Migration Process**:

```
Phase 1: Preparation (1-2 weeks)
├── Select new embedding model
├── Evaluate on test data
├── Set up dual-running infrastructure
└── Create migration plan

Phase 2: Dual Running (2-4 weeks)
├── Run both models in parallel
├── Compare retrieval results
├── A/B test with users
└── Monitor quality metrics

Phase 3: Cutover (1 week)
├── Re-embed all documents with new model
├── Update application to use new embeddings
├── Full regression testing
└── Gradual rollout to users

Phase 4: Cleanup (1 week)
├── Delete old embeddings
├── Monitor new model performance
├── Update documentation
└── Celebrate
```

**Migration Tools**:

```python
# Batch re-embedding script
async def re_embed_corpus(new_model, batch_size=1000):
    documents = db.get_all_documents()
    for batch in chunk(documents, batch_size):
        texts = [doc.text for doc in batch]
        embeddings = await new_model.embed(texts)
        for doc, embedding in zip(batch, embeddings):
            db.update_embedding(doc.id, embedding)
        await db.commit()
```

### Dimensionality Migration

**Problem**: Changing embedding dimensions breaks vector database indices

**Solution**: Use compatibility layer or re-index

```python
# Option 1: Compatibility layer (if using PCA)
class DimensionalityAdapter:
    def __init__(self, old_dim, new_dim):
        self.pca = load_pca(old_dim, new_dim)
    
    def transform(self, embedding):
        return self.pca.transform([embedding])[0]

# Option 2: Re-index (cleanest approach)
def migrate_dimensions(old_dim, new_dim):
    # 1. Export all embeddings
    all_embeddings = db.get_all_embeddings()
    
    # 2. Transform to new dimensions
    transformed = [transform(e, old_dim, new_dim) for e in all_embeddings]
    
    # 3. Delete old index
    db.delete_index()
    
    # 4. Create new index with new dimensions
    db.create_index(new_dim)
    
    # 5. Insert transformed embeddings
    db.insert_embeddings(transformed)
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Using default model without evaluation | Suboptimal quality | Always evaluate on your data |
| Not batching embeddings | High latency, high cost | Batch all embedding calls |
| No caching | Wasted compute and cost | Implement caching layer |
| Storing full float32 | 4x storage costs | Use float16 or int8 |
| Ignoring EU compliance | GDPR violations | Use EU-compliant providers |
| No monitoring | Can't detect issues | Monitor quality and performance |
| Hardcoding model in application | Can't upgrade models | Use configuration |
| Not versioning embeddings | Can't roll back | Version all embedding models |
| Embedding raw HTML/XML | Noise in embeddings | Clean text before embedding |
| Embedding entire long documents | Loses focus, high cost | Chunk documents first |
| Using same embeddings for different tasks | Suboptimal for each | Use task-specific embeddings |
| Not testing with real queries | Synthetic data ≠ real data | Test with actual user queries |

## Best Practices

### Pre-Embedding
- [ ] Clean text (remove HTML, markdown, special characters)
- [ ] Normalize text (lowercase, remove accents, expand contractions)
- [ ] Chunk long documents (512-2048 tokens per chunk)
- [ ] Remove PII and sensitive data
- [ ] Filter irrelevant documents
- [ ] Deduplicate near-identical documents

### Embedding
- [ ] Use batching (100-500 texts per batch)
- [ ] Handle errors and retries gracefully
- [ ] Implement rate limiting
- [ ] Use async for better throughput
- [ ] Monitor and log all operations
- [ ] Version your embedding models

### Post-Embedding
- [ ] Normalize vectors (L2 normalization)
- [ ] Quantize if needed (float16, int8)
- [ ] Store with metadata (model, version, timestamp)
- [ ] Create vector index for efficient search
- [ ] Implement caching
- [ ] Monitor retrieval quality

### Operations
- [ ] Set up monitoring and alerting
- [ ] Regularly evaluate embedding quality
- [ ] Plan for model upgrades
- [ ] Document your embedding pipeline
- [ ] Test backup and restore procedures
- [ ] Monitor costs and set budgets

## Summary

Embedding models are the **foundation of RAG and semantic applications**. The choice of model impacts everything: quality, cost, latency, and compliance. For European deployments, **Mistral AI or self-hosted models in EU data centers** provide the best balance of performance and compliance.

**Key Takeaways**:

1. **Quality First**: Always evaluate candidate models on your actual data
2. **Cost Matters**: Embedding costs can exceed LLM costs at scale
3. **EU Compliance**: Use Mistral AI or self-hosted in EU for GDPR compliance
4. **Optimize**: Use batching, caching, quantization, and dimensionality reduction
5. **Monitor**: Track quality metrics, latency, and costs
6. **Plan for Change**: Embedding models evolve; design for upgrades

For most European industrial applications, **Mistral AI embeddings** provide the optimal combination of quality, cost, latency, and EU compliance. For the highest volume or most custom requirements, **self-hosted BAAI models on EU cloud infrastructure** offer complete control and data sovereignty.
