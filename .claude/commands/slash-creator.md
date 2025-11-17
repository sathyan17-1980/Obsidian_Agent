# Slash Command Creator

**Purpose:** Guide for creating executable slash commands from documentation files
**Status:** Ready for Use
**Date:** 2025-11-17

---

## Overview

This guide explains how to convert documentation markdown files into executable slash commands that can be run within Claude Code.

### What is a Slash Command?

A slash command is a markdown file with YAML frontmatter that provides step-by-step instructions for an AI agent to execute autonomously. It transforms documentation into actionable workflows.

**Key Difference:**
- **Documentation (.md)**: Explains WHAT a feature does, its capabilities, use cases
- **Slash Command (.md)**: Tells an agent HOW to execute the workflow step-by-step

---

## Anatomy of a Slash Command

### 1. YAML Frontmatter (Required)

```yaml
---
description: One-line summary of what this command does
argument-hint: "[required-arg] [--optional-flag value]"
---
```

**Fields:**
- `description`: Brief description shown in command list (keep under 80 chars)
- `argument-hint`: Shows users the expected argument format

### 2. Title and Arguments Section

```markdown
# Command Name

## [Topic/Request/Input]

$ARGUMENTS
```

**The `$ARGUMENTS` variable:**
- Automatically replaced with user's input when command runs
- Use this to capture and parse user arguments
- Always parse arguments in first step

### 3. Step-by-Step Instructions

```markdown
## Step 1: Parse Arguments

Extract from $ARGUMENTS:
- Required parameter 1
- Optional parameter 2 (default: value)
- Flags and options

## Step 2: [Action Name]

Specific instructions:
- File paths to read/write
- Commands to execute
- Validation checks
- Error handling

## Step 3: [Next Action]

More specific instructions...
```

**Best Practices:**
- Number steps sequentially
- Each step should be atomic and actionable
- Include exact file paths and commands
- Specify expected inputs/outputs
- Add validation at each step

### 4. Validation Section

```markdown
## Validation

Verify:
- ✅ Condition 1 met
- ✅ Condition 2 met
- ✅ Output files created
- ✅ Tests passing
```

### 5. Report Results Section

```markdown
## Report Results

Provide summary to user:
- What was accomplished
- Files created/modified
- Next steps
- Any warnings or notes
```

---

## Conversion Process: Documentation → Slash Command

### Documentation File Structure

Typical documentation includes:
- Purpose and overview
- Architecture diagrams
- Feature lists
- Use cases and examples
- Configuration details
- API references
- Troubleshooting

### Slash Command Structure

Convert documentation into:
1. **Argument parsing** - Extract user input and set defaults
2. **Pre-flight checks** - Verify configuration, dependencies
3. **Execution steps** - Ordered, actionable instructions
4. **Validation** - Verify success at each stage
5. **Output formatting** - Structured results for user

### Conversion Examples

#### Documentation Says:
```markdown
## Features

- Searches 6 sources in parallel
- Generates flexible outputs
- Saves to Obsidian vault
```

#### Slash Command Says:
```markdown
## Step 3: Execute Multi-Source Research (Parallel)

Research the topic across 6 sources in parallel:

1. **HackerNews Discussions**
   - Search for relevant HN threads
   - Extract key insights and debates
   - Capture community sentiment

2. **Web Search (Brave API)**
   - Use Brave Search API
   - Number of queries based on depth level
   - Extract high-quality web articles

[Continue for all 6 sources...]

**Performance Target**: Complete all 6 sources in <90 seconds
```

---

## Command Patterns and Templates

### Pattern 1: Simple Single-Step Command

```markdown
---
description: Brief description
argument-hint: "[input]"
---

# Command Name

$ARGUMENTS

## Execute Action

[Specific steps to accomplish task]

## Report Results

[What to tell user]
```

**Use for:** Simple transformations, quick operations

### Pattern 2: Multi-Step Workflow

```markdown
---
description: Brief description
argument-hint: "[input] [--options]"
---

# Command Name

## Parse Arguments

$ARGUMENTS

Extract:
- Parameter 1
- Parameter 2 (default: value)

## Step 1: [First Action]

[Instructions]

## Step 2: [Second Action]

[Instructions]

## Step 3: [Third Action]

[Instructions]

## Validation

[Verify success]

## Report Results

[Summary]
```

**Use for:** Complex workflows with multiple stages

### Pattern 3: Chained Commands

```markdown
---
description: Chain multiple commands together
argument-hint: "[input]"
---

# Meta Command

$ARGUMENTS

## Step 1: Execute First Command

Run: core_commands/first.md

Pass arguments: $ARGUMENTS

## Step 2: Execute Second Command

Run: core_commands/second.md

Use output from Step 1

## Final Summary

[Combine results from all commands]
```

