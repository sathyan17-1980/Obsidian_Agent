# MVP Tool Designs - YouTube Video Production Agent

**Status**: ✅ FINALIZED - Ready for Implementation
**Date**: 2025-01-27
**Architecture**: 3 Consolidated Tools following Anthropic Principles

---

## Overview

This document contains the **finalized MVP tool designs** for the YouTube video production AI agent. All user decisions have been confirmed, and this represents the exact specification for implementation.

**No alternative options are included** - this is the single, approved design path.

---

## Architecture Summary

### Tech Stack (Confirmed)
- **Framework**: Pydantic AI + FastAPI
- **Package Manager**: UV
- **Type Safety**: Ruff + mypy (strict mode)
- **Logging**: Structlog (AI-optimized)
- **Architecture**: Vertical Slice Architecture (VSA)
- **API Strategy**: Hybrid (OpenAI-compatible + Direct workflow endpoints)

### Directory Structure (Finalized)

```
app/
├── main.py                             # FastAPI app entry point
├── pyproject.toml                      # UV dependencies
│
├── shared/                             # Cross-cutting concerns (NO core/ directory)
│   ├── __init__.py
│   ├── config.py                       # Pydantic BaseSettings
│   ├── logging.py                      # Structlog configuration
│   └── middleware.py                   # Request correlation, error handling
│
├── agent/                              # Pydantic AI orchestrator
│   ├── __init__.py
│   ├── agent.py                        # Main agent instance
│   ├── dependencies.py                 # AgentDependencies (RunContext)
│   └── prompts.py                      # System prompts
│
├── tools/                              # 3 consolidated tools (vertical slices)
│   ├── __init__.py
│   ├── youtube_video_planner/
│   │   ├── __init__.py
│   │   ├── tool.py                     # @agent.tool decorator
│   │   ├── schemas.py                  # Pydantic models (input/output)
│   │   └── service.py                  # Business logic
│   ├── youtube_scene_producer/
│   │   ├── __init__.py
│   │   ├── tool.py
│   │   ├── schemas.py
│   │   └── service.py
│   └── youtube_production_manager/
│       ├── __init__.py
│       ├── tool.py
│       ├── schemas.py
│       └── service.py
│
├── api/                                # FastAPI routes (Hybrid approach)
│   ├── __init__.py
│   ├── openai/                         # OpenAI-compatible endpoints
│   │   ├── __init__.py
│   │   └── routes.py                   # POST /v1/chat/completions
│   └── workflows/                      # Direct workflow endpoints
│       ├── __init__.py
│       └── routes.py                   # POST /api/workflows/video/plan
│                                       # POST /api/workflows/video/produce
│                                       # POST /api/workflows/video/manage
│
└── tests/
    ├── __init__.py
    ├── shared/
    │   └── test_logging.py
    ├── agent/
    │   └── test_agent.py
    ├── tools/
    │   ├── test_youtube_video_planner.py
    │   ├── test_youtube_scene_producer.py
    │   └── test_youtube_production_manager.py
    └── integration/
        └── test_video_workflow.py
```

**Key Decision**: `core/` directory **eliminated** - use `shared/` only for simplicity.

---

## Tool 1: youtube_video_planner

**Purpose**: Analyze video ideas, check copyright, recommend format (song/drama), and generate scene structure.

### Function Signature

