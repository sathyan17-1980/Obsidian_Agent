# Testing and Validation Strategy: Folder Management Enhancement

**Related Plan**: FOLDER-MANAGEMENT-ENHANCEMENT-PLAN.md
**Feature**: Obsidian Folder Management Tool Enhancement
**Version**: 1.0
**Date**: 2025-01-22

---

## Overview

This document provides a comprehensive testing and validation strategy for the folder management enhancement feature. It details all testing types, validation approaches, acceptance criteria, and quality assurance processes.

### Testing Pyramid Summary

```
                [E2E/Acceptance Tests]           2 tests
                        |
                        |
            [Integration Tests]               10 tests
                    |
                    |
        [Unit Tests]                          30+ tests
            |
            |
[Static Analysis & Linting]                 Continuous
```

**Total Test Count**: 42+ automated tests
**Manual Validation Scenarios**: 8 scenarios
**Quality Gates**: 10 gates
**Target Coverage**: >90% on service layer

---

## 1. Pre-Deployment Validation

**Purpose**: Comprehensive validation before deployment to ensure code quality, security, and correctness.

All pre-deployment validations must pass before code is merged to main branch. These validations are automated via CI/CD and run on every pull request.

---

### 1.1 Dependency Validation

**Purpose**: Ensure all dependencies are correctly specified, compatible, and secure.

#### Validation 1.1.1: Dependency Installation Check
**Tool**: UV package manager
**Command**:
```bash
uv sync --frozen
```

**Validates**:
- [ ] All dependencies in `pyproject.toml` can be resolved
- [ ] No conflicting version requirements
- [ ] Lock file (if exists) matches pyproject.toml
- [ ] Installation completes without errors
- [ ] Python version requirement met (>=3.12)

**Success Criteria**: Exit code 0, all packages installed

**Failure Handling**:
- Check pyproject.toml for version conflicts
- Update dependency versions if needed
- Regenerate lock file: `uv lock`

---

#### Validation 1.1.2: Dependency Version Verification
**Tool**: UV + custom script
**Command**:
```bash
uv pip list --format=json | python scripts/check_versions.py
```

**Validates**:
- [ ] Core dependencies present:
  - `fastapi >= 0.119.0`
  - `pydantic >= 2.12.2`
  - `pydantic-ai >= 1.0.18`
  - `structlog >= 25.4.0`
  - `aiofiles >= 25.1.0`
  - `aioshutil >= 1.3`
- [ ] Dev dependencies present:
  - `pytest >= 8.4.2`
  - `pytest-asyncio >= 1.2.0`
  - `pytest-cov >= 4.0.0` (if coverage enabled)
  - `mypy >= 1.18.2`
  - `ruff >= 0.14.0`

**Success Criteria**: All required dependencies at minimum versions

---

#### Validation 1.1.3: Dependency Security Audit
**Tool**: `pip-audit` or `safety` (if available)
**Command**:
```bash
uv pip list --format=json | safety check --stdin
# OR
pip-audit
```

**Validates**:
- [ ] No known security vulnerabilities in dependencies
- [ ] No deprecated packages with security issues
- [ ] All CVE warnings addressed

**Success Criteria**: 0 high/critical vulnerabilities

**Acceptable**: Low/medium vulnerabilities with documented acceptance

---

#### Validation 1.1.4: Import Verification
**Tool**: Python import check
**Command**:
```bash
python -c "
import src.tools.obsidian_folder_manager.tool
import src.tools.obsidian_folder_manager.schemas
import src.tools.obsidian_folder_manager.service
import src.shared.config
import src.shared.logging
import src.shared.vault_security
print('All imports successful')
"
```

**Validates**:
- [ ] All source modules can be imported
- [ ] No import errors or circular dependencies
- [ ] All third-party imports available

**Success Criteria**: No ImportError exceptions

---

### 1.2 Linting and Type Checking

**Purpose**: Enforce code quality standards and type safety.

#### Validation 1.2.1: Ruff Linting
**Tool**: Ruff
**Command**:
```bash
uv run ruff check src/tools/obsidian_folder_manager/ --output-format=github
uv run ruff check src/shared/config.py --output-format=github
```

**Configuration**: Uses ruff defaults + project-specific rules

**Validates**:
- [ ] No syntax errors
- [ ] No unused imports
- [ ] No undefined variables
- [ ] PEP 8 compliance (line length, naming conventions)
- [ ] No complexity issues (if configured)
- [ ] Import ordering correct
- [ ] No common anti-patterns

**Success Criteria**:
- **MUST**: 0 errors
- **SHOULD**: 0 warnings
- **Acceptable**: Warnings with documented rationale (e.g., `# noqa: <code>`)

**Failure Handling**:
```bash
# Auto-fix what can be fixed
uv run ruff check --fix src/tools/obsidian_folder_manager/

# Review remaining issues manually
uv run ruff check src/tools/obsidian_folder_manager/
```

---

#### Validation 1.2.2: Ruff Formatting
**Tool**: Ruff formatter
**Command**:
```bash
uv run ruff format --check src/tools/obsidian_folder_manager/
uv run ruff format --check src/shared/config.py
```

**Validates**:
- [ ] Code formatted consistently
- [ ] Line length compliance (<100 chars)
- [ ] Indentation correct (4 spaces)
- [ ] String quote consistency

**Success Criteria**: 0 files need reformatting

**Failure Handling**:
```bash
# Auto-format all files
uv run ruff format src/tools/obsidian_folder_manager/
```

---

#### Validation 1.2.3: MyPy Type Checking (Strict Mode)
**Tool**: MyPy
**Command**:
```bash
uv run mypy src/tools/obsidian_folder_manager/ --strict
uv run mypy src/shared/config.py --strict
```

**Configuration** (from `pyproject.toml`):
```toml
[tool.mypy]
python_version = "3.12"
strict = true
disallow_untyped_defs = true
disallow_any_generics = true
disallow_untyped_calls = true
warn_return_any = true
warn_unused_configs = true
```

**Validates**:
- [ ] All functions have type hints
- [ ] All parameters typed
- [ ] All return values typed
- [ ] No `Any` types without justification
- [ ] No untyped function calls
- [ ] No implicit optionals
- [ ] Generics properly typed

**Success Criteria**:
- **MUST**: 0 errors
- **Code Coverage**: 100% of functions have type annotations

**Common Patterns**:
```python
# ✅ GOOD: Full type annotations
async def archive_folder(
    full_path: Path,
    request: ManageFolderRequest,
    vault_path: str,
) -> FolderOperationResult:
    ...

# ❌ BAD: No type annotations
async def archive_folder(full_path, request, vault_path):
    ...

# ❌ BAD: Using Any
from typing import Any
def process(data: Any) -> Any:
    ...
```

---

#### Validation 1.2.4: Type Coverage Report
**Tool**: MyPy with coverage report
**Command**:
```bash
uv run mypy src/tools/obsidian_folder_manager/ --strict --html-report mypy-report/
```

**Validates**:
- [ ] Type coverage >99% (target: 100%)
- [ ] No untyped code paths
- [ ] All public APIs fully typed

**Success Criteria**: HTML report shows >99% typed

---

### 1.3 Unit Tests (Pytest)

**Purpose**: Test individual components in isolation.

#### Validation 1.3.1: Run All Unit Tests
**Tool**: Pytest
**Command**:
```bash
uv run pytest tests/tools/obsidian_folder_manager/ -v -m unit
```

**Configuration** (from `pyproject.toml`):
```toml
[tool.pytest.ini_options]
addopts = "--strict-markers --strict-config -ra"
asyncio_mode = "auto"
markers = [
    "unit: Unit tests that test individual components in isolation",
]
```

**Test Categories**:
1. **Path Validation Tests** (5 tests)
   - `tests/tools/obsidian_folder_manager/test_service.py::TestPathValidation`

2. **Archive Operation Tests** (10 tests)
   - `tests/tools/obsidian_folder_manager/test_service.py::TestArchiveFolderOperation`

3. **Schema Validation Tests** (5 tests)
   - `tests/tools/obsidian_folder_manager/test_schemas.py::TestSchemaValidation`

4. **Error Handling Tests** (8 tests)
   - `tests/tools/obsidian_folder_manager/test_error_handling.py::TestErrorHandling`

5. **Wikilink Update Tests** (6 tests)
   - `tests/tools/obsidian_folder_manager/test_wikilink_updates.py::TestWikilinkUpdates`

**Validates**:
- [ ] All unit tests pass
- [ ] 0 failures
- [ ] 0 errors
- [ ] 0 skipped tests (unless intentionally skipped with reason)
- [ ] Test duration reasonable (<30 seconds total)

**Success Criteria**:
- **MUST**: All 30+ unit tests pass
- **Performance**: Test suite <30 seconds
- **Isolation**: Each test independent (can run in any order)

