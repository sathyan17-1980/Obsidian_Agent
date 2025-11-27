# Planning Phase Complete - Ready for Testing

**Date**: 2025-01-27
**Status**: ✅ PLANNING COMPLETE - Ready for test execution
**Test Case**: "உடையது விளம்பேல்" - Don't be a blowhard

---

## ✅ All User Decisions Confirmed

| Question | User's Answer | Implementation Status |
|----------|---------------|----------------------|
| 1. Audience Language | Update ALL to "general audience (family-friendly)", "Made for Kids" OPTIONAL | ✅ Updated |
| 2. Architecture | Eliminate `core/`, use `shared/` only | ✅ Finalized |
| 3. Character Reference | User will create with provided prompt | ✅ Prompt provided below |
| 4. Music Prompts | Automated (tool generates Suno prompt) | ✅ Added to youtube_scene_producer |
| 5. Series Continuity | Kavi recurring BUT user can specify new character per episode | ✅ Added character_choice parameter |
| 6. API Endpoints | Option C: Hybrid (chat + direct endpoints) | ✅ Architecture defined |
| 7. Feedback Storage | Stateless for now | ✅ Confirmed |

---

## 📐 Finalized Architecture

```
app/
├── main.py                             # FastAPI app entry point
├── pyproject.toml                      # UV dependencies
│
├── shared/                             # Cross-cutting concerns
│   ├── __init__.py
│   ├── config.py                       # Settings (Pydantic BaseSettings)
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
│   │   ├── tool.py                     # Pydantic AI @agent.tool decorator
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
│       └── routes.py                   # POST /api/workflows/video/*
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

**Key Points**:
- ✅ `core/` eliminated (simpler VSA)
- ✅ `shared/` for cross-cutting concerns
- ✅ `agent/` for Pydantic AI orchestration
- ✅ `tools/` for 3 consolidated tools
- ✅ `api/` split into `openai/` and `workflows/` (Hybrid approach)

---

## 🔄 Updated Tool Specifications

### Changes Based on User Decisions

#### 1. youtube_video_planner - Added Character Selection

**NEW Parameter**:
```python
character_choice: Literal["new", "existing"] = "new"
existing_character_name: Optional[str] = None  # Required if character_choice="existing"
reference_image: Optional[str] = None  # Path to reference (if existing character)
```

**How It Works**:
- **New Character**: User wants fresh character for this video
  - Tool generates character design as part of scene structure
  - User creates reference image from generated design

- **Existing Character** (e.g., Kavi): User wants recurring character
  - User provides: `character_choice="existing"`, `existing_character_name="Kavi the Peacock"`, `reference_image="characters/kavi-peacock.png"`
  - Tool maintains character consistency across all scenes

**Updated Function Signature**:
```python
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

#### 2. youtube_scene_producer - Added Music Prompt Generation

**NEW Output**: Music prompts for Suno (automated)

**For Drama Videos**:
- Generates background music prompt for Suno
- Includes: Genre, mood, tempo, instruments, duration
- Example: "Gentle acoustic background music for kids, playful piano and soft strings, upbeat but calm, 4:30 duration, no lyrics, educational storytelling vibe"

**For Song Videos**:
- Generates complete song prompt for Suno
- Includes: Lyrics (Tamil/English), genre, style, tempo, target audience
- Example: "Kids educational song in Tamil, nursery rhyme style, upbeat tempo, playful acoustic instruments, female child voice, lyrics about sharing and kindness"

**Updated Returns**:
Each scene package now includes:
1. Image Generation Prompt (Leonardo.ai)
2. Animation Prompt (MiniMax Hailuo)
3. Dialogue (Tamil/English)
4. Voice Direction (ElevenLabs/Azure TTS)
5. Timing & Duration
6. Transition to Next Scene
7. Audio Sync Notes
8. **NEW**: Music Prompt (Suno) - for background music or full song

---

## 🎨 Character Reference Creation Prompt

**For your test case, here's the prompt to create Kavi the Peacock reference image:**

### Step 1: Generate Character Reference in Leonardo.ai

**Prompt**:
```
Character design sheet for Kavi the Peacock, young male peacock character (child equivalent, 6-7 years old), vibrant iridescent blue-green feathers on body, small elegant red vest with gold trim, delicate silver anklets on both feet, large expressive brown eyes with long eyelashes showing innocence, small orange beak, friendly and approachable personality, 3D Pixar Disney animation style, turnaround character sheet showing front view 3/4 view and side profile, white background, consistent lighting, character reference for animation, highly detailed feathers with realistic iridescence, warm and inviting expression, rendered in Unreal Engine, 8K quality, Pixar quality character design

Style: 3D Render, Character Sheet
Aspect Ratio: 1:1 (square)
Model: Leonardo Phoenix or Leonardo Kino XL
```