```python
@agent.tool
async def youtube_video_planner(
    ctx: RunContext[AgentDependencies],
    idea: str,
    operation: Literal["analyze", "structure"],
    format_choice: Optional[Literal["song", "drama"]] = None,
    character_choice: Literal["new", "existing"] = "new",
    existing_character_name: Optional[str] = None,
    reference_image: Optional[str] = None,
    language: Literal["tamil", "english", "both"] = "tamil",
    response_format: Literal["minimal", "concise", "detailed"] = "concise"
) -> str:
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `idea` | `str` | ✅ Yes | - | Story concept, moral, or theme (Tamil or English) |
| `operation` | `Literal` | ✅ Yes | - | "analyze" (initial analysis) or "structure" (generate scene breakdown) |
| `format_choice` | `Optional[Literal]` | Conditional | `None` | Required for "structure" operation: "song" or "drama" |
| `character_choice` | `Literal` | No | `"new"` | "new" (create fresh character) or "existing" (use recurring character like Kavi) |
| `existing_character_name` | `Optional[str]` | Conditional | `None` | Required if character_choice="existing" (e.g., "Kavi the Peacock") |
| `reference_image` | `Optional[str]` | No | `None` | Path to character reference (e.g., "characters/kavi-peacock.png") |
| `language` | `Literal` | No | `"tamil"` | Primary language(s): "tamil", "english", or "both" |
| `response_format` | `Literal` | No | `"concise"` | Token efficiency: "minimal" (~100 tokens), "concise" (~300 tokens), "detailed" (~800 tokens) |

### Operations

#### Operation: "analyze"

**What it does**: Analyzes idea and recommends format (song vs drama) with copyright check.

**Returns**:
- Format recommendation (song OR drama) with reasoning
- Copyright status (CLEAR or POTENTIAL ISSUES with details)
- Pros/cons for each format
- Audience appropriateness (general audience, family-friendly)
- Cultural authenticity notes (for Tamil content)

**Token Usage**:
- Minimal: ~100 tokens (recommendation only)
- Concise: ~300 tokens (recommendation + reasoning + copyright)
- Detailed: ~800 tokens (full analysis with alternatives)

**Example**:
```python
result = youtube_video_planner(
    idea="உடையது விளம்பேல் - Don't be a blowhard",
    operation="analyze",
    character_choice="new",
    language="tamil",
    response_format="concise"
)
# Returns: Drama recommended, copyright CLEAR, pros/cons
```

#### Operation: "structure"

**What it does**: Generates complete scene breakdown after user confirms format.

**Returns**:
- Scene count and descriptions (6-8 for drama, 3-5 for song)
- Character emotional arc (start → change → end)
- Key moments and transitions
- Duration per scene (targeting 2-5 minute total)
- Continuity notes (visual, narrative, audio)
- Character design (if character_choice="new")

**Token Usage**:
- Minimal: ~200 tokens (scene list only)
- Concise: ~500 tokens (scene breakdown with arcs)
- Detailed: ~1200 tokens (comprehensive with continuity notes)

**Example (New Character)**:
```python
structure = youtube_video_planner(
    idea="உடையது விளம்பேல்",
    operation="structure",
    format_choice="drama",
    character_choice="new",  # Creates new character
    language="tamil",
    response_format="concise"
)
# Returns: 8-scene breakdown with new character design
```

**Example (Existing Character - Kavi Episode 2)**:
```python
structure = youtube_video_planner(
    idea="Kavi learns to share",
    operation="structure",
    format_choice="drama",
    character_choice="existing",
    existing_character_name="Kavi the Peacock",
    reference_image="characters/kavi-peacock.png",
    language="tamil",
    response_format="concise"
)
# Returns: 8-scene breakdown maintaining Kavi consistency
```

---

## Tool 2: youtube_scene_producer

**Purpose**: Generate complete production-ready prompts for all scene elements (image, animation, dialogue, voice, music).

### Function Signature

```python
@agent.tool
async def youtube_scene_producer(
    ctx: RunContext[AgentDependencies],
    scene_structure: str,
    operation: Literal["generate", "refine"] = "generate",
    scene_numbers: Optional[list[int]] = None,
    feedback: Optional[str] = None,
    reference_image: Optional[str] = None,
    language: Literal["tamil", "english", "both"] = "tamil",
    response_format: Literal["minimal", "concise", "detailed"] = "concise"
) -> str:
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `scene_structure` | `str` | ✅ Yes | - | Complete scene breakdown from youtube_video_planner |
| `operation` | `Literal` | No | `"generate"` | "generate" (create initial prompts) or "refine" (improve based on feedback) |
| `scene_numbers` | `Optional[list[int]]` | No | `None` | Which scenes to generate (1-indexed). None = all scenes |
| `feedback` | `Optional[str]` | Conditional | `None` | Required for "refine" operation. User feedback from production results |
| `reference_image` | `Optional[str]` | No | `None` | Path to character reference for visual consistency |
| `language` | `Literal` | No | `"tamil"` | Language(s) for dialogue: "tamil", "english", or "both" |
| `response_format` | `Literal` | No | `"concise"` | Token efficiency: "minimal" (~200/scene), "concise" (~400/scene), "detailed" (~800/scene) |

