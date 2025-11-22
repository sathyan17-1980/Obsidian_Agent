# Implementation Plan Template

## Meta Information
- **Feature Name**: [Descriptive name]
- **Feature ID**: [Unique identifier, e.g., FEAT-001]
- **Created**: [Date]
- **Owner**: [Who is responsible]
- **Status**: [Planning | In Progress | Review | Complete]

---

## 1. Goal & Problem Statement

### 1.1 Problem Statement
**Current Pain Point**:
- What problem exists today?
- Who is affected by this problem?
- What is the business/user impact?

**Example**:
```
Problem: LLM agents frequently confuse folder_manage and note_manage tools, leading to:
- Failed operations (using wrong tool for task)
- Poor user experience (confusing error messages)
- Wasted tokens (retrying with correct tool)
- Impact: 20% of folder operations fail on first attempt due to tool confusion
```

### 1.2 Goal Statement
**Objective**: [One clear, measurable statement]

**Example**:
```
Goal: Reduce folder/note tool confusion to <5% by implementing 6-layer separation
strategy and adding archive operation with automatic date-based organization.
```

### 1.3 Non-Goals (Out of Scope)
**What we will NOT do**:
- [Item 1]
- [Item 2]

**Example**:
```
Non-Goals:
- Batch folder operations (future feature)
- Folder templates/scaffolding (future feature)
- Folder metadata (.folder-meta.json) (not in scope)
```

---

## 2. User Stories

### 2.1 User Personas
**Who will use this feature?**

| Persona | Role | Pain Point | Need |
|---------|------|------------|------|
| [Name] | [Role description] | [What problem they have] | [What they need] |

**Example**:
| Persona | Role | Pain Point | Need |
|---------|------|------------|------|
| Knowledge Worker | Uses Obsidian for PKM | Needs to reorganize vault structure but worried about breaking wikilinks | Safe folder operations with automatic wikilink updates |
| LLM Agent | Autonomous vault organizer | Gets confused between folder and note operations | Clear tool separation with explicit guidance |
| Power User | Manages large vaults | Manually archiving old projects is tedious | One-shot archive operation with auto-dating |

### 2.2 User Stories (with Acceptance Criteria)

**Format**: As a [persona], I want [capability], so that [benefit]

**Story 1**: Tool Separation
```
As an LLM agent,
I want clear differentiation between folder_manage and note_manage tools,
So that I can select the correct tool on first attempt without trial-and-error.

Acceptance Criteria:
- [ ] Tool docstrings include "Do NOT use for" section redirecting to correct tool
- [ ] Path validation rejects .md files with helpful error messages
- [ ] System prompt includes tool selection decision tree
- [ ] Tool selection accuracy >95% in evaluation tests
- [ ] Error messages guide to correct tool with example usage
```

**Story 2**: Archive Operation
```
As a knowledge worker,
I want to archive old project folders with automatic date-based organization,
So that I can keep my vault organized without manually creating dated folders.

Acceptance Criteria:
- [ ] Archive operation creates folders at archive/YYYY-MM-DD/folder-name
- [ ] Wikilinks automatically updated to new archive location
- [ ] Custom archive base folder supported (e.g., old-projects/)
- [ ] Custom date format supported (e.g., %Y/%m)
- [ ] Dry-run mode shows archive destination without moving
- [ ] Operation completes in <5s for folders with wikilink updates
```

**Story 3**: Cross-Platform Compatibility
```
As a multi-platform user,
I want folder operations to work identically on Windows, macOS, and Linux,
So that I can collaborate across platforms without path issues.

Acceptance Criteria:
- [ ] All operations pass tests on Windows, macOS, Linux
- [ ] Paths normalized to forward slashes (Obsidian standard)
- [ ] Windows reserved names (CON, PRN) rejected on all platforms
- [ ] Unicode folder names supported
- [ ] Case-only renames work on case-insensitive filesystems
```

---

## 3. Success Criteria

### 3.1 Functional Requirements
**Must Have (P0)**:
- [ ] [Requirement 1]
- [ ] [Requirement 2]