---

#### Validation 1.3.2: Test Coverage Analysis
**Tool**: pytest-cov
**Command**:
```bash
uv run pytest tests/tools/obsidian_folder_manager/ \
    --cov=src/tools/obsidian_folder_manager/ \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=json \
    --cov-fail-under=90
```

**Validates**:
- [ ] Overall coverage >90%
- [ ] `service.py` coverage >90%
- [ ] `tool.py` coverage >80% (tool registration has limited testability)
- [ ] `schemas.py` coverage >90%
- [ ] No critical code paths untested

**Success Criteria**:
- **MUST**: Overall >90% coverage
- **MUST**: service.py >90%
- **Critical Paths**: 100% coverage on error handling, security validation, wikilink updates

**Output Formats**:
- **Terminal**: Summary with missing lines
- **HTML**: `htmlcov/index.html` - Visual report
- **JSON**: `coverage.json` - Machine-readable for CI/CD

**Coverage Review Checklist**:
- [ ] All `validate_folder_path()` branches covered
- [ ] All `_archive_folder()` branches covered
- [ ] Error handling paths covered
- [ ] Edge cases covered (empty folders, special characters, etc.)

---

#### Validation 1.3.3: Test Quality Checks
**Tool**: Pytest with custom checks
**Command**:
```bash
# Check for test smells
uv run pytest tests/tools/obsidian_folder_manager/ --collect-only | grep "test_"

# Verify test naming conventions
find tests/tools/obsidian_folder_manager/ -name "test_*.py" | xargs grep -L "class Test"
```

**Validates**:
- [ ] All test functions start with `test_`
- [ ] All test classes start with `Test`
- [ ] All test files start with `test_`
- [ ] Test docstrings present and descriptive
- [ ] Tests use proper fixtures (tmp_path, etc.)
- [ ] No test interdependencies
- [ ] No hardcoded paths or data

**Success Criteria**: All tests follow conventions

---

### 1.4 Integration Tests

**Purpose**: Test multiple components working together.

#### Validation 1.4.1: Run All Integration Tests
**Tool**: Pytest
**Command**:
```bash
uv run pytest tests/integration/ -v -m integration
```

**Test Categories**:
1. **Tool Integration** (4 tests)
   - Tool-to-service integration
   - Response format validation
   - Parameter passing

2. **System Prompt Integration** (2 tests)
   - Decision tree presence
   - Prompt formatting

3. **Cross-Component Integration** (4 tests)
   - Vault security integration
   - Obsidian parsers integration
   - Logging integration
   - Config integration

**Validates**:
- [ ] All integration tests pass
- [ ] Components interact correctly
- [ ] Data flows properly between layers
- [ ] No integration bugs

**Success Criteria**: All 10 integration tests pass

---

#### Validation 1.4.2: End-to-End Workflow Tests
**Tool**: Pytest
**Command**:
```bash
uv run pytest tests/e2e/ -v
```

**Test Scenarios**:
1. **Complete Archive Workflow** (1 test)
   - User request → tool selection → execution → result

2. **Error Recovery Workflow** (1 test)
   - Wrong tool → error → self-correction

**Validates**:
- [ ] Full workflows complete successfully
- [ ] User experience smooth
- [ ] Error recovery works

**Success Criteria**: Both E2E tests pass

---

### 1.5 Security Tests

**Purpose**: Ensure security vulnerabilities are prevented.

#### Validation 1.5.1: Security Unit Tests
**Tool**: Pytest with security focus
**Command**:
```bash
uv run pytest tests/security/ -v
```

**File**: `tests/security/test_folder_security.py` (new file)

**Test Categories**:

**1. Path Traversal Prevention** (2 tests)
```python
async def test_directory_traversal_blocked():
    """Test that directory traversal attacks are prevented."""
    attack_paths = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32",
        "projects/../../sensitive",
        "folder/../../../etc",
    ]

    for path in attack_paths:
        request = ManageFolderRequest(path=path, operation=FolderOperation.CREATE)
        with pytest.raises(ValueError, match="invalid path"):
            await manage_folder_service(request, vault_path="/vault")

async def test_absolute_path_rejected():
    """Test that absolute paths are rejected."""
    absolute_paths = [
        "/etc/passwd",
        "C:\\Windows\\System32",
        "/home/user/.ssh",
    ]

    for path in absolute_paths:
        request = ManageFolderRequest(path=path, operation=FolderOperation.CREATE)
        with pytest.raises(ValueError, match="must be relative"):
            await manage_folder_service(request, vault_path="/vault")
```

**2. Sensitive Folder Protection** (1 test)
```python
async def test_sensitive_folders_protected():
    """Test that sensitive folders are protected from operations."""
    protected = [".obsidian", ".git", ".trash", ".DS_Store"]

    for folder in protected:
        request = ManageFolderRequest(path=folder, operation=FolderOperation.DELETE)
        with pytest.raises(ValueError, match="protected"):
            await manage_folder_service(request, vault_path="/vault")
```

**3. Code Injection Prevention** (1 test)
```python
async def test_no_code_injection():
    """Test that folder names cannot inject code."""
    malicious_names = [
        "folder; rm -rf /",
        "folder && cat /etc/passwd",
        "folder$(malicious command)",
        "folder' OR '1'='1",
        "folder`whoami`",
    ]

    for name in malicious_names:
        # Should treat as literal string, not execute
        # May create folder or reject based on validation
        # But MUST NOT execute commands
        request = ManageFolderRequest(path=name, operation=FolderOperation.CREATE)
        # Either succeeds with sanitized name or rejects, but never executes
        try:
            result = await manage_folder_service(request, vault_path="/tmp/test-vault")
            # If succeeds, verify name is literal
            assert name not in result.message  # Original not in message
        except ValueError:
            # Acceptable to reject
            pass
```

**4. Symlink Security** (1 test)
```python
async def test_symlink_escape_prevented():
    """Test that symlinks cannot escape vault."""
    vault = tmp_path / "vault"
    vault.mkdir()

    # Create symlink pointing outside vault
    (vault / "external").symlink_to("/tmp")

    request = ManageFolderRequest(path="external", operation=FolderOperation.ARCHIVE)

    # Should detect and handle symlink appropriately
    # Either resolve safely or reject
    # MUST NOT allow escape from vault
    with pytest.raises(ValueError, match="symlink|invalid"):
        await manage_folder_service(request, vault_path=str(vault))
```

**5. No Sensitive Data in Logs** (1 test)
```python
async def test_no_sensitive_data_in_logs(caplog):
    """Test that logs don't contain sensitive data."""
    sensitive_data = {
        "api_key": "sk-abc123",
        "password": "secret123",
        "token": "bearer xyz",
    }

    # Run operation with potential sensitive data
    request = ManageFolderRequest(path="test-folder", operation=FolderOperation.CREATE)
    await manage_folder_service(request, vault_path="/tmp/vault")

    # Check logs don't contain sensitive patterns
    log_output = caplog.text.lower()
    assert "api_key" not in log_output or "sk-" not in log_output
    assert "password" not in log_output or "secret" not in log_output
    assert "token" not in log_output or "bearer" not in log_output
```

**Validates**:
- [ ] Directory traversal blocked
- [ ] Absolute paths rejected
- [ ] Sensitive folders protected
- [ ] Code injection prevented
- [ ] Symlink escapes prevented
- [ ] No sensitive data logged

**Success Criteria**: All 6 security tests pass

---

#### Validation 1.5.2: Static Security Analysis
**Tool**: Bandit (if available)
**Command**:
```bash
uv run bandit -r src/tools/obsidian_folder_manager/ -ll
```

**Validates**:
- [ ] No hardcoded passwords
- [ ] No insecure temp file usage
- [ ] No shell injection vulnerabilities
- [ ] No pickle usage (arbitrary code execution)
- [ ] No weak cryptography (if any crypto used)

**Success Criteria**: 0 medium/high severity issues

---

### 1.6 Pre-Deployment Validation Summary

**Complete Pre-Deployment Checklist**:

#### Phase 1: Dependencies ✓
- [ ] 1.1.1: Dependency installation check (uv sync)
- [ ] 1.1.2: Dependency version verification
- [ ] 1.1.3: Security audit (safety/pip-audit)
- [ ] 1.1.4: Import verification

#### Phase 2: Code Quality ✓
- [ ] 1.2.1: Ruff linting (0 errors)
- [ ] 1.2.2: Ruff formatting check
- [ ] 1.2.3: MyPy type checking strict mode (0 errors)
- [ ] 1.2.4: Type coverage >99%

#### Phase 3: Unit Tests ✓
- [ ] 1.3.1: All 30+ unit tests pass
- [ ] 1.3.2: Test coverage >90%
- [ ] 1.3.3: Test quality checks pass

