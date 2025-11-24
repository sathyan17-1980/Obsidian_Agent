# Generic Coding Agent Implementation Template

## Purpose

This document provides a standardized template for implementing features in the Obsidian Agent codebase. Use this template to create clear, actionable implementation plans that coding agents can execute end-to-end with high reliability.

---

## Template Structure

### 1. Mission Statement

**Define the feature clearly:**

```
[Feature Name]: [One-sentence description]

Problem: [What problem does this solve?]
Goal: [What should be achieved?]
Scope: [What's included and what's excluded?]
```

---

### 2. Context Assessment

**Current State:**
- ✅ What already exists and works?
- ⚠️ What problems exist?
- ❌ What's missing?

**Architecture:**
```
[Describe relevant parts of the codebase]
src/
├── [relevant directories]
└── [relevant files]

tests/
├── [test structure]
```

**Dependencies:**
- What other components does this interact with?
- What shared utilities are available?
- What external libraries are needed?

---

### 3. Design Decisions

**Key Design Questions:**

1. **Architecture Pattern**
   - Which pattern fits best? (vertical slice, service layer, etc.)
   - Why this pattern over alternatives?

2. **API Design**
   - What parameters are required vs optional?
   - What should the return type be?
   - How should errors be handled?

3. **Performance Considerations**
   - What are the performance targets?
   - What are potential bottlenecks?
   - How will we optimize?

4. **Cross-Component Interaction**
   - How does this integrate with existing tools?
   - How do we prevent confusion/overlap?
   - What boundaries must be enforced?

---

## Implementation Standards

### Code Quality Requirements

Based on `CLAUDE.md` principles:

#### 1. TYPE SAFETY IS NON-NEGOTIABLE ⭐

```python
# ✅ GOOD: Strict type annotations
def process_request(user_id: str, query: str) -> dict[str, Any]:
    """Process a user request and return results.

    Args:
        user_id: Unique identifier for the user.
        query: The search query string.

    Returns:
        Dictionary containing results and metadata.

    Raises:
        ValueError: If query is empty or invalid.
    """
    # Implementation

# ❌ BAD: Missing type hints
def process_request(user_id, query):
    # Implementation
```

**Requirements:**
- All functions MUST have type annotations
- All parameters MUST be typed
- Return types MUST be specified
- No `Any` types without explicit justification
- Strict mypy configuration enforced

#### 2. Documentation Standards

**Google-style docstrings for all functions:**

```python
def function_name(param1: str, param2: int = 10) -> str:
    """[One-line summary of what this does].

    [Optional longer description if needed]

    Args:
        param1: Description of param1.
            Additional context about when/how to use it.
        param2: Description of param2. Range: 1-100.
            Default: 10 (balanced performance).

    Returns:
        Description of return value.
        Format: [Structure details if complex].

    Raises:
        ValueError: If param2 is out of range.
        ProcessingError: If processing fails after retries.

    Examples:
        >>> function_name("example", 20)
        'result'
    """
```

**Agent Tool Docstrings (Special Requirements):**

For tools that LLMs will call, include:

```python
@agent.tool
async def tool_name(...) -> str:
    """[One-line summary].

    Use this when you need to:
    - [Specific scenario 1 where this tool is right choice]
    - [Specific scenario 2]
    - [Specific scenario 3]

    Do NOT use this for:
    - [Scenario where OTHER_TOOL should be used] (use other_tool instead)
    - [Scenario where ANOTHER_TOOL should be used] (use another_tool instead)
    - [Anti-pattern to avoid]

    Args:
        param: [Description + WHY you'd choose different values]
        response_format: Control output verbosity.
            - "minimal": [Description] (~50 tokens, use when [scenario])
            - "concise": [Description] (~150 tokens, default)
            - "detailed": [Description] (~1500+ tokens, use when [scenario])

    Returns:
        [Description of return value + format structure]

    Performance Notes:
        - Minimal format: ~50 tokens (use for [scenario])
        - Concise format: ~150 tokens (default)
        - Detailed format: ~1500+ tokens (only when needed)
        - Typical execution time: [duration]
        - Max [resource limit]: [value]

    Examples:
        # [Description of realistic scenario]
        tool_name(
            param="realistic/path/example.md",
            response_format="concise"
        )

        # [Another realistic scenario]
        tool_name(
            param="another/real/example.md",
            response_format="minimal"
        )
    """
```