### Operations

#### Operation: "generate"

**What it does**: Generates complete scene packages for all (or specified) scenes.

**Returns** (for each scene):
1. **Image Generation Prompt** (Leonardo.ai ready)
   - 3D Pixar style, character details, setting, lighting, camera angle
   - Character Reference instructions (if reference_image provided)
2. **Animation Prompt** (MiniMax Hailuo ready)
   - Camera movement (pan, zoom, dolly, static)
   - Character actions and movements
   - Duration (10-30 seconds per scene)
3. **Dialogue** (Tamil and/or English)
   - Age-appropriate vocabulary (general audience, family-friendly)
   - Natural, conversational tone
   - 1-2 sentences per scene max
4. **Voice Direction** (ElevenLabs/Azure TTS)
   - Voice type (child, energetic, calm, elderly)
   - Emotion tags ([excited], [whispers], [dramatic])
   - Pacing (fast, normal, slow)
   - Specific Azure TTS voice IDs (e.g., ta-IN-ValluvarNeural)
5. **Timing & Duration**: How long scene should be
6. **Transition to Next Scene**: Cut, fade, dissolve, wipe (with duration)
7. **Audio Sync Notes**: When dialogue starts, background music cues
8. **Music Prompt (Suno)** - AUTOMATED ✅
   - For drama: Background music prompt (instrumental, full video duration)
   - For song: Full song prompt with lyrics
   - Generated automatically at the top of output

**Token Usage**:
- Minimal: ~200 tokens per scene (prompts only, no explanation)
- Concise: ~400 tokens per scene (prompts + brief notes) - **DEFAULT**
- Detailed: ~800 tokens per scene (prompts + detailed direction + alternatives)

**Total for 8-scene drama**:
- Minimal: ~1,600 tokens
- Concise: ~3,200 tokens
- Detailed: ~6,400 tokens

**Example (Generate All Scenes)**:
```python
scenes = youtube_scene_producer(
    scene_structure="[8-scene breakdown from planner]",
    operation="generate",
    reference_image="characters/kavi-peacock.png",
    language="tamil",
    response_format="concise"
)
# Returns: Suno music prompt + 8 complete scene packages (~3,200 tokens)
```

#### Operation: "refine"

**What it does**: Refines specific scenes based on user feedback from actual production.

**Returns**: Updated prompts for specified scenes only.

**Example (Refine Failed Scenes)**:
```python
refined = youtube_scene_producer(
    scene_structure="[8-scene breakdown]",
    operation="refine",
    scene_numbers=[7, 8],
    feedback="Scene 7 character looks different (wrong colors), Scene 8 animation too fast",
    reference_image="characters/kavi-peacock.png",
    language="tamil",
    response_format="concise"
)
# Returns: Refined prompts for scenes 7 and 8 only (~800 tokens)
```

---

## Tool 3: youtube_production_manager

**Purpose**: Handle post-production operations (feedback processing, timeline assembly, YouTube metadata, quality checks).

### Function Signature

