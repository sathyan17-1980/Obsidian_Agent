# Implementation Plan: Obsidian Folder Management Tool Enhancement

## 1. Meta Information

| Field | Value |
|-------|-------|
| **Feature ID** | TOOL-FOLDER-ENHANCE-001 |
| **Feature Name** | Folder Management Tool Enhancement |
| **Owner** | Development Team |
| **Status** | Planning → Ready for Implementation |
| **Priority** | P0 (Tool confusion is impacting user experience) |
| **Target Version** | v0.3.0 |
| **Estimated Effort** | 5-6 days |
| **Created** | 2025-01-22 |
| **Last Updated** | 2025-01-22 |

---

## 2. Goal & Problem Statement

### Current Pain Point

**Problem**: LLM agents confuse `obsidian_folder_manage` and `obsidian_note_manage` tools approximately 20% of the time, leading to:
- Failed operations with cryptic errors
- Multiple retries consuming tokens
- User frustration with incorrect tool selection
- Broken workflows when agent uses wrong tool

**Impact Metrics**:
- ~20% tool selection error rate in production agent logs
- Average 2.3 retries per confused operation
- Estimated 15-30% token waste from retries
- User reported "agent doesn't understand folders vs files"

### Measurable Goal

**Primary Goal**: Reduce LLM tool confusion from 20% to <5% through 6-layer separation strategy and enhanced agent guidance.

**Secondary Goal**: Add archive operation with automatic date-based organization to enable seamless project lifecycle management.

**Target Metrics**:
| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|-------------------|
| Tool selection accuracy | 80% | >95% | 50-test evaluation suite |
| Archive operation latency | N/A | <500ms | Benchmark on 1000-note vault |
| Wikilink update correctness | 95% | >99% | Integration test suite |
| Cross-platform test pass rate | 100% | 100% | CI/CD on Linux, macOS, Windows |
| Test coverage | 85% | >90% | pytest --cov |

### Non-Goals (Out of Scope)

- ❌ Batch folder operations (e.g., archive 10 folders at once) - Future feature
- ❌ Folder templates or scaffolding - Different feature
- ❌ Folder permissions or access control - Not applicable to Obsidian
- ❌ Folder synchronization across vaults - Out of scope
- ❌ Changes to note management tool - Separate tool, no modifications

---

## 3. User Stories

### Personas

| Persona | Description | Primary Use Cases |
|---------|-------------|-------------------|
| **Knowledge Worker** | Uses Obsidian daily for projects, notes, research | Organize projects, archive completed work, maintain vault structure |
| **LLM Agent** | AI assistant using tools to help user | Select correct tool, execute operations efficiently, provide helpful errors |
| **Developer** | Maintains and extends the agent | Clear separation, testable code, cross-platform compatibility |

### User Story 1: Clear Tool Separation

**As a** LLM agent
**I want** clear guidance on when to use folder_manage vs note_manage
**So that** I select the right tool on the first try without retries

**Acceptance Criteria**:
- [ ] Tool docstring includes "Use this when" section with 5+ specific scenarios
- [ ] Tool docstring includes "Do NOT use for" section with 5+ negative scenarios
- [ ] System prompt includes decision tree for tool selection
- [ ] Path validation rejects .md files with error message suggesting correct tool
- [ ] Runtime validation detects wrong-tool usage and provides correction guidance
- [ ] Evaluation tests show >95% tool selection accuracy across 50 test scenarios

**Priority**: P0 (Must Have)

---

### User Story 2: Archive Old Projects

**As a** knowledge worker
**I want** to archive old project folders with automatic date-based organization
**So that** I can keep my vault clean without manually creating archive folders and dates

**Acceptance Criteria**:
- [ ] Archive operation creates folder at `archive/YYYY-MM-DD/folder-name`
- [ ] Wikilinks are automatically updated in all affected notes
- [ ] Archive operation completes in <500ms for typical folder (10-50 notes)
- [ ] Custom archive base folder can be specified (e.g., `old-projects/YYYY-MM-DD/`)
- [ ] Custom date format can be specified (e.g., `%Y/%m` for year/month)
- [ ] Dry-run mode shows destination without moving folder
- [ ] Error when archive destination already exists (prevents overwrites)

**Priority**: P0 (Must Have)

---

### User Story 3: Helpful Error Messages

**As a** LLM agent
**I want** error messages that tell me exactly what went wrong and which tool to use instead
**So that** I can self-correct without user intervention

**Acceptance Criteria**:
- [ ] Error message includes: what happened, why it failed, which tool to use instead
- [ ] Error message includes example of correct tool usage
- [ ] Error message formatted for easy LLM parsing (structured sections)
- [ ] All error paths tested with assertions on error message content
- [ ] Token-efficient error messages (<100 tokens)

**Priority**: P1 (Should Have)

---

### User Story 4: Cross-Platform Reliability

**As a** developer
**I want** the folder tool to work identically on Windows, macOS, and Linux
**So that** users get consistent behavior regardless of platform

**Acceptance Criteria**:
- [ ] All tests pass on Linux, macOS, Windows via CI/CD
- [ ] Path separators normalized to forward slashes in all outputs
- [ ] Windows reserved names (CON, PRN, etc.) rejected on all platforms
- [ ] Unicode folder names supported on all platforms
- [ ] Case-only renames handled correctly on case-insensitive filesystems (macOS, Windows)

**Priority**: P0 (Must Have)

