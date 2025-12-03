# Add to Obsidian - Import Existing Documents

You are tasked with adding existing documents from the working directory to the user's Obsidian vault.

## Context

The user has existing markdown files they want to organize into their Obsidian vault:
- **Vault Root:** `C:\Users\sathy\OneDrive\Documents\Obsidian Vault`
- **Research:** `{vault}\research\`
- **Notes:** `{vault}\` (root)
- **LinkedIn:** `{vault}\AI research\LinkedIn Post\`
- **Blog:** `{vault}\AI research\Blog Post\`

## Command Usage

```bash
/add-to-obsidian [file1.md] [file2.md] ... [--type TYPE] [--folder FOLDER]
```

**Parameters:**
- Files: One or more markdown files to add (required)
- `--type`: Content type: `linkedin`, `blog`, `research`, `note` (optional, auto-detect if not provided)
- `--folder`: Custom folder within vault (optional)

## Behavior

### Auto-Detection Mode (Recommended)
When user just provides filenames without `--type`:

```bash
/add-to-obsidian linkedin_draft.md blog_draft.md
```

**You will:**
1. Read each file
2. Check frontmatter for `platform:` field
3. Check filename patterns (`linkedin_`, `blog_`, etc.)
4. Check content for indicators (hashtags, word count, structure)
5. Ask user to confirm detected type before saving

### Explicit Type Mode
When user provides `--type`:

```bash
/add-to-obsidian AI_Music_Generation_API_Research_Report.md --type research
```

**You will:**
1. Read the file
2. Add appropriate header based on type
3. Save to correct vault location
4. Confirm completion

### Custom Folder Mode
When user provides `--folder`:

```bash
/add-to-obsidian christmas-song-ring-the-magic-bells-complete.md --folder "Creative Projects"
```

**You will:**
1. Create folder if it doesn't exist: `{vault}\Creative Projects\`
2. Save file there with basic note formatting
3. Add frontmatter with date and tags

## Content Type Detection

### LinkedIn Post Indicators:
- Filename starts with `linkedin_`
- Frontmatter: `platform: linkedin`
- Word count: 150-500 words
- Contains hashtags like `#AI #MachineLearning`
- Conversational tone, personal anecdotes

### Blog Article Indicators:
- Filename starts with `blog_`
- Frontmatter: `platform: blog`
- Word count: 800-2000+ words
- Has sections with `##` headers
- Has references/citations section
- SEO-optimized structure

### Research Report Indicators:
- Filename contains `Research_Report`, `_research`, `_analysis`
- Contains "References", "Sources", "Bibliography"
- Has structured sections (Executive Summary, Findings, etc.)
- Citations with URLs

### General Note Indicators:
- None of the above patterns
- Generic content
- Documentation, guides, project files

## Adding Different Types

### Adding LinkedIn Posts
**Destination:** `AI research\LinkedIn Post\{filename}.md`

**Processing:**
1. Read file content
2. Add header:
```markdown
# 📱 LINKEDIN POST - {Extracted Topic}

**Platform:** LinkedIn
**Format:** Social media post ({word_count} words)
**Purpose:** Engagement and professional networking

---
```
3. Preserve existing frontmatter
4. Save to LinkedIn folder

### Adding Blog Articles
**Destination:** `AI research\Blog Post\{filename}.md`

**Processing:**
1. Read file content
2. Add header:
```markdown
# 📝 BLOG ARTICLE - {Extracted Topic}

**Platform:** Blog/Medium/Personal Website
**Format:** Long-form article ({word_count} words)
**Purpose:** In-depth educational content with SEO optimization

---
```
3. Preserve existing frontmatter and structure
4. Save to Blog folder

### Adding Research Reports
**Destination:** `research\{date}-{topic-slug}\{filename}.md`

**Processing:**
1. Read file content
2. Extract topic from title or filename
3. Create dated folder: `research\2025-11-30-{topic}\`
4. Save report in folder
5. Optionally generate companion files:
   - `research-summary.md` (extract executive summary)
   - `sources.md` (extract references)

### Adding General Notes
**Destination:** `{vault}\{filename}.md` or `{vault}\{custom-folder}\{filename}.md`

**Processing:**
1. Read file content
2. Add minimal frontmatter if missing:
```yaml
---
created: 2025-11-30
tags: [imported]
---
```
3. Save to vault root or custom folder

## Interactive Mode

When auto-detection is uncertain, prompt user:

```
📄 Analyzing: AI_Music_Generation_API_Research_Report.md

Detected characteristics:
- Word count: 3,450 words
- Has References section
- Structured with Executive Summary
- Filename contains "Research_Report"

Suggested type: Research Report
Suggested location: research\2025-11-30-ai-music-generation\

