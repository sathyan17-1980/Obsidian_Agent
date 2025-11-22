# Complete Component Testing & Validation Checklist

**Purpose**: Ensure ALL components are tested, ALL validation commands documented, and ALL tests pass before deployment.

**Related Documents**:
- Test Strategy: `TESTING-AND-VALIDATION-STRATEGY.md`
- Pre-Deployment: `PRE-DEPLOYMENT-VALIDATION-SUMMARY.md`
- Full Suite: `FULL-TEST-SUITE-OVERVIEW.md`

---

## 1. Component Coverage Matrix

### 1.1 All Components to Test

| Component Type | File Path | What to Test | Test File | Status |
|----------------|-----------|--------------|-----------|--------|
| **📊 MODELS/SCHEMAS** | | | | |
| FolderOperation Enum | `src/tools/obsidian_folder_manager/schemas.py` | ARCHIVE enum added | `tests/tools/obsidian_folder_manager/test_schemas.py` | ☐ Write |
| ManageFolderRequest | `src/tools/obsidian_folder_manager/schemas.py` | archive_base, date_format fields | `tests/tools/obsidian_folder_manager/test_schemas.py` | ☐ Write |
| FolderOperationResult | `src/tools/obsidian_folder_manager/schemas.py` | Result metadata for archive | `tests/tools/obsidian_folder_manager/test_schemas.py` | ☐ Write |
| Pydantic Validation | `src/tools/obsidian_folder_manager/schemas.py` | Field validation rules | `tests/tools/obsidian_folder_manager/test_schemas.py` | ☐ Write |
| **🔧 SERVICES** | | | | |
| validate_folder_path() | `src/tools/obsidian_folder_manager/service.py` | File rejection, folder acceptance | `tests/tools/obsidian_folder_manager/test_service.py` | ☐ Write |
| _archive_folder() | `src/tools/obsidian_folder_manager/service.py` | Archive operation logic | `tests/tools/obsidian_folder_manager/test_service.py` | ☐ Write |
| manage_folder_service() | `src/tools/obsidian_folder_manager/service.py` | Archive operation routing | `tests/tools/obsidian_folder_manager/test_service.py` | ☐ Update |
| _update_wikilinks_for_folder_rename() | `src/tools/obsidian_folder_manager/service.py` | Wikilink updates for archive | `tests/tools/obsidian_folder_manager/test_wikilink_updates.py` | ☐ Write |
| Error Handling | `src/tools/obsidian_folder_manager/service.py` | All error paths | `tests/tools/obsidian_folder_manager/test_error_handling.py` | ☐ Write |
| **🎯 TOOLS** | | | | |
| obsidian_folder_manage | `src/tools/obsidian_folder_manager/tool.py` | Tool registration | `tests/tools/obsidian_folder_manager/test_tool.py` | ☐ Write |
| Tool Docstring | `src/tools/obsidian_folder_manager/tool.py` | Archive operation documented | Manual review | ☐ Review |
| Parameter Passing | `src/tools/obsidian_folder_manager/tool.py` | archive_base, date_format | `tests/integration/test_tool_integration.py` | ☐ Write |
| Response Formatting | `src/tools/obsidian_folder_manager/tool.py` | Archive response format | `tests/integration/test_tool_integration.py` | ☐ Write |
| **🌐 APIS** | | | | |
| Agent API | `src/main.py` | Tool execution endpoint | `tests/e2e/test_folder_workflows.py` | ☐ Write |
| Health Check | `src/main.py` | Service health | Smoke tests | ☐ Write |
| **🔗 INTEGRATIONS** | | | | |
| Vault Security | `src/shared/vault_security.py` | Path validation integration | `tests/integration/test_cross_component.py` | ☐ Write |
| Obsidian Parsers | `src/shared/obsidian_parsers.py` | Wikilink extraction | `tests/integration/test_cross_component.py` | ☐ Write |
| Config | `src/shared/config.py` | System prompt decision tree | `tests/integration/test_system_prompt_integration.py` | ☐ Write |
| Logging | `src/shared/logging.py` | Structured logging | `tests/integration/test_cross_component.py` | ☐ Write |

