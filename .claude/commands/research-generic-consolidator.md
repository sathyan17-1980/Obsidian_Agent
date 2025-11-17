# Generic Research Consolidator

**Purpose:** Multi-source research agent for any topic with flexible output formats
**Status:** Ready for Use
**Date:** 2025-11-17

## Quick Start

```bash
/research-generic "What are the latest developments in quantum computing?"
```

---

## What This Agent Does

The Generic Research Consolidator is a versatile multi-source research system that:

1. **Researches 6 Sources in Parallel:**
   - HackerNews discussions
   - Web articles (Brave Search API)
   - Full article content extraction
   - Your Obsidian vault (mandatory)
   - Google Drive documents
   - YouTube transcripts

2. **Generates Flexible Outputs:**
   - Research summaries
   - Technical reports
   - Q&A documents
   - Comparative analysis
   - Literature reviews
   - Custom formats (you specify)

3. **Ensures Quality:**
   - Detects and resolves conflicts across sources
   - Verifies all citations
   - Semantic deduplication
   - Authority-based ranking

4. **Saves Everything to Obsidian:**
   - Research summaries
   - Generated outputs
   - Sources and citations
   - Metadata and conflicts

---

## Architecture

```
USER INPUT (Any research topic)
         |
         v
RESEARCH CONSOLIDATOR (Orchestrator)
         |
         +-- HackerNews Researcher ----+
         +-- Web Searcher (Brave API) -+
         +-- Article Reader -----------+---- PARALLEL
         +-- Obsidian Vault -----------+    EXECUTION
         +-- Google Drive -------------+
         +-- YouTube Transcripts ------+
         |
         v
AGGREGATION & CONFLICT DETECTION
         |
         v
FLEXIBLE OUTPUT GENERATION
  - Research Summary
  - Technical Report
  - Q&A Document
  - Custom Format
         |
         v
OBSIDIAN VAULT STORAGE
```

---

## Use Cases

### 1. Research Summary (Default)
**Input:** "What are embeddings in machine learning?"
**Output:**
- Executive summary (200-300 words)
- Key findings (bullet points)
- Detailed sections
- All sources cited

### 2. Technical Report
**Input:** "Compare RAG vs fine-tuning approaches"
**Output:**
- Introduction
- Background
- Comparative analysis
- Pros/cons table
- Recommendations
- References

### 3. Q&A Document
**Input:** "How do transformers work?"
**Output:**
- Question breakdown
- Answer with examples
- Common misconceptions
- Related questions
- Further reading

### 4. Literature Review
**Input:** "Recent advances in multimodal AI"
**Output:**
- Overview of field
- Key papers and contributions
- Methodology comparison
- Future directions
- Bibliography

### 5. Competitive Analysis
**Input:** "AI code assistants comparison"
**Output:**
- Market landscape
- Feature comparison matrix
- Strengths/weaknesses
- Pricing analysis
- Recommendations

---

## Usage Examples

### Basic Research (Default Output)

```bash
/research-generic "What are the latest developments in quantum computing?"
```

**Generates:**
- Research summary (500-1000 words)
- Key findings
- All sources cited
- Saved to Obsidian

---

### Custom Output Format

```bash
/research-generic "Explain neural networks" --format "beginner-guide"
```

**Generates:**
- ELI5 explanation
- Visual analogies
- Step-by-step breakdown
- Common misconceptions
- Next steps for learning

---

### Comparative Analysis

```bash
/research-generic "RAG vs Fine-tuning" --format "comparison"
```

**Generates:**
- Side-by-side comparison
- Use case recommendations
- Pros/cons table
- Cost analysis
- Implementation guidance

---

### Deep Dive Research

```bash
/research-generic "Constitutional AI safety" --depth deep --format "technical-report"
```

**Generates:**
- Comprehensive technical report (2000+ words)
- Methodology section
- Implementation details
- Evaluation criteria
- Future research directions

---

## Research Depth Levels

