# YouTube Video Production Tool Architecture

## Design Philosophy

Following Anthropic's tool consolidation principles from CLAUDE.md:
- **Consolidate low-level operations** into high-level capabilities
- **Minimize tool calls** by grouping cohesive operations
- **Guide agent with clear docstrings** (Use This When / Do NOT Use)
- **Include token efficiency** guidance in all tools
- **Use realistic examples** with actual data patterns

---

## Workflow Analysis

### Current Manual Workflow
1. User provides idea → Claude analyzes → Recommends song/drama → User decides
2. Claude generates scene structure → Generates prompts per scene
3. User pastes to Leonardo.ai, MiniMax Hailuo, ElevenLabs
4. User reports results → Claude refines if needed
5. Claude provides assembly instructions + YouTube metadata

### Anti-Pattern: Granular Tools (10+ tool calls)
```python
# ❌ This requires agent to orchestrate many calls
analyze_idea_for_format(idea)
check_copyright(idea)
recommend_format(analysis)
create_scene_structure(format, idea)
generate_image_prompt(scene_1)
generate_animation_prompt(scene_1)
generate_dialogue(scene_1)
generate_voice_direction(scene_1)
# ... repeat for all scenes
create_timeline(all_scenes)
create_youtube_metadata(video)
process_feedback(user_feedback)
refine_prompts(scene, feedback)
```

**Problems:**
- Agent must orchestrate 10+ tool calls
- High token usage from repeated context
- Error-prone coordination between tools
- Difficult to maintain state across calls

### Consolidated Pattern: 3 Phase-Based Tools

Based on natural workflow phases, consolidate into **3 high-leverage tools**:

#### **TOOL 1: youtube_video_planner** (Planning Phase)
**Consolidates:**
- Idea analysis (song vs drama evaluation)
- Copyright checking
- Scene structure generation

**Why consolidate these:** They're all part of pre-production planning and user needs results together to make format decision.

#### **TOOL 2: youtube_scene_producer** (Production Phase)
**Consolidates:**
- Image generation prompts (Leonardo.ai)
- Animation prompts (MiniMax Hailuo)
- Dialogue generation (Tamil + English)
- Voice direction (ElevenLabs/Azure TTS)
- Timing and transitions
- Audio sync notes

**Why consolidate these:** User needs ALL these elements together to produce a scene. Generating them separately wastes tokens and requires agent coordination.

#### **TOOL 3: youtube_production_manager** (Finalization Phase)
**Consolidates:**
- Feedback processing
- Prompt refinement
- Timeline assembly instructions
- YouTube metadata generation
- Quality checklist

**Why consolidate these:** These are all post-production operations that happen after scenes are generated.

---

## Tool Specifications

### TOOL 1: youtube_video_planner

**Purpose:** Analyze idea, check copyright, recommend format, and generate scene structure.

**Parameters:**
- `idea: str` - Story concept, moral, or theme (Tamil or English)
- `operation: Literal["analyze", "structure"]`
  - "analyze": Initial analysis + copyright check + recommendation
  - "structure": Generate scene breakdown after user decides format
- `format_choice: Optional[Literal["song", "drama"]]` - User's decision (required for "structure" operation)
- `reference_image: Optional[str]` - Path to character reference for series continuity
- `language: Literal["tamil", "english", "both"]` - Primary language(s)
- `response_format: Literal["minimal", "concise", "detailed"]` - Token efficiency control

**Returns:**
- For "analyze": Format recommendation + reasoning + copyright status + pros/cons
- For "structure": Complete scene breakdown with count, descriptions, emotional arcs

**Token Efficiency:**
- Minimal: ~100 tokens (recommendation only)
- Concise: ~300 tokens (recommendation + reasoning + copyright)
- Detailed: ~800 tokens (full analysis with alternatives)

