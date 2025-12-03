# Feature Planning & Implementation Template

## Purpose

This document provides a comprehensive template for planning and implementing features in the Obsidian Agent codebase. Use this template to guide the complete lifecycle from research → planning → implementation → validation. This template works for both human developers and AI planning agents.

---

## Document Navigation

This template follows a complete feature development lifecycle:

```
Phase 0: Research & Discovery
├── Explore existing codebase patterns
├── Research implementation options
├── Research technologies & libraries
└── Identify constraints & requirements

Phase 1: Planning & Design
├── Problem statement & user story
├── Solution approach & rationale
├── Context assessment
├── Design decisions
└── Implementation strategy

Phase 2: Implementation
├── Code quality standards
├── Schemas design & implementation
├── Service layer implementation
├── Tool registration / Feature integration
└── Documentation

Phase 3: Testing & Validation
├── Pre-deployment test suite
├── User acceptance testing (UAT)
├── Quality gates
├── Edge cases & acceptance criteria
├── Validation commands
└── Deployment validation (optional)
```

---

# PHASE 0: Research & Discovery

**Purpose:** Understand the problem space, existing solutions, and available options before jumping into implementation.

**Audience:** Both humans and AI agents should complete this phase to ensure informed decisions.

---

## Step 0.1: Explore Existing Codebase

### Files to Read

**1. Core Architecture Files:**
- `src/agent/agent.py` - Agent initialization and tool registration patterns
- `src/shared/` - Shared utilities (config, logging, security, validation)
- `CLAUDE.md` - Project coding standards and requirements

**2. Similar Existing Tools:**

Identify the tool/feature most similar to what you're building:
- Read its `tool.py` - How is it registered? What's the docstring structure?
- Read its `schemas.py` - How are requests/responses modeled?
- Read its `service.py` - What patterns are used for business logic?
- Read its tests in `tests/tools/<name>/` - What testing patterns are used?

**3. Relevant Shared Utilities:**

Check what's already available:
- `src/shared/vault_security.py` - Path validation and security
- `src/shared/logging.py` - Structured logging
- `src/shared/config.py` - Configuration management
- [Other relevant shared modules]

### Document Your Findings

**Codebase Patterns Discovered:**

```markdown
**Pattern 1: Tool Registration**
- File: src/tools/[tool_name]/tool.py
- Pattern: [Describe the pattern]
- Example: [Code snippet or reference]

**Pattern 2: Schema Validation**
- File: src/tools/[tool_name]/schemas.py
- Pattern: [Describe the pattern]
- Example: [Code snippet or reference]

**Pattern 3: Service Layer**
- File: src/tools/[tool_name]/service.py
- Pattern: [Describe the pattern]
- Example: [Code snippet or reference]

**Reusable Components:**
- `validate_vault_path()` - Path validation
- `get_logger()` - Structured logging
- [Other components identified]

**Integration Points:**
- [Component 1]: [How it integrates]
- [Component 2]: [How it integrates]
```

---

## Step 0.2: Research Implementation Options

### When to Use Which Options Analysis Format

**Use Simple Pros/Cons Format when:**
- ✅ Comparing 2-4 conceptually different approaches
- ✅ Architectural decisions (new tool vs. extend existing)
- ✅ Qualitative tradeoffs (maintainability, consistency)
- ✅ Early exploration phase (divergent thinking)

**Use Decision Matrix when:**
- ✅ Comparing 3+ similar solutions (e.g., library choices)
- ✅ Need objective scoring across multiple criteria
- ✅ Quantitative comparison (performance, complexity, cost)
- ✅ Need to defend decision with data

**Use BOTH when:**
- ✅ First use Pros/Cons to narrow from many options to 2-3 finalists
- ✅ Then use Decision Matrix for final selection with detailed scoring

---

### Format A: Simple Pros/Cons (Qualitative)

**Option 1: [Name of Approach]**
- **Description:** [What is this approach? 2-3 sentences]
- **Pros:**
  - [Advantage 1]
  - [Advantage 2]
  - [Advantage 3]
- **Cons:**
  - [Disadvantage 1]
  - [Disadvantage 2]
  - [Disadvantage 3]
- **Effort:** [Low/Medium/High] + brief justification (1-2 sentences)
- **Precedent:** [Has this been done elsewhere in codebase? Reference if yes]

**Option 2: [Name of Approach]**
- **Description:** [What is this approach?]
- **Pros:** [...]
- **Cons:** [...]
- **Effort:** [...]
- **Precedent:** [...]

**Option 3: [Name of Approach]** (if applicable)
- [...]

**Recommended Approach:** Option #X

**Rationale:**
[2-3 sentences explaining why this option is best based on:
- Alignment with existing patterns
- Maintainability
- Effort vs. value
- Team preferences/constraints]

---

### Format B: Decision Matrix (Quantitative)

**Use this when comparing multiple similar solutions (e.g., library choices).**

