# Research-Topic Command - Comprehensive Guide

**Command:** `/research-topic`
**Version:** 2.0 (with 55-point Quality Framework)
**Status:** Production Ready
**Last Updated:** 2025-11-19

---

## Overview

The **research-topic** command is a specialized multi-source research agent designed specifically for **LinkedIn posts and Blog articles**. Unlike research-generic (which produces objective research), research-topic creates **personal brand content** that positions you as a knowledgeable AI expert building your thought leadership.

### Key Capabilities

- **Multi-Source Research**: Simultaneously queries 6 different sources
- **Dual Platform Output**: LinkedIn posts + Blog articles
- **Multiple Drafts**: 3 variations per platform (6 total drafts)
- **Personal Branding**: 55-point quality framework with voice matching
- **Voice Matching**: Matches your unique writing style
- **Series Continuity**: Links posts in ongoing educational series
- **Automatic PDF Generation**: Professional PDF with all 6 drafts
- **Git Integration**: Automatic commit and push to repository
- **Obsidian Integration**: Organized vault storage

---

## Quick Start

### Basic Usage

```bash
/research-topic "Why AI enthusiasts should learn embeddings"
```

### With Options

```bash
/research-topic "Transformer architecture basics" --depth light --drafts 1
```

### All Parameters

```bash
/research-topic "topic" --depth [minimal|light|moderate|deep|extensive] --drafts [1-5]
```

---

## Command Parameters

### 1. Topic (REQUIRED)

The subject for your LinkedIn/Blog content.

**Best Practices:**
- ✅ Educational angle: "Why AI enthusiasts should learn embeddings"
- ✅ Clear focus: "Understanding transformer attention mechanisms"
- ✅ Audience-centric: "How RAG improves chatbot accuracy"
- ❌ Too broad: "AI"
- ❌ Too technical without context: "HNSW algorithm implementation"

**Think:** What would make a compelling LinkedIn post or blog article?

### 2. Depth (Optional, default: "moderate")

Controls research thoroughness and quality.

| Depth | Duration | Queries/Source | Cost | Use When |
|-------|----------|----------------|------|----------|
| `minimal` | ~60s | 1-3 | ~$0.14 | Testing, simple familiar topics |
| `light` | ~90s | 3-5 | ~$0.14 | Quick turnaround, known topics |
| `moderate` | ~120s | 5-8 | ~$0.18 | Standard posts (DEFAULT) |
| `deep` | ~180s | 8-12 | ~$0.20 | Complex topics, high-quality content |
| `extensive` | ~240s | 12+ | ~$0.22+ | Comprehensive guides, cornerstone content |

**Recommendation:** Use `moderate` for weekly posts, `deep` for flagship content.

### 3. Drafts (Optional, default: 3)

Number of draft variations per platform.

| Drafts | Output | Use When |
|--------|--------|----------|
| 1 | 1 LinkedIn + 1 Blog | You want single best version |
| 3 | 3 LinkedIn + 3 Blog | Standard (gives variety) |
| 5 | 5 LinkedIn + 5 Blog | Need many options to choose from |

**Default:** 3 drafts per platform (6 total)
- Draft 1: Technical (temperature 0.3) - Precise, fact-heavy
- Draft 2: Story-Driven (temperature 0.6) - Engaging, narrative
- Draft 3: Balanced (temperature 0.5) - Mix of both

---

## Research Sources (6 Parallel)

### 1. HackerNews Discussions
- **What:** Tech community discussions
- **Value:** Practitioner insights, real-world debates
- **Content Use:** Quotes, community perspectives, trending topics

### 2. Web Search (Brave API)
- **What:** High-quality articles and official docs
- **Value:** Authoritative information, current trends
- **Content Use:** Statistics, expert quotes, technical details

### 3. Full Article Content Extraction
- **What:** Complete article text from top sources
- **Value:** Deep technical content, code examples
- **Content Use:** Detailed explanations, concrete examples

### 4. Obsidian Vault (MANDATORY)
- **What:** Your personal notes and past research
- **Value:** Your unique perspective, existing knowledge
- **Content Use:** Personal insights, continuity with past posts

