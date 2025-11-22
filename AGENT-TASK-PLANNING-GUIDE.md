# Agent Task Planning Guide

**Purpose**: Comprehensive guide for planning AI agent tasks and features
**Audience**: Developers building AI agents with Pydantic AI, FastAPI, or similar frameworks
**Last Updated**: 2025-01-22

---

## Table of Contents

1. [Planning Philosophy](#planning-philosophy)
2. [Planning Workflow](#planning-workflow)
3. [Task Decomposition](#task-decomposition)
4. [Agent Tool Design](#agent-tool-design)
5. [Validation Planning](#validation-planning)
6. [Common Patterns](#common-patterns)
7. [Common Pitfalls](#common-pitfalls)
8. [Quick Reference Templates](#quick-reference-templates)
9. [Examples](#examples)

---

## Planning Philosophy

### Core Principles

**1. Agent-First Thinking**
- Design for LLM comprehension, not just human readability
- Tools are the CONTRACT between deterministic code and non-deterministic agents
- Clear contracts → better performance

**2. Plan for Testability**
- Every feature should have defined success criteria
- Tests should be planned BEFORE implementation (TDD approach)
- Validation strategy is part of the plan, not an afterthought

**3. Comprehensive but Practical**
- Planning should be thorough but not paralyzing
- Balance between over-planning (YAGNI violations) and under-planning (missing requirements)
- Iterate: Start with MVP, plan incremental improvements

**4. Type Safety is Non-Negotiable**
- All functions, methods, and variables MUST have type annotations
- Strict mypy configuration enforced
- No `Any` types without explicit justification

---

## Planning Workflow

### 5-Phase Planning Process

```
Phase 1: Discovery & Problem Definition (20% of planning time)
    ↓
Phase 2: Solution Design & Architecture (30% of planning time)
    ↓
Phase 3: Task Breakdown & Estimation (20% of planning time)
    ↓
Phase 4: Validation Strategy (20% of planning time)
    ↓
Phase 5: Documentation & Review (10% of planning time)
```

### Phase 1: Discovery & Problem Definition

**Objective**: Understand WHAT needs to be built and WHY

**Key Questions**:
- What problem are we solving?
- Who is the user/persona?
- What is the current state and pain points?
- What does success look like? (quantifiable metrics)
- What is the scope? (MVP vs nice-to-have)

**Deliverables**:
- Problem statement (2-3 sentences)
- User stories with acceptance criteria
- Success criteria (measurable metrics)
- Out of scope items (explicitly stated)

**Example Output**:
```markdown
## Problem Statement
LLM agents are confusing the `obsidian_folder_manage` and `obsidian_note_manage`
tools in ~20% of cases, leading to errors and poor user experience.

## User Story
As a user, I want the agent to correctly distinguish between folder and note
operations so that I don't receive errors when asking to manage folders.

**Acceptance Criteria**:
- Agent selects correct tool >95% of the time
- Clear error messages when wrong operation attempted
- No breaking changes to existing functionality

## Success Criteria
- Tool selection accuracy: 80% → >95%
- Error rate: 20% → <5%
- User satisfaction: >90% (post-deployment survey)
```

**Time**: 2-4 hours for typical feature

---

### Phase 2: Solution Design & Architecture

**Objective**: Understand HOW to build the solution

**Key Questions**:
- What components need to change? (models, services, APIs, tools)
- What is the architecture? (vertical slice, layered, etc.)
- What are the external dependencies?
- What are the integration points?
- What are the performance requirements?
- What are the security considerations?

**Deliverables**:
- Proposed solution description
- Architecture diagram (if complex)
- Component list with responsibilities
- Technology choices and justifications
- Security considerations
- Performance requirements

**Example Output**:
```markdown
## Proposed Solution: 6-Layer Tool Separation

**Layer 1: Path-Level Validation**
- Validate folder vs file paths before tool execution
- Clear error messages redirecting to correct tool

**Layer 2: Tool Docstrings**
- "Use this when" (affirmative guidance)
- "Do NOT use this for" (negative guidance)
- Examples with realistic data

**Layer 3: System Prompt Enhancement**
- Explicit tool selection guidance
- Common mistake prevention

**Layer 4: Parameter-Level Validation**
- Pydantic schemas enforce correct types
- Custom validators for business logic

**Layer 5: Operation-Level Separation**
- Folder operations: create, rename, move, delete, list, archive
- Note operations: read, write, update, search

**Layer 6: Runtime Tool Selection Detection**
- Evaluation tests measuring tool selection accuracy
- Automated regression testing

## Components to Change
1. `src/tools/obsidian_folder_manager/schemas.py` - Add ARCHIVE enum
2. `src/tools/obsidian_folder_manager/service.py` - Implement archive logic
3. `src/tools/obsidian_folder_manager/tool.py` - Update docstrings
4. `src/agent/system_prompt.py` - Add tool selection guidance
5. `tests/evaluation/tool_selection_accuracy.py` - New evaluation tests

## Performance Requirements
- Archive operation: <1 second for folders <100 files
- Tool selection: <100ms overhead
- Wikilink updates: <2 seconds for <1000 affected links
```

**Time**: 4-8 hours for typical feature

---

### Phase 3: Task Breakdown & Estimation

**Objective**: Break solution into actionable tasks with clear Definition of Done

**Key Questions**:
- What are the discrete tasks?
- What is the dependency order?
- What is the Definition of Done for each task?
- What is the estimated time for each task?
- What are the risks/blockers?

**Deliverables**:
- Task list with dependencies
- Definition of Done for each task
- Time estimates (T-shirt sizes or hours)
- Risk assessment for each task
- Critical path identification

**Example Output**:
```markdown
## Tasks

### Phase 1: Schema Changes (Priority: P0, Estimate: 2 hours)

**Task 1.1: Add ARCHIVE Enum to FolderOperation**
- Dependencies: None
- Definition of Done:
  - ✅ ARCHIVE added to FolderOperation enum in schemas.py
  - ✅ Type annotations correct
  - ✅ mypy passes with --strict
  - ✅ 2 unit tests pass (enum exists, enum value correct)
- Estimate: 30 minutes
- Risk: Low

**Task 1.2: Add Archive Parameters to ManageFolderRequest**
- Dependencies: Task 1.1
- Definition of Done:
  - ✅ archive_base field added (default: "archive")
  - ✅ date_format field added (default: "%Y-%m-%d")
  - ✅ Pydantic validation works
  - ✅ 3 unit tests pass (defaults, custom values, validation)
- Estimate: 1 hour
- Risk: Low

### Phase 2: Service Implementation (Priority: P0, Estimate: 6 hours)

**Task 2.1: Implement _archive_folder() Function**
- Dependencies: Task 1.2
- Definition of Done:
  - ✅ Function creates archive/YYYY-MM-DD/ directory structure
  - ✅ Function moves folder to archive location
  - ✅ Function preserves all files and subdirectories
  - ✅ Type annotations correct
  - ✅ Comprehensive logging (start, success, error)
  - ✅ 8 unit tests pass (basic, custom base, custom date format, errors)
- Estimate: 3 hours
- Risk: Medium (file system operations can be flaky)

[... continue for all tasks ...]
```

**Time**: 2-4 hours for typical feature

---

### Phase 4: Validation Strategy

**Objective**: Define HOW we'll verify the solution works correctly

**Key Questions**:
- What types of testing are needed? (unit, integration, E2E, performance, security)
- How many tests are needed?
- What are the test categories?
- What are the validation commands?
- What are the quality gates?
- What is the deployment strategy?
- What is the monitoring strategy?

**Deliverables**:
- Complete test plan with test counts by category
- Validation commands for each phase
- Quality gates (coverage %, 0 type errors, etc.)
- Pre-deployment validation checklist
- Deployment validation strategy
- Post-deployment monitoring plan
- Manual testing requirements

**Example Output**:
```markdown
## Validation Strategy

### Test Pyramid

| Test Type | Count | Coverage | Purpose |
|-----------|-------|----------|---------|
| Unit Tests | 33 | Services, schemas, utils | Fast feedback, isolate components |
| Integration Tests | 10 | Tool + Service + Vault | Verify component interactions |
| E2E Tests | 2 | Full agent workflows | Verify user scenarios |
| Evaluation Tests | 50 | Tool selection accuracy | Measure agent performance |
| Security Tests | 6 | Path traversal, injection | Prevent vulnerabilities |
| Performance Tests | 6 | Latency, throughput | Ensure acceptable performance |

**Total**: 107 tests

### Quality Gates (Must Pass Before Deployment)

1. **Code Quality**
   - ✅ Ruff: 0 linting errors
   - ✅ MyPy: 0 type errors (--strict mode)
   - ✅ Test Coverage: >90%

2. **Functional**
   - ✅ All unit tests pass (33/33)
   - ✅ All integration tests pass (10/10)
   - ✅ All E2E tests pass (2/2)

3. **Performance**
   - ✅ Archive operation: <1s for <100 files
   - ✅ Tool selection accuracy: >95%

4. **Security**
   - ✅ Bandit: 0 high/medium vulnerabilities
   - ✅ All security tests pass (6/6)

### Validation Commands

**Pre-Deployment**:
```bash
# 1. Dependencies
uv sync --frozen

# 2. Code Quality
uv run ruff check src/tools/obsidian_folder_manager/
uv run mypy src/tools/obsidian_folder_manager/ --strict

# 3. Tests
uv run pytest tests/tools/obsidian_folder_manager/ -v -m unit \
    --cov=src/tools/obsidian_folder_manager/ \
    --cov-fail-under=90

# 4. Security
uv run bandit -r src/tools/obsidian_folder_manager/ -ll
```

### Deployment Strategy

**4-Stage Deployment**:
1. Local/Dev → Smoke tests
2. Staging → Integration validation + 15 min UAT
3. Canary (5%) → 24-hour monitoring
4. Production (100%) → Phased rollout over 2-3 days

### Monitoring (Post-Deployment)

**Day 1-7**: Intensive monitoring
- Metrics: Archive success rate, tool selection accuracy, error rate, latency
- Alerts: Error rate >1%, latency >500ms, success rate <98%
- Manual checks: Daily spot testing

**Week 2-4**: Weekly monitoring
- Metrics review
- User feedback collection
- Performance trend analysis
```

**Time**: 4-8 hours for typical feature

---

### Phase 5: Documentation & Review

**Objective**: Document the plan and get stakeholder buy-in

**Key Questions**:
- Is the plan complete?
- Are all questions answered?
- Do stakeholders approve?
- Is anything missing?

**Deliverables**:
- Complete implementation plan document
- Stakeholder review and approval
- Open questions documented
- Risks acknowledged

**Time**: 1-2 hours for typical feature

---

## Task Decomposition

### Decomposition Strategies

#### 1. Vertical Slice Decomposition (Recommended)

Break tasks by end-to-end functionality across all layers.

**Example**: Archive Folder Feature
```
Slice 1: Basic Archive Operation
├─ Schema: Add ARCHIVE enum
├─ Service: Implement _archive_folder()
├─ Tool: Register archive operation
├─ Tests: 15 tests for archive path
└─ Documentation: Update tool docstring

Slice 2: Archive with Custom Parameters
├─ Schema: Add archive_base, date_format fields
├─ Service: Support custom parameters
├─ Tool: Update docstring with examples
├─ Tests: 8 tests for custom params
└─ Documentation: Update examples

Slice 3: Wikilink Updates on Archive
├─ Service: Implement wikilink detection
├─ Service: Implement wikilink replacement
├─ Tool: Update to call wikilink service
├─ Tests: 6 tests for wikilink updates
└─ Documentation: Document wikilink behavior
```

**Benefits**:
- Each slice delivers working functionality
- Easy to prioritize (can drop slice 3 if needed)
- Clear progress tracking

#### 2. Layer-Based Decomposition

Break tasks by architectural layer (models → services → APIs → tools).

**Example**: Archive Folder Feature
```
Phase 1: Data Layer
├─ Task 1.1: Add ARCHIVE enum to schemas
├─ Task 1.2: Add archive parameters to request schema
└─ Task 1.3: Add archive response schema

Phase 2: Service Layer
├─ Task 2.1: Implement _archive_folder()
├─ Task 2.2: Implement wikilink update service
└─ Task 2.3: Update manage_folder_service()

Phase 3: Tool Layer
├─ Task 3.1: Register archive operation in tool
├─ Task 3.2: Update tool docstring
└─ Task 3.3: Add system prompt guidance

Phase 4: Testing
├─ Task 4.1: Write unit tests (33 tests)
├─ Task 4.2: Write integration tests (10 tests)
└─ Task 4.3: Write E2E tests (2 tests)
```

**Benefits**:
- Clear separation of concerns
- Easy to parallelize (if multiple developers)
- Follows architecture naturally

**Drawbacks**:
- No working functionality until all layers complete
- Harder to demo progress
- Higher risk of integration issues

#### 3. Component-Based Decomposition

Break tasks by component (component = model + service + tests).

**Example**: Archive Folder Feature
```
Component 1: FolderOperation Schema
├─ Task 1.1: Add ARCHIVE enum
├─ Task 1.2: Write schema tests (5 tests)
└─ Task 1.3: Validate with mypy

Component 2: Archive Service
├─ Task 2.1: Implement _archive_folder()
├─ Task 2.2: Write service tests (13 tests)
└─ Task 2.3: Validate with pytest

Component 3: Wikilink Service
├─ Task 3.1: Implement wikilink detection
├─ Task 3.2: Implement wikilink replacement
└─ Task 3.3: Write wikilink tests (6 tests)

[... continue for all components ...]
```

**Benefits**:
- Complete one component at a time
- Easy to track (19 components → 19 checkboxes)
- Natural unit of work

---

## Agent Tool Design

### Tool Design Principles

**1. Single Responsibility**
Each tool should do ONE thing well. Don't create "swiss army knife" tools.

❌ **Bad**: `obsidian_manage(type="folder"|"note", operation="read"|"write"|"delete"|...)`
✅ **Good**: `obsidian_folder_manage()` and `obsidian_note_manage()` as separate tools

**2. Consolidated Operations Within Responsibility**
Within a single responsibility, consolidate related operations to reduce tool calls.

❌ **Bad**: Separate tools for `read_note()`, `write_note()`, `update_note()`, `append_note()`
✅ **Good**: `obsidian_note_manage(operation="read"|"write"|"update"|"append")`

**3. Agent-Optimized Docstrings**
Tool docstrings are read by LLMs. They must guide tool selection and usage.

**Required Elements**:
- One-line summary
- "Use this when" (affirmative guidance)
- "Do NOT use this for" (negative guidance, points to correct tool)
- Args with guidance on WHEN to use each parameter
- Returns with format details
- Performance notes (token usage, execution time, limits)
- Examples with realistic data

**Example**:
```python
@agent.tool
async def obsidian_folder_manage(
    ctx: RunContext[AgentDependencies],
    path: str,
    operation: FolderOperation,
    new_path: str | None = None,
    archive_base: str = "archive",
    date_format: str = "%Y-%m-%d",
) -> str:
    """Manage folders in Obsidian vault (create, rename, move, delete, list, archive).

    Use this when you need to:
    - Create a new folder in the vault
    - Rename an existing folder
    - Move a folder to a different location
    - Delete a folder (and all contents)
    - List all folders in the vault
    - Archive a folder with automatic date-based organization

    Do NOT use this for:
    - Managing NOTE FILES (use obsidian_note_manage instead)
    - Searching for notes (use obsidian_vault_query instead)
    - Reading note content (use obsidian_note_manage with operation="read")
    - Analyzing note relationships (use obsidian_graph_analyze instead)

    Args:
        path: Relative path to folder from vault root.
            Examples: "projects/alpha", "archive/2025-01", "daily"
            Do NOT include vault path - just relative path within vault.
            Do NOT include .md extension - this tool is for FOLDERS only.
        operation: What to do with the folder.
            - "create": Create new folder
            - "rename": Rename folder (requires new_path)
            - "move": Move folder to new location (requires new_path)
            - "delete": Delete folder and all contents (DESTRUCTIVE - use carefully)
            - "list": List all folders in vault
            - "archive": Move folder to archive/YYYY-MM-DD/folder-name
        new_path: Required for rename/move operations.
            Examples: "projects/alpha-v2", "archive/old-projects/alpha"
        archive_base: Base directory for archive operation (default: "archive").
            Use default unless user explicitly requests custom location.
        date_format: Date format for archive directory (default: "%Y-%m-%d").
            Default creates "archive/2025-01-22/folder-name"
            Use "%Y/%m" for "archive/2025/01/folder-name" (monthly organization)

    Returns:
        Success message describing what was done.
        Format: "✅ Operation completed: [details]"
        On error: "❌ Error: [error message with guidance]"

    Performance Notes:
        - Create/rename/move: <100ms for typical folders
        - Delete: ~1s per 100 files (DESTRUCTIVE - prompts for confirmation)
        - Archive: ~1-2s for <100 files (includes wikilink updates)
        - List: <200ms for vaults with <1000 folders
        - Max folder size: No limit, but operations >1000 files may be slow

    Examples:
        # Create a new project folder
        obsidian_folder_manage(
            path="projects/website-redesign",
            operation="create"
        )

        # Archive completed project with default settings
        obsidian_folder_manage(
            path="projects/old-website",
            operation="archive"
        )

        # Archive with monthly organization
        obsidian_folder_manage(
            path="projects/completed-2024",
            operation="archive",
            date_format="%Y/%m"
        )

        # Rename a folder
        obsidian_folder_manage(
            path="projects/alpha",
            operation="rename",
            new_path="projects/alpha-v2"
        )
    """
```

**4. Token-Efficient Response Formats**
Provide response format parameters to control token usage.

```python
response_format: str = "concise"  # "minimal" | "concise" | "detailed"
```

Document token costs in Performance Notes:
```markdown
Performance Notes:
    - Minimal format: ~50 tokens (use for metadata checks)
    - Concise format: ~150 tokens (default, good balance)
    - Detailed format: ~1500+ tokens (only when full content needed)
```

**5. Type Safety**
All tool parameters and returns must be type-safe.

```python
# ✅ Good - Type-safe with enum
async def manage_folder(
    ctx: RunContext[AgentDependencies],
    path: str,
    operation: FolderOperation,  # Enum
) -> str:  # Structured return

# ❌ Bad - Stringly-typed
async def manage_folder(
    ctx: RunContext[AgentDependencies],
    path: str,
    operation: str,  # Could be anything
) -> Any:  # Unstructured return
```

---

## Validation Planning

### Validation Pyramid

```
Manual Testing (User)
    ↑ (12 tests)
    │
Post-Deployment Monitoring
    ↑ (6 automated monitors)
    │
Deployment Validation
    ↑ (12 smoke tests)
    │
Pre-Deployment Validation
    ↑ (48 checks)
    │
Security Tests
    ↑ (6 tests)
    │
Performance Tests
    ↑ (6 tests)
    │
E2E Tests
    ↑ (2 tests)
    │
Integration Tests
    ↑ (10 tests)
    │
Unit Tests (Base)
    ↓ (30+ tests)
```

### Test Planning Checklist

When planning validation for any feature, ensure you have:

**✅ Unit Tests** (Foundation)
- Test each function/method in isolation
- Mock external dependencies
- Aim for >90% code coverage
- Fast execution (<1s total)

**✅ Integration Tests** (Component Interactions)
- Test 2-3 components working together
- Real dependencies (test database, test vault)
- Cover key integration points
- Moderate execution time (5-30s total)

**✅ E2E Tests** (User Workflows)
- Test complete user scenarios end-to-end
- Real environment (as close to production as possible)
- Cover critical user paths
- Slower execution (30s-5min total)

**✅ Evaluation Tests** (Agent Performance)
- For AI agent features: measure tool selection accuracy, response quality
- Dataset of test cases with expected outputs
- Statistical analysis (accuracy, precision, recall)
- Run before deployment and periodically

**✅ Performance Tests** (Latency, Throughput)
- Measure key operations under load
- Set SLOs (Service Level Objectives)
- Test at expected scale + 2x
- Identify bottlenecks

**✅ Security Tests** (Vulnerabilities)
- Path traversal attacks
- Injection attacks (SQL, command, XSS)
- Authentication/authorization bypass
- Sensitive data exposure
- Use Bandit for static analysis

**✅ Pre-Deployment Validation** (Quality Gates)
- Dependency validation
- Linting and type checking
- All tests pass
- Coverage meets threshold
- Security scan passes

**✅ Deployment Validation** (Staged Rollout)
- Smoke tests after each deployment stage
- Monitoring and alerting configured
- Rollback procedure documented and tested
- Incremental rollout (5% → 25% → 50% → 100%)

**✅ Post-Deployment Validation** (Production Monitoring)
- Metrics dashboards
- Automated smoke tests (every 6 hours)
- Error rate monitoring
- Latency monitoring
- User feedback collection
- Success criteria validation

**✅ Manual Testing** (User Acceptance)
- UAT (User Acceptance Testing) scenarios
- Real user workflows
- Edge cases and happy paths
- Sign-off from stakeholders

---

## Common Patterns

### Pattern 1: Feature Flag for Gradual Rollout

**When to Use**: Deploying risky features, A/B testing, gradual rollout

**Implementation**:
```python
# src/shared/config.py
class Settings(BaseSettings):
    enable_archive_feature: bool = False  # Feature flag

# src/tools/obsidian_folder_manager/tool.py
@agent.tool
async def obsidian_folder_manage(...) -> str:
    if operation == FolderOperation.ARCHIVE:
        if not ctx.deps.config.enable_archive_feature:
            return "❌ Archive feature not yet available"
    # ... rest of implementation
```

**Benefits**:
- Deploy code to production without enabling feature
- Enable for specific users/percentage
- Quick rollback (just toggle flag)

---

### Pattern 2: Comprehensive Error Messages

**When to Use**: Always, especially for agent-facing tools

**Implementation**:
```python
def validate_folder_path(path: str) -> None:
    """Validate that path is a folder, not a file."""
    if path.endswith(('.md', '.markdown', '.txt')):
        msg = (
            f"❌ Invalid path for folder operation: '{path}'\n\n"
            f"This tool operates on FOLDERS only.\n"
            f"To work with note files, use:\n\n"
            f"obsidian_note_manage(\n"
            f"    path='{path}',\n"
            f"    operation='read',\n"
            f")\n"
        )
        raise ValueError(msg)
```

**Benefits**:
- Agent learns correct tool to use
- User sees helpful error message
- Reduces support burden

---

### Pattern 3: Structured Logging for Debugging

**When to Use**: Always, especially for complex operations

**Implementation**:
```python
from src.shared.logging import get_logger

logger = get_logger(__name__)

async def _archive_folder(
    vault_path: Path,
    folder_path: str,
    archive_base: str,
    date_format: str,
) -> Path:
    """Archive folder with date-based organization."""
    logger.info(
        "archive_folder_started",
        folder_path=folder_path,
        archive_base=archive_base,
        date_format=date_format,
    )

    try:
        # ... implementation ...
        logger.info(
            "archive_folder_completed",
            folder_path=folder_path,
            archive_path=str(archive_path),
            files_moved=file_count,
            duration_ms=duration,
        )
        return archive_path
    except Exception:
        logger.exception(
            "archive_folder_failed",
            folder_path=folder_path,
            archive_base=archive_base,
        )
        raise
```

**Benefits**:
- Easy debugging with correlation_id
- AI agent can read logs to fix issues
- Performance tracking built-in

---

### Pattern 4: Test Data Builders

**When to Use**: Complex test setup, repeated test data creation

**Implementation**:
```python
# tests/tools/obsidian_folder_manager/builders.py
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TestVaultBuilder:
    """Builder for creating test vault structures."""

    vault_path: Path
    folders: list[str]
    notes: dict[str, str]  # path -> content

    @classmethod
    def create(cls, tmp_path: Path) -> "TestVaultBuilder":
        return cls(vault_path=tmp_path, folders=[], notes={})

    def with_folder(self, path: str) -> "TestVaultBuilder":
        self.folders.append(path)
        return self

    def with_note(self, path: str, content: str) -> "TestVaultBuilder":
        self.notes[path] = content
        return self

    def build(self) -> Path:
        for folder in self.folders:
            (self.vault_path / folder).mkdir(parents=True, exist_ok=True)
        for note_path, content in self.notes.items():
            (self.vault_path / note_path).write_text(content)
        return self.vault_path

# Usage in tests
def test_archive_folder(tmp_path: Path):
    vault = (
        TestVaultBuilder.create(tmp_path)
        .with_folder("projects/alpha")
        .with_note("projects/alpha/readme.md", "# Alpha Project")
        .with_note("projects/alpha/tasks.md", "- [ ] Task 1")
        .build()
    )
    # ... test logic ...
```

**Benefits**:
- Clean, readable test setup
- Reusable across tests
- Easy to extend

---

## Common Pitfalls

### Pitfall 1: Under-Specified Success Criteria

**Problem**: Vague success criteria like "feature works well" or "users are happy"

**Example**:
```markdown
❌ Bad:
Success Criteria:
- Feature works correctly
- Performance is good
- Users like it

✅ Good:
Success Criteria:
- Tool selection accuracy: >95% (measured by 50 evaluation tests)
- Archive operation latency: <1s for folders with <100 files (P95)
- User satisfaction: >4.5/5 stars (post-deployment survey, n>30)
- Error rate: <5% (production metrics, 30-day window)
```

**Fix**: Make all success criteria measurable and quantifiable

---

### Pitfall 2: Missing Negative Guidance in Tool Docstrings

**Problem**: Agent doesn't know when NOT to use a tool, leads to tool confusion

**Example**:
```python
❌ Bad:
"""Manage folders in Obsidian vault.

Use this when you need to create, rename, move, or delete folders.
"""

✅ Good:
"""Manage folders in Obsidian vault.

Use this when you need to:
- Create, rename, move, or delete FOLDERS

Do NOT use this for:
- Managing note FILES (use obsidian_note_manage instead)
- Searching for notes (use obsidian_vault_query instead)
- Reading note content (use obsidian_note_manage with operation="read")
"""
```

**Fix**: Always include "Do NOT use this for" section pointing to correct alternatives

---

### Pitfall 3: No Definition of Done for Tasks

**Problem**: Tasks are "done" but don't meet quality standards

**Example**:
```markdown
❌ Bad:
Task 1.1: Add ARCHIVE enum
- Estimate: 30 minutes

✅ Good:
Task 1.1: Add ARCHIVE enum to FolderOperation
- Dependencies: None
- Definition of Done:
  - ✅ ARCHIVE added to FolderOperation enum in schemas.py
  - ✅ Type annotations correct
  - ✅ mypy passes with --strict
  - ✅ 2 unit tests pass (enum exists, enum value correct)
- Estimate: 30 minutes
- Risk: Low
```

**Fix**: Every task must have explicit Definition of Done

---

### Pitfall 4: Testing as an Afterthought

**Problem**: Tests written after implementation, leading to low coverage and poor quality

**Example**:
```markdown
❌ Bad:
Phase 1: Implement feature (2 weeks)
Phase 2: Write tests (2 days)
Phase 3: Deploy (1 day)

✅ Good:
Phase 1: Schema Changes
  Task 1.1: Add ARCHIVE enum
  Task 1.2: Write schema tests (5 tests)
  Task 1.3: Validate with mypy + pytest

Phase 2: Service Implementation
  Task 2.1: Implement _archive_folder()
  Task 2.2: Write service tests (13 tests)
  Task 2.3: Validate with pytest

[Tests are part of each phase, not separate phase]
```

**Fix**: Use TDD approach - plan tests WITH implementation tasks

---

### Pitfall 5: No Rollback Plan

**Problem**: Deployment fails, no clear way to rollback, production broken

**Example**:
```markdown
❌ Bad:
Deployment:
1. Push to production
2. Hope it works

✅ Good:
Deployment:
Stage 1: Deploy to staging → Run smoke tests → User validates
Stage 2: Deploy to 5% production → Monitor 24h → Check metrics
Stage 3: Deploy to 100% → Monitor 48h

Rollback Procedure (at each stage):
1. Toggle feature flag to disable
2. If severe: git revert + redeploy previous version
3. Notify stakeholders
4. Post-mortem to prevent recurrence
```

**Fix**: Document rollback procedure for each deployment stage

---

### Pitfall 6: Ignoring Token Costs in Agent Tools

**Problem**: Agent tools return massive responses, causing token waste and slow performance

**Example**:
```python
❌ Bad:
@agent.tool
async def read_note(path: str) -> str:
    """Read a note."""
    return vault.read(path)  # Could be 10,000 tokens!

✅ Good:
@agent.tool
async def read_note(
    path: str,
    response_format: str = "concise"  # minimal|concise|detailed
) -> str:
    """Read a note with token-efficient formatting.

    Performance Notes:
        - Minimal: ~50 tokens (title, tags only)
        - Concise: ~150 tokens (title, tags, preview)
        - Detailed: ~1500+ tokens (full content)
    """
    content = vault.read(path)
    if response_format == "minimal":
        return format_minimal(content)  # ~50 tokens
    elif response_format == "concise":
        return format_concise(content)  # ~150 tokens
    else:
        return content  # Full content
```

**Fix**: Provide response format parameters and document token costs

---

### Pitfall 7: No Component Coverage Matrix

**Problem**: Unclear which components need testing, leading to gaps

**Example**:
```markdown
❌ Bad:
Testing:
- Write some unit tests
- Write some integration tests
- Deploy

✅ Good:
Component Coverage Matrix:

| Component | File | What to Test | Test File |
|-----------|------|--------------|-----------|
| FolderOperation Enum | schemas.py | ARCHIVE exists | test_schemas.py |
| ManageFolderRequest | schemas.py | archive params | test_schemas.py |
| validate_folder_path() | service.py | File rejection | test_service.py |
| _archive_folder() | service.py | Archive logic | test_service.py |
| obsidian_folder_manage | tool.py | Tool registration | test_tool.py |
| Agent API | main.py | Tool execution | test_workflows.py |

Total: 19 components, 9 test files, 70 tests
```

**Fix**: Create component coverage matrix ensuring every component has tests

---

## Quick Reference Templates

### Template 1: Implementation Plan (Complete)

Use IMPLEMENTATION-PLAN-TEMPLATE.md (600 lines) for complete template

**Quick Version** (for simple features):
```markdown
# [Feature Name] Implementation Plan

## 1. Goal & Problem Statement
**Problem**: [What problem are we solving? 2-3 sentences]

**Goal**: [What are we building? 1 sentence]

**Success Criteria**:
- [Metric 1]: [Current] → [Target]
- [Metric 2]: [Current] → [Target]
- [Metric 3]: [Current] → [Target]

## 2. User Stories

### User Story 1: [Title]
**As a** [persona]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria**:
- ✅ [Criterion 1]
- ✅ [Criterion 2]
- ✅ [Criterion 3]

**Priority**: P0 (Must Have) | P1 (Should Have) | P2 (Nice to Have)

## 3. Proposed Solution
[High-level approach - 3-5 paragraphs]

**Components to Change**:
1. [Component 1] - [What changes]
2. [Component 2] - [What changes]
3. [Component 3] - [What changes]

## 4. Tasks

### Phase 1: [Phase Name] (Estimate: [X hours])

**Task 1.1: [Task Name]**
- Dependencies: [Task IDs or None]
- Definition of Done:
  - ✅ [DoD item 1]
  - ✅ [DoD item 2]
  - ✅ [Tests pass: X/X]
- Estimate: [X hours/days]
- Risk: Low | Medium | High

[... repeat for all tasks ...]

## 5. Validation Strategy

**Test Summary**:
- Unit Tests: [X tests]
- Integration Tests: [X tests]
- E2E Tests: [X tests]
- Total: [X tests]

**Quality Gates**:
- ✅ All tests pass ([X]/[X])
- ✅ Coverage >90%
- ✅ MyPy 0 errors (--strict)
- ✅ Ruff 0 errors

**Deployment**: [4-stage | 2-stage | single deployment]

## 6. Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [How to mitigate] |
```

---

### Template 2: Test Plan

```markdown
# [Feature Name] Test Plan

## Test Summary

| Category | Count | Coverage |
|----------|-------|----------|
| Unit Tests | [X] | [Component names] |
| Integration Tests | [X] | [Integration points] |
| E2E Tests | [X] | [User workflows] |
| Performance Tests | [X] | [Operations tested] |
| Security Tests | [X] | [Vulnerabilities checked] |
| **Total** | **[X]** | - |

## Unit Tests ([X] tests)

### Test File: tests/[path]/test_[module].py

**Test 1: [Test Name]**
```python
def test_[name]():
    """Test that [what is being tested]."""
    # Arrange
    [setup]

    # Act
    result = [function_call]

    # Assert
    assert [expectation]
```

[... repeat for all unit tests ...]

## Integration Tests ([X] tests)

[... similar structure ...]

## Validation Commands

```bash
# Unit Tests
uv run pytest tests/[path]/ -v -m unit --cov

# Integration Tests
uv run pytest tests/integration/ -v -m integration

# All Tests
uv run pytest tests/ -v --cov-fail-under=90
```

## Quality Gates

- ✅ All tests pass ([X]/[X])
- ✅ Coverage >[X]%
- ✅ MyPy 0 errors
- ✅ Ruff 0 errors
```

---

### Template 3: Component Coverage Matrix

```markdown
# Component Coverage Matrix

| Component Type | File Path | What to Test | Test File | Status |
|----------------|-----------|--------------|-----------|--------|
| **MODELS/SCHEMAS** | | | | |
| [Model 1] | [path] | [Test areas] | [test_file.py] | ☐ Write |
| [Model 2] | [path] | [Test areas] | [test_file.py] | ☐ Write |
| **SERVICES** | | | | |
| [Service 1] | [path] | [Test areas] | [test_file.py] | ☐ Write |
| [Service 2] | [path] | [Test areas] | [test_file.py] | ☐ Write |
| **TOOLS** | | | | |
| [Tool 1] | [path] | [Test areas] | [test_file.py] | ☐ Write |
| **APIS** | | | | |
| [API 1] | [path] | [Test areas] | [test_file.py] | ☐ Write |
| **INTEGRATIONS** | | | | |
| [Integration 1] | [path] | [Test areas] | [test_file.py] | ☐ Write |

**Total Components**: [X]
**Total Test Files**: [X]
**Total Tests**: [X]
```

---

## Examples

### Example 1: Simple Feature - Add New Enum Value

**Feature**: Add "STARRED" status to note status enum

**Planning Time**: 1 hour

**Implementation Plan**:
```markdown
# Add STARRED Status Implementation Plan

## 1. Goal
Allow users to mark notes as "starred" for quick access.

**Success Criteria**:
- STARRED status available in API
- >95% of starred note operations succeed
- No breaking changes to existing statuses

## 2. User Story
As a user, I want to mark notes as starred so that I can quickly find important notes.

**Acceptance Criteria**:
- ✅ Can set note status to STARRED
- ✅ Can query all starred notes
- ✅ Starred status persists across sessions

**Priority**: P1 (Should Have)

## 3. Tasks

**Task 1: Add STARRED to NoteStatus Enum** (30 min)
- Definition of Done:
  - ✅ STARRED added to enum
  - ✅ mypy passes
  - ✅ 2 unit tests pass

**Task 2: Update Note Service** (30 min)
- Definition of Done:
  - ✅ set_status() accepts STARRED
  - ✅ get_starred_notes() returns all starred notes
  - ✅ 5 unit tests pass

**Task 3: Update Tool Docstring** (15 min)
- Definition of Done:
  - ✅ Docstring documents STARRED status
  - ✅ Example added

**Task 4: Integration Test** (30 min)
- Definition of Done:
  - ✅ E2E test: Set star, query starred, verify
  - ✅ 1 integration test passes

## 4. Validation
- Unit Tests: 7
- Integration Tests: 1
- Total: 8 tests

**Quality Gates**:
- ✅ 8/8 tests pass
- ✅ mypy 0 errors
- ✅ ruff 0 errors

**Deployment**: Single deployment (low risk)
```

**Total Effort**: 2 hours planning + 2 hours implementation = 4 hours

---

### Example 2: Medium Feature - Archive Folder

See FOLDER-MANAGEMENT-ENHANCEMENT-PLAN.md for complete example

**Feature**: Add archive operation to folder management tool

**Planning Time**: 8-12 hours

**Key Elements**:
- 2 user stories (tool separation, archive operation)
- 20+ tasks across 4 phases
- 70 total tests
- 6-layer separation strategy
- 4-stage deployment

**Total Effort**: 12 hours planning + 80-120 hours implementation = ~2-3 weeks

---

### Example 3: Complex Feature - Multi-Agent Collaboration

**Feature**: Allow multiple agents to collaborate on tasks

**Planning Time**: 40-80 hours (1-2 weeks)

**Complexity Factors**:
- Distributed systems (agent communication, state synchronization)
- Concurrency (race conditions, deadlocks)
- Security (agent authentication, authorization)
- Observability (distributed tracing, debugging)
- Performance (latency, throughput at scale)

**Key Planning Activities**:
- Architecture design (event-driven? message queue? peer-to-peer?)
- Technology evaluation (RabbitMQ? Kafka? Redis Pub/Sub?)
- Data modeling (agent state, message schemas)
- Failure modes analysis (what if agent crashes mid-task?)
- Simulation testing (agent behavior under load)
- Gradual rollout (single agent → 2 agents → N agents)

**Total Effort**: 2 weeks planning + 6-12 months implementation

---

## Conclusion

**Key Takeaways**:

1. **Planning is an investment**, not overhead
   - 10-20% of total effort on planning saves 50%+ on rework

2. **Plan for the agent, not just the code**
   - Tool docstrings are contracts between code and LLM
   - Clear contracts → better agent performance

3. **Tests are part of the plan, not an afterthought**
   - TDD approach: plan tests WITH tasks
   - Component coverage matrix ensures no gaps

4. **Validation is comprehensive**
   - Unit → Integration → E2E → Performance → Security
   - Pre-deployment → Deployment → Post-deployment
   - Automated + Manual

5. **Documentation is essential**
   - Future you (and others) will thank you
   - AI agents can read docs to fix issues

**Next Steps**:

1. Choose your feature complexity (simple, medium, complex)
2. Select appropriate template
3. Follow 5-phase planning workflow
4. Create component coverage matrix
5. Plan tests WITH implementation tasks
6. Review with stakeholders
7. Begin implementation

**Remember**: A well-planned feature is half-implemented. Take time to plan thoroughly - it pays off.

---

**Related Documents**:
- IMPLEMENTATION-PLAN-TEMPLATE.md - Complete planning template (600 lines)
- FOLDER-MANAGEMENT-ENHANCEMENT-PLAN.md - Medium feature example
- PLANNING.md - Master index of all planning documentation
- CLAUDE.md - AI Agent Development Instructions (coding standards)
