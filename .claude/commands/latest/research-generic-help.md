# Research-Generic Command - Comprehensive Guide

**Command:** `/research-generic`
**Version:** 2.0 (with 21-point Quality Framework)
**Status:** Production Ready
**Last Updated:** 2025-11-30

---

## Overview

The **research-generic** command is a versatile multi-source research agent that conducts comprehensive research on any topic and generates flexible output formats. Unlike research-topic (which focuses on LinkedIn/Blog content), research-generic produces academic-style research outputs suitable for technical documentation, reports, and knowledge management.

### Key Capabilities

- **Multi-Source Research**: Simultaneously queries 6 different sources
- **Flexible Output Formats**: 5 different output styles (summary, report, qa, comparison, guide)
- **Adjustable Depth**: 5 research depth levels from minimal to extensive
- **Quality Framework**: 21-point quality standard ensuring research-backed content
- **Automatic PDF Generation**: Professional PDF output for sharing
- **Git Integration**: Automatic commit and push to repository
- **Obsidian Integration**: Saves all research to your vault with organized structure

---

## Quick Start

### Basic Usage

```bash
/research-generic "What are the latest developments in quantum computing?"
```

### With Options

```bash
/research-generic "RAG vs Fine-tuning" --depth deep --format comparison
```

### All Parameters

```bash
/research-generic "topic" --depth [minimal|light|moderate|deep|extensive] --format [summary|report|qa|comparison|guide]
```

---

## Command Parameters

### 1. Topic (REQUIRED)

The research question or topic to investigate.

**Best Practices:**
- ✅ Specific: "How do transformer attention mechanisms work?"
- ✅ Focused: "RAG vs Fine-tuning for LLMs"
- ❌ Vague: "AI" or "Machine Learning"

### 2. Depth (Optional, default: "moderate")

Controls research thoroughness and number of queries per source.

| Depth | Duration | Queries/Source | Cost | Use When |
|-------|----------|----------------|------|----------|
| `minimal` | ~60s | 1-3 | ~$0.10 | Quick fact-checking, simple topics |
| `light` | ~90s | 3-5 | ~$0.12 | Basic research, familiar topics |
| `moderate` | ~120s | 5-8 | ~$0.15 | Standard research (DEFAULT) |
| `deep` | ~180s | 8-12 | ~$0.18 | Complex topics, comprehensive analysis |
| `extensive` | ~240s | 12+ | ~$0.20+ | Research papers, multi-topic deep dives |

### 3. Format (Optional, default: "summary")

Output format style.

| Format | Description | Best For |
|--------|-------------|----------|
| `summary` | Research summary with key findings | General knowledge gathering |
| `report` | Technical report with methodology | Technical documentation |
| `qa` | Q&A document with examples | Educational content, FAQs |
| `comparison` | Side-by-side comparison | Evaluating options, alternatives |
| `guide` | Beginner's guide with learning path | Teaching, onboarding |

### 4. Technical Level (Optional, default: "moderate")

Content complexity and terminology.

| Level | Description | Audience |
|-------|-------------|----------|
| `beginner` | ELI5 style, simple language | Non-technical audience |
| `moderate` | Technical terms explained | General technical audience |
| `advanced` | Assumes technical background | Technical professionals |
| `expert` | Specialized terminology, dense | Domain experts, researchers |

### 5. Word Count (Optional, default: 1000)

Target output length.

| Count | Description | Use Case |
|-------|-------------|----------|
| 500 | Executive summary | Quick overview, briefings |
| 1000 | Balanced detail (DEFAULT) | Standard documentation |
| 2000 | Comprehensive deep dive | Detailed analysis |
| 3000+ | Research paper style | Academic, thorough coverage |

---

## Research Sources (6 Parallel)

The command queries **6 sources simultaneously** for comprehensive coverage:

### 1. HackerNews Discussions
- **What:** Community discussions and debates
- **Value:** Real-world insights, practitioner perspectives
- **Authority:** 0.50

### 2. Web Search (Brave API)
- **What:** High-quality web articles and documentation
- **Value:** Current information, official resources
- **Authority:** Varies by domain (.edu: 0.95, official docs: 0.90)

### 3. Full Article Content Extraction
- **What:** Complete text from top web articles
- **Value:** Detailed technical content, tutorials
- **Authority:** Same as source domain

### 4. Obsidian Vault (MANDATORY)
- **What:** Your personal notes and past research
- **Value:** Personalized context, existing knowledge
- **Authority:** 0.70
- **Note:** Vault path must be configured

### 5. Google Drive (Optional)
- **What:** Your documents (PDFs, DOCX, Google Docs)
- **Value:** Private research, team documents
- **Authority:** 0.75

### 6. YouTube Transcripts
- **What:** Educational video content
- **Value:** Visual explanations, tutorials
- **Authority:** 0.60

**Performance:** All 6 sources complete in <90 seconds

---

## 21-Point Quality Framework

All research outputs adhere to strict quality standards:

### Research Grounding (5 points)
1. Specific technical details (not generic claims)
2. Authority quotes that teach
3. Concrete examples from actual sources
4. Research depth shown through specifics
5. One memorable concrete example with data

### Citation Quality (5 points)
6. Exact attribution from analyzed sources
7. Actual URLs from research
8. Real statistics (traceable)
9. Every claim sourced
10. Inline citations throughout

### Technical Depth (4 points)
11. Concrete technical examples from sources
12. Specific details proving expertise
13. Realistic code examples
14. Clear memorable analogies

### Content Structure (4 points)
15. Real-world applications
16. Misconceptions addressed (guide/qa)
17. Specific named resources from research
18. "Why this matters" sections (guide/qa)

### Quality Validation (3 points)
19. Specific findings (not vague)
20. 8-10+ sources cited
21. Zero hallucinations (source-backed only)

---

## Output Formats Explained

### Summary Format (Default)

**Structure:**
- Executive Summary (200-300 words)
- Key Findings (bulleted)
- Detailed Analysis (sections with citations)
- Conflicts & Resolutions
- Sources (numbered)

**Best For:** General research, knowledge gathering, quick reference

**Example Use Case:**
```bash
/research-generic "What is semantic search?" --depth moderate --format summary
```

### Technical Report Format

**Structure:**
- Abstract
- Introduction (background)
- Methodology (6 sources explained)
- Findings (organized by theme)
- Discussion (analysis)
- Conclusions (recommendations)
- References

**Best For:** Technical documentation, formal reports, research papers

**Example Use Case:**
```bash
/research-generic "Vector database performance comparison" --depth deep --format report
```

### Q&A Format

**Structure:**
- Main Question
- Comprehensive Answer
- Key Points
- Real-world Examples
- Common Misconceptions
- Related Questions
- Further Reading

**Best For:** FAQs, educational content, documentation

**Example Use Case:**
```bash
/research-generic "How do embeddings work?" --depth moderate --format qa
```

### Comparison Format

**Structure:**
- Overview
- Feature Comparison (table)
- Pros & Cons (both options)
- Recommendations (use case guidance)
- Sources

**Best For:** Evaluating alternatives, technology decisions

**Example Use Case:**
```bash
/research-generic "RAG vs Fine-tuning" --depth deep --format comparison
```

### Beginner's Guide Format

**Structure:**
- What Is It? (simple explanation)
- Why Does It Matter?
- How Does It Work? (step-by-step)
- Real-World Examples
- Common Misconceptions
- Getting Started
- Resources for Learning

**Best For:** Teaching, onboarding, educational materials

**Example Use Case:**
```bash
/research-generic "Introduction to vector databases" --depth moderate --format guide
```

---

## Output Files & Structure

All research saves to organized folder in Obsidian vault:

```
{OBSIDIAN_VAULT_PATH}/research/{YYYY-MM-DD}-{topic-slug}/
├── research-topic.md          # Metadata and request details
├── output.md                  # Generated research in requested format
├── sources.md                 # All citations and references
├── conflicts.md               # Detected conflicts (if any)
├── metadata.json              # Machine-readable stats
└── {topic-slug}_research.pdf  # Professional PDF for sharing
```

### Also Creates:
- PDF in project root: `/home/user/Obsidian_Agent/{topic-slug}_research.pdf`
- Git commit with descriptive message
- Push to remote repository

---

## Advanced Features

### Conflict Detection & Resolution

The system automatically detects 4 types of conflicts:

1. **Factual Conflicts** (HIGH severity)
   - Example: "Transformers introduced in 2017" vs "2018"
   - Resolution: Prefer higher authority + more recent

2. **Temporal Conflicts** (MEDIUM severity)
   - Different dates for same event
   - Resolution: Check multiple sources, prefer official

3. **Definitional Conflicts** (MEDIUM severity)
   - Different definitions of same term
   - Resolution: Use most authoritative source

4. **Opinion Conflicts** (LOW severity)
   - Differing opinions on best practices
   - Resolution: Present both perspectives

**Unresolved conflicts** are flagged in `conflicts.md` for manual review.

### Source Authority Ranking

Sources ranked by reliability:

- **0.95** - arxiv.org, .edu domains
- **0.90** - Official documentation, openai.com
- **0.85** - GitHub repositories
- **0.75** - Google Drive (your documents)
- **0.70** - Obsidian vault (your notes)
- **0.60** - YouTube, Medium
- **0.50** - Reddit, HackerNews

Higher authority sources win during conflict resolution.

### Deduplication

**Semantic Deduplication:**
- Similarity >0.90 = duplicate
- Keeps highest authority version

**URL Deduplication:**
- Same URL from different sources = merged
- Prefers full article over snippet

**Result:** 20-40 unique sources (from 28-50+ total)

---

## Cost & Performance

### Cost by Depth

| Depth | Total Cost | API Calls | LLM Tokens |
|-------|-----------|-----------|------------|
| minimal | ~$0.10 | Low | ~5K |
| light | ~$0.12 | Medium | ~8K |
| moderate | ~$0.15 | Medium | ~12K |
| deep | ~$0.18 | High | ~18K |
| extensive | ~$0.20+ | Very High | ~25K+ |

### Performance Targets

| Phase | Target Time |
|-------|-------------|
| Research (6 sources) | <90s |
| Aggregation & Dedup | <30s |
| Content Generation | <60s |
| Storage | <5s |
| **Total** | **<3 minutes** |

### ROI vs Manual Research

- **120x faster** (6 hours → 3 minutes)
- **1,667x cheaper** ($300 → $0.18)
- **3-6x more sources** (28+ vs 5-10 manual)

---

## Prerequisites

### Required

1. **Obsidian Vault Path**
   - Set `OBSIDIAN_VAULT_PATH` environment variable
   - Or provide when prompted
   - **CRITICAL:** Research cannot proceed without this

2. **API Keys**
   - `BRAVE_API_KEY_FREE` and/or `BRAVE_API_KEY_PRO`
   - `ANTHROPIC_API_KEY` (or equivalent LLM API)

### Optional

3. **Google Drive**
   - `GOOGLE_DRIVE_CREDENTIALS_PATH` for OAuth
   - Enables Drive search integration

4. **Dependencies**
   - newspaper3k (article extraction)
   - youtube-transcript-api (video transcripts)
   - weasyprint (PDF generation)

---

## Usage Examples

### Example 1: Quick Fact Check
```bash
/research-generic "What is the capital of quantum computing research?" --depth minimal
```
- **Duration:** ~60s
- **Cost:** ~$0.10
- **Output:** Quick summary with 3-5 sources