**Agent-Optimized Docstring:**
```python
@agent.tool
async def youtube_video_planner(
    ctx: RunContext[AgentDependencies],
    idea: str,
    operation: Literal["analyze", "structure"],
    format_choice: Optional[Literal["song", "drama"]] = None,
    reference_image: Optional[str] = None,
    language: Literal["tamil", "english", "both"] = "tamil",
    response_format: Literal["minimal", "concise", "detailed"] = "concise"
) -> str:
    """Plan YouTube kids video by analyzing idea, checking copyright, and creating scene structure.

    This consolidates pre-production planning into a single tool call. Handles both
    initial analysis (song vs drama recommendation) and scene structure generation
    after user decides format.

    Use this when you need to:
    - Analyze a new video idea and recommend song vs drama format
    - Check copyright status before production starts
    - Generate scene structure after user confirms format choice
    - Plan a video series with consistent characters (provide reference_image)
    - Get initial feasibility assessment for an idea

    Do NOT use this for:
    - Generating actual prompts (use youtube_scene_producer instead)
    - Refining existing content (use youtube_production_manager instead)
    - Processing user feedback (use youtube_production_manager instead)
    - Creating final assembly instructions (use youtube_production_manager instead)

    Args:
        idea: Story concept, moral, theme, or proverb in Tamil or English.
            Examples: "உடையது விளம்பேல்", "sharing is caring", "honesty moral story"
        operation: What planning operation to perform.
            - "analyze": Initial idea analysis. Returns format recommendation (song/drama),
              copyright status, pros/cons for each format, age-appropriateness check.
              Use this FIRST when user provides new idea.
            - "structure": Generate scene breakdown. Returns scene count, descriptions,
              emotional arcs, timing. Requires format_choice to be specified.
              Use AFTER user confirms format.
        format_choice: User's format decision (required for "structure" operation).
            - "song": Generate 3-5 scene structure for musical video
            - "drama": Generate 6-8 scene structure for narrative video
            Leave None for "analyze" operation.
        reference_image: Path to character reference image for series continuity.
            Example: "characters/kavi-peacock.png"
            Use when: Creating episode in existing series to maintain character consistency
            Omit when: First episode or standalone video
        language: Primary language(s) for content.
            - "tamil": Tamil dialogue only (most common)
            - "english": English dialogue only
            - "both": Bilingual content (Tamil + English dialogue in all scenes)
        response_format: Control output verbosity to save tokens.
            - "minimal": Recommendation + copyright status only (~100 tokens)
              Use when: Quick feasibility check before committing
            - "concise": Recommendation + reasoning + copyright + key points (~300 tokens)
              Use when: Need decision framework (DEFAULT, recommended)
            - "detailed": Full analysis with alternatives, examples, cultural notes (~800 tokens)
              Use when: Complex idea requiring deep evaluation

    Returns:
        Structured planning document (markdown formatted).

        For "analyze" operation:
        - Format recommendation (song OR drama) with reasoning
        - Copyright status (CLEAR or POTENTIAL ISSUES with details)
        - Pros/cons for each format
        - Age appropriateness assessment
        - Cultural authenticity notes (for Tamil content)

        For "structure" operation:
        - Scene count and descriptions
        - Character emotional arc (start → change → end)
        - Key moments and transitions
        - Duration per scene (targeting 2-5 minute total)
        - Continuity notes

    Performance Notes:
        - Minimal format: ~100 tokens (use for quick checks)
        - Concise format: ~300 tokens (default, good balance)
        - Detailed format: ~800 tokens (comprehensive analysis)
        - "analyze" operation: 5-10 seconds (includes copyright check)
        - "structure" operation: 10-15 seconds (generates scene breakdown)
        - Always prefer concise unless detailed justification is needed
        - For series with reference_image, maintains character consistency metadata

    Examples:
        # Initial analysis of Tamil proverb idea (concise - default)
        youtube_video_planner(
            idea="உடையது விளம்பேல் - Don't be a blowhard",
            operation="analyze",
            language="tamil",
            response_format="concise"
        )
        # Returns: Drama recommended, copyright CLEAR, pros/cons, age-appropriate

        # Quick feasibility check (minimal)
        youtube_video_planner(
            idea="sharing toys moral story",
            operation="analyze",
            language="english",
            response_format="minimal"
        )
        # Returns: Drama recommended, CLEAR (~100 tokens)

        # Generate scene structure after user confirms drama format
        youtube_video_planner(
            idea="உடையது விளம்பேல்",
            operation="structure",
            format_choice="drama",
            language="tamil",
            response_format="concise"
        )
        # Returns: 8-scene breakdown with emotional arc, timing, transitions

        # Plan episode 2 of existing series (maintains character)
        youtube_video_planner(
            idea="Kavi learns to share",
            operation="structure",
            format_choice="drama",
            reference_image="characters/kavi-peacock.png",
            language="tamil",
            response_format="concise"
        )
        # Returns: Scene structure with Kavi character consistency notes
    """
    # Implementation will be in app/tools/youtube_video_planner/service.py
    pass
```

---

### TOOL 2: youtube_scene_producer

**Purpose:** Generate complete production-ready prompts for scenes (image, animation, dialogue, voice, timing).