```python
@agent.tool
async def youtube_production_manager(
    ctx: RunContext[AgentDependencies],
    operation: Literal["feedback", "timeline", "metadata", "quality_check"],
    all_scenes: str,
    user_feedback: Optional[str] = None,
    video_duration: Optional[int] = None,
    character_name: Optional[str] = None,
    moral_theme: Optional[str] = None,
    response_format: Literal["minimal", "concise", "detailed"] = "concise"
) -> str:
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `operation` | `Literal` | ✅ Yes | - | "feedback", "timeline", "metadata", or "quality_check" |
| `all_scenes` | `str` | ✅ Yes | - | Complete scene packages from youtube_scene_producer |
| `user_feedback` | `Optional[str]` | Conditional | `None` | Required for "feedback" operation. User's production results |
| `video_duration` | `Optional[int]` | Conditional | `None` | Required for "timeline" operation. Total duration in seconds |
| `character_name` | `Optional[str]` | Conditional | `None` | Required for "metadata" operation. Main character name |
| `moral_theme` | `Optional[str]` | Conditional | `None` | Required for "metadata" operation. Story moral or theme |
| `response_format` | `Literal` | No | `"concise"` | Token efficiency: "minimal" (~100), "concise" (~300), "detailed" (~600) |

### Operations

#### Operation: "feedback"

**What it does**: Analyzes user feedback, identifies failed scenes, recommends next steps.

**Returns**:
- Analysis of what succeeded vs failed
- Specific scenes that need refinement
- Recommended next steps (refine prompts vs retry vs adjust)
- Which tool to use (youtube_scene_producer with operation="refine")

**Token Usage**: ~100-600 tokens depending on response_format

**Example**:
```python
analysis = youtube_production_manager(
    operation="feedback",
    all_scenes="[All 8 scene packages]",
    user_feedback="Scenes 1-6 worked great. Scene 7 and 8 failed - character inconsistent.",
    response_format="concise"
)
# Returns: Analysis identifying scenes 7-8 need refinement (~300 tokens)
```

#### Operation: "timeline"

**What it does**: Generates video assembly instructions with scene timing.

**Returns**:
- FFmpeg or Shotstack assembly instructions
- Scene-by-scene timing (start time, duration, end time)
- Transition effects and durations
- Audio layer timing (dialogue, music, effects, ambience)
- Final output specifications (resolution, frame rate, format)

**Token Usage**: ~200-800 tokens depending on response_format

**Example**:
```python
timeline = youtube_production_manager(
    operation="timeline",
    all_scenes="[All 8 scene packages]",
    video_duration=270,  # 4:30 in seconds
    response_format="concise"
)
# Returns: Complete assembly instructions with FFmpeg commands (~400 tokens)
```

#### Operation: "metadata"

**What it does**: Generates YouTube upload metadata (title, description, tags, thumbnail).

**Returns**:
- YouTube Title (Tamil + English, SEO-optimized)
- Description (story summary, moral lesson, age range)
- Tags (15-20 relevant tags)
- Category (Education)
- Thumbnail notes (which scene to use, text overlay suggestions)
- **"Made for Kids" designation: OPTIONAL** ✅ (user choice for general audience reach)

**Token Usage**: ~100-400 tokens depending on response_format

**Example**:
```python
metadata = youtube_production_manager(
    operation="metadata",
    all_scenes="[All 8 scene packages]",
    character_name="Kavi the Peacock",
    moral_theme="Don't be a blowhard",
    response_format="concise"
)
# Returns: Complete YouTube metadata (~200 tokens)
```

#### Operation: "quality_check"

**What it does**: Generates review checklist for final QA before upload.

**Returns**:
- Visual checklist (character consistency, colors, glitches)
- Audio checklist (dialogue clarity, music balance, no clipping)
- Content checklist (moral clear, age-appropriate, story flow)
- Technical checklist (aspect ratio, duration, file size)

**Token Usage**: ~200-600 tokens depending on response_format

**Example**:
```python
checklist = youtube_production_manager(
    operation="quality_check",
    all_scenes="[All 8 scene packages]",
    response_format="detailed"
)
# Returns: Comprehensive QA checklist (~600 tokens)
```

---

## Workflow Integration

### Complete Video Production Flow

```
STEP 1: User provides idea
    ↓