#### 3. Logging Standards

**Philosophy:** Logs are for AI debugging. Include context for LLMs to understand issues.

```python
from src.shared.logging import get_logger

logger = get_logger(__name__)

# ✅ GOOD: Structured logging with context
logger.info(
    "operation_completed",
    operation="create",
    path="projects/alpha",
    duration_ms=45.2,
    items_processed=10
)

# ❌ BAD: String formatting
logger.info(f"Operation completed for {path}")

# ✅ GOOD: Exception logging with context
try:
    result = await operation()
except ValueError as e:
    logger.exception(
        "operation_failed",
        operation="create",
        path=path,
        expected="string",
        received=type(value).__name__
    )
    raise
```

**Required Logging:**
- Entry/exit for complex operations
- All exceptions with context
- Performance metrics (duration_ms)
- State transitions
- External API calls

**DO NOT Log:**
- Sensitive data (passwords, API keys, tokens)
- Spam in loops (log summaries instead)

---

### Security & Validation

#### Path Validation

```python
from src.shared.vault_security import validate_vault_path, is_path_allowed

# Always validate paths
full_path = validate_vault_path(vault_root, user_provided_path)

# Check against blocked patterns
if not is_path_allowed(path):
    raise SecurityError(f"Path blocked by security rules: {path}")
```

#### Input Validation

```python
from pydantic import BaseModel, Field, model_validator

class RequestModel(BaseModel):
    """Request schema with validation."""

    path: str = Field(description="Path to resource")
    operation: OperationEnum = Field(description="Operation to perform")

    @model_validator(mode="after")
    def validate_operation_params(self) -> "RequestModel":
        """Validate operation-specific requirements.

        Returns:
            Validated request.

        Raises:
            ValueError: If validation fails.
        """
        if self.operation == Operation.DELETE and not self.confirm:
            raise ValueError("DELETE requires confirmation")
        return self
```

#### Error Messages

**Principle:** Every error should tell user:
1. What went wrong
2. Why it went wrong
3. How to fix it

```python
# ✅ GOOD: Actionable error
raise ValueError(
    f"Invalid folder name: '{name}' is a reserved Windows name.\n"
    f"Try: 'config' or 'constants' instead."
)

# ❌ BAD: Vague error
raise ValueError("Invalid name")
```

---

### Testing Requirements

#### Test Structure

**Mirror source structure:**
```
src/tools/my_tool/
├── tool.py
├── schemas.py
└── service.py

tests/tools/my_tool/
├── test_tool.py      # Tool registration tests
├── test_schemas.py   # Schema validation tests
└── test_service.py   # Service layer unit tests
```

#### Test Categories

**1. Unit Tests** (`@pytest.mark.unit`)

```python
import pytest
from src.tools.my_tool.service import my_service_function

pytestmark = pytest.mark.unit

class TestMyServiceFunction:
    """Tests for my_service_function."""

    async def test_basic_operation(self, tmp_path):
        """Test basic operation succeeds."""
        # Setup
        vault = tmp_path / "vault"
        vault.mkdir()

        # Execute
        result = await my_service_function(...)

        # Assert
        assert result.success is True
        assert result.data == expected_data

    async def test_error_handling(self, tmp_path):
        """Test error is raised for invalid input."""
        with pytest.raises(ValueError, match="expected error message"):
            await my_service_function(invalid_input)

    async def test_edge_case(self, tmp_path):
        """Test edge case behavior."""
        # Test boundary conditions
```

**Test Coverage Goals:**
- 90%+ coverage on service layer
- 80%+ coverage overall
- All error paths tested
- All edge cases covered

**2. Integration Tests** (`@pytest.mark.integration`)

