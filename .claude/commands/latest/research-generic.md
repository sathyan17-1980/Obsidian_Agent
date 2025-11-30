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
   - Search educational channels (prioritize: 3Blue1Brown, Two Minute Papers, Lex Fridman, Andrew Ng, etc.)
   - Extract transcript content
   - Summarize key points
   - **Featured Source**: https://www.3blue1brown.com/ - Exceptional visual explanations of mathematical concepts

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

**CRITICAL: Research Quality Standards (21 Applicable Points)**

Apply these quality standards from the 55-point framework to ensure high-quality, research-backed content:

**Research Grounding (Core Requirements):**
1. ✅ Include SPECIFIC technical details from research (not generic claims)
   - Example: "1536-dimensional vectors" not "high-dimensional vectors"
   - Example: "achieved 95.97% macro accuracy" not "high accuracy"
2. ✅ Quote authoritative sources that TEACH something
   - Use quotes found in your research, not marketing copy
   - Example: "As Cloudflare's guide explains, '{exact teaching quote}'"
3. ✅ Reference CONCRETE examples from actual sources
   - Real algorithms (HNSW, FAISS), actual metrics, specific implementations
4. ✅ Show research depth through specifics, not vague statements
   - Cite 8-10+ different sources throughout the document
5. ✅ ONE memorable concrete example with actual numbers/data
   - Example: "king" - "man" + "woman" = "queen" (embedding space math)
   - Example: "15.36 billion numbers searched in <100ms"

**Citation and Source Quality:**
6. ✅ Authority quotes with exact attribution FROM YOUR RESEARCH
   - All quotes must come from sources you actually analyzed
7. ✅ References include actual URLs found in research
   - No generic "additional reading" - specific resources with links
8. ✅ Statistics from real sources, not fabricated
   - Every number must be traceable to a source
9. ✅ Every claim traceable to a source analyzed
   - No hallucinations or assumptions
10. ✅ All claims must have inline citations [1][2][3]

**Technical Depth and Examples:**
11. ✅ Concrete technical examples FROM ACTUAL SOURCES
    - Code snippets, algorithms, mathematical formulas from research
12. ✅ Specific technical details prove expertise
    - Show depth: dimension counts, latency numbers, accuracy metrics
13. ✅ Code examples use realistic data, not foo/bar
    - When including code: use real-world variable names and data
14. ✅ Simple memorable analogy (ONE, not mixing metaphors)
    - Make complex concepts accessible with single clear analogy

**Content Structure (Format-Dependent):**
15. ✅ Real-world applications
    - Show practical use cases and implementations
16. ✅ Misconceptions section (for guide/qa formats)
    - Address common misunderstandings found in research
17. ✅ Specific, named free resources FOUND IN RESEARCH
    - "Google's ML Crash Course" not "there are free courses"
    - Include exact course names, documentation titles, tool names
18. ✅ "Why this matters" section (for guide/qa formats)
    - Explicit practical value and outcomes

**Quality Validation:**
19. ✅ NOT high-level or vague - SPECIFIC findings from research
    - Bad: "Embeddings are important for AI"
    - Good: "Embeddings transform text into 1536-dimensional vectors that capture semantic meaning"
20. ✅ Shows research depth: cites 8-10+ different sources
    - Demonstrates comprehensive multi-source analysis
21. ✅ No hallucinations - only source-backed information
    - Every fact, quote, and example must come from analyzed sources

**Format-Specific Application:**
- **Summary/Report**: Apply all 21 points, focus on citations and technical depth
- **Q&A**: Apply all 21 points + misconceptions section + "why this matters"
- **Comparison**: Apply citation standards + specific metrics from sources
- **Guide**: Apply all 21 points + misconceptions + resources + "why this matters"

**Technical Level Adjustments:**
- **Beginner**: Use analogies (#14), explain technical details simply, more context
- **Moderate**: Balance technical depth with accessibility, some jargon explained
- **Advanced**: Full technical detail, assume background, dense citations
- **Expert**: Specialized terminology, research-paper density, extensive citations

### Step 6: Save to Obsidian Vault

Create organized folder structure:

```
{OBSIDIAN_VAULT_PATH}/research/{YYYY-MM-DD}-{topic-slug}/
├── research-topic.md          # Metadata and request details
├── output.md                  # Generated output in requested format
├── sources.md                 # All citations and references
├── conflicts.md               # Detected conflicts (if any)
├── metadata.json              # Research metadata and stats
└── {topic-slug}_research.pdf  # Comprehensive PDF with research output
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
- ✅ All 6 research sources were queried
- ✅ Output matches requested format
- ✅ Word count within ±20% of target
- ✅ All citations are valid and accessible
- ✅ Conflicts detected and resolved (or flagged)
- ✅ Files saved to Obsidian vault
- ✅ Proper markdown formatting
- ✅ Technical level matches request
- ✅ No hallucinations (all info source-backed)
- ✅ PDF file created and readable
- ✅ PDF committed and pushed to git repository

---

## References

- **Full Documentation**: `.claude/commands/research-generic-consolidator.md`
- **Specialized Version**: `.claude/commands/research-topic-merged.md` (for LinkedIn/Blog)
- **Brave API Config**: `docs/brave-api-configuration.md`
- **Coding Standards**: `CLAUDE.md`
