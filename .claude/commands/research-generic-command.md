---
description: Multi-source research agent for any topic with flexible output formats
argument-hint: "[topic] [--depth minimal|light|moderate|deep|extensive] [--format summary|report|qa|comparison|guide] [--deep-research] [--linkedin] [--blog] [--branding]"
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

**NEW: Research Mode Flag:**

- **--deep-research**: Enable iterative, multi-round research exploration - OPTIONAL
  - **When ABSENT (default)**: Use 6-source parallel approach (fast, predictable)
    - Execution time: 60-240 seconds (based on depth level)
    - Queries all 6 sources in parallel: HN, Web, Articles, Obsidian, Drive, YouTube
    - Structured, predictable output
    - Best for: Most research needs, time-sensitive work, known topics

  - **When PRESENT**: Use Task tool with specialized research agent (thorough, adaptive)
    - Execution time: 5-15 minutes
    - Iterative exploration: Follows interesting threads, refines questions
    - Dynamic source selection: Chooses sources based on discoveries
    - Multi-hop reasoning: "To understand X, first need Y"
    - Better conflict resolution through deeper investigation
    - Best for: Complex topics, contradictory information, cutting-edge research, comprehensive analysis

  - **Tradeoff**: Speed vs. thoroughness - use `--deep-research` when quality > speed

**NEW: Optional Content Generation Flags:**

- **--linkedin**: Generate LinkedIn post (150-300 words) - OPTIONAL
  - Only include if user wants shareable LinkedIn content
  - When present: Generate informative LinkedIn post after research
  - When absent: Skip LinkedIn generation

- **--blog**: Generate blog article (800-1500 words) - OPTIONAL
  - Only include if user wants blog content
  - When present: Generate comprehensive blog article after research
  - When absent: Skip blog generation

- **--branding**: Apply personal branding framework - OPTIONAL
  - Only relevant when --linkedin or --blog is present
  - When present: Apply personal voice, series continuity, expert positioning
  - When absent: Generate objective, informative content without personal voice
  - NOTE: Requires --linkedin or --blog to have any effect

**Example Commands:**
```bash
# Just research, no content (fast - default)
/research-generic "transformer architecture" --format summary

# Deep research for complex topic (5-15 min)
/research-generic "how do attention mechanisms differ across transformer variants" --deep-research --format report

# Research + LinkedIn (no personal branding)
/research-generic "transformer architecture" --format report --linkedin

# Deep research + LinkedIn + Blog with personal branding
/research-generic "why learn embeddings" --deep-research --format guide --linkedin --blog --branding

# Research + Blog only
/research-generic "vector databases comparison" --format comparison --blog
```

### Step 2: Verify Obsidian Vault Configuration

Check if OBSIDIAN_VAULT_PATH is configured:
- Read environment variables or .env file
- If not set, prompt user for vault path
- **CRITICAL**: Obsidian vault integration is MANDATORY

### Step 3: Execute Multi-Source Research

**First, check if `--deep-research` flag is present in $ARGUMENTS:**

#### Option A: Deep Research Mode (if --deep-research flag present)

If `--deep-research` flag is detected, use the Task tool to launch a specialized research agent for iterative exploration:

**Approach:**
- Use Task tool with subagent_type="Explore" or subagent_type="general-purpose"
- Agent performs multi-round research with dynamic source selection
- Follows interesting threads discovered during initial research
- Refines questions based on findings
- Deep dives into contradictions and gaps
- Synthesizes comprehensive understanding

**Agent Prompt Template:**
```
Research the following topic comprehensively using iterative exploration:

**Topic**: {topic}
**Depth Target**: {depth level}
**Format Needed**: {format}
**Technical Level**: {technical_level}

Use the following approach:
1. Initial broad search across multiple sources (web, documentation, papers)
2. Identify key subtopics and knowledge gaps
3. Follow interesting threads with focused follow-up searches
4. Resolve contradictions by consulting authoritative sources
5. Gather concrete examples, technical details, benchmarks, and quotes
6. Synthesize findings into structured output matching {format}

Quality requirements:
- Concrete examples (not vague statements)
- Detailed explanations with technical depth
- All claims must have citations
- Include specific versions, numbers, algorithms
- Authority quotes from primary sources

Return comprehensive research findings ready for {format} output generation.
```

**Expected outcome**: Agent returns detailed research findings after 5-15 minutes of iterative exploration.

**Skip to Step 4** after receiving agent results.

---

#### Option B: Fast Parallel Research (default - if --deep-research flag absent)

