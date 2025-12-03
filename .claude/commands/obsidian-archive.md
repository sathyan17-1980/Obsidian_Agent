# Obsidian Archive Command - Complete Workflow

You are tasked with archiving ALL generated content from a research session into the user's Obsidian vault with full organization.

## Context

The user generates content (LinkedIn posts, blog articles, research) in the working directory and wants everything automatically organized into their Obsidian vault.

**Vault Configuration:**
- **Vault Root:** `C:\Users\sathy\OneDrive\Documents\Obsidian Vault`
- **LinkedIn:** `{vault}\AI research\LinkedIn Post`
- **Blog:** `{vault}\AI research\Blog Post`
- **Research:** `{vault}\research\{date}-{topic-slug}`

## Command Usage

```
/obsidian-archive [topic]
```

**Parameters:**
- `topic` (optional): Topic name for organization. If not provided, auto-detect from file frontmatter.

## What This Command Does

This command performs a COMPLETE archival workflow:

### Step 1: Scan Working Directory
- Find all `.md` files in current directory matching patterns:
  - `linkedin_post*.md`
  - `blog_post*.md`
  - `*_draft*.md`
  - Files with frontmatter containing `platform: linkedin` or `platform: blog`

### Step 2: Auto-Detect Content Types
For each file found:
- Read frontmatter metadata
- Detect platform from `platform:` field
- Extract topic from `topic:` field
- Identify if it's Part 1, Part 2, etc.

### Step 3: Organize by Platform

**LinkedIn Posts:**
- Add platform header: `# 📱 LINKEDIN POST - {Topic}`
- Copy to: `{vault}\AI research\LinkedIn Post\{topic-slug}.md`
- Preserve frontmatter and add metadata section

**Blog Articles:**
- Add platform header: `# 📝 BLOG ARTICLE - {Topic}`
- Copy to: `{vault}\AI research\Blog Post\{topic-slug}.md`
- Preserve frontmatter and add metadata section

**Research Files:**
- Create folder: `{vault}\research\{date}-{topic-slug}`
- Generate `research-topic.md` with metadata
- Generate `sources.md` if citations found
- Generate `research-summary.md` with synthesis

### Step 4: Create Research Archive
If research metadata files exist (sources.md, research-summary.md), archive them:
- Create dated research folder
- Move all research metadata files
- Create index linking to LinkedIn and Blog posts

### Step 5: Generate Summary
Create `ARCHIVE_SUMMARY.md` in working directory with:
- List of all files archived
- Vault locations for each file
- File sizes and word counts
- Quick access links

### Step 6: Optional Cleanup
Ask user if they want to:
- Keep original draft files in working directory
- Move them to `_archived/` subdirectory
- Delete them (with confirmation)

## Example Output

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
    ├── research-topic.md
    ├── sources.md (35 citations)
    └── research-summary.md
  - Created: research\2025-11-30-neural-networks-part-2\
    ├── research-topic.md
    ├── sources.md (30 citations)
    └── research-summary.md

📊 Summary: 4 content files + 6 research files archived (32 KB total)
📝 Archive summary saved to: ARCHIVE_SUMMARY.md

🗑️  Clean up draft files? [Keep/Archive/Delete]
```

## Advanced Features

### Multi-Part Series Detection
- Automatically detect "Part 1", "Part 2" in titles
- Maintain series continuity in research archive
- Link parts together in research metadata

### Duplicate Detection
- Check if file already exists in vault
- Compare content to detect if it's truly a duplicate
- Offer options:
  - Overwrite (with backup)
  - Skip (keep existing)
  - Save as new version (append `-v2`, `-v3`)

### Citation Management
- Extract all citations from blog posts
- Generate consolidated bibliography
- Add citation count to research metadata

### Tag Extraction
- Extract hashtags from LinkedIn posts
- Add as tags to frontmatter
- Create tag index in research archive

## Implementation Steps

When user runs `/obsidian-archive`:

1. **Scan**: Use `ls *.md` and `grep` to find all markdown files
2. **Parse**: Read each file and extract frontmatter
3. **Classify**: Determine content type (linkedin, blog, research)
4. **Prepare**: Add platform headers, organize by type
5. **Create Directories**: Use `mkdir -p` for all target paths
6. **Copy Files**: Use `cp` to move files to vault locations
7. **Generate Metadata**: Create research metadata files
8. **Summarize**: Generate ARCHIVE_SUMMARY.md
9. **Cleanup**: Prompt user for draft file cleanup preference

## Error Handling

- If vault path doesn't exist: Error with clear message
- If file already exists: Prompt for overwrite/skip/version
- If frontmatter missing: Try to detect from filename
- If can't determine type: Ask user for clarification

## Configuration Override

User can override default paths by setting in `.env`:
```env
OBSIDIAN_LINKEDIN_PATH=custom/path/linkedin
OBSIDIAN_BLOG_PATH=custom/path/blog
OBSIDIAN_RESEARCH_PATH=custom/path/research
```

## Success Criteria

After running `/obsidian-archive`, the user should:
- ✅ See all content organized in their Obsidian vault
- ✅ Have clear visual indicators (📱 LinkedIn, 📝 Blog)
- ✅ Have complete research archives with metadata
- ✅ Know exactly where everything was saved
- ✅ Be able to immediately publish from Obsidian vault
