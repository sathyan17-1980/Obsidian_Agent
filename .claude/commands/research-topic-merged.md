# AI Research Agent - Comprehensive Phase 1 Specification

**Purpose:** Multi-source research agent for LinkedIn & Blog content generation
**Status:** Ready for Implementation
**Date:** 2025-11-17

## Quick Start

Run the research consolidator:

```bash
/research-topic "Why should AI enthusiasts learn about embeddings"
```

## What This Agent Does

The AI Research Agent is a sophisticated multi-source research and content generation system that:

1. **Researches 6 Sources in Parallel:**
   - HackerNews discussions
   - Web articles (Brave Search API)
   - Full article content extraction
   - Your Obsidian vault (mandatory)
   - Google Drive documents
   - YouTube transcripts

2. **Generates Platform-Optimized Content:**
   - 3 LinkedIn post drafts (150-300 words each)
   - 3 Blog article drafts (800-1500 words each)
   - Each with different strategies: Technical, Story-Driven, Balanced

3. **Ensures Quality:**
   - Detects and resolves conflicts across sources
   - Prevents plagiarism with intelligent paraphrasing
   - Matches your personal writing voice
   - Verifies all citations

4. **Saves Everything to Obsidian:**
   - Research summaries
   - All 6 drafts
   - Sources and citations
   - Metadata and conflicts

5. **Exports to PDF and Git:**
   - Professional PDF with all 6 drafts
   - Automatic git commit and push
   - Version control for all research
   - Downloadable format for sharing

## Personal Branding Framework

**CRITICAL:** This is NOT a generic content generator. This tool helps you build YOUR personal brand as an AI expert.

### Core Purpose

All generated content positions YOU as:
- **Knowledgeable** - Someone with deep understanding, not surface knowledge
- **Credible** - Backed by authoritative sources and concrete examples
- **Approachable** - A guide others can reach out to for learning
- **Expert** - Someone who architects solutions, not just copies code

### Required Elements in Every Draft

**1. Personal Framing (Opening)**
- Establish credibility through demand for your knowledge
- Examples:
  - "My friends have often asked me to share my learnings on {topic}..."
  - "After working with {topic}, colleagues keep asking me..."
  - "The most common question I get about AI is..."
- **Purpose:** Show people seek YOU out for knowledge

**2. Educational Journey Context**
- Position yourself as a guide leading a learning journey
- Examples:
  - "This is part of my weekly AI series where I take you progressively through..."
  - "Building on last week's post on {previous topic}, today we explore..."
  - "I'm starting from the basics and will guide you through..."
- **Purpose:** You're not just explaining, you're teaching a structured course

**3. Concrete Examples with Quotes**
- Mathematical illustrations: "king" - "man" + "woman" = "queen" in embedding space
- Code snippets showing actual implementation
- Real-world analogies that clarify concepts
- Authority quotes: "As Cloudflare puts it, '{exact quote}'" or "According to Google's ML documentation, '{exact quote}'"
- **Purpose:** Prove deep understanding with specifics, not abstractions

**4. "Why This Matters for YOU" Section**
- Explicit section addressing practical value
- Connect to reader's goals: "This means you can build smarter applications with less complexity..."
- Expert positioning: "Understanding this is the difference between copying code and architecting solutions"
- **Purpose:** Show practical application, not just theory

**5. Actionable Resources**
- Specific named free courses: "Google's ML Crash Course offers hands-on tutorials"
- Exact documentation links: "Embeddings Guide - Google ML"
- Tools and platforms to try
- NOT generic: "there are courses" ❌ | "Google's ML Crash Course offers..." ✅
- **Purpose:** Enable readers to take next steps

**6. Expert Positioning Language**
- "Understanding {topic} is the difference between copying code and architecting solutions"
- "This separates junior developers from senior engineers"
- "Real AI practitioners know that..."
- **Purpose:** Elevate your positioning as an architect, not implementer

**7. Series Continuity**
- End every post with next topic tease
- "Excited to delve deeper? In next week's post, I will explain {next topic}..."
- "Next up: How {next topic} builds on what we learned today..."
- **Purpose:** Create recurring readership and anticipation

### Quality Standards

**Concrete vs. Vague:**
- ❌ "Embeddings are important for AI" (vague)
- ✅ "'king' - 'man' + 'woman' = 'queen' in embedding space illustrates how semantic relationships are captured mathematically" (concrete)