If `--deep-research` flag is NOT present, use the standard 6-source parallel approach:

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

---

### Quality Standards for Research Output

Apply these quality standards to ALL research outputs (regardless of format or flags):

**1. Concrete vs. Vague Examples:**

Always provide specific, concrete examples rather than vague generalizations.

- ❌ **Vague**: "Vector databases are fast"
- ✅ **Concrete**: "searching through 10 million document embeddings takes just 80 milliseconds. This is due to algorithms like HNSW (Hierarchical Navigable Small World)"

- ❌ **Vague**: "Embeddings have many dimensions"
- ✅ **Concrete**: "1536 dimensions has become the industry standard—especially with OpenAI's text-embedding-ada-002 model. While 1536 has become the industry standard, some are moving to 3072 dimensions for even higher precision, and some lightweight models use just 384 dimensions for speed-critical applications"

- ❌ **Vague**: "Vector databases help with AI applications"
- ✅ **Concrete**: "Vector databases is one of the reasons Retrieval-Augmented Generation (RAG) do not hallucinate, grounding LLM responses in actual data. This is one of the reasons we are able to build Smart assistants that remember context, able to understand meaning"

**2. High-level vs. Detailed Explanations:**

Provide detailed explanations with technical depth, not just high-level overviews.

- ❌ **High-level**: "Vector databases store embeddings in multiple dimensions"
- ✅ **Detailed**: "The word 'king' is represented as a single vector with 1536 dimensions. Each dimension captures different abstract patterns—potentially gender associations, formality, historical context, royalty, and hundreds of other nuanced features. For eg. the 1st dimension could store 'How masculine vs feminine?', the second dimension could store 'How formal is this?' and so on for each of the 1536 dimensions"

- ❌ **High-level**: "Dimension choice affects performance"
- ✅ **Detailed**: "The dimension being chosen is a trade-off between accuracy, speed, and cost. While 1536 has become the industry standard, some are moving to 3072 dimensions for even higher precision, and some lightweight models use just 384 dimensions for speed-critical applications"

- ❌ **High-level**: "Vector databases enable fast search"
- ✅ **Detailed**: "When you search, the search query is converted into a vector with the same 1536 dimensions. The vector database then calculates which stored vectors are closest in this dimensional space using similarity measures and returns the most relevant matches. The speed is amazing: searching through 10 million document embeddings takes just 80 milliseconds"

**3. Citation Requirements:**

- ALL factual claims must have citations
- Include specific quotes from authoritative sources when possible
- Format: "As [Source] puts it, '[exact quote]'" or [Fact (Source, Year)]
- Prefer primary sources over secondary (.edu, arxiv, official documentation)
- Include publication dates when available

**4. Technical Details:**

Include specific technical details rather than generic descriptions:

- Specific versions: "Python 3.11+, PyTorch 2.0, CUDA 11.8"
- Concrete numbers: "1536-dimensional vectors", "10ms latency", "95% recall"
- Named algorithms: "HNSW (Hierarchical Navigable Small World)", "cosine similarity", "k-NN search"
- Exact terminology: "semantic search", "embedding space", "vector similarity"

**Apply these standards to:**
- Research summaries
- Technical reports
- Q&A documents
- Comparison analyses
- Beginner's guides

**Do NOT apply personal branding elements** (see Personal Branding Mode below) **unless --linkedin or --blog flags are present with --branding flag**.

---

### Personal Branding Mode (Optional Enhancement)

**When to use:** If you're creating content for personal brand building (educational content, thought leadership, teaching).

**Applicable formats:** Guide, Q&A, Summary (when publishing)

**How to enable:** Add `--branding` flag to command, or manually enhance output with these requirements.

**Required Elements for Personal Branding:**

1. **Personal Framing (Opening)** - Establish credibility
   - "My friends/colleagues have often asked me about {topic}..."
   - "After working with {topic}, I'm frequently asked..."
   - Shows people seek YOU for knowledge

2. **Educational Series Context** - Position as guide
   - "This is part of my weekly AI series..."
   - "Building on last week's post on {previous topic}..."
   - You're leading a learning journey

3. **Concrete Examples with Quotes** - Show depth
   - Specific technical examples: "king" - "man" + "woman" = "queen"
   - Authority quotes: "As Cloudflare puts it, '{exact quote}'"
   - Code snippets, mathematical illustrations
   - Proves deep understanding, not surface knowledge