### Example 2: Technical Documentation
```bash
/research-generic "How do vector databases handle approximate nearest neighbor search?" --depth deep --format report
```
- **Duration:** ~180s
- **Cost:** ~$0.18
- **Output:** Comprehensive technical report with 8-12 sources

### Example 3: Comparison Research
```bash
/research-generic "Pinecone vs Weaviate vs Qdrant" --depth deep --format comparison
```
- **Duration:** ~180s
- **Cost:** ~$0.18
- **Output:** Side-by-side comparison with pros/cons

### Example 4: Beginner's Guide
```bash
/research-generic "Introduction to embeddings" --depth moderate --format guide
```
- **Duration:** ~120s
- **Cost:** ~$0.15
- **Output:** Step-by-step beginner-friendly guide

### Example 5: Q&A Documentation
```bash
/research-generic "Why use semantic search instead of keyword search?" --depth moderate --format qa
```
- **Duration:** ~120s
- **Cost:** ~$0.15
- **Output:** Question-answer format with examples

---

## Common Use Cases

### 1. Technical Research
- **Scenario:** Understanding new technology or framework
- **Command:** `--depth deep --format report`
- **Output:** Comprehensive technical documentation

### 2. Decision Making
- **Scenario:** Choosing between alternatives
- **Command:** `--depth deep --format comparison`
- **Output:** Feature comparison with recommendations

### 3. Knowledge Base Building
- **Scenario:** Creating documentation for team
- **Command:** `--depth moderate --format summary`
- **Output:** Well-organized knowledge base article

### 4. Learning & Teaching
- **Scenario:** Creating educational materials
- **Command:** `--depth moderate --format guide`
- **Output:** Beginner-friendly learning guide

### 5. Quick Lookups
- **Scenario:** Verifying facts or definitions
- **Command:** `--depth minimal --format summary`
- **Output:** Quick reference with key facts

---

## Validation Checklist

Before marking research complete, system verifies:

- ✅ All 6 research sources queried (or attempted)
- ✅ Output matches requested format
- ✅ Word count within ±20% of target
- ✅ All citations valid and accessible
- ✅ Conflicts detected and resolved (or flagged)
- ✅ Files saved to Obsidian vault
- ✅ Proper markdown formatting
- ✅ Technical level matches request
- ✅ No hallucinations (all info source-backed)
- ✅ PDF file created and readable
- ✅ PDF committed and pushed to git

---

## Best Practices

### Research Topics

**✅ DO:**
- Be specific: "How do HNSW algorithms work?"
- Focus on single question: "What is RAG?"
- Use technical terms if needed: "Transformer attention mechanisms"

**❌ DON'T:**
- Be vague: "AI stuff"
- Ask multiple questions: "What is AI and how does ML work?"
- Use overly broad topics: "Computer Science"

### Depth Selection

**Use minimal when:**
- Quick fact-checking
- Testing the system
- Time-sensitive research

**Use moderate when:**
- Standard documentation needs
- Balanced quality/speed required
- Most use cases (DEFAULT)

**Use deep/extensive when:**
- Complex technical topics
- High-quality output critical
- Comprehensive coverage needed

### Format Selection

| If You Need... | Use Format |
|----------------|------------|
| General knowledge | `summary` |
| Formal documentation | `report` |
| FAQ or educational | `qa` |
| Choose between options | `comparison` |
| Teaching materials | `guide` |

---

## Common Pitfalls to Avoid

### 1. Wrong Depth Level
❌ Using `extensive` for simple facts → wastes time/money
✅ Match depth to complexity

### 2. Missing Obsidian Path
❌ Not configuring vault path → research fails
✅ Set `OBSIDIAN_VAULT_PATH` before starting

### 3. Format Mismatch
❌ Using `comparison` for single topic → awkward output
✅ Use `summary` or `report` for single topics