**Example**:
- [ ] Archive operation creates `archive/YYYY-MM-DD/folder` paths
- [ ] Path validation rejects `.md` files with actionable error
- [ ] All 6 operations work: CREATE, RENAME, MOVE, DELETE, LIST, ARCHIVE
- [ ] Wikilinks updated automatically on RENAME, MOVE, ARCHIVE
- [ ] Tests pass on Windows, macOS, Linux

**Should Have (P1)**:
- [ ] [Requirement 1]

**Example**:
- [ ] Dry-run mode for all destructive operations
- [ ] Custom archive_base and date_format parameters

**Could Have (P2)**:
- [ ] [Nice-to-have 1]

### 3.2 Non-Functional Requirements

**Performance**:
- [ ] CREATE operation: <50ms
- [ ] RENAME/MOVE/ARCHIVE (with wikilinks): <5s for 1000 notes
- [ ] DELETE operation: <200ms
- [ ] LIST operation: <500ms for 200 folders

**Quality**:
- [ ] 90%+ test coverage on service layer
- [ ] 0 mypy errors (strict mode)
- [ ] 0 ruff linting errors
- [ ] All tests pass on 3 platforms (CI/CD)

**UX**:
- [ ] Error messages include what/why/how-to-fix
- [ ] LLM tool selection accuracy >95%
- [ ] Token-efficient responses (3-tier system)

**Security**:
- [ ] Path traversal attacks blocked
- [ ] Critical folders protected (.obsidian, .git)
- [ ] Windows reserved names rejected
- [ ] No sensitive data in logs

### 3.3 Metrics & Measurement

| Metric | Baseline | Target | How to Measure |
|--------|----------|--------|----------------|
| [Metric name] | [Current value] | [Goal value] | [Measurement method] |

**Example**:
| Metric | Baseline | Target | How to Measure |
|--------|----------|--------|----------------|
| Tool selection accuracy | ~80% | >95% | Evaluation tests with 50 ambiguous prompts |
| Operation latency (archive) | N/A | <5s | Benchmark test with 1000-note vault |
| Test coverage (service layer) | 85% | >90% | pytest --cov report |
| Cross-platform test pass rate | 0% | 100% | CI/CD on 3 platforms |

---

## 4. Documentation to Reference

### 4.1 Internal Documentation
**Must read before implementation**:
- [ ] `CLAUDE.md` - Global development rules
- [ ] `README.md` - Project overview
- [ ] Existing implementation: `src/tools/obsidian_folder_manager/`
- [ ] Existing tests: `tests/tools/obsidian_folder_manager/`

### 4.2 External Resources
**Reference materials**:
- [ ] [Link to design doc]
- [ ] [Link to API spec]
- [ ] [Link to related feature]

**Example**:
- [ ] Anthropic tool calling best practices
- [ ] Obsidian wikilink format specification
- [ ] pathlib cross-platform documentation

### 4.3 Code to Review
**Key files to understand**:
- [ ] `src/shared/vault_security.py` - Path validation utilities
- [ ] `src/shared/obsidian_parsers.py` - Wikilink extraction
- [ ] `src/shared/logging.py` - Structured logging
- [ ] `src/agent/agent.py` - Tool registration patterns

---

## 5. Task Breakdown

### 5.1 High-Level Phases

```
Phase 1: Planning & Design       [X days]
Phase 2: Tool Separation         [Y days]
Phase 3: Archive Implementation  [Z days]
Phase 4: Testing & Validation    [W days]
Phase 5: Documentation & Review  [V days]
```

### 5.2 Detailed Task List

#### Phase 1: Planning & Design (Est: 0.5 days)
- [ ] **PLAN-1**: Review existing implementation
  - Read `src/tools/obsidian_folder_manager/` files
  - Understand current architecture
  - Document gaps
  - **DoD**: Gap analysis document created

- [ ] **PLAN-2**: Design tool separation strategy
  - Document 6-layer separation approach
  - Design path validation logic
  - Design system prompt enhancements
  - **DoD**: Separation strategy approved