#### Phase 4: Integration Tests ✓
- [ ] 1.4.1: All 10 integration tests pass
- [ ] 1.4.2: Both E2E tests pass

#### Phase 5: Security ✓
- [ ] 1.5.1: All 6 security tests pass
- [ ] 1.5.2: Static security analysis clean

**Total Automated Checks**: 20+ validation steps
**Total Tests**: 48+ tests (30 unit + 10 integration + 2 E2E + 6 security)

**CI/CD Integration**:
```yaml
# .github/workflows/pre-deployment.yml
name: Pre-Deployment Validation

on: [push, pull_request]

jobs:
  pre-deployment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: 1.1 Dependency Validation
        run: |
          uv sync --frozen
          uv pip list

      - name: 1.2 Linting and Type Checking
        run: |
          uv run ruff check src/tools/obsidian_folder_manager/
          uv run ruff format --check src/tools/obsidian_folder_manager/
          uv run mypy src/tools/obsidian_folder_manager/ --strict

      - name: 1.3 Unit Tests
        run: |
          uv run pytest tests/tools/obsidian_folder_manager/ -v -m unit \
            --cov=src/tools/obsidian_folder_manager/ \
            --cov-report=term-missing \
            --cov-fail-under=90

      - name: 1.4 Integration Tests
        run: |
          uv run pytest tests/integration/ -v -m integration
          uv run pytest tests/e2e/ -v

      - name: 1.5 Security Tests
        run: |
          uv run pytest tests/security/ -v
```

---

## 2. Unit Testing Strategy

### 1.1 Path Validation Tests (5 tests)

**File**: `tests/tools/obsidian_folder_manager/test_service.py`
**Class**: `TestPathValidation` (new class)

#### Test 1: `test_rejects_md_extension`
**Purpose**: Verify .md files rejected with helpful error

```python
async def test_rejects_md_extension(self, tmp_path):
    """Test that .md file paths are rejected with error directing to note_manage."""
    vault = tmp_path / "vault"
    vault.mkdir()

    request = ManageFolderRequest(
        path="projects/note.md",
        operation=FolderOperation.CREATE,
    )

    with pytest.raises(ValueError, match="operates on FOLDERS only"):
        await manage_folder_service(
            request=request,
            vault_path=str(vault),
            max_folder_depth=10,
            max_wikilink_scan_notes=1000,
        )
```

**Validates**:
- [ ] Raises ValueError with correct message
- [ ] Error message mentions "FOLDERS only"
- [ ] Error message mentions obsidian_note_manage
- [ ] Error message includes example usage

---

#### Test 2: `test_rejects_markdown_extension`
**Purpose**: Verify .markdown extension also rejected

**Validates**:
- [ ] .markdown extension rejected same as .md
- [ ] Consistent error message format

---

#### Test 3: `test_rejects_any_file_extension`
**Purpose**: Verify any file extension rejected (.txt, .json, .pdf, etc.)

**Validates**:
- [ ] Extensions beyond .md are rejected (.json, .txt, .pdf, .csv)
- [ ] Error message says "appears to be a file"
- [ ] Error message includes detected extension in message

---

#### Test 4: `test_accepts_folder_without_extension`
**Purpose**: Verify valid folder paths accepted

```python
async def test_accepts_folder_without_extension(self, tmp_path):
    """Test that folder paths without extensions are accepted."""
    vault = tmp_path / "vault"
    vault.mkdir()

    # Test various valid folder paths
    valid_paths = [
        "projects/2025",
        "daily",
        "archive/old-projects",
        "folder-with-dashes",
        "folder_with_underscores",
    ]

    for path in valid_paths:
        request = ManageFolderRequest(
            path=path,
            operation=FolderOperation.CREATE,
        )

        result = await manage_folder_service(
            request=request,
            vault_path=str(vault),
            max_folder_depth=10,
            max_wikilink_scan_notes=1000,
        )

        assert result.success is True
```

**Validates**:
- [ ] Simple folder names accepted
- [ ] Nested paths accepted
- [ ] Dashes in names accepted
- [ ] Underscores in names accepted
- [ ] No false positives (valid paths not rejected)

---

#### Test 5: `test_accepts_folder_with_dot_in_name`
**Purpose**: Verify folders with dots but no extension accepted

**Test Cases**:
- "projects/version-2.0" (dot followed by number)
- "projects/data.2025" (dot not at extension position)
- "archive/old.backup" (could look like extension but is folder name)

**Validates**:
- [ ] Dots in middle of name accepted
- [ ] Only rejects if dot is clearly a file extension
- [ ] Edge cases handled correctly

---

### 1.2 Archive Operation Tests (10 tests)

**File**: `tests/tools/obsidian_folder_manager/test_service.py`
**Class**: `TestArchiveFolderOperation` (new class)

#### Test 1: `test_archive_simple_folder`
**Purpose**: Basic archive with default settings

**Validates**:
- [ ] Success status returned
- [ ] Archive path matches format: `archive/YYYY-MM-DD/folder-name`
- [ ] Date is today's date
- [ ] Source folder no longer exists
- [ ] Destination folder exists with correct contents
- [ ] Folder contents intact after move

---

#### Test 2: `test_archive_with_wikilink_updates`
**Purpose**: Verify wikilinks updated in all notes

**Setup**:
- Create folder: `projects/alpha` with note `overview.md`
- Create note: `index.md` with link `[[projects/alpha/overview]]`
- Create note: `docs/guide.md` with link `![[projects/alpha/overview]]` (embed)

**Validates**:
- [ ] Success status
- [ ] `links_updated` metadata = 2 (two notes updated)
- [ ] `index.md` wikilink changed to `[[archive/YYYY-MM-DD/alpha/overview]]`
- [ ] `docs/guide.md` embed changed to `![[archive/YYYY-MM-DD/alpha/overview]]`
- [ ] Other content in notes unchanged
- [ ] No links to old path remain

---

#### Test 3: `test_archive_nested_folder`
**Purpose**: Archive folder with nested subfolders and files

**Setup**:
```
projects/
  alpha/
    docs/
      guide.md
      api.md
    src/
      main.py
    README.md
```

**Validates**:
- [ ] Entire structure moved to archive
- [ ] Nested folders preserved
- [ ] All files present in archive location
- [ ] Directory structure identical after move

---

#### Test 4: `test_archive_custom_base`
**Purpose**: Archive with custom base folder

**Test**:
```python
request = ManageFolderRequest(
    path="drafts/old-idea",
    operation=FolderOperation.ARCHIVE,
    archive_base="old-drafts",
)
```

**Validates**:
- [ ] Archive path: `old-drafts/YYYY-MM-DD/old-idea`
- [ ] Custom base folder created
- [ ] Metadata includes archive_base="old-drafts"
- [ ] Nested custom base works: `archive/projects/YYYY-MM-DD/`

---

#### Test 5: `test_archive_custom_date_format`
**Purpose**: Archive with different date formats

**Test Cases**:
- `%Y-%m-%d` → `2025-01-22` (default, ISO format)
- `%Y/%m` → `2025/01` (year/month only)
- `%Y-%m` → `2025-01` (year-month hyphen)
- `%Y/Q1` → `2025/Q1` (quarterly - manual Q mapping)

**Validates**:
- [ ] Date format applied correctly
- [ ] Path separators in date format handled (creates nested folders)
- [ ] Metadata includes correct date string
- [ ] Archive path uses custom format

---

#### Test 6: `test_archive_dry_run`
**Purpose**: Dry-run shows destination without moving

**Validates**:
- [ ] Success status with dry_run=True in metadata
- [ ] Result includes where folder would be moved
- [ ] Source folder still exists (not moved)
- [ ] Destination folder not created
- [ ] Message indicates dry-run mode

---

#### Test 7: `test_archive_destination_exists_error`
**Purpose**: Error when archive destination already exists

**Setup**:
- Create folder: `projects/alpha`
- Pre-create archive: `archive/2025-01-22/alpha/`
- Try to archive `projects/alpha`

**Validates**:
- [ ] Raises ValueError
- [ ] Error message says "destination already exists"
- [ ] Error provides 3 resolution options (different base, delete existing, use move operation)
- [ ] Source folder not deleted/moved

---

#### Test 8: `test_archive_folder_not_found`
**Purpose**: Error when source folder doesn't exist

**Validates**:
- [ ] Raises FileNotFoundError
- [ ] Error message says "Folder not found"
- [ ] Error includes the path that wasn't found

---

#### Test 9: `test_archive_with_special_characters`
**Purpose**: Archive folder with special characters in name

**Test Paths**:
- `projects/website-redesign` (hyphen)
- `projects/data_analysis` (underscore)
- `projects/2025 planning` (space)
- `projects/(archived)` (parentheses)