### 5. Google Drive (Optional)
- **What:** Your documents and team resources
- **Value:** Private research, specialized knowledge
- **Content Use:** Internal examples, proprietary insights

### 6. YouTube Transcripts
- **What:** Educational video content
- **Value:** Different perspective, visual concepts explained
- **Content Use:** Expert quotes, alternative explanations

**Performance:** All 6 sources complete in <90 seconds

---

## 55-Point Quality Framework

### Personal Branding Elements (7 core requirements)

Every draft MUST include:

1. **Personal Framing (Opening)**
   - "My friends have often asked me to share my learnings on {topic}..."
   - "After working with {topic}, colleagues keep asking me..."
   - **Purpose:** Show people seek YOU for knowledge

2. **Educational Series Context**
   - "This is part of my weekly AI series..."
   - "Building on last week's post on {previous topic}..."
   - **Purpose:** Position as guide leading a learning journey

3. **Concrete Examples with Quotes**
   - Mathematical: "king" - "man" + "woman" = "queen"
   - Authority quotes: "As Cloudflare puts it, '{exact quote}'"
   - **Purpose:** Prove deep understanding, not surface knowledge

4. **"Why This Matters for YOU" Section**
   - Explicit section addressing reader benefits
   - "This means you can build smarter applications..."
   - **Purpose:** Show practical value, not just theory

5. **Actionable Resources**
   - "Google's ML Crash Course offers hands-on tutorials"
   - Specific free courses with exact names
   - **Purpose:** Enable reader learning, position as enabler

6. **Expert Positioning Language**
   - "Understanding this is the difference between copying code and architecting solutions"
   - "Real AI practitioners know that..."
   - **Purpose:** Elevate beyond basics, show expertise

7. **Series Continuity**
   - "Excited to delve deeper? In next week's post, I will explain {next topic}..."
   - **Purpose:** Build ongoing engagement, recurring readership

### LinkedIn-Specific Quality (20 points)

**Content Requirements:**
- ✅ Callback to previous week's topic
- ✅ Specific numbers (1536 dimensions, 15.36 billion)
- ✅ ONE memorable concrete example
- ✅ Teaching quote from authoritative source
- ✅ Personal experience signal
- ✅ Dual question hook opening
- ✅ "In a nutshell" crystallization
- ✅ "And the best part?" excitement turn
- ✅ Second person ("you build" not "developers build")
- ✅ Beginner positioning ("even if you're just starting")

**Voice & Style:**
- ✅ "That is because" (not "This is because")
- ✅ "Every" rhetorical rhythm
- ✅ Foundation callbacks
- ✅ Impossibility→solution reveal
- ✅ Identity transformation framing

**Structure:**
- ✅ Target 280-330 words (concise, not 380+)
- ✅ ONE clear resource with context
- ✅ Series continuity teaser
- ✅ 2 specific additional reading links
- ✅ NO code snippets (save for blog)
- ✅ NO bullet points (paragraph flow)

### Blog-Specific Quality (25 points)

**Research Integration:**
- ✅ Deep research findings (8-10+ sources)
- ✅ Actual statistics from sources
- ✅ Authority quotes that teach
- ✅ Concrete examples from research
- ✅ Real algorithms/metrics referenced

**Voice & Structure:**
- ✅ Conversational personal voice
- ✅ Target 1,200-1,400 words (not 1,800+)
- ✅ Personal experience throughout
- ✅ Dual question hooks
- ✅ "Think of it this way:" analogies

**Content Depth:**
- ✅ Specific technical details
- ✅ Code examples with realistic data
- ✅ Misconceptions section
- ✅ References with actual URLs
- ✅ Real-world applications in second person

**Quality Standards:**
- ✅ All claims research-backed
- ✅ No fabricated statistics
- ✅ Simple memorable analogies (not mixed)
- ✅ Shows research depth
- ✅ Conversational not corporate

### Research Quality (21 points)

Same as research-generic:
- Specific technical details from research
- Authority quotes with exact attribution
- Concrete examples from actual sources
- 8-10+ sources cited
- No hallucinations
- [See research-generic-help.md for full details]