| Depth | Queries/Source | Time | Cost | Use Case |
|-------|----------------|------|------|----------|
| **minimal** | 1-3 | ~60s | ~$0.10 | Quick fact-checking |
| **light** | 3-5 | ~90s | ~$0.12 | Basic research |
| **moderate** (DEFAULT) | 5-8 | ~120s | ~$0.15 | Standard research |
| **deep** | 8-12 | ~180s | ~$0.18 | Comprehensive analysis |
| **extensive** | 12+ | ~240s | ~$0.20+ | Multi-topic deep dive |

---

## Output Formats

### 1. Research Summary (Default)
```markdown
# {Topic}

## Executive Summary
[200-300 word overview]

## Key Findings
- Finding 1
- Finding 2
- Finding 3

## Detailed Analysis
### Section 1
[Content]

### Section 2
[Content]

## Conflicts & Resolutions
[Any conflicts detected]

## Sources
[All citations]
```

### 2. Technical Report
```markdown
# {Topic}: Technical Report

## Abstract
[Brief overview]

## Introduction
[Background and context]

## Methodology
[How research was conducted]

## Findings
[Detailed results]

## Discussion
[Analysis and interpretation]

## Conclusions
[Summary and recommendations]

## References
[All sources]
```

### 3. Q&A Document
```markdown
# {Topic}: Questions & Answers

## Main Question
{User's question}

## Answer
[Comprehensive answer]

## Key Points
- Point 1
- Point 2

## Examples
[Real-world examples]

## Common Misconceptions
[Address misunderstandings]

## Related Questions
- Question 1
- Question 2

## Further Reading
[Curated sources]
```

### 4. Comparison Analysis
```markdown
# {Option A} vs {Option B}

## Overview
[Brief comparison]

## Feature Comparison
| Feature | Option A | Option B |
|---------|----------|----------|
| ... | ... | ... |

## Pros & Cons
### Option A
**Pros:**
- Pro 1

**Cons:**
- Con 1

### Option B
**Pros:**
- Pro 1

**Cons:**
- Con 1

## Recommendations
[Use case guidance]

## Sources
[Citations]
```

### 5. Beginner's Guide
```markdown
# {Topic}: A Beginner's Guide

## What Is It?
[Simple explanation]

## Why Does It Matter?
[Importance]

## How Does It Work?
[Step-by-step breakdown]

## Real-World Examples
[Practical applications]

## Common Misconceptions
[Address confusion]

## Getting Started
[Next steps]

## Resources for Learning
[Curated learning path]
```

---

## Obsidian Vault Structure

All outputs saved to your local Obsidian vault:

```
ObsidianVault/
├── research/
│   ├── 2025-11-17-quantum-computing/
│   │   ├── research-topic.md          # Metadata
│   │   ├── output.md                  # Generated output
│   │   ├── sources.md                 # All citations (28+)
│   │   ├── conflicts.md               # Detected conflicts (if any)
│   │   └── metadata.json              # Research metadata
│   │
│   ├── 2025-11-18-neural-networks/
│   │   └── ...
│   │
│   └── index.md                       # Research history
│
└── cache/                             # Research cache
    ├── web_search/
    ├── articles/
    ├── youtube/
    └── ...
```

---

## Configuration

### Required Environment Variables