---

### User Story 5: Token-Efficient Operations

**As a** LLM agent
**I want** to control response verbosity based on my needs
**So that** I don't waste tokens on unnecessary details

**Acceptance Criteria**:
- [ ] `response_format="minimal"` returns ~50 tokens (status only)
- [ ] `response_format="concise"` returns ~150 tokens (status + key metadata)
- [ ] `response_format="detailed"` returns ~300+ tokens (full details)
- [ ] Performance notes documented in tool docstring
- [ ] Token estimates included in all responses

**Priority**: P1 (Should Have)

---

## 4. Success Criteria

### Functional Requirements (P0)

1. **Path Validation**
   - Rejects paths ending in `.md` with error directing to note_manage
   - Rejects paths with file extensions with helpful error
   - Accepts folder paths without extensions
   - Error messages include tool selection guidance

2. **Archive Operation**
   - Creates archive path: `archive/YYYY-MM-DD/folder-name`
   - Updates wikilinks in all affected notes
   - Supports custom archive base folder
   - Supports custom date format
   - Dry-run mode for testing
   - Error when destination exists

3. **Tool Separation**
   - Enhanced docstring with "Use this when" (5+ items)
   - Enhanced docstring with "Do NOT use for" (5+ items)
   - System prompt decision tree
   - Runtime wrong-tool detection
   - 95%+ tool selection accuracy

### Non-Functional Requirements (P0)

1. **Performance**
   - Archive operation: <500ms for typical folder (10-50 notes)
   - Path validation: <10ms per call
   - Wikilink updates: <2s for 1000-note vault
   - List operation: <100ms for 50 folders

2. **Quality**
   - All linters pass: `ruff check` and `mypy` with no errors
   - Test coverage >90% on service layer
   - All existing tests continue to pass (no regressions)
   - 35+ tests total (20 existing + 15 new)

3. **Usability**
   - Error messages <100 tokens
   - Clear examples in tool docstring (7+ examples)
   - Token estimates in all responses
   - Structured error format for LLM parsing

4. **Security**
   - Path traversal protection maintained
   - Blocked patterns enforced (.obsidian, .git)
   - Windows reserved names validated
   - Confirm-delete protection maintained

### Metrics with Targets

| Metric | Baseline | Target | How to Measure |
|--------|----------|--------|----------------|
| **Tool Selection Accuracy** | 80% | >95% | 50-test evaluation suite with folder/note confusion scenarios |
| **Archive Latency** | N/A | <500ms | Benchmark: archive folder with 25 notes, 5MB total |
| **Wikilink Update Time** | ~2s | <2s | Benchmark: 1000-note vault, 50 wikilink updates |
| **Test Coverage** | 85% | >90% | `pytest --cov src/tools/obsidian_folder_manager/` |
| **Linter Pass Rate** | 100% | 100% | `ruff check && mypy` with no errors |
| **Cross-Platform Tests** | 100% | 100% | CI/CD on ubuntu-latest, macos-latest, windows-latest |
| **Error Message Tokens** | N/A | <100 | Count tokens in all error messages |
| **Total Test Count** | 20 | 35+ | `pytest --collect-only` count |

---

## 5. Documentation to Reference

### Must Read Before Starting

1. **Global Development Rules**
   - File: `CLAUDE.md`
   - Sections: Type Safety, Agent Tool Docstrings, Logging Rules, Testing Requirements
   - Why: Non-negotiable standards that must be followed

2. **Planning Framework**
   - File: `IMPLEMENTATION-PLAN-TEMPLATE.md`
   - Why: Template used to create this plan

3. **Planning Improvements Analysis**
   - File: `PLANNING-IMPROVEMENTS.md`
   - Why: Understand what makes a good plan vs bad plan

### Code to Review

1. **Existing Folder Manager Implementation**
   - Files:
     - `src/tools/obsidian_folder_manager/tool.py` (agent registration)
     - `src/tools/obsidian_folder_manager/schemas.py` (data models)
     - `src/tools/obsidian_folder_manager/service.py` (business logic)
   - Why: Understand current implementation, add to it, don't rewrite

2. **Existing Tests**
   - File: `tests/tools/obsidian_folder_manager/test_service.py`
   - Current: 20 passing tests
   - Why: Understand test patterns, ensure no regressions

3. **Note Manager Tool (for comparison)**
   - Files:
     - `src/tools/obsidian_note_manager/tool.py`
     - `src/tools/obsidian_note_manager/schemas.py`
   - Why: Understand note_manage to ensure clear separation

4. **Shared Utilities**
   - `src/shared/vault_security.py` - Path validation patterns
   - `src/shared/obsidian_parsers.py` - Wikilink parsing
   - `src/shared/config.py` - System prompt
   - `src/shared/logging.py` - Structured logging patterns

### Standards to Follow

1. **Type Safety**: All functions must have type annotations, strict mypy enforcement
2. **KISS Principle**: Simple, readable solutions over clever abstractions
3. **YAGNI Principle**: Don't build features until actually needed
4. **Agent Tool Docstrings**: 7 required sections (see CLAUDE.md)
5. **Structured Logging**: Always use kwargs, never string formatting
6. **Testing**: Mirror source structure, unit + integration tests
7. **Cross-Platform**: Use pathlib.Path, normalize to forward slashes
8. **Async Operations**: Use aioshutil, aiofiles for I/O

### External Resources