**Validates**:
- [ ] All special characters preserved in archive
- [ ] Paths properly escaped/quoted if needed
- [ ] No path corruption

---

#### Test 10: `test_archive_updates_multiple_wikilink_formats`
**Purpose**: Verify all wikilink formats updated

**Setup - Note with various wikilink formats**:
```markdown
# Test Note

Regular link: [[projects/alpha/overview]]
Display text: [[projects/alpha/overview|Alpha Overview]]
With heading: [[projects/alpha/overview#introduction]]
Embed: ![[projects/alpha/diagram.png]]
Multiple on line: [[projects/alpha/a]] and [[projects/alpha/b]]
```

**Validates**:
- [ ] Regular wikilinks updated
- [ ] Display text preserved, path updated
- [ ] Heading anchors preserved
- [ ] Embed syntax updated
- [ ] Multiple links per line all updated

---

### 1.3 Schema Validation Tests (5 tests)

**File**: `tests/tools/obsidian_folder_manager/test_schemas.py` (new file)

#### Test 1: `test_folder_operation_enum_has_archive`
**Purpose**: Verify ARCHIVE added to enum

**Validates**:
- [ ] `FolderOperation.ARCHIVE` exists
- [ ] Value is "archive"
- [ ] All operations: CREATE, RENAME, MOVE, DELETE, LIST, ARCHIVE

---

#### Test 2: `test_manage_folder_request_archive_params`
**Purpose**: Verify archive parameters in request schema

**Validates**:
- [ ] `archive_base` field exists with default="archive"
- [ ] `date_format` field exists with default="%Y-%m-%d"
- [ ] Parameters have correct types (str)
- [ ] Field descriptions present

---

#### Test 3: `test_request_validation_with_archive`
**Purpose**: Request validates with archive operation

```python
def test_request_validation_with_archive():
    """Test ManageFolderRequest validates with archive operation."""
    request = ManageFolderRequest(
        path="projects/old",
        operation=FolderOperation.ARCHIVE,
        archive_base="old-projects",
        date_format="%Y/%m",
    )

    assert request.path == "projects/old"
    assert request.operation == FolderOperation.ARCHIVE
    assert request.archive_base == "old-projects"
    assert request.date_format == "%Y/%m"
```

**Validates**:
- [ ] Pydantic validation passes
- [ ] All fields correctly assigned
- [ ] Defaults applied when not specified

---

#### Test 4: `test_invalid_operation_rejected`
**Purpose**: Invalid operation strings rejected by schema

**Test**:
```python
with pytest.raises(ValidationError):
    ManageFolderRequest(
        path="test",
        operation="invalid_operation"
    )
```

**Validates**:
- [ ] Pydantic ValidationError raised
- [ ] Only valid enum values accepted

---

#### Test 5: `test_archive_params_ignored_for_other_operations`
**Purpose**: Archive params don't interfere with other operations

**Validates**:
- [ ] CREATE operation works with archive_base/date_format present (ignored)
- [ ] RENAME operation not affected
- [ ] No unexpected side effects

---

### 1.4 Error Handling Tests (8 tests)

**File**: `tests/tools/obsidian_folder_manager/test_error_handling.py` (new file)

#### Test 1: `test_error_message_structure`
**Purpose**: Verify error messages follow structured format

**Validates**:
- [ ] Error has "what" section (what went wrong)
- [ ] Error has "why" section (why it failed)
- [ ] Error has "how" section (what to do instead)
- [ ] Error includes example of correct usage
- [ ] Error is <100 tokens

---

#### Test 2: `test_file_path_error_suggests_note_manage`
**Purpose**: File path error explicitly mentions note_manage

**Validates**:
- [ ] Error message includes "obsidian_note_manage"
- [ ] Error shows example call to note_manage
- [ ] Tool selection guide included

---

#### Test 3: `test_archive_conflict_error_provides_options`
**Purpose**: Archive destination exists error helpful

**Validates**:
- [ ] Error lists 3 resolution options
- [ ] Options: different archive_base, delete existing, use move
- [ ] Each option actionable

---

#### Test 4: `test_wikilink_scan_failure_non_fatal`
**Purpose**: Wikilink update failures don't block operation

**Setup**: Mock wikilink scanner to raise exception

**Validates**:
- [ ] Archive operation completes
- [ ] Error logged but not raised
- [ ] Result indicates wikilink update failed
- [ ] Metadata shows links_updated=0 with error

---

#### Test 5: `test_permission_error_handled`
**Purpose**: File permission errors handled gracefully

**Setup**: Create read-only folder, try to move

**Validates**:
- [ ] PermissionError caught
- [ ] Helpful error message
- [ ] Suggests checking permissions
- [ ] Original folder unchanged

---

#### Test 6: `test_disk_full_error_handled`
**Purpose**: Disk full during archive handled

**Setup**: Mock move operation to raise OSError (disk full)

**Validates**:
- [ ] OSError caught and re-raised with context
- [ ] Error message mentions disk space
- [ ] Original folder preserved (atomic operation)

---

#### Test 7: `test_invalid_date_format_error`
**Purpose**: Invalid date format strings rejected

**Test**: `date_format="invalid%Z%Q"`

**Validates**:
- [ ] Error raised during date formatting
- [ ] Error message explains date format invalid
- [ ] Suggests valid format examples

---

#### Test 8: `test_circular_archive_prevented`
**Purpose**: Cannot archive folder into itself

**Test**: Archive `archive` folder with `archive_base="archive"`

**Validates**:
- [ ] Error raised preventing circular operation
- [ ] Clear error message
- [ ] Folder unchanged

---

### 1.5 Wikilink Update Tests (6 tests)

**File**: `tests/tools/obsidian_folder_manager/test_wikilink_updates.py` (new file)

#### Test 1: `test_updates_regular_wikilinks`
**Purpose**: Basic wikilink format updated

**Validates**: `[[projects/alpha/note]]` → `[[archive/2025-01-22/alpha/note]]`

---

#### Test 2: `test_updates_wikilinks_with_display_text`
**Purpose**: Display text format updated

**Validates**: `[[projects/alpha/note|Display]]` → `[[archive/2025-01-22/alpha/note|Display]]`
Display text unchanged.

---

#### Test 3: `test_updates_wikilinks_with_headings`
**Purpose**: Heading anchors preserved

**Validates**: `[[projects/alpha/note#section]]` → `[[archive/2025-01-22/alpha/note#section]]`

---

#### Test 4: `test_updates_embed_syntax`
**Purpose**: Embed wikilinks updated

**Validates**: `![[projects/alpha/image.png]]` → `![[archive/2025-01-22/alpha/image.png]]`

---

#### Test 5: `test_does_not_update_unrelated_wikilinks`
**Purpose**: Other wikilinks unchanged

**Setup**:
- Archive: `projects/alpha`
- Note has: `[[projects/beta/note]]` (different folder)

**Validates**:
- [ ] `projects/beta` links unchanged
- [ ] Only `projects/alpha` links updated

---

#### Test 6: `test_wikilink_update_count_accurate`
**Purpose**: Metadata reports correct update count

**Setup**:
- 3 notes with wikilinks to archived folder
- 2 notes without wikilinks

**Validates**:
- [ ] `links_updated` = 3 (only notes with links)
- [ ] Count matches actual updates

---

## 2. Integration Testing Strategy

### 2.1 Tool Integration Tests (4 tests)

**File**: `tests/tools/obsidian_folder_manager/test_tool_integration.py` (new file)

#### Test 1: `test_tool_to_service_integration`
**Purpose**: Tool registration correctly calls service layer

**Validates**:
- [ ] Tool function accepts all parameters
- [ ] Parameters correctly passed to ManageFolderRequest
- [ ] Service result correctly formatted for agent
- [ ] Token estimate included in response

---

#### Test 2: `test_response_format_minimal`
**Purpose**: Minimal response format returns ~50 tokens

**Validates**:
- [ ] Response <70 tokens
- [ ] Includes operation status
- [ ] Omits verbose details
- [ ] Includes token estimate

---

#### Test 3: `test_response_format_concise`
**Purpose**: Concise response format returns ~150 tokens

**Validates**:
- [ ] Response 100-200 tokens
- [ ] Includes status + key metadata
- [ ] Includes new path
- [ ] Includes links updated count

---

#### Test 4: `test_response_format_detailed`
**Purpose**: Detailed response format returns full details

**Validates**:
- [ ] Response >150 tokens
- [ ] Includes all metadata
- [ ] Includes archive date
- [ ] Includes folder statistics if available

---

### 2.2 System Prompt Integration Tests (2 tests)

**File**: `tests/integration/test_system_prompt_integration.py` (new file)

