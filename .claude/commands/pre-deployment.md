---
description: Run comprehensive pre-deployment validation before merging to main
---

# Pre-Deployment Validation Sequence

You are guiding the user through comprehensive pre-deployment validation to ensure all quality gates pass before merging to main.

## Overview

This is the **Pre-Deployment Validation Sequence** from PLANNING.md - designed to catch issues before deployment.

**Total Time**: ~2-3 hours
**Goal**: All quality gates pass, code ready to merge and deploy

## Primary Guide

Your PRIMARY reference is:
📘 **PRE-DEPLOYMENT-VALIDATION-SUMMARY.md**

This document contains all 5 validation phases with commands and success criteria.

## Pre-Flight Check

Before starting validation, ensure implementation is complete:

```bash
# Check current branch
git status

# Verify all changes committed
# Expected: "nothing to commit, working tree clean" OR known uncommitted changes
```

**Important**: Implementation should be complete before running pre-deployment validation.

## Validation Phase 1: Dependency Validation (5 minutes)

### 1.1 Verify Dependencies Installed

```bash
uv sync --frozen
```

**Success Criteria**: ✅ All dependencies installed successfully, no errors

### 1.2 Verify Dependency Versions

```bash
uv pip list | grep -E "(ruff|mypy|pytest|pydantic|fastapi)"
```

**Success Criteria**: ✅ Key packages present:
- ruff >= 0.14.0
- mypy >= 1.18.2
- pytest >= 8.4.2
- pydantic >= 2.10.6
- fastapi >= 0.115.6

### 1.3 Security Audit

```bash
uv pip check
```

**Success Criteria**: ✅ No dependency conflicts

### 1.4 Verify Imports

```bash
python -c "from src.tools.obsidian_folder_manager import schemas, service, tool; print('✅ All imports successful')"
```

**Success Criteria**: ✅ All imports work without errors

**Phase 1 Result**: ☐ PASS ☐ FAIL

---

## Validation Phase 2: Linting and Type Checking (5 minutes)

### 2.1 Ruff Linting

```bash
uv run ruff check src/tools/obsidian_folder_manager/ --output-format=github
```

**Success Criteria**: ✅ 0 linting errors

**If FAIL**: Run auto-fix and re-check:
```bash
uv run ruff check --fix src/tools/obsidian_folder_manager/
uv run ruff check src/tools/obsidian_folder_manager/
```

### 2.2 Ruff Formatting

```bash
uv run ruff format --check src/tools/obsidian_folder_manager/
```

**Success Criteria**: ✅ All files formatted correctly

**If FAIL**: Run formatter and re-check:
```bash
uv run ruff format src/tools/obsidian_folder_manager/
uv run ruff format --check src/tools/obsidian_folder_manager/
```

### 2.3 MyPy Strict Type Checking

```bash
uv run mypy src/tools/obsidian_folder_manager/ --strict --show-error-codes
```

**Success Criteria**: ✅ 0 type errors

**Common Type Errors & Fixes**:
- `error: Missing return statement` → Add return statement or `-> None`
- `error: Need type annotation` → Add type hints to variable
- `error: Incompatible return value type` → Fix return type or annotation

### 2.4 Type Coverage

```bash
uv run mypy src/tools/obsidian_folder_manager/ --strict --html-report mypy-report
cat mypy-report/index.html | grep -o "imprecision: [0-9]*"
```

**Success Criteria**: ✅ Type coverage >99% (imprecision <1%)

**Phase 2 Result**: ☐ PASS ☐ FAIL

---

## Validation Phase 3: Unit Tests (30 minutes)

### 3.1 Run All Unit Tests

```bash
uv run pytest tests/tools/obsidian_folder_manager/ -v -m unit \
    --cov=src/tools/obsidian_folder_manager/ \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-fail-under=90
```

**Success Criteria**:
- ✅ All unit tests pass (33/33 expected)
- ✅ Coverage >90%
- ✅ 0 test failures
- ✅ 0 test errors

**Expected Output**:
```
========== 33 passed in X.XXs ==========
Coverage: 92%
```

### 3.2 Review Coverage Report

```bash
# View coverage report
cat htmlcov/index.html | grep "pc_cov"

# Identify uncovered lines
uv run pytest tests/tools/obsidian_folder_manager/ -v \
    --cov=src/tools/obsidian_folder_manager/ \
    --cov-report=term-missing
```

**Success Criteria**: ✅ Coverage >90%, critical paths covered

### 3.3 Test Quality Check

Review test output for:
- ✅ No skipped tests (unless explicitly marked for future implementation)
- ✅ No warnings about deprecated features
- ✅ Test execution time reasonable (<30 seconds total)

**Phase 3 Result**: ☐ PASS ☐ FAIL

---

## Validation Phase 4: Integration Tests (15 minutes)

### 4.1 Run Integration Tests

```bash
uv run pytest tests/integration/ -v -m integration \
    --maxfail=1 \
    --tb=short
```

**Success Criteria**:
- ✅ All integration tests pass (10/10 expected)
- ✅ 0 test failures
- ✅ Tests complete in <2 minutes

### 4.2 Run End-to-End Tests

```bash
uv run pytest tests/e2e/ -v \
    --maxfail=1 \
    --tb=short
```

**Success Criteria**:
- ✅ All E2E tests pass (2/2 expected)
- ✅ Complete user workflows tested
- ✅ Tests complete in <5 minutes

**Phase 4 Result**: ☐ PASS ☐ FAIL

---

## Validation Phase 5: Security Tests (10 minutes)

### 5.1 Security Unit Tests