STEP 2: youtube_video_planner(operation="analyze")
    ↓ Returns: Format recommendation + copyright status
    ↓
STEP 3: User decides format (song/drama)
    ↓
STEP 4: youtube_video_planner(operation="structure")
    ↓ Returns: Scene breakdown
    ↓
STEP 5: youtube_scene_producer(operation="generate")
    ↓ Returns: All scene prompts + Suno music prompt
    ↓
STEP 6: User pastes prompts to tools (Leonardo.ai, MiniMax, Azure TTS, Suno)
    ↓
STEP 7: User reports results
    ↓
STEP 8: youtube_production_manager(operation="feedback")
    ↓ Returns: Analysis of failures
    ↓
STEP 9 (if needed): youtube_scene_producer(operation="refine")
    ↓ Returns: Refined prompts for failed scenes
    ↓
STEP 10: youtube_production_manager(operation="timeline")
    ↓ Returns: Assembly instructions
    ↓
STEP 11: User assembles video
    ↓
STEP 12: youtube_production_manager(operation="metadata")
    ↓ Returns: YouTube metadata
    ↓
STEP 13: youtube_production_manager(operation="quality_check")
    ↓ Returns: QA checklist
    ↓
STEP 14: User uploads to YouTube
```

**Total Tool Calls**: 5-7 (vs 15+ with granular tools)
**Token Overhead**: ~1,400 tokens (vs ~3,000 with granular tools)
**Savings**: ~53% overhead reduction + 50% token savings from response_format optimization

---

## API Endpoints (Hybrid Approach)

### OpenAI-Compatible Endpoint

**Conversational workflow** - Agent orchestrates tool calls automatically.

```python
POST /v1/chat/completions
Content-Type: application/json

{
  "model": "claude-sonnet-4.5",
  "messages": [
    {"role": "user", "content": "Analyze this idea: உடையது விளம்பேல் - Don't be a blowhard"}
  ]
}

# Agent automatically calls youtube_video_planner(operation="analyze")
# Returns conversational response with analysis
```

### Direct Workflow Endpoints

**Programmatic access** - Direct tool calls without conversation.

#### Plan Endpoint

```python
POST /api/workflows/video/plan
Content-Type: application/json

{
  "idea": "உடையது விளம்பேல் - Don't be a blowhard",
  "operation": "analyze",
  "language": "tamil",
  "response_format": "concise"
}

# Directly calls youtube_video_planner
# Returns JSON with analysis
```

#### Produce Endpoint

```python
POST /api/workflows/video/produce
Content-Type: application/json

{
  "scene_structure": "[8-scene breakdown]",
  "operation": "generate",
  "reference_image": "characters/kavi-peacock.png",
  "language": "tamil",
  "response_format": "concise"
}

# Directly calls youtube_scene_producer
# Returns JSON with all scene prompts
```

#### Manage Endpoint

```python
POST /api/workflows/video/manage
Content-Type: application/json

{
  "operation": "timeline",
  "all_scenes": "[All scene packages]",
  "video_duration": 270,
  "response_format": "concise"
}

