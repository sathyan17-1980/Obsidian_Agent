# Latest Research Commands

This directory contains the latest stable versions of the research commands and their comprehensive help documentation.

**Last Updated:** 2025-11-30

---

## Available Commands

### 1. research-generic
**File:** `research-generic.md`
**Help:** `research-generic-help.md`
**Version:** 2.0
**Purpose:** Multi-source research for any topic with flexible output formats

**Use for:**
- Technical documentation
- Research reports
- Knowledge management
- Objective analysis
- Academic-style outputs

**Output Formats:**
- Summary (default)
- Technical Report
- Q&A Document
- Comparison Analysis
- Beginner's Guide

---

### 2. research-topic
**File:** `research-topic.md`
**Help:** `research-topic-help.md`
**Version:** 2.0
**Purpose:** LinkedIn posts and Blog articles for personal brand building

**Use for:**
- LinkedIn posts (150-300 words)
- Blog articles (800-1500 words)
- Thought leadership content
- Educational series
- Personal branding

**Output:**
- 3 LinkedIn drafts (Technical, Story, Balanced)
- 3 Blog drafts (Technical, Story, Balanced)
- 6 total drafts to choose from

---

## Quick Reference

### When to Use Each

| Situation | Use Command |
|-----------|-------------|
| Need objective research | `research-generic` |
| Building personal brand | `research-topic` |
| Technical documentation | `research-generic --format report` |
| LinkedIn/Blog content | `research-topic` |
| Comparison analysis | `research-generic --format comparison` |
| Educational series | `research-topic` |
| Internal wiki/docs | `research-generic --format summary` |

---

## Quality Frameworks

### research-generic: 21-Point Framework
- Research grounding (5 points)
- Citation quality (5 points)
- Technical depth (4 points)
- Content structure (4 points)
- Quality validation (3 points)

### research-topic: 55-Point Framework
- Personal branding (7 core elements)
- LinkedIn quality (20 points)
- Blog quality (25 points)
- Research quality (21 points)

---

## Research Sources (Both Commands)

Both commands query **6 sources in parallel**:

1. **HackerNews Discussions** - Community insights
2. **Web Search (Brave API)** - High-quality articles
3. **Full Article Content** - Complete text extraction
4. **Obsidian Vault** - Your personal notes (MANDATORY)
5. **Google Drive** - Your documents (optional)
6. **YouTube Transcripts** - Educational videos

**Performance:** <90 seconds for all sources

---

## Common Parameters

### Depth Levels (Both Commands)
- `minimal` - ~60s, 1-3 queries/source, ~$0.10-0.14
- `light` - ~90s, 3-5 queries/source, ~$0.12-0.14
- `moderate` - ~120s, 5-8 queries/source, ~$0.15-0.18 (DEFAULT)
- `deep` - ~180s, 8-12 queries/source, ~$0.18-0.20
- `extensive` - ~240s, 12+ queries/source, ~$0.20-0.22+

### Output Features (Both Commands)
- Professional PDF generation
- Automatic git commit and push
- Organized Obsidian vault storage
- Conflict detection and resolution
- Citation verification
- Source authority ranking

---

## File Structure

```
.claude/commands/latest/
├── README.md                      # This file
├── research-generic.md            # Command specification
├── research-generic-help.md       # Comprehensive help guide
├── research-topic.md              # Command specification
└── research-topic-help.md         # Comprehensive help guide
```

---

## Getting Started

### For First-Time Users

1. **Read the help documents** in this directory
2. **Set up Obsidian vault path:**
   ```bash
   export OBSIDIAN_VAULT_PATH="/path/to/vault"
   ```
3. **Test with a simple query:**
   ```bash
   /research-generic "What is semantic search?" --depth minimal
   ```
4. **Review outputs** in your Obsidian vault

### For research-topic Users

1. **Create voice profile** from 5+ writing samples (5,000+ words)
2. **Test with familiar topic:**
   ```bash
   /research-topic "Why learn embeddings" --depth light --drafts 1
   ```
3. **Review all 6 drafts** and select your favorites
4. **Publish and track engagement**

---

## Prerequisites

### Required for Both
- `OBSIDIAN_VAULT_PATH` environment variable
- `BRAVE_API_KEY_FREE` or `BRAVE_API_KEY_PRO`
- `ANTHROPIC_API_KEY` (or equivalent LLM API)

### Recommended for research-topic
- Voice profile (dramatically improves quality)
- Writing samples (5+, 5,000+ words total)

### Optional for Both
- Google Drive OAuth credentials
- Dependencies: newspaper3k, youtube-transcript-api, weasyprint

---

## Support

### Documentation
- `research-generic-help.md` - Complete guide for generic research
- `research-topic-help.md` - Complete guide for LinkedIn/Blog content
- Command files - Full specifications with all steps

### Related Files
- `research-generic-consolidator.md` - Detailed consolidator docs
- `research-topic-merged.md` - Merged MVP specification
- `brave-api-configuration.md` - API setup guide

---

## Version History

### 2.0 (2025-11-30)
- ✅ Added 21-point quality framework to research-generic
- ✅ Enhanced citation and research standards
- ✅ Format-specific quality applications

### 2.0 (2025-11-19)
- ✅ Added 55-point quality framework to research-topic
- ✅ Enhanced personal branding requirements
- ✅ LinkedIn and blog-specific quality standards

### 1.0 (2025-11-17)
- Initial release of both commands
- 6-source multi-source research
- PDF generation and git integration

---

## Quick Examples

### research-generic Examples

```bash
# Quick fact check
/research-generic "What is RAG?" --depth minimal

# Technical documentation
/research-generic "Vector database internals" --depth deep --format report

# Comparison analysis
/research-generic "RAG vs Fine-tuning" --depth deep --format comparison

# Beginner's guide
/research-generic "Introduction to embeddings" --depth moderate --format guide
```

### research-topic Examples

```bash
# Weekly LinkedIn post
/research-topic "Why learn embeddings" --depth moderate

# Quick social content
/research-topic "What is RAG?" --depth light --drafts 1

# Flagship content
/research-topic "Complete vector database guide" --depth deep --drafts 5

# Series continuation
/research-topic "Vector databases build on embeddings" --depth moderate
```

---

## Key Differences

| Feature | research-generic | research-topic |
|---------|-----------------|----------------|
| **Purpose** | Objective research | Personal branding |
| **Outputs** | 1 in requested format | 6 drafts (3+3) |
| **Formats** | 5 options | LinkedIn + Blog |
| **Voice** | Objective | Personal (voice-matched) |
| **Quality** | 21 points | 55 points |
| **Use Case** | Documentation | Social media |

---

## License

Part of the Obsidian Agent project.
Powered by Brave Search, Claude AI, and open-source tools.

**Maintained by:** Obsidian Agent Team
**Last Updated:** 2025-11-30