**Settings in Leonardo.ai**:
- **Preset**: 3D Render or Cinematic
- **Image Dimensions**: 1024×1024 (square)
- **Number of Images**: Generate 3-4 variations
- **Prompt Magic**: ON (if available)
- **PhotoReal**: OFF (maintain cartoon style)

**After Generation**:
1. Select the best version (most consistent, friendly, age-appropriate)
2. Download as `kavi-peacock-reference.png`
3. Save to `characters/` folder in your project
4. Use this for ALL future Kavi episodes

**Why This Works**:
- ✅ Turnaround sheet shows multiple angles (helps Leonardo maintain consistency)
- ✅ Specific details (blue-green, red vest, silver anklets) are unique identifiers
- ✅ "Character reference for animation" signals intended use
- ✅ White background makes it easy to use as reference
- ✅ Pixar style matches your video aesthetic

---

## 🧪 Test Execution Plan: "உடையது விளம்பேல்"

### Test Scenario Details

**Idea**: "உடையது விளம்பேல் - Don't be a blowhard and keep speaking about yourself at all times"
**Language**: Tamil
**Expected Format**: Drama (based on moral story structure)
**Character**: NEW character for this test (you'll create reference after Step 1)
**Expected Scenes**: 6-8 scenes (typical for drama)
**Expected Duration**: 2-5 minutes

---

### Step-by-Step Test Execution

#### **STEP 1: Analyze Idea**

**User Action**: Provide idea to agent

**Agent Call**:
```python
youtube_video_planner(
    idea="உடையது விளம்பேல் - Don't be a blowhard and keep speaking about yourself at all times",
    operation="analyze",
    character_choice="new",  # New character for this test
    language="tamil",
    response_format="concise"
)
```

**Expected Output** (~300 tokens):
```markdown
## Video Format Analysis

### Recommendation: Drama ✅

**Reasoning**:
- Clear character arc: Boastful → Consequence → Realization → Humility
- Strong cause-effect relationship (boasting → isolation → learning)
- Emotional journey suitable for storytelling
- Moral is better shown through narrative than song

**Pros for Drama**:
- Character development (boastful to humble)
- Relatable scenarios (showing off to friends)
- Visual storytelling opportunities (facial expressions, reactions)
- Clear beginning, middle, end

**Cons for Song**:
- Moral requires context/story to land properly
- Risk of repetitive lyrics becoming preachy
- Less emotional impact than narrative

### Copyright Status: CLEAR ✅

**Analysis**:
- Public domain Tamil proverb (traditional wisdom)
- No existing copyrighted characters referenced
- Original character creation (peacock, rabbit, owl - generic animals)
- Safe to proceed

### Age Appropriateness: ✅ General Audience (Family-Friendly)

- Positive moral message (humility over pride)
- No scary or inappropriate content
- Relatable for all ages (everyone knows someone boastful)
- Educational value for children, entertaining for adults

**Recommended Format**: Drama (6-8 scenes, 3-4 minutes)
```

**User Decision**: Confirm Drama ✅

---

#### **STEP 2: Generate Scene Structure**

**User Action**: Confirm format choice

**Agent Call**:
```python
youtube_video_planner(
    idea="உடையது விளம்பேல் - Don't be a blowhard and keep speaking about yourself at all times",
    operation="structure",
    format_choice="drama",
    character_choice="new",  # New character
    language="tamil",
    response_format="concise"
)
```

**Expected Output** (~500 tokens):
```markdown
## Scene Structure: "உடையது விளம்பேல்" (Don't Be a Blowhard)

**Total Scenes**: 8
**Total Duration**: 4 minutes 30 seconds
**Character**: Kavi the Peacock (young, boastful, learns humility)

### Character Emotional Arc
**Start**: Overly proud, boastful, self-absorbed
**Turning Point**: Faces consequence (storm ruins his feathers)
**Change**: Realizes beauty comes from within
**End**: Humble, kind, values friendship over appearance

---

### Scene Breakdown

**Scene 1: Kavi Shows Off** (30 seconds)
- Kavi displays his feathers to village birds
- Boasts about his beauty
- Other birds look annoyed, roll eyes
- **Emotion**: Pride, obliviousness

**Scene 2: Kavi Brags to Forest Friends** (25 seconds)
- Kavi corners forest animals (rabbit, turtle, deer)
- Talks endlessly about himself
- Friends exchange awkward glances
- **Emotion**: Self-absorption, friends' discomfort

**Scene 3: The Rainstorm** (35 seconds)
- Sudden storm drenches Kavi
- His beautiful feathers droop, bedraggled
- Stands alone, shocked
- **Emotion**: Shock, vulnerability, loss

**Scene 4: Wise Owl Appears** (30 seconds)
- Kindly owl approaches sad Kavi
- Offers wisdom: "True beauty is in the heart"
- Kavi listens, tearful
- **Emotion**: Sadness, realization

**Scene 5: Kavi Apologizes to Friends** (25 seconds)
- Kavi finds rabbit, turtle, deer
- Apologizes for being self-centered
- Asks for forgiveness
- **Emotion**: Humility, sincerity

**Scene 6: Friends Forgive Kavi** (25 seconds)
- Animals smile, welcome Kavi back
- Group hug/gathering
- Kavi's feathers starting to dry, but he doesn't focus on them
- **Emotion**: Joy, acceptance, friendship

**Scene 7: Kavi Helps Others** (30 seconds)
- Kavi helps rabbit gather food
- Focuses on others, not himself
- Friends appreciate him for kindness
- **Emotion**: Generosity, purpose

**Scene 8: Moral Lesson** (30 seconds)
- Kavi with friends, happy and humble
- Feathers now dry and beautiful again
- But Kavi doesn't boast - smiles humbly
- Narrator/owl: "உடையது விளம்பேல்" message
- **Emotion**: Contentment, wisdom, resolution

---

### Continuity Notes
- **Character Design**: Kavi should look slightly disheveled after Scene 3 until Scene 8
- **Color Grading**: Bright → Dark (storm) → Warm (resolution)
- **Music**: Playful → Melancholic → Hopeful → Joyful
- **Pacing**: Quick → Slow (storm) → Gentle (resolution)

### Key Moments
1. **Setup** (Scenes 1-2): Establish Kavi's pride
2. **Conflict** (Scene 3): Storm challenges his vanity
3. **Wisdom** (Scene 4): Owl teaches lesson
4. **Resolution** (Scenes 5-8): Kavi changes, values relationships

**Next Step**: Generate complete scene packages with prompts
```

**User Decision**: Approve structure ✅

---

#### **STEP 3: Generate All Scene Prompts**

**User Action**: Confirm scene structure

**Agent Call**:
```python
youtube_scene_producer(
    scene_structure="[Full structure from Step 2]",
    operation="generate",
    character_choice="new",  # New character, no reference yet
    language="tamil",
    response_format="concise"
)
```

**Expected Output** (~3,200 tokens for 8 scenes, ~400 tokens/scene):

**Example for Scene 1**:
```markdown
## SCENE 1: Kavi Shows Off (30 seconds)

### Image Generation Prompt (Leonardo.ai)
Kavi the young peacock, vibrant blue-green iridescent body, small red vest with gold trim, silver anklets on feet, large expressive brown eyes with long lashes, small orange beak, standing proudly on wooden fence post in Tamil village courtyard, fanning magnificent tail feathers in full display, chest puffed out, head tilted back with overconfident smirk, village birds (sparrows, mynahs, parrots) in background looking unimpressed and rolling eyes, sun-drenched courtyard with vibrant bougainvillea flowers and terracotta pots, warm golden morning sunlight, soft rim lighting on feathers creating rainbow glints, 3D Pixar Disney style, exaggerated expressions, warm color palette, low angle camera looking up at Kavi, cinematic lighting, 8K quality

**Leonardo.ai Settings**:
- Model: Leonardo Phoenix
- Aspect Ratio: 9:16 (vertical, 576×1024)
- Number of Images: 2-3
- Character Reference: None (first image, will become reference)

---

### Animation Prompt (MiniMax Hailuo)
**Camera**: Slow push-in from medium shot to close-up
**Character Action**: Kavi's tail feathers slowly fan out to full display, chest puffs up with pride, head tilts back, slight shimmer effect on feathers catching sunlight
**Background Action**: Village birds turn heads to look, some roll eyes, one covers face with wing
**Duration**: 30 seconds
**Movement Style**: Smooth, exaggerated Pixar-style animation with emphasis on prideful gestures
**Camera Control**: "slow zoom in, slight upward tilt"

---

### Dialogue (Tamil)
**Kavi**: "பாருங்க! என் அழகான இறகுகளை! நான் எவ்வளவு அழகாக இருக்கிறேன்!"
*(English: "Look! My beautiful feathers! How handsome I am!")*

**Village Bird 1** *(whispers)*: "அடடா, மறுபடியும் தன்னைப் பற்றி பேசுகிறான்..."
*(English: "Oh no, he's talking about himself again...")*

---

### Voice Direction (ElevenLabs / Azure TTS)
**Kavi**:
- Voice Type: Energetic child voice (Tamil male child)
- Emotion Tags: [excited], [boastful], [proud]
- Pacing: Fast, animated
- Tone: High-pitched, enthusiastic

**Village Bird**:
- Voice Type: Older bird voice (Tamil female)
- Emotion Tags: [whispering], [exasperated], [annoyed]
- Pacing: Normal
- Tone: Dry, tired

**Azure TTS Tamil Voice Recommendations**:
- Kavi: `ta-IN-ValluvarNeural` (male, young tone)
- Village Bird: `ta-IN-PallaviNeural` (female, mature tone)

---

### Timing & Duration
**Total Scene**: 30 seconds

**Timeline**:
- 0:00-0:02: Background village ambience (birds chirping)
- 0:02-0:08: Kavi's dialogue
- 0:09-0:12: Village bird's whispered comment
- 0:13-0:30: Soft background music (playful, slightly mischievous)

---

### Transition to Scene 2
- **Type**: Dissolve
- **Duration**: 1 second
- **Effect**: Fade from bright courtyard to softer forest lighting
- **Audio**: Background music continues seamlessly

---

### Audio Sync Notes
**Dialogue Layer**:
- Kavi starts at 0:02 (after 2-second ambience)
- Village bird whisper at 0:09 (1 second after Kavi finishes)

**Music Layer**:
- Background music fades in at 0:13
- Volume: 20% (subtle, doesn't overpower dialogue)
- Continue through transition to Scene 2

**Ambience Layer**:
- Village sounds (birds, distant activity) 0:00-0:30
- Volume: 15% (very subtle background)

---

### Music Prompt (Suno) - Background Music

**For the entire drama** (generated once, used across scenes):

**Prompt**:
```
Gentle acoustic background music for Tamil kids story, playful piano melody with soft strings, upbeat but calm tempo, educational storytelling vibe, positive and warm atmosphere, no lyrics instrumental only, suitable for 3-5 minute video, seamless looping sections for scene transitions, family-friendly, Pixar movie soundtrack style, 4 minutes 30 seconds duration
```

**Suno Settings**:
- Style: Instrumental, Acoustic, Kids Music
- Mood: Playful, Warm, Educational
- Duration: 4:30 (full video length)
- Lyrics: None (instrumental only)

**Usage Instructions**:
- This background music plays throughout the video at low volume (15-25%)
- Fades in/out during scene transitions
- Volume adjusts based on dialogue (duck under dialogue, raise during silence)
- Creates cohesive audio continuity across all 8 scenes

---

### Notes for User
1. **Save Scene 1 Image**: After generating in Leonardo.ai, save the best version as `kavi-peacock-reference.png`
2. **Use as Character Reference**: Upload this image to Leonardo.ai Character Reference for Scenes 2-8
3. **Set Reference Strength**: High (to maintain consistency)
4. **Generate Background Music**: Paste Suno prompt, generate once, download
5. **Sync Audio**: Use timeline above for precise audio placement

---
```

**This repeats for all 8 scenes**, each with:
- Image generation prompt (Leonardo.ai)
- Animation prompt (MiniMax Hailuo)
- Dialogue (Tamil + English translation)
- Voice direction (ElevenLabs/Azure TTS)
- Timing & duration
- Transition to next scene
- Audio sync notes
- Music prompt (Suno) - included in Scene 1, referenced in subsequent scenes

**Total Output**: ~3,200 tokens (8 scenes × ~400 tokens each)

---

#### **STEP 4: User Creates Character Reference**

**User Action**:
1. Paste Scene 1 image prompt into Leonardo.ai
2. Generate 2-3 variations
3. Select best version (most consistent, friendly, on-brand)
4. Download as `characters/kavi-peacock-reference.png`
5. Upload to Leonardo.ai as Character Reference
6. Set Reference Strength: HIGH

**This reference is now saved for**:
- All remaining scenes in this video (Scenes 2-8)
- All future Kavi episodes

---

#### **STEP 5: User Generates All Assets Manually**

**For Each Scene (1-8)**:

**Images** (Leonardo.ai):
1. Paste image generation prompt
2. Upload character reference (from Scene 1)
3. Set reference strength: High
4. Generate 2-3 variations
5. Select best version
6. Download as `scene_01.png` through `scene_08.png`

**Animation** (MiniMax Hailuo):
1. Upload scene image
2. Paste animation prompt
3. Set duration (10-30 seconds per scene)
4. Generate video
5. Download as `scene_01_animated.mp4` through `scene_08_animated.mp4`

**Voice** (Azure TTS or ElevenLabs):
1. Paste Tamil dialogue
2. Select voice (ta-IN-ValluvarNeural for Kavi, ta-IN-PallaviNeural for others)
3. Apply emotion tags
4. Generate audio
5. Download as `dialogue_scene_01.mp3` through `dialogue_scene_08.mp3`

**Music** (Suno):
1. Paste Suno background music prompt (from Scene 1 output)
2. Generate 2-3 variations
3. Select best version
4. Download as `background_music.mp3` (4:30 duration)

**Expected Results**:
- 8 images (scene_01.png to scene_08.png)
- 8 animated videos (scene_01_animated.mp4 to scene_08_animated.mp4)
- 8 dialogue audio files (dialogue_scene_01.mp3 to dialogue_scene_08.mp3)
- 1 background music file (background_music.mp3)

---

#### **STEP 6: User Reports Results**

**Best Case** (all successful):
```
User: "All 8 scenes generated successfully! Images look consistent, animations are smooth, voice is clear."
```
→ Skip to Step 8 (Timeline Assembly)

**Common Case** (some failures):
```
User: "Scenes 1-6 worked great. Scene 7 character looks different (wrong colors), Scene 8 animation too fast."
```
→ Proceed to Step 7 (Refinement)

---

#### **STEP 7: Agent Processes Feedback & Refines**

**Agent Call** (Feedback Analysis):
```python
youtube_production_manager(
    operation="feedback",
    all_scenes="[Full scenes from Step 3]",
    user_feedback="Scenes 1-6 worked great. Scene 7 character looks different (wrong colors), Scene 8 animation too fast.",
    response_format="concise"
)
```

**Expected Output** (~300 tokens):
```markdown
## Feedback Analysis

### Success Rate: 75% (6/8 scenes successful) ✅

### Successful Scenes
- **Scenes 1-6**: ✅ All elements generated correctly
  - Character consistency maintained
  - Animation timing appropriate
  - Voice quality good

### Failed Scenes

#### Scene 7: Character Inconsistency ❌
**Issue**: Character looks different (wrong colors)

**Root Cause**: Likely Leonardo.ai didn't apply Character Reference correctly

**Recommended Fix**:
1. Verify Character Reference is uploaded and selected
2. Ensure Reference Strength is set to HIGH
3. Regenerate Scene 7 image with exact same prompt
4. If still failing, manually adjust prompt to emphasize character details:
   - Add: "IMPORTANT: Blue-green iridescent body, red vest, silver anklets (match reference image exactly)"

**Next Step**: Call youtube_scene_producer with operation="refine", scene_numbers=[7]

---

#### Scene 8: Animation Too Fast ❌
**Issue**: Animation timing inappropriate

**Root Cause**: MiniMax Hailuo animation speed not matching requested duration

**Recommended Fix**:
1. Regenerate animation with explicit timing control
2. Update animation prompt to emphasize: "SLOW pacing, gentle movements, 30 seconds duration"
3. Use camera control: "static shot, minimal movement"

**Next Step**: Call youtube_scene_producer with operation="refine", scene_numbers=[8]

---

### Refinement Strategy

**Option 1** (Recommended): Refine both scenes in one call
```python
youtube_scene_producer(
    scene_structure=original_structure,
    operation="refine",
    scene_numbers=[7, 8],
    feedback="Scene 7 wrong colors, Scene 8 animation too fast",
    reference_image="characters/kavi-peacock-reference.png",
    language="tamil"
)
```

**Option 2**: Refine one at a time (if issues are very different)
```python
# First refine Scene 7
youtube_scene_producer(..., scene_numbers=[7], feedback="wrong colors")
# Then refine Scene 8
youtube_scene_producer(..., scene_numbers=[8], feedback="animation too fast")
```

**Estimated Success Rate After Refinement**: 95%+ (character reference fixes are highly effective)
```

**Agent Call** (Refinement):
```python
youtube_scene_producer(
    scene_structure="[Full structure from Step 2]",
    operation="refine",
    scene_numbers=[7, 8],
    feedback="Scene 7 character looks different (wrong colors), Scene 8 animation too fast",
    reference_image="characters/kavi-peacock-reference.png",
    language="tamil",
    response_format="concise"
)
```

**Expected Output** (~800 tokens for 2 scenes):
```markdown
## Refined Scene Prompts

### SCENE 7: Kavi Helps Others (30 seconds) - REFINED

#### Image Generation Prompt (Leonardo.ai) - UPDATED
**IMPORTANT: Character Reference MUST match exactly**

Kavi the young peacock (MATCH REFERENCE EXACTLY: vibrant blue-green iridescent body, small red vest with gold trim, silver anklets on both feet, large expressive brown eyes with long lashes, small orange beak), helping brown rabbit gather berries in forest clearing, Kavi holding small basket with wing while rabbit picks berries from low bush, both smiling warmly, gentle afternoon sunlight filtering through green canopy, warm friendly atmosphere, vibrant forest colors, 3D Pixar Disney style, eye-level medium shot showing both characters, soft natural lighting, focus on kindness and friendship, rendered in Unreal Engine, 8K quality

**Leonardo.ai Settings - CRITICAL**:
- ✅ Upload Character Reference: kavi-peacock-reference.png
- ✅ Reference Strength: HIGH (maximum)
- ✅ Verify reference is applied before generating
- Model: Leonardo Phoenix
- Aspect Ratio: 9:16 (576×1024)

**What Changed**:
- Added "MATCH REFERENCE EXACTLY" instruction
- Emphasized character details in parentheses
- Explicit reminder to verify reference strength

---

#### Animation Prompt (MiniMax Hailuo) - SAME AS ORIGINAL
[Original animation prompt unchanged - only image needed refinement]

---

### SCENE 8: Moral Lesson (30 seconds) - REFINED

#### Image Generation Prompt (Leonardo.ai) - SAME AS ORIGINAL
[Original image prompt unchanged]

---

#### Animation Prompt (MiniMax Hailuo) - UPDATED
**Camera**: STATIC shot, minimal camera movement
**Character Action**: Kavi and friends standing together, SLOW gentle breathing animations, subtle head turns, soft smiles, feathers gently rustling in breeze - GENTLE and SLOW movements only
**Background Action**: Light breeze in trees, soft golden hour lighting, peaceful atmosphere
**Duration**: 30 seconds (IMPORTANT: SLOW pacing throughout)
**Movement Style**: CALM, PEACEFUL, CONTEMPLATIVE - avoid fast movements
**Camera Control**: "static wide shot, no zoom, no pan, hold position, slow gentle character animations only, 30 second duration"

**MiniMax Hailuo Settings - CRITICAL**:
- Duration: Set to maximum (30 seconds)
- Camera Movement: NONE or MINIMAL
- Pacing: SLOW (if available in settings)

**What Changed**:
- Changed camera from moving to STATIC
- Emphasized SLOW and GENTLE movements repeatedly
- Explicit duration reminder
- Added camera control instructions to prevent fast pacing

---

### Regeneration Checklist

**For Scene 7** (Image Only):
- [ ] Character reference uploaded and selected
- [ ] Reference strength set to HIGH
- [ ] Prompt emphasizes "MATCH REFERENCE EXACTLY"
- [ ] Preview shows reference is applied
- [ ] Generate 2-3 variations

**For Scene 8** (Animation Only):
- [ ] Use successfully generated Scene 8 image (don't regenerate image)
- [ ] Upload image to MiniMax Hailuo
- [ ] Use REFINED animation prompt above
- [ ] Set duration to 30 seconds
- [ ] Preview/test before finalizing

**Expected Success Rate**: 95%+ after refinement
```

**User Action**: Regenerate Scene 7 (image) and Scene 8 (animation) with refined prompts

---

#### **STEP 8: Generate Assembly Timeline**

**Agent Call**:
```python
youtube_production_manager(
    operation="timeline",
    all_scenes="[Full scenes from Step 3]",
    video_duration=270,  # 4:30 in seconds
    response_format="concise"
)
```

**Expected Output** (~400 tokens):
```markdown
## Video Assembly Timeline

**Total Duration**: 4 minutes 30 seconds (270 seconds)

### Scene-by-Scene Timeline

| Scene | Start Time | Duration | End Time | Transition |
|-------|-----------|----------|----------|------------|
| Scene 1 | 0:00 | 30s | 0:30 | Dissolve (1s) |
| Scene 2 | 0:31 | 25s | 0:56 | Cut (0.5s) |
| Scene 3 | 0:56.5 | 35s | 1:31.5 | Dissolve (1.5s) |
| Scene 4 | 1:33 | 30s | 2:03 | Crossfade (1s) |
| Scene 5 | 2:04 | 25s | 2:29 | Cut (0.5s) |
| Scene 6 | 2:29.5 | 25s | 2:54.5 | Dissolve (1s) |
| Scene 7 | 2:55.5 | 30s | 3:25.5 | Crossfade (1s) |
| Scene 8 | 3:26.5 | 30s | 3:56.5 | Fade to black (3s) |
| **End Credits** | 3:59.5 | 30s | 4:29.5 | |

---

### Audio Layers

#### Layer 1: Video (with scene dialogue)
```
scene_01_animated.mp4 (with dialogue_scene_01.mp3 synced)
scene_02_animated.mp4 (with dialogue_scene_02.mp3 synced)
scene_03_animated.mp4 (with dialogue_scene_03.mp3 synced)
... [continues for all 8 scenes]
```

#### Layer 2: Background Music
```
background_music.mp3 (4:30 duration, continuous)
- Volume: 20% during dialogue
- Volume: 35% during non-dialogue moments
- Fade in: 0:00-0:02 (2 seconds)
- Fade out: 4:27-4:30 (3 seconds)
```

#### Layer 3: Ambience (optional)
```
Village ambience: 0:00-0:56 (Scenes 1-2)
Forest ambience: 0:56-2:29 (Scenes 3-5)
Village ambience: 2:29-4:30 (Scenes 6-8)
Volume: 10-15% (very subtle)
```

---

### FFmpeg Assembly Command

**Step 1: Concatenate Videos**
```bash
# Create input list
cat > scenes.txt << EOF
file 'scene_01_animated.mp4'
file 'scene_02_animated.mp4'
file 'scene_03_animated.mp4'
file 'scene_04_animated.mp4'
file 'scene_05_animated.mp4'
file 'scene_06_animated.mp4'
file 'scene_07_animated.mp4'
file 'scene_08_animated.mp4'
EOF

# Concatenate videos
ffmpeg -f concat -safe 0 -i scenes.txt -c copy video_only.mp4
```

**Step 2: Mix Audio**
```bash
ffmpeg -i video_only.mp4 \
       -i background_music.mp3 \
       -filter_complex "[1:a]volume=0.25[bg];[0:a][bg]amix=inputs=2:duration=first" \
       -c:v copy -c:a aac \
       final_video.mp4
```

**Step 3: Add Transitions (Optional - using MLT framework or video editor)**
- Dissolve transitions between scenes (1-1.5 seconds)
- Fade to black at end (3 seconds)

---

### Alternative: Shotstack API

**JSON Configuration**:
```json
{
  "timeline": {
    "tracks": [
      {
        "clips": [
          {
            "asset": {"type": "video", "src": "scene_01_animated.mp4"},
            "start": 0,
            "length": 30,
            "transition": {"in": "fade", "out": "fade"}
          },
          // ... [repeat for all 8 scenes with transitions]
        ]
      },
      {
        "clips": [
          {
            "asset": {"type": "audio", "src": "background_music.mp3"},
            "start": 0,
            "length": 270,
            "volume": 0.25
          }
        ]
      }
    ]
  },
  "output": {
    "format": "mp4",
    "resolution": "hd",
    "aspectRatio": "9:16",
    "fps": 30
  }
}
```

---

### Final Output Specifications

- **Resolution**: 1080×1920 (9:16 vertical)
- **Frame Rate**: 30fps
- **Audio**: 44.1kHz stereo, AAC codec
- **Video Codec**: H.264
- **Bitrate**: 8-10 Mbps (high quality)
- **File Size**: ~200-300 MB
- **Format**: MP4
- **Duration**: 4:30 (exactly)

---

### Quality Checklist Before Publishing

- [ ] All scene transitions are smooth
- [ ] Background music volume doesn't overpower dialogue
- [ ] No audio clipping or distortion
- [ ] Character looks consistent across all scenes
- [ ] Video plays smoothly without stuttering
- [ ] Aspect ratio is correct (9:16 vertical)
- [ ] Total duration matches expected 4:30
```

**User Action**: Assemble video using FFmpeg or Shotstack

---

#### **STEP 9: Generate YouTube Metadata**

**Agent Call**:
```python
youtube_production_manager(
    operation="metadata",
    all_scenes="[Full scenes from Step 3]",
    character_name="Kavi the Peacock",
    moral_theme="Don't be a blowhard",
    response_format="concise"
)
```

**Expected Output** (~200 tokens):
```markdown
## YouTube Upload Metadata

### Title (Tamil + English for SEO)
```
கவி மயில் கதை: உடையது விளம்பேல் | Kavi the Peacock: Don't Be a Blowhard | Tamil Moral Story
```

**Why This Title**:
- Includes character name (Kavi) for series continuity
- Tamil moral in Tamil script (authentic)
- English translation for broader reach
- "Tamil Moral Story" for SEO

---

### Description
```
Join Kavi the Peacock as he learns an important lesson about humility! When Kavi spends all his time boasting about his beautiful feathers, he discovers that true beauty comes from within. A heartwarming Tamil moral story teaching the timeless wisdom: "உடையது விளம்பேல்" (Don't be a blowhard).

🦚 Story Summary:
Kavi is a young peacock who loves to show off his beautiful feathers. But when his pride is challenged, he learns that kindness and humility are more valuable than appearance.

📚 Moral Lesson:
Don't boast about yourself all the time. True beauty comes from a kind heart and humble character.

🎯 Perfect For:
✅ General audience (family-friendly)
✅ Tamil language learners
✅ Moral education
✅ Character development
✅ Positive values

🎬 Production:
- 3D Pixar-style animation
- Tamil dialogue with English subtitles (optional)
- 4:30 minutes of engaging storytelling

---

Subscribe to KIDZ SEASON TV for more Tamil moral stories with Kavi and friends!

#TamilStories #MoralStories #KaviThePeacock #TamilKids #EducationalVideos #FamilyFriendly #3DAnimation #PixarStyle #TamilMoral #HumilityLesson
```

---

### Tags (15-20 relevant tags)
```
Tamil moral stories
Kavi the Peacock
Tamil kids stories
moral lessons for kids
humility story
உடையது விளம்பேல்
3D animation Tamil
Pixar style stories
educational videos Tamil
family friendly content
Tamil proverbs
character development
positive values
KIDZ SEASON TV
peacock story
animal moral tales
Tamil educational content
kids stories 2025
```

---

### Video Settings

**Category**: Education
**Language**: Tamil
**Made for Kids**: OPTIONAL (your choice - general audience allows broader reach)
**License**: Standard YouTube License
**Allow Embedding**: Yes
**Publish to Subscriptions Feed**: Yes
**Comments**: Enabled (moderate if "Made for Kids" is OFF)

---

### Thumbnail Recommendations

**Option 1**: Use Scene 1 (Kavi showing off)
- Shows main character clearly
- Bright, colorful, eye-catching
- Expressive facial expression

**Option 2**: Use Scene 4 (Kavi with Owl)
- Shows character arc (sad Kavi)
- Creates curiosity ("What happened?")
- Emotionally engaging

**Option 3**: Custom Thumbnail
- Kavi's face (close-up, big eyes)
- Text overlay: "உடையது விளம்பேல்" (Tamil)
- Text overlay: "Don't Be a Blowhard!" (English)
- Bright background (yellow or orange)

**Thumbnail Specifications**:
- Resolution: 1280×720 pixels
- Format: JPG or PNG
- File size: <2MB
- Aspect ratio: 16:9 (even though video is 9:16)

**Recommended Text Overlay**:
```
Top: கவி மயில் கதை (Kavi the Peacock)
Bottom: உடையது விளம்பேல் (Don't Be a Blowhard)
```

---

### End Screen Elements (Last 20 seconds)

**Element 1**: Subscribe button (center)
**Element 2**: Next Kavi episode (if available, right side)
**Element 3**: Best for Viewer playlist (left side)

---

### Publishing Checklist

- [ ] Video file uploaded (final_video.mp4)
- [ ] Title added (Tamil + English)
- [ ] Description complete with emojis and hashtags
- [ ] All 15-20 tags added
- [ ] Thumbnail created and uploaded
- [ ] Category set to Education
- [ ] Language set to Tamil
- [ ] "Made for Kids" decision made (optional)
- [ ] End screen configured
- [ ] Publish time scheduled (or publish immediately)
```

**User Action**: Upload to YouTube with provided metadata

---

#### **STEP 10: Quality Checklist**

**Agent Call**:
```python
youtube_production_manager(
    operation="quality_check",
    all_scenes="[Full scenes from Step 3]",
    response_format="detailed"
)
```

**Expected Output** (~600 tokens):
[Comprehensive QA checklist - Visual, Audio, Content, Technical]

**User Action**: Review video against checklist before publishing

---

## 🎯 Success Metrics for Test

**If this test is successful, you should have**:

1. ✅ **Complete Video Package**:
   - 8 scene images (consistent character)
   - 8 animated videos (smooth transitions)
   - 8 voice audio files (clear Tamil dialogue)
   - 1 background music file (4:30 Suno track)
   - 1 assembled final video (1080×1920 MP4, 4:30)
   - 1 character reference (kavi-peacock-reference.png for future use)

2. ✅ **Workflow Validation**:
   - Agent correctly analyzed idea (Drama recommendation)
   - Agent generated proper scene structure (8 scenes, emotional arc)
   - Agent generated all prompts in ONE call (not 8 separate calls)
   - Agent generated Suno music prompt automatically
   - Agent handled feedback and refined failed scenes
   - Agent provided assembly timeline and YouTube metadata

3. ✅ **Tool Performance**:
   - Token efficiency (concise format: ~5,000 tokens vs detailed: ~10,000)
   - Clear, actionable prompts (user can paste directly)
   - Proper character consistency guidance
   - Helpful error messages (if any failures)

4. ✅ **Ready for Production**:
   - Character reference saved for future Kavi episodes
   - Workflow proven end-to-end
   - User comfortable with manual paste workflow
   - Feedback loop validated (refinement works)

---

## 📝 What Happens After Test

**If successful**:
1. ✅ Planning phase validated
2. ✅ Move to Implementation phase
3. ✅ Build actual tools with Pydantic AI
4. ✅ Create API endpoints (Hybrid approach)
5. ✅ Deploy and test with real API calls

**If issues found**:
1. 🔄 Refine tool specifications
2. 🔄 Adjust prompts or workflow
3. 🔄 Re-test with same idea
4. 🔄 Iterate until workflow is smooth

---

## 🚀 Ready for Your Test

**You can now test with**: "உடையது விளம்பேல் - Don't be a blowhard and keep speaking about yourself at all times"

**I will simulate** each of the 10 steps above and show you exactly what the agent would output at each stage.

**Just say**: "Let's test Step 1" and I'll show you the simulated output for the idea analysis!

Or if you have any questions about the planning, ask away before we test. 🎬
