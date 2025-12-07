---
description: Create an executable slash command from a documentation markdown file
argument-hint: "[path-to-documentation.md] [--output command-name.md]"
---

# Create Slash Command from Documentation

## Documentation File Path

$ARGUMENTS

---

## Your Task

Convert a documentation markdown file into an executable slash command that can be run autonomously by an AI agent.

### Step 1: Parse Arguments

Parse the arguments from: **$ARGUMENTS**

Extract:
- **Documentation File Path** (REQUIRED): Path to the source .md documentation file
- **Output File Name** (OPTIONAL): Name for the slash command file
  - If not provided: Auto-generate from documentation filename
  - Format: Convert `feature-name-docs.md` → `feature-name.md`
  - Remove suffixes like: `-docs`, `-documentation`, `-consolidator`, `-spec`

Example argument formats:
```
.claude/commands/my-feature-docs.md
.claude/commands/research-consolidator.md --output research.md
docs/workflow-spec.md --output execute-workflow.md
```

### Step 2: Read and Analyze Documentation

Read the documentation file specified in Step 1.

Analyze the documentation to identify:
1. **Core Purpose**: What does this feature/workflow do?
2. **Input Parameters**: What arguments does it need from users?
3. **Execution Steps**: What are the key stages of the workflow?
4. **Output Format**: What should the final result look like?
5. **Dependencies**: What tools, APIs, or configurations are required?
6. **Validation Criteria**: How to verify success?

### Step 3: Extract Key Information

From the documentation, extract:

#### Purpose and Description
- One-line description (for YAML frontmatter)
- Primary use case
- Key differentiators from other commands

#### Arguments and Options
- Required parameters
- Optional parameters with defaults
- Flags and their meanings
- Argument format examples

#### Workflow Steps
- Pre-flight checks (config, dependencies)
- Main execution stages
- Post-processing tasks
- Error handling approaches

#### Output Specifications
- What gets generated
- Where it gets saved
- Format templates
- Success metrics

### Step 4: Design the Slash Command Structure

Based on the analysis, design the command structure:

1. **YAML Frontmatter**
   ```yaml
   ---
   description: [One-line summary under 80 chars]
   argument-hint: "[required] [--optional value]"
   ---
   ```

2. **Title and Argument Section**
   ```markdown
   # [Command Name]

   ## [Topic/Input/Request]

   $ARGUMENTS
   ```

3. **Step-by-Step Instructions**
   - Step 1: Parse Arguments and Set Defaults
   - Step 2: Verify Prerequisites
   - Step 3-N: Execute Workflow Stages
   - Step N+1: Validate Results
   - Step N+2: Report Results

### Step 5: Transform Documentation into Instructions

Convert each documentation section into actionable steps:

#### Documentation Pattern → Instruction Pattern

**Documentation Says:**
```markdown
## Features
- Multi-source research
- Conflict detection
- Citation verification
```

**Slash Command Says:**
```markdown
## Step 3: Execute Multi-Source Research

Research the topic across 6 sources in parallel:

1. **Source A**
   - Action to take
   - Data to extract
   - Expected outcome

2. **Source B**
   - Action to take
   - Data to extract
   - Expected outcome

**Performance Target**: [time/quality metric]
```

#### Key Transformations

1. **Feature Lists** → **Execution Steps**
   - FROM: "Searches 6 sources"
   - TO: "Step 3: Execute search across these 6 sources: [list with specific actions]"

2. **Use Cases** → **Conditional Logic**
   - FROM: "Use Case 1: Quick research"
   - TO: "If depth='minimal': Execute quick research workflow [specific steps]"

3. **Configuration** → **Pre-flight Checks**
   - FROM: "Requires OBSIDIAN_VAULT_PATH"
   - TO: "Step 2: Verify OBSIDIAN_VAULT_PATH is configured. If not: prompt user and save."

4. **Output Examples** → **Templates**
   - FROM: "Generates research summary"
   - TO: "Generate output using this template: [exact markdown template]"

5. **Architecture Diagrams** → **Workflow Steps**
   - FROM: Flowchart showing components
   - TO: Sequential steps that implement the flow

### Step 6: Add Argument Parsing Logic

Create detailed argument parsing section:

```markdown
## Step 1: Parse Arguments and Set Defaults

Parse the arguments from: **$ARGUMENTS**

Extract:
- **Parameter1**: Description (REQUIRED)
  - Example: "research topic", "file path"
  - Validation: Not empty, meets format requirements

- **Parameter2**: Description (default: "value")
  - `option1`: When to use option 1 (~metrics, cost)
  - `option2`: When to use option 2 (~metrics, cost)
  - `option3`: When to use option 3 (~metrics, cost)
  - Default choice: option2 (explain why)

- **Flag1**: Boolean flag (default: false)
  - When to enable: [specific use case]
  - Impact: [what changes when enabled]

Example valid inputs:
```
/command "required value"
/command "required value" --parameter2 option1
/command "required value" --parameter2 option3 --flag1
```
```