4. **"Why This Matters for YOU" Section** - Practical value
   - Explicit section addressing reader's goals
   - Connect to outcomes: "This means you can build..."
   - Expert positioning: "difference between copying code and architecting solutions"

5. **Actionable Resources** - Enable learning
   - Specific named resources: "Google's ML Crash Course"
   - Free courses with exact names and links
   - Tools and platforms to try
   - Not generic: "there are courses" ❌ | "Google's ML Crash Course offers..." ✅

6. **Expert Positioning Language**
   - "Understanding this is the difference between {novice} and {expert}"
   - "Real practitioners know that..."
   - "What separates beginners from architects is..."

7. **Series Continuity** - Build engagement
   - End with: "In next week's post, I'll explain {next topic}..."
   - Create anticipation for ongoing readership
   - Show learning progression

**Enhanced Guide Format with Personal Branding:**

```markdown
# Why Every {Audience} Should Master {Topic}: A Practitioner's Guide

## My Journey with {Topic}
[Personal framing: "Colleagues have asked me..." + Series context]

## What Is {Topic}? (The Fundamentals)
[Definition with concrete example]
[Authority quote: "As {Source} puts it, '{exact quote}'"]
[Technical illustration or code example]

## Why This Matters for You
[Explicit section on practical value]
[3-5 concrete use cases with specifics]
[Expert positioning: "difference between copying and architecting"]

## How {Topic} Works (Technical Breakdown)
[Step-by-step with technical details]
[Common misconceptions addressed]

## Getting Started: Your Learning Path
[Specific named resources:]
- "{Exact Course Name} offers hands-on tutorials"
- "{Specific Documentation} provides excellent guide"
- "Try {Specific Tool/Platform} for practice"

## Key Takeaways
- [Specific, actionable points, NOT generic]
- [With concrete examples and outcomes]

## What's Next in This Series
["In next week's article, I'll explore {next topic}..."]

## Additional Reading
- [{Resource 1}]({URL}) - {Description}
- [{Resource 2}]({URL}) - {Description}
```

**Anti-Patterns to Avoid:**
- ❌ Generic educational tone without personal framing
- ❌ High-level vague statements without concrete examples
- ❌ No authority quotes or specific sources
- ❌ Missing "why this matters" practical value
- ❌ Generic "there are resources" instead of specific named courses
- ❌ No expert positioning language
- ❌ Standalone content with no series continuity

**Quality Requirements:**
- Match requested technical level
- Target word count (±20%)
- All claims must have citations
- No hallucinations (only source-backed info)
- Proper markdown formatting

---

### Step 6: Optional LinkedIn Post Generation (Conditional)

**ONLY execute this step if `--linkedin` flag is present in $ARGUMENTS**

If `--linkedin` flag is detected, generate a LinkedIn post (150-300 words) based on the research findings.

#### Check for Branding Flag

- If `--branding` flag is ALSO present: Apply personal branding framework (7 elements from Personal Branding Mode section)
- If `--branding` flag is NOT present: Generate informative, objective LinkedIn post without personal voice

#### LinkedIn Post Structure (WITHOUT --branding)

```markdown
# {Topic}: Key Insights

## The Challenge
[Brief problem statement or context - 2-3 sentences]

## What the Research Shows
[3-5 key findings from research, with specific examples]
- Finding 1 (with concrete example)
- Finding 2 (with data/quote)
- Finding 3 (with technical detail)

## Why This Matters
[Practical implications - 2-3 sentences]

## Key Takeaway
[One memorable insight or actionable point]

---
**Word count:** 150-300 words
**Hashtags:** #{relevant} #{technology} #{topics}
**Sources:** [Top 3 sources cited]
```

#### LinkedIn Post Structure (WITH --branding)

When `--branding` flag is present, apply all 7 personal branding elements:

```markdown
# Why Every {Audience} Should Understand {Topic}

## Personal Framing
"My colleagues have frequently asked me about {topic}, so I'm sharing key insights from my research..."
[Establish credibility - people seek YOU for knowledge]

## The Hook
{Concrete question or surprising fact from research}
"Did you know that {specific concrete example}?"

## The Core Insight
[Authority quote]: "As {Source} puts it, '{exact quote}'"
[Concrete example]: {Specific technical detail or code example}
[Why it matters]: "This means you can {practical outcome}..."

## Expert Positioning
"Understanding this is the difference between {copying code} and {architecting solutions}."
"What separates beginners from practitioners is {specific knowledge}..."

## Actionable Resources
Based on my research, here are specific resources:
- {Exact Course/Resource Name} offers {specific benefit}
- {Specific Documentation} provides {concrete value}

## Series Continuity
"This is part of my weekly series on {topic}. In next week's post, I'll explore {next topic}..."

## Key Takeaways
- {Specific, actionable point with concrete example}
- {Another specific point with data}
- {Third point with technical detail}

---
**Word count:** 200-300 words
**Hashtags:** #{relevant} #{technology} #{topics}
**Additional Reading:** [Links to top sources]
```