```python
pytestmark = pytest.mark.integration

class TestEndToEndWorkflow:
    """Integration tests for complete workflows."""

    async def test_multi_step_workflow(self, tmp_path):
        """Test complete workflow: create → update → delete."""
        # Step 1: Create
        result1 = await create_operation(...)
        assert result1.success is True

        # Step 2: Update
        result2 = await update_operation(...)
        assert result2.success is True

        # Step 3: Delete
        result3 = await delete_operation(...)
        assert result3.success is True
```

**3. Cross-Platform Tests**

```python
import platform

class TestCrossPlatform:
    """Tests for cross-platform compatibility."""

    async def test_path_normalization(self, tmp_path):
        """Test paths work on Windows, macOS, Linux."""
        # Test with both separators
        result = await operation(path="folder/subfolder")
        assert result.success is True

        # Verify path uses forward slashes (Obsidian standard)
        assert "\\" not in result.path

    @pytest.mark.skipif(
        platform.system() != "Windows",
        reason="Windows-specific test"
    )
    async def test_windows_reserved_names(self, tmp_path):
        """Test Windows reserved names rejected."""
        with pytest.raises(ValueError, match="reserved"):
            await create_folder("CON")
```

#### Test Data Strategy

**Use realistic data:**

```python
# ✅ GOOD: Realistic test data
test_vault = tmp_path / "vault"
(test_vault / "projects" / "2025").mkdir(parents=True)
(test_vault / "projects" / "2025" / "alpha.md").write_text(
    "---\ntitle: Project Alpha\ntags: [project, active]\n---\n\n# Overview\n\nContent here"
)

# ❌ BAD: Toy test data
(tmp_path / "foo").mkdir()
(tmp_path / "foo" / "bar.md").write_text("test")
```

---

### Performance Standards

#### Benchmarks

Set clear performance targets:

```python
# Performance targets for operations
PERFORMANCE_TARGETS = {
    "create": 50,      # ms
    "read": 100,       # ms
    "update": 200,     # ms
    "delete": 50,      # ms
    "search": 500,     # ms for 1000 items
}
```

#### Token Efficiency (for Agent Tools)

**3-tier response system:**

| Format | Tokens | Use Case |
|--------|--------|----------|
| minimal | ~50 | Confirmations, existence checks |
| concise | ~150 | Default, balanced |
| detailed | ~1500+ | Full content needed |

**Implementation:**

```python
def format_response(data: dict, format: ResponseFormat) -> dict:
    """Format response based on verbosity level."""
    if format == ResponseFormat.MINIMAL:
        return {
            "status": data["status"],
            "token_estimate": 50
        }
    elif format == ResponseFormat.CONCISE:
        return {
            "status": data["status"],
            "summary": data["summary"][:100],
            "token_estimate": 150
        }
    else:  # DETAILED
        return {
            **data,
            "token_estimate": estimate_tokens(data)
        }
```

---

### Cross-Platform Compatibility

#### Path Handling

```python
from pathlib import Path

# ✅ GOOD: Use pathlib.Path
path = Path(user_input)
full_path = vault_root / path
normalized = str(full_path).replace("\\", "/")

# ❌ BAD: Use os.path
import os
path = os.path.join(vault_root, user_input)
```

#### File Operations

```python
import aioshutil
import aiofiles

# ✅ GOOD: Async operations
await aioshutil.move(str(source), str(dest))

async with aiofiles.open(path, 'r', encoding='utf-8') as f:
    content = await f.read()

# ❌ BAD: Blocking operations
shutil.move(source, dest)
with open(path) as f:
    content = f.read()
```

#### Platform-Specific Validations

```python
# Validate against most restrictive platform
WINDOWS_RESERVED = {"CON", "PRN", "AUX", "NUL", ...}
INVALID_CHARS = {"<", ">", ":", '"', "|", "?", "*", "/", "\\"}

def validate_name(name: str) -> None:
    """Validate name works on all platforms."""
    # Check Windows reserved (even on Linux/macOS)
    if name.upper() in WINDOWS_RESERVED:
        raise ValueError(f"'{name}' is reserved on Windows")

    # Check invalid chars (union of all platforms)
    invalid = set(name) & INVALID_CHARS
    if invalid:
        raise ValueError(f"Invalid characters: {invalid}")
```