| Option | Effort (1-5) | Maintainability (1-5) | Performance (1-5) | Consistency (1-5) | Cross-Platform (1-5) | Total Score |
|--------|--------------|----------------------|-------------------|-------------------|---------------------|-------------|
| Option 1: [Name] | 3 | 5 | 4 | 5 | 5 | 22/25 |
| Option 2: [Name] | 4 | 3 | 5 | 3 | 4 | 19/25 |
| Option 3: [Name] | 5 | 4 | 3 | 4 | 5 | 21/25 |

**Scoring Scale:** 1=Poor, 5=Excellent

**Criteria Definitions:**
- **Effort:** Lower is better (1=High effort, 5=Low effort)
- **Maintainability:** Code clarity, debugging ease
- **Performance:** Speed, resource usage
- **Consistency:** Alignment with existing codebase patterns
- **Cross-Platform:** Windows/Linux/macOS support

**Weights:** (Adjust if certain criteria are more important)
- All criteria equal weight (default)
- OR: Effort (2x), Performance (1.5x), Others (1x)

**Recommended Option:** Option #X (highest total score)

**Rationale:**
[Justify the choice based on scores and context]

---

## Step 0.3: Research Technologies & Libraries

### Library/Technology Research Template

For each technology/library being considered:

**Technology 1: [Name]**
- **Purpose:** [What does it do? One sentence]
- **Why Needed:** [Specific use case for this feature]
- **Already in Project:** ☐ Yes (check `pyproject.toml`) ☐ No (requires addition)
- **Cross-Platform:** ☐ Windows ☐ Linux ☐ macOS ☐ All
- **Async Support:** ☐ Yes ☐ No ☐ N/A
- **Documentation:** [URL]
  - **Key Sections:**
    - [Section 1]: [Summary]
    - [Section 2]: [Summary]
  - **Relevant Features:**
    - [Feature 1]
    - [Feature 2]
- **Alternatives Considered:** [Other options, why this one is better]

**Technology 2: [Name]**
- [...]

### Research Documentation Links

Document all external research with structured format:

**1. [Library/Framework Name]**
- **URL:** [Full URL]
- **Anchor:** [#specific-section] (if applicable)
- **Summary:** [1-2 sentence summary of relevant content]
- **Key Takeaways:**
  - [Takeaway 1: How to use it]
  - [Takeaway 2: Limitations/gotchas]
  - [Takeaway 3: Best practices]
- **Code Example:** [If applicable, brief example]

**2. [Stack Overflow / Blog Post]**
- **URL:** [Full URL]
- **Problem Addressed:** [What problem does this solve?]
- **Solution Summary:** [Brief description]
- **Applicability:** [How does this apply to our feature?]

**3. [Official Documentation]**
- [...]

### Technology Stack Summary

| Technology | Purpose | Cross-Platform | Async | Already in Project | Justification |
|------------|---------|----------------|-------|-------------------|---------------|
| [Tech 1] | [Purpose] | ✅ Yes | ✅ Yes | ✅ Yes | [Why chosen] |
| [Tech 2] | [Purpose] | ✅ Yes | ❌ No | ❌ No | [Why chosen] |
| [Tech 3] | [Purpose] | ⚠️ Partial | ✅ Yes | ✅ Yes | [Why chosen] |

**Dependencies to Add:**
```toml
# Add to pyproject.toml [project.dependencies]
"library-name>=1.2.3"
```

---

## Step 0.4: Identify Constraints & Requirements

### Security & Domain Constraints

**Vault Boundary Enforcement:**
- [ ] Operations must be restricted to vault path specified in `.env`
- [ ] Path validation using `validate_vault_path(vault_root, user_path)`
- [ ] Absolute paths rejected
- [ ] Path traversal attempts (`../../../etc/passwd`) blocked
- [ ] Sensitive folders protected (`.obsidian`, `.git`, `.env`)

**Input Validation:**
- [ ] All user inputs validated via Pydantic schemas
- [ ] File/folder names validated against platform-specific rules
- [ ] Windows reserved names rejected (CON, PRN, AUX, etc.)
- [ ] Invalid characters blocked

**Data Privacy:**
- [ ] No sensitive data logged (passwords, tokens, API keys)
- [ ] User data redacted in logs
- [ ] Error messages don't leak sensitive information

### Technical Constraints

**Performance Requirements:**
- Small operations: < [X]ms target
- Medium operations: < [Y]ms target
- Large operations: < [Z]s target
- [Define what "small/medium/large" means for your feature]

**Token Efficiency (for Agent Tools):**
- Minimal format: ~50 tokens (metadata/confirmations only)
- Concise format: ~150 tokens (default, balanced)
- Detailed format: ~1500+ tokens (full content, use sparingly)

**Resource Limits:**
- Max file size: [X] MB
- Max batch size: [Y] items
- Timeout: [Z] seconds

### Business Requirements

**User Story:**
```
As a [type of user]
I want to [perform some action]
So that [achieve some benefit/solve some problem]
```

**Example:**
```
As an Obsidian user
I want to archive old project folders with automatic date prefixes
So that I can keep my vault organized without manually creating date-based folders
```

**Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

# PHASE 1: Planning & Design

**Purpose:** Based on research, create a concrete plan with clear rationale.

---

## 1.1: Problem Statement & User Story

### Feature Name
[Concise, descriptive name - e.g., "Folder Management Tool"]

### Problem
[What problem does this solve? Who experiences this problem? 2-3 sentences]

**Example:**
"Users need to perform folder operations (create, move, rename, archive, delete) within their Obsidian vault. Currently, there's no agent tool for folder operations, forcing users to manipulate files individually or manually manage folders outside the agent interface."

### User Story
```
As a [type of user]
I want to [perform some action]
So that [achieve some benefit]
```

### Current Pain Points
- [Pain point 1]
- [Pain point 2]
- [Pain point 3]

### Proposed Solution
[1-2 sentences describing what you'll build]

**Example:**
"Build a new `obsidian_folder_manager` tool that provides folder operations (create, move, rename, archive, delete) with security validation, wikilink auto-update, and integration with existing vault security patterns."

### Why This Approach
[Based on Phase 0 research, justify the chosen approach]

**Example:**
"Based on research (Step 0.2), we chose Option 2 (dedicated folder tool) because:
- Maintains separation of concerns (folders vs. notes)
- Follows existing tool pattern from `obsidian_note_manager`
- Prevents tool confusion by having clear boundaries
- Lower effort than modifying existing tools (Medium vs. High effort)"

### Scope

**✅ In Scope:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

**❌ Out of Scope:**
- [Non-feature 1]
- [Non-feature 2]

**🔮 Future Enhancements:**
- [Potential future feature 1]
- [Potential future feature 2]

---

## 1.2: Context Assessment

### Current State

**✅ What already exists and works:**
- [Existing component 1]
- [Existing component 2]
- [Existing pattern 1]

**⚠️ What problems exist:**
- [Problem 1]
- [Problem 2]

**❌ What's missing:**
- [Gap 1]
- [Gap 2]

### Architecture

**Relevant parts of the codebase:**
```
src/
├── agent/
│   └── agent.py              # Tool registration patterns
├── tools/
│   ├── [similar_tool]/       # Pattern to follow
│   │   ├── tool.py
│   │   ├── schemas.py
│   │   └── service.py
│   └── [new_tool]/           # What we're building
│       ├── tool.py
│       ├── schemas.py
│       └── service.py
├── shared/
│   ├── vault_security.py     # Path validation
│   ├── logging.py            # Structured logging
│   └── config.py             # Configuration

tests/
├── tools/
│   └── [new_tool]/
│       ├── test_tool.py
│       ├── test_schemas.py
│       └── test_service.py
└── integration/
    └── test_[new_tool]_integration.py
```

### Dependencies

**Internal Dependencies:**
- `src.shared.vault_security` - Path validation
- `src.shared.logging` - Structured logging
- `src.shared.config` - Configuration management
- [Other internal dependencies]

**External Dependencies:**
(From Phase 0, Step 0.3 research)
- `aioshutil` - Async file system operations
- `pathlib` - Cross-platform path handling
- [Other external dependencies]

**Integration Points:**
- [Component 1]: [How they interact]
- [Component 2]: [How they interact]

---

## 1.3: Design Decisions

### Key Design Questions

#### 1. Architecture Pattern
**Question:** Which pattern fits best? (vertical slice, service layer, etc.)

**Decision:** [Chosen pattern]

**Rationale:** [Why this pattern over alternatives?]

#### 2. Feature Type
**Question:** What type of feature is this?

**Options:**
- ☐ **New Tool** - Creating a brand new agent tool
- ☐ **Tool Enhancement** - Adding operations to existing tool
- ☐ **Non-Tool Feature** - API endpoint, middleware, utility
- ☐ **Cross-Cutting Feature** - Affects multiple tools (e.g., batch support)

**Selected:** [Which type?]

**Implications:** [What does this mean for implementation?]

#### 3. API Design
**Parameters:**
- **Required parameters:** [List with types]
- **Optional parameters:** [List with types and defaults]
- **Return type:** [Type and structure]

**Error Handling:**
- [Error scenario 1]: [How handled]
- [Error scenario 2]: [How handled]

#### 4. Performance Considerations

**Performance Targets:**
| Operation | Scale | Target Latency | Measurement |
|-----------|-------|----------------|-------------|
| [Op 1] | Small (5 items) | < 100ms | p95 |
| [Op 1] | Medium (25 items) | < 500ms | p95 |
| [Op 1] | Large (100 items) | < 2s | p95 |

**Potential Bottlenecks:**
- [Bottleneck 1]: [How to optimize]
- [Bottleneck 2]: [How to optimize]

#### 5. Cross-Component Interaction

**Integration with Existing Systems:**
- **Tool 1**: [How they interact, boundaries]
- **Tool 2**: [How they interact, boundaries]

**Preventing Confusion/Overlap:**
- [Strategy 1]
- [Strategy 2]

**Boundaries to Enforce:**
- [Boundary 1]
- [Boundary 2]

---

## 1.4: Implementation Strategy

### Foundational Work Needed

**Before implementing the core feature:**

- [ ] Add new dependencies to `pyproject.toml`
  - [ ] `dependency-name>=version`
- [ ] Create shared utilities in `src/shared/` (if needed)
  - [ ] [Utility 1]
  - [ ] [Utility 2]
- [ ] Extend existing security validations (if needed)
  - [ ] [Validation 1]
- [ ] Set up environment variables in `.env.example` (if needed)
  - [ ] `NEW_VAR=value  # Description`
- [ ] Update configuration schemas (if needed)
  - [ ] [Config 1]

### Core Implementation Needed

**Main components to build:**

#### 1. Schemas (`src/tools/[tool_name]/schemas.py`)
- [ ] Define operation enums
- [ ] Create request model with validation
- [ ] Create response model
- [ ] Add Pydantic validators (@model_validator)

#### 2. Service Layer (`src/tools/[tool_name]/service.py`)
- [ ] Implement business logic functions
- [ ] Add error handling
- [ ] Add structured logging
- [ ] Add performance tracking
- [ ] Implement async operations (no blocking I/O)

#### 3. Tool Registration (`src/tools/[tool_name]/tool.py`)
- [ ] Register tool with Pydantic AI agent
- [ ] Write comprehensive agent-friendly docstring
  - [ ] "Use this when" section
  - [ ] "Do NOT use this for" section
  - [ ] Performance notes
  - [ ] Examples with realistic data
- [ ] Handle parameter extraction
- [ ] Format responses by verbosity level

#### 4. Additional Components (if applicable)
- [ ] [Component 1]
- [ ] [Component 2]

### Integration Work Needed

**How this integrates with existing systems:**

- [ ] Update tool registration in `src/agent/agent.py` (if new tool)
- [ ] Modify existing tool X to work with new feature (if enhancement)
- [ ] Update batch processor to support new operations (if batch support)
- [ ] Add system prompt guidance for tool selection (if tool confusion possible)
- [ ] Update shared utilities for new use cases (if needed)
- [ ] Add new routes/endpoints (if API changes)

---

# PHASE 2: Implementation

**Purpose:** Build the feature following established patterns and quality standards.

**IMPORTANT:** See `CLAUDE.md` for complete implementation standards. The sections below are summaries - always refer to CLAUDE.md for authoritative guidance.

---

## 2.1: Code Quality Standards Summary

### Type Safety (See CLAUDE.md for complete requirements)
- All functions MUST have type annotations
- All parameters MUST be typed
- Return types MUST be specified
- No `Any` types without explicit justification

### Documentation Standards (See CLAUDE.md for complete requirements)
- Google-style docstrings for all functions
- Enhanced agent-friendly docstrings for tools (with "Use this when" / "Do NOT use")
- Performance notes in tool docstrings
- Examples with realistic data

### Logging Standards (See CLAUDE.md for complete requirements)
- Structured logging with keyword arguments
- No string formatting in logs
- Exception logging with context
- No sensitive data in logs

### Security & Validation (See CLAUDE.md for complete requirements)
- Path validation using `validate_vault_path()`
- Input validation using Pydantic schemas
- Actionable error messages (what/why/how)

### Cross-Platform Compatibility (See CLAUDE.md for complete requirements)
- Use `pathlib.Path` (not `os.path`)
- Async operations (no blocking I/O)
- Platform-specific validations (Windows reserved names, etc.)

**→ Refer to CLAUDE.md for complete code examples and detailed standards**

---

## 2.2: Implementation Phases

### Phase 2a: Design & Schemas

**Tasks:**
- [ ] Define Pydantic schemas for requests/responses
- [ ] Create enums for operations/modes
- [ ] Add validation logic (@model_validator)
- [ ] Write schema tests

**Files:**
- `src/tools/[tool_name]/schemas.py`
- `tests/tools/[tool_name]/test_schemas.py`

**See CLAUDE.md for complete schema template**

---

### Phase 2b: Service Layer

**Tasks:**
- [ ] Implement business logic in service.py
- [ ] Add proper error handling
- [ ] Add structured logging
- [ ] Add performance tracking
- [ ] Write service unit tests

**Files:**
- `src/tools/[tool_name]/service.py`
- `tests/tools/[tool_name]/test_service.py`

**See CLAUDE.md for complete service template**

---

### Phase 2c: Tool Registration / Feature Integration

**Choose the appropriate implementation based on feature type:**

#### Option A: New Tool Creation

**Tasks:**
- [ ] Register tool with agent
- [ ] Write comprehensive docstring (use enhanced template from CLAUDE.md)
- [ ] Add parameter extraction
- [ ] Add response formatting
- [ ] Write tool integration tests

**Files:**
- `src/tools/[tool_name]/tool.py`
- `tests/tools/[tool_name]/test_tool.py`

**See CLAUDE.md for complete tool registration template and enhanced docstring requirements**

#### Option B: Enhancing Existing Tools

**Tasks:**
- [ ] Add new operation to existing enum
- [ ] Extend service layer with new operation logic
- [ ] Update tool docstring (add to "Use this when")
- [ ] Add tests for new operation

#### Option C: Non-Tool Features

**Examples:** API endpoints, middleware, utilities

**Tasks:**
- [ ] Implement feature in appropriate location
- [ ] Add integration with existing systems
- [ ] Write unit and integration tests
- [ ] Update documentation

#### Option D: Cross-Cutting Features

**Examples:** Adding batch support across multiple tools

**Tasks:**
- [ ] Identify all affected tools
- [ ] Implement shared logic in `src/shared/`
- [ ] Update each tool to use shared logic
- [ ] Add integration tests for cross-tool workflows
- [ ] Update documentation for all affected tools

---

### Phase 2d: Documentation

**Tasks:**
- [ ] Update README.md with tool usage
- [ ] Add examples to docstring
- [ ] Create tool-specific README if complex
- [ ] Document edge cases and limitations

**See CLAUDE.md for README template**

---

# PHASE 3: Testing & Validation

**Purpose:** Ensure feature works correctly across all scenarios and platforms.

---

## 3.1: Pre-Deployment Test Suite

### Test Suite Overview

Complete this checklist before merging to main:

| Test Category | # Tests | Duration | Automated | Command |
|---------------|---------|----------|-----------|---------|
| **Dependency Validation** | 4 checks | ~5 min | ✅ Yes | `uv sync --frozen` |
| **Linting & Type Check** | 4 checks | ~1 min | ✅ Yes | `uv run ruff check` + `mypy` |
| **Unit Tests** | [N]+ | ~30 sec | ✅ Yes | `pytest tests/tools/[tool]/ -m unit` |
| **Test Coverage** | 1 report | ~30 sec | ✅ Yes | `pytest --cov --cov-fail-under=90` |
| **Integration Tests** | [N] | ~10 sec | ✅ Yes | `pytest tests/integration/ -m integration` |
| **E2E Tests** | [N] | ~5 sec | ✅ Yes | `pytest tests/e2e/` |
| **Security Tests** | 6+ | ~5 sec | ✅ Yes | `pytest tests/security/` |
| **Platform Tests** | 9 | ~15 min | ✅ Yes (CI/CD) | GitHub Actions matrix |
| **Performance Tests** | [N] | ~2 min | ✅ Yes | `python tests/performance/[tool]_bench.py` |
| **Evaluation Tests** | 50 | ~5 min | ✅ Yes | `python tests/evaluation/[tool]_accuracy.py` |
| **UAT** | [N] scenarios | 30-60 min | ❌ No | Manual testing |
| **TOTAL** | **[Total]** | **~1-2 hours** | **Mostly automated** | See sections below |

**Success Criteria:** All automated tests pass + UAT sign-off (if applicable)

---

### 3.1.1: Dependency Validation (4 Checks)

**Duration:** ~5 minutes (automated)

✅ **Check 1: Dependency Installation**
```bash
uv sync --frozen
```

✅ **Check 2: Version Verification**
```bash
uv run python -c "import pytest; import mypy; import ruff"
```

✅ **Check 3: Security Audit**
```bash
uv run pip-audit
```

✅ **Check 4: Import Verification**
```bash
uv run python -c "from src.tools.[tool_name] import *"
```

---

### 3.1.2: Linting & Type Checking (4 Checks)

**Duration:** ~1 minute (automated)

✅ **Check 1: Ruff Linting**
```bash
uv run ruff check src/tools/[tool_name]/
```

✅ **Check 2: Ruff Formatting**
```bash
uv run ruff format --check src/tools/[tool_name]/
```

✅ **Check 3: MyPy Type Checking**
```bash
uv run mypy src/tools/[tool_name]/ --strict
```

✅ **Check 4: Type Coverage Report**
```bash
uv run mypy src/tools/[tool_name]/ --html-report mypy-report/
```

---

### 3.1.3: Unit Tests

**Duration:** ~30 seconds (automated)

**Command:**
```bash
uv run pytest tests/tools/[tool_name]/ -v -m unit
```

**Test Coverage Goals:**
- Service layer: >90%
- Schemas: >90%
- Tool: >80%
- Overall: >80%

---

### 3.1.4: Test Coverage Analysis

**Command:**
```bash
uv run pytest tests/tools/[tool_name]/ \
    --cov=src/tools/[tool_name] \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-fail-under=90
```

---

### 3.1.5: Integration Tests

**Command:**
```bash
uv run pytest tests/integration/ -v -m integration -k "[feature_name]"
```

---

### 3.1.6: E2E Tests

**Command:**
```bash
uv run pytest tests/e2e/ -v -k "[feature_name]"
```

---

### 3.1.7: Security Tests ⭐ CRITICAL

**Duration:** ~5 seconds (automated)

**Purpose:** Prevent security vulnerabilities

**Command:**
```bash
uv run pytest tests/security/test_[tool]_security.py -v
```

**Security Test Checklist:**

```python
import pytest

pytestmark = pytest.mark.security

class TestPathTraversalPrevention:
    """Test path traversal attacks are blocked."""

    async def test_relative_path_traversal_rejected(self, tmp_path):
        """Test ../../../etc/passwd is blocked."""
        with pytest.raises(SecurityError, match="path traversal"):
            await operation(path="../../../etc/passwd")

class TestAbsolutePathRejection:
    """Test absolute paths outside vault are rejected."""

    async def test_unix_absolute_path_rejected(self, tmp_path):
        """Test /etc/passwd is rejected."""
        with pytest.raises(SecurityError):
            await operation(path="/etc/passwd")

class TestSensitiveFolderProtection:
    """Test sensitive folders are protected."""

    async def test_obsidian_folder_protected(self, tmp_path):
        """Test .obsidian/ access is blocked."""
        with pytest.raises(SecurityError):
            await operation(path=".obsidian/config")

class TestCodeInjectionPrevention:
    """Test shell command injection is prevented."""

    async def test_shell_metacharacters_sanitized(self, tmp_path):
        """Test shell metacharacters are sanitized."""
        result = await operation(path="folder; rm -rf /")
        # Verify only folder operation performed

class TestSymlinkEscapePrevention:
    """Test symlinks pointing outside vault are blocked."""

    async def test_symlink_outside_vault_blocked(self, tmp_path):
        """Test symlink escape is prevented."""
        with pytest.raises(SecurityError):
            await operation(path="link_to_outside")

class TestDataPrivacy:
    """Test sensitive data is not logged."""

    async def test_no_sensitive_data_in_logs(self, caplog):
        """Test sensitive data not logged."""
        # Verify logs don't contain sensitive data
```

**Success Criteria:** All 6+ security tests pass

---

### 3.1.8: Platform Tests ⭐ IMPORTANT

**Duration:** ~15 minutes (automated via CI/CD, runs in parallel)

**Purpose:** Ensure cross-platform compatibility

**CI/CD Configuration:**
```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    python-version: ['3.11', '3.12']
```

**Platform Test Checklist:**

**Windows-Specific Tests:**
- [ ] Windows reserved names rejected (CON, PRN, AUX, NUL, COM1-9, LPT1-9)
- [ ] Backslash paths converted to forward slashes
- [ ] Case-insensitive filesystem handling
- [ ] Long path support (>260 chars)

**macOS-Specific Tests:**
- [ ] Case-sensitive APFS filesystem handling
- [ ] Unicode normalization (NFD vs NFC)
- [ ] `.DS_Store` ignored

**Linux-Specific Tests:**
- [ ] Case-sensitive filesystem handling
- [ ] Symlinks handled correctly
- [ ] File permissions preserved (chmod)

**Universal Tests:**
- [ ] Path normalization (always forward slashes)
- [ ] `pathlib.Path` used (not `os.path`)
- [ ] Async operations (no blocking I/O)
- [ ] Timestamps preserved

---

### 3.1.9: Performance Benchmarks

**Duration:** ~2 minutes (automated)

**Purpose:** Ensure performance targets met

**Command:**
```bash
uv run python tests/performance/[tool]_benchmark.py
```

**Performance Targets:**

| Operation | Scale | Target Latency | Measurement |
|-----------|-------|----------------|-------------|
| [Op 1] | Small (5 items) | < 100ms | p95 |
| [Op 1] | Medium (25 items) | < 500ms | p95 |
| [Op 1] | Large (100 items) | < 2s | p95 |

---

### 3.1.10: Evaluation Tests (For Agent Tools Only) ⭐

**Duration:** ~5 minutes (automated)

**Purpose:** Measure agent's ability to select correct tool

**When to Include:** New agent tools, modified tool docstrings, overlapping operations

**Command:**
```bash
uv run python tests/evaluation/[tool]_selection_accuracy.py
```

**Targets:**
- Obvious Cases: 100%
- Ambiguous Cases: >80%
- Edge Cases: >70%
- Wrong Tool: 100% (should NOT select)
- Mixed Operations: >90%
- **Overall: >95%**

---

## 3.2: User Acceptance Testing (UAT)

**Duration:** 30-60 minutes (manual)

**Purpose:** Validate feature meets user expectations and catches UX issues

**When to Include:**
- ✅ New tools that users will interact with
- ✅ Changes to existing user workflows
- ✅ Features with subjective "quality" criteria
- ❌ Internal refactoring with no user-facing changes

### UAT Scenario Template

```markdown
☐ **UAT Scenario 1: [Primary Use Case]** (10-15 min)
- **Setup:** [Preconditions]
- **Actions:**
  1. [Step 1]
  2. [Step 2]
- **Expected:** [Expected outcome]
- **Actual:** [Record actual]
- **Pass/Fail:** ☐ Pass ☐ Fail

☐ **UAT Scenario 2: [Edge Case]** (10-15 min)
- [...]

☐ **UAT Scenario 3: [Error Handling]** (10-15 min)
- [...]
```

### UAT Sign-Off

**Tester:** [Name]
**Date:** [Date]
**Overall Result:** ☐ Approved ☐ Not Approved ☐ N/A

---

## 3.3: Quality Gates ⭐ CRITICAL

All features must pass through these gates before proceeding:

### Gate 1: Pre-Deployment ✓

**Must Complete Before Merging to Main:**

- [ ] All 48+ automated tests pass
- [ ] Test coverage >90% (service layer)
- [ ] Linting & type checking: 0 errors
- [ ] **UAT sign-off obtained** (if manual testing required)
- [ ] Documentation updated
- [ ] Code review approved

---

### Gate 2: Staging Validation ✓ (Optional)

**Required if deploying to staging:**

- [ ] Staging deployment successful
- [ ] Staging smoke tests pass
- [ ] Performance acceptable
- [ ] No regressions detected
- [ ] **Manual staging verification** (10-15 min)

**Sign-Off Required:** ☐ Approved for production ☐ Not Approved

---

### Gate 3: Production Validation ✓ (Optional)

**Required if deploying to production:**

- [ ] Canary deployment (24 hours)
- [ ] Production rollout (25% → 50% → 100%)
- [ ] **Production Day 1 smoke test** (10 min)
- [ ] All metrics within targets

**Sign-Off Required:** ☐ Approved ☐ Rollback Required

---

### Gate 4: Post-Deployment Monitoring ✓ (Optional)

**Required for production features:**

- [ ] Week 1-4 health checks (10 min/week)
- [ ] User feedback collection
- [ ] Long-term monitoring (30+ days)

---

## 3.4: Edge Cases & Acceptance Criteria

### Edge Cases for Testing

#### Security Edge Cases
- [ ] Path traversal attempts
- [ ] Absolute paths outside vault
- [ ] Sensitive folder access
- [ ] Code injection attempts
- [ ] Symlinks pointing outside vault

#### Functional Edge Cases
- [ ] Empty inputs
- [ ] Special characters in names
- [ ] Unicode characters
- [ ] Very long inputs
- [ ] Concurrent operations

#### Platform-Specific Edge Cases
- [ ] Windows reserved names
- [ ] Case-sensitive vs insensitive filesystems
- [ ] Path separator differences
- [ ] Long path support
- [ ] File permissions

#### Performance Edge Cases
- [ ] Large batch operations
- [ ] Very large files
- [ ] Very large vaults
- [ ] Resource exhaustion scenarios

---

### Acceptance Criteria

#### Functional Requirements
- [ ] All [N] operations work correctly
- [ ] Cross-platform support (Windows, macOS, Linux)
- [ ] Security validation blocks dangerous operations
- [ ] Error messages clear and actionable
- [ ] All edge cases handled gracefully

#### Non-Functional Requirements
- [ ] Test coverage >90% on service layer
- [ ] All tests pass on 3 platforms
- [ ] Linting passes: 0 errors
- [ ] Type checking passes: 0 errors (strict mode)
- [ ] Performance targets met
- [ ] Token-efficient responses (for agent tools)
- [ ] Evaluation accuracy >95% (for agent tools)

#### Documentation Requirements
- [ ] Comprehensive tool docstring
- [ ] README updated with examples
- [ ] Edge cases documented
- [ ] Performance characteristics documented

#### Integration Requirements
- [ ] Tool registered (if new tool)
- [ ] Config updated (if needed)
- [ ] Dependencies added to pyproject.toml (if needed)

---

## 3.5: Validation Commands Reference

### Complete Test Execution Workflow

**Step 1: Dependency & Environment Setup**
```bash
uv sync --frozen
```

**Step 2: Linting & Type Checking**
```bash
uv run ruff check src/tools/[tool_name]/
uv run ruff check --fix src/tools/[tool_name]/
uv run ruff format src/tools/[tool_name]/
uv run mypy src/tools/[tool_name]/ --strict
```

**Step 3: Unit Tests**
```bash
uv run pytest tests/tools/[tool_name]/ -v -m unit \
    --cov=src/tools/[tool_name] \
    --cov-report=term-missing \
    --cov-fail-under=90
```

**Step 4: Integration Tests**
```bash
uv run pytest tests/integration/ -v -m integration -k "[feature_name]"
```

**Step 5: E2E Tests**
```bash
uv run pytest tests/e2e/ -v -k "[feature_name]"
```

**Step 6: Security Tests**
```bash
uv run pytest tests/security/ -v
```

**Step 7: Performance Benchmarks**
```bash
uv run python tests/performance/[tool]_benchmark.py
```

**Step 8: Evaluation Tests** (agent tools only)
```bash
uv run python tests/evaluation/[tool]_selection_accuracy.py
```

**Step 9: E2E Validation** (curl examples)

Start server:
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8030 --reload
```

**Example: Create Operation**
```bash
curl -X POST http://localhost:8030/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{
      "role": "user",
      "content": "[Feature-specific create command]"
    }]
  }'