**Use for:** Orchestrating multiple existing commands

### Pattern 4: Research and Generate

```markdown
---
description: Research topic and generate output
argument-hint: "[topic] [--format output-type]"
---

# Research Command

## Parse Arguments

$ARGUMENTS

Extract:
- Topic (required)
- Format (default: summary)
- Depth (default: moderate)

## Step 1: Gather Information

[How to research the topic]
- Source 1
- Source 2
- Source 3

## Step 2: Aggregate Results

[How to combine and deduplicate]

## Step 3: Generate Output

[How to create final output in requested format]

## Step 4: Save Results

[Where and how to save]

## Report Results

[Summary of what was generated]
```

**Use for:** Research and content generation workflows

---

## Best Practices

### DO ✅

1. **Be Specific with Paths**
   ```markdown
   Create file: `src/tools/new_feature/tool.py`
   ```
   NOT: "Create a new tool file"

2. **Provide Exact Commands**
   ```markdown
   Run: `uv run pytest tests/tools/new_feature/ -v`
   ```
   NOT: "Run the tests"

3. **Include Templates and Examples**
   ```markdown
   Generate output in this format:
   ```
   # {Title}

   ## {Section}
   [Content]
   ```
   ```

4. **Set Clear Defaults**
   ```markdown
   - Depth: Research depth (default: "moderate")
   ```

5. **Specify Error Handling**
   ```markdown
   If vault path not found:
   - Prompt user for path
   - Validate path exists
   - Save to config
   ```

6. **Make Steps Atomic**
   Each step should be completable without dependencies on future steps

7. **Include Validation**
   After each major step, verify it succeeded before continuing

### DON'T ❌

1. **Don't Be Vague**
   ❌ "Process the files"
   ✅ "For each .py file in src/tools/, run ruff check"

2. **Don't Skip Argument Parsing**
   ❌ Starting directly with execution
   ✅ Always parse $ARGUMENTS first

3. **Don't Assume Context**
   Remember: Another agent executes this without your conversation history

4. **Don't Mix Documentation and Instructions**
   ❌ "This command is useful for..." (documentation)
   ✅ "Execute the following steps:" (instruction)

5. **Don't Forget Edge Cases**
   Handle missing files, invalid input, configuration errors

6. **Don't Leave Outputs Unspecified**
   Always tell agent what to show user at the end

---

## File Naming Conventions

### Documentation Files
- Descriptive names: `slash-creator.md`, `research-generic-consolidator.md`
- Located in: `.claude/commands/`
- Purpose: Explain features, architecture, use cases

### Slash Command Files
- Action-oriented names: `create-slash-command.md`, `research-generic.md`
- Located in: `.claude/commands/` or `.claude/commands/core_commands/`
- Purpose: Executable instructions for agents

### Relationship
```
documentation.md          →  executable-command.md
research-topic-merged.md  →  (slash command embedded in doc)
slash-creator.md          →  create-slash-command.md
ai-research-agent.md      →  research-topic.md (if separate)
```

---

## Testing Your Slash Command

### 1. Readability Test
Can another person (or agent) execute this without context?
- All paths are explicit
- All commands are exact
- All formats are templated

### 2. Execution Test
Run the command with test input:
```bash
/your-command "test input" --option value
```

Verify:
- Arguments parsed correctly
- All steps execute in order
- Validation catches errors
- Output matches specification

### 3. Edge Case Test
Test with:
- Missing arguments (should use defaults or prompt)
- Invalid input (should handle gracefully)
- Missing dependencies (should check and fail early)

---

## Common Patterns in Existing Commands

### Pattern: Argument Parsing
```markdown
## Step 1: Parse Arguments and Set Defaults

Parse the arguments from: **$ARGUMENTS**

Extract:
- **Parameter1**: Description (REQUIRED)
- **Parameter2**: Description (default: "value")
  - `option1`: Use case 1
  - `option2`: Use case 2
```

### Pattern: Conditional Logic
```markdown
## Step 2: Verify Configuration

Check if CONFIG_VAR is set:
- If set: Use existing value
- If not set: Prompt user for input
- Validate input meets requirements
```

### Pattern: Parallel Execution
```markdown
## Step 3: Execute in Parallel

Run these tasks concurrently:
1. Task A (expected time: 30s)
2. Task B (expected time: 45s)
3. Task C (expected time: 20s)

Wait for all to complete before proceeding.
```

### Pattern: Iterative Processing
```markdown
## Step 4: Process Each Item

For each file in list:
1. Read file content
2. Transform data
3. Validate output
4. Save result

Track progress: {current}/{total} completed
```