Is this correct? [Yes/No/Custom]
```

## Batch Processing

When multiple files provided:

```bash
/add-to-obsidian *.md --type note --folder "Imported Documents"
```

**You will:**
1. List all files to be processed (confirm count)
2. Ask for confirmation before batch import
3. Process each file
4. Show progress: "Processing 3/15: blog_draft.md..."
5. Generate summary at end

## Examples

### Example 1: Add with auto-detection
```bash
/add-to-obsidian linkedin_draft.md
```

**Output:**
```
📄 Analyzing linkedin_draft.md...
✅ Detected: LinkedIn Post
📊 Word count: 287 words
💾 Saving to: AI research\LinkedIn Post\linkedin-draft.md

✅ Added to Obsidian vault!
📍 Location: AI research\LinkedIn Post\linkedin-draft.md
```

### Example 2: Add research report
```bash
/add-to-obsidian AI_Video_Creation_Research_Report.md --type research
```

**Output:**
```
📄 Processing AI_Video_Creation_Research_Report.md...
📁 Creating: research\2025-11-30-ai-video-creation\
💾 Saving report...

✅ Research report added!
📍 Location: research\2025-11-30-ai-video-creation\
   ├── AI_Video_Creation_Research_Report.md
   └── research-summary.md (generated)
```

### Example 3: Add to custom folder
```bash
/add-to-obsidian christmas-song-ring-the-magic-bells-complete.md --folder "Creative Projects"
```

**Output:**
```
📄 Processing christmas-song-ring-the-magic-bells-complete.md...
📁 Creating folder: Creative Projects\
💾 Saving as note...

✅ Note added!
📍 Location: Creative Projects\christmas-song-ring-the-magic-bells-complete.md
```

### Example 4: Batch add multiple files
```bash
/add-to-obsidian blog_draft.md linkedin_draft.md blog_draft_voice_matched.md
```

**Output:**
```
📦 Batch processing 3 files...

✅ blog_draft.md → AI research\Blog Post\ (1,245 words)
✅ linkedin_draft.md → AI research\LinkedIn Post\ (298 words)
✅ blog_draft_voice_matched.md → AI research\Blog Post\ (1,312 words)

📊 Summary: 3 files added (2.8 KB total)
```

## Smart Features

### Duplicate Handling
If file already exists in vault:
```
⚠️  File already exists: linkedin-draft.md

Options:
1. Overwrite (backup existing as .backup)
2. Skip (keep existing)
3. Save as new version (linkedin-draft-v2.md)
4. Compare and merge

Your choice: [1/2/3/4]
```

### Topic Extraction
Automatically extract topic from:
- File's `# Title` (first H1 heading)
- Frontmatter `topic:` or `title:` field
- Filename (convert `AI_Music_Generation` → "AI Music Generation")

### Tag Extraction
- Extract hashtags from LinkedIn posts → add to tags
- Extract keywords from blog posts → suggest tags
- Allow user to add custom tags during import

### Metadata Enrichment
Add useful metadata when importing:
```yaml
---
imported: 2025-11-30
source: working-directory
original_filename: AI_Music_Generation_API_Research_Report.md
word_count: 3450
tags: [ai, music, api, research]
---
```

## Error Handling

### File Not Found
```
❌ Error: linkedin_draft.md not found
💡 Tip: Use tab completion or `ls *.md` to see available files
```

### Vault Path Invalid
```
❌ Error: Obsidian vault not found at configured path
💡 Check OBSIDIAN_VAULT_PATH in .env file
```

### No Files Matched
```
❌ Error: No .md files found matching pattern
💡 Current directory: C:\Users\sathy\Downloads\AI Mastery\Obsidian-Agent-Post
```

## Success Summary

After completion, always show:
```
✅ Import Complete!

Files added: 3
Total size: 28 KB
Vault location: C:\Users\sathy\OneDrive\Documents\Obsidian Vault

Quick access:
- LinkedIn Posts: AI research\LinkedIn Post\
- Blog Articles: AI research\Blog Post\
- Research: research\

🎯 Next steps:
1. Open Obsidian to verify
2. Review imported content
3. Add additional tags if needed
```

## Configuration

Read from `.env`:
```env
OBSIDIAN_VAULT_PATH=C:\Users\sathy\OneDrive\Documents\Obsidian Vault
OBSIDIAN_AUTO_DETECT=true
OBSIDIAN_ADD_METADATA=true
OBSIDIAN_BACKUP_EXISTING=true
```

## Important Notes

- Always preserve existing frontmatter
- Add headers AFTER frontmatter, before content
- Create backups before overwriting
- Use UTF-8 encoding for Windows compatibility
- Support both absolute and relative file paths
- Maintain file modification timestamps when possible