**Summary**:
- **Models/Schemas**: 4 components to test
- **Services**: 5 components to test
- **Tools**: 4 components to test
- **APIs**: 2 components to test
- **Integrations**: 4 components to test
- **TOTAL**: 19 components requiring tests

---

## 2. Complete Test Writing Plan

### 2.1 Tests to Write (New)

#### Test File 1: `tests/tools/obsidian_folder_manager/test_schemas.py` (NEW)

**Tests to Write**: 5 tests

```python
"""Tests for folder manager schemas."""
import pytest
from pydantic import ValidationError
from src.tools.obsidian_folder_manager.schemas import (
    FolderOperation,
    ManageFolderRequest,
    FolderOperationResult,
)


class TestSchemaValidation:
    """Tests for schema validation."""

    def test_folder_operation_enum_has_archive(self):
        """Test that ARCHIVE operation exists in enum."""
        # ☐ WRITE THIS TEST
        assert hasattr(FolderOperation, 'ARCHIVE')
        assert FolderOperation.ARCHIVE == "archive"
        # Verify all operations
        operations = [FolderOperation.CREATE, FolderOperation.RENAME,
                     FolderOperation.MOVE, FolderOperation.DELETE,
                     FolderOperation.LIST, FolderOperation.ARCHIVE]
        assert len(operations) == 6

    def test_manage_folder_request_archive_params(self):
        """Test archive parameters in request schema."""
        # ☐ WRITE THIS TEST
        request = ManageFolderRequest(
            path="test-folder",
            operation=FolderOperation.ARCHIVE,
            archive_base="custom-archive",
            date_format="%Y/%m",
        )
        assert request.archive_base == "custom-archive"
        assert request.date_format == "%Y/%m"

    def test_request_validation_with_archive(self):
        """Test ManageFolderRequest validates with archive operation."""
        # ☐ WRITE THIS TEST
        request = ManageFolderRequest(
            path="projects/old",
            operation=FolderOperation.ARCHIVE,
        )
        # Should use defaults
        assert request.archive_base == "archive"
        assert request.date_format == "%Y-%m-%d"

    def test_invalid_operation_rejected(self):
        """Test invalid operation strings rejected by schema."""
        # ☐ WRITE THIS TEST
        with pytest.raises(ValidationError):
            ManageFolderRequest(
                path="test",
                operation="invalid_operation"
            )

    def test_archive_params_defaults(self):
        """Test archive parameters have correct defaults."""
        # ☐ WRITE THIS TEST
        request = ManageFolderRequest(
            path="test",
            operation=FolderOperation.CREATE,
        )
        # Archive params should still have defaults even for non-archive operations
        assert request.archive_base == "archive"
        assert request.date_format == "%Y-%m-%d"
```

**Status**: ☐ File needs to be created
**Command to Run**: `uv run pytest tests/tools/obsidian_folder_manager/test_schemas.py -v`

---

#### Test File 2: `tests/tools/obsidian_folder_manager/test_service.py` (UPDATE EXISTING)

**Tests to Add**: 13 tests (5 path validation + 8 archive operation)

**New Test Class 1: TestPathValidation**

```python
class TestPathValidation:
    """Tests for path validation."""

    async def test_rejects_md_extension(self, tmp_path):
        """Test that .md file paths are rejected."""
        # ☐ WRITE THIS TEST
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

    async def test_rejects_markdown_extension(self, tmp_path):
        """Test that .markdown extension also rejected."""
        # ☐ WRITE THIS TEST
        # Similar to above but with .markdown extension

    async def test_rejects_any_file_extension(self, tmp_path):
        """Test that any file extension rejected (.txt, .json, etc.)"""
        # ☐ WRITE THIS TEST
        # Test .json, .txt, .pdf, .csv

    async def test_accepts_folder_without_extension(self, tmp_path):
        """Test that folder paths without extensions are accepted."""
        # ☐ WRITE THIS TEST
        # Test: "projects/2025", "daily", "archive/old-projects"

    async def test_accepts_folder_with_dot_in_name(self, tmp_path):
        """Test folders with dots but no extension accepted."""
        # ☐ WRITE THIS TEST
        # Test: "version-2.0", "data.2025"
```

**New Test Class 2: TestArchiveFolderOperation**

