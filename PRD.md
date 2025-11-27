# Product Requirements Document: Nithya-Creator

**Version**: 1.0
**Date**: 2025-01-27
**Status**: Planning Complete - Ready for Implementation
**Owner**: KIDZ SEASON TV

---

## Executive Summary

**Nithya-Creator** is an AI-powered YouTube video production assistant that automates prompt generation for family-friendly educational content. The system reduces video production time from 3+ hours to ~2 hours by generating production-ready prompts for images, animations, dialogue, voice, and music across all video scenes in a single workflow.

Built for the **KIDZ SEASON TV** YouTube channel, Nithya-Creator enables rapid creation of high-quality Tamil and English moral stories with consistent characters (like Kavi the Peacock) and professional production values. The MVP focuses on manual workflow integration with existing tools (Leonardo.ai, MiniMax Hailuo, Suno, Azure TTS), with future expansion planned for other content creators.

**Key Value Proposition**: Turn a story idea into complete production prompts in under 1 minute, maintain character consistency across series, and iterate quickly based on feedback.

---

## Mission & Vision

### Mission
Empower content creators to produce high-quality, culturally authentic educational videos at scale by automating the creative-technical workflow while preserving artistic control.

### Vision
**Short-term (6 months)**: Become the primary production tool for KIDZ SEASON TV, enabling 2-3 videos per week with consistent quality.

**Long-term (12-24 months)**: Expand Nithya-Creator to serve 100+ educational content creators, offering character libraries, series planning, analytics, and team collaboration features.

---

## Target Users

### Primary User (MVP)
**Profile**: Solo content creator for KIDZ SEASON TV
**Needs**:
- Rapidly generate production prompts for 4-5 minute videos
- Maintain character consistency across episodes (Kavi the Peacock series)
- Reduce manual prompt writing time
- Iterate quickly when scenes fail in production
- Produce both Tamil and English content for general audience

**Pain Points**:
- Manual prompt writing takes 30-45 minutes per video
- Character inconsistency across scenes
- No systematic workflow for series continuity
- Time-consuming refinement when tools produce poor results
- Difficult to maintain quality at 2-3 videos/week pace

### Future Users (Post-MVP)
**Profile**: Educational content creators (individual/small teams)
**Characteristics**:
- Produce family-friendly content in various languages
- Need character library management
- Want analytics to track video performance
- Require team collaboration (writer, editor, producer roles)
- Batch processing for series production (10-20 videos)

---

## Success Metrics

### Primary Metrics (MVP)

| Metric | Baseline | Target (3 months) | Measurement |
|--------|----------|-------------------|-------------|
| **Video Production Time** | 3+ hours | <2 hours | Time from idea to final video |
| **Videos Produced/Week** | 1-2 | 2-3 | Weekly output count |
| **Scene Success Rate** | ~70% | >90% | Scenes generated correctly on first try |
| **Prompt Generation Time** | 30-45 min | <5 min | Time to generate all scene prompts |

### Secondary Metrics

- **Character Consistency**: >95% scenes maintain character appearance (measured by visual review)
- **Workflow Completion Rate**: >80% videos complete full workflow without abandonment
- **User Satisfaction**: Qualitative feedback on ease of use, quality of prompts

### Future Metrics (Post-MVP)

- **Active Creators**: Number of creators using Nithya-Creator
- **Videos Created**: Total videos produced across all users
- **Retention Rate**: Monthly active users (MAU)
- **Character Reuse**: Percentage of videos using character library
- **Series Completion**: Videos in series vs standalone

---

## MVP Scope

### In Scope ✅

**Core Workflow**:
1. ✅ Idea analysis (song vs drama recommendation + copyright check)
2. ✅ Scene structure generation (6-8 scenes for drama, 3-5 for song)
3. ✅ Complete prompt generation (image, animation, dialogue, voice, music)
4. ✅ Feedback processing and scene refinement
5. ✅ Timeline assembly instructions (FFmpeg/Shotstack)
6. ✅ YouTube metadata generation (title, description, tags, thumbnail)