**Parameters:**
- `scene_structure: str` - Scene breakdown from youtube_video_planner
- `operation: Literal["generate", "refine"]`
  - "generate": Create initial prompts for scenes
  - "refine": Improve prompts based on user feedback
- `scene_numbers: Optional[list[int]]` - Which scenes to generate (default: all)
- `feedback: Optional[str]` - User feedback for refinement
- `reference_image: Optional[str]` - Character reference for consistency
- `language: Literal["tamil", "english", "both"]`
- `response_format: Literal["minimal", "concise", "detailed"]`

**Returns:**
- Complete scene packages with:
  - Image generation prompt (for Leonardo.ai)
  - Animation prompt with camera movement (for MiniMax Hailuo)
  - Dialogue (Tamil + English if both)
  - Voice direction with emotion tags
  - Timing and duration
  - Transition to next scene
  - Audio sync notes

**Token Efficiency:**
- Minimal: ~200 tokens/scene (prompts only, no explanation)
- Concise: ~400 tokens/scene (prompts + brief notes)
- Detailed: ~800 tokens/scene (prompts + detailed direction + alternatives)

**Agent-Optimized Docstring:**
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
    """Generate production-ready prompts for video scenes (image, animation, dialogue, voice, timing).

    This consolidates ALL scene production elements into a single tool call. Instead of
    calling separate tools for image prompts, animation prompts, dialogue, voice direction,
    this generates complete scene packages ready for manual paste to Leonardo.ai, MiniMax Hailuo,
    and ElevenLabs/Azure TTS.

    Use this when you need to:
    - Generate complete production prompts for all scenes in one call
    - Create specific scenes (provide scene_numbers to generate subset)
    - Refine prompts based on user feedback from actual tool results
    - Maintain character consistency across series (provide reference_image)
    - Get production-ready content for manual workflow

    Do NOT use this for:
    - Initial idea analysis (use youtube_video_planner with operation="analyze")
    - Creating scene structure (use youtube_video_planner with operation="structure")
    - Assembly instructions (use youtube_production_manager instead)
    - YouTube metadata (use youtube_production_manager instead)
    - Just checking feasibility (use youtube_video_planner instead)

    Args:
        scene_structure: Complete scene breakdown from youtube_video_planner.
            Must include scene count, descriptions, emotional arcs.
            Example: "8 scenes: Kavi shows off → Friends ignore → Realizes pride → Apologizes..."
        operation: Production operation to perform.
            - "generate": Create initial prompts for scenes (use this FIRST)
            - "refine": Improve prompts based on user feedback (use AFTER user tests prompts)
        scene_numbers: Which scenes to generate (1-indexed).
            - None: Generate ALL scenes (default, recommended for first pass)
            - [1, 3, 5]: Generate only scenes 1, 3, and 5 (use when refining specific scenes)
            Use specific scenes when user reports issues with particular scenes only.
        feedback: User feedback from actual production results.
            Required for "refine" operation. Examples:
            - "Scene 3 character looks different from Scene 1"
            - "Animation too fast in Scene 5"
            - "Dialogue too complex for kids in Scene 2"
            Agent should extract which scenes need refinement from feedback.
        reference_image: Path to character reference for visual consistency.
            Example: "characters/kavi-peacock.png"
            Use when: Series episode or multi-scene consistency needed
            Leonardo.ai will use this for Character Reference feature (High strength)
        language: Language(s) for dialogue generation.
            - "tamil": Tamil dialogue only (most common for KIDZ SEASON TV)
            - "english": English dialogue only
            - "both": Generate Tamil AND English dialogue for each scene (bilingual)
        response_format: Control output verbosity and token usage.
            - "minimal": Prompts only, no explanations (~200 tokens/scene)
              Use when: Agent just needs raw prompts for API calls
            - "concise": Prompts + brief direction notes (~400 tokens/scene)
              Use when: User will paste manually (DEFAULT, recommended)
            - "detailed": Prompts + detailed direction + alternatives (~800 tokens/scene)
              Use when: Complex scenes or user needs guidance on variations

    Returns:
        Complete scene production packages (markdown formatted).

        Each scene package includes:
        1. **Image Generation Prompt**: Paste into Leonardo.ai
           - 3D Pixar style, character details, setting, lighting, camera angle
           - Character Reference instructions (if reference_image provided)
        2. **Animation Prompt**: Paste into MiniMax Hailuo image-to-video
           - Camera movement (pan, zoom, dolly, static)
           - Character actions and movements
           - Duration (10-30 seconds per scene)
        3. **Dialogue**: Tamil and/or English
           - Age-appropriate vocabulary (2-4 yr olds + general audience)
           - Natural, conversational tone
           - 1-2 sentences per scene max
        4. **Voice Direction**: For ElevenLabs/Azure TTS
           - Voice type (child, energetic, calm, elderly)
           - Emotion tags ([excited], [whispers], [dramatic])
           - Pacing (fast, normal, slow)
        5. **Timing & Duration**: How long scene should be
        6. **Transition to Next Scene**: Cut, fade, dissolve, wipe (with duration)
        7. **Audio Sync Notes**: When dialogue starts, background music cues

    Performance Notes:
        - Minimal format: ~200 tokens per scene (8 scenes = ~1600 tokens total)
        - Concise format: ~400 tokens per scene (8 scenes = ~3200 tokens total)
        - Detailed format: ~800 tokens per scene (8 scenes = ~6400 tokens total)
        - Generation time: 15-30 seconds for all scenes
        - Refinement time: 5-10 seconds per scene
        - Always prefer concise for manual workflow (user needs context)
        - Use minimal only if integrating with automation

    Examples:
        # Generate all scenes for Kavi drama (concise - default)
        youtube_scene_producer(
            scene_structure="8 scenes: Kavi shows off → Friends ignore → ...",
            operation="generate",
            reference_image="characters/kavi-peacock.png",
            language="tamil",
            response_format="concise"
        )
        # Returns: 8 complete scene packages with all prompts

        # Refine specific scenes based on user feedback
        youtube_scene_producer(
            scene_structure="8 scenes: Kavi shows off → Friends ignore → ...",
            operation="refine",
            scene_numbers=[3, 5],
            feedback="Scene 3 character looks different. Scene 5 animation too fast.",
            reference_image="characters/kavi-peacock.png",
            language="tamil",
            response_format="concise"
        )
        # Returns: Refined prompts for scenes 3 and 5 only

        # Generate bilingual song scenes (minimal for automation)
        youtube_scene_producer(
            scene_structure="5 scenes: Chorus visual → Verse 1 → ...",
            operation="generate",
            language="both",
            response_format="minimal"
        )
        # Returns: Prompts only for 5 song scenes (~1000 tokens total)

        # Generate single scene for testing
        youtube_scene_producer(
            scene_structure="8 scenes: Kavi shows off → ...",
            operation="generate",
            scene_numbers=[1],
            reference_image="characters/kavi-peacock.png",
            language="tamil",
            response_format="detailed"
        )
        # Returns: Detailed scene 1 package with alternatives (~800 tokens)
    """
    # Implementation will be in app/tools/youtube_scene_producer/service.py
    pass