```python
class TestArchiveFolderOperation:
    """Tests for ARCHIVE folder operation."""

    async def test_archive_simple_folder(self, tmp_path):
        """Test archiving folder with default settings."""
        # ☐ WRITE THIS TEST
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / "old-project").mkdir()

        request = ManageFolderRequest(
            path="old-project",
            operation=FolderOperation.ARCHIVE,
        )

        result = await manage_folder_service(
            request=request,
            vault_path=str(vault),
            max_folder_depth=10,
            max_wikilink_scan_notes=1000,
        )

        assert result.success is True
        assert "archive/" in result.new_path
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
        assert result.new_path == f"archive/{date_str}/old-project"

    async def test_archive_with_wikilink_updates(self, tmp_path):
        """Test archive updates wikilinks in other notes."""
        # ☐ WRITE THIS TEST
        # Create folder with note
        # Create wikilink to that note
        # Archive folder
        # Verify wikilink updated

    async def test_archive_nested_folder(self, tmp_path):
        """Test archive folder with nested subfolders."""
        # ☐ WRITE THIS TEST

    async def test_archive_custom_base(self, tmp_path):
        """Test archive with custom base folder."""
        # ☐ WRITE THIS TEST

    async def test_archive_custom_date_format(self, tmp_path):
        """Test archive with different date formats."""
        # ☐ WRITE THIS TEST

    async def test_archive_dry_run(self, tmp_path):
        """Test dry-run shows destination without moving."""
        # ☐ WRITE THIS TEST

    async def test_archive_destination_exists_error(self, tmp_path):
        """Test error when archive destination already exists."""
        # ☐ WRITE THIS TEST

    async def test_archive_folder_not_found(self, tmp_path):
        """Test error when source folder doesn't exist."""
        # ☐ WRITE THIS TEST
```

**Status**: ☐ Add 13 new tests to existing file
**Command to Run**: `uv run pytest tests/tools/obsidian_folder_manager/test_service.py -v`

---

#### Test File 3: `tests/tools/obsidian_folder_manager/test_error_handling.py` (NEW)

**Tests to Write**: 8 tests

```python
"""Tests for error handling in folder manager."""


class TestErrorHandling:
    """Tests for error message quality and handling."""

    async def test_error_message_structure(self, tmp_path):
        """Test error messages have what/why/how structure."""
        # ☐ WRITE THIS TEST

    async def test_file_path_error_suggests_note_manage(self, tmp_path):
        """Test file path error mentions note_manage."""
        # ☐ WRITE THIS TEST

    async def test_archive_conflict_error_provides_options(self, tmp_path):
        """Test archive destination exists error helpful."""
        # ☐ WRITE THIS TEST

    async def test_wikilink_scan_failure_non_fatal(self, tmp_path):
        """Test wikilink update failures don't block operation."""
        # ☐ WRITE THIS TEST

    async def test_permission_error_handled(self, tmp_path):
        """Test file permission errors handled gracefully."""
        # ☐ WRITE THIS TEST

    async def test_disk_full_error_handled(self, tmp_path):
        """Test disk full during archive handled."""
        # ☐ WRITE THIS TEST

    async def test_invalid_date_format_error(self, tmp_path):
        """Test invalid date format strings rejected."""
        # ☐ WRITE THIS TEST

    async def test_circular_archive_prevented(self, tmp_path):
        """Test cannot archive folder into itself."""
        # ☐ WRITE THIS TEST
```

**Status**: ☐ File needs to be created
**Command to Run**: `uv run pytest tests/tools/obsidian_folder_manager/test_error_handling.py -v`

---

#### Test File 4: `tests/tools/obsidian_folder_manager/test_wikilink_updates.py` (NEW)

**Tests to Write**: 6 tests

