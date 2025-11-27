# Sources for: How to Choose the Right Vector Database

**Total Sources:** 7 authoritative sources
**Verification Rate:** 100%

## Primary Technical Documentation

[1] **An Opinionated Checklist to Choose a Vector Database** - Pinecone Engineering Team (2025)
    Authority: 0.90
    Key insight: Three main evaluation categories: technology, developer experience, and enterprise readiness. Provides decision tree for selection.
    Coverage: Comprehensive framework for all five criteria

[2] **Choosing an AWS Vector Database for RAG Use Cases** - AWS Prescriptive Guidance (2025)
    Authority: 0.85
    Key insight: Query frequency is crucial—internal use cases have low query rates while consumer-facing applications need high throughput.
    Coverage: Query patterns, integration with AWS services, cost optimization

[3] **How to Choose a Vector Database** - Elastic Blog (2024)
    Authority: 0.85
    Key insight: SQL support via PostgreSQL pgvector or YugabyteDB allows combining vector searches with relational queries, reducing operational complexity.
    Coverage: Integration requirements, hybrid search capabilities

## Benchmarks and Comparative Analysis

[4] **Vector Database Comparison 2025: Pinecone vs Weaviate vs Qdrant vs FAISS vs Milvus vs Chroma** - LiquidMetal AI (2025)
    Authority: 0.75
    Key insight: Milvus/Zilliz showed <10ms p50 latency with highest QPS; Pinecone and Qdrant 20-50ms; real performance varies with embedding dimension and filter complexity.
    Coverage: Performance benchmarks, scale testing, latency comparisons

[5] **Vector Database Selection Criteria for Embedding-Based Applications** - Dev3lop (2025)
    Authority: 0.70
    Key insight: Milvus supports 11 different index types optimized for enterprise scale (billions of vectors); different solutions excel at different scales.
    Coverage: Scale & data volume, index types, architectural capabilities

## Cost and Operational Analysis

[6] **Vector Data Store Evaluation Criteria** - Sanjeev Mohan, Medium (2024)
    Authority: 0.65
    Key insight: "Cost can become the biggest impediment to mass adoption of LLMs, making it imperative to calculate the total cost of ownership (TCO)."
    Coverage: Storage costs ($0.10-0.30/GB managed vs $0.02-0.05 self-hosted), engineering time costs

[7] **Top Vector Databases for RAG** - AIMultiple Research (2025)
    Authority: 0.70
    Key insight: Many databases deliver 10-100ms query times on 1M-10M vector datasets, though actual performance depends heavily on hardware, index type, and load.
    Coverage: General performance characteristics, typical latency ranges

## Vector Database Capabilities Referenced

### **Pinecone**
- Optimized for: 1M-100M vectors
- Latency: 20-50ms p50 (sub-2ms in optimized configs)
- Pricing: ~$70/month managed for 10M vectors (1536-dim)
- Best for: Managed simplicity, consistent performance

### **Milvus/Zilliz**
- Optimized for: Billions of vectors, enterprise scale
- Latency: <10ms p50 with highest QPS
- Features: 11 index types, horizontal scaling
- Best for: Large-scale deployments

### **Qdrant**
- Optimized for: 10M-1B vectors
- Implementation: Rust-based efficiency
- Latency: 20-50ms p50
- Pricing: ~$30/month self-hosted on AWS
- Best for: Cost-conscious at scale

### **Weaviate**
- Optimized for: 1M-50M vectors with graph features
- Features: Hybrid search (vector + keyword)
- Latency: Higher when graph features enabled
- Best for: Semantic richness, hybrid search

### **pgvector (PostgreSQL)**
- Optimized for: Integration with existing PostgreSQL
- Features: SQL joins with vector search
- Best for: Minimal operational overhead, combined queries

### **Chroma**
- Optimized for: <1M vectors
- Best for: Ease of use, getting started

## Key Quantitative Data

- **Standard embedding dimension:** 1536 (OpenAI text-embedding-ada-002)
- **Emerging dimensions:** 3072 (higher precision), 384 (speed-critical)
- **Scale thresholds:**
  - <1M vectors: Any solution works, prioritize ease
  - 1M-100M: Most managed solutions perform well
  - 100M-1B: Need Qdrant or Milvus for efficiency
  - >1B: Enterprise solutions with horizontal scaling

- **Query rate examples:**
  - Internal docs (500 employees, 10 searches/day): 0.06 QPS
  - E-commerce (10K concurrent users): 1000+ QPS
  - Cost difference: 10x between serverless and dedicated

- **Cost breakdown:**
  - Managed storage: $0.10-0.30/GB-month
  - Self-hosted storage: $0.02-0.05/GB-month
  - Engineering time: $150/hour maintenance
  - Example: $70/month managed vs $30/month + $600/month engineering = managed is cheaper

- **Performance ranges:**
  - Milvus: <10ms p50
  - Pinecone/Qdrant: 20-50ms p50
  - Weaviate: Higher with graph features
  - *All vary with dimension, filters, network latency*