#### Test 1: `test_decision_tree_in_system_prompt`
**Purpose**: Verify decision tree added to config

**Validates**:
- [ ] agent_system_prompt contains "Tool Selection Decision Tree"
- [ ] Decision tree has 4 decision points
- [ ] Tool categories section present
- [ ] STRUCTURE vs CONTENT tools categorized

---

#### Test 2: `test_system_prompt_formatting`
**Purpose**: System prompt is valid and parseable

**Validates**:
- [ ] No syntax errors in prompt
- [ ] Markdown formatting valid
- [ ] Examples properly formatted
- [ ] No duplicate sections

---

### 2.3 Cross-Component Integration Tests (4 tests)

**File**: `tests/integration/test_cross_component.py` (new file)

#### Test 1: `test_vault_security_integration`
**Purpose**: Path validation integrates with vault_security

**Validates**:
- [ ] Directory traversal blocked
- [ ] .obsidian folder blocked
- [ ] .git folder blocked
- [ ] validate_folder_path called before vault_security

---

#### Test 2: `test_obsidian_parsers_integration`
**Purpose**: Wikilink parsing uses obsidian_parsers

**Validates**:
- [ ] extract_wikilinks_from_content() used
- [ ] All wikilink formats detected
- [ ] Parser errors handled gracefully

---

#### Test 3: `test_logging_integration`
**Purpose**: Structured logging works throughout

**Validates**:
- [ ] All operations logged with structured fields
- [ ] Correlation IDs present (if applicable)
- [ ] Error logs include stack traces
- [ ] Log levels appropriate

---

#### Test 4: `test_config_integration`
**Purpose**: Config settings respected

**Validates**:
- [ ] max_wikilink_scan_notes limit enforced
- [ ] max_folder_depth limit enforced
- [ ] Vault path from config used

---

## 3. End-to-End (E2E) Testing Strategy

### 3.1 Complete Workflow Tests (2 tests)

**File**: `tests/e2e/test_folder_workflows.py` (new file)

#### Test 1: `test_complete_archive_workflow`
**Purpose**: End-to-end archive from agent request to result

**Workflow**:
1. Agent receives user request: "Archive the old-website folder"
2. Tool selection: Agent selects `obsidian_folder_manage`
3. Parameter extraction: `operation="archive"`, `path="projects/old-website"`
4. Tool execution: Archive operation runs
5. Wikilink updates: All references updated
6. Response formatting: Result returned to agent
7. Agent reply: Formatted response to user

**Validates**:
- [ ] Full workflow completes without errors
- [ ] Each step logged appropriately
- [ ] Final result matches expectations
- [ ] User-facing message clear and helpful

---

#### Test 2: `test_error_recovery_workflow`
**Purpose**: Agent recovers from tool selection error

**Workflow**:
1. Agent receives: "Archive note.md"
2. Agent (incorrectly) calls: `obsidian_folder_manage(path="note.md", operation="archive")`
3. Error raised: "operates on FOLDERS only"
4. Error message suggests: Use `obsidian_note_manage` instead
5. Agent corrects: Calls `obsidian_note_manage` (simulated)
6. Operation succeeds

**Validates**:
- [ ] Error message clear enough for agent to self-correct
- [ ] Error includes example of correct tool
- [ ] Agent can extract correct tool name from error
- [ ] Recovery path successful

---

## 4. Cross-Platform Testing Strategy

### 4.1 Platform-Specific Tests (9 tests)

**File**: `tests/platform/test_cross_platform.py` (new file)
**Runs On**: Linux, macOS, Windows via CI/CD

#### Test 1: `test_path_separators_normalized`
**Purpose**: All platforms return forward slashes

**Test On**: All 3 platforms