**Character Management**:
- ✅ New character creation (user generates reference image)
- ✅ Existing character reuse (reference image system)
- ✅ Series continuity support (Kavi the Peacock episodes)

**Languages**:
- ✅ Tamil (primary)
- ✅ English
- ✅ Bilingual (both languages in same video)

**Integration**:
- ✅ Manual workflow with Leonardo.ai, MiniMax Hailuo, Suno, Azure TTS, ElevenLabs
- ✅ Stateless feedback loop (no database required)

**API**:
- ✅ OpenAI-compatible endpoint (`/v1/chat/completions`)
- ✅ Direct workflow endpoints (`/api/workflows/video/*`)
- ✅ Hybrid approach for flexibility

### Out of Scope ❌ (MVP)

- ❌ Direct API integrations (Leonardo.ai, MiniMax API calls) - manual only
- ❌ Automated video assembly - user runs FFmpeg/Shotstack manually
- ❌ Character library UI - manual file management
- ❌ Analytics dashboard - no tracking/metrics
- ❌ Multi-user support - single user only
- ❌ Series planning tools - manual episode planning
- ❌ Batch processing - one video at a time
- ❌ Database persistence - stateless only
- ❌ Authentication/authorization - local deployment

### Future Roadmap (Post-MVP)

**Phase 2 (3-6 months)** - Character Library & Analytics:
- Character library management UI (browse, select, upload characters)
- Analytics dashboard (videos produced, success rates, character usage)
- Series planning tools (brainstorm episodes, track series)
- PostgreSQL for data persistence

**Phase 3 (6-12 months)** - Multi-User & Collaboration:
- User authentication and authorization
- Team collaboration (roles: creator, editor, reviewer)
- Shared character libraries
- Template library (reusable story patterns)

**Phase 4 (12-24 months)** - API Integrations & Automation:
- Direct Leonardo.ai API integration (skip manual paste)
- MiniMax Hailuo API integration
- Automated video assembly (end-to-end)
- Batch processing (generate 10 videos in one workflow)
- Advanced analytics (view counts, engagement, A/B testing)

---

## Core Architecture

### Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Agent Framework** | Pydantic AI | Type-safe tool calling, dependency injection |
| **API Framework** | FastAPI | Async support, auto-generated docs, high performance |
| **Package Manager** | UV | Fast, reliable dependency management |
| **Type Safety** | Ruff + mypy (strict) | Catch errors early, better IDE support |
| **Logging** | Structlog | AI-optimized, structured logs for debugging |
| **LLM** | Claude Sonnet 4.5 | Best creative writing, 3.3x cheaper than GPT-4 |
| **Deployment** | Docker + Railway/Render | Simple containerized deployment |

### Architecture Pattern: Vertical Slice Architecture (VSA)

```
app/
├── main.py                    # FastAPI entry point
├── shared/                    # Cross-cutting concerns (no core/)
│   ├── config.py              # Pydantic BaseSettings
│   ├── logging.py             # Structlog configuration
│   └── middleware.py          # Request correlation, errors
├── agent/                     # Pydantic AI orchestrator
│   ├── agent.py               # Main agent instance
│   ├── dependencies.py        # AgentDependencies
│   └── prompts.py             # System prompts
├── tools/                     # 3 consolidated tools
│   ├── youtube_video_planner/
│   ├── youtube_scene_producer/
│   └── youtube_production_manager/
└── api/                       # Hybrid API endpoints
    ├── openai/                # OpenAI-compatible
    └── workflows/             # Direct tool access
```

**Key Decision**: Eliminated `core/` directory - simpler structure with `shared/` only.

---

## Core Patterns & Principles

### Tool Consolidation (Anthropic Best Practices)

**Problem**: Granular tools (10+) require complex orchestration and high token usage.

**Solution**: 3 consolidated tools, each handling a complete workflow phase:

