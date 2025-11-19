---
description: Multi-source research agent for LinkedIn & Blog content generation
argument-hint: "[topic] [--depth minimal|light|moderate|deep|extensive] [--drafts 1-5]"
---

# Research Topic - LinkedIn & Blog Content Generator

## Research Topic

$ARGUMENTS

---

## Your Task

Execute a comprehensive multi-source research workflow and generate platform-optimized content (LinkedIn posts and Blog articles) for the topic above.

### Step 1: Parse Arguments and Set Defaults

Parse the arguments from: **$ARGUMENTS**

Extract:
- **Topic**: The research question or topic (REQUIRED)
  - Example: "Why AI enthusiasts should learn embeddings"
  - Validation: Not empty, clear and specific

- **Depth**: Research depth level (default: "moderate")
  - `minimal`: Quick research (~60s, 1-3 queries/source, ~$0.14)
    - Use when: Testing, simple topics, time-sensitive
  - `light`: Basic research (~90s, 3-5 queries/source, ~$0.14)
    - Use when: Familiar topics, quick turnaround needed
  - `moderate`: Standard research (~120s, 5-8 queries/source, ~$0.18) - DEFAULT
    - Use when: Most research tasks, balanced quality/speed
  - `deep`: Comprehensive analysis (~180s, 8-12 queries/source, ~$0.20)
    - Use when: Complex topics, high-quality content needed
  - `extensive`: Multi-topic deep dive (~240s, 12+ queries/source, ~$0.22+)
    - Use when: Research papers, comprehensive guides

- **Drafts**: Number of draft variations per platform (default: 3)
  - Range: 1-5
  - Default: 3 (Technical, Story-Driven, Balanced)
  - More drafts = more variety, but higher cost

Example valid inputs:
```
/research-topic "Why AI enthusiasts should learn embeddings"
/research-topic "Transformer architecture basics" --depth light --drafts 1
/research-topic "Constitutional AI vs RLHF" --depth deep --drafts 5
```

### Step 2: Verify Prerequisites and Configuration

Check required configuration before starting research:

1. **Obsidian Vault Path (MANDATORY)**
   - Check if `OBSIDIAN_VAULT_PATH` environment variable is set
   - If not set:
     - Prompt user: "Please provide your Obsidian vault path:"
     - Validate path exists and is writable
     - Save to environment or .env file
   - **CRITICAL**: This integration is mandatory - research cannot proceed without it

2. **Voice Profile (REQUIRED for Quality)**
   - Check if voice profile exists at: `{OBSIDIAN_VAULT_PATH}/voice-profile/voice-profile-v1.json`
   - If not found:
     - Warn user: "No voice profile found. Content will be generic without voice matching."
     - Offer to create profile: "Provide 5+ writing samples (5,000+ words total) to create voice profile?"
     - If user provides samples: Run voice profile creation
     - If not: Proceed without voice matching (lower quality expected)

3. **API Keys**
   - Brave Search API: Check `BRAVE_API_KEY_FREE` and `BRAVE_API_KEY_PRO`
     - Already configured: ✅
     - FREE tier: 2,000 queries/month
     - PRO tier: Higher limits (use for deep/extensive research)
   - LLM API: Check `ANTHROPIC_API_KEY` or similar
   - Google Drive (optional): Check `GOOGLE_DRIVE_CREDENTIALS_PATH`

4. **Dependencies**
   - Verify required packages installed (newspaper3k, youtube-transcript-api, etc.)
   - If missing: Provide installation command

### Step 3: Execute Multi-Source Research (Parallel)

Research the topic across 6 sources in parallel. Execute ALL sources concurrently for maximum speed.

**Performance Target**: Complete all 6 sources in <90 seconds

#### Source 1: HackerNews Discussions

**Actions:**
- Search HackerNews API for topic-related discussions
- Query format: Extract key terms from topic and search
- Number of queries based on depth level (minimal: 1-3, moderate: 5-8, deep: 8-12)

**Extract from each thread:**
- Title and URL
- Top 5-10 comments (highest rated)
- Community sentiment (positive/negative/neutral)
- Key technical insights or debates
- Publication date

**Expected Results:**
- 5-15 relevant HN threads
- 30-50 top comments extracted
- Community perspectives on topic

**Error Handling:**
- If HN API unavailable: Log warning, continue with other sources
- If no results found: Note in research summary, not a failure

#### Source 2: Web Search (Brave API)

**Actions:**
- Use Brave Search API to find high-quality web articles
- Tier selection:
  - minimal/light depth: Use FREE tier (save quota)
  - moderate/deep/extensive: Use PRO tier (better quality)
- Number of queries: Match depth level
- Search strategy: Vary query phrasing for diversity

**Extract from each result:**
- Title, URL, snippet
- Domain authority (prefer .edu, .org, official docs)
- Publication date
- Author (if available)

**Expected Results:**
- 8-15 web articles
- Mix of technical docs, tutorials, explainers
- High domain authority sources

**Error Handling:**
- If API rate limit hit: Fall back to FREE tier or cache
- If no results: Broaden query terms

#### Source 3: Full Article Content Extraction

**Actions:**
- Take top 5-10 URLs from Web Search results
- Extract full article content using 3-tier fallback:
  1. **Tier 1**: newspaper3k (best for news/blogs)
  2. **Tier 2**: BeautifulSoup with custom selectors
  3. **Tier 3**: Raw HTML text extraction

**Extract from each article:**
- Full text content
- Code examples (if present)
- Images/diagrams (note URLs)
- Author and publication info
- Structured sections/headings

**Expected Results:**
- 5-10 full articles extracted
- Success rate target: >70%
- Rich content for drafting

