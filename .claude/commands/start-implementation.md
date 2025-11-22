---
description: Start implementing the folder management enhancement following TDD approach
---

# Implementation Sequence: Start Development

You are guiding the user through implementing the folder management enhancement feature following a test-driven development approach.

## Overview

This is the **Implementation Sequence** from PLANNING.md - designed to guide step-by-step implementation following TDD principles.

**Total Time**: 2-3 weeks of development
**Goal**: Implement all components with 70 tests passing, ready for deployment

## Primary Guide

Your PRIMARY reference is:
📘 **COMPLETE-COMPONENT-TESTING-CHECKLIST.md**

This document contains:
- Section 1: Component Coverage Matrix (19 components)
- Section 2: Complete Test Writing Plan (70 tests with code skeletons)
- Section 3: Complete Validation Commands
- Section 4: Ensuring All Tests Pass (12-step checklist)

## Initial Setup (5 minutes)

### Step 1: Read the Primary Guide

1. Open `/home/user/Obsidian_Agent/COMPLETE-COMPONENT-TESTING-CHECKLIST.md`
2. Review Section 1: Component Coverage Matrix
   - Understand all 19 components to be implemented
   - Note: 4 Models, 5 Services, 4 Tools, 2 APIs, 4 Integrations
3. Review Section 2: Complete Test Writing Plan
   - 50 new tests + 20 existing = 70 total tests
   - 9 test files to create/update

### Step 2: Understand Success Criteria

Open `/home/user/Obsidian_Agent/FOLDER-MANAGEMENT-ENHANCEMENT-PLAN.md` Section 3:

**Success Criteria**:
- ✅ Tool selection accuracy: >95% (from ~80%)
- ✅ Archive success rate: >99%
- ✅ Test coverage: >90%
- ✅ Type safety: 0 `Any` types
- ✅ P95 latency: <200ms

### Step 3: Verify Development Environment

Run pre-implementation validation:

```bash
# Verify environment
uv sync --frozen

# Verify linting and type checking tools work
uv run ruff --version
uv run mypy --version
uv run pytest --version

# Verify existing tests pass
uv run pytest tests/tools/obsidian_folder_manager/test_service.py -v
```

Expected: 20/20 existing tests pass

## Implementation Workflow (Component-by-Component)

Follow this workflow for EACH component:

### Workflow Steps:

```
1. Read component from COMPLETE-COMPONENT-TESTING-CHECKLIST.md Section 1
   ↓
2. Write test from Section 2 (use code skeleton provided)
   ↓
3. Run test (expect FAIL - TDD approach)
   ↓
4. Implement component to make test pass
   ↓
5. Run validation command from Section 3
   ↓
6. Mark component complete when all tests pass
   ↓
7. Commit changes with descriptive message
   ↓
8. Repeat for next component
```

## Phase 1: Schema Changes (Estimate: 2 hours)

### Component 1.1: FolderOperation Enum

**From COMPLETE-COMPONENT-TESTING-CHECKLIST.md Section 2:**

1. **Write Test First** (TDD):
   - Create `tests/tools/obsidian_folder_manager/test_schemas.py`
   - Copy test skeleton from Section 2:
     ```python
     def test_folder_operation_enum_has_archive():
         """Test that ARCHIVE operation exists in enum."""
         assert hasattr(FolderOperation, 'ARCHIVE')
         assert FolderOperation.ARCHIVE == "archive"
     ```

2. **Run Test** (expect FAIL):
   ```bash
   uv run pytest tests/tools/obsidian_folder_manager/test_schemas.py::test_folder_operation_enum_has_archive -v
   ```

3. **Implement**:
   - Open `src/tools/obsidian_folder_manager/schemas.py`
   - Add ARCHIVE to FolderOperation enum

4. **Run Test** (expect PASS):
   ```bash
   uv run pytest tests/tools/obsidian_folder_manager/test_schemas.py::test_folder_operation_enum_has_archive -v
   ```

5. **Validate**:
   ```bash
   uv run mypy src/tools/obsidian_folder_manager/schemas.py --strict
   ```

6. **Commit**:
   ```bash
   git add src/tools/obsidian_folder_manager/schemas.py tests/tools/obsidian_folder_manager/test_schemas.py
   git commit -m "Add ARCHIVE enum to FolderOperation with test"
   ```

### Component 1.2: ManageFolderRequest Schema

Repeat the same workflow:
1. Write test from Section 2 skeleton
2. Run test (FAIL)
3. Implement
4. Run test (PASS)
5. Validate
6. Commit

**Continue this pattern for all components...**

## Phase Completion Validation

After completing each phase, run phase validation from Section 3:

### After Schema Changes (Phase 1):
```bash
uv run mypy src/tools/obsidian_folder_manager/schemas.py --strict
uv run pytest tests/tools/obsidian_folder_manager/test_schemas.py -v
```
Expected: All 5 schema tests pass