# Directly calls youtube_production_manager
# Returns JSON with assembly instructions
```

---

## Key Design Decisions (Finalized)

### 1. Audience
- **General audience (family-friendly)** - not locked to "kids only"
- YouTube "Made for Kids" designation is **OPTIONAL** (user choice)

### 2. Architecture
- `core/` directory **eliminated** - use `shared/` only
- Simpler VSA structure for easier maintenance

### 3. Character Management
- Support for **both new and existing characters**
- `character_choice` parameter: "new" | "existing"
- Enables series continuity (Kavi episodes) AND standalone videos

### 4. Music Prompts
- **Automated** - tool generates Suno prompts automatically
- For drama: Background music (instrumental)
- For song: Full song with lyrics
- Included in youtube_scene_producer output

### 5. API Strategy
- **Hybrid approach** - both OpenAI-compatible AND direct endpoints
- Conversational workflow for natural language interaction
- Programmatic access for automation/scripting

### 6. Feedback Storage
- **Stateless for MVP** - no database required
- User provides feedback each time
- Can migrate to PostgreSQL later for analytics

### 7. Manual Production
- User manually pastes prompts to:
  - Leonardo.ai (images with Character Reference)
  - MiniMax Hailuo (image-to-video animation)
  - Azure TTS / ElevenLabs (voice)
  - Suno (music)
- Feedback loop for refinement

---

## Token Efficiency

### Response Format Strategy

All tools support 3 response formats:

| Format | Tokens | Use Case |
|--------|--------|----------|
| **minimal** | 50-100 | Quick checks, automation |
| **concise** | 150-400 | Default, balanced (recommended for manual workflow) |
| **detailed** | 500-1500 | Complex scenarios, debugging |

**Default**: `concise` (provides context without overwhelming token usage)

### Token Usage Examples

**Full 8-scene drama workflow (concise)**:
- Step 2: Analyze idea (~300 tokens)
- Step 4: Scene structure (~500 tokens)
- Step 5: All scene prompts (~3,200 tokens)
- Step 8: Feedback analysis (~300 tokens)
- Step 10: Timeline (~400 tokens)
- Step 12: Metadata (~200 tokens)
- **Total: ~4,900 tokens**

**vs. Detailed format: ~9,800 tokens**
**Savings: 50% by using concise**

---

## Error Handling

All tools follow **Anthropic's helpful error pattern**:

**✅ GOOD Error Response**:
```markdown
## ❌ Error: Missing Scene Structure

**Problem**: The `scene_structure` parameter is empty.

**Expected Format**: 8 scenes: Kavi shows off → Friends ignore → ...

**How to Fix**:
1. First call youtube_video_planner(operation="structure")
2. Then pass the result to youtube_scene_producer

**Example**: [correct usage code]
```

**❌ BAD Error Response** (never do this):
```
Error: Invalid input
Traceback (most recent call last):
  ...
ValueError: validation failed
```

---

## Implementation Checklist

### Phase 1: Core Tools (Priority 1)
- [ ] Implement youtube_video_planner (tool.py, schemas.py, service.py)
- [ ] Implement youtube_scene_producer (tool.py, schemas.py, service.py)
- [ ] Implement youtube_production_manager (tool.py, schemas.py, service.py)
- [ ] Write unit tests for all 3 tools
- [ ] Validate token usage matches specifications

### Phase 2: Agent & API (Priority 2)
- [ ] Create AgentDependencies structure
- [ ] Configure Pydantic AI agent with tools
- [ ] Implement OpenAI-compatible endpoint (/v1/chat/completions)
- [ ] Implement direct workflow endpoints (/api/workflows/video/*)
- [ ] Add request correlation and logging

### Phase 3: Testing & Deployment (Priority 3)
- [ ] Create integration tests for full workflow
- [ ] Test with real "உடையது விளம்பேல்" test case
- [ ] Create evaluation tasks
- [ ] Document API with examples
- [ ] Deploy MVP

---

## References

- **Tool Architecture Design**: `docs/tool-architecture-design.md`
- **Planning Document**: `docs/planning-complete-ready-for-testing.md`
- **Alignment Review**: `docs/alignment-review-from-start.md`
- **Workflow Documentation**: `.claude/workflows/youtube-video-creation-workflow.md`
- **Production Example**: `examples/kavi-peacock-complete-video-production.md`
- **Anthropic Article**: "Writing Tools for Agents" (principles applied throughout)

---

**Status**: ✅ Ready for implementation - All decisions finalized
**Next Step**: Begin Phase 1 implementation (Core Tools)