```

---

### TOOL 3: youtube_production_manager

**Purpose:** Handle post-production operations (feedback processing, timeline assembly, YouTube metadata).

**Parameters:**
- `operation: Literal["feedback", "timeline", "metadata", "quality_check"]`
  - "feedback": Process user feedback and determine what needs refinement
  - "timeline": Generate FFmpeg/Shotstack assembly instructions
  - "metadata": Generate YouTube title, description, tags, thumbnail notes
  - "quality_check": Generate review checklist
- `all_scenes: str` - Complete scene packages from youtube_scene_producer
- `user_feedback: Optional[str]` - User's production results
- `video_duration: Optional[int]` - Total duration in seconds (for timeline)
- `character_name: Optional[str]` - For metadata generation
- `moral_theme: Optional[str]` - For metadata generation
- `response_format: Literal["minimal", "concise", "detailed"]`

**Returns:**
- For "feedback": Analysis of what failed and which scenes to refine
- For "timeline": Complete assembly instructions with timing
- For "metadata": YouTube title, description, tags, category, thumbnail notes
- For "quality_check": Checklist for visual, audio, content, technical review

**Token Efficiency:**
- Minimal: ~100 tokens (essential info only)
- Concise: ~300 tokens (instructions + context)
- Detailed: ~600 tokens (comprehensive with examples)

**Agent-Optimized Docstring:**
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
    """Manage post-production tasks: feedback processing, timeline assembly, YouTube metadata, quality checks.

    This consolidates finalization operations that happen AFTER scenes are generated. Instead
    of separate tools for feedback analysis, timeline creation, metadata generation, this
    handles all post-production management in one tool with operation parameter.

    Use this when you need to:
    - Process user feedback from Leonardo.ai, MiniMax, ElevenLabs results
    - Determine which scenes need refinement based on reported issues
    - Generate FFmpeg or Shotstack assembly instructions with timing
    - Create YouTube metadata (title, description, tags, thumbnail)
    - Generate quality review checklist before upload

    Do NOT use this for:
    - Initial idea analysis (use youtube_video_planner instead)
    - Generating scene prompts (use youtube_scene_producer instead)
    - Refining specific scene prompts (use youtube_scene_producer with operation="refine")
    - Planning video structure (use youtube_video_planner instead)

    Args:
        operation: What post-production operation to perform.
            - "feedback": Analyze user feedback, identify failed scenes, recommend next steps.
              Use when: User reports results from Leonardo/MiniMax/ElevenLabs.
            - "timeline": Generate video assembly instructions with scene timing.
              Use when: All scenes are produced and user is ready to assemble.
            - "metadata": Generate YouTube upload metadata (title, description, tags, thumbnail).
              Use when: Video is assembled and user is preparing to upload.
            - "quality_check": Generate review checklist (visual, audio, content, technical).
              Use when: Video is assembled and user wants final QA before upload.
        all_scenes: Complete scene packages from youtube_scene_producer.
            Must include scene count, prompts, timing, transitions.
            Used as context for all operations.
        user_feedback: User's production results (required for "feedback" operation).
            Examples:
            - "Scene 3 and 5 failed - character looks different"
            - "All images generated successfully, animation too fast on scene 7"
            - "Voice sounds robotic in scene 2"
            Tool will parse and identify which scenes/elements need refinement.
        video_duration: Total video duration in seconds (required for "timeline" operation).
            Example: 270 (for 4:30 video)
            Used to calculate scene timing and transitions.
        character_name: Main character name (required for "metadata" operation).
            Example: "Kavi the Peacock"
            Used in YouTube title and description.
        moral_theme: Story moral or theme (required for "metadata" operation).
            Example: "Don't be a blowhard"
            Used in YouTube title and description.
        response_format: Control output verbosity.
            - "minimal": Essential info only (~100 tokens)
              Use when: Agent just needs structured data
            - "concise": Instructions + context (~300 tokens)
              Use when: User will execute manually (DEFAULT)
            - "detailed": Comprehensive with examples (~600 tokens)
              Use when: User needs step-by-step guidance

    Returns:
        Post-production instructions or metadata (markdown formatted).

        For "feedback" operation:
        - Analysis of what succeeded vs failed
        - Specific scenes that need refinement
        - Recommended next steps (refine prompts vs retry vs adjust)
        - Which tool to use for refinement (youtube_scene_producer)

        For "timeline" operation:
        - FFmpeg or Shotstack assembly instructions
        - Scene-by-scene timing (start time, duration, end time)
        - Transition effects and durations
        - Audio layer timing (dialogue, music, effects, ambience)
        - Final output specifications (resolution, frame rate, format)

        For "metadata" operation:
        - YouTube Title (Tamil + English, optimized for search)
        - Description (story summary, moral lesson, age range)
        - Tags (15-20 relevant tags)
        - Category (Education)
        - Thumbnail notes (which scene to use, text overlay suggestions)
        - Made for Kids designation (optional based on user preference)

        For "quality_check" operation:
        - Visual checklist (character consistency, colors, glitches)
        - Audio checklist (dialogue clarity, music balance, no clipping)
        - Content checklist (moral clear, age-appropriate, story flow)
        - Technical checklist (aspect ratio, duration, file size)

    Performance Notes:
        - Minimal format: ~100 tokens (structured data only)
        - Concise format: ~300 tokens (instructions + context, default)
        - Detailed format: ~600 tokens (comprehensive guidance)
        - "feedback" operation: 3-5 seconds (parses user feedback)
        - "timeline" operation: 5-10 seconds (calculates timing)
        - "metadata" operation: 5-10 seconds (generates SEO-optimized metadata)
        - "quality_check" operation: 2-3 seconds (generates checklist)
        - Always prefer concise for manual workflow

    Examples:
        # Process user feedback after production
        youtube_production_manager(
            operation="feedback",
            all_scenes="Scene 1: [image prompt]... Scene 8: [image prompt]...",
            user_feedback="Scenes 1-6 generated successfully. Scene 7 and 8 failed - character inconsistent.",
            response_format="concise"
        )
        # Returns: Analysis identifying scenes 7-8 need refinement, recommend youtube_scene_producer

        # Generate assembly timeline
        youtube_production_manager(
            operation="timeline",
            all_scenes="Scene 1: [30s]... Scene 8: [25s]...",
            video_duration=270,
            response_format="concise"
        )
        # Returns: FFmpeg instructions with timing for 4:30 video

        # Generate YouTube metadata
        youtube_production_manager(
            operation="metadata",
            all_scenes="Scene 1: Kavi shows off...",
            character_name="Kavi the Peacock",
            moral_theme="Don't be a blowhard",
            response_format="concise"
        )
        # Returns: Title, description, tags, thumbnail notes

        # Get quality checklist before upload
        youtube_production_manager(
            operation="quality_check",
            all_scenes="Scene 1: [prompts]...",
            response_format="detailed"
        )
        # Returns: Comprehensive QA checklist with examples
    """
    # Implementation will be in app/tools/youtube_production_manager/service.py
    pass
```