### After Service Changes (Phase 2):
```bash
uv run mypy src/tools/obsidian_folder_manager/service.py --strict
uv run ruff check src/tools/obsidian_folder_manager/service.py
uv run pytest tests/tools/obsidian_folder_manager/test_service.py -v
```
Expected: All 33 tests pass (20 existing + 13 new)

### Continue for all phases...

## Implementation Phases Overview

From COMPLETE-COMPONENT-TESTING-CHECKLIST.md Section 5:

**Week 1: Core Implementation**
- ☐ Phase 1: Schema Changes (5 tests) - Day 1
- ☐ Phase 2: Service Implementation (13 tests) - Days 2-3
- ☐ Phase 3: Tool Integration (4 tests) - Day 4
- ☐ Phase 4: Error Handling (8 tests) - Day 5

**Week 2: Advanced Features**
- ☐ Phase 5: Wikilink Updates (6 tests) - Days 1-2
- ☐ Phase 6: Cross-Component (10 tests) - Days 3-4
- ☐ Phase 7: Security & Workflows (8 tests) - Day 5

**Week 3: Polish & Validation**
- ☐ Code review and refinement - Days 1-2
- ☐ Performance optimization - Day 3
- ☐ Documentation updates - Day 4
- ☐ Final pre-deployment validation - Day 5

## Reference Documents (Keep Open)

While implementing, keep these documents available for reference:

1. **COMPLETE-COMPONENT-TESTING-CHECKLIST.md** (PRIMARY)
   - Component list, test code, validation commands

2. **PRE-DEPLOYMENT-VALIDATION-SUMMARY.md** (REFERENCE)
   - Quick command reference for validation

3. **TESTING-AND-VALIDATION-STRATEGY.md** (REFERENCE)
   - Detailed test specifications when needed

4. **FOLDER-MANAGEMENT-ENHANCEMENT-PLAN.md** (REFERENCE)
   - Section 6: Tasks with Definition of Done
   - Section 5: Proposed Solution details

## Progress Tracking

Use the checklist from COMPLETE-COMPONENT-TESTING-CHECKLIST.md Section 6:

```
☐ Phase 1: Schema Changes (5 tests)
☐ Phase 2: Service Implementation (13 tests)
☐ Phase 3: Tool Integration (4 tests)
☐ Phase 4: Error Handling (8 tests)
☐ Phase 5: Wikilink Updates (6 tests)
☐ Phase 6: Cross-Component (10 tests)
☐ Phase 7: Security & Workflows (8 tests)
```

After each phase, mark it complete and run validation.

## Troubleshooting

If you encounter errors, refer to COMPLETE-COMPONENT-TESTING-CHECKLIST.md Section 4:

**Common Errors & Fixes**:
| Error | Likely Cause | Fix |
|-------|--------------|-----|
| ModuleNotFoundError | Missing import | Add import statement |
| TypeError | Function signature changed | Update call signature |
| AssertionError | Test logic incorrect | Review expectations |
| MyPy error | Type annotation missing | Add type hints |

## When Implementation is Complete

Run the complete validation from Section 4 (12-step checklist):

```bash
☐ Step 1: uv sync --frozen
☐ Step 2: pytest test_schemas.py -v (5/5)
☐ Step 3: pytest test_service.py -v (33/33)
☐ Step 4: pytest test_error_handling.py -v (8/8)
☐ Step 5: pytest test_wikilink_updates.py -v (6/6)
☐ Step 6: pytest tests/integration/ -v (10/10)
☐ Step 7: pytest tests/e2e/ -v (2/2)
☐ Step 8: pytest tests/security/ -v (6/6)
☐ Step 9: pytest tests/ -v --tb=short (70/70)
☐ Step 10: pytest --cov --cov-fail-under=90 (>90%)
☐ Step 11: mypy --strict (0 errors)
☐ Step 12: ruff check (0 errors)
```

**Success Criteria**: 70/70 tests pass, >90% coverage, 0 type errors, 0 linting errors

## What's Next?

When all implementation is complete and validation passes:

**Run `/pre-deployment`** to execute comprehensive pre-deployment validation before merging to main.

## Tips for Success

1. **Follow TDD**: Write test first, see it fail, implement, see it pass
2. **Commit Often**: Commit after each component (19 commits minimum)
3. **Validate Early**: Run validation commands after each component
4. **Use Code Skeletons**: Section 2 provides exact test code - use it!
5. **Track Progress**: Check off components as you complete them
6. **Ask for Help**: If stuck, refer to detailed specifications in TESTING-AND-VALIDATION-STRATEGY.md

**Ready to start?** Begin with Phase 1, Component 1.1: FolderOperation Enum!