```python
"""Tests for wikilink updates during folder operations."""


class TestWikilinkUpdates:
    """Tests for wikilink update functionality."""

    async def test_updates_regular_wikilinks(self, tmp_path):
        """Test regular wikilink format updated."""
        # ☐ WRITE THIS TEST
        # [[projects/alpha/note]] → [[archive/2025-01-22/alpha/note]]

    async def test_updates_wikilinks_with_display_text(self, tmp_path):
        """Test display text format updated."""
        # ☐ WRITE THIS TEST
        # [[projects/alpha/note|Display]] → [[archive/.../note|Display]]

    async def test_updates_wikilinks_with_headings(self, tmp_path):
        """Test heading anchors preserved."""
        # ☐ WRITE THIS TEST
        # [[projects/alpha/note#section]] → [[archive/.../note#section]]

    async def test_updates_embed_syntax(self, tmp_path):
        """Test embed wikilinks updated."""
        # ☐ WRITE THIS TEST
        # ![[projects/alpha/image.png]] → ![[archive/.../image.png]]

    async def test_does_not_update_unrelated_wikilinks(self, tmp_path):
        """Test other wikilinks unchanged."""
        # ☐ WRITE THIS TEST

    async def test_wikilink_update_count_accurate(self, tmp_path):
        """Test metadata reports correct update count."""
        # ☐ WRITE THIS TEST
```

**Status**: ☐ File needs to be created
**Command to Run**: `uv run pytest tests/tools/obsidian_folder_manager/test_wikilink_updates.py -v`

---

#### Test File 5: `tests/integration/test_tool_integration.py` (NEW)

**Tests to Write**: 4 tests

```python
"""Integration tests for tool registration and execution."""


class TestToolIntegration:
    """Tests for tool-to-service integration."""

    async def test_tool_to_service_integration(self):
        """Test tool function correctly calls service layer."""
        # ☐ WRITE THIS TEST

    async def test_response_format_minimal(self):
        """Test minimal response format returns ~50 tokens."""
        # ☐ WRITE THIS TEST

    async def test_response_format_concise(self):
        """Test concise response format returns ~150 tokens."""
        # ☐ WRITE THIS TEST

    async def test_response_format_detailed(self):
        """Test detailed response format returns full details."""
        # ☐ WRITE THIS TEST
```

**Status**: ☐ File needs to be created
**Command to Run**: `uv run pytest tests/integration/test_tool_integration.py -v`

---

#### Test File 6: `tests/integration/test_system_prompt_integration.py` (NEW)

**Tests to Write**: 2 tests

```python
"""Integration tests for system prompt."""


class TestSystemPromptIntegration:
    """Tests for system prompt integration."""

    def test_decision_tree_in_system_prompt(self):
        """Test decision tree added to config."""
        # ☐ WRITE THIS TEST
        from src.shared.config import agent_system_prompt
        assert "Tool Selection Decision Tree" in agent_system_prompt

    def test_system_prompt_formatting(self):
        """Test system prompt is valid and parseable."""
        # ☐ WRITE THIS TEST
```

**Status**: ☐ File needs to be created
**Command to Run**: `uv run pytest tests/integration/test_system_prompt_integration.py -v`

---

#### Test File 7: `tests/integration/test_cross_component.py` (NEW)

**Tests to Write**: 4 tests

```python
"""Cross-component integration tests."""


class TestCrossComponentIntegration:
    """Tests for cross-component integration."""

    async def test_vault_security_integration(self, tmp_path):
        """Test path validation integrates with vault_security."""
        # ☐ WRITE THIS TEST

    async def test_obsidian_parsers_integration(self, tmp_path):
        """Test wikilink parsing uses obsidian_parsers."""
        # ☐ WRITE THIS TEST

    async def test_logging_integration(self, tmp_path):
        """Test structured logging works throughout."""
        # ☐ WRITE THIS TEST

    async def test_config_integration(self, tmp_path):
        """Test config settings respected."""
        # ☐ WRITE THIS TEST
```

**Status**: ☐ File needs to be created
**Command to Run**: `uv run pytest tests/integration/test_cross_component.py -v`

---

#### Test File 8: `tests/e2e/test_folder_workflows.py` (NEW)

**Tests to Write**: 2 tests

```python
"""End-to-end workflow tests."""


class TestFolderWorkflows:
    """E2E tests for complete workflows."""

    async def test_complete_archive_workflow(self):
        """Test end-to-end archive from agent request to result."""
        # ☐ WRITE THIS TEST

    async def test_error_recovery_workflow(self):
        """Test agent recovers from tool selection error."""
        # ☐ WRITE THIS TEST
```

**Status**: ☐ File needs to be created
**Command to Run**: `uv run pytest tests/e2e/test_folder_workflows.py -v`

