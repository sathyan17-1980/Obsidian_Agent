---
description: Multi-source research agent for any topic with flexible output formats
argument-hint: "[topic] [--depth minimal|light|moderate|deep|extensive] [--format summary|report|qa|comparison|guide]"
---

# Generic Research Consolidator

## Research Topic

$ARGUMENTS

---

## Your Task

Execute a comprehensive multi-source research workflow for the topic above. This is a generic research consolidator that supports flexible output formats.

### Step 1: Parse Arguments and Set Defaults

Parse the arguments from: **$ARGUMENTS**

Extract:
- **Topic**: The main research question/topic (REQUIRED)
- **Depth**: Research depth level (default: "moderate")
  - `minimal`: Quick fact-checking (~60s, 1-3 queries/source)
  - `light`: Basic research (~90s, 3-5 queries/source)
  - `moderate`: Standard research (~120s, 5-8 queries/source) - DEFAULT
  - `deep`: Comprehensive analysis (~180s, 8-12 queries/source)
  - `extensive`: Multi-topic deep dive (~240s, 12+ queries/source)

- **Format**: Output format (default: "summary")
  - `summary`: Research summary with key findings (default)
  - `report`: Technical report with methodology
  - `qa`: Q&A document with examples
  - `comparison`: Side-by-side comparison analysis
  - `guide`: Beginner's guide with learning path

- **Technical Level**: Content complexity (default: "moderate")
  - `beginner`: ELI5 style, simple language
  - `moderate`: Some technical terms, explained when used
  - `advanced`: Technical terminology, assumes background
  - `expert`: Specialized terminology, dense content

- **Word Count**: Target length (default: 1000)
  - 500: Executive summary
  - 1000: Balanced detail (default)
  - 2000: Comprehensive deep dive
  - 3000+: Research paper style

### Step 2: Verify Obsidian Vault Configuration

Check if OBSIDIAN_VAULT_PATH is configured:
- Read environment variables or .env file
- If not set, prompt user for vault path
- **CRITICAL**: Obsidian vault integration is MANDATORY

### Step 3: Execute Multi-Source Research (Parallel)

Research the topic across 6 sources in parallel:

1. **HackerNews Discussions**
   - Search for relevant HN threads
   - Extract key insights and debates
   - Capture community sentiment

2. **Web Search (Brave API)**
   - Use Brave Search API (PRO tier for deep/extensive)
   - Number of queries based on depth level
   - Extract high-quality web articles

3. **Full Article Content**
   - Extract full text from top articles
   - Parse markdown/HTML content
   - Capture code examples and visuals

4. **Obsidian Vault (MANDATORY)**
   - Semantic search with embeddings
   - Tag and frontmatter filtering
   - Find related existing notes

5. **Google Drive (if configured)**
   - Search PDFs, DOCX, Google Docs
   - Extract relevant content
   - Index for future searches

6. **YouTube Transcripts**
   - Search educational channels
   - Extract transcript content
   - Summarize key points

**Performance Target**: Complete all 6 sources in <90 seconds

### Step 4: Aggregate and Detect Conflicts

After gathering all sources:

1. **Aggregate Results**
   - Combine findings from all 6 sources
   - Deduplicate semantically similar content
   - Rank by source authority

2. **Detect Conflicts**
   - Identify contradictory information
   - Note temporal conflicts (dates, versions)
   - Flag factual discrepancies

3. **Resolve Conflicts**
   - Prefer higher authority sources (.edu, arxiv, official docs)
   - Prefer more recent information
   - Note unresolved conflicts for user review

4. **Verify Citations**
   - Check URL accessibility (HTTP 200)
   - Verify domain authority
   - Include publication dates when available

### Step 5: Generate Output in Requested Format

Based on the `format` parameter, generate appropriate output:

#### Format: Summary (Default)
```markdown
# {Topic}

## Executive Summary
[200-300 word overview]

## Key Findings
- Finding 1 (with citation)
- Finding 2 (with citation)
- Finding 3 (with citation)

## Detailed Analysis
### [Section 1 Name]
[Content with inline citations]

### [Section 2 Name]
[Content with inline citations]

## Conflicts & Resolutions
[Any conflicts detected and how resolved]

## Sources
[All citations numbered and linked]
```

#### Format: Technical Report
```markdown
# {Topic}: Technical Report

## Abstract
[Brief overview]

## Introduction
[Background and context]

## Methodology
[How research was conducted - mention 6 sources]

## Findings
[Detailed results organized by theme]

## Discussion
[Analysis and interpretation]

## Conclusions
[Summary and recommendations]

## References
[All sources, properly formatted]
```

#### Format: Q&A Document
```markdown
# {Topic}: Questions & Answers

## Main Question
{User's topic/question}

## Answer
[Comprehensive answer with examples]

## Key Points
- Point 1
- Point 2
- Point 3

## Examples
[Real-world examples and applications]

## Common Misconceptions
[Address misunderstandings]

## Related Questions
- Related question 1
- Related question 2

## Further Reading
[Curated sources for deep dive]
```