```bash
uv run pytest tests/security/ -v \
    --tb=short
```

**Success Criteria**:
- ✅ All security tests pass (6/6 expected)
- ✅ Path traversal prevention verified
- ✅ Input validation verified

### 5.2 Static Security Analysis (Bandit)

```bash
uv run bandit -r src/tools/obsidian_folder_manager/ \
    -ll \
    -f json \
    -o bandit-report.json

# View results
uv run bandit -r src/tools/obsidian_folder_manager/ -ll
```

**Success Criteria**:
- ✅ 0 high severity issues
- ✅ 0 medium severity issues
- ✅ Low severity issues reviewed and accepted (if any)

**Phase 5 Result**: ☐ PASS ☐ FAIL

---

## Complete Validation Summary

Run the complete test suite one final time:

```bash
# All tests together
uv run pytest tests/ -v \
    --cov=src/tools/obsidian_folder_manager/ \
    --cov-fail-under=90 \
    --tb=short

# Get final test count
uv run pytest tests/ --collect-only | grep "test session starts"
```

**Expected**: 70/70 tests pass

## 12-Step Final Checklist

From COMPLETE-COMPONENT-TESTING-CHECKLIST.md Section 4:

```bash
☐ Step 1: uv sync --frozen  # Dependencies
☐ Step 2: pytest test_schemas.py -v  # 5/5 pass
☐ Step 3: pytest test_service.py -v  # 33/33 pass
☐ Step 4: pytest test_error_handling.py -v  # 8/8 pass
☐ Step 5: pytest test_wikilink_updates.py -v  # 6/6 pass
☐ Step 6: pytest tests/integration/ -v  # 10/10 pass
☐ Step 7: pytest tests/e2e/ -v  # 2/2 pass
☐ Step 8: pytest tests/security/ -v  # 6/6 pass
☐ Step 9: pytest tests/ -v --tb=short  # 70/70 pass
☐ Step 10: pytest --cov --cov-fail-under=90  # >90% coverage
☐ Step 11: mypy --strict  # 0 errors
☐ Step 12: ruff check  # 0 errors
```

## Quality Gates Summary

All quality gates MUST pass:

### Code Quality Gates
- ✅ Ruff: 0 linting errors
- ✅ MyPy: 0 type errors (strict mode)
- ✅ Type coverage: >99%
- ✅ Code formatting: All files formatted

### Functional Gates
- ✅ Unit tests: 33/33 pass
- ✅ Integration tests: 10/10 pass
- ✅ E2E tests: 2/2 pass
- ✅ Total tests: 70/70 pass (100% pass rate)

### Quality Gates
- ✅ Test coverage: >90%
- ✅ No skipped tests (unless explicitly marked)
- ✅ Test execution time: <5 minutes total

### Security Gates
- ✅ Security tests: 6/6 pass
- ✅ Bandit: 0 high/medium vulnerabilities
- ✅ Path traversal prevention verified

## Results

Record your validation results:

**Phase 1 - Dependency Validation**: ☐ PASS ☐ FAIL
**Phase 2 - Linting & Type Checking**: ☐ PASS ☐ FAIL
**Phase 3 - Unit Tests**: ☐ PASS ☐ FAIL
**Phase 4 - Integration Tests**: ☐ PASS ☐ FAIL
**Phase 5 - Security Tests**: ☐ PASS ☐ FAIL

**Overall Result**: ☐ ALL PASS (Ready to Deploy) ☐ NEEDS WORK

## If All Validation Passes ✅

Congratulations! Your code is ready for deployment.

**Next Steps**:

1. **Commit any final changes**:
   ```bash
   git add .
   git commit -m "Pre-deployment validation complete - all quality gates pass"
   ```

2. **Push to branch**:
   ```bash
   git push -u origin <your-branch-name>
   ```

3. **Ready for deployment** → Run `/deploy` to begin staged deployment process

## If Validation Fails ❌

### Troubleshooting Guide

**Common Issues**:

1. **Linting errors** → Run `ruff check --fix` and review remaining errors
2. **Type errors** → Add type annotations, fix return types
3. **Test failures** → Review test output, fix implementation
4. **Low coverage** → Write additional tests for uncovered lines
5. **Security issues** → Review Bandit output, fix vulnerabilities

### Getting Help

If stuck, refer to:
- **COMPLETE-COMPONENT-TESTING-CHECKLIST.md** Section 4 - Failure handling procedures
- **TESTING-AND-VALIDATION-STRATEGY.md** Section 1 - Detailed pre-deployment validation
- **FOLDER-MANAGEMENT-ENHANCEMENT-PLAN.md** Section 7 - Validation strategy

### Re-run Validation

After fixing issues:
1. Fix the specific issue
2. Re-run the failed validation phase
3. If pass, continue to next phase
4. Repeat until all phases pass

## Detailed Reports

After validation, review detailed reports:

**Coverage Report**: `htmlcov/index.html`
**MyPy Report**: `mypy-report/index.html`
**Bandit Report**: `bandit-report.json`

## Time Summary

| Phase | Estimated Time | Actual Time |
|-------|----------------|-------------|
| Phase 1: Dependencies | 5 min | ___ min |
| Phase 2: Linting & Types | 5 min | ___ min |
| Phase 3: Unit Tests | 30 min | ___ min |
| Phase 4: Integration Tests | 15 min | ___ min |
| Phase 5: Security Tests | 10 min | ___ min |
| **Total** | **65 min (~1 hour)** | **___ min** |

**Good job!** Pre-deployment validation ensures production quality code.