---

#### Test File 9: `tests/security/test_folder_security.py` (NEW)

**Tests to Write**: 6 tests

```python
"""Security tests for folder manager."""


class TestFolderSecurity:
    """Security validation tests."""

    async def test_directory_traversal_blocked(self, tmp_path):
        """Test directory traversal attacks prevented."""
        # ☐ WRITE THIS TEST

    async def test_absolute_path_rejected(self, tmp_path):
        """Test absolute paths rejected."""
        # ☐ WRITE THIS TEST

    async def test_sensitive_folders_protected(self, tmp_path):
        """Test sensitive folders protected."""
        # ☐ WRITE THIS TEST

    async def test_no_code_injection(self, tmp_path):
        """Test folder names cannot inject code."""
        # ☐ WRITE THIS TEST

    async def test_symlink_escape_prevented(self, tmp_path):
        """Test symlinks cannot escape vault."""
        # ☐ WRITE THIS TEST

    async def test_no_sensitive_data_in_logs(self, tmp_path, caplog):
        """Test logs don't contain sensitive data."""
        # ☐ WRITE THIS TEST
```

**Status**: ☐ File needs to be created
**Command to Run**: `uv run pytest tests/security/test_folder_security.py -v`

---

### 2.2 Tests to Update (Existing)

#### Test File: `tests/tools/obsidian_folder_manager/test_service.py` (EXISTING)

**Current Status**: 20 existing tests (all passing)

**Updates Needed**:
- [ ] Add `TestPathValidation` class (5 new tests)
- [ ] Add `TestArchiveFolderOperation` class (8 new tests)
- [ ] Ensure existing 20 tests still pass (regression check)

**Status**: ☐ Add 13 tests to existing file
**Command to Run**: `uv run pytest tests/tools/obsidian_folder_manager/test_service.py -v`

---

### 2.3 Test Summary

| Test File | Status | Tests to Write | Tests to Update | Total Tests |
|-----------|--------|----------------|-----------------|-------------|
| test_schemas.py | NEW | 5 | - | 5 |
| test_service.py | UPDATE | 13 | 20 (keep passing) | 33 |
| test_error_handling.py | NEW | 8 | - | 8 |
| test_wikilink_updates.py | NEW | 6 | - | 6 |
| test_tool_integration.py | NEW | 4 | - | 4 |
| test_system_prompt_integration.py | NEW | 2 | - | 2 |
| test_cross_component.py | NEW | 4 | - | 4 |
| test_folder_workflows.py | NEW | 2 | - | 2 |
| test_folder_security.py | NEW | 6 | - | 6 |
| **TOTAL** | **8 NEW + 1 UPDATE** | **50** | **20** | **70** |

---

## 3. Complete Validation Commands

### 3.1 Pre-Implementation Validation

**Before writing any code, verify environment:**

```bash
# 1. Verify Python version
python --version  # Should be >=3.12

# 2. Verify UV installed
uv --version

# 3. Install dependencies
uv sync

# 4. Verify dependencies installed
uv pip list

# Expected output should include:
# - pytest >=8.4.2
# - pytest-asyncio >=1.2.0
# - mypy >=1.18.2
# - ruff >=0.14.0
```

**Status**: ☐ Complete

---

### 3.2 During Implementation Validation

**After writing each component, validate immediately:**

#### After Schema Changes

```bash
# 1. Type check schemas
uv run mypy src/tools/obsidian_folder_manager/schemas.py --strict

# 2. Run schema tests
uv run pytest tests/tools/obsidian_folder_manager/test_schemas.py -v

# Expected: All 5 schema tests pass
```

**Status**: ☐ Complete

---

#### After Service Changes

```bash
# 1. Type check service
uv run mypy src/tools/obsidian_folder_manager/service.py --strict

# 2. Lint service
uv run ruff check src/tools/obsidian_folder_manager/service.py

# 3. Run service tests
uv run pytest tests/tools/obsidian_folder_manager/test_service.py -v

# Expected: All 33 tests pass (20 existing + 13 new)
```

**Status**: ☐ Complete

---

#### After Tool Changes