1. **Obsidian Wikilink Format**: `[[path/to/note]]`, `[[note|display]]`, `[[note#heading]]`
2. **Python pathlib Documentation**: https://docs.python.org/3/library/pathlib.html
3. **Pydantic BaseModel**: https://docs.pydantic.dev/latest/
4. **Structlog**: https://www.structlog.org/en/stable/

---

## 6. Task Breakdown with Definition of Done

### Phase 1: Tool Separation (Path Validation + Documentation) - Est: 2 days

#### Task SEP-1: Add Path Validation Function
**Estimate**: 1 hour
**File**: `src/tools/obsidian_folder_manager/service.py`

**Description**: Create `validate_folder_path()` function that rejects file paths with helpful errors.

**Implementation**:
```python
def validate_folder_path(path: str) -> None:
    """Validate that path is a folder, not a file.

    Rejects:
    - Paths ending in .md, .markdown, .txt
    - Paths with any file extension

    Raises helpful error with tool selection guidance.
    """
```

**Definition of Done**:
- [ ] Function implemented with type hints
- [ ] Rejects paths ending in `.md` with error mentioning `obsidian_note_manage`
- [ ] Rejects paths with any extension (e.g., `.json`, `.txt`)
- [ ] Error message includes example of correct tool usage
- [ ] Error message formatted with clear sections (what/why/how)
- [ ] Integrated into `manage_folder_service()` as first validation step
- [ ] Logged with structured logging: `logger.info("path_validation", ...)`

---

#### Task SEP-2: Add Path Validation Tests
**Estimate**: 1 hour
**File**: `tests/tools/obsidian_folder_manager/test_service.py`

**Description**: Add 3 tests for path validation to `TestSecurityValidation` class.

**Definition of Done**:
- [ ] `test_rejects_file_path_with_md_extension` - asserts ValueError with "operates on FOLDERS"
- [ ] `test_rejects_file_path_with_any_extension` - asserts ValueError with "appears to be a file"
- [ ] `test_accepts_folder_path_without_extension` - asserts success
- [ ] All tests pass: `pytest tests/tools/obsidian_folder_manager/test_service.py::TestSecurityValidation -v`
- [ ] Linters pass: `ruff check src/tools/obsidian_folder_manager/ && mypy src/tools/obsidian_folder_manager/`

**Dependencies**: Requires SEP-1 complete

---

#### Task SEP-3: Enhanced Tool Docstring
**Estimate**: 2 hours
**File**: `src/tools/obsidian_folder_manager/tool.py`

**Description**: Replace entire tool docstring with enhanced version including 7 required sections per CLAUDE.md.

**Required Sections**:
1. One-line summary
2. "Use this when" (5+ specific scenarios)
3. "Do NOT use for" (5+ scenarios with tool redirects)
4. Args (with parameter guidance and token implications)
5. Returns (with format details)
6. Performance Notes (token usage, execution time, limits)
7. Examples (7+ realistic examples covering all operations)

**Definition of Done**:
- [ ] All 7 sections present in correct order
- [ ] "Use this when" has 5+ folder operation scenarios
- [ ] "Do NOT use for" explicitly directs to `obsidian_note_manage` for file operations
- [ ] "Do NOT use for" explicitly directs to `obsidian_vault_query` for search
- [ ] All parameters documented with WHY to choose different values
- [ ] `archive_base` and `date_format` parameters added to signature and docstring
- [ ] Performance notes include token estimates for all response formats
- [ ] 7+ examples with realistic paths (not "foo", "test")
- [ ] Examples include archive operation with different configurations
- [ ] Token estimates explicitly mentioned (minimal ~50, concise ~150, detailed ~300+)
- [ ] Path format rules section with ✅ folder vs ❌ file examples
- [ ] Docstring follows Google-style format
- [ ] No spelling or grammar errors

**Dependencies**: None (can be done in parallel with SEP-1)

---

#### Task SEP-4: System Prompt Enhancement
**Estimate**: 1 hour
**File**: `src/shared/config.py`

**Description**: Add tool selection decision tree to `agent_system_prompt`.

**Definition of Done**:
- [ ] Decision tree section added after line 100 (after tool descriptions)
- [ ] Decision tree has 4 steps: extension check → keyword check → content/metadata check → container check
- [ ] Tool categories section added: STRUCTURE (folders) vs CONTENT (notes) vs DISCOVERY (search) vs RELATIONSHIP (graph)
- [ ] Each tool listed under correct category
- [ ] Clear examples for each decision point
- [ ] Integrated naturally into existing prompt flow

**Dependencies**: None (can be done in parallel)

---

#### Task SEP-5: Verify Tool Separation
**Estimate**: 2 hours
**File**: N/A (testing task)

**Description**: Manual testing and evaluation of tool separation effectiveness.

**Definition of Done**:
- [ ] Create 20 test prompts mixing folder/note operations
- [ ] Run agent against test prompts, measure tool selection accuracy
- [ ] Document: prompt, expected tool, actual tool, success/failure
- [ ] Achieve >90% accuracy on test set (target: 18/20 correct)
- [ ] Identify failure patterns and document in notes
- [ ] If <90%, iterate on docstring/system prompt and retest
- [ ] Save test prompts to `tests/evaluation/tool_selection_tests.json` (create file)

**Dependencies**: Requires SEP-1, SEP-2, SEP-3, SEP-4 complete

---

### Phase 2: Archive Operation Implementation - Est: 2 days