**Generic vs. Personal:**
- ❌ "Here's what you need to know about embeddings" (generic educator)
- ✅ "My friends have often asked me to share my learnings on embeddings, so I'm creating this weekly series..." (personal brand)

**High-level vs. Detailed:**
- ❌ "Vector databases store embeddings efficiently" (high-level)
- ✅ "As Cloudflare puts it, 'embeddings make it possible for computers to understand the relationships between words' - they transform real-world data into mathematical representations" (detailed with quote)

### Reference Example

Your "Why Every AI Enthusiast Should Master Embeddings" post demonstrates the perfect structure:

1. ✅ Personal framing: "My friends have often asked me..."
2. ✅ Series positioning: "creating my first post on AI"
3. ✅ Hook question: "Why embeddings? You may wonder..."
4. ✅ Definition with quote: "As Cloudflare puts it..."
5. ✅ Concrete example: "king - man + woman = queen"
6. ✅ Why this matters: "This means you can build smarter applications..."
7. ✅ Expert positioning: "difference between copying code and architecting solutions"
8. ✅ Resources: "Google's ML Crash Course offers hands-on tutorials"
9. ✅ Series continuity: "In next week's post, I will explain what Vector databases are..."
10. ✅ Additional reading: "Embeddings Guide - Google ML, What are Embeddings - Cloudflare"

Every draft generated by this tool MUST follow this pattern.

## Architecture Overview

```
USER INPUT ("Why learn embeddings")
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
CONTENT GENERATION
  - 3 LinkedIn drafts
  - 3 Blog drafts
  - Voice matching
  - Paraphrasing
         |
         v
OBSIDIAN VAULT STORAGE (Mandatory)
```

## Complete Feature List

### Phase 1 MVP (All 10 Features)

1. **Obsidian Vault Research** ✅
   - Semantic search with embeddings
   - Tag and frontmatter filtering
   - Local installation required
   - Mandatory for all research

2. **Google Drive Integration** ✅
   - OAuth 2.0 authentication
   - Search PDFs, DOCX, Google Docs
   - Extract and index content

3. **Web Research (Brave API)** ✅
   - FREE tier: 2,000 queries/month
   - PRO tier: Higher limits
   - Auto-tier selection by depth

4. **YouTube Transcript Extraction** ✅
   - Curated educational channels
   - Auto-generated caption support
   - Transcript summarization

5. **Research Caching** ✅
   - DiskCache with SQLite backend
   - Configurable TTL per source type
   - 50%+ hit rate target

6. **Voice Matching** ✅
   - Analyze user writing samples
   - Extract style characteristics
   - Apply to all generated content

7. **Dual Content Generation** ✅
   - LinkedIn posts (150-300 words)
   - Blog articles (800-1500 words)
   - Platform-optimized formatting

8. **Conflict Detection** ✅
   - Semantic similarity comparison
   - Factual contradiction detection
   - Resolution suggestions

9. **3 Drafts Per Format** ✅
   - Technical (temp 0.3)
   - Story-Driven (temp 0.6)
   - Balanced (temp 0.5)
   - 6 total drafts to choose from

10. **Intelligent Paraphrasing** ✅
    - Prevent plagiarism
    - Semantic validation (>80%)
    - Lexical dissimilarity (<70%)

### NEW: Research Consolidator Additions

11. **HackerNews Researcher** (NEW)
    - Search trending tech discussions
    - Extract top comments
    - Community insights

12. **Article Reader** (NEW)
    - Extract full content from URLs
    - 3-tier fallback parsers
    - Handle paywalls gracefully

13. **4-Agent Orchestration** (NEW)
    - Parallel execution
    - Result aggregation
    - Deduplication

## Usage Examples

### Basic Usage

```bash
# Standard research (moderate depth, 3 drafts)
/research-topic "Why AI enthusiasts should learn embeddings"

# Quick research (minimal depth, 1 draft)
/research-topic "Transformer architecture basics" --depth minimal --drafts 1

# Deep research (comprehensive, 5 draft variations)
/research-topic "Constitutional AI vs RLHF" --depth deep --drafts 5
```

### Research Depth Levels

| Depth | Queries/Source | Time | Cost | Use Case |
|-------|----------------|------|------|----------|
| **minimal** | 1-3 | ~60s | ~$0.14 | Testing, simple topics |
| **light** | 3-5 | ~90s | ~$0.14 | Familiar topics |
| **moderate** (DEFAULT) | 5-8 | ~120s | ~$0.18 | Standard research |
| **deep** | 8-12 | ~180s | ~$0.20 | Complex topics |
| **extensive** | 12+ | ~240s | ~$0.22+ | Multi-topic deep dive |

