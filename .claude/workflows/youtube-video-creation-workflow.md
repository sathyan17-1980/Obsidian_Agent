# YouTube Kids Video Creation Workflow

## Overview
Complete workflow for creating production-ready YouTube videos for 2-4 year olds using AI tools.

---

## Input Requirements
- **Idea**: Story concept, moral, or theme (can be in Tamil or English)
- **Optional**: Reference image for character continuity in series

---

## Step-by-Step Process

### **STEP 1: Idea Analysis & Copyright Check**

**Objective**: Determine if the idea works better as SONG or DRAMA, and verify no copyright issues.

**Input**: User provides idea (e.g., "உடையது விளம்பேல்" - Don't be a blowhard)

**LLM Analysis** (Claude Sonnet 4.5 recommended):

1. **Song vs Drama Evaluation**:
   - **For Drama**: Evaluate if moral/story has clear character arc, cause-effect relationship, emotional journey
   - **For Song**: Evaluate if moral can be conveyed in simple, repetitive lyrics with catchy melody
   - **Recommendation**: Provide reasoning for both with pros/cons
   - **Age appropriateness**: Confirm suitable for 2-4 yr olds

2. **Copyright Check**:
   - Verify if idea is based on public domain content (proverbs, traditional stories)
   - Check for conflicts with existing copyrighted characters/stories
   - Confirm original elements are unique
   - Declare: CLEAR or POTENTIAL ISSUES (with details)

**Output**:
- Recommendation: Song OR Drama (with reasoning)
- Copyright Status: CLEAR or flagged issues
- **User Decision Required**: User chooses final format

---

### **STEP 2: Content Generation Based on Format**

#### **IF DRAMA:**

##### **2a. Image Prompts (10-12 scenes)**
- Generate detailed image prompts for each scene
- Requirements:
  - **Character consistency**: Same appearance, clothing, personality across all scenes
  - **3D Pixar style**: Vibrant colors, expressive faces, soft lighting
  - **Camera angles**: Specify for each scene (low angle, close-up, wide shot, etc.)
  - **Setting details**: Environment, props, background elements
  - **Mood/Lighting**: Time of day, emotional tone, lighting style
  - **Cultural elements**: If Tamil/Indian content, include appropriate cultural details

##### **2b. Animation Direction (per scene)**
- **Camera movement**: Pan, zoom, dolly, static
- **Character animation**: What actions/movements occur
- **Duration**: MINIMUM 25-45 seconds per scene (see Pacing & Timing section for specifics)
  - **CRITICAL**: Specify "MINIMUM [X] seconds" in animation tool to prevent compression
  - Add direction: "slow pacing", "hold shots longer", "let action play out fully"
- **Transition to next scene**: Fade, cut, dissolve, wipe

##### **2c. Dialogue Generation (Tamil + English)**
- Generate dialogue for **EVERY scene** in BOTH languages
- **CRITICAL**: No silent scenes - every scene must have dialogue or narration
- **User Preference**: Balanced with visual moments (not overly dialogue-heavy)
- Requirements:
  - **Age-appropriate**: Simple vocabulary for 2-4 yr olds
  - **Natural flow**: Conversational, not preachy
  - **Emotional tone**: Match scene mood (excited, sad, thoughtful)
  - **Length**: Keep dialogue short (1-2 sentences per scene max)
  - **Breathing room**: Allow pauses for visual storytelling without constant talking
  - **Tamil quality**: User will rewrite Tamil for authenticity
  - **Visual-heavy scenes**: Add narrator commentary or sound effect descriptions

##### **2d. Voice Direction**
- **Character voices**: Specify voice type (child, elderly, energetic, calm)
- **Emotion tags**: Happy, sad, excited, whispering, dramatic
- **Pacing**: Fast, normal, slow
- **Audio sync notes**: Where dialogue aligns with visuals

---

#### **IF SONG:**

##### **2a. Lyrics (Tamil + English)**
- Simple, repetitive structure
- Rhyming scheme for memorability
- Chorus that reinforces moral
- Age-appropriate vocabulary

##### **2b. Music Prompt (for Suno)**
- Genre: Kids music, nursery rhyme, playful, educational
- Tempo: Upbeat, moderate, slow
- Instruments: Describe desired sound (acoustic, playful piano, gentle guitar)
- Mood: Cheerful, calming, energetic

##### **2c. Image Prompts (3-5 scenes)**
- Simpler than drama (fewer scenes)
- Focus on visual representation of lyrics
- Repetitive visual motifs for chorus

##### **2d. Animation Direction**
- Sync with music beats
- Visual accents on key lyrics
- Looping animations for repetitive parts

---

### **STEP 3: Video Production Flow**

#### **3a. Scene-by-Scene Video Assembly**

For each scene, provide:

1. **Image Generation Prompt**: Paste into Leonardo.ai
   - Use Character Reference feature (upload reference image if series)
   - Set to 9:16 aspect ratio (576×1024 or 768×1344)
   - Generate 2-3 variations per scene

2. **Animation Prompt**: Paste into image-to-video tool
   - **Tool**: MiniMax Hailuo (recommended for kids content, $0.08/sec)
   - **Alternative**: Runway Gen-3 Turbo, Luma Dream Machine
   - **Camera movement**: Specify pan, zoom, dolly, static
   - **Character action**: What the character does
   - **Duration**: MINIMUM 25-45 seconds per scene (see guidelines below)
   - **CRITICAL**: Always include "MINIMUM [X] seconds duration" in prompt
   - **Pacing controls**: "slow pacing", "hold shots longer", "static camera"
   - **Director controls**: "pan down slowly", "gentle dolly zoom", "slow zoom in"

3. **Transition to Next Scene**:
   - Type: Cut, fade, dissolve, wipe
   - Duration: 0.5-1 second
   - Color/effect: Match mood shift

---

#### **3b. Continuity Elements**

**Visual Continuity**:
- Character design consistency (use same reference image)
- Lighting consistency (maintain time of day across scenes)
- Color grading (same warm/cool tone throughout)
- Prop consistency (if character holds item, maintain across scenes)

**Narrative Continuity**:
- Story flow (cause → effect → resolution)
- Character emotional arc (start → change → end)
- Location consistency (if in same place, maintain layout)

**Audio Continuity**:
- Voice consistency (same voice actor/TTS throughout)
- Background music/ambience (fade in/out, don't cut abruptly)
- Sound effects (consistent style - cartoon vs realistic)

---

#### **3c. Pacing & Timing**

**Total Video Duration**: 3-4 minutes (optimal for 2-4 yr olds)

**Scene Duration Guidelines** (UPDATED based on production testing + user preference):
- **Opening scene**: 25-30 seconds (establish character/setting)
- **Middle scenes**: 20-25 seconds each (story progression, keeps audience engaged)
- **Climax scene**: 25-30 seconds (key learning moment, emotional peak)
- **Resolution scene**: 20-25 seconds (moral reinforcement, closure)

**Target for 10-12 scene drama**:
- 10 scenes: 30 + (20×6) + 30 + 25 = ~205-235 seconds (3.4-3.9 minutes)
- 12 scenes: 25 + (20×8) + 30 + 20 = ~215-245 seconds (3.6-4.1 minutes)

**User Preference**: 10-12 shorter scenes (maintains audience interest better than 8 longer scenes)

**Dialogue Pacing**:
- Pause 1-2 seconds after dialogue before next scene
- Allow time for visual action without dialogue
- Don't rush - kids need processing time

---

### **STEP 4: Audio Production**

#### **4a. Voice Generation (for Drama)**

**Tool**: ElevenLabs (English), Azure TTS (Tamil recommended)

**Per Scene**:
1. Dialogue text (from Step 2c)
2. Voice selection:
   - **Main character**: Consistent voice throughout
   - **Supporting characters**: Distinct voices
3. Emotion tags: `[excited]`, `[whispers]`, `[giggles]`, `[dramatic tone]`
4. Generate audio file for each scene

**Alternative**: Murf AI (has kids voices for English)

---

#### **4b. Music Generation (for Song)**

**Tool**: Suno (manual, no API)

1. Paste lyrics + music prompt
2. Generate 2-3 variations
3. Select best version
4. Download audio file

**For Drama Background Music**:
- Use SOUNDRAW API (instrumental only)
- Generate subtle background track
- Keep volume low (don't overpower dialogue)

---

#### **4c. Audio Sync Notes**

For each scene, specify:
- **Dialogue start time**: When voice begins (e.g., "0:02")
- **Background music**: Fade in/out points
- **Sound effects**: Where to add (door open, bird chirp, footsteps)
- **Silence**: Where to pause for visual impact

---

#### **4d. Dual-Language Captions (NEW)**

**User Preference**: Dual-language display (Tamil + English burned into video)

**Format**: On-screen text overlay showing both languages simultaneously

For each scene, provide caption text with:
- **Tamil text**: Original dialogue (top line)
- **English translation**: Below Tamil text (bottom line)
- **Timing**: When captions appear and disappear (synced to dialogue)
- **Positioning**: Bottom third of screen (safe zone for 9:16 vertical video)
- **Styling**:
  - Font: Bold, sans-serif (readable for kids/parents)
  - Background: Semi-transparent black bar behind text
  - Tamil: Larger font size (primary language)
  - English: Slightly smaller font (secondary)

**Example Caption Display**:
```
┌─────────────────────────────────┐
│                                 │
│         [Video Content]         │
│                                 │
│  ┌───────────────────────────┐  │
│  │ பாருங்க! என் அழகான இறகுகளை!│  │
│  │ Look! My beautiful feathers!│  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

**Benefits**:
- Always visible (no viewer toggle needed)
- Accessible to non-Tamil speakers (parents, educators)
- Reinforces language learning (kids see both simultaneously)
- Cultural bridge for bilingual families

**Alternative Formats** (if user changes preference):
- **SRT file**: Separate upload to YouTube (toggleable)
- **VTT**: For web players
- **English-only**: Just English translation

---

### **STEP 5: Video Assembly**

**Tool**: FFmpeg or Shotstack API

**Assembly Order**:
1. Import all animated scene videos (from Step 3)
2. Import all voice audio files (from Step 4)
3. Import background music (if applicable)
4. Import sound effects

**Timeline**:
```
Scene 1 (30s) → Transition (0.5s) → Scene 2 (20s) → Transition (0.5s) → ...
├─ Video: scene1.mp4
├─ Audio: dialogue_scene1.mp3 (0:02-0:08)
└─ Music: background.mp3 (volume: 20%, fade in 0-2s)
```

**Final Output**:
- Resolution: 1080×1920 (9:16 vertical for YouTube Shorts/Kids)
- Frame rate: 30fps
- Audio: 44.1kHz stereo
- Format: MP4 (H.264 video, AAC audio)
- Duration: 2-5 minutes

---

### **STEP 6: Quality Review**

**Visual Check**:
- [ ] Character looks consistent across all scenes
- [ ] No visual glitches or artifacts
- [ ] Colors are vibrant and age-appropriate
- [ ] Text/titles are readable (if any)

**Audio Check**:
- [ ] Dialogue is clear and audible
- [ ] Background music doesn't overpower voice
- [ ] No audio clipping or distortion
- [ ] Proper silence/pauses between scenes

**Content Check**:
- [ ] Moral/message is clear
- [ ] Age-appropriate (no scary/inappropriate content)
- [ ] Story flows logically
- [ ] Ending reinforces positive message

**Technical Check**:
- [ ] Correct aspect ratio (9:16)
- [ ] Duration within target (2-5 minutes)
- [ ] File size appropriate for upload (<2GB)

---

### **STEP 7: YouTube Upload Preparation**

**Metadata**:
- **Title**: "[Character Name]'s [Story Theme] | [Moral] | Tamil Kids Stories"
- **Description**: Story summary, moral lesson, age range
- **Tags**: Tamil kids stories, moral stories, 3D animation, Pixar style, preschool, toddlers
- **Category**: Education
- **Made for Kids**: YES (COPPA compliance)
- **Language**: Tamil or English (primary language)

**Thumbnail**:
- Use Scene 1 or climax scene
- Add text overlay with title (Tamil + English)
- Bright, colorful, clear character face
- 1280×720 resolution

---

## Output Deliverables (Per Video)

### **Files Generated**:
1. `character_reference.png` - Main character design
2. `scene_01.png` through `scene_12.png` - Generated images (10-12 scenes)
3. `scene_01_animated.mp4` through `scene_12_animated.mp4` - Animated scenes
4. `dialogue_scene_01.mp3` through `dialogue_scene_12.mp3` - Voice audio
5. `background_music.mp3` - Background music (if applicable)
6. `final_video.mp4` - Complete assembled video with dual-language captions
7. `thumbnail.jpg` - YouTube thumbnail
8. `captions_dual_language.txt` - Tamil + English caption text with timing (NEW)

### **Documentation**:
1. `storyboard.md` - Scene-by-scene breakdown with timing
2. `dialogue_tamil.txt` - Tamil dialogue (original + rewritten)
3. `dialogue_english.txt` - English dialogue
4. `copyright_clearance.txt` - Copyright check results
5. `production_notes.txt` - Any special instructions or variations

---

## Tools Stack

| Stage | Tool | Purpose | Cost |
|-------|------|---------|------|
| **LLM Orchestration** | Claude Sonnet 4.5 | Idea analysis, prompt generation, dialogue | $3/$15 per M tokens |
| **Image Generation** | Leonardo.ai | 3D Pixar-style images with character reference | $49-299/mo |
| **Image-to-Video** | MiniMax Hailuo | Animate images into video clips | $10-95/mo |
| **Voice (Tamil)** | Azure TTS Neural | High-quality Tamil voice synthesis | Pay-per-use (~$5/mo) |
| **Voice (English)** | Murf AI or ElevenLabs | Kids voices for English dialogue | $52/mo or $11/mo |
| **Music (Song)** | Suno | Custom songs with lyrics (manual) | $10-30/mo |
| **Music (Background)** | SOUNDRAW API | Instrumental background tracks | $200-500/mo |
| **Video Assembly** | FFmpeg or Shotstack | Combine scenes, audio, transitions | Free or $49+/mo |
| **Copyright Check** | Copyleaks + ACRCloud | Validate originality, music rights | $14-610/mo |

---

## Estimated Production Time

**Per 3-minute video** (manual workflow):
- Step 1 (Analysis): 5-10 minutes
- Step 2 (Content generation): 15-20 minutes
- Step 3 (Image generation): 30-45 minutes (8 scenes × 3 variations)
- Step 3 (Animation): 60-90 minutes (8 scenes × 10 seconds)
- Step 4 (Voice generation): 15-20 minutes
- Step 5 (Assembly): 30-45 minutes
- Step 6 (Review/edits): 20-30 minutes

**Total**: 3-4 hours per video (manual)

**With automation** (Pydantic AI + FastAPI pipeline):
- Steps 1-2: 5-10 minutes (automated)
- Steps 3-4: 90-120 minutes (API calls, automated)
- Steps 5-6: 30-45 minutes (semi-automated)

**Total**: 2-2.5 hours per video (60% time savings)

---

## Quality Standards

**Visual**:
- Minimum 1080p resolution
- Smooth animations (no flickering)
- Vibrant, saturated colors
- Clear character expressions

**Audio**:
- Clear dialogue (no background noise)
- Balanced audio levels
- Appropriate pacing for 2-4 yr olds

**Content**:
- Positive, educational messages
- Age-appropriate themes
- Culturally authentic (for Tamil content)
- No violence, scary content, or inappropriate themes

---

## Compliance Requirements

**YouTube Kids**:
- Mark as "Made for Kids"
- No personalized ads
- Comments disabled automatically
- No external links in description

**COPPA (Children's Online Privacy Protection Act)**:
- No data collection from children <13
- No behavioral advertising
- Proper content designation

**Copyright**:
- All music properly licensed
- Original characters and stories
- No use of copyrighted materials without permission
- Document all copyright clearances

---

## Version History

- v1.0 (2025-01-27): Initial workflow documentation
- v1.1 (2025-01-27): Updated based on production testing and user preferences
  - **Scene structure**: 10-12 shorter scenes (was 6-8) to maintain audience interest
  - **Scene durations**: 25-30s opening, 20-25s middle, 25-30s climax, 20-25s resolution
  - **Target video duration**: 3-4 minutes (210-240 seconds)
  - Added explicit "MINIMUM duration" requirements for animation prompts
  - Required dialogue for ALL scenes (no silent scenes)
  - **Dialogue style**: Balanced with visual moments (user preference)
  - **Captions**: Dual-language display (Tamil + English burned into video)
  - Added pacing controls ("slow pacing", "hold shots longer")