**Validates**:
- [ ] Result paths use `/` not `\`
- [ ] Wikilinks use `/` not `\`
- [ ] Metadata paths use `/` not `\`

---

#### Test 2: `test_windows_reserved_names_rejected`
**Purpose**: Windows reserved names rejected on all platforms

**Test**: CON, PRN, AUX, NUL, COM1, COM2, LPT1, LPT2

**Validates**:
- [ ] Linux rejects reserved names (preventive)
- [ ] macOS rejects reserved names (preventive)
- [ ] Windows rejects reserved names (actual restriction)

---

#### Test 3: `test_case_only_rename_handling`
**Purpose**: Case-only renames work on case-insensitive filesystems

**Test**: Rename `Projects` → `projects`

**Validates**:
- [ ] Linux: Direct rename works
- [ ] macOS: Handles case-insensitive filesystem
- [ ] Windows: Handles case-insensitive filesystem
- [ ] No data loss on any platform

---

#### Test 4: `test_unicode_folder_names`
**Purpose**: Unicode characters supported

**Test Folders**:
- `项目/2025` (Chinese)
- `プロジェクト` (Japanese)
- `مشاريع` (Arabic)
- `📁 Projects` (Emoji)

**Validates**:
- [ ] All platforms create folders
- [ ] All platforms archive folders
- [ ] Paths correctly encoded
- [ ] No character corruption

---

#### Test 5: `test_long_path_handling`
**Purpose**: Long paths handled correctly

**Setup**:
- Create deeply nested folder (10+ levels)
- Archive to create even longer path

**Validates**:
- [ ] Linux: Supports long paths (PATH_MAX)
- [ ] macOS: Supports long paths
- [ ] Windows: Handles paths >260 characters (or errors gracefully)

---

#### Test 6: `test_symlink_handling`
**Purpose**: Symlinks handled appropriately

**Test**: Create symlink to folder, try to archive

**Validates**:
- [ ] Symlinks detected
- [ ] Behavior documented (follow or error)
- [ ] No infinite loops
- [ ] Consistent across platforms

---

#### Test 7: `test_file_permission_differences`
**Purpose**: Permission models respected

**Validates**:
- [ ] Linux: chmod permissions respected
- [ ] macOS: chmod permissions respected
- [ ] Windows: ACL permissions respected
- [ ] Permission errors clear on all platforms

---

#### Test 8: `test_pathlib_consistency`
**Purpose**: pathlib.Path usage consistent

**Validates**:
- [ ] All path operations use pathlib.Path
- [ ] No os.path usage in service layer
- [ ] Path joins use `/` operator
- [ ] Cross-platform compatibility

---

#### Test 9: `test_timestamps_preserved`
**Purpose**: File timestamps preserved during archive

**Validates**:
- [ ] Modified time preserved (all platforms)
- [ ] Created time preserved (where supported)
- [ ] Timestamp format consistent

---

### 4.2 CI/CD Pipeline Tests

**File**: `.github/workflows/test.yml`

**Matrix**:
```yaml
os: [ubuntu-latest, macos-latest, windows-latest]
python: ['3.11', '3.12']
```

**Total Combinations**: 6 (3 OS × 2 Python)

**Validates**:
- [ ] All unit tests pass on all platforms
- [ ] All integration tests pass on all platforms
- [ ] Linters pass on all platforms
- [ ] No platform-specific failures
- [ ] Test duration <5 minutes per platform

---

## 5. Performance Testing Strategy

### 5.1 Performance Benchmarks (6 benchmarks)

**File**: `tests/performance/folder_benchmark.py` (new file)

#### Benchmark 1: Archive Small Folder
**Setup**: Folder with 5 notes (total 50KB)

**Target**: <100ms
**Validates**:
- [ ] Median time <100ms
- [ ] p95 time <150ms
- [ ] p99 time <200ms

---

#### Benchmark 2: Archive Medium Folder
**Setup**: Folder with 25 notes (total 5MB)

**Target**: <500ms
**Validates**:
- [ ] Median time <500ms
- [ ] p95 time <750ms
- [ ] p99 time <1000ms

---

#### Benchmark 3: Archive Large Folder
**Setup**: Folder with 100 notes (total 20MB)

**Target**: <2s
**Validates**:
- [ ] Median time <2s
- [ ] p95 time <3s
- [ ] No timeout errors

---

#### Benchmark 4: Wikilink Updates - Small Vault
**Setup**: 100-note vault, 10 notes with wikilinks to archived folder

**Target**: <200ms
**Validates**:
- [ ] Scan time <100ms
- [ ] Update time <100ms
- [ ] Total <200ms

---

#### Benchmark 5: Wikilink Updates - Large Vault
**Setup**: 1000-note vault, 50 notes with wikilinks

**Target**: <2s
**Validates**:
- [ ] Scan limited by max_wikilink_scan_notes
- [ ] Update time <2s
- [ ] No memory issues

---

#### Benchmark 6: Path Validation
**Setup**: Run path validation 1000 times

**Target**: <10ms per call
**Validates**:
- [ ] Median <5ms
- [ ] p95 <10ms
- [ ] No caching needed

---

### 5.2 Scalability Tests (3 tests)

**File**: `tests/performance/scalability_test.py` (new file)

#### Test 1: `test_deep_nesting_performance`
**Purpose**: Performance with deeply nested folders

**Setup**: Create 10-level nested structure

**Validates**:
- [ ] Archive completes without timeout
- [ ] Performance degrades linearly (not exponentially)
- [ ] Memory usage reasonable

---

#### Test 2: `test_many_files_performance`
**Purpose**: Folder with many files

**Setup**: Folder with 1000 files

**Validates**:
- [ ] Archive completes
- [ ] Performance acceptable
- [ ] No file descriptor limits hit

---

#### Test 3: `test_concurrent_operations`
**Purpose**: Multiple archive operations in parallel

**Setup**: 5 concurrent archive operations

**Validates**:
- [ ] All operations complete
- [ ] No race conditions
- [ ] No file lock conflicts
- [ ] Total time ~1.2x single operation (good parallelism)

---

## 6. Security Testing Strategy

### 6.1 Security Tests (6 tests)

**File**: `tests/security/test_folder_security.py` (new file)

#### Test 1: `test_directory_traversal_blocked`
**Purpose**: Path traversal attacks prevented

**Test Paths**:
- `../../../etc/passwd`
- `..\\..\\..\\windows\\system32`
- `projects/../../sensitive`

**Validates**:
- [ ] All traversal attempts blocked
- [ ] Error message clear
- [ ] No partial execution

---

#### Test 2: `test_absolute_path_rejected`
**Purpose**: Absolute paths rejected

**Test Paths**:
- `/etc/passwd`
- `C:\\Windows\\System32`
- `/home/user/.ssh`

**Validates**:
- [ ] Absolute paths rejected
- [ ] Error says "must be relative"

---

#### Test 3: `test_sensitive_folders_protected`
**Purpose**: Cannot archive system folders

**Test Paths**:
- `.obsidian`
- `.git`
- `.trash`

**Validates**:
- [ ] Blocked patterns enforced
- [ ] Error says folder is protected

---

#### Test 4: `test_symlink_escape_prevented`
**Purpose**: Symlinks cannot escape vault

**Setup**:
- Create symlink pointing outside vault
- Try to archive

**Validates**:
- [ ] Symlink escape detected
- [ ] Operation blocked or symlink resolved safely

---

#### Test 5: `test_no_code_injection`
**Purpose**: Folder names cannot inject code

**Test Names**:
- `folder; rm -rf /`
- `folder$(malicious command)`
- `folder' OR '1'='1`

**Validates**:
- [ ] All names treated as literals
- [ ] No shell execution
- [ ] No SQL injection (not applicable but test anyway)

---

#### Test 6: `test_no_sensitive_data_in_logs`
**Purpose**: Logs don't contain sensitive data

**Validates**:
- [ ] No API keys in logs
- [ ] No passwords in logs
- [ ] Paths logged (acceptable for local tool)
- [ ] Error details appropriately masked

---

## 7. Tool Selection Evaluation Testing

### 7.1 Automated Evaluation Suite (50 tests)

**File**: `tests/evaluation/tool_selection_accuracy.py` (new file)

**Purpose**: Measure agent's ability to select correct tool

#### Test Categories (10 tests each)

**Category 1: Obvious Folder Operations** (10 tests)
- "Create a new folder called projects"
- "Rename the old-projects folder to archive"
- "Move the drafts folder into archive"
- "Delete the empty temp folder"
- "List all folders in projects"
- "Archive the 2023 folder"
- "Create nested folders for 2025/january/notes"
- "Move archive folder to old-archive"
- "Rename Projects to projects (case change)"
- "List subfolders recursively in archive"

**Expected**: 100% use `obsidian_folder_manage`

---

**Category 2: Obvious Note Operations** (10 tests)
- "Create a new note called todo.md"
- "Read the contents of README.md"
- "Update the frontmatter in project-plan.md"
- "Delete the old-note.md file"
- "Append to daily-note.md"
- "Create meeting-notes.md in meetings folder"
- "Read overview.md and summarize it"
- "Update tags in research.md"
- "Patch the date in journal.md"
- "Delete all notes tagged #draft"

**Expected**: 100% use `obsidian_note_manage`

---

**Category 3: Ambiguous Cases** (10 tests)
- "Create something called test in projects"
  - **Expected**: Ask for clarification OR default to folder (no extension)
- "Delete old-stuff"
  - **Expected**: Ask if folder or file OR check existence first
- "Archive the meeting notes"
  - **Expected**: Ask if folder or specific note file
- "Move alpha to archive"
  - **Expected**: Determine if alpha is folder or file
- "Organize the daily folder"
  - **Expected**: Likely vault_organizer, not folder_manage
- "List everything in projects"
  - **Expected**: Could be folder LIST or vault_query
- "Rename old to new"
  - **Expected**: Ask for clarification (folder or file?)
- "Create backup"
  - **Expected**: Ask if folder or note
- "Delete empty items"
  - **Expected**: Needs clarification on scope
- "Update the structure"
  - **Expected**: Vague, should ask for clarification

**Expected**: >80% correct handling (clarification or correct tool)

---

**Category 4: Edge Cases** (10 tests)
- "Create a folder called note.md" (folder with .md in name)
  - **Expected**: Likely error or confusion (intentional trap)
- "Archive file.txt" (non-markdown file)
  - **Expected**: Reject or note_manage (not folder_manage)
- "Move folder/with/slashes" (path as name)
  - **Expected**: Parse correctly or ask for clarification
- "Create .hidden-folder" (hidden folder)
  - **Expected**: Allow or reject based on policy
- "Archive 'projects/alpha'" (with quotes)
  - **Expected**: Parse quotes correctly, archive folder
- "Delete CON" (Windows reserved name)
  - **Expected**: Error about reserved name
- "Create folder with emoji 📁"
  - **Expected**: Allow unicode
- "Archive projects/alpha/../../sensitive" (traversal attempt)
  - **Expected**: Error about invalid path
- "Move to destination/" (trailing slash)
  - **Expected**: Handle gracefully
- "Create a folder and a note both called test"
  - **Expected**: Two operations or ask for clarification

**Expected**: >70% correct handling (many are intentionally tricky)

---

**Category 5: Mixed Operations** (10 tests)
- "Create a projects folder and a README.md inside it"
  - **Expected**: Two tools (folder_manage + note_manage)
- "Archive old-projects and update the index.md to reflect this"
  - **Expected**: folder_manage (archive) + note_manage (update)
- "Reorganize the vault by moving folders and updating notes"
  - **Expected**: Multiple tool calls or vault_organizer
- "Create a new project structure with folders and template notes"
  - **Expected**: Multiple folder_manage + note_manage calls
- "Archive 2023 folder and create a summary note of what was archived"
  - **Expected**: folder_manage + note_manage
- "List all folders and create an index note with the list"
  - **Expected**: folder_manage (list) + note_manage (create)
- "Move meeting-notes folder and update all links to it"
  - **Expected**: folder_manage (auto-updates links)
- "Delete empty folders and orphaned notes"
  - **Expected**: vault_organizer or multiple tool calls
- "Create archive structure and move old folders into it"
  - **Expected**: Multiple folder_manage calls
- "Rename folder and update the note that references it"
  - **Expected**: folder_manage (auto-updates links) or + note_manage

**Expected**: >90% correct sequencing and tool selection

---

### 7.2 Evaluation Metrics

**File**: `tests/evaluation/tool_selection_accuracy.py`

**Metrics Tracked**:
- **Overall Accuracy**: Correct tool(s) selected / Total tests
- **Category Accuracy**: Per-category breakdown
- **Confusion Matrix**: folder_manage vs note_manage vs other
- **Clarification Rate**: Tests requiring user clarification
- **Error Rate**: Tests resulting in errors
- **Multi-Tool Accuracy**: Correct sequencing for mixed operations

**Target**: >95% overall accuracy (47+/50 tests)

**Report Output**:
```json
{
  "timestamp": "2025-01-22T10:30:00Z",
  "total_tests": 50,
  "passed": 48,
  "failed": 2,
  "accuracy": 0.96,
  "categories": {
    "obvious_folder": {"accuracy": 1.0, "passed": 10, "failed": 0},
    "obvious_note": {"accuracy": 1.0, "passed": 10, "failed": 0},
    "ambiguous": {"accuracy": 0.9, "passed": 9, "failed": 1},
    "edge_cases": {"accuracy": 0.8, "passed": 8, "failed": 2},
    "mixed": {"accuracy": 1.0, "passed": 10, "failed": 0}
  },
  "failed_tests": [
    {"test": "Create a folder called note.md", "expected": "clarify", "actual": "folder_manage"},
    {"test": "Archive file.txt", "expected": "note_manage", "actual": "folder_manage"}
  ]
}
```

---

## 8. Regression Testing Strategy

### 8.1 Existing Functionality Tests (20 tests)

**Purpose**: Ensure no existing features broken

**File**: `tests/tools/obsidian_folder_manager/test_service.py`

**Existing Test Classes** (must all still pass):
- `TestCreateFolderOperation` (5 tests)
- `TestRenameFolderOperation` (4 tests)
- `TestMoveFolderOperation` (4 tests)
- `TestDeleteFolderOperation` (4 tests)
- `TestListFolderOperation` (3 tests)

**Criteria**: All 20 existing tests pass without modification

---

### 8.2 API Compatibility Tests (3 tests)

**File**: `tests/regression/test_api_compatibility.py` (new file)

#### Test 1: `test_existing_operations_unchanged`
**Purpose**: CREATE, RENAME, MOVE, DELETE, LIST work identically

**Validates**:
- [ ] All operations accept same parameters
- [ ] Response format unchanged
- [ ] No breaking changes

---

#### Test 2: `test_new_params_have_defaults`
**Purpose**: New parameters don't break existing calls

**Test**: Call archive without archive_base/date_format

**Validates**:
- [ ] Defaults applied
- [ ] Operation succeeds
- [ ] Backward compatible

---

#### Test 3: `test_response_format_backward_compatible`
**Purpose**: Response structure unchanged for existing operations

**Validates**:
- [ ] FolderOperationResult schema unchanged
- [ ] Only additions to metadata (no removals)
- [ ] Existing fields have same types

---

## 9. Acceptance Testing Strategy

### 9.1 User Story Validation

**Purpose**: Verify all user stories from plan satisfied

#### Story 1: Clear Tool Separation
**Tests**: tool_selection_accuracy.py (50 tests)

**Acceptance Criteria**:
- [x] Tool docstring includes "Use this when" section with 5+ scenarios
- [x] Tool docstring includes "Do NOT use for" section with 5+ scenarios
- [x] System prompt includes decision tree
- [x] Path validation rejects .md files with helpful error
- [x] Runtime validation detects wrong-tool usage
- [x] Evaluation tests show >95% accuracy

**Validation**: Run evaluation suite, verify >95% accuracy

---

#### Story 2: Archive Old Projects
**Tests**: TestArchiveFolderOperation (10 tests)

**Acceptance Criteria**:
- [x] Archive creates archive/YYYY-MM-DD/folder-name
- [x] Wikilinks automatically updated
- [x] Archive <500ms for typical folder
- [x] Custom archive_base supported
- [x] Custom date_format supported
- [x] Dry-run mode works
- [x] Error when destination exists

**Validation**: All archive tests pass + benchmark <500ms

---

#### Story 3: Helpful Error Messages
**Tests**: test_error_handling.py (8 tests)

**Acceptance Criteria**:
- [x] Error messages include: what/why/how
- [x] Error includes example of correct usage
- [x] Structured sections for LLM parsing
- [x] All error paths tested
- [x] Token-efficient (<100 tokens)

**Validation**: All error tests pass, manually review error messages

---

#### Story 4: Cross-Platform Reliability
**Tests**: test_cross_platform.py (9 tests) + CI/CD

**Acceptance Criteria**:
- [x] Tests pass on Linux, macOS, Windows
- [x] Paths normalized to forward slashes
- [x] Windows reserved names rejected on all platforms
- [x] Unicode folder names supported
- [x] Case-only renames handled

**Validation**: CI/CD shows green on all platforms

---

#### Story 5: Token-Efficient Operations
**Tests**: test_tool_integration.py (response format tests)

**Acceptance Criteria**:
- [x] minimal = ~50 tokens
- [x] concise = ~150 tokens
- [x] detailed = ~300+ tokens
- [x] Performance notes in docstring
- [x] Token estimates in responses

**Validation**: Response format tests pass, manual token counting

---

### 9.2 End-User Acceptance Tests (EUATs)

**Performed By**: Real users or user proxies
**Environment**: Staging or production-like vault

#### EUAT 1: Archive Project Workflow
**Scenario**: User completes a project and wants to archive it

**Steps**:
1. User tells agent: "I finished the website-redesign project, please archive it"
2. Agent archives projects/website-redesign
3. User verifies: Folder moved to archive/YYYY-MM-DD/website-redesign
4. User checks: Links in other notes updated
5. User confirms: No broken links

**Success Criteria**: Workflow completes smoothly, user satisfied

---

#### EUAT 2: Mistake Recovery
**Scenario**: User accidentally asks agent to archive a note file

**Steps**:
1. User says: "Archive meeting-notes.md"
2. Agent attempts operation
3. Agent receives error about file vs folder
4. Agent self-corrects: "I see meeting-notes.md is a file. Did you mean to archive the meeting-notes folder, or delete/move the note file?"
5. User clarifies
6. Agent performs correct operation

**Success Criteria**: Agent recovers gracefully, user not frustrated

---

#### EUAT 3: Custom Archive Location
**Scenario**: User wants old drafts archived to special location

**Steps**:
1. User says: "Archive my old drafts to old-drafts folder organized by month"
2. Agent calls: obsidian_folder_manage(path="drafts/old", operation="archive", archive_base="old-drafts", date_format="%Y/%m")
3. User verifies: Folder moved to old-drafts/2025/01/old/
4. User satisfied with organization

**Success Criteria**: Custom parameters work as expected

---

## 10. Quality Gates (Pre-Merge Checklist)

### Gate 1: Static Analysis & Type Safety
**Run**: `uv run ruff check src/tools/obsidian_folder_manager/` AND `uv run mypy src/tools/obsidian_folder_manager/`

**Criteria**:
- [ ] Ruff: 0 errors, 0 warnings
- [ ] Mypy: 0 errors (strict mode)
- [ ] All functions have type hints
- [ ] No `Any` types without justification

---

### Gate 2: Unit Tests
**Run**: `uv run pytest tests/tools/obsidian_folder_manager/ -v`

**Criteria**:
- [ ] 35+ tests pass
- [ ] 0 failures
- [ ] 0 skipped tests
- [ ] Test duration <10 seconds

---

### Gate 3: Test Coverage
**Run**: `uv run pytest --cov=src/tools/obsidian_folder_manager/ --cov-report=term-missing --cov-report=html`

**Criteria**:
- [ ] service.py: >90% coverage
- [ ] tool.py: >80% coverage (tool registration has limited testability)
- [ ] schemas.py: >90% coverage
- [ ] Overall: >90% coverage
- [ ] Review HTML report for missed edge cases

---

### Gate 4: Integration Tests
**Run**: `uv run pytest tests/integration/ -v`

**Criteria**:
- [ ] All integration tests pass
- [ ] Tool-to-service integration verified
- [ ] System prompt integration verified
- [ ] Cross-component integration verified

---

### Gate 5: Cross-Platform Tests (CI/CD)
**Run**: GitHub Actions workflow on push

**Criteria**:
- [ ] ubuntu-latest: Python 3.11, 3.12 ✓
- [ ] macos-latest: Python 3.11, 3.12 ✓
- [ ] windows-latest: Python 3.11, 3.12 ✓
- [ ] All 6 matrix combinations pass
- [ ] No platform-specific failures

---

### Gate 6: Tool Selection Evaluation
**Run**: `uv run python tests/evaluation/tool_selection_accuracy.py`

**Criteria**:
- [ ] Overall accuracy >95% (47+/50 tests)
- [ ] Obvious folder operations: 100%
- [ ] Obvious note operations: 100%
- [ ] Ambiguous cases: >80%
- [ ] Edge cases: >70%
- [ ] Mixed operations: >90%
- [ ] Results saved to JSON with timestamp

---

### Gate 7: Performance Benchmarks
**Run**: `uv run python tests/performance/folder_benchmark.py`

**Criteria**:
- [ ] Archive small folder: <100ms (p95)
- [ ] Archive medium folder: <500ms (p95)
- [ ] Archive large folder: <2s (p95)
- [ ] Wikilink small vault: <200ms
- [ ] Wikilink large vault: <2s
- [ ] Path validation: <10ms per call
- [ ] Results saved to benchmark report

---

### Gate 8: Documentation Review
**Manual Review**

**Criteria**:
- [ ] README.md updated with archive examples
- [ ] CHANGELOG.md updated with changes
- [ ] Tool docstring has all 7 required sections
- [ ] No spelling or grammar errors
- [ ] Examples are realistic and helpful
- [ ] All links work

---

### Gate 9: Code Review
**Manual Review**

**Criteria**:
- [ ] Code follows CLAUDE.md standards (TYPE SAFETY, KISS, YAGNI)
- [ ] Structured logging used throughout
- [ ] Error messages helpful and token-efficient
- [ ] No code duplication
- [ ] Comments explain "why", not "what"
- [ ] Security considerations addressed

---

### Gate 10: User Acceptance
**Manual Testing**

**Criteria**:
- [ ] EUAT 1 (Archive workflow) successful
- [ ] EUAT 2 (Mistake recovery) successful
- [ ] EUAT 3 (Custom archive) successful
- [ ] No user confusion about tool selection
- [ ] Performance acceptable in real usage

---

## 11. Test Execution Plan

### Phase 1: Tool Separation Testing (After SEP tasks)
**When**: After SEP-1 through SEP-5 complete

**Run**:
1. Unit tests: Path validation (5 tests)
2. Integration tests: Tool-to-service (1 test)
3. Quality Gate 1: Linting & type safety
4. Quality Gate 2: Unit tests
5. Manual: Review error messages for helpfulness

**Expected Duration**: 1 hour

---

### Phase 2: Archive Operation Testing (After ARCH tasks)
**When**: After ARCH-1 through ARCH-5 complete

**Run**:
1. Unit tests: Archive operation (10 tests)
2. Unit tests: Schema validation (5 tests)
3. Unit tests: Wikilink updates (6 tests)
4. Integration tests: Response formatting (3 tests)
5. Quality Gate 2: Unit tests (now 35+ tests)
6. Quality Gate 3: Coverage (should be >90%)
7. Performance benchmarks: Archive operations
8. Manual: Test archive with real vault

**Expected Duration**: 2 hours

---

### Phase 3: Cross-Platform Testing (After CROSS tasks)
**When**: After CROSS-1 through CROSS-5 complete

**Run**:
1. CI/CD: Push to trigger workflow
2. Monitor: All 6 platform combinations
3. Platform tests: 9 cross-platform tests
4. Quality Gate 5: Cross-platform tests
5. Manual: Test on local Windows/Mac if available

**Expected Duration**: 30 minutes (mostly waiting for CI/CD)

---

### Phase 4: Final Validation (Before Merge)
**When**: All implementation phases complete

**Run**:
1. All quality gates (1-10)
2. Tool selection evaluation suite (50 tests)
3. Performance benchmarks (6 benchmarks)
4. Regression tests (20 existing tests)
5. User acceptance tests (3 EUATs)
6. Code review checklist
7. Documentation review

**Expected Duration**: 3 hours

**Go/No-Go Decision**: All quality gates must pass before merge

---

## 12. Test Data Management

### 12.1 Test Fixtures

**Location**: `tests/fixtures/`

#### Fixture 1: Sample Vault Structure
**File**: `tests/fixtures/sample_vault/`

```
sample_vault/
├── projects/
│   ├── 2023/
│   │   └── old-website/
│   │       ├── overview.md
│   │       ├── tasks.md
│   │       └── notes.md
│   ├── 2024/
│   │   └── current-project/
│   │       └── README.md
│   └── alpha/
│       └── design.md
├── archive/
├── daily/
│   ├── 2025-01-20.md
│   └── 2025-01-21.md
├── index.md
└── .obsidian/
    └── (blocked)