```bash
# 1. Type check tool
uv run mypy src/tools/obsidian_folder_manager/tool.py --strict

# 2. Lint tool
uv run ruff check src/tools/obsidian_folder_manager/tool.py

# 3. Run tool integration tests
uv run pytest tests/integration/test_tool_integration.py -v

# Expected: All 4 tool integration tests pass
```

**Status**: ☐ Complete

---

#### After Config/Shared Changes

```bash
# 1. Type check config
uv run mypy src/shared/config.py --strict

# 2. Run system prompt tests
uv run pytest tests/integration/test_system_prompt_integration.py -v

# Expected: Both system prompt tests pass
```

**Status**: ☐ Complete

---

### 3.3 Complete Test Suite Validation

**Run all tests together:**

```bash
# 1. Run ALL tests
uv run pytest tests/ -v

# Expected output:
# tests/tools/obsidian_folder_manager/test_schemas.py ........... 5 passed
# tests/tools/obsidian_folder_manager/test_service.py ........... 33 passed
# tests/tools/obsidian_folder_manager/test_error_handling.py ... 8 passed
# tests/tools/obsidian_folder_manager/test_wikilink_updates.py . 6 passed
# tests/integration/test_tool_integration.py .................... 4 passed
# tests/integration/test_system_prompt_integration.py ........... 2 passed
# tests/integration/test_cross_component.py ..................... 4 passed
# tests/e2e/test_folder_workflows.py ............................ 2 passed
# tests/security/test_folder_security.py ........................ 6 passed
# ============================================= 70 passed in X.XXs

# 2. Run with coverage
uv run pytest tests/ -v \
    --cov=src/tools/obsidian_folder_manager/ \
    --cov=src/shared/config.py \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-fail-under=90

# Expected: Coverage >90%

# 3. Run only unit tests
uv run pytest tests/tools/obsidian_folder_manager/ -v -m unit

# Expected: All unit tests pass

# 4. Run only integration tests
uv run pytest tests/integration/ -v -m integration

# Expected: All integration tests pass

# 5. Run only security tests
uv run pytest tests/security/ -v

# Expected: All 6 security tests pass
```

**Status**: ☐ Complete

---

### 3.4 Code Quality Validation

```bash
# 1. Lint all modified files
uv run ruff check src/tools/obsidian_folder_manager/
uv run ruff check src/shared/config.py

# Expected: 0 errors, 0 warnings

# 2. Format check
uv run ruff format --check src/tools/obsidian_folder_manager/
uv run ruff format --check src/shared/config.py

# Expected: All files already formatted

# 3. Type check all modified files
uv run mypy src/tools/obsidian_folder_manager/ --strict
uv run mypy src/shared/config.py --strict

# Expected: 0 errors, all functions typed

# 4. Type coverage report
uv run mypy src/tools/obsidian_folder_manager/ --strict --html-report mypy-report/

# Expected: >99% type coverage
# Open: mypy-report/index.html to view
```

**Status**: ☐ Complete

---

### 3.5 Pre-Deployment Validation (Complete Suite)

```bash
# Run the complete pre-deployment validation suite
# This is the FINAL check before deployment

# 1. Dependency Validation
uv sync --frozen
uv pip list

# 2. Code Quality
uv run ruff check src/tools/obsidian_folder_manager/ --output-format=github
uv run ruff format --check src/tools/obsidian_folder_manager/
uv run mypy src/tools/obsidian_folder_manager/ --strict

# 3. Unit Tests + Coverage
uv run pytest tests/tools/obsidian_folder_manager/ -v -m unit \
    --cov=src/tools/obsidian_folder_manager/ \
    --cov-report=term-missing \
    --cov-fail-under=90

# 4. Integration Tests
uv run pytest tests/integration/ -v -m integration

# 5. E2E Tests
uv run pytest tests/e2e/ -v

# 6. Security Tests
uv run pytest tests/security/ -v

# 7. ALL Tests
uv run pytest tests/ -v

# Expected: ALL checks pass, 0 errors, 0 failures
```

**Status**: ☐ Complete

---

## 4. Ensuring All Tests Pass

### 4.1 Test Execution Checklist

Run tests in this order and ensure each step passes before proceeding:

#### Step 1: Verify Environment
```bash
☐ uv sync --frozen
☐ uv pip list | grep -E "pytest|mypy|ruff"
```
**Must Pass**: All dependencies installed