- [ ] **PLAN-3**: Design archive operation
  - Define archive path format
  - Design wikilink update logic
  - Define error cases
  - **DoD**: Archive operation spec written

#### Phase 2: Tool Separation (Est: 2 days)
- [ ] **SEP-1**: Add path validation (1 hour)
  - Implement `validate_folder_path()` function
  - Add to `manage_folder_service()`
  - **DoD**: Path validation rejects .md files with helpful error
  - **File**: `src/tools/obsidian_folder_manager/service.py`

- [ ] **SEP-2**: Enhance tool docstring (2 hours)
  - Add "Do NOT use" section
  - Add realistic examples
  - Add performance notes
  - **DoD**: Docstring includes all 7 required sections per CLAUDE.md
  - **File**: `src/tools/obsidian_folder_manager/tool.py`

- [ ] **SEP-3**: Update system prompt (1 hour)
  - Add tool selection decision tree
  - Add tool categories
  - **DoD**: System prompt includes clear differentiation
  - **File**: `src/shared/config.py`

- [ ] **SEP-4**: Add separation tests (2 hours)
  - Test path validation rejections
  - Test error message guidance
  - **DoD**: 3+ tests verify separation behavior
  - **File**: `tests/tools/obsidian_folder_manager/test_service.py`

- [ ] **SEP-5**: Run linters (15 min)
  - Run `ruff check` and `mypy`
  - Fix any errors
  - **DoD**: 0 linting errors

#### Phase 3: Archive Implementation (Est: 1.5 days)
- [ ] **ARCH-1**: Update schemas (30 min)
  - Add `ARCHIVE` to `FolderOperation` enum
  - Add `archive_base` and `date_format` fields
  - **DoD**: Schema validation passes
  - **File**: `src/tools/obsidian_folder_manager/schemas.py`

- [ ] **ARCH-2**: Implement archive service (3 hours)
  - Implement `_archive_folder()` function
  - Add to `manage_folder_service()` switch
  - Handle date formatting
  - Handle wikilink updates
  - **DoD**: Archive operation functional
  - **File**: `src/tools/obsidian_folder_manager/service.py`

- [ ] **ARCH-3**: Update tool registration (1 hour)
  - Add archive parameters to function signature
  - Update request creation
  - Update response formatting
  - **DoD**: Archive callable from agent
  - **File**: `src/tools/obsidian_folder_manager/tool.py`

- [ ] **ARCH-4**: Add archive tests (3 hours)
  - Test simple archive
  - Test wikilink updates
  - Test custom base/format
  - Test dry-run
  - Test error cases
  - **DoD**: 7+ archive tests passing
  - **File**: `tests/tools/obsidian_folder_manager/test_service.py`

- [ ] **ARCH-5**: Run linters (15 min)
  - Run `ruff check` and `mypy`
  - Fix any errors
  - **DoD**: 0 linting errors

#### Phase 4: Testing & Validation (Est: 1.5 days)
- [ ] **TEST-1**: Set up cross-platform CI/CD (2 hours)
  - Create GitHub Actions workflow
  - Configure matrix: ubuntu, macos, windows
  - Configure Python 3.11, 3.12
  - **DoD**: CI/CD runs on push to branch
  - **File**: `.github/workflows/test.yml`

- [ ] **TEST-2**: Run tests locally (1 hour)
  - Run full test suite
  - Check coverage report
  - **DoD**: All tests pass, >90% coverage

- [ ] **TEST-3**: Fix cross-platform issues (4 hours)
  - Review CI/CD failures
  - Fix platform-specific bugs
  - **DoD**: All tests pass on 3 platforms

- [ ] **TEST-4**: Performance benchmarks (2 hours)
  - Benchmark all operations
  - Test with 1000-note vault
  - **DoD**: All performance targets met

- [ ] **TEST-5**: LLM evaluation tests (2 hours)
  - Create 50 ambiguous test prompts
  - Run through agent
  - Measure tool selection accuracy
  - **DoD**: >95% accuracy on tool selection