```

**Step 10: Manual Validation Checklist**

- [ ] Feature works in OpenAI-compatible client
- [ ] Agent selects correct tool
- [ ] Error messages are clear and actionable
- [ ] Logging provides sufficient context
- [ ] Performance feels responsive
- [ ] Works on Windows/macOS/Linux

---

## 3.6: Deployment Validation (Optional)

**Include if deploying to production with staged rollout.**

### Stage 1: Local/Dev Validation
- [ ] Build succeeds
- [ ] Server starts
- [ ] Basic smoke test passes

### Stage 2: Staging Validation
- [ ] Staging deployment successful
- [ ] Staging smoke tests pass
- [ ] Manual verification (10-15 min)
- [ ] **Sign-off:** ☐ Approved for production

### Stage 3: Canary Deployment
- [ ] 5% traffic (24 hours)
- [ ] Error rate <1%
- [ ] Latency within targets

### Stage 4: Production Rollout
- [ ] 25% rollout (4 hours)
- [ ] 50% rollout (2 hours)
- [ ] 100% rollout (24 hours)
- [ ] Production Day 1 smoke test (10 min)

### Stage 5: Post-Deployment Monitoring
- [ ] Week 1-4 check-ins (10 min/week)
- [ ] User feedback collection
- [ ] Long-term monitoring (30+ days)

---

# Implementation Checklist

## Phase 0: Research & Discovery
- [ ] Explored existing codebase patterns
- [ ] Researched implementation options (2-5 options)
- [ ] Selected recommended approach with rationale
- [ ] Researched technologies & libraries
- [ ] Documented research with URLs
- [ ] Identified constraints
- [ ] Defined user story

## Phase 1: Planning & Design
- [ ] Wrote problem statement
- [ ] Defined user story
- [ ] Documented solution and rationale
- [ ] Completed context assessment
- [ ] Made key design decisions
- [ ] Created implementation strategy

## Phase 2: Implementation
- [ ] Schemas implemented
- [ ] Service layer implemented
- [ ] Tool registered / feature integrated
- [ ] Documentation written
- [ ] All code follows CLAUDE.md standards

## Phase 3: Testing & Validation
- [ ] All pre-deployment tests pass
- [ ] UAT completed (if applicable)
- [ ] All quality gates passed
- [ ] Edge cases documented and tested
- [ ] Acceptance criteria met
- [ ] Validation commands documented

## Final Sign-Off
- [ ] Code review approved
- [ ] QA approved
- [ ] Product owner approved
- [ ] Ready to merge to main

---

# Success Metrics Summary

## Technical Success
- ✅ All automated tests pass (90%+ coverage)
- ✅ 0 linting errors
- ✅ 0 type errors
- ✅ All security tests pass
- ✅ Cross-platform tests pass
- ✅ Performance targets met
- ✅ Evaluation accuracy >95% (if agent tool)

## User Success
- ✅ UAT approved (if applicable)
- ✅ Clear, actionable error messages
- ✅ Tool selection accurate
- ✅ User satisfaction >80%

## Business Success
- ✅ No rollback required
- ✅ No critical incidents
- ✅ Feature meets requirements
- ✅ Support tickets not increased

---

# Common Pitfalls to Avoid

❌ **Don't** use `os.path` - use `pathlib.Path`
❌ **Don't** use blocking I/O - use async operations
❌ **Don't** skip type hints - mypy strict mode required
❌ **Don't** use string formatting in logs - use structured kwargs
❌ **Don't** write vague error messages - be specific
❌ **Don't** skip validation - validate all inputs
❌ **Don't** test with toy data - use realistic scenarios
❌ **Don't** skip cross-platform testing - use CI/CD matrix
❌ **Don't** skip security tests - prevent vulnerabilities
❌ **Don't** skip UAT for user-facing features
❌ **Don't** skip quality gates

---

# Quick Reference: Command Summary

```bash
# Linting & Type Checking
uv run ruff check src/tools/[tool_name]/
uv run mypy src/tools/[tool_name]/ --strict

# Unit Tests
uv run pytest tests/tools/[tool_name]/ -v -m unit \
    --cov=src/tools/[tool_name] --cov-fail-under=90

# Integration Tests
uv run pytest tests/integration/ -v -m integration

# E2E Tests
uv run pytest tests/e2e/ -v

# Security Tests
uv run pytest tests/security/ -v

# Performance Benchmarks
uv run python tests/performance/[tool]_benchmark.py

# Evaluation Tests
uv run python tests/evaluation/[tool]_selection_accuracy.py

# Start server
uv run uvicorn src.main:app --host 0.0.0.0 --port 8030 --reload
```

---

**Version:** 2.0 (Enhanced with Phase 0 Research & comprehensive validation)
**Last Updated:** 2025-01-24
**Maintained By:** Development Team

**Use this template for every new feature to maintain codebase quality and enable reliable human and AI agent execution.**