```

**Purpose**: Realistic vault structure for integration tests

---

#### Fixture 2: Wikilink Test Notes
**File**: `tests/fixtures/wikilink_samples.md`

**Content**: Notes with all wikilink formats for testing updates

---

#### Fixture 3: Edge Case Folder Names
**File**: `tests/fixtures/edge_case_names.json`

```json
{
  "unicode": ["项目", "プロジェクト", "📁 folder"],
  "special_chars": ["folder-name", "folder_name", "folder (old)"],
  "windows_reserved": ["CON", "PRN", "AUX", "NUL"],
  "edge_cases": ["folder.2025", ".hidden", "folder with spaces"]
}
```

---

### 12.2 Test Data Generation

**File**: `tests/utils/test_data_generator.py` (new file)

**Functions**:
- `create_sample_vault(path, size="small")` - Generate vault with N notes
- `create_wikilink_test_notes(vault_path, target_folder)` - Generate notes linking to folder
- `generate_edge_case_names()` - Return list of edge case folder names

---

## 13. Continuous Testing

### 13.1 Pre-Commit Hooks
**File**: `.pre-commit-config.yaml` (if exists)

**Hooks**:
- `ruff check` - Linting
- `mypy` - Type checking
- `pytest tests/tools/obsidian_folder_manager/ -x` - Fast fail on first error

**Purpose**: Catch issues before commit

---

### 13.2 CI/CD On Every Push
**Trigger**: Push to any branch

**Runs**:
- All quality gates
- Full test suite
- Cross-platform matrix

**Notifications**: Fail build if any test fails

---

### 13.3 Scheduled Regression Testing
**Trigger**: Daily at 2 AM

**Runs**:
- Full test suite
- Performance benchmarks
- Generate trend reports

**Purpose**: Catch regressions early

---

## 14. Test Reporting

### 14.1 Test Report Formats

#### JUnit XML
**File**: `test-results/junit.xml`
**Purpose**: CI/CD integration

**Generate**: `pytest --junitxml=test-results/junit.xml`

---

#### HTML Coverage Report
**File**: `htmlcov/index.html`
**Purpose**: Visual coverage analysis

**Generate**: `pytest --cov --cov-report=html`

---

#### JSON Evaluation Report
**File**: `evaluation-results/tool-selection-YYYY-MM-DD.json`
**Purpose**: Track tool selection accuracy over time

---

#### Performance Benchmark Report
**File**: `benchmark-results/performance-YYYY-MM-DD.json`
**Purpose**: Track performance trends

---

### 14.2 Test Metrics Dashboard

**Tracked Metrics**:
- Total test count
- Pass/fail rate
- Test coverage percentage
- Tool selection accuracy
- Performance benchmark trends
- Time to run full suite

**Visualization**: Consider GitHub Actions summary or custom dashboard

---

## 15. Test Maintenance

### 15.1 Test Review Cadence
- **Weekly**: Review failed tests, update as needed
- **Monthly**: Review test coverage, add tests for gaps
- **Per Release**: Update evaluation suite with new scenarios

---

### 15.2 Test Debt Tracking
- Identify flaky tests
- Document known issues
- Plan test improvements
- Remove obsolete tests

---

## Summary: Testing Checklist

### Unit Tests (30+)
- [x] Path validation (5 tests)
- [x] Archive operation (10 tests)
- [x] Schema validation (5 tests)
- [x] Error handling (8 tests)
- [x] Wikilink updates (6 tests)

### Integration Tests (10)
- [x] Tool integration (4 tests)
- [x] System prompt integration (2 tests)
- [x] Cross-component integration (4 tests)

### E2E Tests (2)
- [x] Complete archive workflow (1 test)
- [x] Error recovery workflow (1 test)

### Cross-Platform Tests (9)
- [x] Path normalization (1 test)
- [x] Windows reserved names (1 test)
- [x] Case-only renames (1 test)
- [x] Unicode support (1 test)
- [x] Long paths (1 test)
- [x] Symlinks (1 test)
- [x] Permissions (1 test)
- [x] pathlib consistency (1 test)
- [x] Timestamps (1 test)

### Performance Tests (6)
- [x] Archive small folder (<100ms)
- [x] Archive medium folder (<500ms)
- [x] Archive large folder (<2s)
- [x] Wikilink small vault (<200ms)
- [x] Wikilink large vault (<2s)
- [x] Path validation (<10ms)

### Security Tests (6)
- [x] Directory traversal blocked
- [x] Absolute paths rejected
- [x] Sensitive folders protected
- [x] Symlink escape prevented
- [x] No code injection
- [x] No sensitive data in logs

### Evaluation Tests (50)
- [x] Obvious folder operations (10)
- [x] Obvious note operations (10)
- [x] Ambiguous cases (10)
- [x] Edge cases (10)
- [x] Mixed operations (10)

### Regression Tests (20)
- [x] All existing tests still pass

### Acceptance Tests (3 EUATs)
- [x] Archive project workflow
- [x] Mistake recovery
- [x] Custom archive location

### Quality Gates (10)
- [x] Static analysis & type safety
- [x] Unit tests
- [x] Test coverage (>90%)
- [x] Integration tests
- [x] Cross-platform tests
- [x] Tool selection evaluation (>95%)
- [x] Performance benchmarks
- [x] Documentation review
- [x] Code review
- [x] User acceptance

---

**Total Tests**: 135+ (unit + integration + e2e + platform + perf + security + evaluation + regression + acceptance)

**Target Metrics**:
- Test pass rate: 100%
- Coverage: >90%
- Tool selection accuracy: >95%
- Performance: All benchmarks met
- Cross-platform: 100% on Linux, macOS, Windows

---

**Document Version**: 1.0
**Last Updated**: 2025-01-22
**Next Review**: After implementation complete