#### LinkedIn Post Quality Checklist

- ✅ 150-300 word count
- ✅ Concrete examples (not vague statements)
- ✅ At least 1 specific quote or data point
- ✅ Technical details (versions, numbers, algorithms)
- ✅ Practical value clearly stated
- ✅ Proper markdown formatting
- ✅ Sources cited (minimum 2-3)
- ✅ If --branding: All 7 personal branding elements present
- ✅ If no --branding: Objective, informative tone

#### Save LinkedIn Post

Create file: `{OBSIDIAN_VAULT_PATH}/research/{date}-{slug}/linkedin/linkedin-post.md`

---

### Step 7: Optional Blog Article Generation (Conditional)

**ONLY execute this step if `--blog` flag is present in $ARGUMENTS**

If `--blog` flag is detected, generate a comprehensive blog article (800-1500 words) based on the research findings.

#### Check for Branding Flag

- If `--branding` flag is ALSO present: Apply personal branding framework
- If `--branding` flag is NOT present: Generate informative, objective blog article without personal voice

#### Blog Article Structure (WITHOUT --branding)

```markdown
# {Topic}: A Comprehensive Analysis

## Introduction
[Context and importance - 100-150 words]
- What is this topic?
- Why does it matter?
- What will this article cover?

## Background and Context
[Technical background - 150-200 words]
- Historical context or evolution
- Key concepts and definitions
- Current state of the field

## Core Concepts
[Main content organized in 3-5 sections - 400-600 words total]

### {Concept 1}
[Detailed explanation with concrete examples]
[Technical details and specifications]
[Citations and quotes from authoritative sources]

### {Concept 2}
[Detailed explanation with concrete examples]
[Data points and benchmarks]
[Real-world applications]

### {Concept 3}
[Detailed explanation with concrete examples]
[Code examples or technical illustrations]
[Performance characteristics]

## Practical Applications
[Real-world use cases - 150-200 words]
- Application 1 (with specific company/product example)
- Application 2 (with data on impact/scale)
- Application 3 (with technical implementation details)

## Challenges and Considerations
[Limitations and trade-offs - 100-150 words]
- Challenge 1 (with concrete example)
- Challenge 2 (with mitigation strategies)

## Conclusion
[Summary and key takeaways - 100-150 words]
- Main points recap
- Future outlook
- Actionable next steps

## Further Reading
[Curated sources - 5-10 high-quality references]
- [{Resource Name}]({URL}) - {Description}
- [{Course/Tutorial}]({URL}) - {Description}

---
**Word count:** 800-1500 words
**Reading time:** 4-7 minutes
**Technical level:** {as specified in arguments}
```

#### Blog Article Structure (WITH --branding)

When `--branding` flag is present, use enhanced structure with personal elements:

```markdown
# Why Every {Audience} Should Master {Topic}: A Practitioner's Guide

## My Journey with {Topic}
[Personal framing - 100 words]
"Colleagues have often asked me to explain {topic}..."
"This is part of my weekly series on {broader theme}..."
[Establish credibility and series context]

## What Is {Topic}? (The Fundamentals)
[Definition with concrete example - 200 words]
[Authority quote]: "As {Source} puts it, '{exact quote}'"
[Technical illustration or code example]
[Concrete example like 'king - man + woman = queen']

## Why This Matters for You
[Explicit practical value section - 200 words]
"Understanding {topic} is the difference between {copying code} and {architecting solutions}."

**Real-world impact:**
- {Specific use case with company example}
- {Concrete outcome with data}
- {Technical capability with specific detail}

## How {Topic} Works (Technical Breakdown)
[3-4 detailed sections - 400-500 words total]

### {Technical Aspect 1}
[Step-by-step explanation]
[Concrete examples with code/math]
[Common misconceptions addressed]

### {Technical Aspect 2}
[Detailed technical content]
[Specific algorithms, versions, benchmarks]
[Authority quotes and citations]

### {Technical Aspect 3}
[Advanced concepts]
[Real-world performance data]
[Implementation considerations]

## Getting Started: Your Learning Path
[Specific named resources - 150 words]
NOT generic: "there are courses" ❌
SPECIFIC: "Google's ML Crash Course offers..." ✅

**Free Resources:**
- "{Exact Course Name}" offers hands-on tutorials on {specific topics}
- "{Specific Documentation}" provides excellent guide to {specific aspect}
- "Try {Specific Tool/Platform}" for practice with {specific feature}

**Books and Papers:**
- [{Specific Book}]({link}) - {Why it's valuable}
- [{Specific Paper}]({arxiv link}) - {Key contribution}

## Key Takeaways
[5-7 specific, actionable points - 150 words]
- ✅ {Specific point with concrete example}
- ✅ {Technical detail with data}
- ✅ {Actionable recommendation with specific tool/approach}

## What's Next in This Series
["In next week's article, I'll explore {next topic}, covering {specific aspects}..."]
[Create anticipation and continuity]

## Additional Reading
[All research sources with descriptions]
- [{Resource 1}]({URL}) - {What you'll learn}
- [{Resource 2}]({URL}) - {Key insights}

---
**Word count:** 1000-1500 words
**Reading time:** 5-8 minutes
**Series:** {Series name if applicable}
```