#### Task ARCH-1: Update Schemas
**Estimate**: 30 minutes
**File**: `src/tools/obsidian_folder_manager/schemas.py`

**Description**: Add ARCHIVE enum and archive parameters to request schema.

**Definition of Done**:
- [ ] `ARCHIVE = "archive"` added to `FolderOperation` enum with docstring
- [ ] `archive_base: str = Field(default="archive", ...)` added to `ManageFolderRequest`
- [ ] `date_format: str = Field(default="%Y-%m-%d", ...)` added to `ManageFolderRequest`
- [ ] Field descriptions clearly explain purpose and defaults
- [ ] Type hints correct
- [ ] Mypy passes: `mypy src/tools/obsidian_folder_manager/schemas.py`

---

#### Task ARCH-2: Implement Archive Service Function
**Estimate**: 3 hours
**File**: `src/tools/obsidian_folder_manager/service.py`

**Description**: Implement `_archive_folder()` function with wikilink updates.

**Definition of Done**:
- [ ] Function signature matches: `async def _archive_folder(full_path, request, vault_path, vault_root, max_wikilink_scan_notes) -> FolderOperationResult`
- [ ] Validates source folder exists
- [ ] Generates archive path: `{archive_base}/{date_format}/{folder_name}`
- [ ] Checks destination doesn't exist (error if exists)
- [ ] Dry-run mode returns result without moving
- [ ] Creates archive date folder with parents
- [ ] Moves folder using `aioshutil.move()`
- [ ] Updates wikilinks if `update_wikilinks=True`
- [ ] Returns result with new_path and metadata (archive_path, date, archive_base, links_updated)
- [ ] Structured logging: "folder_archived" with old_path, archive_path, date
- [ ] Error messages helpful with suggestions
- [ ] Import datetime added at top of file
- [ ] Type hints on all parameters and return
- [ ] Docstring with Args, Returns, Raises sections

---

#### Task ARCH-3: Integrate Archive into Service Router
**Estimate**: 30 minutes
**File**: `src/tools/obsidian_folder_manager/service.py`

**Description**: Add ARCHIVE case to operation router in `manage_folder_service()`.

**Definition of Done**:
- [ ] `elif request.operation == FolderOperation.ARCHIVE:` added after LIST case
- [ ] Calls `_archive_folder()` with correct parameters
- [ ] Result properly returned and logged
- [ ] No changes to existing operation cases
- [ ] Linters pass

**Dependencies**: Requires ARCH-1, ARCH-2 complete

---

#### Task ARCH-4: Update Tool Registration
**Estimate**: 1 hour
**File**: `src/tools/obsidian_folder_manager/tool.py`

**Description**: Add archive parameters to tool function and update response formatting.

**Definition of Done**:
- [ ] `archive_base: str = "archive"` added to function signature
- [ ] `date_format: str = "%Y-%m-%d"` added to function signature
- [ ] Parameters passed to `ManageFolderRequest()` in tool function
- [ ] Response formatting handles ARCHIVE operation metadata
- [ ] Archive date displayed in response if present
- [ ] Links_updated displayed for ARCHIVE like RENAME/MOVE
- [ ] Token estimate accurate for ARCHIVE responses

**Dependencies**: Requires ARCH-3 complete

---

#### Task ARCH-5: Archive Operation Tests
**Estimate**: 3 hours
**File**: `tests/tools/obsidian_folder_manager/test_service.py`

**Description**: Add comprehensive test suite for archive operation.

**Tests to Create**:
1. `test_archive_simple_folder` - Basic archive with default settings
2. `test_archive_with_wikilink_updates` - Verify wikilinks updated
3. `test_archive_custom_base` - Custom archive_base parameter
4. `test_archive_custom_date_format` - Custom date_format parameter
5. `test_archive_dry_run` - Dry-run doesn't move folder
6. `test_archive_destination_exists_error` - Error when destination exists
7. `test_archive_folder_not_found` - Error when source doesn't exist

**Definition of Done**:
- [ ] New test class `TestArchiveFolderOperation` created
- [ ] All 7 tests implemented with descriptive docstrings
- [ ] Tests use `tmp_path` fixture for isolation
- [ ] Tests verify: success status, new_path format, folder moved, wikilinks updated
- [ ] Date verification using `datetime.now().strftime()`
- [ ] Error tests use `pytest.raises()` with match pattern
- [ ] All tests pass: `pytest tests/tools/obsidian_folder_manager/test_service.py::TestArchiveFolderOperation -v`
- [ ] Existing tests still pass (no regressions)

**Dependencies**: Requires ARCH-4 complete

---

### Phase 3: Cross-Platform Testing & CI/CD - Est: 1 day

#### Task CROSS-1: Create CI/CD Workflow
**Estimate**: 2 hours
**File**: `.github/workflows/test.yml`

**Description**: Create GitHub Actions workflow for multi-platform testing.

**Definition of Done**:
- [ ] File created at `.github/workflows/test.yml`
- [ ] Matrix strategy: [ubuntu-latest, macos-latest, windows-latest]
- [ ] Python versions: [3.11, 3.12]
- [ ] Steps: checkout, install uv, install python, sync deps, lint, test folder manager, test all
- [ ] Linting: `ruff check` and `mypy` both run
- [ ] Folder manager tests run separately for visibility
- [ ] All tests run with `-v` flag
- [ ] fail-fast: false (test all platforms even if one fails)
- [ ] Workflow file valid YAML