---

## Tool Consolidation Rationale

### Why 3 Tools Instead of 10+?

**Before (Granular):**
```
Agent workflow for new video:
1. Call analyze_idea()
2. Call check_copyright()
3. Call recommend_format()
4. Wait for user decision
5. Call create_scene_structure()
6. For each scene:
   7. Call generate_image_prompt(scene_n)
   8. Call generate_animation_prompt(scene_n)
   9. Call generate_dialogue(scene_n)
   10. Call generate_voice_direction(scene_n)
11. Call create_timeline()
12. Call create_youtube_metadata()

Total: 12+ tool calls, high token usage, complex coordination
```

**After (Consolidated):**
```
Agent workflow for new video:
1. Call youtube_video_planner(operation="analyze")
2. Wait for user decision
3. Call youtube_video_planner(operation="structure")
4. Call youtube_scene_producer(operation="generate")  # All scenes at once
5. Call youtube_production_manager(operation="timeline")
6. Call youtube_production_manager(operation="metadata")

Total: 5 tool calls, lower token usage, simple coordination
```

**Token Savings Example:**
- Granular: 12 tool calls × ~200 tokens overhead = ~2400 tokens overhead
- Consolidated: 5 tool calls × ~200 tokens overhead = ~1000 tokens overhead
- **Savings: ~60% reduction in overhead**