1. **youtube_video_planner** - Planning phase
   - Operations: `analyze` (idea → format recommendation) | `structure` (format → scene breakdown)
   - Consolidates: idea analysis + copyright check + scene structure generation

2. **youtube_scene_producer** - Production phase
   - Operations: `generate` (all prompts) | `refine` (failed scenes)
   - Consolidates: image + animation + dialogue + voice + timing + music prompts

3. **youtube_production_manager** - Finalization phase
   - Operations: `feedback` | `timeline` | `metadata` | `quality_check`
   - Consolidates: feedback processing + assembly + YouTube metadata + QA

**Benefits**:
- ~60% reduction in tool call overhead (5-7 calls vs 15+ calls)
- ~50% token savings (concise vs detailed response formats)
- Simpler agent orchestration
- Clear workflow boundaries

### Token Efficiency Strategy

All tools support 3 response formats:

| Format | Tokens/Scene | Use Case |
|--------|--------------|----------|
| `minimal` | ~100 | Quick checks, automation |
| `concise` | ~300 | **Default** - balanced for manual workflow |
| `detailed` | ~800 | Complex scenarios, debugging |

**Example**: Full 8-scene drama workflow
- Concise: ~5,000 tokens total
- Detailed: ~10,000 tokens total
- **Savings: 50% by defaulting to concise**

### Error Handling Philosophy

**Principle**: Helpful errors > opaque tracebacks (Anthropic guidance)

**Good Error**:
```markdown
## ❌ Error: Missing Scene Structure

**Problem**: The `scene_structure` parameter is empty.
**Expected Format**: 8 scenes: Kavi shows off → Friends ignore → ...
**How to Fix**:
1. Call youtube_video_planner(operation="structure") first
2. Pass result to youtube_scene_producer

**Example**: [correct usage code]
```

**Bad Error**: `ValueError: validation failed` with traceback

---

## Tools & Features

### Tool 1: youtube_video_planner

**Purpose**: Analyze ideas, recommend format, check copyright, generate scene structure.

**Key Features**:
- Analyzes idea for song vs drama format (with pros/cons)
- Checks copyright status (public domain, conflicts)
- Supports new characters OR existing characters (series continuity)
- Generates 6-8 scene structure for drama, 3-5 for song
- Character emotional arc (start → change → end)

**Parameters**:
- `idea`: Story concept (Tamil/English)
- `operation`: "analyze" or "structure"
- `character_choice`: "new" or "existing" ← **Key for series**
- `existing_character_name`: e.g., "Kavi the Peacock"
- `reference_image`: Path to character reference
- `language`: "tamil", "english", or "both"
- `response_format`: "minimal", "concise", "detailed"

**Output Examples**:
- Analyze: Drama recommended, copyright CLEAR, reasoning (~300 tokens)
- Structure: 8 scenes with emotional arc (~500 tokens)

---

### Tool 2: youtube_scene_producer

**Purpose**: Generate complete production-ready prompts for all scenes.

**Key Features**:
- Generates ALL scene elements in one call (not per-scene)
- **Automated music prompt generation** (Suno) ← **New feature**
- Character Reference integration (Leonardo.ai HIGH strength)
- Refines failed scenes based on user feedback
- Supports Tamil, English, or bilingual dialogue

**What Each Scene Package Includes**:
1. Image Generation Prompt (Leonardo.ai, 3D Pixar style)
2. Animation Prompt (MiniMax Hailuo, camera + character actions)
3. Dialogue (Tamil + English translation)
4. Voice Direction (Azure TTS voice IDs, emotion tags)
5. Timing & Duration (10-30 seconds per scene)
6. Transition to Next Scene (dissolve, cut, fade)
7. Audio Sync Notes (when dialogue/music plays)
8. **Music Prompt (Suno)** - Background music or full song

**Parameters**:
- `scene_structure`: From youtube_video_planner
- `operation`: "generate" or "refine"
- `scene_numbers`: Which scenes (None = all)
- `feedback`: User feedback for refinement
- `reference_image`: Character reference path
- `language`: "tamil", "english", "both"
- `response_format`: "minimal", "concise", "detailed"