### Step 7: Create Executable Steps

For each major stage in the workflow, create explicit instructions:

#### Template for Each Step:

```markdown
## Step [N]: [Action Name]

[Brief description of what this step accomplishes]

### Actions:

1. **Sub-action 1**
   - Specific instruction
   - File path or command to execute
   - Expected result

2. **Sub-action 2**
   - Specific instruction
   - Data to process
   - Validation check

### Validation:
- ✅ Check condition 1
- ✅ Check condition 2
- ✅ Verify output exists

### Error Handling:
- If error X: Do Y
- If error Z: Do W

### Performance Target:
[Time, resource usage, or quality metric]
```

### Step 8: Add Output Templates

Include exact templates for all outputs:

```markdown
## Step [N]: Generate Output

Create output in the following format:

```markdown
# {Title}

## {Section 1}
{Content with {variables}}

## {Section 2}
{More content}

### {Subsection}
- {List item 1}
- {List item 2}

## {Final Section}
{Conclusion}
```

**Quality Requirements:**
- Requirement 1 (specific metric)
- Requirement 2 (validation criteria)
- Requirement 3 (format standard)
```

### Step 9: Add Validation and Reporting

Create comprehensive validation section:

```markdown
## Validation

Before marking complete, verify:
- ✅ All required inputs were processed
- ✅ All outputs were generated
- ✅ Files saved to correct locations
- ✅ Format matches specifications
- ✅ Quality metrics met:
  - Metric 1: [threshold]
  - Metric 2: [threshold]
- ✅ No errors or warnings
```

And reporting section:

```markdown
## Report Results

Provide summary to user:

```markdown
## ✅ [Command Name] Complete

**Input**: {summarize input}
**Output**: {summarize output}

**Generated Files**:
- `{path/to/file1}` - {description}
- `{path/to/file2}` - {description}

**Metrics**:
- Metric 1: {value}
- Metric 2: {value}
- Execution Time: {duration}
- Estimated Cost: ${cost}

**Next Steps**:
- {Action user can take}
- {Another option}
```
```

### Step 10: Write the Slash Command File

Combine all sections into a complete slash command:

1. **YAML Frontmatter** (from Step 4)
2. **Title and $ARGUMENTS** (from Step 4)
3. **Argument Parsing** (from Step 6)
4. **Execution Steps** (from Step 7)
5. **Output Templates** (from Step 8)
6. **Validation** (from Step 9)
7. **Reporting** (from Step 9)

**Additional Sections to Include:**

```markdown
## Important Notes

### [Topic 1]
- Key point about usage
- Warning or limitation
- Best practice

### [Topic 2]
- More guidance
- Performance considerations
- Cost implications

## Common Pitfalls to Avoid

- ❌ Anti-pattern 1 (explain why bad)
  - ✅ Correct approach instead

- ❌ Anti-pattern 2 (explain why bad)
  - ✅ Correct approach instead

## References

- **Full Documentation**: [path to source doc]
- **Related Commands**: [other relevant commands]
- **External Resources**: [links if applicable]
```

### Step 11: Determine Output File Path

Calculate the output file path:

1. If `--output` was specified in arguments:
   - Use that filename
   - Ensure it ends with `.md`
   - Path: `.claude/commands/{output-name}.md`

2. If not specified:
   - Take source filename
   - Remove common suffixes: `-docs`, `-documentation`, `-consolidator`, `-spec`, `-guide`
   - Keep descriptive part
   - Path: `.claude/commands/{cleaned-name}.md`

Examples:
```
research-consolidator-docs.md → research-consolidator.md
feature-specification.md → feature.md
workflow-guide.md → workflow.md
api-documentation.md → api.md
```

3. Verify output path:
   - Check if file already exists
   - If exists: Ask user to confirm overwrite
   - Create path if needed

### Step 12: Save the Slash Command

Write the complete slash command to the calculated path.

**File Path**: `.claude/commands/{output-name}.md`

**Content**: Complete slash command from Step 10

### Step 13: Validate the Generated Command

Review the generated slash command to ensure:

1. **Structure Completeness**
   - ✅ YAML frontmatter present and correct
   - ✅ $ARGUMENTS variable used
   - ✅ All steps numbered sequentially
   - ✅ Validation section included
   - ✅ Reporting section included

2. **Actionability Test**
   - ✅ Another agent could execute without context
   - ✅ All file paths are explicit
   - ✅ All commands are exact
   - ✅ All templates are complete
   - ✅ Error handling specified

3. **Completeness Test**
   - ✅ All major features from docs covered
   - ✅ All parameters documented
   - ✅ All edge cases handled
   - ✅ Examples provided