---

## Output: LinkedIn Posts

### Format & Structure

**Word Count:** 150-300 words (target: 280-330)

**Required Structure:**
```markdown
{Personal Framing - establish credibility}
"My friends have asked me to share my learnings on {topic}..."

{Hook Question - dual question}
"You may wonder, why {topic}, or how {question}?"

{Core Concept - with concrete example}
"So what is {topic}? {Definition}. As {Authority} puts it, '{quote}.'"

{Concrete Example - mathematical/technical}
"Think of it this way: 'king' - 'man' + 'woman' = 'queen'..."

{Why This Matters - REQUIRED section}
"Why this matters for you: {benefit}. This means you can {outcome}..."

{Expert Positioning}
"Understanding this is the difference between copying code and architecting solutions."

{Actionable Resources}
"The best part? Google's ML Crash Course offers hands-on tutorials."

{Series Continuity}
"Excited to delve deeper? In next week's post, I will explain {next topic}..."

{Additional Reading}
- {Specific Resource 1} - {Source}
- {Specific Resource 2} - {Source}

#{hashtag1} #{hashtag2} #{hashtag3}
```

### 3 Draft Variations

**Draft 1: Technical**
- Temperature: 0.3
- Style: Precise, fact-heavy, technical terminology
- Audience: Technical professionals
- Examples: Code-focused, mathematical

**Draft 2: Story-Driven**
- Temperature: 0.6
- Style: Narrative, relatable, engaging
- Audience: General/beginner audience
- Examples: Analogies, real-world stories

**Draft 3: Balanced**
- Temperature: 0.5
- Style: Mix of technical and accessible
- Audience: Mixed technical levels
- Examples: Both technical and analogies

**All drafts include:** All 7 personal branding elements + LinkedIn quality standards

---

## Output: Blog Articles

### Format & Structure

**Word Count:** 800-1500 words (target: 1,200-1,400)

**Required Structure:**
```markdown
# {Title - SEO-optimized with personal angle}

{Introduction - 150-200 words WITH personal branding}
- Personal framing
- Series context
- Hook question
- Authority quote preview
- Article roadmap

## What Is {Topic}? (Understanding the Fundamentals)
{300-400 words}
- Clear definition with concrete example
- Authority quotes: "According to {Source}, '{quote}'" [1][2]
- Technical illustration
- Real-world analogy

## Why This Matters for You (Practical Applications)
{300-400 words}
- Explicit "Why this matters for you:" section
- 3-5 concrete use cases
- Expert positioning
- Complexity simplification

## How {Topic} Works (Technical Deep Dive)
{300-400 words}
- Step-by-step breakdown
- Code examples or pseudocode
- Citations [5][6][7]
- Common misconceptions
- Performance characteristics

## Getting Started: Resources and Next Steps
{200-300 words}
- Actionable learning path
- Specific free resources with links
- Tools and frameworks to try
- Expert tip

## Key Takeaways
{100-150 words}
- Bullet list with specifics
- NOT generic statements

## What's Next in This Series
{50-100 words}
- Tease next topic
- Show progression
- Create anticipation

## Additional Reading
- [{Resource 1}]({URL}) - {Description}
- [{Resource 2}]({URL}) - {Description}

## References
[1] {Full citation}
[2] {Full citation}
...
```

### 3 Draft Variations

Same as LinkedIn (Technical, Story-Driven, Balanced) but:
- Longer form (800-1500 words)
- More technical depth
- Code examples included
- Comprehensive citations

---

## Personal Branding Philosophy

### Core Purpose

Position YOU as:
- **Knowledgeable** - Deep understanding, not surface
- **Credible** - Backed by sources and examples
- **Approachable** - A guide others can reach out to
- **Expert** - Someone who architects, not just copies

### Anti-Patterns (DO NOT DO)

❌ **Generic Educational Tone**
- Bad: "Here's what you need to know about embeddings"
- Good: "My friends have often asked me to share my learnings on embeddings..."

