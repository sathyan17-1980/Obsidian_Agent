# Research Prompt: AI Research Agent for LinkedIn & Blog Content Creation

## Task Description

You are tasked with conducting comprehensive research for a new AI research agent that generates LinkedIn posts and blog articles. This is a **research-only task** - do NOT implement code, only analyze feasibility, design architecture, and document findings.

---

## Problem Statement

**Core Idea**: Build an AI agent-powered research tool that accepts a topic as input, scans internal documents (Obsidian vault) and the web (HackerNews, Brave Search), and generates two outputs:
1. **LinkedIn Post**: Short, engaging, platform-optimized (150-300 words)
2. **Blog Article**: Comprehensive, detailed, educational (800-1500 words)

**User Need**: Content creators spend 3-6 hours researching topics, synthesizing information from multiple sources, and crafting platform-specific content. For example:
- **Topic**: "Why should AI enthusiasts learn about how embeddings work"
- **Current Process**: Manually search HackerNews, Google, internal notes → copy-paste → rewrite for each platform
- **Expected Output**: Agent should:
  - Research HackerNews for trending discussions on embeddings
  - Search web for authoritative articles/tutorials
  - Extract key insights from article URLs
  - Scan internal Obsidian notes for personal perspectives
  - Generate LinkedIn post (concise, hook-first, with links)
  - Generate blog article (comprehensive, structured, educational)

**Scope**:
- Multi-source research (HackerNews API, Brave Search API, newspaper4k article extraction, Obsidian vault)
- Intelligent orchestration (4 specialized agents working in coordination)
- Platform-optimized output (LinkedIn vs Blog formatting/length/tone)
- Reference tracking (all sources cited with links)
- Token efficiency (minimal research for simple topics, detailed for complex)

---

## Research Standards & Templates

Your research MUST align with the following standards and templates:

### 1. Coding Standards (Base Architecture)

**Source**: `CLAUDE.md` from the Obsidian_Agent repository
**Location**: `/home/user/Obsidian_Agent/CLAUDE.md`

**Key Requirements**:
- Use vertical slice architecture (each tool is independent: `tool.py`, `schemas.py`, `service.py`)
- All code must have strict type safety (Pydantic models, mypy strict mode)
- Structured logging optimized for AI debugging (Structlog with keyword arguments)
- Agent-centric tool docstrings with specific sections:
  - "Use this when you need to:" (affirmative guidance)
  - "Do NOT use this for:" (negative guidance pointing to alternative tools)
  - Performance Notes (token costs, execution time, resource limits)
  - Realistic examples (not foo/bar, use actual topics/scenarios)
- Testing mirrors source structure (every `src/` file has `tests/` equivalent)

### 2. Global Rules (Core Principles)

**Key Principles**:
1. **TYPE SAFETY IS NON-NEGOTIABLE**: All functions/methods/variables MUST have type annotations, strict mypy enforcement
2. **KISS & YAGNI**: Simple solutions over abstractions, avoid building unrequired features
3. **Vertical Slice Architecture**: Organize as independent slices with schemas, services, tools
4. **Agent Tool Docstrings**: Guide LLM reasoning during tool selection (critical for agent performance)
5. **Structured Logging**: AI-comprehensible logs with descriptive event names, debugging context, masked sensitive data

### 3. Research Document Template

