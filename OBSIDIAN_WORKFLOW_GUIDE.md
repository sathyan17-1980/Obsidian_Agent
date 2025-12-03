# Obsidian Workflow Guide - Single Command Archival

This guide explains how to automatically save all your generated content to your Obsidian vault with a single command.

---

## Quick Start

### Option 1: Archive Everything (Recommended)
```bash
/obsidian-archive
```

This command will:
- ✅ Find all LinkedIn posts, blog articles, and research files
- ✅ Add platform headers (📱 LinkedIn, 📝 Blog)
- ✅ Save to correct vault locations
- ✅ Create research archive folders
- ✅ Generate summary of what was saved

### Option 2: Save Individual Files
```bash
/obsidian-save [file_path] [content_type] [topic]
```

Example:
```bash
/obsidian-save linkedin_post_draft.md linkedin "Neural Networks Part 1"
```

---

## What Happens Automatically

### 1. Content Detection
The command scans your working directory for:
- `linkedin_post*.md` files
- `blog_post*.md` files
- Any `.md` files with `platform: linkedin` or `platform: blog` in frontmatter

### 2. Platform Organization

**LinkedIn Posts** → `C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\LinkedIn Post\`
- Adds header: `# 📱 LINKEDIN POST - {Topic}`
- Filename: `{topic-slug}.md`
- Example: `neural-networks-part-1.md`

**Blog Articles** → `C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\Blog Post\`
- Adds header: `# 📝 BLOG ARTICLE - {Topic}`
- Filename: `{topic-slug}.md`
- Example: `neural-networks-part-1.md`

**Research Archives** → `C:\Users\sathy\OneDrive\Documents\Obsidian Vault\research\{date}-{topic-slug}\`
- Creates folder structure:
  ```
  research\2025-11-30-neural-networks-part-1\
  ├── research-topic.md
  ├── sources.md
  └── research-summary.md
  ```

### 3. Header Addition
Before saving, the command adds visual headers:

```markdown
# 📱 LINKEDIN POST - Neural Networks Part 1

**Platform:** LinkedIn
**Format:** Social media post (312 words)
**Purpose:** Engagement and professional networking

---

[Your content here...]
```

### 4. Summary Generation
Creates `ARCHIVE_SUMMARY.md` showing:
- All files saved
- Vault locations
- File sizes
- Quick access links

---

## Current Manual Steps (What We Did)

### Step 1: Generate Content
Run research command:
```bash
/research-topic "Neural Networks Part 1" --depth deep --drafts 1
```

This creates in working directory:
- `linkedin_post_part1_draft.md`
- `blog_post_part1_draft.md`

### Step 2: Add Platform Headers (Manual)
Edit each file to add:
```markdown
# 📱 LINKEDIN POST - Neural Networks Part 1
```

### Step 3: Copy to Obsidian (Manual)
```bash
cp linkedin_post_part1_draft.md "C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\LinkedIn Post\neural-networks-part-1.md"
cp blog_post_part1_draft.md "C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\Blog Post\neural-networks-part-1.md"
```

### Step 4: Create Research Archive (Manual)
```bash
mkdir -p "C:\Users\sathy\OneDrive\Documents\Obsidian Vault\research\2025-11-30-neural-networks-part-1"
# Create research-topic.md, sources.md, research-summary.md
```

---

## New Automated Workflow

### Single Command Does Everything:
```bash
/obsidian-archive
```

**Output:**
```
📦 Archiving content to Obsidian vault...

✅ LinkedIn Posts:
  - neural-networks-part-1.md → AI research\LinkedIn Post\ (2.8 KB)
  - neural-networks-part-2.md → AI research\LinkedIn Post\ (3.1 KB)

✅ Blog Articles:
  - neural-networks-part-1.md → AI research\Blog Post\ (12 KB)
  - neural-networks-part-2.md → AI research\Blog Post\ (14 KB)

✅ Research Archive:
  - Created: research\2025-11-30-neural-networks-part-1\
  - Created: research\2025-11-30-neural-networks-part-2\

📊 Summary: 4 content files + 6 research files archived (32 KB total)
📝 Archive summary: ARCHIVE_SUMMARY.md