#### Blog Article Quality Checklist

- ✅ 800-1500 word count
- ✅ Concrete examples throughout (not vague statements)
- ✅ At least 3-5 authoritative quotes
- ✅ Technical details (specific versions, numbers, algorithms)
- ✅ Code examples or mathematical illustrations where relevant
- ✅ Real-world applications with specific companies/products
- ✅ Practical value explicitly stated
- ✅ Proper markdown formatting with headers
- ✅ 5-10 high-quality sources cited
- ✅ If --branding: All 7 personal branding elements present
- ✅ If no --branding: Objective, educational tone
- ✅ Beginner-friendly if technical_level=beginner
- ✅ Advanced technical content if technical_level=expert

#### Save Blog Article

Create file: `{OBSIDIAN_VAULT_PATH}/research/{date}-{slug}/blog/blog-article.md`

---

### Step 8: Save to Obsidian Vault

Create organized folder structure:

```
{OBSIDIAN_VAULT_PATH}/research/{YYYY-MM-DD}-{topic-slug}/
├── research-topic.md          # Metadata and request details
├── output.md                  # Generated output in requested format
├── sources.md                 # All citations and references
├── conflicts.md               # Detected conflicts (if any)
├── metadata.json              # Research metadata and stats
├── {topic-slug}_research.pdf  # Comprehensive PDF with research output
├── linkedin/                  # OPTIONAL: Only if --linkedin flag present
│   └── linkedin-post.md       # Generated LinkedIn post (150-300 words)
└── blog/                      # OPTIONAL: Only if --blog flag present
    └── blog-article.md        # Generated blog article (800-1500 words)
```

**Note:** `linkedin/` and `blog/` folders are created ONLY if their respective flags are present.

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
- Download PDF for offline review or sharing
```

### Step 8: Generate Comprehensive PDF

Create a professionally formatted PDF containing the complete research output for easy sharing and offline review.

**Prerequisites Check:**
- Verify weasyprint is installed: `python3 -c "from weasyprint import HTML"`
- If not installed: `pip install weasyprint`

**PDF Generation Process:**

1. **Create HTML Template**
   - Generate comprehensive HTML file with research output
   - Include professional styling (fonts, colors, spacing, page breaks)
   - Add metadata and table of contents

2. **HTML Structure:**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{topic} - Research Report</title>
    <style>
        /* Professional styling with page breaks, typography, colors */
    </style>
</head>
<body>
    <!-- Cover page -->
    <!-- Research output in requested format -->
    <!-- Sources and references -->
    <!-- Research methodology -->
</body>
</html>
```

3. **Content to Include:**
   - **Cover Page:**
     - Research title
     - Generation date
     - Research metrics (depth, format, sources, word count)
     - Quick statistics

   - **Main Content:**
     - Complete output in requested format
     - All sections with proper formatting
     - Code examples and technical content
     - Citations and inline references

   - **Sources Section:**
     - All citations numbered and formatted
     - Source authority scores
     - Publication dates and URLs

   - **Methodology Section:**
     - 6 sources breakdown
     - Research parameters
     - Quality metrics
     - Conflict resolutions (if any)

4. **Convert HTML to PDF:**
```python
from weasyprint import HTML
HTML('/tmp/{topic_slug}_research.html').write_pdf('/tmp/{topic_slug}_research.pdf')
```