```bash
# Brave Search API (already configured)
BRAVE_API_KEY_FREE=BSAfhmAUjm78j3TKqPkDlByE0ecpRt7
BRAVE_API_KEY_PRO=BSAwntGzdRA-yo5lL0O4eoDrSgr2nBk

# Obsidian (mandatory)
OBSIDIAN_VAULT_PATH=/Users/you/Documents/ObsidianVault

# Google Drive (optional)
GOOGLE_DRIVE_CREDENTIALS_PATH=.credentials/google_drive_credentials.json

# LLM API
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## Parameters

### Basic Parameters

```python
research_generic(
    topic: str,                        # REQUIRED: Research topic or question
    depth: str = "moderate",           # minimal, light, moderate, deep, extensive
    format: str = "summary",           # summary, report, qa, comparison, guide
    max_sources: int = 30,             # Maximum sources to aggregate
    obsidian_vault_path: str = None    # Path to Obsidian vault (REQUIRED)
)
```

### Advanced Parameters

```python
research_generic(
    topic: str,
    depth: str = "moderate",
    format: str = "summary",
    max_sources: int = 30,

    # Source filtering
    include_hackernews: bool = True,
    include_web_search: bool = True,
    include_articles: bool = True,
    include_obsidian: bool = True,     # MANDATORY
    include_google_drive: bool = True,
    include_youtube: bool = True,

    # Output customization
    word_count_target: int = 1000,     # Target length (flexible)
    technical_level: str = "moderate", # beginner, moderate, advanced, expert
    include_code_examples: bool = False,
    include_visualizations: bool = False,

    # Quality settings
    min_source_authority: float = 0.6, # Filter low-quality sources
    resolve_conflicts: bool = True,    # Auto-resolve conflicts
    verify_citations: bool = True,     # Verify URLs accessible

    # Storage
    obsidian_vault_path: str,          # REQUIRED
    save_to_obsidian: bool = True
)
```

---

## Output Customization

### Technical Level

```python
# Beginner (ELI5)
technical_level="beginner"
→ Simple language, analogies, no jargon

# Moderate (Default)
technical_level="moderate"
→ Some technical terms, explained when used

# Advanced
technical_level="advanced"
→ Technical terminology, assumes background knowledge

# Expert
technical_level="expert"
→ Specialized terminology, dense technical content
```

### Word Count Targets

```python
# Quick summary
word_count_target=500
→ Executive summary style

# Standard (Default)
word_count_target=1000
→ Balanced detail and brevity

# Comprehensive
word_count_target=2000
→ Deep dive with multiple sections

# Extensive
word_count_target=3000+
→ Research paper style
```

---

## Cost Breakdown

### Per Research Query (Moderate Depth)

| Component | Cost | Notes |
|-----------|------|-------|
| HackerNews API | $0.00 | Free |
| Brave Search (PRO) | $0.04 | 8 queries × $0.005 |
| Article Extraction | $0.00 | Local processing |
| Obsidian Search | $0.00 | Local |
| Google Drive API | $0.00 | Free quota |
| YouTube Transcripts | $0.00 | Free |
| **Research Subtotal** | **$0.04** | |
| LLM (Output Generation) | $0.08-0.12 | Varies by format/length |
| **TOTAL** | **~$0.12-0.16** | |

### Cost by Output Format

| Format | Word Count | LLM Cost | Total Cost |
|--------|------------|----------|------------|
| **Summary** | 500-1000 | ~$0.08 | ~$0.12 |
| **Technical Report** | 1500-2000 | ~$0.12 | ~$0.16 |
| **Q&A** | 800-1200 | ~$0.09 | ~$0.13 |
| **Comparison** | 1000-1500 | ~$0.10 | ~$0.14 |
| **Beginner's Guide** | 1200-1800 | ~$0.11 | ~$0.15 |

---

## Performance Targets

| Phase | Target | Expected |
|-------|--------|----------|
| Research (6 sources) | <90s | 75-90s |
| Aggregation | <30s | 20-30s |
| Output Generation | <60s | 30-60s |
| Storage | <5s | 2-5s |
| **Total End-to-End** | **<3 min** | **2-3 min** |

---

## Quality Assurance

### Conflict Detection

```markdown
## Detected Conflicts

### Conflict 1: Transformer Architecture Publication Date
**Severity:** Low
**Type:** Temporal

**Source A (arxiv.org):**
"Attention Is All You Need" published June 2017

**Source B (Wikipedia):**
Published December 2017

**Resolution:**
ArXiv preprint: June 2017, Official publication: December 2017 (NIPS)
Using June 2017 as first publication.