4. **Quality Test**
   - ✅ Description clear and under 80 chars
   - ✅ Argument hint shows correct format
   - ✅ Instructions are specific, not vague
   - ✅ Defaults make sense
   - ✅ Performance targets specified

### Step 14: Report Results

Provide comprehensive summary:

```markdown
## ✅ Slash Command Created

**Source Documentation**: {source-file-path}
**Generated Command**: `.claude/commands/{output-name}.md`

### Command Details

**Description**: {description from YAML}
**Arguments**: {argument-hint from YAML}

**Usage Examples**:
```bash
/{command-name} "example input"
/{command-name} "example input" --option value
/{command-name} "example input" --option1 val1 --option2 val2
```

### What Was Generated

**Sections Created**:
1. ✅ YAML frontmatter with description and argument hint
2. ✅ Argument parsing with defaults
3. ✅ {N} execution steps
4. ✅ Output templates
5. ✅ Validation criteria
6. ✅ Results reporting
7. ✅ Important notes and pitfalls
8. ✅ References to source docs

**Key Features Implemented**:
- {Feature 1 from docs}
- {Feature 2 from docs}
- {Feature 3 from docs}

**Parameters Supported**:
- {Parameter 1}: {description}
- {Parameter 2}: {description}
- {Parameter 3}: {description}

### Next Steps

1. **Test the command**:
   ```bash
   /{command-name} "test input"
   ```

2. **Review the generated file**: `.claude/commands/{output-name}.md`

3. **Commit to git** (if satisfied):
   ```bash
   git add .claude/commands/{output-name}.md
   git commit -m "Add /{command-name} slash command"
   git push
   ```

4. **Update if needed**: Edit `.claude/commands/{output-name}.md` directly

### Quality Metrics

- ✅ All {N} major workflow stages covered
- ✅ {M} parameters documented with examples
- ✅ {K} validation checks specified
- ✅ Executable without conversation context
- ✅ Source documentation: {source-file-path}
```

---

## Important Notes

### Conversion Principles

1. **Documentation is Descriptive** → **Commands are Prescriptive**
   - Docs explain features → Commands give instructions
   - Docs show possibilities → Commands specify actions
   - Docs discuss → Commands direct

2. **Preserve Critical Details**
   - Keep exact file paths, commands, API endpoints
   - Include performance targets and cost estimates
   - Maintain templates and output formats
   - Transfer validation criteria

3. **Make Implicit Explicit**
   - If docs say "research sources", command lists exact sources with actions
   - If docs show example, command provides complete template
   - If docs mention config, command checks and prompts

4. **Handle Edge Cases**
   - Missing configuration
   - Invalid input
   - Failed operations
   - Partial results

### Quality Checklist

Before considering the command complete:

- ✅ Can be executed without seeing the source documentation
- ✅ All arguments have defaults or validation
- ✅ Every step is actionable (no vague instructions)
- ✅ Output formats are templated (not "generate a summary")
- ✅ File paths are absolute and explicit
- ✅ Commands are exact and copy-pasteable
- ✅ Validation criteria are measurable
- ✅ Error handling covers common failures
- ✅ References back to source documentation

### Common Mistakes to Avoid

- ❌ **Copying documentation prose directly**
  - Documentation: "This feature is useful for multi-source research"
  - Command should say: "Execute research across these 6 sources: [specific list with actions]"

- ❌ **Vague instructions**
  - Bad: "Process the data appropriately"
  - Good: "For each source, extract: title, URL, key points (3-5 bullets), publish date"

- ❌ **Missing argument parsing**
  - Always start with parsing $ARGUMENTS and setting defaults

- ❌ **Forgetting validation**
  - Every command needs validation and results reporting

- ❌ **No error handling**
  - Specify what to do when things fail

---

## Examples Reference

### Simple Command Example
See: `.claude/commands/core_commands/commit.md`
- Clean argument parsing
- Single focused workflow
- Clear validation

### Complex Command Example
See: `.claude/commands/research-generic-command.md`
- Multiple parameters with defaults
- Multi-step parallel execution
- Flexible output formats
- Comprehensive validation

### Chained Command Example
See: `.claude/commands/end-to-end-feature.md`
- Calls other commands in sequence
- Passes data between steps
- Aggregates results

---

## Validation

After generating the slash command:

1. **Read it yourself** - Does it make sense?
2. **Check completeness** - Are all features covered?
3. **Test executability** - Could you follow these instructions?
4. **Verify specificity** - Are there any vague instructions?
5. **Confirm templates** - Are output formats specified exactly?

---

## References

- **Documentation Guide**: `.claude/commands/slash-creator.md`
- **Existing Commands**: `.claude/commands/` (for reference)
- **Core Commands**: `.claude/commands/core_commands/` (for patterns)
- **Coding Standards**: `CLAUDE.md`