**Output Examples**:
- Generate all (8 scenes): ~3,200 tokens (concise)
- Refine 2 scenes: ~800 tokens

---

### Tool 3: youtube_production_manager

**Purpose**: Handle post-production (feedback, timeline, metadata, QA).

**Key Features**:
- Processes user feedback, identifies failed scenes
- Generates FFmpeg/Shotstack assembly timeline
- Creates SEO-optimized YouTube metadata (Tamil + English)
- Generates quality checklist (visual, audio, content, technical)
- **"Made for Kids" is OPTIONAL** (general audience flexibility)

**Parameters**:
- `operation`: "feedback", "timeline", "metadata", "quality_check"
- `all_scenes`: Scene packages from youtube_scene_producer
- `user_feedback`: Production results
- `video_duration`: Total seconds (for timeline)
- `character_name`: For metadata
- `moral_theme`: For metadata
- `response_format`: "minimal", "concise", "detailed"

**Output Examples**:
- Feedback: Analysis of failures (~300 tokens)
- Timeline: FFmpeg commands with timing (~400 tokens)
- Metadata: YouTube title, description, tags (~200 tokens)
- Quality check: QA checklist (~600 tokens)

---

## Workflow Integration

### Complete 14-Step Production Flow

```
USER INPUT
    ↓
[1] User provides idea (e.g., "உடையது விளம்பேல்")
    ↓
[2] youtube_video_planner(operation="analyze")
    → Returns: Drama recommended, copyright CLEAR
    ↓
[3] User confirms: "Go with drama"
    ↓
[4] youtube_video_planner(operation="structure")
    → Returns: 8-scene breakdown with emotional arc
    ↓
[5] User approves structure
    ↓
[6] youtube_scene_producer(operation="generate")
    → Returns: Suno music prompt + 8 complete scene packages
    ↓
MANUAL PRODUCTION (User pastes prompts)
    ↓
[7] User generates assets:
    - Suno (background music, 4:30)
    - Leonardo.ai (8 images with character reference)
    - MiniMax Hailuo (8 animated videos)
    - Azure TTS (8 voice audio files)
    ↓
[8] User reports results:
    "Scenes 1-6 ✅, Scenes 7-8 ❌ (character inconsistent)"
    ↓
[9] youtube_production_manager(operation="feedback")
    → Returns: Analysis identifying scenes 7-8 need refinement
    ↓
[10] youtube_scene_producer(operation="refine", scene_numbers=[7,8])
    → Returns: Refined prompts for scenes 7-8
    ↓
[11] User regenerates scenes 7-8: "All done ✅"
    ↓
[12] youtube_production_manager(operation="timeline")
    → Returns: FFmpeg assembly instructions
    ↓
[13] User assembles video (FFmpeg/Shotstack)
    ↓
[14] youtube_production_manager(operation="metadata")
    → Returns: YouTube title, description, tags, thumbnail
    ↓
[15] youtube_production_manager(operation="quality_check")
    → Returns: QA checklist
    ↓
[16] User uploads to YouTube
    ↓
PUBLISHED VIDEO ✅
```

**Total Tool Calls**: 5-7 (vs 15+ with granular tools)
**Total Time**: <2 hours (vs 3+ hours manual)

---

## Non-Functional Requirements

### Performance

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Tool Response Time** | 3-10 seconds | LLM generation time (Claude Sonnet 4.5) |
| **Full Workflow Time** | 30-60 seconds | All 5-7 tool calls combined |
| **API Latency (p95)** | <2 seconds | FastAPI overhead minimal |
| **Token Usage/Video** | <10,000 tokens | Cost control (~$0.03/video at Claude pricing) |

**Recommendation**: Each tool call should respond in 3-10 seconds. Full workflow from idea to prompts: 30-60 seconds.

### Availability & Reliability