---

#### Task CROSS-2: Path Normalization Audit
**Estimate**: 2 hours
**File**: `src/tools/obsidian_folder_manager/service.py`

**Description**: Audit all path returns and ensure forward slash normalization.

**Definition of Done**:
- [ ] All path strings returned use `.replace("\\", "/")` before return
- [ ] Check: `FolderOperationResult.path` field
- [ ] Check: `FolderOperationResult.new_path` field
- [ ] Check: All metadata dictionary path values
- [ ] Check: Error messages with paths
- [ ] Check: Log messages with paths
- [ ] Add test: `test_path_normalization_windows_style` to verify
- [ ] Test passes on all platforms

---

#### Task CROSS-3: Windows Reserved Names Test
**Estimate**: 1 hour
**File**: `tests/tools/obsidian_folder_manager/test_service.py`

**Description**: Add test verifying Windows reserved names rejected on all platforms.

**Definition of Done**:
- [ ] Test `test_windows_reserved_names` created
- [ ] Tests names: CON, PRN, AUX, NUL, COM1, LPT1
- [ ] Each name raises `ValueError` from vault_security validation
- [ ] Test passes on Linux, macOS, Windows
- [ ] Existing vault_security validation already handles this (verify)

---

#### Task CROSS-4: Unicode Folder Names Test
**Estimate**: 1 hour
**File**: `tests/tools/obsidian_folder_manager/test_service.py`

**Description**: Add test with unicode folder names (emoji, non-ASCII).

**Definition of Done**:
- [ ] Test `test_unicode_folder_names` created
- [ ] Tests: "项目/2025" (Chinese), "プロジェクト" (Japanese), "📁 Projects" (emoji)
- [ ] CREATE operation succeeds
- [ ] RENAME operation succeeds
- [ ] ARCHIVE operation succeeds
- [ ] Paths correctly normalized
- [ ] Test passes on all platforms via CI/CD

---

#### Task CROSS-5: Verify CI/CD Green
**Estimate**: 2 hours (includes wait time)
**File**: N/A (CI/CD monitoring)

**Description**: Push branch, monitor CI/CD, fix any platform-specific failures.

**Definition of Done**:
- [ ] Code pushed to branch
- [ ] CI/CD workflow runs automatically
- [ ] All 6 matrix jobs pass (3 OS × 2 Python versions)
- [ ] Linting passes on all platforms
- [ ] All tests pass on all platforms
- [ ] Test run time <5 minutes per platform
- [ ] If failures: investigate logs, fix issues, push again
- [ ] Green checkmarks on all CI/CD jobs

**Dependencies**: Requires CROSS-1, CROSS-2, CROSS-3, CROSS-4 complete

---

### Phase 4: Documentation & Final Polish - Est: 0.5 days

#### Task DOC-1: Update README
**Estimate**: 1 hour
**File**: `README.md`

**Description**: Add archive operation examples to tool description.

**Definition of Done**:
- [ ] Archive operation described in obsidian_folder_manage section (around line 145)
- [ ] 2+ code examples showing archive usage
- [ ] Example shows auto-dating result in comment
- [ ] Example shows custom archive_base
- [ ] Consistent formatting with existing README style
- [ ] No broken links
- [ ] No spelling/grammar errors

---