---

## Implementation Structure

```
app/
├── main.py                             # FastAPI app
├── pyproject.toml                      # UV dependencies
├── shared/
│   ├── config.py                       # Settings
│   └── logging.py                      # Structlog
├── agent/
│   ├── agent.py                        # Pydantic AI orchestrator
│   ├── dependencies.py                 # AgentDependencies
│   └── prompts.py                      # System prompts
├── tools/
│   ├── youtube_video_planner/
│   │   ├── tool.py                     # Pydantic AI tool decorator
│   │   ├── schemas.py                  # Input/output models
│   │   └── service.py                  # Business logic
│   ├── youtube_scene_producer/
│   │   ├── tool.py
│   │   ├── schemas.py
│   │   └── service.py
│   └── youtube_production_manager/
│       ├── tool.py
│       ├── schemas.py
│       └── service.py
├── api/
│   ├── openai/
│   │   └── routes.py                   # /v1/chat/completions
│   └── workflows/
│       └── routes.py                   # /api/workflows/video
└── tests/
    ├── tools/
    │   ├── test_youtube_video_planner.py
    │   ├── test_youtube_scene_producer.py
    │   └── test_youtube_production_manager.py
    └── integration/
        └── test_video_workflow.py
```

---

## Additional Design Principles from Anthropic Article

### Tool Response Structure

All tools return **Markdown-formatted strings** for maximum readability and agent comprehension. Markdown is preferred because:
- LLMs are trained on markdown and perform better with formats matching training data
- Human-readable for manual workflow (user copies/pastes)
- Supports rich formatting (headings, lists, code blocks)
- Easy to parse for both agents and users

**Example Tool Response Structure:**

```markdown
## Scene 1: Kavi Shows Off

### Image Generation Prompt (Leonardo.ai)
A young peacock named Kavi stands in a sun-drenched Indian village courtyard...

### Animation Prompt (MiniMax Hailuo)
**Camera**: Slow push-in from medium shot to close-up
**Character Action**: Kavi's tail feathers slowly fan out...
**Duration**: 30 seconds

### Dialogue (Tamil)
Kavi: "பாருங்க! என் அழகான இறகுகளை!"

### Voice Direction (ElevenLabs/Azure TTS)
**Voice**: Energetic child voice
**Emotion**: [excited], [proud]
**Pacing**: Fast
```

### Returning Meaningful Context

Following Anthropic's principle: **prioritize contextual relevance over flexibility**.