| Metric | Target | Notes |
|--------|--------|-------|
| **Uptime** | 99% during working hours (8am-10pm local) | Best effort outside hours |
| **Error Rate** | <5% | Tool failures, not user errors |
| **Data Loss** | Zero tolerance | Stateless MVP - no data to lose |

**Recommendation**: 99% uptime during working hours sufficient for single-user MVP.

### Scalability

| Phase | Users | Architecture | Notes |
|-------|-------|--------------|-------|
| **MVP** | 1 (single user) | Stateless, local/cloud | No database, simple deployment |
| **Phase 2** | 10-50 | Add PostgreSQL | Character library, analytics |
| **Phase 3** | 50-100 | Horizontal scaling | Load balancer, multiple instances |
| **Phase 4** | 100-1000 | Microservices | Separate services per tool |

**Recommendation**: Start single-user, architect for 10-100 concurrent users in future.

### Cost Targets

**MVP (Monthly)**:
- FastAPI hosting (Railway/Render): $15-25
- Claude Sonnet 4.5 API: $20-50 (based on 20-40 videos/month)
- Domain + SSL: $5-10
- **Total**: $40-85/month

**Post-MVP (with database, analytics)**:
- Hosting: $50-100
- Database (PostgreSQL): $25-50
- LLM API: $100-200 (more users)
- **Total**: $175-350/month

**Recommendation**: Target $50-200/month for MVP, scale cost with users in Phase 2+.

---

## Character Library (Future - Phase 2)

### Problem Statement
Currently, character references are managed manually (files on disk). As series grow (10+ Kavi episodes), need systematic way to:
- Browse available characters
- Select character for new video
- Upload new character references
- Track character usage across videos

### Proposed Solution (Phase 2)

**Character Library UI**:
```
┌─────────────────────────────────────┐
│  Character Library                  │
├─────────────────────────────────────┤
│                                     │
│  [Kavi Peacock]  [Mira Rabbit]     │
│   🦚 12 videos   🐰 3 videos        │
│                                     │
│  [+ Add New Character]              │
│                                     │
└─────────────────────────────────────┘
```

**Features**:
- View all characters with preview images
- Filter by: series, usage count, creation date
- Select character for video (auto-fills `existing_character_name` + `reference_image`)
- Upload new character with metadata (name, description, tags)
- Track: videos using character, creation date, tags

**Database Schema**:
```sql
CREATE TABLE characters (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  reference_image_url TEXT NOT NULL,
  tags TEXT[],
  created_at TIMESTAMP,
  video_count INTEGER DEFAULT 0
);

CREATE TABLE videos (
  id UUID PRIMARY KEY,
  title VARCHAR(500),
  character_id UUID REFERENCES characters(id),
  created_at TIMESTAMP,
  status VARCHAR(50)  -- draft, in_progress, published
);
```

---

## Series Planning Tools (Future - Phase 2)

### Problem Statement
Creating 10-20 episodes of Kavi requires:
- Brainstorming episode ideas
- Ensuring variety (different morals, settings, characters)
- Tracking which ideas are completed
- Maintaining story continuity

### Proposed Solution (Phase 2)

**Series Planner UI**:
```
┌─────────────────────────────────────┐
│  Kavi the Peacock Series            │
├─────────────────────────────────────┤
│                                     │
│  Episode 1: Don't Be a Blowhard ✅  │
│  Episode 2: Sharing is Caring  🟡   │
│  Episode 3: Honesty Pays      ⬜    │
│  ...                                │
│                                     │
│  [+ Add Episode Idea]               │
│  [🤖 Generate 10 Episode Ideas]     │
│                                     │
└─────────────────────────────────────┘
```

**Features**:
- Create series (name, character, target episode count)
- Add episode ideas manually or generate with AI
- Track status: planned → in_progress → completed → published
- Ensure variety: AI suggests diverse morals/themes
- Continuity notes: character development across episodes