❌ **Vague High-Level Statements**
- Bad: "Embeddings are important for AI"
- Good: "'king' - 'man' + 'woman' = 'queen' in embedding space illustrates semantic relationships"

❌ **No Authority Quotes**
- Bad: "Embeddings help computers understand text"
- Good: "As Cloudflare puts it, 'embeddings make it possible for computers to understand relationships between words'"

❌ **Missing Practical Value**
- Bad: "This is a useful technique"
- Good: "Why this matters for you: This means you can build smarter applications with less complexity"

❌ **Generic Resources**
- Bad: "There are free courses available"
- Good: "Google's ML Crash Course offers hands-on tutorials in vector mathematics"

❌ **Standalone Content**
- Bad: [No mention of series or next topic]
- Good: "In next week's post, I will explain how Vector Databases build on embeddings..."

### Quality Examples

**Concrete vs. Vague:**
- ❌ "Embeddings are important for AI"
- ✅ "'king' - 'man' + 'woman' = 'queen' in embedding space illustrates semantic meaning"

**Generic vs. Personal:**
- ❌ "This guide explains embeddings"
- ✅ "My friends have often asked me to share my learnings on embeddings, so I'm creating this weekly series"

**High-level vs. Detailed:**
- ❌ "Vector databases store embeddings efficiently"
- ✅ "As Cloudflare puts it, 'embeddings make it possible for computers to understand relationships' - they transform data into 1536-dimensional mathematical representations"

---

## Voice Matching

### What Is Voice Matching?

Analyzes your writing style and makes content sound like YOU wrote it.

### How It Works

1. **Analyze Writing Samples**
   - Need 5+ samples (5,000+ words total)
   - Extracts patterns:
     - Sentence structure
     - Vocabulary level
     - Tone (casual/formal)
     - Common phrases

2. **Apply to Generated Content**
   - Match sentence length patterns
   - Use similar vocabulary
   - Mirror formality level
   - Target: >70% voice match score

### Setup Voice Profile

```bash
# Store writing samples in Obsidian
{OBSIDIAN_VAULT_PATH}/voice-profile/voice-profile-v1.json
```

**Without Voice Profile:**
- Content uses generic AI voice
- Still follows 55-point framework
- Lower quality/engagement expected

**With Voice Profile:**
- Content sounds like YOU
- Higher engagement
- More authentic personal brand

---

## Output Files & Structure

```
{OBSIDIAN_VAULT_PATH}/research/{YYYY-MM-DD}-{topic-slug}/
├── research-topic.md                           # Metadata
├── research-summary.md                         # Aggregated research
├── linkedin/
│   ├── draft-1-technical.md                   # LinkedIn Technical
│   ├── draft-2-story.md                       # LinkedIn Story
│   └── draft-3-balanced.md                    # LinkedIn Balanced
├── blog/
│   ├── draft-1-technical.md                   # Blog Technical
│   ├── draft-2-story.md                       # Blog Story
│   └── draft-3-balanced.md                    # Blog Balanced
├── sources.md                                  # All citations
├── conflicts.md                                # Detected conflicts
├── metadata.json                               # Machine-readable stats
├── user-selection.md                           # Track your choices
└── {topic-slug}_research_all_drafts.pdf       # PDF with all 6 drafts
```

### Also Creates:
- PDF in project root: `/home/user/Obsidian_Agent/{topic-slug}_research_all_drafts.pdf`
- Git commit with descriptive message
- Push to remote repository

---

## Workflow: From Research to Publication

### Step 1: Run Research (3 minutes)
```bash
/research-topic "Why AI enthusiasts should learn embeddings" --depth moderate --drafts 3
```

### Step 2: Review Outputs (10-15 minutes)
- Open Obsidian vault: `research/{date}-{slug}/`
- Read `research-summary.md` for full research findings
- Review 3 LinkedIn drafts in `linkedin/` folder
- Review 3 blog drafts in `blog/` folder
- Check `conflicts.md` if conflicts detected

### Step 3: Select & Edit (10-20 minutes)
- Choose 1 LinkedIn draft (often balanced works well)
- Choose 1 blog draft (often technical for depth)
- Make minor edits for personalization
- Note selections in `user-selection.md`