**Confidence:** 95%
```

### Citation Verification

All citations are verified for:
- ✅ URL accessibility (HTTP 200 status)
- ✅ Domain authority (prefer .edu, arxiv, official docs)
- ✅ Publication date (recent preferred)
- ✅ Author credibility (when available)

### Source Authority Ranking

```python
Authority Scores:
- arxiv.org: 0.95
- *.edu: 0.90
- github.com: 0.85
- openai.com: 0.90
- medium.com: 0.60
- reddit.com: 0.50
```

---

## Example Workflows

### 1. Quick Fact-Check

```bash
# Minimal research, summary output
/research-generic "What is the capital of France?" --depth minimal
```

**Time:** ~60 seconds
**Cost:** ~$0.10
**Output:** Brief factual answer with sources

---

### 2. Technical Deep Dive

```bash
# Deep research, technical report
/research-generic "How does RLHF work in language models?" \
  --depth deep \
  --format report \
  --technical-level advanced
```

**Time:** ~3 minutes
**Cost:** ~$0.18
**Output:** Comprehensive technical report (2000+ words)

---

### 3. Comparative Analysis

```bash
# Moderate research, comparison format
/research-generic "RAG vs Fine-tuning for domain adaptation" \
  --depth moderate \
  --format comparison
```

**Time:** ~2 minutes
**Cost:** ~$0.14
**Output:** Side-by-side comparison with recommendations

---

### 4. Learning Resource

```bash
# Light research, beginner guide
/research-generic "Explain neural networks" \
  --depth light \
  --format guide \
  --technical-level beginner
```

**Time:** ~90 seconds
**Cost:** ~$0.12
**Output:** ELI5-style guide with learning path

---

### 5. Literature Review

```bash
# Extensive research, technical report
/research-generic "Recent advances in multimodal AI (2024)" \
  --depth extensive \
  --format report \
  --technical-level expert \
  --word-count 3000
```

**Time:** ~4 minutes
**Cost:** ~$0.22
**Output:** Academic-style literature review

---

## Data Models

### Research Query (Input)

```python
{
    "topic": "What are embeddings in machine learning?",
    "depth": "moderate",
    "format": "summary",
    "technical_level": "moderate",
    "word_count_target": 1000,
    "include_sources": {
        "hackernews": true,
        "web_search": true,
        "articles": true,
        "obsidian": true,
        "google_drive": true,
        "youtube": true
    },
    "obsidian_vault_path": "/Users/you/Documents/ObsidianVault"
}
```

### Research Output (Result)

```python
{
    "topic": "What are embeddings in machine learning?",
    "generated_at": "2025-11-17T14:35:22Z",
    "format": "summary",

    "output": {
        "title": "Embeddings in Machine Learning: A Comprehensive Overview",
        "content": "[Full generated content]",
        "word_count": 1247,
        "sections": [
            {"heading": "Executive Summary", "content": "..."},
            {"heading": "Key Findings", "content": "..."},
            {"heading": "Detailed Analysis", "content": "..."}
        ]
    },

    "research_summary": {
        "total_sources": 28,
        "sources_by_type": {
            "hackernews": 10,
            "web": 8,
            "articles": 5,
            "obsidian": 3,
            "google_drive": 2,
            "youtube": 0
        },
        "key_facts": ["...", "...", "..."],
        "conflicts_detected": 1,
        "conflicts_resolved": 1
    },

    "quality_metrics": {
        "avg_source_authority": 0.82,
        "citation_verification_rate": 1.0,
        "conflict_resolution_confidence": 0.91
    },

    "obsidian_path": "research/2025-11-17-embeddings-ml",
    "execution_time_seconds": 142.3,
    "total_cost_usd": 0.14
}
```

---

## Common Pitfalls

### ❌ Vague Research Topics
```bash
# BAD: Too broad
/research-generic "AI"

# GOOD: Specific
/research-generic "How do transformer attention mechanisms work?"
```

### ❌ Wrong Depth for Task
```bash
# BAD: Deep research for simple fact
/research-generic "What is Python?" --depth extensive

# GOOD: Minimal for simple facts
/research-generic "What is Python?" --depth minimal
```

### ❌ Format Mismatch
```bash
# BAD: Comparison format for single topic
/research-generic "What are embeddings?" --format comparison

# GOOD: Summary for single topic
/research-generic "What are embeddings?" --format summary
```

### ❌ Not Specifying Obsidian Path
```bash
# BAD: No vault path (will fail)
/research-generic "Neural networks"