#### Phase 5: Documentation & Review (Est: 0.5 days)
- [ ] **DOC-1**: Update README (1 hour)
  - Add archive operation examples
  - Update tool description
  - **DoD**: README includes archive usage
  - **File**: `README.md`

- [ ] **DOC-2**: Add inline documentation (1 hour)
  - Review all new code for docstrings
  - Add missing type annotations
  - **DoD**: 100% of functions have docstrings

- [ ] **DOC-3**: Create migration guide (30 min)
  - Document any breaking changes
  - Document new parameters
  - **DoD**: Migration guide complete (if needed)

- [ ] **DOC-4**: Code review (2 hours)
  - Self-review all changes
  - Check adherence to CLAUDE.md
  - **DoD**: All code follows standards

### 5.3 Dependencies & Blockers
**Dependencies**:
- [ ] None (all dependencies already in project)

**Potential Blockers**:
- Cross-platform testing may reveal OS-specific bugs
- Wikilink update performance on large vaults

---

## 6. Validation Strategy

### 6.1 Testing Approach

**Test Pyramid**:
```
        [E2E Tests]           5 tests
           /   \
     [Integration]          10 tests
        /       \
    [Unit Tests]           35+ tests
```

**Test Categories**:
1. **Unit Tests** (35+ tests)
   - Path validation (3 tests)
   - Archive operation (7 tests)
   - Each CRUD operation (5 tests each)
   - Security validation (3 tests)

2. **Integration Tests** (10 tests)
   - Multi-step workflows
   - Wikilink updates across vault
   - Error recovery

3. **Cross-Platform Tests** (8 tests)
   - Windows reserved names
   - Unicode folder names
   - Path normalization
   - Case-only renames

4. **Evaluation Tests** (50 tests)
   - LLM tool selection accuracy
   - Ambiguous prompt handling

### 6.2 Quality Gates

**Before Merge**:
- [ ] All tests pass on Linux, macOS, Windows
- [ ] Test coverage >90% on service layer
- [ ] 0 mypy errors (strict mode)
- [ ] 0 ruff linting errors
- [ ] LLM tool selection accuracy >95%
- [ ] Performance benchmarks meet targets
- [ ] Code review approved
- [ ] Documentation updated

**Automated Checks** (CI/CD):
- [ ] Linting (ruff, mypy)
- [ ] Unit tests
- [ ] Integration tests
- [ ] Cross-platform tests
- [ ] Coverage report

### 6.3 Manual Validation

**Test Scenarios**:
1. Archive old project folder
   - Verify wikilinks updated
   - Verify archive path format
   - Check dry-run mode

2. Try to use folder_manage with .md file
   - Verify helpful error message
   - Verify guidance to correct tool

3. Create nested folder structure
   - Verify parent creation works
   - Verify Windows reserved names rejected

4. List folders with pagination
   - Verify pagination works
   - Verify stats included

---

## 7. Desired Codebase Structure

### 7.1 File Structure (End State)

```
src/tools/obsidian_folder_manager/
├── __init__.py
├── tool.py                    # MODIFIED: Enhanced docstring, archive params
├── schemas.py                 # MODIFIED: Add ARCHIVE enum, archive fields
├── service.py                 # MODIFIED: Add validate_folder_path(), _archive_folder()

tests/tools/obsidian_folder_manager/
├── __init__.py
├── test_service.py            # MODIFIED: Add archive tests, path validation tests

src/shared/
├── config.py                  # MODIFIED: Add tool selection decision tree

.github/workflows/
├── test.yml                   # NEW: Cross-platform CI/CD

README.md                      # MODIFIED: Add archive examples
```

### 7.2 Code Organization Principles

**Per CLAUDE.md**:
- ✅ Vertical slice architecture maintained
- ✅ Each tool in `src/tools/<name>/` with tool.py, schemas.py, service.py
- ✅ Shared utilities in `src/shared/`
- ✅ Tests mirror source structure
- ✅ Type safety enforced (mypy strict)

### 7.3 Interfaces & Contracts