**Required Sections** (in order):
1. **Mission Statement**:
   - Feature Name: [One line]
   - Problem: [One sentence describing the problem]
   - Goal: [One sentence describing what should be achieved]
   - Scope:
     - ✅ **Included**: [Bullet list of what's in scope]
     - ❌ **Excluded**: [Bullet list of what's explicitly out of scope]

2. **Context Assessment**:
   - **Current State**:
     - ✅ What already exists and works?
     - ⚠️ What problems exist?
     - ❌ What's missing?
   - **Architecture**: Proposed structure diagram
   - **Dependencies**: What components can be reused? What's needed?

3. **Problem Domain Analysis**:
   - Current manual process (status quo)
   - User personas and their needs
   - Real-world examples
   - Success criteria (Must Have / Should Have / Could Have)

4. **Architecture Design**:
   - Application of vertical slice pattern
   - Data models (Pydantic schemas with full type annotations)
   - Tool interfaces (agent-facing tools with comprehensive docstrings)
   - Multi-agent orchestration design

5. **Technical Implementation Strategy**:
   - Phase-by-phase breakdown (Foundation → Core Features → Integration)
   - Each phase with: Goal, Tasks, Testing approach, Validation commands

6. **Cost & Performance Analysis**:
   - Cost breakdown (LLM API costs, external APIs, infrastructure, etc.)
   - Performance targets (latency, throughput, scalability)
   - Comparison to manual content creation

7. **Risk Assessment & Mitigation**:
   - Technical risks (with impact, likelihood, mitigation)
   - Business risks (with impact, likelihood, mitigation)

8. **Common Pitfalls to Avoid**:
   - ❌ **Don't** [anti-pattern] - [explanation and what to do instead]
   - Organize by category (Research, Content Generation, Agent Orchestration, etc.)
   - 40+ specific pitfalls covering implementation mistakes

9. **Success Criteria Template**:
   - ✅ **Functional Requirements**: [Checkboxes for each feature]
   - ✅ **Non-Functional Requirements**: [Performance, Type Safety, Logging, Security]
   - ✅ **Documentation Requirements**: [README, API docs, deployment guides]
   - ✅ **Testing Requirements**: [Unit, Integration, Validation tests]
   - ✅ **Deployment Requirements**: [Docker, config, health checks]

10. **Conclusion**:
    - Summary of key strengths
    - Risks with mitigations
    - Go/No-Go decision criteria
    - Recommendation (next steps)

---

## Reference Architecture

**Base Project**: Obsidian AI Agent
**Repository**: `https://github.com/sathyan17-1980/Obsidian_Agent`

**Key Patterns to Reuse**:
- FastAPI + Pydantic AI for agent orchestration
- OpenAI-compatible API endpoints
- Vertical slice architecture in `src/tools/`
- Shared utilities in `src/shared/` (config, logging, security)
- Testing patterns from `tests/` with pytest markers (@pytest.mark.unit, @pytest.mark.integration)

**Multi-Agent Architecture Pattern**:
```
src/tools/research_agent/
├── __init__.py
├── schemas.py              # Pydantic models (ResearchQuery, ContentOutput, etc.)
├── orchestrator.py         # Research Consolidator agent (main coordinator)
├── hackernews_agent.py     # HackerNews Researcher sub-agent
├── web_search_agent.py     # Web Searcher sub-agent
├── article_reader_agent.py # Article Reader sub-agent
├── content_generator.py    # LinkedIn/Blog content generation logic
├── service.py              # Business logic (coordination, aggregation)
└── tool.py                 # Agent registration (@agent.tool with comprehensive docstring)

tests/tools/research_agent/
├── test_schemas.py         # Schema validation tests
├── test_orchestrator.py    # Orchestrator agent tests
├── test_hackernews_agent.py
├── test_web_search_agent.py
├── test_article_reader_agent.py
├── test_content_generator.py
├── test_service.py         # Service layer unit tests
└── test_tool.py            # Tool integration tests
```

---

## Specific Requirements for This Research

### Core Functionality to Research

1. **Multi-Agent Orchestration**:
   - How to coordinate 4 agents (1 orchestrator + 3 specialized sub-agents)
   - Communication patterns (sequential vs parallel execution)
   - Error handling when sub-agents fail
   - Result aggregation and deduplication
   - Performance: Target end-to-end research in <2 minutes

2. **HackerNews Research Agent**:
   - HackerNews API integration (Algolia HN Search API)
   - Search strategies (keyword match, ranking by points/relevance)
   - Story filtering (min points threshold, time range)
   - Comment extraction (top comments for context)
   - Performance: <10 seconds for top 10 stories

3. **Web Search Agent**:
   - Brave Search API integration
   - Query formulation from topic
   - Result ranking and relevance filtering
   - Domain authority consideration (prefer authoritative sources)
   - Performance: <5 seconds for top 10 results

4. **Article Reader Agent**:
   - newspaper4k integration for content extraction
   - HTML parsing and main content detection
   - Handling paywalls and dynamic content
   - Summary generation (key points extraction)
   - Performance: <3 seconds per article, max 10 articles

5. **Obsidian Vault Integration**:
   - Reuse existing obsidian_note_manager tool
   - Vector search for semantic similarity to topic
   - Tag-based filtering (e.g., #ai, #embeddings)
   - Relevance ranking by content similarity
   - Performance: <5 seconds for vault search

6. **Content Generation**:
   - LinkedIn post generation (150-300 words, hook-first, platform voice)
   - Blog article generation (800-1500 words, structured, educational)
   - Citation management (reference all sources)
   - Tone adaptation (professional LinkedIn vs conversational Blog)
   - Performance: <30 seconds for both outputs

### Technical Decisions to Research

1. **Agent Orchestration Strategy**:
   - Sequential execution (HN → Web → Articles → Obsidian → Generate)
   - Parallel execution (all research agents run concurrently)
   - Hybrid approach (research parallel, generation sequential)
   - Pydantic AI RunContext sharing between agents
   - Error recovery and retry logic

2. **AI/LLM Strategy**:
   - Which LLM for content generation (GPT-4, Claude Sonnet, etc.)
   - Prompt engineering for LinkedIn vs Blog tone
   - How to structure research context for generation
   - Token optimization (summarize research before generation)
   - Cost per content piece (research + generation)

3. **External API Integration**:
   - HackerNews Algolia API (https://hn.algolia.com/api)
   - Brave Search API (authentication, rate limits, pricing)
   - newspaper4k Python library (installation, dependencies)
   - API error handling and fallbacks
   - Rate limit management and caching

4. **Performance & Cost Optimization**:
   - When to run agents in parallel vs sequential
   - How to cache research results (same topic reuse)
   - Token efficiency (minimal summaries vs full content)
   - API cost management (Brave Search pricing tier)
   - Time budget allocation per agent

5. **Content Quality Assurance**:
   - How to validate generated content (no hallucinations)
   - Citation accuracy (all sources verifiable)
   - Platform compliance (LinkedIn character limits, formatting)
   - Plagiarism detection and originality
   - Fact-checking mechanisms

6. **Security & Privacy**:
   - API key management (Brave Search, LLM providers)
   - Obsidian vault access permissions
   - User data isolation (multi-user scenarios)
   - Input validation to prevent injection attacks
   - Audit logging for research queries

### Business Viability to Assess

1. **Market Analysis**:
   - Existing solutions (Jasper AI, Copy.ai, ContentBot, human writers)
   - Competitive advantages (multi-source research, Obsidian integration)
   - Target users (content creators, technical bloggers, thought leaders)

2. **Pricing Strategy**:
   - Free tier (5 research queries/month)
   - Pay-as-you-go ($0.50 per research query)
   - Subscription ($20/month for 50 queries)
   - ROI vs manual content creation (6 hours × $50/hr = $300 saved)

3. **Go-to-Market**:
   - Target customers (indie hackers, tech bloggers, marketing teams)
   - Distribution channels (Obsidian plugin marketplace, web app)
   - Partnerships (content platforms, SEO tools)

4. **Risk Assessment**:
   - Technical risks (API rate limits, LLM hallucination, article extraction failures)
   - Business risks (content quality perception, market adoption, API costs)
   - Mitigations for each risk

---

## Expected Deliverables

### Primary Output: Research Document

**File**: `ai-research-agent-analysis.md`
**Location**: `plans/` directory
**Length**: 1500-2000 lines (comprehensive)

**Must Include**:
1. Mission Statement (Problem/Goal/Scope with ✅/❌ format)
2. Context Assessment (✅/⚠️/❌ current state, architecture, dependencies)
3. Problem Domain Analysis (manual process, user personas, examples)
4. Architecture Design (4 agents, data models, tool docstrings, orchestration)
5. Implementation Strategy (6 phases with tasks/testing/validation)
6. Storage Architecture (research cache, result persistence)
7. Cost & Performance Analysis (API costs, token usage, time budgets)
8. Risk Assessment (technical + business with mitigations)
9. Common Pitfalls (40+ anti-patterns organized by category)
10. Success Criteria Template (functional, non-functional, docs, testing)
11. Conclusion (strengths, risks, go/no-go criteria, recommendation)

### Tool Docstrings (7 Required)

For each agent tool, provide **complete docstring** following the template in CLAUDE.md:

**Required Tools**:
1. `research_topic` - Main entry point (orchestrator tool)
2. `hackernews_research` - Search HackerNews for stories
3. `web_search` - Search web using Brave API
4. `article_extract` - Extract content from URLs
5. `obsidian_vault_research` - Search internal notes
6. `generate_linkedin_post` - Create LinkedIn content
7. `generate_blog_article` - Create blog content

Each tool docstring must include:
- One-line summary
- "Use this when you need to:" (5+ scenarios)
- "Do NOT use this for:" (3+ scenarios with alternatives)
- Args with parameter guidance and token implications
- Returns with format structure
- Performance Notes (token usage, execution time, costs)
- Examples (3+ realistic scenarios)

### Data Models (Pydantic Schemas)

Provide complete Pydantic models with:
- Strict type annotations (no `Any` without justification)
- Field descriptions
- Validation logic (@model_validator where needed)
- Enums for categorical values

**Required Models**:
- `ResearchQuery` (topic, depth, sources, output formats)
- `HackerNewsStory` (title, url, points, comments, timestamp)
- `WebSearchResult` (title, url, snippet, domain)
- `ArticleContent` (url, title, text, author, publish_date)
- `ObsidianNote` (path, content, tags, relevance_score)
- `ResearchContext` (aggregated research from all sources)
- `LinkedInPost` (content, hashtags, word_count, citations)
- `BlogArticle` (title, content, sections, word_count, citations)
- `ContentOutput` (linkedin_post, blog_article, research_summary)

---

## Quality Criteria

Your research will be evaluated on:

### Completeness (40%)
- [ ] All 10 required sections present
- [ ] 7 tool docstrings with all subsections
- [ ] 9 data models with complete type annotations
- [ ] 40+ common pitfalls documented
- [ ] 60+ success criteria checkboxes

### Alignment with Templates (30%)
- [ ] Mission Statement in exact format (Problem/Goal/Scope)
- [ ] Context Assessment with ✅/⚠️/❌ symbols
- [ ] Common Pitfalls section present
- [ ] Success Criteria Template at end
- [ ] Follows CLAUDE.md structure

### Technical Depth (20%)
- [ ] Architecture design is specific (4-agent orchestration detailed)
- [ ] Cost analysis has actual numbers (Brave API + LLM costs)
- [ ] Performance targets are measurable (<2 min end-to-end)
- [ ] Risk mitigations are actionable
- [ ] Implementation phases have clear deliverables

### Actionability (10%)
- [ ] Can transition directly to implementation
- [ ] Validation commands are exact (pytest commands, API tests)
- [ ] Examples use realistic data (actual topics like "embeddings", "RAG")
- [ ] Go/No-Go criteria are clear
- [ ] Recommendation includes specific next steps

---

## Constraints & Guidelines

### What to DO:
✅ Research HackerNews Algolia API documentation
✅ Research Brave Search API pricing and capabilities
✅ Research newspaper4k library features and limitations
✅ Provide realistic cost estimates (Brave API + LLM costs)
✅ Design complete data models (Pydantic with all fields)
✅ Document 40+ common pitfalls (multi-agent coordination, API failures)
✅ Create 60+ success criteria (validation checklist)
✅ Include real-world examples (actual topics, real HN stories)
✅ Calculate ROI vs manual content creation (6 hours baseline)
✅ Consider security (API keys, vault access, audit logging)

### What NOT to DO:
❌ Do NOT write implementation code (research only)
❌ Do NOT use vague placeholders ("TBD", "to be determined")
❌ Do NOT skip sections from the template
❌ Do NOT use toy examples (foo/bar/test-topic)
❌ Do NOT ignore performance constraints (must have targets)
❌ Do NOT forget token efficiency (minimal/concise/detailed formats)
❌ Do NOT omit risk mitigations (every risk needs mitigation plan)
❌ Do NOT assume 100% LLM accuracy (document quality validation)

---

## Research Process Recommendations

### Phase 1: Understand the Domain (30 minutes)
1. Research existing AI content tools (Jasper, Copy.ai, ContentBot)
2. Understand manual content creation process (research → outline → write)
3. Identify user personas (Tech Blogger, Content Marketer, Thought Leader)
4. Document real-world example (topic → LinkedIn + Blog)

### Phase 2: Design Architecture (60 minutes)
1. Design 4-agent orchestration pattern (1 coordinator + 3 specialists)
2. Design 7 core tools (research, hackernews, web, article, vault, linkedin, blog)
3. Create data models (ResearchQuery, HNStory, WebResult, ArticleContent, etc.)
4. Design agent communication (RunContext sharing, result passing)

### Phase 3: Technical Analysis (45 minutes)
1. Research HackerNews Algolia API (endpoints, rate limits)
2. Research Brave Search API (pricing, capabilities, limits)
3. Research newspaper4k library (installation, usage, edge cases)
4. Calculate costs (Brave + LLM tokens per research query)
5. Set performance targets (time budget per agent)

### Phase 4: Risk & Viability (30 minutes)
1. Identify technical risks (API failures, extraction errors, LLM hallucination)
2. Identify business risks (content quality, market adoption, API costs)
3. Define mitigations for each risk
4. Calculate ROI (AI tool cost vs $300 manual creation baseline)

### Phase 5: Documentation (60 minutes)
1. Write all 10 required sections in order
2. Create 40+ common pitfalls (organized by category)
3. Create 60+ success criteria (functional, non-functional, docs, testing)
4. Write comprehensive tool docstrings (7 tools with all subsections)
5. Proofread for template compliance

---

## Success Indicators

You've completed the research successfully when:

1. ✅ **Template Compliance**: All sections from template present
2. ✅ **Principle Adherence**: TYPE SAFETY, KISS, YAGNI, vertical slices mentioned
3. ✅ **Completeness**: 1500+ lines covering all required topics
4. ✅ **Specificity**: Numbers, not hand-waving ("$0.50 per query", not "cheap")
5. ✅ **Actionability**: Another agent could implement from your research alone
6. ✅ **Realistic Examples**: Real topics (embeddings, RAG, AI safety), not foo/bar
7. ✅ **Tool Docstrings**: All 7 tools have complete agent-centric documentation
8. ✅ **Data Models**: Full Pydantic schemas with strict types
9. ✅ **Common Pitfalls**: 40+ anti-patterns documented
10. ✅ **Success Criteria**: 60+ validation checkboxes

---

## Questions to Answer Through Research

Your research should definitively answer:

1. **Feasibility**: Can this be built with current APIs/libraries? (HN API + Brave + newspaper4k)
2. **Architecture**: What's the optimal multi-agent design? (4 agents, orchestration pattern)
3. **Cost**: What's the total cost per research query? (Target: <$1)
4. **Performance**: Can it meet targets? (<2 minutes end-to-end)
5. **Quality**: Can it match human content quality? (vs 6 hours manual work)
6. **Viability**: Is there a market? (vs Jasper, Copy.ai, manual writing)
7. **Go/No-Go**: Should this be built? (Based on cost/quality validation)

---

## Final Checklist

Before submitting research, verify:

- [ ] Mission Statement uses exact template format
- [ ] Context Assessment has ✅/⚠️/❌ symbols
- [ ] All 7 tool docstrings have 8 required subsections
- [ ] All 9 data models use Pydantic with strict types
- [ ] Common Pitfalls section has 40+ anti-patterns
- [ ] Success Criteria section has 60+ checkboxes
- [ ] Cost analysis includes specific numbers (Brave + LLM costs)
- [ ] Performance targets are measurable (<2 min, <10s per agent)
- [ ] Examples use realistic data (real topics, HN stories)
- [ ] Conclusion includes go/no-go criteria
- [ ] Document is 1500+ lines
- [ ] All sections from template present

---

**Begin research now. Focus on depth, specificity, and actionability. This research should enable an implementation decision without further investigation.**