### Step 4: Publish
- **LinkedIn:** Copy selected draft → LinkedIn post editor → Publish
- **Blog:** Copy selected draft → Blog platform → Publish

### Step 5: Track & Improve
- Update `user-selection.md` with:
  - Publication dates and URLs
  - Engagement metrics
  - What worked well
  - Feedback for future research

**Total Time:** ~30-40 minutes (vs 6+ hours manual)

---

## Cost & Performance

### Cost by Depth

| Depth | Total Cost | Sources | Drafts | Total Output |
|-------|-----------|---------|--------|--------------|
| minimal | ~$0.14 | 20-30 | 6 | ~6K words |
| light | ~$0.14 | 25-35 | 6 | ~6K words |
| moderate | ~$0.18 | 28-45 | 6 | ~6K words |
| deep | ~$0.20 | 35-50 | 6 | ~6K words |
| extensive | ~$0.22+ | 40-60+ | 6 | ~6K words |

**Cost Breakdown:**
- Research APIs: ~$0.04 (Brave Search PRO)
- LLM (6 drafts + paraphrasing): ~$0.14
- Voice matching: Included
- PDF generation: Free

### Performance Targets

| Phase | Target Time |
|-------|-------------|
| Research (6 sources) | <90s |
| Aggregation & Conflict Detection | <30s |
| Content Generation (6 drafts) | <60s |
| Voice Matching | <20s |
| Storage & PDF | <10s |
| **Total** | **<3.5 minutes** |

### ROI vs Manual Content Creation

- **120x faster** (6 hours → 3 minutes research)
- **1,667x cheaper** ($300 → $0.18)
- **6 drafts vs 1** manual draft
- **Better quality:** 28+ sources vs 5-10 manual

---

## Prerequisites

### Required

1. **Obsidian Vault Path**
   - Set `OBSIDIAN_VAULT_PATH` environment variable
   - **CRITICAL:** Cannot proceed without this

2. **API Keys**
   - `BRAVE_API_KEY_FREE` and/or `BRAVE_API_KEY_PRO`
   - `ANTHROPIC_API_KEY` (or equivalent LLM)

### Strongly Recommended

3. **Voice Profile**
   - Create from 5+ writing samples (5,000+ words)
   - Dramatically improves output quality
   - Without it: generic AI voice

### Optional

4. **Google Drive**
   - `GOOGLE_DRIVE_CREDENTIALS_PATH` for OAuth
   - Adds Drive documents to research

5. **Dependencies**
   - newspaper3k, youtube-transcript-api, weasyprint

---

## Usage Examples

### Example 1: Weekly LinkedIn Post
```bash
/research-topic "Why AI enthusiasts should learn embeddings" --depth moderate
```
- **Duration:** ~120s
- **Cost:** ~$0.18
- **Output:** 6 drafts (3 LinkedIn + 3 Blog)
- **Use Case:** Regular weekly content

### Example 2: Quick Social Post
```bash
/research-topic "What is RAG in AI?" --depth light --drafts 1
```
- **Duration:** ~90s
- **Cost:** ~$0.14
- **Output:** 2 drafts (1 LinkedIn + 1 Blog)
- **Use Case:** Quick social media content

### Example 3: Flagship Content
```bash
/research-topic "Complete guide to vector databases" --depth deep --drafts 5
```
- **Duration:** ~180s
- **Cost:** ~$0.20
- **Output:** 10 drafts (5 LinkedIn + 5 Blog)
- **Use Case:** Cornerstone content, high engagement

### Example 4: Series Continuation
```bash
/research-topic "How vector databases build on embeddings" --depth moderate
```
- **Duration:** ~120s
- **Cost:** ~$0.18
- **Output:** 6 drafts referencing previous posts
- **Use Case:** Multi-part educational series

---

## Best Practices

### Topic Selection

**Good Topics:**
- ✅ "Why every AI enthusiast should master embeddings"
- ✅ "How RAG improves chatbot accuracy"
- ✅ "Understanding transformer attention mechanisms"
- ✅ "Vector databases explained for beginners"