### Pattern: Error Recovery
```markdown
## Step 5: Execute with Retry Logic

Attempt operation:
- Try up to 3 times
- Wait 2s between retries
- If all attempts fail: Log error and continue
- If success: Proceed to next step
```

---

## Advanced Features

### Nested Commands

```markdown
## Step 2: Execute Sub-Command

Run planning workflow:

core_commands/planning.md

Pass these arguments: "$FEATURE_NAME"

Capture the output and use for next step.
```

### Dynamic Argument Construction

```markdown
## Step 3: Build Command Arguments

Construct arguments based on user input:
- If format = "report": Add --technical-level advanced
- If depth = "deep": Add --max-sources 50
- Always add: --vault-path {OBSIDIAN_VAULT_PATH}

Final command: /research {topic} {constructed_args}
```

### Conditional Workflows

```markdown
## Step 4: Choose Execution Path

Based on {parameter}:

### If parameter = "quick":
- Use minimal depth
- Skip validation
- Generate summary only

### If parameter = "thorough":
- Use deep depth
- Full validation
- Generate detailed report

### Otherwise:
- Use moderate depth (default)
- Standard validation
- Generate standard output
```

---

## Integration with Core Commands

Your slash command can leverage existing core commands:

### Available Core Commands
- `core_commands/prime.md` - Load codebase context
- `core_commands/planning.md` - Create implementation plans
- `core_commands/execute.md` - Execute implementation plans
- `core_commands/commit.md` - Create git commits

### Integration Example

```markdown
## Step 1: Prime Codebase Understanding

core_commands/prime.md

## Step 2: Create Implementation Plan

core_commands/planning.md

Use arguments: $ARGUMENTS

## Step 3: Execute Plan

core_commands/execute.md

Use plan file from Step 2
```

---

## Validation Checklist

Before finalizing your slash command:

### Structure
- ✅ Has YAML frontmatter with description and argument-hint
- ✅ Uses $ARGUMENTS variable for user input
- ✅ Steps are numbered and sequential
- ✅ Each step has clear, actionable instructions

### Completeness
- ✅ Argument parsing with defaults specified
- ✅ Pre-flight checks for dependencies/config
- ✅ Error handling for common failures
- ✅ Validation after major steps
- ✅ Final results reporting section

### Quality
- ✅ Executable without conversation context
- ✅ All file paths are explicit and absolute
- ✅ All commands are exact (copy-pasteable)
- ✅ Templates provided for outputs
- ✅ Edge cases handled

### Usability
- ✅ Description is clear and under 80 characters
- ✅ Argument hint shows expected format
- ✅ Defaults are sensible
- ✅ Output is user-friendly

---

## Examples from Existing Commands

### Example 1: Simple Command
**File**: `.claude/commands/core_commands/commit.md`
- Parses optional file arguments
- Creates git commit with conventional format
- Single clear workflow

### Example 2: Multi-Step Workflow
**File**: `.claude/commands/core_commands/planning.md`
- Parses feature description
- Researches codebase
- Creates structured plan document
- Multiple validation points

### Example 3: Complex Research Command
**File**: `.claude/commands/research-generic.md`
- Parses topic and multiple options
- Executes parallel research across 6 sources
- Aggregates and resolves conflicts
- Generates flexible output formats
- Saves to structured folders

### Example 4: Meta Command (Chaining)
**File**: `.claude/commands/end-to-end-feature.md`
- Chains 4 core commands together
- Passes arguments between steps
- Tracks progress across all stages

---

## When to Create a Slash Command

### Good Use Cases ✅
- Repetitive multi-step workflows
- Complex operations with many parameters
- Research and content generation tasks
- Development workflows (planning, implementing, testing)
- Integration of multiple tools/commands

### Not Needed ❌
- Single bash commands (just run directly)
- One-time operations
- Highly variable workflows (better as conversation)
- Simple file operations (use Read/Write tools)

---

## Maintenance

### Updating Slash Commands

When updating a slash command:
1. Document changes in git commit message
2. Update description if functionality changed
3. Maintain backward compatibility when possible
4. Update examples if argument format changed
5. Test thoroughly before committing

### Version Control

```markdown
---
description: Command description
argument-hint: "[args]"
version: 1.1.0
last-updated: 2025-11-17
---
```

Consider adding version and last-updated metadata for complex commands.

---

## Resources

### Related Files
- **Core Commands**: `.claude/commands/core_commands/`
- **Example Commands**: `.claude/commands/research-generic.md`
- **Documentation**: `CLAUDE.md` (project coding standards)

### Command Execution
- Commands are executed by Claude Code CLI
- Use `/command-name args` to invoke
- View available commands with `/help`

---

**Status:** ✅ READY FOR USE
**Version:** 1.0
**Date:** 2025-11-17