**AI-Generated Episode Ideas**:
```python
POST /api/series/brainstorm
{
  "character_name": "Kavi the Peacock",
  "episode_count": 10,
  "themes": ["humility", "sharing", "honesty", "friendship"],
  "existing_episodes": ["Don't Be a Blowhard"]
}

# Returns: 10 unique episode ideas with variety
```

---

## Analytics Dashboard (Future - Phase 2)

### Problem Statement
No visibility into:
- Production efficiency (time per video, success rates)
- Character usage patterns
- Series progress
- YouTube performance

### Proposed Solution (Phase 2)

**Analytics Dashboard**:
```
┌─────────────────────────────────────┐
│  Nithya-Creator Analytics           │
├─────────────────────────────────────┤
│                                     │
│  📊 Production Stats                │
│  ├─ Videos Created: 24              │
│  ├─ Avg Time/Video: 1.8 hours       │
│  ├─ Scene Success Rate: 92%         │
│  └─ Characters Used: 3              │
│                                     │
│  📈 Series Progress                 │
│  ├─ Kavi Series: 12/20 episodes     │
│  └─ Mira Series: 3/10 episodes      │
│                                     │
│  🎯 Most Used Characters            │
│  ├─ Kavi: 12 videos                 │
│  └─ Mira: 3 videos                  │
│                                     │
└─────────────────────────────────────┘
```

**Metrics Tracked**:
- Videos created (total, per week, per character)
- Production time (average, trend over time)
- Scene success rate (first-try success, refinement needed)
- Character usage (most popular, underutilized)
- Series completion rate
- YouTube performance (views, engagement) - if integrated

---

## Risks & Mitigation

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **LLM API outage** | High - blocks all workflows | Low | Implement retry logic, timeout handling, clear error messages |
| **Token cost spike** | Medium - budget overrun | Medium | Monitor token usage, implement caps, default to "concise" format |
| **Character inconsistency** | High - video quality | Medium | Enforce Character Reference HIGH strength, validate in feedback step |
| **Manual tool failures** | Medium - workflow blocked | Medium | Provide refinement loop, clear error guidance |

### Product Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Doesn't save time** | Critical - no value | Low | Test with real workflow, measure metrics |
| **Prompts too generic** | High - quality issues | Medium | Iterate on prompt templates, add examples, user feedback |
| **Learning curve** | Medium - adoption | Low | Clear documentation, test execution plan, examples |
| **Scalability issues** | Medium - future growth | Low | Design for 10-100 users from start |

### Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **No other creators adopt** | Medium - limits growth | Medium | Focus on MVP value first, iterate based on KIDZ SEASON TV feedback |
| **API pricing changes** | Medium - cost increase | Low | Monitor pricing, have fallback options (GPT-4, local models) |
| **Copyright issues** | High - legal liability | Low | Automated copyright check, user confirms clearance |

---

## Timeline & Milestones

### Phase 1: MVP Implementation (2-3 weeks)

**Week 1-2: Core Tools**
- [ ] Implement youtube_video_planner (tool, schemas, service, tests)
- [ ] Implement youtube_scene_producer (tool, schemas, service, tests)
- [ ] Implement youtube_production_manager (tool, schemas, service, tests)
- [ ] Write unit tests (80%+ coverage)
- [ ] Validate token usage matches specifications

**Week 2-3: Agent & API**
- [ ] Create AgentDependencies structure
- [ ] Configure Pydantic AI agent with tools
- [ ] Implement OpenAI-compatible endpoint (`/v1/chat/completions`)
- [ ] Implement direct workflow endpoints (`/api/workflows/video/*`)
- [ ] Add logging, error handling, validation

**Week 3: Testing & Deployment**
- [ ] Test with real "உடையது விளம்பேல்" workflow
- [ ] Create evaluation tasks
- [ ] Deploy to Railway/Render
- [ ] Document API with examples
- [ ] User acceptance testing

**Success Criteria**: Full workflow from idea → prompts → assembly → YouTube works end-to-end in <2 hours.

---

### Phase 2: Character Library & Analytics (3-6 months post-MVP)