**Avoid:**
- ❌ Too broad: "AI and ML"
- ❌ Too narrow: "HNSW parameter tuning in Faiss"
- ❌ Not educational: "My AI project update"

### Depth Selection

**For Weekly Posts:** Use `moderate`
- Balanced quality and speed
- Good source coverage
- Professional output

**For Testing:** Use `light` or `minimal`
- Quick iteration
- Lower cost
- Good for familiar topics

**For Flagship Content:** Use `deep`
- Comprehensive research
- High-quality sources
- Worth the extra cost

### Draft Selection Guide

**LinkedIn:**
- **Technical audience:** Choose Technical draft
- **General audience:** Choose Story draft
- **Mixed audience:** Choose Balanced draft (most common)

**Blog:**
- **Technical readers:** Choose Technical draft
- **Beginners:** Choose Story draft
- **SEO focus:** Choose Balanced draft

### Personalization Tips

Even with great drafts, add personal touches:
- ✅ Update examples with your experience
- ✅ Add recent developments since research
- ✅ Include your specific call-to-action
- ✅ Adjust tone slightly for your audience
- ✅ Add images/diagrams if available

---

## Common Pitfalls

### 1. Not Reading research-summary.md
❌ Publishing draft without reviewing research
✅ Read summary to understand full context

### 2. Ignoring conflicts.md
❌ Conflicting info in content
✅ Always check for unresolved conflicts

### 3. Publishing Without Edits
❌ Copy-paste draft directly
✅ Add personal touches, verify examples

### 4. Wrong Depth for Topic
❌ Using `minimal` for complex unfamiliar topic
✅ Match depth to complexity

### 5. No Voice Profile
❌ Generic AI voice reduces engagement
✅ Create voice profile from your writing

### 6. Not Tracking Series
❌ Disconnected posts without continuity
✅ Use series continuity in drafts

---

## Validation Checklist

Before content is finalized, system validates:

**Functional:**
- ✅ All 6 sources queried
- ✅ 3 LinkedIn + 3 Blog drafts generated
- ✅ Word counts correct (150-300 LinkedIn, 800-1500 Blog)
- ✅ All drafts pass plagiarism check (<70% similarity)
- ✅ Voice matching applied (if profile exists)
- ✅ All citations verified
- ✅ Files saved to Obsidian

**Quality (55 points):**
- ✅ Personal branding (7 elements)
- ✅ LinkedIn quality (20 points)
- ✅ Blog quality (25 points)
- ✅ Research quality (21 points)
- ✅ No hallucinations
- ✅ Proper formatting

---

## Troubleshooting

### "No voice profile found"
**Impact:** Content uses generic voice
**Solution:**
1. Create voice profile from 5+ writing samples
2. Save to: `{OBSIDIAN_VAULT_PATH}/voice-profile/voice-profile-v1.json`
3. Or proceed without (lower quality)

### "Conflicts detected"
**Impact:** Contradictory information in sources
**Solution:**
1. Review `conflicts.md`
2. Check resolution or manually resolve
3. Verify final drafts don't include conflicting info

### "Plagiarism check failed"
**Impact:** Content too similar to source
**Solution:**
- System automatically retries with more paraphrasing
- Max 2 retries
- Flags for manual review if still fails

### "Voice match score low"
**Impact:** Content doesn't sound like you
**Solution:**
1. Check voice profile has 5,000+ words
2. Use diverse writing samples
3. Update profile with recent writing

---

## Advanced Features

### Series Management

Drafts automatically include:
- **Callback:** "Last week we learned about {previous topic}"
- **Current topic:** Today's content
- **Teaser:** "Next week I'll explain {next topic}"

**Manual Override:** Edit drafts to adjust series flow

### Paraphrasing Quality

All content is paraphrased to avoid plagiarism:
- **Semantic similarity:** >80% (meaning preserved)
- **Lexical dissimilarity:** <70% (words changed)
- **Validation:** Automatic checks before finalizing

### SEO Optimization (Blog)