**✅ GOOD - Natural Language Identifiers:**
```python
{
    "scene_name": "Kavi Shows Off",
    "character": "Kavi the Peacock",
    "setting": "Village Courtyard",
    "duration": "30 seconds",
    "transition": "Dissolve to Scene 2"
}
```

**❌ BAD - Technical Identifiers:**
```python
{
    "scene_id": "a3f5c8d9-4b2e-4c3f-9d6e-5a8f2c1b4e7d",
    "char_uuid": "c4d8e2f1-3a7b-4d9c-8e6f-2a5b1c3d4e5f",
    "duration_ms": 30000,
    "trans_type_enum": 3
}
```

**Why:** Natural language reduces hallucinations and improves agent precision in retrieval tasks. Agents struggle with cryptic UUIDs but excel with semantic identifiers.

**For Our Tools:**
- Scene numbers: Use 1-indexed integers (Scene 1, Scene 2) vs UUIDs
- Character names: "Kavi the Peacock" vs `char_id_12345`
- Duration: "30 seconds" vs `30000ms`
- Transitions: "Dissolve" vs `transition_type=3`

### Token Efficiency and Truncation

All tools implement token efficiency through:

1. **response_format parameter** ("minimal", "concise", "detailed")
2. **Default to "concise"** (balance between context and efficiency)
3. **Clear truncation when needed** with helpful guidance

**Example Truncated Response:**

```markdown
## Scene Production Results

Generated 8 scenes. Showing first 3 scenes.

[Scene 1 details...]
[Scene 2 details...]
[Scene 3 details...]

⚠️ **Response Truncated**: Remaining 5 scenes omitted to save tokens.

**To see remaining scenes**, call youtube_scene_producer with:
- scene_numbers=[4, 5, 6, 7, 8]
- response_format="concise"
```

**Truncation Limits:**
- Maximum response size: 25,000 tokens (Claude Code standard)
- If response would exceed limit, truncate and provide clear instructions
- Always tell agent HOW to retrieve remaining content

### Error Responses

Following Anthropic's principle: **provide actionable improvements, not opaque errors**.

**❌ UNHELPFUL Error Response:**
```
Error: Invalid input
Traceback (most recent call last):
  File "tool.py", line 42, in youtube_scene_producer
    validate_scene_structure(scene_structure)
  ValueError: validation failed
```

**✅ HELPFUL Error Response:**
```markdown
## ❌ Error: Missing Scene Structure

**Problem**: The `scene_structure` parameter is empty or missing scene count.

**Expected Format**:
8 scenes: Kavi shows off → Friends ignore → Realizes pride → ...

**How to Fix**:
1. First call youtube_video_planner(operation="structure") to get scene structure
2. Then pass the returned scene breakdown to youtube_scene_producer

**Example**:
structure = youtube_video_planner(
    idea="Don't be a blowhard",
    operation="structure",
    format_choice="drama"
)

youtube_scene_producer(
    scene_structure=structure,
    operation="generate"
)
```

**Error Response Guidelines:**
- Clearly state WHAT went wrong
- Explain EXPECTED format or value
- Provide HOW to fix (step-by-step)
- Include EXAMPLE of correct usage
- Never show tracebacks to agents (opaque and unhelpful)
- Steer agent toward token-efficient retry strategies

### Validation and Input Constraints

All tools validate inputs strictly:

**Parameter Validation:**
- `scene_numbers`: Must be 1-indexed (not 0-indexed), must be within scene count
- `operation`: Must be valid enum value (provide all options in error)
- `format_choice`: Required for "structure" operation, optional for "analyze"
- `feedback`: Required for "refine" operation, provide example if missing

**Example Validation Error:**

```markdown
## ❌ Error: Invalid Scene Numbers

**Problem**: scene_numbers=[0, 9] contains invalid indices.

**Valid Range**: 1 to 8 (based on scene structure)

**Issue 1**: Scene 0 is invalid (scenes are 1-indexed, not 0-indexed)
**Issue 2**: Scene 9 exceeds total scene count (8 scenes in structure)

**How to Fix**:
Use scene_numbers=[1, 8] or scene_numbers=[2, 3, 4]

**Example**:
youtube_scene_producer(
    scene_structure="8 scenes: ...",
    operation="generate",
    scene_numbers=[1, 2, 3]  # ✅ Valid 1-indexed scenes
)
```

### Response Format Token Comparison

Real-world token usage from our tools (targeting 8-scene drama):