---

## Implementation Template

### Phase 1: Design & Schemas

**Tasks:**
- [ ] Define Pydantic schemas for requests/responses
- [ ] Create enums for operations/modes
- [ ] Add validation logic (@model_validator)
- [ ] Write schema tests

**Files:**
- `src/tools/[tool_name]/schemas.py`
- `tests/tools/[tool_name]/test_schemas.py`

**Template:**

```python
# schemas.py
from enum import Enum
from pydantic import BaseModel, Field, model_validator

class OperationEnum(str, Enum):
    """Operations supported by this tool."""
    OP1 = "op1"
    OP2 = "op2"

class ToolRequest(BaseModel):
    """Request schema for tool operation."""

    path: str = Field(description="Path to resource")
    operation: OperationEnum = Field(description="Operation to perform")

    @model_validator(mode="after")
    def validate_params(self) -> "ToolRequest":
        """Validate operation-specific params."""
        if self.operation == OperationEnum.OP1:
            # Validate OP1 requirements
            pass
        return self

class ToolResult(BaseModel):
    """Result from tool operation."""

    success: bool = Field(description="Whether operation succeeded")
    message: str = Field(description="Human-readable status")
    data: dict[str, Any] = Field(default_factory=dict)
    token_estimate: int = Field(default=50)
```

---

### Phase 2: Service Layer

**Tasks:**
- [ ] Implement business logic in service.py
- [ ] Add proper error handling
- [ ] Add structured logging
- [ ] Add performance tracking
- [ ] Write service unit tests

**Files:**
- `src/tools/[tool_name]/service.py`
- `tests/tools/[tool_name]/test_service.py`

**Template:**

```python
# service.py
import time
from pathlib import Path
from src.shared.logging import get_logger
from src.shared.vault_security import validate_vault_path

logger = get_logger(__name__)

async def operation_service(
    request: ToolRequest,
    vault_path: str,
) -> ToolResult:
    """Execute operation.

    Args:
        request: Validated request.
        vault_path: Vault root path.

    Returns:
        Operation result.

    Raises:
        ValueError: If validation fails.
        FileNotFoundError: If resource not found.
    """
    start_time = time.perf_counter()

    # Validate path
    full_path = validate_vault_path(vault_path, request.path)

    logger.info(
        "operation_started",
        operation=request.operation.value,
        path=request.path
    )

    try:
        # Execute operation
        result = await _execute_operation(request, Path(full_path))

        duration_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            "operation_completed",
            operation=request.operation.value,
            path=request.path,
            success=result.success,
            duration_ms=duration_ms
        )

        return result

    except Exception as e:
        logger.exception(
            "operation_failed",
            operation=request.operation.value,
            path=request.path,
            error=str(e)
        )
        raise

async def _execute_operation(
    request: ToolRequest,
    full_path: Path
) -> ToolResult:
    """Execute specific operation logic."""
    # Implementation
    pass
```

---

### Phase 3: Tool Registration

**Tasks:**
- [ ] Register tool with agent
- [ ] Write comprehensive docstring (use template above)
- [ ] Add parameter extraction
- [ ] Add response formatting
- [ ] Write tool integration tests

**Files:**
- `src/tools/[tool_name]/tool.py`
- `tests/tools/[tool_name]/test_tool.py`

**Template:**

```python
# tool.py
from typing import TYPE_CHECKING
from pydantic_ai import RunContext
from src.agent.schemas import AgentDependencies
from src.shared.logging import get_logger

if TYPE_CHECKING:
    from pydantic_ai import Agent

logger = get_logger(__name__)

def register_tool(agent: "Agent[AgentDependencies, str]") -> None:
    """Register tool with agent."""

    @agent.tool
    async def tool_name(
        ctx: RunContext["AgentDependencies"],
        path: str,
        operation: str,
        response_format: str = "concise",
    ) -> str:
        """[Comprehensive docstring - see template above]"""

        # Validate operation
        try:
            op_enum = OperationEnum(operation)
        except ValueError:
            return f"Invalid operation: {operation}"

        # Create request
        try:
            request = ToolRequest(
                path=path,
                operation=op_enum,
                response_format=response_format,  # type: ignore
            )
        except ValueError as e:
            logger.error("invalid_request", error=str(e))
            return f"Invalid request: {e}"

        # Execute service
        try:
            result = await operation_service(
                request=request,
                vault_path=ctx.deps.vault_path,
            )

            if not result.success:
                return f"Operation failed: {result.message}"

            # Format response
            return f"✓ {result.message}\n(~{result.token_estimate} tokens)"

        except Exception as e:
            logger.exception("tool_execution_failed", path=path)
            return f"Error: {e}"

    logger.info("tool_registered", tool="tool_name")
```