---

#### Step 2: Schema Tests
```bash
☐ uv run pytest tests/tools/obsidian_folder_manager/test_schemas.py -v
```
**Must Pass**: 5/5 tests pass

---

#### Step 3: Service Tests
```bash
☐ uv run pytest tests/tools/obsidian_folder_manager/test_service.py -v
```
**Must Pass**: 33/33 tests pass (20 existing + 13 new)

---

#### Step 4: Error Handling Tests
```bash
☐ uv run pytest tests/tools/obsidian_folder_manager/test_error_handling.py -v
```
**Must Pass**: 8/8 tests pass

---

#### Step 5: Wikilink Tests
```bash
☐ uv run pytest tests/tools/obsidian_folder_manager/test_wikilink_updates.py -v
```
**Must Pass**: 6/6 tests pass

---

#### Step 6: Integration Tests
```bash
☐ uv run pytest tests/integration/test_tool_integration.py -v
☐ uv run pytest tests/integration/test_system_prompt_integration.py -v
☐ uv run pytest tests/integration/test_cross_component.py -v
```
**Must Pass**: 10/10 tests pass (4+2+4)

---

#### Step 7: E2E Tests
```bash
☐ uv run pytest tests/e2e/test_folder_workflows.py -v
```
**Must Pass**: 2/2 tests pass

---

#### Step 8: Security Tests
```bash
☐ uv run pytest tests/security/test_folder_security.py -v
```
**Must Pass**: 6/6 tests pass

---

#### Step 9: Full Suite
```bash
☐ uv run pytest tests/ -v --tb=short
```
**Must Pass**: 70/70 tests pass, 0 failures, 0 errors

---

#### Step 10: Coverage Check
```bash
☐ uv run pytest tests/tools/obsidian_folder_manager/ \
    --cov=src/tools/obsidian_folder_manager/ \
    --cov-report=term-missing \
    --cov-fail-under=90
```
**Must Pass**: Coverage >90%

---

#### Step 11: Type Checking
```bash
☐ uv run mypy src/tools/obsidian_folder_manager/ --strict
```
**Must Pass**: 0 errors

---

#### Step 12: Linting
```bash
☐ uv run ruff check src/tools/obsidian_folder_manager/
```
**Must Pass**: 0 errors, 0 warnings

---

### 4.2 Failure Handling Procedures

**If Any Test Fails**:

1. **Don't Proceed** - Fix failing test before continuing
2. **Read Error Message** - Pytest provides detailed error output
3. **Check Logs** - Use `--tb=long` for full traceback: `pytest --tb=long`
4. **Debug Test** - Run single failing test: `pytest path/to/test.py::test_name -v`
5. **Fix Code or Test** - Determine if issue is in code or test
6. **Re-run** - Verify fix: `pytest path/to/test.py::test_name -v`
7. **Re-run Suite** - Ensure no regressions: `pytest tests/ -v`

**Common Failure Patterns**:

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| `ModuleNotFoundError` | Missing import or dependency | Add import or install package |
| `TypeError: ... missing required argument` | Function signature changed | Update test call signature |
| `AssertionError: assert False` | Test logic incorrect | Review test expectations |
| `FileNotFoundError` | Test fixture missing | Create test fixture/temp files |
| `ValidationError` | Pydantic validation failed | Check schema field types |

---

### 4.3 Success Criteria Summary

**All Tests Pass When**:

✅ **Schema Tests (5)**: All Pydantic models validate correctly
✅ **Service Tests (33)**: All business logic works (20 existing + 13 new)
✅ **Error Handling (8)**: All error paths tested
✅ **Wikilink Tests (6)**: All wikilink update scenarios work
✅ **Tool Integration (4)**: Tool registration and execution works
✅ **System Prompt (2)**: Decision tree integrated
✅ **Cross-Component (4)**: All integrations work
✅ **E2E Tests (2)**: Complete workflows work
✅ **Security Tests (6)**: All security validations pass

**Total**: 70/70 tests pass (100% pass rate)

**Additional Success Criteria**:
✅ Test coverage >90%
✅ MyPy type checking: 0 errors
✅ Ruff linting: 0 errors
✅ All existing tests still pass (no regressions)