**Error Handling:**
- If extraction fails: Try next tier parser
- If all tiers fail: Use snippet from web search instead
- Paywall encountered: Log and skip (don't waste time)

#### Source 4: Obsidian Vault Search (MANDATORY)

**Actions:**
- Semantic search using embeddings:
  - Encode topic into vector
  - Search vault for semantically similar notes
  - Rank by similarity score
- Tag filtering: Look for relevant tags
- Frontmatter filtering: Check status, category metadata
- Number of results: Based on depth (minimal: 3, moderate: 5-8, deep: 10-15)

**Extract from each note:**
- Full note content
- Title and frontmatter metadata
- Tags and links
- Creation/modification dates
- Related notes (via [[links]])

**Expected Results:**
- 3-15 related notes from personal vault
- Personal insights and past research
- Context from your existing knowledge base

**Error Handling:**
- If vault path invalid: FAIL EARLY - this is mandatory
- If no semantic search available: Fall back to keyword search
- If no results: Not an error, just note in summary

#### Source 5: Google Drive Search (Optional)

**Actions:**
- OAuth 2.0 authentication (use cached tokens if available)
- Search query across PDFs, DOCX, Google Docs
- File type filter: Focus on documents, not images/videos
- Number of results: Match depth level

**Extract from each document:**
- Full text content
- Document metadata (title, author, modified date)
- Sharing/permissions info (for citation)
- Relevant passages (highlight key sections)

**Expected Results:**
- 2-5 relevant documents
- Personal documents, shared research, notes
- Additional context from your Drive

**Error Handling:**
- If OAuth expired: Attempt token refresh, else skip this source
- If Drive API unavailable: Log warning, continue
- If no credentials: Skip this source (optional)

#### Source 6: YouTube Transcript Extraction

**Actions:**
- Search for educational videos on topic
- Curated channel list (prioritize quality tech education channels)
- Extract transcripts using youtube-transcript-api
- Number of videos: Based on depth (minimal: 0-1, moderate: 1-3, deep: 3-5)

**Extract from each video:**
- Full transcript text
- Video title, channel, URL
- Publication date
- Transcript timestamps (for citation)
- Summarize key points (3-5 bullets)

**Expected Results:**
- 1-5 video transcripts
- Educational content, tutorials, talks
- Different perspective (visual/verbal vs written)

**Error Handling:**
- If auto-generated captions only: Use them (note lower quality)
- If no transcripts available: Skip video
- If API error: Log and continue

**Parallel Execution Notes:**
- All 6 sources run concurrently (asyncio or threading)
- Don't wait for slow sources - use timeouts
- Collect results as they complete
- Log timing for each source (performance monitoring)

### Step 4: Aggregate Results and Detect Conflicts

After all research sources complete, aggregate and deduplicate:

**Expected at this point:**
- 28-50+ total sources collected
- Sources breakdown:
  - HackerNews: 5-15 threads
  - Web: 8-15 articles
  - Articles (full): 5-10 extractions
  - Obsidian: 3-15 notes
  - Google Drive: 0-5 documents
  - YouTube: 0-5 transcripts

#### 4.1 Deduplication

**Semantic Deduplication:**
- Encode all source snippets into vectors
- Calculate cosine similarity between all pairs
- If similarity >0.90: Mark as duplicate
- Keep source with highest authority, discard duplicate

**URL Deduplication:**
- Same URL from different sources: Merge into one
- Prefer full article extraction over snippet

**Expected after deduplication:**
- 20-40 unique sources remaining
- No redundant content

#### 4.2 Conflict Detection

**Types of conflicts to detect:**

1. **Factual Conflicts**
   - Example: "Transformers were introduced in 2017" vs "Transformers were introduced in 2018"
   - Detection: Look for contradictory statements about dates, numbers, definitions
   - Severity: HIGH

2. **Temporal Conflicts**
   - Example: Different publication dates for same event
   - Detection: Compare dates/versions across sources
   - Severity: MEDIUM

3. **Definitional Conflicts**
   - Example: Different definitions of same technical term
   - Detection: Extract definitions and compare
   - Severity: MEDIUM

4. **Opinion Conflicts**
   - Example: "RAG is better than fine-tuning" vs "Fine-tuning is better than RAG"
   - Detection: Sentiment analysis on comparative statements
   - Severity: LOW (expected for opinions)

**For each conflict detected:**
- Document the conflict in `conflicts.md`
- Note sources involved
- Attempt automatic resolution (see Step 4.3)

#### 4.3 Conflict Resolution

**Resolution Strategies:**

1. **Prefer Higher Authority Sources**
   - Authority ranking:
     - arxiv.org, *.edu: 0.95
     - openai.com, official docs: 0.90
     - github.com: 0.85
     - medium.com: 0.60
     - reddit.com, HN: 0.50
   - Personal Obsidian vault: 0.70 (you wrote it, but verify)

2. **Prefer More Recent Information**
   - For fast-moving topics (AI, tech), newer = better
   - Exception: Historical facts should use original sources

3. **Verify with Multiple Sources**
   - If 3+ sources agree: High confidence
   - If 2 sources disagree, 1 agrees with one: Medium confidence
   - If sources split evenly: Flag for manual review

4. **Flag Unresolvable Conflicts**
   - Save to `conflicts.md` for user review
   - Include confidence scores
   - Provide recommendation but note uncertainty

**Output:**
- Resolved conflicts: Note resolution in research summary
- Unresolved conflicts: List in `conflicts.md` with details
- Conflict count: Track total detected vs resolved

#### 4.4 Citation Management

**Create citation list:**
- Number all sources (1-N)
- Format:
  ```markdown
  [1] Title - Author (Date) - URL - Source Type - Authority: 0.XX
  ```
- Group by source type for easy reference
- Verify all URLs accessible (HTTP 200 check)
- Flag broken links but keep citation

**Expected output:**
- 20-40 numbered citations
- 100% URL verification rate
- Grouped and formatted for easy reference

### Step 5: Generate Platform-Optimized Content

Now generate content drafts using the aggregated research.

**CRITICAL: Personal Branding Framework**

All content MUST position the user as an AI expert building their personal brand. This is NOT generic educational content - it's YOU (the user) teaching others.

**Required Elements (MUST Include in Every Draft):**

1. **Personal Framing (Opening)** - Establish credibility and demand
   - Examples:
     - "My friends have often asked me to share my learnings on {topic}..."
     - "After working with {topic} for months, colleagues keep asking me..."
     - "The most common question I get about AI is..."
   - **Purpose:** Show that people seek YOU out for knowledge

2. **Educational Journey Context** - Position as guide
   - Examples:
     - "This is part of my weekly AI series where I take you progressively through..."
     - "Building on last week's post on {previous topic}, today we explore..."
     - "I'm starting from the basics and will guide you through..."
   - **Purpose:** You're leading a learning journey, not just explaining a topic

3. **Concrete Examples with Quotes** - Show depth of knowledge
   - **REQUIRED:** Include specific examples like:
     - Mathematical illustrations: "king" - "man" + "woman" = "queen"
     - Code snippets or technical details
     - Real-world analogies
   - **REQUIRED:** Quote authoritative sources:
     - "As Cloudflare puts it, '{exact quote}'"
     - "According to Google's ML documentation, '{exact quote}'"
     - "Research from {institution} shows that '{exact quote}'"
   - **Purpose:** Prove you understand deeply, not just superficially

4. **"Why This Matters for YOU" Section** - Practical value
   - **MUST include explicit section:** "Why this matters for you:"
   - Connect to reader's goals:
     - "This means you can build smarter applications with less complexity..."
     - "Understanding this is the difference between {novice} and {expert}..."
     - "This unlocks {specific capability}..."
   - **Purpose:** Show practical application, not just theory

5. **Actionable Resources** - Enable learning
   - **REQUIRED:** Include specific free resources:
     - "Google's ML Crash Course offers hands-on tutorials"
     - "Check out {Specific Course Name} for free exercises"
     - Links to documentation: "Embeddings Guide - Google ML"
   - **Purpose:** You're not just teaching, you're enabling

6. **Expert Positioning Language** - Elevate beyond basics
   - Use phrases like:
     - "Understanding {topic} is the difference between copying code and architecting solutions"
     - "This separates junior developers from senior engineers"
     - "Real AI practitioners know that..."
   - **Purpose:** Position as someone who architects, not just implements

7. **Series Continuity** - Build ongoing engagement
   - **End every post with:**
     - "Excited to delve deeper? In next week's post, I will explain {next topic}..."
     - "Next up: How {next topic} builds on what we learned today..."
     - "Stay tuned for my next post on {related topic}..."
   - **Purpose:** Create anticipation and recurring readership

**Generation Strategy:**

For each platform (LinkedIn, Blog), generate {num_drafts} variations (default: 3) with different strategies:

1. **Draft 1: Technical** (temperature 0.3)
   - Precise, fact-heavy, technical terminology
   - Code examples if relevant
   - For technical audience
   - **STILL include all 7 personal branding elements above**

2. **Draft 2: Story-Driven** (temperature 0.6)
   - Narrative approach, relatable examples
   - Personal voice, engaging
   - For general audience
   - **STILL include all 7 personal branding elements above**

3. **Draft 3: Balanced** (temperature 0.5)
   - Mix of technical and accessible
   - Professional tone
   - For mixed audience
   - **STILL include all 7 personal branding elements above**

**ANTI-PATTERNS (DO NOT DO):**
- ❌ Generic educational tone without personal framing
- ❌ High-level vague statements without concrete examples
- ❌ No authoritative quotes or specific sources
- ❌ Missing "why this matters" practical value
- ❌ No resources or next steps for readers
- ❌ Generic expert language without positioning
- ❌ Standalone posts with no series continuity

#### 5.1 LinkedIn Post Generation

**For each of {num_drafts} drafts:**

**Requirements:**
- Word count: 150-300 words
- Format: Short paragraphs (2-3 sentences each)
- Hook: Strong opening line
- Value: Clear takeaway
- CTA: End with question or action
- Hashtags: 3-5 relevant hashtags
- Formatting: Use line breaks, emojis optional

**Content structure (MUST FOLLOW):**
```markdown
{Personal Framing - 1-2 sentences establishing credibility}
Example: "My friends have often asked me to share my learnings on {topic}. So I'm creating this post as part of my weekly AI series..."

{Hook/Question - 1 sentence that connects to reader's curiosity}
Example: "You may wonder, why should every AI enthusiast understand {topic}? That's because..."

{Core Concept Explanation - 2-3 sentences with CONCRETE example}
Example: "So what is {topic}? {Definition with specific example}. As {Authority Source} puts it, '{exact quote}.'"

{Concrete Example - Mathematical or technical illustration}
Example: "Think of it this way: 'king' minus 'man' plus 'woman' equals 'queen' in embedding space..."

{Why This Matters Section - REQUIRED, 1-2 sentences}
Example: "Why this matters for you: {topic} simplifies {problem} while retaining {benefit}. This means you can {practical application}..."

{Expert Positioning - 1 sentence showing depth}
Example: "Understanding this is the difference between copying code and architecting solutions."

{Actionable Resources - 1-2 specific resources}
Example: "The best part? There are tons of free courses like {Specific Course Name}."

{Series Continuity - Tease next topic}
Example: "Excited to delve deeper? In next week's post, I will explain {related topic}..."

{Additional Reading - 2-3 specific links}
Example: "Additional documents to read on this:"
- {Resource Name 1} - {Source}
- {Resource Name 2} - {Source}

#{hashtag1} #{hashtag2} #{hashtag3}
```

**Reference Example Structure (from embeddings post):**
Use this exact flow:
1. Personal framing: "My friends have often asked me..."
2. Series positioning: "I am creating my first post on AI..."
3. Hook question: "Why embeddings? You may wonder..."
4. Definition with quote: "As Cloudflare puts it, '{quote}'"
5. Concrete example: "king" - "man" + "woman" = "queen"
6. Why this matters: "Why this matters for you: embeddings 'simplify...'"
7. Expert positioning: "difference between copying code and architecting solutions"
8. Resources: "tons of free courses on embedding models, like Google's ML Crash Course"
9. Series continuity: "In next week's post, I will explain what Vector databases are..."
10. Additional reading with specific links

**Paraphrasing requirements:**
- All research content MUST be paraphrased
- Semantic similarity to sources: >80% (preserve meaning)
- Lexical dissimilarity to sources: <70% (change words)
- No direct quotes without attribution
- Use validation: Run paraphrase checker before finalizing

**Voice matching:**
- If voice profile exists: Apply user's writing style
  - Match sentence structure patterns
  - Use similar vocabulary level
  - Mirror tone (casual/formal)
  - Target voice match score: >70%
- If no voice profile: Use strategy-appropriate voice

**Citations:**
- Include 2-3 key citations inline
- Format: "According to [Source Name]..."
- Link to full sources list in comments or description

**Expected output per draft:**
- 150-300 words
- Voice-matched (if profile available)
- Plagiarism-free (lexical dissimilarity <70%)
- Engaging and platform-optimized
- Strategy-aligned (technical/story/balanced)

#### 5.2 Blog Article Generation

**For each of {num_drafts} drafts:**

**Requirements:**
- Word count: 800-1500 words
- Format: Long-form article with sections
- SEO: Target keyword usage (natural, not stuffed)
- Structure: Clear hierarchy (H1, H2, H3)
- Depth: Comprehensive coverage of topic
- Citations: Inline references with numbers

**Content structure (MUST FOLLOW):**
```markdown
# {Title - SEO-optimized, keyword-rich, personal angle}
Example: "Why Every AI Enthusiast Should Master {Topic}: A Practitioner's Guide"

{Introduction - 150-200 words WITH personal branding}
**REQUIRED Opening Pattern:**
- Personal framing: "Many colleagues have asked me about {topic}..."
- Series context: "This is part of my weekly deep-dive series on AI fundamentals..."
- Hook question: "Why does {topic} matter? Because..."
- Preview with authority quote: "As {Source} explains, '{quote}'"
- Article roadmap: "In this guide, I'll walk you through..."

## What Is {Topic}? (Understanding the Fundamentals)
{300-400 words}
**MUST include:**
- Clear definition with concrete example
- Authority quotes: "According to {Source}, '{exact quote}'" [1][2]
- Technical illustration (diagram description, code snippet, or mathematical example)
- Real-world analogy that clarifies the concept
- Example: "Think of it like this: 'king' - 'man' + 'woman' = 'queen'..."

## Why This Matters for You (Practical Applications)
{300-400 words}
**MUST include:**
- Explicit "Why this matters for you:" section header or intro
- 3-5 concrete use cases:
  - "Building a chatbot that understands context"
  - "Analyzing sentiment in customer reviews"
  - "Creating recommendation engines"
- Expert positioning: "This is the difference between copying tutorials and architecting solutions"
- Complexity simplification: "This means you can {outcome} with less complexity..." [3][4]

## How {Topic} Works (Technical Deep Dive)
{300-400 words}
**MUST include:**
- Step-by-step breakdown with specific technical details
- Code examples or pseudocode (if applicable)
- Citations for technical claims: [5][6][7]
- Common misconceptions addressed
- Performance characteristics or benchmarks

## Getting Started: Resources and Next Steps
{200-300 words}
**MUST include:**
- Actionable learning path:
  - "Start with {Free Course Name} which offers hands-on tutorials"
  - "Google's {Specific Guide Name} provides excellent documentation"
  - "Practice with {Specific Tool/Platform}"
- Specific free resources (not generic):
  - Course links with descriptions
  - Documentation with exact URLs
  - Tools and frameworks to try
- Expert tip: "What separates beginners from practitioners is {insight}..."

## Key Takeaways
{100-150 words}
- Bullet list of main points with specifics:
  - "{Topic} simplifies {problem} while preserving {benefit}"
  - "Real-world applications include {specific examples}"
  - "Free resources available at {specific sources}"
  - "Understanding this enables you to {concrete capability}"
- NOT generic statements

## What's Next in This Series
{50-100 words}
**REQUIRED series continuity:**
- Tease next topic: "In next week's article, I'll explore {related topic}..."
- Show progression: "We'll build on today's foundation to understand {advanced concept}..."
- Create anticipation: "You'll learn how {next topic} connects to what we covered today..."

## Additional Reading
- [{Resource 1 Name}]({URL}) - {Brief description}
- [{Resource 2 Name}]({URL}) - {Brief description}
- [{Resource 3 Name}]({URL}) - {Brief description}

## References
[1] {Full citation with author, date, exact quote source}
[2] {Full citation}
...
```

**Blog Must-Haves Checklist:**
- ✅ Personal framing in introduction
- ✅ Series context ("part of my weekly series...")
- ✅ Authority quotes with exact attribution
- ✅ Concrete technical examples (code, math, diagrams)
- ✅ Explicit "Why this matters for you" section
- ✅ Specific, named free resources (not "there are courses")
- ✅ Expert positioning language
- ✅ Series continuity ("next week I'll cover...")
- ✅ Additional reading with specific links
- ✅ NOT high-level or vague
- ✅ Shows YOUR expertise, not just info aggregation

**Paraphrasing requirements:**
- Same as LinkedIn: >80% semantic, <70% lexical
- Longer form allows more creative paraphrasing
- Use examples to illustrate concepts (not just restate)
- Add original analysis and synthesis

**Voice matching:**
- Apply user's writing style throughout
- Match paragraph length preferences
- Use similar transition phrases
- Mirror complexity level
- Target voice match score: >70%

**SEO optimization:**
- Natural keyword usage (5-10 instances)
- Headers include keywords
- Meta description ready (first paragraph)
- Internal/external links where relevant
- Target SEO score: >0.80

**Expected output per draft:**
- 800-1500 words
- Well-structured with clear sections
- Voice-matched and plagiarism-free
- SEO-optimized
- Strategy-aligned

#### 5.3 Content Validation

**For EACH generated draft (LinkedIn + Blog), validate:**

1. **Plagiarism Check**
   - Run lexical similarity check against all sources
   - Threshold: <70% similarity to any single source
   - If fails: Regenerate with more aggressive paraphrasing
   - Tool: Use sentence-transformers for semantic similarity

2. **Voice Match Score (if profile exists)**
   - Compare draft to voice profile characteristics
   - Metrics: vocabulary, sentence length, formality, tone
   - Threshold: >70% match
   - If fails: Adjust tone and regenerate

3. **Word Count Validation**
   - LinkedIn: 150-300 words (strict)
   - Blog: 800-1500 words (flexible ±10%)
   - If out of range: Trim or expand

4. **Citation Verification**
   - All claims must have citations
   - All citations must be in sources list
   - No "dead" citation numbers
   - Format consistent

5. **Quality Checks**
   - Grammar and spelling (automated check)
   - Readability score (Flesch-Kincaid grade level)
   - Coherence (logical flow between sections)
   - Engagement prediction (if model available)

**If any validation fails:**
- Log the failure
- Attempt regeneration (max 2 retries)
- If still fails: Flag for manual review, but save draft

### Step 6: Save All Outputs to Obsidian Vault

Create organized folder structure in Obsidian vault for all research outputs.

**Folder structure:**
```
{OBSIDIAN_VAULT_PATH}/research/{YYYY-MM-DD}-{topic-slug}/
├── research-topic.md                    # Topic metadata and request details
├── research-summary.md                  # Aggregated research findings
├── linkedin/
│   ├── draft-1-technical.md
│   ├── draft-2-story.md
│   └── draft-3-balanced.md
├── blog/
│   ├── draft-1-technical.md
│   ├── draft-2-story.md
│   └── draft-3-balanced.md
├── sources.md                           # All citations (numbered)
├── conflicts.md                         # Detected conflicts and resolutions
├── metadata.json                        # Machine-readable metadata
├── user-selection.md                    # Placeholder for user's chosen drafts
└── {topic-slug}_research_all_drafts.pdf # Comprehensive PDF with all 6 drafts
```

**Create topic slug:**
- Convert topic to lowercase
- Replace spaces with hyphens
- Remove special characters
- Truncate to 50 chars max
- Example: "Why AI enthusiasts should learn embeddings" → "why-ai-enthusiasts-should-learn"

#### 6.1 research-topic.md

```markdown
---
date: {YYYY-MM-DD}
time: {HH:MM:SS}
topic: "{topic}"
depth: "{depth}"
num_drafts: {num_drafts}
status: completed
tags: [research, {topic-tags}]
---

# Research Topic: {topic}

**Generated:** {timestamp}
**Depth:** {depth}
**Drafts:** {num_drafts} per platform

## Request Parameters
- Research depth: {depth} ({queries_per_source} queries/source)
- Number of draft variations: {num_drafts}
- Voice matching: {enabled/disabled}
- Total sources collected: {total_sources}
- Execution time: {duration} seconds
- Estimated cost: ${cost}

## Research Summary
{Brief 2-3 sentence overview of what was found}

## Key Findings
- {Finding 1}
- {Finding 2}
- {Finding 3}
- {Finding 4}
- {Finding 5}

## Sources Breakdown
- HackerNews: {hn_count} threads
- Web articles: {web_count}
- Full articles: {article_count}
- Obsidian notes: {obs_count}
- Google Drive: {drive_count}
- YouTube transcripts: {yt_count}

## Quality Metrics
- Source authority (avg): {avg_authority}
- Conflicts detected: {conflict_count}
- Conflicts resolved: {resolved_count}
- Citation verification rate: {verification_rate}%
- Voice match score: {voice_match_score} (if applicable)

## Generated Outputs
- LinkedIn drafts: {num_drafts} (see `linkedin/` folder)
- Blog drafts: {num_drafts} (see `blog/` folder)
- Full research summary: `research-summary.md`
- All sources: `sources.md`
- Conflicts: `conflicts.md` (if any)

## Next Steps
1. Review all drafts in `linkedin/` and `blog/` folders
2. Select your preferred draft from each platform
3. Edit and personalize as needed
4. Publish to LinkedIn and blog
5. Track engagement and iterate
```

#### 6.2 research-summary.md

```markdown
# {Topic}: Research Summary

**Generated:** {timestamp}
**Total Sources:** {total_sources}

## Executive Summary
{3-5 paragraph comprehensive summary of all research findings}

## Key Concepts
### Concept 1: {Name}
{Explanation with citations [1][2]}

### Concept 2: {Name}
{Explanation with citations [3][4][5]}

### Concept 3: {Name}
{Explanation with citations [6][7]}

## Detailed Findings

### From HackerNews Discussions
{Summary of community insights, debates, sentiment}
- Top insight 1 [citation]
- Top insight 2 [citation]
- Controversial point [citation]

### From Web Research
{Summary of technical articles, tutorials, official docs}
- Key finding 1 [citation]
- Key finding 2 [citation]

### From Your Obsidian Vault
{What was found in personal notes}
- Related note 1: [[Note Title]]
- Related note 2: [[Note Title]]
- Personal insights

### From Google Drive (if any)
{Documents found and extracted}

### From YouTube (if any)
{Video transcripts and key points}

## Synthesis
{How all sources connect, what's the overall picture}

## Gaps and Uncertainties
{What's still unclear, conflicting, or needs more research}

## References
See `sources.md` for complete citation list.
```

#### 6.3 LinkedIn Draft Files

For each draft, create: `linkedin/draft-{N}-{strategy}.md`

```markdown
---
platform: linkedin
draft_number: {N}
strategy: {technical|story|balanced}
word_count: {count}
voice_match_score: {score}
plagiarism_check: passed
generated: {timestamp}
---

# LinkedIn Post - Draft {N} ({Strategy})

{Post content here - 150-300 words}

---

## Metadata
- Word count: {count}
- Strategy: {strategy}
- Temperature: {temp}
- Voice match: {score}
- Engagement prediction: {score}

## Key Citations
[1] {citation}
[2] {citation}
[3] {citation}

## Hashtags
#{tag1} #{tag2} #{tag3} #{tag4} #{tag5}

## Notes
{Any notes about this draft - tone, audience, when to use}
```

#### 6.4 Blog Draft Files

For each draft, create: `blog/draft-{N}-{strategy}.md`

```markdown
---
platform: blog
draft_number: {N}
strategy: {technical|story|balanced}
word_count: {count}
voice_match_score: {score}
seo_score: {score}
plagiarism_check: passed
generated: {timestamp}
---

{Full blog article content - 800-1500 words}

---

## Metadata
- Word count: {count}
- Strategy: {strategy}
- Temperature: {temp}
- Voice match: {score}
- SEO score: {score}
- Reading time: {minutes} min

## Notes
{Any notes about this draft - tone, audience, suggested edits}
```

#### 6.5 sources.md

```markdown
# Sources for: {Topic}

**Total Sources:** {total_sources}
**Verification Rate:** {rate}%

## HackerNews Discussions ({count})

[1] {Title} - HackerNews ({date})
    URL: {url}
    Authority: 0.50
    Key insight: {1-sentence summary}

[2] {Title} - HackerNews ({date})
    URL: {url}
    Authority: 0.50
    Key insight: {1-sentence summary}

## Web Articles ({count})

[N] {Title} - {Author} ({date})
    URL: {url}
    Domain: {domain}
    Authority: {score}
    Summary: {1-2 sentence summary}

## Full Article Extractions ({count})

[N] {Title} - {Author} ({date})
    URL: {url}
    Extracted: Full text ({word_count} words)
    Authority: {score}

## Obsidian Vault Notes ({count})

[N] [[{Note Title}]]
    Created: {date}
    Tags: {tags}
    Relevance: {score}

## Google Drive Documents ({count})

[N] {Doc Title} - {author} ({modified_date})
    File type: {PDF|DOCX|Google Doc}
    Sharing: {private|shared}

## YouTube Transcripts ({count})

[N] {Video Title} - {Channel} ({date})
    URL: {url}
    Duration: {duration}
    Transcript: {available|auto-generated}
```

#### 6.6 conflicts.md

```markdown
# Conflicts Detected: {Topic}

**Total Conflicts:** {conflict_count}
**Resolved:** {resolved_count}
**Unresolved:** {unresolved_count}

{If no conflicts:}
✅ No conflicts detected across all sources. All information was consistent.

{If conflicts exist:}

## Conflict 1: {Brief Description}

**Type:** {Factual|Temporal|Definitional|Opinion}
**Severity:** {HIGH|MEDIUM|LOW}

**Source A:** [{citation_num}] {source_name}
> "{Quote or summary of position A}"

**Source B:** [{citation_num}] {source_name}
> "{Quote or summary of position B}"

**Source C (if applicable):** [{citation_num}] {source_name}
> "{Quote or summary of position C}"

**Resolution:**
{How this was resolved or "UNRESOLVED - Manual review needed"}

**Confidence:** {0.XX}

**Action Taken:**
{What was done in the generated content - which source was used, how conflict was noted}

---

## Conflict 2: {Brief Description}
{Repeat structure}

---

## Unresolved Conflicts Requiring Manual Review

{List any conflicts that couldn't be auto-resolved}

### Conflict {N}: {Description}
**Sources:** [{num1}], [{num2}], [{num3}]
**Recommendation:** {What the agent recommends}
**User Action:** {What user should do}
```

#### 6.7 metadata.json

```json
{
  "topic": "{topic}",
  "generated_at": "{ISO 8601 timestamp}",
  "depth": "{depth}",
  "num_drafts": {num},

  "research": {
    "total_sources": {count},
    "sources_by_type": {
      "hackernews": {count},
      "web": {count},
      "articles": {count},
      "obsidian": {count},
      "google_drive": {count},
      "youtube": {count}
    },
    "execution_time_seconds": {duration},
    "cost_usd": {cost}
  },

  "quality": {
    "avg_source_authority": {score},
    "conflicts_detected": {count},
    "conflicts_resolved": {count},
    "citation_verification_rate": {rate},
    "voice_match_enabled": {true|false},
    "avg_voice_match_score": {score}
  },

  "outputs": {
    "linkedin_drafts": {num},
    "blog_drafts": {num},
    "all_passed_validation": {true|false}
  },

  "vault_path": "{relative_path_in_vault}"
}
```

#### 6.8 user-selection.md

```markdown
# Your Selected Drafts

Use this file to note which drafts you chose and any edits you made.

## LinkedIn Post

**Selected Draft:** {1|2|3} ({strategy})

**Edits Made:**
- {Edit 1}
- {Edit 2}

**Published:**
- Date: {date}
- URL: {url}
- Engagement: {likes/comments/shares}

---

## Blog Article

**Selected Draft:** {1|2|3} ({strategy})

**Edits Made:**
- {Edit 1}
- {Edit 2}

**Published:**
- Date: {date}
- URL: {url}
- Analytics: {pageviews, time on page, etc.}

---

## Feedback for Future Research

{What worked well, what to improve}
```

### Step 7: Validation

Before completing, verify all requirements met:

#### Functional Validation

- ✅ All 6 research sources were queried (or attempted)
- ✅ Results aggregated and deduplicated
- ✅ Conflicts detected and resolved (or flagged)
- ✅ {num_drafts} LinkedIn drafts generated per strategy
- ✅ {num_drafts} Blog drafts generated per strategy
- ✅ All drafts within word count ranges:
  - LinkedIn: 150-300 words
  - Blog: 800-1500 words (±10% acceptable)
- ✅ All drafts passed plagiarism check (<70% lexical similarity)
- ✅ Voice matching applied (if profile exists, score >70%)
- ✅ All citations verified and numbered
- ✅ All files saved to Obsidian vault

#### Quality Validation

- ✅ Total sources collected: 20-50 (target: 28+)
- ✅ Source authority average: >0.70
- ✅ Citation verification rate: 100% (all URLs checked)
- ✅ Drafts are publishable without major edits
- ✅ No hallucinations (all claims sourced)
- ✅ Proper markdown formatting
- ✅ SEO optimization (blogs): >0.80 score

#### Performance Validation

- ✅ Total execution time: <5 minutes (target: 2.5-3.5 min)
  - Research phase: <90 seconds
  - Aggregation: <30 seconds
  - Content generation: <60 seconds
  - Storage: <5 seconds
- ✅ Total cost: Within expected range for depth
  - minimal: ~$0.14
  - moderate: ~$0.18
  - deep: ~$0.20
  - extensive: ~$0.22+
- ✅ Cache hit rate: >50% (if repeated topic)

#### File System Validation

- ✅ Folder created: `{OBSIDIAN_VAULT_PATH}/research/{date}-{slug}/`
- ✅ Files exist:
  - `research-topic.md`
  - `research-summary.md`
  - `linkedin/draft-1-technical.md`
  - `linkedin/draft-2-story.md`
  - `linkedin/draft-3-balanced.md`
  - `blog/draft-1-technical.md`
  - `blog/draft-2-story.md`
  - `blog/draft-3-balanced.md`
  - `sources.md`
  - `conflicts.md` (if conflicts detected)
  - `metadata.json`
  - `user-selection.md` (template)
  - `{topic-slug}_research_all_drafts.pdf`
- ✅ All files have proper frontmatter
- ✅ All files are valid markdown
- ✅ PDF file created and readable (70-100KB)

### Step 8: Report Results

Provide comprehensive summary to user:

```markdown
## ✅ Research Topic Complete: {topic}

### Research Summary

**Topic:** {topic}
**Depth:** {depth} ({queries_per_source} queries/source)
**Execution Time:** {duration} seconds ({minutes}:{seconds})
**Total Cost:** ${cost}

### Sources Collected

**Total:** {total_sources} sources
- HackerNews: {hn_count} discussions
- Web articles: {web_count}
- Full article extractions: {article_count}
- Obsidian vault notes: {obs_count}
- Google Drive documents: {drive_count}
- YouTube transcripts: {yt_count}

**Quality Metrics:**
- Average source authority: {avg_authority}/1.0
- Citations verified: {verification_rate}%
- Conflicts detected: {conflict_count}
- Conflicts resolved: {resolved_count}

### Generated Content

**LinkedIn Posts:** {num_drafts} drafts
- Draft 1 (Technical): {word_count} words - Voice match: {score}
- Draft 2 (Story): {word_count} words - Voice match: {score}
- Draft 3 (Balanced): {word_count} words - Voice match: {score}

**Blog Articles:** {num_drafts} drafts
- Draft 1 (Technical): {word_count} words - SEO: {score} - Voice match: {score}
- Draft 2 (Story): {word_count} words - SEO: {score} - Voice match: {score}
- Draft 3 (Balanced): {word_count} words - SEO: {score} - Voice match: {score}

**All Validation Checks:** ✅ PASSED
- Plagiarism check: All drafts <70% lexical similarity
- Word count: All within range
- Voice matching: {avg_score}/1.0
- Citations: 100% verified

### Saved to Obsidian

**Location:** `{OBSIDIAN_VAULT_PATH}/research/{date}-{slug}/`

**Files created:**
- Research summary and metadata
- {num_drafts} LinkedIn drafts
- {num_drafts} Blog drafts
- {total_sources} sources documented
- {conflict_count} conflicts documented (if any)
- Comprehensive PDF with all 6 drafts

### Next Steps

1. **Review your drafts:**
   - Open Obsidian vault: `research/{date}-{slug}/`
   - Read `research-summary.md` for full research findings
   - Review all LinkedIn drafts in `linkedin/` folder
   - Review all blog drafts in `blog/` folder

2. **Select your favorites:**
   - Choose 1 LinkedIn draft and 1 blog draft
   - Edit and personalize as needed
   - Note your selection in `user-selection.md`

3. **Check conflicts (if any):**
   - Open `conflicts.md`
   - Review any unresolved conflicts
   - Make informed decisions on conflicting info

4. **Publish your content:**
   - LinkedIn: Copy selected draft to LinkedIn post
   - Blog: Copy selected draft to your blog platform
   - Track engagement and update `user-selection.md`

5. **Iterate and improve:**
   - Note what worked well
   - Provide feedback for future research
   - Build voice profile if not already done

### Performance

**ROI vs Manual Research:**
- Time saved: ~5.5 hours (6 hours manual → 3 minutes AI)
- Cost saved: ~$299.82 ($300 manual → $0.18 AI)
- Sources researched: {total_sources} vs typical 5-10 manual
- Improvement: **120x faster, 1,667x cheaper, 3-6x more sources**

### Quality Notes

{If voice matching enabled:}
✅ Voice matching applied - Avg score: {score}/1.0
Content should match your writing style.

{If no voice profile:}
⚠️ No voice profile found - Content uses generic voice.
Recommendation: Create voice profile with 5+ writing samples for better results.

{If conflicts exist:}
⚠️ {unresolved_count} unresolved conflicts detected.
Review `conflicts.md` for details and manual resolution.

{If high engagement prediction:}
✨ High engagement potential predicted for selected strategy.

{If any validation warnings:}
⚠️ Warnings: {list any warnings from validation}
```

### Step 9: Generate Comprehensive PDF

Create a professionally formatted PDF containing all 6 content drafts for easy sharing and offline review.

**Prerequisites Check:**
- Verify weasyprint is installed: `python3 -c "from weasyprint import HTML"`
- If not installed: `pip install weasyprint`

**PDF Generation Process:**

1. **Create HTML Template**
   - Generate comprehensive HTML file with all drafts
   - Include professional styling (fonts, colors, spacing, page breaks)
   - Add table of contents and metadata

2. **HTML Structure:**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{topic} - Research Drafts</title>
    <style>
        /* Professional styling with page breaks, typography, colors */
    </style>
</head>
<body>
    <!-- Cover page -->
    <!-- LinkedIn section (3 drafts) -->
    <!-- Blog section (3 drafts) -->
    <!-- Research methodology -->
</body>
</html>
```

3. **Content to Include:**
   - **Cover Page:**
     - Research title
     - Generation date
     - Research metrics (depth, sources, drafts)
     - Quick statistics

   - **LinkedIn Posts Section:**
     - All 3 drafts with full metadata
     - Strategy explanations
     - Engagement predictions
     - Hashtags and citations

   - **Blog Articles Section:**
     - All 3 drafts with complete content
     - SEO scores
     - Reading time estimates
     - Technical examples and code blocks

   - **About Section:**
     - Research methodology
     - Source breakdown
     - Quality metrics
     - Usage recommendations

4. **Convert HTML to PDF:**
```python
from weasyprint import HTML
HTML('/tmp/{topic_slug}_all_drafts.html').write_pdf('/tmp/{topic_slug}_research_all_drafts.pdf')
```

5. **Copy PDF to Multiple Locations:**
   - Project root: `/home/user/Obsidian_Agent/{topic_slug}_research_all_drafts.pdf`
   - Obsidian vault: `{OBSIDIAN_VAULT_PATH}/research/{date}-{slug}/{topic_slug}_research_all_drafts.pdf`

6. **Verify PDF Creation:**
   - Check file exists
   - Verify file size (should be 70-100KB typically)
   - Confirm readability

**Expected Output:**
- Professional 20-25 page PDF
- File size: 70-100 KB
- All 6 drafts with metadata
- Easy to share and print

### Step 10: Commit and Push to Git Repository

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
git add {topic_slug}_research_all_drafts.pdf
```

3. **Create Descriptive Commit:**
```bash
git commit -m "$(cat <<'EOF'
Add comprehensive PDF with {topic} research drafts

Generated downloadable PDF containing all 6 content drafts (3 LinkedIn posts + 3 blog articles) from the {topic} research. Includes professional formatting, metadata, and usage recommendations.

Research metrics:
- Depth: {depth}
- Sources: {total_sources}
- Word count: ~{total_words}
- SEO scores: {avg_seo}
- Quality: All validation checks passed
EOF
)"
```

4. **Push to Remote:**
```bash
git push -u origin {current-branch}
```
   - Use current branch name (e.g., `claude/add-research-consolidator-command-01WGSPJAiMcq5dSaWYxGXdap`)
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
- **Filename:** {topic_slug}_research_all_drafts.pdf
- **Size:** {file_size} KB
- **Pages:** 20-25 pages

**Locations:**
1. **Project root:** `/home/user/Obsidian_Agent/{topic_slug}_research_all_drafts.pdf`
2. **Obsidian vault:** `{OBSIDIAN_VAULT_PATH}/research/{date}-{slug}/{topic_slug}_research_all_drafts.pdf`
3. **Git repository:** Committed and pushed to `{branch_name}`

**Git Status:**
- ✅ Committed with descriptive message
- ✅ Pushed to remote repository
- ✅ Working tree clean

You can now download the PDF from your repository or find it in the locations above! 🎉
```

---

## Important Notes

### Research Quality

**Source Diversity is Key:**
- 6 parallel sources ensure comprehensive coverage
- Mix of community (HN), technical (articles), personal (Obsidian), and media (YouTube)
- 28+ sources vs typical 5-10 in manual research

**Conflict Resolution Matters:**
- Not all sources agree - that's normal
- Resolution strategy: Authority + Recency + Consensus
- Unresolved conflicts flagged for your review
- Don't ignore conflicts - address them in content

**Voice Matching Improves Quality:**
- Generic AI content is obvious and less engaging
- Your voice profile makes content sound like YOU
- 5+ writing samples (5,000+ words) recommended
- Voice match score >70% target

### Cost Management

**Research depth impacts cost:**
- minimal: ~$0.14 (testing, simple topics)
- moderate: ~$0.18 (most use cases) - DEFAULT
- deep: ~$0.20 (complex topics)
- extensive: ~$0.22+ (multi-topic research)

**Cost breakdown:**
- Research APIs: ~$0.04 (Brave Search PRO)
- LLM (6 drafts + paraphrasing): ~$0.14
- Other APIs: $0.00 (free tiers)

**ROI is exceptional:**
- 120x faster than manual
- 1,667x cheaper than manual ($300 → $0.18)
- Better quality (more sources, conflict detection)

### Performance Expectations

**Target timings:**
- Research (6 sources): <90s
- Aggregation & dedup: <30s
- Content generation: <60s
- Storage: <5s
- **Total: <3 minutes**

**What slows things down:**
- Article extraction failures (20-30% fail) → retries
- Slow API responses → use timeouts
- Large number of sources → more deduplication
- Voice matching → additional LLM call

**What speeds things up:**
- Cache hits (50%+ on repeated topics)
- Parallel execution (all 6 sources at once)
- Tier fallback (use FREE tier when possible)

### Content Quality

**Plagiarism Prevention:**
- All research content is paraphrased
- Validation: <70% lexical similarity to any source
- Semantic similarity maintained: >80% (meaning preserved)
- No direct quotes without attribution

**Platform Optimization:**
- LinkedIn: Short, punchy, engaging (150-300 words)
- Blog: Comprehensive, SEO-optimized (800-1500 words)
- Different strategies for different audiences

**3 Drafts Per Platform:**
- Technical (temp 0.3): Precise, fact-heavy
- Story-Driven (temp 0.6): Engaging, narrative
- Balanced (temp 0.5): Mix of both
- Choose what fits your audience

## Common Pitfalls to Avoid

### Research Phase

- ❌ **Running sources sequentially instead of parallel**
  - WHY BAD: 6x slower (6 × 15s = 90s vs 15s parallel)
  - ✅ CORRECT: Use asyncio/threading to run all 6 at once

- ❌ **Not validating Obsidian path early**
  - WHY BAD: Wasted research if path is invalid (mandatory requirement)
  - ✅ CORRECT: Check path in Step 2 before research starts

- ❌ **Trusting article extraction 100%**
  - WHY BAD: 20-30% of extractions fail (paywalls, JS-heavy sites)
  - ✅ CORRECT: Use 3-tier fallback, accept some failures

- ❌ **Not caching aggressively**
  - WHY BAD: Repeated API calls waste money and quota
  - ✅ CORRECT: Cache all research results, 50%+ hit rate target

- ❌ **Ignoring duplicate sources**
  - WHY BAD: Same URL counted twice, inflated source count
  - ✅ CORRECT: Deduplicate by URL and semantic similarity

### Content Generation

- ❌ **Generating drafts without voice profile**
  - WHY BAD: Generic AI content is obvious and less engaging
  - ✅ CORRECT: Create voice profile from writing samples first

- ❌ **No research grounding in prompts**
  - WHY BAD: LLM hallucinates, makes up facts
  - ✅ CORRECT: Include research summary in generation prompt

- ❌ **Not validating paraphrase quality**
  - WHY BAD: Risk of plagiarism if content too similar to sources
  - ✅ CORRECT: Check <70% lexical similarity, >80% semantic

- ❌ **Skipping conflict detection**
  - WHY BAD: Content includes contradictory info, looks sloppy
  - ✅ CORRECT: Detect conflicts, resolve or flag them

- ❌ **Using same temperature for all drafts**
  - WHY BAD: All drafts sound the same, no variety
  - ✅ CORRECT: Technical=0.3, Story=0.6, Balanced=0.5

### Storage Phase

- ❌ **Not organizing files properly**
  - WHY BAD: Hard to find research later, messy vault
  - ✅ CORRECT: Use date-slug folder structure, consistent naming

- ❌ **Missing metadata or citations**
  - WHY BAD: Can't verify claims later, unprofessional
  - ✅ CORRECT: Save sources.md with all citations numbered

- ❌ **Overwriting existing research**
  - WHY BAD: Lose previous work
  - ✅ CORRECT: Use date-slug to create unique folders

## References

- **Full Documentation**: `.claude/commands/research-topic-merged.md`
- **Generic Research Command**: `.claude/commands/research-generic.md` (for non-content research)
- **Brave API Config**: `docs/brave-api-configuration.md`
- **Coding Standards**: `CLAUDE.md`
- **Voice Profile Setup**: `scripts/create_voice_profile.py`
- **Google OAuth Setup**: `scripts/setup_google_drive_oauth.py`
