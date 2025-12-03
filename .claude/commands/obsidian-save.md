# Obsidian Save Command

You are tasked with saving generated content to the user's Obsidian vault with proper organization and metadata.

## Context

The user has configured:
- **Obsidian Vault Path:** `C:\Users\sathy\OneDrive\Documents\Obsidian Vault`
- **LinkedIn Post Path:** `C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\LinkedIn Post`
- **Blog Post Path:** `C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\Blog Post`
- **Research Archive Path:** `C:\Users\sathy\OneDrive\Documents\Obsidian Vault\research`

## Task

When the user invokes `/obsidian-save [file_path] [content_type] [topic]`, you must:

### 1. Validate Input
- `file_path`: Path to the file to save (required)
- `content_type`: One of: `linkedin`, `blog`, `research`, `note` (required)
- `topic`: Topic name for research organization (optional, auto-detect if not provided)

### 2. Determine Save Location

**For LinkedIn posts (`content_type=linkedin`):**
- Save to: `C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\LinkedIn Post\`
- Filename format: `{topic-slug}.md` (e.g., `neural-networks-part-1.md`)
- Add header: `# 📱 LINKEDIN POST - {Topic}` with platform metadata

**For Blog posts (`content_type=blog`):**
- Save to: `C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\Blog Post\`
- Filename format: `{topic-slug}.md`
- Add header: `# 📝 BLOG ARTICLE - {Topic}` with platform metadata

**For Research archives (`content_type=research`):**
- Save to: `C:\Users\sathy\OneDrive\Documents\Obsidian Vault\research\{date}-{topic-slug}\`
- Create folder structure with:
  - `research-topic.md` (metadata)
  - `sources.md` (citations)
  - `research-summary.md` (synthesis)

**For General notes (`content_type=note`):**
- Save to: `C:\Users\sathy\OneDrive\Documents\Obsidian Vault\{topic-slug}.md`
- Add basic frontmatter with date and tags

### 3. Add Platform Headers

For LinkedIn and Blog content, ensure files start with:

```markdown
# {EMOJI} {PLATFORM} - {Topic}

**Platform:** {Platform Name}
**Format:** {Format Description}
**Purpose:** {Purpose Description}

---
```

### 4. Create Directory Structure

- Use `mkdir -p` to create directories if they don't exist
- Organize research files by date: `YYYY-MM-DD-{topic-slug}`

### 5. Confirmation

After saving, provide:
- Full path where file was saved
- File size
- Confirmation message
- Quick preview of first few lines

## Examples

### Example 1: Save LinkedIn post
```
User: /obsidian-save linkedin_post_draft.md linkedin "Neural Networks Part 1"
Assistant:
- Reads linkedin_post_draft.md
- Adds header: # 📱 LINKEDIN POST - Neural Networks Part 1
- Saves to: C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\LinkedIn Post\neural-networks-part-1.md
- Confirms: "✅ Saved to Obsidian vault (2.8 KB)"
```

### Example 2: Save blog article
```
User: /obsidian-save blog_draft.md blog "Deep Learning Fundamentals"
Assistant:
- Reads blog_draft.md
- Adds header: # 📝 BLOG ARTICLE - Deep Learning Fundamentals
- Saves to: C:\Users\sathy\OneDrive\Documents\Obsidian Vault\AI research\Blog Post\deep-learning-fundamentals.md
- Confirms: "✅ Saved to Obsidian vault (12 KB)"
```

### Example 3: Auto-detect and save multiple files
```
User: /obsidian-save linkedin_post.md blog_post.md
Assistant:
- Detects content types from file content and frontmatter
- Saves linkedin_post.md to LinkedIn Post folder
- Saves blog_post.md to Blog Post folder
- Confirms both saves
```

## Important Notes

- Always preserve existing frontmatter metadata
- Add platform headers AFTER frontmatter, before content
- Use UTF-8 encoding for Windows compatibility
- Create backup if file already exists (append `.backup-{timestamp}`)
- Verify paths exist before writing
- Support both absolute and relative paths for input files