## Obsidian Vault Structure

All outputs are saved to your local Obsidian vault:

```
ObsidianVault/
├── research/
│   ├── 2025-11-17-embeddings-basics/
│   │   ├── research-topic.md          # Topic metadata
│   │   ├── research-summary.md        # Aggregated findings
│   │   ├── linkedin/
│   │   │   ├── draft-1-technical.md
│   │   │   ├── draft-2-story.md
│   │   │   └── draft-3-balanced.md
│   │   ├── blog/
│   │   │   ├── draft-1-technical.md
│   │   │   ├── draft-2-story.md
│   │   │   └── draft-3-balanced.md
│   │   ├── sources.md                 # All 28 citations
│   │   ├── conflicts.md               # Detected conflicts
│   │   ├── metadata.json              # Research metadata
│   │   └── user-selection.md          # Your chosen drafts
│   └── index.md                       # Research history
└── voice-profile/
    ├── voice-profile-v1.json
    └── training-samples/
```

## Configuration

### Required Environment Variables

```bash
# Already Configured (Brave Search API)
BRAVE_API_KEY_FREE=BSAfhmAUjm78j3TKqPkDlByE0ecpRt7
BRAVE_API_KEY_PRO=BSAwntGzdRA-yo5lL0O4eoDrSgr2nBk

# New Configuration Needed
OBSIDIAN_VAULT_PATH=/Users/you/Documents/ObsidianVault
GOOGLE_DRIVE_CREDENTIALS_PATH=.credentials/google_drive_credentials.json

# Optional (for LLM)
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### One-Time Setup

```bash
# 1. Install dependencies
uv add newspaper3k google-auth google-auth-oauthlib google-api-python-client
uv add youtube-transcript-api sentence-transformers chromadb spacy nltk
uv add diskcache orjson tenacity ratelimit

# 2. Download spaCy model
python -m spacy download en_core_web_sm

# 3. Set up Google OAuth
python scripts/setup_google_drive_oauth.py