---

### Phase 4: Testing

**Tasks:**
- [ ] Write unit tests (90%+ coverage target)
- [ ] Write integration tests
- [ ] Write cross-platform tests
- [ ] Set up CI/CD matrix
- [ ] Run performance benchmarks

**CI/CD Template:**

```yaml
# .github/workflows/test-[feature].yml
name: Test [Feature]

on:
  push:
    paths:
      - 'src/tools/[tool_name]/**'
      - 'tests/tools/[tool_name]/**'
  pull_request:
    paths:
      - 'src/tools/[tool_name]/**'
      - 'tests/tools/[tool_name]/**'

jobs:
  test:
    name: Test on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}

    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Set up Python
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync

      - name: Run linting
        run: |
          uv run ruff check src/tools/[tool_name]/
          uv run mypy src/tools/[tool_name]/

      - name: Run tests
        run: uv run pytest tests/tools/[tool_name]/ -v --cov=src/tools/[tool_name]
```

---

### Phase 5: Documentation

**Tasks:**
- [ ] Update README.md with tool usage
- [ ] Add examples to docstring
- [ ] Create tool-specific README if complex
- [ ] Document edge cases and limitations

**README Template:**

```markdown
### [Tool Number]. [tool_name] - [Brief Description]

[2-3 sentence overview of what the tool does]

```python
# Example 1: [Common use case]
tool_name(
    path="realistic/example/path",
    operation="common_op",
    response_format="concise"
)

# Example 2: [Another common use case]
tool_name(
    path="another/realistic/path",
    operation="another_op",
    response_format="minimal"
)
```

**Features:**
- ✅ [Feature 1]
- ✅ [Feature 2]
- ✅ [Feature 3]

**Performance:**
- [Operation 1]: ~[time]ms, ~[tokens] tokens
- [Operation 2]: ~[time]ms, ~[tokens] tokens
```

---

## Checklist for Complete Implementation

### Code Quality
- [ ] All functions have type annotations
- [ ] All functions have Google-style docstrings
- [ ] Agent tools have enhanced docstrings (use this when/do not use)
- [ ] Structured logging used throughout
- [ ] No string formatting in logs (use kwargs)
- [ ] Error messages are clear and actionable
- [ ] Linters pass: `ruff check` and `mypy` with no errors

### Security
- [ ] Path validation using `validate_vault_path()`
- [ ] Input validation using Pydantic schemas
- [ ] Sensitive data not logged
- [ ] Critical resources protected
- [ ] Error messages don't leak sensitive info

### Testing
- [ ] Unit tests written (90%+ coverage target)
- [ ] Integration tests written
- [ ] Cross-platform tests written
- [ ] All tests pass on Linux, macOS, Windows
- [ ] Edge cases covered
- [ ] Error paths tested
- [ ] Performance benchmarks documented

### Documentation
- [ ] README updated with examples
- [ ] Docstrings complete
- [ ] Edge cases documented
- [ ] Performance characteristics documented
- [ ] Migration guide (if breaking changes)

### Performance
- [ ] Performance targets met
- [ ] Token efficiency implemented (for agent tools)
- [ ] Async operations used (no blocking I/O)
- [ ] Resource limits enforced

### Integration
- [ ] Tool registered in agent
- [ ] Config updated (if needed)
- [ ] Environment variables documented (if needed)
- [ ] Dependencies added to pyproject.toml (if needed)