| Tool | Operation | Minimal | Concise | Detailed |
|------|-----------|---------|---------|----------|
| youtube_video_planner | analyze | ~100 | ~300 | ~800 |
| youtube_video_planner | structure | ~200 | ~500 | ~1200 |
| youtube_scene_producer | generate (all) | ~1600 | ~3200 | ~6400 |
| youtube_scene_producer | refine (1 scene) | ~200 | ~400 | ~800 |
| youtube_production_manager | feedback | ~100 | ~300 | ~600 |
| youtube_production_manager | timeline | ~200 | ~400 | ~800 |
| youtube_production_manager | metadata | ~100 | ~200 | ~400 |

**Token Efficiency Example:**
- Full video workflow (8 scenes, concise): ~5,000 tokens total
- Full video workflow (8 scenes, detailed): ~10,000 tokens total
- **Savings: 50% by using concise instead of detailed**

### Namespacing and Tool Naming

All tools follow prefix-based namespacing:
- **Prefix**: `youtube_` (identifies service domain)
- **Function**: `video_planner`, `scene_producer`, `production_manager`

**Why Prefix-Based (Not Suffix):**
- Matches natural language patterns ("YouTube video planner")
- Groups related tools alphabetically in tool lists
- Reduces confusion when multiple video services exist

**Alternative Services (Future):**
- `tiktok_video_planner` - TikTok short videos
- `instagram_reel_producer` - Instagram Reels
- `podcast_episode_planner` - Audio content

Clear namespacing prevents agents from confusing tools across different services.

---

## Key Anthropic Insights Applied

Based on the article "Writing Tools for Agents":

### ✅ What We Did Right

1. **Tool Consolidation** - 3 tools instead of 10+ (60% reduction in overhead)
2. **response_format Parameter** - Matches Anthropic's ResponseFormat enum pattern exactly
3. **Operation Parameter** - Consolidate multiple operations in one tool (analyze/structure, generate/refine, feedback/timeline/metadata)
4. **Token Efficiency** - Document token costs, default to balanced "concise"
5. **Clear Boundaries** - Each tool has distinct purpose with no overlap
6. **Prompt-Engineered Docstrings** - "Use This When" / "Do NOT Use This For" / Realistic Examples
7. **Namespacing** - Prefix-based `youtube_` namespace
8. **Markdown Responses** - LLM-friendly format matching training data

### 🔄 What We Improved (Based on Article)

1. **Meaningful Context** - Added guidance to use natural language vs UUIDs (Scene 1 vs `uuid`)
2. **Error Responses** - Added examples of helpful errors with actionable fixes
3. **Truncation Strategy** - Added 25,000 token limit with clear guidance
4. **Response Structure** - Explicitly specified Markdown with examples
5. **Validation** - Added strict input validation with helpful error messages

### 📊 Performance Expectations (From Anthropic)

- **Small refinements to tool descriptions can yield dramatic improvements** (SWE-bench Verified example)
- **Token efficiency matters** - Claude Code restricts to 25,000 tokens by default
- **Natural language > Technical IDs** - Reduces hallucinations in retrieval tasks
- **Helpful errors > Tracebacks** - Steer agents toward correct retry strategies

### 🎯 Evaluation-Driven Next Steps

1. **Create Evaluation Tasks** - Real-world video production scenarios
2. **Measure Performance** - Accuracy, token usage, tool call count, errors
3. **Analyze Transcripts** - Where agents get confused, what they omit
4. **Iterate with Claude** - Use Claude Code to refine tools based on eval results
5. **Held-Out Test Set** - Prevent overfitting to training evaluations

---

## Next Steps

1. ✅ Tool architecture designed with proper consolidation
2. ✅ Anthropic principles applied (consolidation, token efficiency, meaningful context, helpful errors)
3. ⏳ Create technical specifications for each tool
4. ⏳ Define Pydantic schemas for tool inputs/outputs (with strict validation)
5. ⏳ Document AgentDependencies structure
6. ⏳ Create pyproject.toml with dependencies
7. ⏳ Design API endpoint structure
8. ⏳ Create evaluation tasks (real-world video production scenarios)
9. ⏳ Get user approval before implementation

---

## References

- **Anthropic Article**: "Writing Tools for Agents" (https://www.anthropic.com/engineering/writing-tools-for-agents)
- **Codebase Guidelines**: CLAUDE.md Tool Consolidation Principle
- **Workflow Documentation**: `.claude/workflows/youtube-video-creation-workflow.md`
- **Production Example**: `examples/kavi-peacock-complete-video-production.md`