Blogs include:
- Natural keyword usage (5-10 instances)
- SEO-friendly headers
- Meta description ready (first paragraph)
- Internal/external links
- Target SEO score: >0.80

### Engagement Prediction

System predicts engagement based on:
- Personal branding elements
- Concrete examples
- Voice match quality
- Technical depth
- Series continuity

**High engagement markers:**
- Strong personal framing
- Memorable examples
- Clear value proposition
- Series continuation

---

## Differences from research-generic

| Feature | research-topic | research-generic |
|---------|----------------|------------------|
| **Purpose** | LinkedIn/Blog personal branding | Objective research |
| **Output** | 6 drafts (3+3) | 1 output |
| **Platforms** | LinkedIn + Blog | 5 formats |
| **Personal Branding** | 55-point framework | Not applicable |
| **Voice Matching** | Yes (recommended) | No |
| **Series Continuity** | Yes (automatic) | No |
| **Word Count** | Fixed by platform | Flexible (500-3000+) |
| **Use Case** | Thought leadership | Technical docs |
| **Tone** | Personal, conversational | Objective, academic |

**When to Use Each:**
- **research-topic:** Building personal brand, LinkedIn/Blog, thought leadership
- **research-generic:** Documentation, research reports, objective analysis

---

## Updates & Changelog

### Version 2.0 (2025-11-19)
- ✅ Enhanced 55-point quality framework
- ✅ Added personal branding requirements
- ✅ LinkedIn-specific quality standards (20 points)
- ✅ Blog-specific quality standards (25 points)
- ✅ Comprehensive personal framing guide

### Version 1.0 (2025-11-17)
- Initial release
- 6-source research
- LinkedIn + Blog outputs
- 3 drafts per platform
- Voice matching
- PDF generation

---

## Reference Example

Your "Why Every AI Enthusiast Should Master Embeddings" post is the **gold standard**:

**✅ Perfect Structure:**
1. Personal framing: "My friends have often asked me..."
2. Series positioning: "creating my first post on AI"
3. Hook question: "Why embeddings? You may wonder..."
4. Definition with quote: "As Cloudflare puts it..."
5. Concrete example: "king - man + woman = queen"
6. Why this matters: "This means you can build smarter applications..."
7. Expert positioning: "difference between copying code and architecting solutions"
8. Resources: "Google's ML Crash Course offers hands-on tutorials"
9. Series continuity: "In next week's post, I will explain Vector Databases..."
10. Additional reading: 2 specific resources

**All generated drafts follow this pattern.**

---

## Support & Resources

### Documentation
- Full command spec: `.claude/commands/research-topic.md`
- Merged specification: `.claude/commands/research-topic-merged.md`
- Brave API setup: `docs/brave-api-configuration.md`

### Related Commands
- `/research-generic` - Objective research (not personal branding)
- `/core_commands:planning` - Feature planning

### Questions?
- Review this guide
- Check example posts
- Test with `--depth light --drafts 1`

---

## Success Metrics

Track these for continuous improvement:

### LinkedIn Posts
- Engagement rate (likes, comments, shares)
- Profile views increase
- Connection requests
- DM inquiries

### Blog Articles
- Page views
- Time on page
- Bounce rate
- Social shares
- SEO rankings

### Personal Brand
- Follower growth
- Thought leadership recognition
- Speaking/collaboration opportunities
- Professional opportunities

---

## License & Credits

Part of the Obsidian Agent project.
Powered by Brave Search, Claude AI, and open-source tools.

**Created:** 2025-11-17
**Last Updated:** 2025-11-19
**Version:** 2.0

---

## Final Tips

1. **Start Simple:** Use `--depth light --drafts 1` for your first test
2. **Create Voice Profile:** This makes the biggest quality difference
3. **Build Series:** Use series continuity to build recurring readership
4. **Track Results:** Update `user-selection.md` with engagement data
5. **Iterate:** Learn from metrics, adjust topics/depth
6. **Be Authentic:** Edit drafts to add your unique perspective

**Your personal brand is built one post at a time. This tool accelerates the research, but your voice and perspective make it authentic.**