#### Task DOC-2: Update CHANGELOG
**Estimate**: 30 minutes
**File**: `CHANGELOG.md` (create if doesn't exist)

**Description**: Document changes in changelog format.

**Definition of Done**:
- [ ] New section: `## [Unreleased]` or appropriate version
- [ ] ### Added: Archive operation, 6-layer tool separation
- [ ] ### Enhanced: Tool docstrings with negative guidance
- [ ] ### Fixed: None (new feature, no fixes)
- [ ] ### Changed: System prompt includes decision tree
- [ ] Follows Keep a Changelog format

---

#### Task DOC-3: Final Test Pass
**Estimate**: 1 hour
**File**: N/A (testing task)

**Description**: Run complete test suite and verify metrics.

**Definition of Done**:
- [ ] Run: `pytest tests/tools/obsidian_folder_manager/ -v`
- [ ] Result: 35+ tests pass, 0 failures
- [ ] Run: `pytest tests/ -v`
- [ ] Result: All tests pass, no regressions
- [ ] Run: `pytest --cov src/tools/obsidian_folder_manager/`
- [ ] Result: >90% coverage on service layer
- [ ] Run: `ruff check src/tools/obsidian_folder_manager/`
- [ ] Result: 0 errors
- [ ] Run: `mypy src/tools/obsidian_folder_manager/`
- [ ] Result: 0 errors
- [ ] Screenshot or save output for documentation

---

#### Task DOC-4: Create Evaluation Test Suite
**Estimate**: 2 hours
**File**: `tests/evaluation/tool_selection_accuracy.py` (new file)

**Description**: Create automated evaluation suite for tool selection accuracy.

**Definition of Done**:
- [ ] File created with 50 test scenarios
- [ ] Each scenario: prompt, expected tool, reasoning
- [ ] Test scenarios cover:
  - Obvious folder operations (10 tests)
  - Obvious note operations (10 tests)
  - Ambiguous cases (10 tests)
  - Edge cases (10 tests)
  - Mixed operations (10 tests)
- [ ] Script runs agent against each prompt
- [ ] Script measures accuracy: correct_tool / total_tests
- [ ] Results saved to JSON with timestamp
- [ ] Target: >95% accuracy (47+/50 tests pass)
- [ ] README section explaining how to run evaluation suite

**Dependencies**: Requires all other tasks complete

---

## 7. Validation Strategy

### Test Pyramid

```
      [E2E Tests]            2 tests
       /         \           - Full agent workflow with archive
      /           \          - Multi-step operation with tool selection
     /             \
[Integration Tests]         8 tests
   /               \        - Archive with wikilink updates
  /                 \       - Cross-platform path handling
 /                   \      - Tool selection decision tree
/                     \
[Unit Tests]               25+ tests
 - Path validation (3)
 - Archive operation (7)
 - Schema validation (5)
 - Error handling (10+)
```

**Total Expected**: 35+ tests

---

### Quality Gates (Must Pass Before Merge)

#### Gate 1: Linting & Type Safety
```bash
uv run ruff check src/tools/obsidian_folder_manager/
uv run mypy src/tools/obsidian_folder_manager/
```
**Criteria**: 0 errors, 0 warnings

---

#### Gate 2: Unit Tests
```bash
uv run pytest tests/tools/obsidian_folder_manager/ -v
```
**Criteria**: 35+ tests pass, 0 failures, 0 skipped

---

#### Gate 3: Test Coverage
```bash
uv run pytest --cov=src/tools/obsidian_folder_manager/ --cov-report=term-missing
```
**Criteria**: >90% coverage on service.py

---

#### Gate 4: Integration Tests
```bash
uv run pytest tests/ -v -m integration
```
**Criteria**: All integration tests pass

---

#### Gate 5: Cross-Platform Tests
```bash
# Automated via CI/CD
```
**Criteria**: All tests pass on Linux, macOS, Windows (3 platforms)

---

#### Gate 6: Tool Selection Evaluation
```bash
uv run python tests/evaluation/tool_selection_accuracy.py
```
**Criteria**: >95% accuracy (47+/50 tests correct tool selection)

---

#### Gate 7: Performance Benchmarks
```bash
uv run python tests/performance/folder_benchmark.py
```
**Criteria**:
- Archive operation: <500ms for 25-note folder
- Wikilink updates: <2s for 1000-note vault
- Path validation: <10ms per call

---

### Manual Validation Scenarios

#### Scenario 1: Tool Confusion Prevention
1. Start agent with vault
2. Ask: "Create a new note called test.md in projects folder"
3. Expected: Agent uses `obsidian_note_manage` (NOT folder_manage)
4. Verify: Note created, no error about folder vs file
5. Ask: "Create a new folder called test in projects"
6. Expected: Agent uses `obsidian_folder_manage`
7. Verify: Folder created

---

#### Scenario 2: Archive Workflow
1. Create folder: `projects/2023/old-website` with 5 notes
2. Create note: `index.md` with wikilink: `[[projects/2023/old-website/overview]]`
3. Ask agent: "Archive the old-website folder"
4. Expected: Agent uses `obsidian_folder_manage` with `operation="archive"`
5. Verify:
   - Folder moved to `archive/2025-01-22/old-website/`
   - Wikilink updated to `[[archive/2025-01-22/old-website/overview]]`
   - Agent reports links updated count

---

#### Scenario 3: Error Recovery
1. Ask agent: "Archive projects/note.md"
2. Expected: Error message says "operates on FOLDERS only" and suggests `obsidian_note_manage`
3. Verify: Error message includes example of correct tool usage
4. Ask agent: "Delete the note.md file"
5. Expected: Agent uses `obsidian_note_manage` with `operation="delete"`

---

#### Scenario 4: Cross-Platform Paths
1. Run on Windows: Archive folder with nested structure
2. Verify: All returned paths use forward slashes (not backslashes)
3. Verify: Wikilinks use forward slashes
4. Run same test on macOS and Linux
5. Verify: Identical output (path format consistent)

---

## 8. Risk Assessment & Mitigation

| Risk | Impact | Probability | Mitigation | Rollback Plan |
|------|--------|-------------|------------|---------------|
| **Wikilink updates break vault** | High | Low | • Comprehensive tests with real wikilink patterns<br>• Dry-run mode for testing<br>• Wikilink update unit tested independently<br>• Integration test with real vault structure | • Revert commit<br>• Restore from backup<br>• Wikilink updates can be disabled via parameter |
| **Cross-platform path bugs** | Medium | Medium | • CI/CD on 3 platforms<br>• Path normalization audit<br>• Pathlib.Path usage (not os.path)<br>• Unicode test cases | • Platform-specific fixes<br>• Disable feature on problematic platform |
| **Tool confusion persists** | High | Low | • 6-layer separation strategy<br>• Evaluation suite (50 tests)<br>• Manual validation scenarios<br>• User feedback loop | • Iterate on docstring/prompt<br>• Add more negative guidance<br>• Runtime detection improvements |
| **Archive destination conflicts** | Low | Medium | • Check destination exists before move<br>• Helpful error with 3 resolution options<br>• Dry-run mode for testing | • Manual move to different location<br>• Delete conflicting archive<br>• Use custom archive_base |
| **Performance regression** | Medium | Low | • Performance benchmarks in tests<br>• Wikilink scan limited to 1000 notes<br>• Async operations throughout | • Optimize wikilink scan algorithm<br>• Add caching for repeated scans |
| **Type errors from mypy** | Low | Low | • Strict type annotations<br>• Mypy in CI/CD<br>• Type hints on all functions | • Fix type errors immediately<br>• Run mypy before every commit |
| **Test coverage gaps** | Medium | Low | • Track coverage with pytest-cov<br>• Quality gate: >90% coverage<br>• Review coverage report before merge | • Add tests for uncovered lines<br>• Mandatory before merge |
| **Breaking changes to API** | High | Very Low | • No changes to existing operation parameters<br>• Only additions (archive params)<br>• All existing tests must pass | • Deprecate with warnings first<br>• Provide migration guide |

---

## 9. Desired Codebase Structure (End State)

### Modified Files

```
src/tools/obsidian_folder_manager/
├── tool.py        # MODIFIED
│   ├── Enhanced docstring (7 sections, 400+ lines)
│   ├── Added archive_base parameter
│   ├── Added date_format parameter
│   └── Updated response formatting for ARCHIVE operation
│
├── schemas.py     # MODIFIED
│   ├── Added ARCHIVE to FolderOperation enum
│   ├── Added archive_base field to ManageFolderRequest
│   └── Added date_format field to ManageFolderRequest
│
└── service.py     # MODIFIED
    ├── Added validate_folder_path() function (new)
    ├── Added _archive_folder() function (new)
    ├── Integrated validation in manage_folder_service()
    └── Added ARCHIVE case to operation router

src/shared/
└── config.py      # MODIFIED
    └── Enhanced agent_system_prompt with decision tree

tests/tools/obsidian_folder_manager/
└── test_service.py  # MODIFIED
    ├── Added TestArchiveFolderOperation class (7 tests)
    ├── Added path validation tests (3 tests)
    ├── Added Windows reserved names test (1 test)
    └── Added unicode folder names test (1 test)
```

### New Files

```
.github/workflows/
└── test.yml       # NEW - CI/CD for 3 platforms

tests/evaluation/
├── tool_selection_accuracy.py  # NEW - 50-test evaluation suite
└── tool_selection_tests.json   # NEW - Test scenarios data

tests/performance/
└── folder_benchmark.py  # NEW - Performance benchmarks

FOLDER-MANAGEMENT-ENHANCEMENT-PLAN.md  # NEW - This document
CHANGELOG.md       # NEW or MODIFIED - Release notes
```

### File-Level Changes Summary

| File | Lines Changed | Type | Key Changes |
|------|--------------|------|-------------|
| `tool.py` | +250 | Modified | Enhanced docstring, archive params |
| `schemas.py` | +15 | Modified | ARCHIVE enum, archive fields |
| `service.py` | +120 | Modified | validate_folder_path(), _archive_folder() |
| `config.py` | +30 | Modified | System prompt decision tree |
| `test_service.py` | +300 | Modified | 12+ new tests |
| `test.yml` | +50 | New | CI/CD workflow |
| `tool_selection_accuracy.py` | +200 | New | Evaluation suite |
| `README.md` | +20 | Modified | Archive examples |
| `CHANGELOG.md` | +15 | Modified | Release notes |

**Total**: ~1000 lines added/modified

---

## 10. Additional Considerations

### Security Considerations

- [x] **Path Traversal**: Existing vault_security validation covers this
- [x] **Critical Folder Protection**: .obsidian and .git blocked by existing security
- [x] **Input Validation**: validate_folder_path() adds file extension validation
- [x] **Sensitive Data in Logs**: No sensitive data logged (only paths and metadata)
- [x] **Error Message Information Leakage**: Error messages reveal file structure, but acceptable for local tool

**Action Items**: None, existing security sufficient.

---

### Observability & Debugging

**Logging Strategy**:
- `folder_operation_started` - Log operation start with path, operation type
- `path_validation` - Log validation with path
- `folder_archived` - Log archive with old_path, archive_path, date
- `folder_operation_completed` - Log completion with success, duration_ms
- `folder_operation_failed` - Log errors with exception details

**Metrics to Track**:
- Operation duration (duration_ms)
- Wikilink update count (links_updated)
- Archive operations count (per day)
- Error rate by operation type
- Token usage by response_format

**Correlation**: All logs include operation context via structured logging kwargs.

---

### Accessibility & Usability

**Error Messages**:
- **What**: Clear statement of what went wrong
- **Why**: Explain why operation failed
- **How**: Provide actionable next steps or correct tool

Example:
```
❌ Invalid path for folder operation: 'projects/note.md'

This tool operates on FOLDERS only.
To work with note files, use:

obsidian_note_manage(
    path='projects/note.md',
    operation='read',
    response_format='concise'
)

Tool selection guide:
• Paths ending in .md → obsidian_note_manage
• Paths without extension → obsidian_folder_manage
```

**Help Text**: Enhanced tool docstring with 7+ examples

**Token Efficiency**: 3-tier response system (minimal/concise/detailed)

**Dry-Run Mode**: Test operations without side effects

---

### Future Extensibility

**Extension Points**:
1. **Custom Archive Strategies**: Currently date-based, could add:
   - Tag-based: `archive/by-tag/{tag-name}/`
   - Project-based: `archive/by-project/{project}/`
   - Size-based: `archive/large-projects/`

2. **Folder Templates**: Could add `template` parameter:
   - `operation="create"` with `template="project-structure"`
   - Creates predefined folder hierarchy

3. **Batch Operations**: Could add:
   - `paths: list[str]` for multi-folder archive
   - Returns batch operation result

**Design Decisions**:
- Enum-based operations enable easy addition of new operations
- Metadata dict in result allows flexible return data
- Service layer separated from tool registration (easy to add new interfaces)

---

### Performance Characteristics

**Performance Targets**:
- CREATE: 10-50ms
- RENAME: 50-500ms (depends on wikilink scan)
- MOVE: 50-500ms (depends on wikilink scan)
- ARCHIVE: 50-500ms (depends on wikilink scan)
- DELETE: 50-200ms
- LIST: 50-100ms (minimal), 100-500ms (detailed)

**Scalability Limits**:
- Wikilink scan: Limited to 1000 notes (configurable)
- List results: Capped at 200 folders per request
- Recursive depth: Limited to 5 levels

**Optimization Opportunities**:
- Cache wikilink extraction results
- Parallel wikilink scanning for large vaults
- Incremental wikilink updates (only changed files)

---

### Migration & Rollback

**Breaking Changes**: None (only additions)

**Backward Compatibility**:
- All existing operation parameters unchanged
- New parameters have defaults (archive_base="archive", date_format="%Y-%m-%d")
- Existing API calls work without modifications

**Migration Guide**: Not needed (no breaking changes)

**Rollback Triggers**:
- Tool selection accuracy <80% (worse than baseline)
- Test pass rate <100%
- Cross-platform failures
- Wikilink corruption reports

**Rollback Process**:
1. Revert last commit: `git revert HEAD`
2. Push revert to main
3. CI/CD verifies old version still works
4. User notification: "Archive feature temporarily disabled"

---

### Compliance & Standards

**CLAUDE.md Adherence**:
- [x] TYPE SAFETY: All functions have type annotations
- [x] KISS: Simple implementation, no clever abstractions
- [x] YAGNI: Only implementing requested features
- [x] Agent Tool Docstrings: 7 required sections included
- [x] Structured Logging: All logs use kwargs, no string formatting
- [x] Testing: Tests mirror source structure

**Code Style**:
- Ruff formatting enforced
- Google-style docstrings
- Max line length: 100 characters
- Async/await throughout

---

### Team Collaboration

**Code Review Checklist**:
- [ ] All quality gates pass
- [ ] Tool docstring has all 7 required sections
- [ ] Error messages include "what/why/how"
- [ ] Type hints on all functions
- [ ] Structured logging with appropriate levels
- [ ] Tests cover happy path + error cases
- [ ] Cross-platform tests pass
- [ ] No regressions in existing tests
- [ ] README updated with examples
- [ ] CHANGELOG updated

**Approval Required From**:
- Lead developer (code quality)
- Agent expert (tool docstring effectiveness)

**Communication**:
- Progress updates: Daily standups or async updates
- Blockers: Immediate notification via team chat
- Questions: Technical design decisions documented in PR comments

---

### Monitoring & Alerting

**Production Metrics**:
- Operation success rate (by operation type)
- Average operation duration
- Tool selection accuracy (sampled)
- Error rate by error type
- Wikilink update success rate

**Alerts**:
- Error rate >5% for any operation type
- Tool selection accuracy <90%
- Archive operation duration >2s (p95)
- Wikilink update failures >1%

**User Feedback**:
- Monitor user reports for tool confusion
- Track "wrong tool" error frequency
- Survey user satisfaction after implementation

---

## 11. Approval & Sign-off

### Stakeholder Review

| Stakeholder | Role | Approval Status | Date | Comments |
|-------------|------|-----------------|------|----------|
| [Name] | Lead Developer | Pending | - | - |
| [Name] | Agent Expert | Pending | - | - |
| [Name] | QA Lead | Pending | - | - |

### Implementation Authorization

- [ ] Plan reviewed and approved by lead developer
- [ ] Technical approach validated
- [ ] Resource allocation confirmed (5-6 days)
- [ ] Ready to begin Phase 1 implementation

**Authorized to Begin**: _____________________ Date: __________

---

## 12. Appendix

### Glossary

- **Tool Confusion**: When LLM agent selects wrong tool (e.g., folder_manage for note operation)
- **Wikilink**: Obsidian link format: `[[path/to/note]]`
- **Archive**: Move folder to dated archive location
- **Dry Run**: Simulate operation without making changes
- **Path Normalization**: Convert backslashes to forward slashes for consistency
- **Vertical Slice**: Self-contained feature module (tool.py, schemas.py, service.py)
- **Quality Gate**: Must-pass check before merge

---

### References

1. **CLAUDE.md**: Global development rules and standards
2. **IMPLEMENTATION-PLAN-TEMPLATE.md**: Template used to create this plan
3. **PLANNING-IMPROVEMENTS.md**: Analysis of what makes a good plan
4. **coding-agent.md**: Original implementation plan (superseded by this document)

---

### Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-01-22 | 1.0 | Initial comprehensive plan created using IMPLEMENTATION-PLAN-TEMPLATE | Development Team |

---

## Next Steps

1. **Review & Approve**: Stakeholders review this plan and provide sign-off
2. **Begin Phase 1**: Start with SEP-1 (path validation function)
3. **Daily Updates**: Progress tracking against task DoD checklist
4. **Quality Gates**: Run quality gates after each phase
5. **Phase Completion**: Mark phase complete when all tasks in phase have DoD satisfied

**Ready to begin implementation!** 🚀