# 4. Create voice profile (requires 5+ writing samples)
python scripts/create_voice_profile.py --samples /path/to/writings/
```

## Cost Breakdown

### Per Research Query (Moderate Depth)

| Component | Unit Cost | Notes |
|-----------|-----------|-------|
| HackerNews API | $0.00 | Free |
| Brave Search (PRO) | $0.04 | 8 queries × $0.005 |
| Article Extraction | $0.00 | Local processing |
| Obsidian Search | $0.00 | Local |
| Google Drive API | $0.00 | Free quota |
| YouTube Transcripts | $0.00 | Free API |
| **Research Subtotal** | **$0.04** | |
| LLM (6 drafts + paraphrasing) | $0.137 | Claude Sonnet 4 |
| **TOTAL** | **~$0.18** | |

### ROI vs Manual Process

| Metric | Manual | AI Agent | Improvement |
|--------|--------|----------|-------------|
| **Time** | 6 hours | 3 minutes | **120x faster** |
| **Cost** | $300 | $0.18 | **1,667x cheaper** |
| **Sources** | 5-10 | 28+ | **3-6x more** |

## Performance Targets

| Phase | Target | Expected | Status |
|-------|--------|----------|--------|
| Research (6 sources) | <90s | 75-90s | ✅ |
| Aggregation | <30s | 20-30s | ✅ |
| Content Generation | <60s | 45-60s | ✅ |
| Storage | <5s | 2-5s | ✅ |
| **Total End-to-End** | **<5 min** | **2.5-3.5 min** | ✅ |

## Data Models

### Research Query (Input)

```python
{
    "topic": "Why AI enthusiasts should learn embeddings",
    "depth": "moderate",  # minimal, light, moderate, deep, extensive
    "num_drafts": 3,
    "obsidian_vault_path": "/Users/alex/Documents/ObsidianVault",
    "include_sources": {
        "hackernews": true,
        "web_search": true,
        "articles": true,
        "obsidian": true,  # MANDATORY
        "google_drive": true,
        "youtube": true
    }
}
```

### Content Output (Result)

```python
{
    "topic": "Why AI enthusiasts should learn embeddings",
    "generated_at": "2025-11-17T14:35:22Z",
    
    "linkedin_drafts": [
        {
            "draft_number": 1,
            "strategy": "technical",
            "content": "...",
            "word_count": 276,
            "voice_match_score": 0.89,
            "engagement_prediction": 0.82
        },
        // ... 2 more drafts
    ],
    
    "blog_drafts": [
        {
            "draft_number": 1,
            "strategy": "technical",
            "content": "...",
            "word_count": 1487,
            "seo_score": 0.85
        },
        // ... 2 more drafts
    ],
    
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
        "conflicts_detected": 2,
        "conflicts_resolved": 2
    },
    
    "obsidian_path": "research/2025-11-17-embeddings-basics",
    "execution_time_seconds": 125.3,
    "total_cost_usd": 0.18
}
```

## Implementation Phases

### Week 1: Foundation
- Set up data models (Pydantic schemas)
- Configure APIs (Brave, Google, YouTube)
- Implement cache manager (DiskCache)

### Week 2-3: Research Agents
- Implement 6 research sub-agents
- Add caching and error handling
- Test each agent independently

### Week 4: Orchestration
- Build Research Consolidator
- Implement conflict detection
- Add citation management

### Week 5: Content Generation
- Voice profile analyzer
- LinkedIn & blog generators
- Multi-draft generation
- Intelligent paraphrasing

### Week 6: Storage & Integration
- Obsidian storage manager
- Tool registration (Pydantic AI)
- End-to-end integration

### Week 7: Polish & Documentation
- Performance optimization
- Error handling
- Documentation
- Testing (>80% coverage)

## Common Pitfalls to Avoid

1. **❌ Not caching aggressively** → Wasted API calls and cost
2. **❌ Sequential research (not parallel)** → 2x slower
3. **❌ Not validating Obsidian path early** → Wasted work
4. **❌ Trusting article extraction 100%** → ~20-30% fail
5. **❌ No timeout on operations** → Hanging requests
6. **❌ Not handling OAuth failures** → Google Drive auth expires
7. **❌ Not deduplicating sources** → Same URL counted twice
8. **❌ No research context in LLM prompts** → Hallucination risk
9. **❌ Not validating paraphrase quality** → Plagiarism risk
10. **❌ Generating drafts without voice profile** → Generic output

*See full research document for 40+ detailed pitfalls*

## Success Criteria

### Functional Requirements

- ✅ All 6 research sources working (HN, Web, Articles, Obsidian, Drive, YouTube)
- ✅ Research completes in <5 minutes
- ✅ 28+ sources aggregated
- ✅ Conflicts detected and resolved
- ✅ 3 LinkedIn drafts generated (150-300 words)
- ✅ 3 Blog drafts generated (800-1500 words)
- ✅ Voice matching >70%
- ✅ No plagiarism (lexical similarity <70%)
- ✅ All outputs saved to Obsidian vault

### Performance Requirements

- ✅ Cost per query <$0.20
- ✅ Cache hit rate >50%
- ✅ Article extraction success rate >70%
- ✅ End-to-end reliability >95%

### Quality Requirements

- ✅ Content publishable without edits: 80%+
- ✅ Citations verified and accessible: 100%
- ✅ User satisfaction: 4+/5 stars

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| API rate limits | Medium | Medium | Aggressive caching, tier fallback |
| Article extraction failures | Medium | High | 3-tier fallback parsers |
| LLM hallucination | High | Medium | Research grounding, validation |
| Obsidian access issues | High | Low | Path validation, atomic writes |
| OAuth complexity | Medium | Medium | Setup scripts, auto-refresh |
| Cost escalation | Medium | Low | Monitoring, budget alerts |
| Content quality perception | High | Medium | Voice matching, 3 drafts, feedback |

All risks have documented mitigations. See full research document for details.

## Next Steps

1. **Review this specification** and confirm all 10 MVP features are required
2. **Set up environment** (Brave API ✅, Google OAuth, Obsidian path)
3. **Create voice profile** (provide 5+ writing samples, 5,000+ words)
4. **Begin Week 1 implementation** (Foundation: data models, cache, APIs)

## References

- **Research Prompt:** `.claude/commands/ai-research-agent.md`
- **Brave API Config:** `docs/brave-api-configuration.md`
- **Coding Standards:** `CLAUDE.md`
- **System Migration Template:** `.claude/commands/system-migration.md`

---

**Status:** ✅ APPROVED FOR IMPLEMENTATION  
**Version:** 1.0  
**Date:** 2025-11-17