### 4. Vague Topics
❌ "Tell me about AI" → too broad, unfocused
✅ "How do transformer attention mechanisms work?" → specific

### 5. Ignoring Conflicts
❌ Not reviewing `conflicts.md` → may have incorrect info
✅ Always check for unresolved conflicts

---

## Troubleshooting

### "Obsidian vault path not configured"
**Solution:** Set environment variable or provide when prompted
```bash
export OBSIDIAN_VAULT_PATH="/path/to/vault"
```

### "No results from web search"
**Solution:**
- Check API keys are valid
- Try broader search terms
- Increase depth level

### "PDF generation failed"
**Solution:**
```bash
pip install weasyprint
```

### "Git push failed (403)"
**Solution:** Verify branch name starts with `claude/` and ends with session ID

### "Research taking too long"
**Solution:**
- Reduce depth level
- Check internet connection
- Some sources may be slow (normal for extensive depth)

---

## Technical Architecture

### Research Flow

```
1. Parse Arguments → Validate parameters
2. Check Prerequisites → Verify vault path, API keys
3. Execute Research → 6 sources in parallel (<90s)
4. Aggregate Results → Deduplicate, rank by authority
5. Detect Conflicts → Find contradictions
6. Resolve Conflicts → Use authority + recency
7. Generate Output → Format-specific content
8. Validate Quality → 21-point framework
9. Save to Obsidian → Organized structure
10. Generate PDF → Professional format
11. Git Operations → Commit and push
12. Report Results → Summary to user
```

### Technologies Used

- **Research:** Brave Search API, HackerNews API, YouTube API
- **Extraction:** newspaper3k, BeautifulSoup, custom parsers
- **Search:** Semantic search with embeddings (Obsidian)
- **Quality:** Sentence transformers, plagiarism detection
- **Output:** Markdown, HTML, PDF (weasyprint)
- **Storage:** File system, Obsidian vault, Git

---

## Differences from research-topic

| Feature | research-generic | research-topic |
|---------|-----------------|----------------|
| **Purpose** | General research | LinkedIn/Blog content |
| **Output Formats** | 5 formats (summary, report, qa, comparison, guide) | 2 platforms (LinkedIn posts, Blog articles) |
| **Drafts** | 1 output in requested format | 3 drafts per platform (6 total) |
| **Voice Matching** | Not applicable | User's writing style |
| **Personal Branding** | Not applicable | 7 branding elements |
| **Series Continuity** | Not applicable | Weekly series linking |
| **Word Count** | 500-3000+ (flexible) | Fixed (150-300 LinkedIn, 800-1500 Blog) |
| **Quality Framework** | 21 points (research quality) | 55 points (research + branding) |
| **Use Case** | Technical docs, research | Social media, thought leadership |

**Key Insight:** Use `research-generic` for objective research outputs. Use `research-topic` for personal brand building.

---

## Updates & Changelog

### Version 2.0 (2025-11-30)
- ✅ Added 21-point quality framework
- ✅ Enhanced citation standards
- ✅ Format-specific quality applications
- ✅ Technical level adjustments

### Version 1.0 (2025-11-17)
- Initial release with 6-source research
- 5 output formats
- PDF generation
- Git integration

---

## Support & Resources

### Documentation
- Full command spec: `.claude/commands/research-generic.md`
- Consolidator docs: `.claude/commands/research-generic-consolidator.md`
- Brave API setup: `docs/brave-api-configuration.md`

### Related Commands
- `/research-topic` - LinkedIn/Blog content generation
- `/core_commands:planning` - Feature planning

### Questions?
- Check command file: `.claude/commands/research-generic.md`
- Review examples in this guide
- Test with `--depth minimal` first

---

## License & Credits

Part of the Obsidian Agent project.
Powered by Brave Search, Claude AI, and open-source tools.

**Created:** 2025-11-17
**Last Updated:** 2025-11-30
**Version:** 2.0