Done! All content saved to Obsidian vault.
```

---

## Advanced Usage

### Archive with Topic Override
```bash
/obsidian-archive "Deep Learning Fundamentals"
```

### Save Specific File Type
```bash
/obsidian-save my_post.md linkedin "AI Ethics"
/obsidian-save my_article.md blog "Machine Learning Basics"
```

### Handle Duplicates
When file exists, you'll be prompted:
```
⚠️  File already exists: neural-networks-part-1.md
Choose action:
1. Overwrite (backup created)
2. Skip (keep existing)
3. Save as version 2 (neural-networks-part-1-v2.md)
```

---

## File Naming Conventions

The command automatically converts topics to file-friendly slugs:

| Topic                                      | Filename                                   |
|--------------------------------------------|--------------------------------------------|
| "Neural Networks Part 1"                   | `neural-networks-part-1.md`                |
| "Deep Learning: Transformers Explained"    | `deep-learning-transformers-explained.md`  |
| "AI Ethics & Responsible AI"               | `ai-ethics-responsible-ai.md`              |

---

## Configuration

### Default Paths (from .env)
```env
OBSIDIAN_VAULT_PATH=C:\Users\sathy\OneDrive\Documents\Obsidian Vault
LINKEDIN_POST_PATH=C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\LinkedIn Post
BLOG_POST_PATH=C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\Blog Post
```

### Custom Paths (Optional)
Override in `.env`:
```env
OBSIDIAN_LINKEDIN_PATH=custom/path/linkedin
OBSIDIAN_BLOG_PATH=custom/path/blog
OBSIDIAN_RESEARCH_PATH=custom/path/research
```

---

## Troubleshooting

### Command Not Found
If `/obsidian-archive` doesn't work:
1. Check command file exists: `.claude\commands\obsidian-archive.md`
2. Restart Claude Code session
3. Use full path: `/obsidian-archive` (with leading slash)

### Files Not Detected
If command doesn't find your files:
- Ensure files have `.md` extension
- Check files have frontmatter with `platform:` field
- Verify files are in current working directory

### Path Errors
If paths don't exist:
- Check `OBSIDIAN_VAULT_PATH` in `.env`
- Ensure Obsidian vault is at correct location
- Run test: `ls "C:\Users\sathy\OneDrive\Documents\Obsidian Vault"`

---

## Complete Example Workflow

### 1. Generate Content
```bash
/research-topic "Neural Networks Part 2" --depth deep --drafts 1
```

### 2. Review Drafts
Check generated files in working directory:
- `linkedin_post_part2_draft.md`
- `blog_post_part2_draft.md`

### 3. Archive Everything
```bash
/obsidian-archive
```

### 4. Verify in Obsidian
Open Obsidian vault and check:
- `AI research\LinkedIn Post\neural-networks-part-2.md` ✅
- `AI research\Blog Post\neural-networks-part-2.md` ✅
- `research\2025-11-30-neural-networks-part-2\` ✅

### 5. Publish
- Copy LinkedIn post from vault to LinkedIn
- Copy blog article from vault to Medium/blog platform

---

## Benefits of This Workflow

### Before (Manual - 5 steps, ~5 minutes)
1. Generate content with `/research-topic`
2. Manually add headers to each file
3. Copy LinkedIn post to vault folder
4. Copy blog post to vault folder
5. Create research archive folders and files

### After (Automated - 1 command, ~5 seconds)
1. Run `/obsidian-archive`

**Time Saved:** 4 minutes 55 seconds per research session
**Error Reduction:** No manual file copying errors
**Consistency:** All files get proper headers automatically

---

## Next Steps

1. **Test the command:** Run `/obsidian-archive` to archive your Neural Networks content
2. **Review output:** Check ARCHIVE_SUMMARY.md for confirmation
3. **Open Obsidian:** Verify files appear in correct folders
4. **Publish:** Copy content from Obsidian to LinkedIn/blog

---

## Available Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/obsidian-archive` | Archive all content automatically | `/obsidian-archive` |
| `/obsidian-save` | Save individual file | `/obsidian-save file.md linkedin "Topic"` |
| `/research-topic` | Generate research content | `/research-topic "AI Topic" --depth deep` |

---

## Support

If you encounter issues:
1. Check `.env` configuration
2. Verify Obsidian vault path exists
3. Review ARCHIVE_SUMMARY.md for errors
4. Check command files in `.claude\commands\`

---

**Last Updated:** 2025-11-30
**Vault Location:** `C:\Users\sathy\OneDrive\Documents\Obsidian Vault`