#### Format: Comparison
```markdown
# {Option A} vs {Option B}

## Overview
[Brief comparison summary]

## Feature Comparison
| Feature | Option A | Option B |
|---------|----------|----------|
| ... | ... | ... |

## Pros & Cons
### {Option A}
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

### {Option B}
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

## Recommendations
[Use case guidance - when to use each]

## Sources
[All citations]
```

#### Format: Beginner's Guide
```markdown
# {Topic}: A Beginner's Guide

## What Is It?
[Simple explanation without jargon]

## Why Does It Matter?
[Importance and real-world relevance]

## How Does It Work?
[Step-by-step breakdown with analogies]

## Real-World Examples
[Practical applications]

## Common Misconceptions
[Address confusion points]

## Getting Started
[Next steps for learning]

## Resources for Learning
[Curated learning path]
```

**Quality Requirements:**
- Match requested technical level
- Target word count (±20%)
- All claims must have citations
- No hallucinations (only source-backed info)
- Proper markdown formatting

### Step 6: Save to Obsidian Vault

Create organized folder structure:

```
{OBSIDIAN_VAULT_PATH}/research/{YYYY-MM-DD}-{topic-slug}/
├── research-topic.md          # Metadata and request details
├── output.md                  # Generated output in requested format
├── sources.md                 # All citations and references
├── conflicts.md               # Detected conflicts (if any)
└── metadata.json              # Research metadata and stats
```

**Files to create:**

1. **research-topic.md**
```markdown
---
date: {timestamp}
topic: "{topic}"
depth: "{depth}"
format: "{format}"
status: completed
---

# Research Request

**Topic**: {topic}
**Depth**: {depth}
**Format**: {format}
**Generated**: {timestamp}

## Request Parameters
- Technical Level: {technical_level}
- Word Count Target: {word_count}
- Total Sources: {source_count}
- Execution Time: {duration}s
- Total Cost: ${cost}
```

2. **output.md** - The generated content in requested format

3. **sources.md** - All citations with metadata

4. **conflicts.md** - Detected conflicts and resolutions (if any)

5. **metadata.json** - Machine-readable research metadata

### Step 7: Report Results

After completing the research, provide a summary:

```markdown
## ✅ Research Complete

**Topic**: {topic}
**Format**: {format} ({word_count} words)
**Sources**: {total_sources} (HN: {hn}, Web: {web}, Articles: {articles}, Obsidian: {obs}, Drive: {drive}, YouTube: {yt})
**Conflicts**: {conflict_count} detected, {resolved_count} resolved
**Quality Score**: {avg_authority}/1.0

**Saved to Obsidian**:
- `{vault_path}/research/{date}-{slug}/output.md`
- `{vault_path}/research/{date}-{slug}/sources.md`

**Performance**:
- Research Time: {research_time}s
- Generation Time: {gen_time}s
- Total Time: {total_time}s
- Estimated Cost: ${cost}

**Next Steps**:
- Review output in Obsidian
- Check conflicts.md if unresolved conflicts exist
- Use for further content generation or analysis
```

---

## Important Notes

### Cost Efficiency
- **Minimal depth**: ~$0.10 (60s)
- **Light depth**: ~$0.12 (90s)
- **Moderate depth**: ~$0.15 (120s) - DEFAULT
- **Deep depth**: ~$0.18 (180s)
- **Extensive depth**: ~$0.20+ (240s)

### Best Practices
1. **Start with moderate depth** - good balance of quality and cost
2. **Use minimal for fact-checking** - quick and cheap
3. **Use deep/extensive for comprehensive research** - when quality > speed
4. **Match format to use case** - summary for general, report for technical, guide for learning
5. **Review conflicts.md** - manually verify unresolved conflicts

### Common Pitfalls to Avoid
- ❌ Vague topics ("AI" instead of "How do transformer attention mechanisms work?")
- ❌ Wrong depth (extensive for simple facts)
- ❌ Format mismatch (comparison for single topic)
- ❌ Missing Obsidian vault path (will fail)

### Integration with Other Commands
This command produces research that can be used as input for:
- Content generation workflows
- Voice-matched blog/LinkedIn posts
- Technical documentation
- Learning materials

---

## Validation

Before marking complete, verify:
- ✅ All 6 research sources were queried
- ✅ Output matches requested format
- ✅ Word count within ±20% of target
- ✅ All citations are valid and accessible
- ✅ Conflicts detected and resolved (or flagged)
- ✅ Files saved to Obsidian vault
- ✅ Proper markdown formatting
- ✅ Technical level matches request
- ✅ No hallucinations (all info source-backed)

---

## References

- **Full Documentation**: `.claude/commands/research-generic-consolidator.md`
- **Specialized Version**: `.claude/commands/research-topic-merged.md` (for LinkedIn/Blog)
- **Brave API Config**: `docs/brave-api-configuration.md`
- **Coding Standards**: `CLAUDE.md`