5. **Copy PDF to Multiple Locations:**
   - Project root: `/home/user/Obsidian_Agent/{topic_slug}_research.pdf`
   - Obsidian vault: `{OBSIDIAN_VAULT_PATH}/research/{date}-{slug}/{topic_slug}_research.pdf`

6. **Verify PDF Creation:**
   - Check file exists
   - Verify file size (should be 50-150KB typically, depending on content length)
   - Confirm readability

**Expected Output:**
- Professional 10-30 page PDF (depending on format and word count)
- File size: 50-150 KB
- Complete research output with citations
- Easy to share and print

### Step 9: Commit and Push to Git Repository

Automatically commit the PDF to the current git branch and push to remote.

**Git Operations:**

1. **Verify Git Status:**
```bash
git status
```
   - Confirm we're on the correct branch (should start with `claude/`)
   - Check for untracked files

2. **Add PDF to Git:**
```bash
git add {topic_slug}_research.pdf
```

3. **Create Descriptive Commit:**
```bash
git commit -m "$(cat <<'EOF'
Add research PDF for {topic}

Generated comprehensive research document in {format} format covering {topic}. Includes all sources, citations, and methodology.

Research metrics:
- Depth: {depth}
- Format: {format}
- Sources: {total_sources}
- Word count: {word_count}
- Quality: All validation checks passed
EOF
)"
```

4. **Push to Remote:**
```bash
git push -u origin {current-branch}
```
   - Use current branch name (e.g., `claude/...`)
   - Include `-u` flag to set upstream tracking
   - Retry up to 4 times with exponential backoff (2s, 4s, 8s, 16s) if network errors occur

5. **Verify Success:**
```bash
git status
```
   - Confirm working tree is clean
   - Verify branch is up-to-date with remote

**Error Handling:**
- **If not in git repository:** Skip git operations, warn user
- **If branch doesn't match pattern:** Verify with user before pushing
- **If push fails (403):** Check branch name starts with `claude/` and ends with session ID
- **If network error:** Retry with exponential backoff
- **If conflicts exist:** Halt and notify user to resolve manually

**Expected Output:**
- PDF committed to current branch
- Pushed to remote repository
- Working tree clean
- User can access PDF from repository

**Final Confirmation Message:**
```markdown
## ✅ PDF Generated and Pushed Successfully

**PDF Details:**
- **Filename:** {topic_slug}_research.pdf
- **Size:** {file_size} KB
- **Pages:** {page_count} pages

**Locations:**
1. **Project root:** `/home/user/Obsidian_Agent/{topic_slug}_research.pdf`
2. **Obsidian vault:** `{OBSIDIAN_VAULT_PATH}/research/{date}-{slug}/{topic_slug}_research.pdf`
3. **Git repository:** Committed and pushed to `{branch_name}`

**Git Status:**
- ✅ Committed with descriptive message
- ✅ Pushed to remote repository
- ✅ Working tree clean

You can now download the PDF from your repository or find it in the locations above! 🎉
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

**Research Quality:**
- ✅ All 6 research sources were queried
- ✅ Output matches requested format
- ✅ Word count within ±20% of target
- ✅ All citations are valid and accessible
- ✅ Conflicts detected and resolved (or flagged)
- ✅ Technical level matches request
- ✅ No hallucinations (all info source-backed)
- ✅ Quality standards applied:
  - ✅ Concrete examples (not vague statements)
  - ✅ Detailed explanations (not high-level only)
  - ✅ Technical details included (versions, numbers, algorithms)
  - ✅ All claims have citations

**File Management:**
- ✅ Files saved to Obsidian vault
- ✅ Proper markdown formatting
- ✅ PDF file created and readable
- ✅ PDF committed and pushed to git repository

**Optional Content (if flags present):**
- ✅ If --linkedin: LinkedIn post generated (150-300 words)
  - ✅ If --branding: Personal branding elements present
  - ✅ If no --branding: Objective, informative tone
  - ✅ Saved to linkedin/linkedin-post.md
- ✅ If --blog: Blog article generated (800-1500 words)
  - ✅ If --branding: Personal branding elements present
  - ✅ If no --branding: Objective, educational tone
  - ✅ Saved to blog/blog-article.md

---

## References

- **Full Documentation**: `.claude/commands/research-generic-documentation.md`
- **Specialized Version**: `.claude/commands/research-topic-documentation.md` (for LinkedIn/Blog)
- **Brave API Config**: `docs/brave-api-configuration.md`
- **Coding Standards**: `CLAUDE.md`