**Public API** (tool.py):
```python
async def obsidian_folder_manage(
    ctx: RunContext["AgentDependencies"],
    path: str,                    # Required
    operation: str,               # Required: "create"|"rename"|"move"|"delete"|"list"|"archive"
    new_name: str | None = None,  # For RENAME
    destination: str | None = None,  # For MOVE
    archive_base: str = "archive",   # NEW: For ARCHIVE
    date_format: str = "%Y-%m-%d",   # NEW: For ARCHIVE
    # ... other params
) -> str:
```

**Service Layer** (service.py):
```python
async def manage_folder_service(
    request: ManageFolderRequest,
    vault_path: str,
    max_folder_depth: int,
    max_wikilink_scan_notes: int,
) -> FolderOperationResult:
```

---

## 8. Risk Assessment & Mitigation

### 8.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Wikilink updates break vault | High | Low | Extensive tests, dry-run mode, backup recommendation |
| Cross-platform path issues | Medium | Medium | CI/CD on 3 platforms, pathlib usage, comprehensive tests |
| Performance issues on large vaults | Medium | Medium | Benchmarks, pagination, max_results limits |
| LLM still confuses tools | High | Medium | Strong negative guidance, evaluation tests, iteration |

### 8.2 Rollback Plan

**If critical issues found**:
1. Revert changes to `tool.py`, `schemas.py`, `service.py`
2. Remove `ARCHIVE` enum value
3. Restore original docstrings
4. Roll back version in `pyproject.toml`

**Rollback trigger conditions**:
- Test pass rate <95% on any platform
- LLM tool selection accuracy <80%
- Critical bug found in production

### 8.3 Migration Considerations

**Breaking Changes**: None
- Archive operation is additive
- All existing operations unchanged
- Backward compatible

**Deprecations**: None

---

## 9. Additional Considerations

### 9.1 Security Considerations
- [ ] Path traversal attacks blocked via `validate_vault_path()`
- [ ] Critical folders protected (`.obsidian`, `.git`, `.trash`)
- [ ] Windows reserved names rejected on all platforms
- [ ] No sensitive data in logs (no API keys, vault contents)
- [ ] Error messages don't leak file system structure

### 9.2 Accessibility & Usability
- [ ] Error messages clear and actionable (what/why/how)
- [ ] Help text includes examples with real paths
- [ ] Token-efficient responses (3-tier system)
- [ ] Dry-run mode for all destructive operations

### 9.3 Observability & Debugging
- [ ] Structured logging for all operations
- [ ] Performance metrics (duration_ms)
- [ ] Correlation IDs for request tracing
- [ ] Clear error messages with context

### 9.4 Future Extensibility
**Potential Future Features** (not in this plan):
- Batch folder operations
- Folder templates/scaffolding
- Folder metadata (.folder-meta.json)
- Folder monitoring & analytics

**Design Considerations for Future**:
- Keep operation enum extensible
- Keep service layer modular
- Document extension points

---

## 10. Approval & Sign-off

### 10.1 Reviewers
- [ ] Technical Lead: [Name]
- [ ] Product Owner: [Name]
- [ ] Security Review: [Name]

### 10.2 Approval Checklist
- [ ] Goal and success criteria clear and measurable
- [ ] User stories include acceptance criteria
- [ ] Task breakdown detailed and estimated
- [ ] Risks identified with mitigation plans
- [ ] Testing strategy comprehensive
- [ ] Documentation plan complete
- [ ] Rollback plan defined

### 10.3 Final Approval
- **Approved by**: [Name]
- **Date**: [Date]
- **Next Steps**: Begin Phase 1 implementation

---

## Appendix

### A. Glossary
- **Wikilink**: Obsidian's internal link format `[[note-name]]`
- **Vault**: Obsidian's term for a folder of markdown files
- **Vertical Slice**: Architecture where each feature includes all layers (UI, service, data)

### B. References
- [CLAUDE.md](/home/user/Obsidian_Agent/CLAUDE.md) - Development standards
- [README.md](/home/user/Obsidian_Agent/README.md) - Project overview

### C. Change Log
| Date | Author | Changes |
|------|--------|---------|
| [Date] | [Name] | Initial draft |