---

## Success Criteria Template

**After implementation:**

✅ **Functional Requirements**
- [ ] All [N] operations work correctly
- [ ] Cross-platform support (Windows, macOS, Linux)
- [ ] Security validation blocks dangerous operations
- [ ] Error messages clear and actionable

✅ **Non-Functional Requirements**
- [ ] 90%+ test coverage on service layer
- [ ] All tests pass on 3 platforms (CI/CD)
- [ ] Performance targets met
- [ ] Token-efficient responses (for agent tools)

✅ **Documentation Requirements**
- [ ] Comprehensive tool docstring
- [ ] README with examples
- [ ] Testing guide
- [ ] Performance characteristics documented

---

## Common Pitfalls to Avoid

❌ **Don't** use `os.path` - use `pathlib.Path`
❌ **Don't** use blocking I/O - use async operations
❌ **Don't** skip type hints - mypy strict mode requires them
❌ **Don't** use string formatting in logs - use structured kwargs
❌ **Don't** write vague error messages - be specific and actionable
❌ **Don't** skip validation - validate all inputs
❌ **Don't** forget path normalization - always use forward slashes
❌ **Don't** test with toy data - use realistic test scenarios
❌ **Don't** skip cross-platform testing - use CI/CD matrix
❌ **Don't** forget to update documentation - keep it current

---

## Example: Applying Template to New Feature

### Feature: Add "Duplicate Note" Functionality

**1. Mission**
```
Feature: Duplicate Note Tool
Problem: Users need to create copies of notes with modified titles/paths
Goal: One-shot duplication with wikilink preservation
Scope: Single note duplication (not batch)
```

**2. Context**
```
Current State:
- ✅ note_manage has read/write operations
- ✅ wikilink parsing exists in obsidian_parsers.py
- ❌ No duplication functionality

Architecture:
- Extend obsidian_note_manager or create new tool?
- Decision: Add to note_manager (consolidation principle)
```

**3. Design**
```
Operation: "duplicate"
Parameters:
  - source_path: str (note to duplicate)
  - dest_path: str (new note path)
  - update_title: bool = True (update title in frontmatter)
  - response_format: str = "concise"

Flow:
1. Read source note
2. Parse frontmatter
3. Update title if requested
4. Write to destination
5. Return success with paths
```

**4. Implementation Phases**
- Phase 1: Add "duplicate" to NoteOperation enum
- Phase 2: Implement _duplicate_note() in service.py
- Phase 3: Update tool registration
- Phase 4: Write 8+ tests
- Phase 5: Update README

**5. Testing Plan**
```
- test_duplicate_simple_note
- test_duplicate_updates_title
- test_duplicate_preserves_frontmatter
- test_duplicate_destination_exists_error
- test_duplicate_source_not_found_error
- test_duplicate_dry_run
```

---

## Quick Reference

### File Creation Order

1. `schemas.py` - Define data models
2. `service.py` - Implement business logic
3. `tool.py` - Register with agent
4. `test_schemas.py` - Test validation
5. `test_service.py` - Test operations
6. `test_tool.py` - Test integration
7. Update `README.md`
8. Update `.env.example` (if config changes)

### Command Quick Reference

```bash
# Run tests
uv run pytest tests/tools/[tool_name]/ -v

# Run linters
uv run ruff check src/tools/[tool_name]/
uv run mypy src/tools/[tool_name]/

# Check coverage
uv run pytest tests/tools/[tool_name]/ --cov=src/tools/[tool_name] --cov-report=term-missing

# Run specific test
uv run pytest tests/tools/[tool_name]/test_service.py::TestClass::test_method -v

# Format code
uv run ruff check --fix src/tools/[tool_name]/
```

---

## Conclusion

This template ensures:
1. **Consistency** - All features follow same patterns
2. **Quality** - Type safety, testing, documentation enforced
3. **Reliability** - Clear error handling and validation
4. **Maintainability** - Structured code, comprehensive tests
5. **Agent-friendly** - Clear docstrings, token efficiency

**Use this template for every new feature to maintain codebase quality and enable reliable agent execution.**