# GOOD: Include vault path
/research-generic "Neural networks" --vault /path/to/vault
```

---

## Integration with Existing Tools

### Use as Research Base for Content Generation

```bash
# Step 1: Research the topic
/research-generic "Why learn embeddings?" --depth deep

# Step 2: Review research in Obsidian (research/2025-11-17-embeddings/output.md)

# Step 3: Use research as input for content generation
/research-topic "Why learn embeddings?"  # Uses cached research
```

### Combine with Voice Matching

```bash
# Research first (generic)
/research-generic "Constitutional AI" --depth moderate

# Then generate voice-matched content
# (uses research from previous step automatically)
```

---

## Advanced Features

### Source Filtering

```python
# Only use high-authority sources
research_generic(
    topic="Latest AI research",
    min_source_authority=0.85  # Only .edu, arxiv, official docs
)
```

### Custom Templates

```python
# Use custom output template
research_generic(
    topic="Transformers architecture",
    format="custom",
    template_path="templates/my-template.md"
)
```

### Conflict Resolution Strategies

```python
# Manual conflict review
research_generic(
    topic="AI safety",
    resolve_conflicts=False  # Flag for user review
)

# Auto-resolve with preferences
research_generic(
    topic="AI safety",
    conflict_resolution_strategy="prefer_recent"  # or "prefer_authoritative"
)
```

---

## Success Criteria

### Research Quality
- ✅ 20+ sources aggregated
- ✅ Authority score >0.75
- ✅ Conflicts detected and resolved
- ✅ Citations verified 100%

### Performance
- ✅ Execution time <3 minutes
- ✅ Cost <$0.20 per query
- ✅ Cache hit rate >50%

### Output Quality
- ✅ Accurate and well-cited
- ✅ Appropriate technical level
- ✅ No hallucinations
- ✅ Proper formatting

---

## Troubleshooting

### Issue: "No sources found"
**Cause:** Topic too specific or niche
**Fix:** Broaden topic or reduce min_source_authority

### Issue: "Execution timeout"
**Cause:** Too many sources or slow APIs
**Fix:** Reduce max_sources or use lighter depth

### Issue: "Conflicting information"
**Cause:** Multiple contradictory sources
**Fix:** Review conflicts.md, adjust source authority filters

### Issue: "Output too technical/simple"
**Cause:** Wrong technical_level setting
**Fix:** Adjust technical_level parameter

---

## Differences from research-topic-merged.md

| Feature | Generic Consolidator | LinkedIn/Blog Consolidator |
|---------|---------------------|---------------------------|
| **Output Format** | Flexible (summary, report, Q&A, etc.) | Fixed (LinkedIn + Blog) |
| **Use Case** | Any research topic | Content marketing |
| **Drafts** | 1 output (customizable) | 6 drafts (3 LinkedIn + 3 Blog) |
| **Voice Matching** | Optional | Required |
| **Paraphrasing** | Not required | Required (plagiarism prevention) |
| **Word Count** | Flexible (500-3000+) | Fixed (LinkedIn 150-300, Blog 800-1500) |
| **Target Audience** | Researchers, learners, analysts | Content creators, marketers |

---

## When to Use Which

### Use Generic Consolidator When:
- ✅ Researching any topic (not just content creation)
- ✅ Need technical reports or analysis
- ✅ Want Q&A or comparison formats
- ✅ Doing academic or professional research
- ✅ Exploring a new domain
- ✅ Creating documentation

### Use LinkedIn/Blog Consolidator When:
- ✅ Creating social media content
- ✅ Writing blog posts for publication
- ✅ Need multiple draft variations
- ✅ Require voice matching
- ✅ Marketing or thought leadership content
- ✅ Need platform-optimized formatting

---

## References

- **Specialized Version:** `.claude/commands/research-topic-merged.md`
- **Brave API Config:** `docs/brave-api-configuration.md`
- **Coding Standards:** `CLAUDE.md`

---

**Status:** ✅ READY FOR USE
**Version:** 1.0
**Date:** 2025-11-17