---

## 5. Implementation Timeline with Validation

### Week 1: Models & Services

**Day 1-2: Schemas**
- [ ] Update `schemas.py` (add ARCHIVE enum, archive params)
- [ ] Write `test_schemas.py` (5 tests)
- [ ] **Validate**: `pytest test_schemas.py -v` → 5/5 pass
- [ ] **Validate**: `mypy schemas.py --strict` → 0 errors

**Day 3-4: Service Layer**
- [ ] Add `validate_folder_path()` to `service.py`
- [ ] Write path validation tests (5 tests)
- [ ] **Validate**: `pytest test_service.py::TestPathValidation -v` → 5/5 pass
- [ ] Add `_archive_folder()` to `service.py`
- [ ] Write archive operation tests (8 tests)
- [ ] **Validate**: `pytest test_service.py::TestArchiveFolderOperation -v` → 8/8 pass
- [ ] **Validate**: Existing 20 tests still pass

**Day 5: Error Handling & Wikilinks**
- [ ] Write `test_error_handling.py` (8 tests)
- [ ] Write `test_wikilink_updates.py` (6 tests)
- [ ] **Validate**: All tests pass

---

### Week 2: Tools & Integration

**Day 1-2: Tool Layer**
- [ ] Update `tool.py` (enhance docstring, add params)
- [ ] Write `test_tool_integration.py` (4 tests)
- [ ] **Validate**: Integration tests pass

**Day 3: System Integration**
- [ ] Update `config.py` (add decision tree)
- [ ] Write `test_system_prompt_integration.py` (2 tests)
- [ ] Write `test_cross_component.py` (4 tests)
- [ ] **Validate**: All integration tests pass

**Day 4: E2E & Security**
- [ ] Write `test_folder_workflows.py` (2 tests)
- [ ] Write `test_folder_security.py` (6 tests)
- [ ] **Validate**: All tests pass

**Day 5: Final Validation**
- [ ] Run complete test suite: `pytest tests/ -v`
- [ ] **Validate**: 70/70 tests pass
- [ ] Run coverage: `pytest --cov --cov-fail-under=90`
- [ ] **Validate**: >90% coverage
- [ ] Run quality checks: `ruff check && mypy --strict`
- [ ] **Validate**: 0 errors

---

## 6. Final Pre-Deployment Checklist

**Before creating pull request, verify ALL items checked**:

### Component Testing
- [ ] All 4 schema components tested (models/enums/validation)
- [ ] All 5 service components tested (functions/error handling)
- [ ] All 4 tool components tested (registration/params/responses)
- [ ] All 2 API components tested (endpoints/health)
- [ ] All 4 integration components tested (security/parsers/config/logging)

### Test Writing
- [ ] All 50 new tests written
- [ ] All 20 existing tests still pass
- [ ] Total 70 tests pass (100% pass rate)
- [ ] All test files created as specified

### Validation Commands
- [ ] All dependency validation commands pass
- [ ] All code quality validation commands pass
- [ ] All test execution commands pass
- [ ] All coverage commands pass (>90%)
- [ ] All type checking commands pass (0 errors)
- [ ] All linting commands pass (0 errors)

### All Tests Pass
- [ ] Schema tests: 5/5 pass
- [ ] Service tests: 33/33 pass
- [ ] Error handling: 8/8 pass
- [ ] Wikilink tests: 6/6 pass
- [ ] Tool integration: 4/4 pass
- [ ] System prompt: 2/2 pass
- [ ] Cross-component: 4/4 pass
- [ ] E2E tests: 2/2 pass
- [ ] Security tests: 6/6 pass
- [ ] **TOTAL: 70/70 pass ✅**

### Final Validation
- [ ] `pytest tests/ -v` → 70 passed, 0 failed
- [ ] `pytest --cov --cov-fail-under=90` → Coverage >90%
- [ ] `mypy src/tools/obsidian_folder_manager/ --strict` → 0 errors
- [ ] `ruff check src/tools/obsidian_folder_manager/` → 0 errors
- [ ] No regressions in existing functionality

---

**When all items checked: Ready for deployment** ✅

---

**Version**: 1.0
**Last Updated**: 2025-01-22
**Next Review**: After implementation complete