**Month 1-2: Character Library**
- [ ] Add PostgreSQL database
- [ ] Create character library schema
- [ ] Build character upload/browse UI
- [ ] Integrate with workflow (auto-select character)
- [ ] Track character usage

**Month 2-3: Analytics Dashboard**
- [ ] Track production metrics (time, success rate)
- [ ] Build dashboard UI
- [ ] Add series tracking
- [ ] YouTube performance integration (if API available)

**Month 3-4: Series Planning**
- [ ] Build series planner UI
- [ ] AI episode idea generation
- [ ] Continuity tracking
- [ ] Status management (planned → published)

**Success Criteria**: Character library has 5+ characters, analytics shows production improvements, 1 complete series (10+ episodes).

---

### Phase 3: Multi-User & Collaboration (6-12 months post-MVP)

**Month 6-9: Multi-User Foundation**
- [ ] User authentication (Auth0/Clerk)
- [ ] Multi-tenancy (isolated data)
- [ ] Billing integration (if commercial)
- [ ] Usage limits and quotas

**Month 9-12: Collaboration Features**
- [ ] Team management (roles: creator, editor, reviewer)
- [ ] Shared character libraries
- [ ] Template library
- [ ] Comments and approvals workflow

**Success Criteria**: 10-50 active creators, team collaboration working, revenue positive (if commercial).

---

### Phase 4: API Integrations & Automation (12-24 months post-MVP)

**Month 12-18: Direct API Integrations**
- [ ] Leonardo.ai API integration (skip manual paste)
- [ ] MiniMax Hailuo API integration
- [ ] Automated video assembly (end-to-end)
- [ ] Batch processing (10 videos at once)

**Month 18-24: Advanced Analytics**
- [ ] YouTube Analytics API integration
- [ ] A/B testing (titles, thumbnails)
- [ ] Performance predictions
- [ ] Recommendations engine

**Success Criteria**: Fully automated workflow (idea → published video in 2 hours with zero manual steps), 100+ active creators.

---

## Open Questions

### For User Confirmation
1. **Deployment Preference**: Railway, Render, AWS, or local hosting?
2. **Domain Name**: Custom domain for Nithya-Creator or use default?
3. **Multi-Language Priority**: Besides Tamil/English, which languages next? (Hindi, Telugu, Kannada?)
4. **Character Library Timeline**: Need in Phase 2 (3-6 months) or can wait longer?

### For Future Exploration
1. **Monetization**: Free for KIDZ SEASON TV, paid for other creators? Subscription model?
2. **Template Library**: Reusable story patterns (hero's journey, moral lesson template)?
3. **Voice Cloning**: Use user's own voice instead of Azure TTS?
4. **Mobile App**: Native iOS/Android apps or web-only?

---

## Appendix

### Related Documentation

- **MVP Tool Designs**: `/mvp-tool-designs.md`
- **Tool Architecture**: `/docs/tool-architecture-design.md`
- **Planning Document**: `/docs/planning-complete-ready-for-testing.md`
- **Alignment Review**: `/docs/alignment-review-from-start.md`
- **Workflow Documentation**: `/.claude/workflows/youtube-video-creation-workflow.md`
- **Production Example**: `/examples/kavi-peacock-complete-video-production.md`

### Glossary

- **Character Reference**: Master image used by Leonardo.ai to maintain visual consistency across scenes
- **Scene Package**: Complete set of prompts for one scene (image, animation, dialogue, voice, timing)
- **Vertical Slice Architecture (VSA)**: Feature-based organization (vs layered architecture)
- **Token**: Unit of text processed by LLM (roughly 0.75 words)
- **Anthropic Principles**: Best practices for writing agent tools (consolidation, token efficiency, helpful errors)
- **Stateless**: No database/session storage - each request is independent

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-27 | KIDZ SEASON TV | Initial PRD based on planning phase completion |

---

**Status**: ✅ Planning Complete - Ready for Phase 1 Implementation
**Next Action**: Begin Week 1 implementation (Core Tools)
