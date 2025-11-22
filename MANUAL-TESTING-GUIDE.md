# Manual Testing Guide

**Related Documents**:
- Pre-Deployment: `PRE-DEPLOYMENT-VALIDATION-SUMMARY.md`
- Deployment: `DEPLOYMENT-VALIDATION-STRATEGY.md`
- Post-Deployment: `POST-DEPLOYMENT-VALIDATION-STRATEGY.md`
- Full Suite: `TESTING-AND-VALIDATION-STRATEGY.md`

---

## Overview

**Purpose**: Guide for manual testing activities requiring human verification.

**Target Audience**:
- QA Engineers
- Product Owners
- Developers
- **You (as stakeholder/feature requester)**

**When Manual Testing is Required**:
- ✅ Pre-deployment: User acceptance testing (UAT)
- ✅ Deployment: Staging verification
- ✅ Post-deployment: Production verification
- ✅ Edge cases: Automated tests can't cover
- ✅ User experience: Subjective quality checks

---

## Your Involvement as Stakeholder

### What You MUST Do (Required)

#### 1. User Acceptance Testing (UAT) - **30-60 minutes**
**When**: After implementation, before deployment to staging
**Why**: Verify feature meets your requirements

**Your Role**:
- [ ] Test archive operation with your own Obsidian vault
- [ ] Verify tool selection works as expected
- [ ] Check error messages are helpful
- [ ] Confirm feature meets original requirements
- [ ] Sign off on feature for deployment

**Estimated Time**: 30-60 minutes
**Can be delegated**: No - you requested feature, must approve

---

#### 2. Staging Approval - **15 minutes**
**When**: After deployment to staging, before production
**Why**: Final check before production release

**Your Role**:
- [ ] Test feature in staging environment
- [ ] Confirm no critical bugs
- [ ] Approve for production deployment

**Estimated Time**: 15 minutes
**Can be delegated**: Yes, to trusted team member

---

#### 3. Production Smoke Test - **10 minutes**
**When**: Day 1 after production deployment
**Why**: Verify feature works in production

**Your Role**:
- [ ] Create a test folder in your production vault
- [ ] Archive the folder
- [ ] Verify folder moved correctly
- [ ] Verify wikilinks still work

**Estimated Time**: 10 minutes
**Can be delegated**: Yes, but recommended you do it

---

### What You SHOULD Do (Recommended)

#### 4. Weekly Check-ins - **10 minutes/week for 4 weeks**
**When**: Weeks 1-4 after deployment
**Why**: Monitor feature quality and adoption

**Your Role**:
- [ ] Review metrics dashboard
- [ ] Check for any user complaints
- [ ] Verify feature working as expected
- [ ] Provide feedback on any issues

**Estimated Time**: 10 minutes/week
**Can be delegated**: Yes

---

### What You DON'T Need to Do (Automated)

- ❌ Unit testing (135+ automated tests)
- ❌ Integration testing (automated)
- ❌ Security testing (automated)
- ❌ Performance testing (automated)
- ❌ Cross-platform testing (CI/CD)
- ❌ Continuous monitoring (automated alerts)

---

## Manual Testing Scenarios

### Scenario 1: User Acceptance Testing (UAT)

**Duration**: 30-60 minutes
**Prerequisites**:
- Obsidian vault with test data
- Access to staging environment or local build
- Test account credentials

---

#### UAT Test 1: Basic Archive Operation
**Purpose**: Verify archive operation works correctly

**Steps**:
1. Open your Obsidian vault
2. Create a test folder: "test-archive-folder"
3. Add 3 test notes to the folder:
   - `overview.md` - "This is an overview"
   - `details.md` - "These are details"
   - `notes.md` - "These are notes"
4. Use agent to archive the folder:
   - Say: "Archive the test-archive-folder"
5. Verify results:
   - Folder moved to `archive/2025-01-22/test-archive-folder/` (today's date)
   - All 3 notes present in archive
   - Notes content unchanged
   - Agent confirms successful archive

**Expected Behavior**:
- ✅ Agent uses `obsidian_folder_manage` tool
- ✅ Agent responds: "Successfully archived test-archive-folder to archive/2025-01-22/test-archive-folder"
- ✅ Folder no longer in original location
- ✅ Folder present in archive location
- ✅ All notes intact

**Pass/Fail**: ☐ Pass ☐ Fail

**If Fail, describe issue**:
```
[Your description here]
```

---

#### UAT Test 2: Wikilink Updates
**Purpose**: Verify wikilinks are updated after archive

**Steps**:
1. Create test folder: "project-alpha"
2. Add note in folder: `project-alpha/overview.md` with content:
   ```markdown
   # Project Alpha Overview
   This is the main project.
   ```
3. Create note outside folder: `index.md` with content:
   ```markdown
   # Index
   See [[project-alpha/overview]] for project info.
   ```
4. Archive the folder:
   - Say: "Archive the project-alpha folder"
5. Open `index.md` and verify wikilink:
   - Should now be: `[[archive/2025-01-22/project-alpha/overview]]`
6. Click the wikilink - should work without errors

**Expected Behavior**:
- ✅ Wikilink automatically updated
- ✅ Link still works after update
- ✅ Agent reports: "Wikilinks updated: 1 note"

**Pass/Fail**: ☐ Pass ☐ Fail

**If Fail, describe issue**:
```
[Your description here]
```

---

#### UAT Test 3: Tool Selection Accuracy
**Purpose**: Verify agent selects correct tool

**Steps**:
1. Test folder operations:
   - Say: "Create a new folder called test-projects"
   - Expected: Agent uses `obsidian_folder_manage`

2. Test note operations:
   - Say: "Create a new note called meeting-notes.md"
   - Expected: Agent uses `obsidian_note_manage` (NOT folder_manage)

3. Test ambiguous request:
   - Say: "Create something called test"
   - Expected: Agent asks for clarification OR defaults to folder (no extension)

4. Test archive specifically:
   - Say: "Archive my old drafts"
   - Expected: Agent uses `obsidian_folder_manage` with `operation=archive`

**Expected Behavior**:
- ✅ Agent never confuses folder_manage with note_manage
- ✅ Agent selects correct tool based on request
- ✅ Agent asks for clarification when ambiguous

**Pass/Fail**: ☐ Pass ☐ Fail

**If Fail, describe issue**:
```
[Your description here]
```

---

#### UAT Test 4: Error Messages
**Purpose**: Verify error messages are helpful

**Steps**:
1. Try to archive a non-existent folder:
   - Say: "Archive the non-existent-folder"
   - Expected: Clear error "Folder not found: non-existent-folder"

2. Try to archive a note file:
   - Say: "Archive the test-note.md file"
   - Expected: Error says "operates on FOLDERS only" and suggests `obsidian_note_manage`

3. Try to archive to existing archive location (create duplicate first):
   - Create folder: "duplicate-test"
   - Archive it once
   - Recreate folder: "duplicate-test"
   - Try to archive again
   - Expected: Error says "Archive destination already exists" with 3 resolution options

**Expected Behavior**:
- ✅ All error messages clear and helpful
- ✅ Errors suggest correct action
- ✅ Errors include examples when relevant

**Pass/Fail**: ☐ Pass ☐ Fail

**If Fail, describe issue**:
```
[Your description here]
```

---

#### UAT Test 5: Custom Archive Options
**Purpose**: Verify archive operation supports customization

**Steps**:
1. Test custom archive base:
   - Say: "Archive old-drafts to 'archived-drafts' folder"
   - Expected: Folder moved to `archived-drafts/2025-01-22/old-drafts/`

2. Test dry-run mode (if accessible):
   - Say: "Show me where test-folder would be archived without actually moving it"
   - Expected: Agent shows archive destination but doesn't move folder
   - Verify folder still in original location

**Expected Behavior**:
- ✅ Custom archive base works
- ✅ Dry-run mode shows destination without moving (if supported via chat)

**Pass/Fail**: ☐ Pass ☐ Fail

**If Fail, describe issue**:
```
[Your description here]
```

---

### UAT Sign-Off

**Tester Name**: ______________________

**Date**: ______________________

**Overall Assessment**:
☐ **APPROVED** - Feature meets requirements, ready for deployment
☐ **APPROVED WITH MINOR ISSUES** - Can deploy, but issues noted below
☐ **NOT APPROVED** - Critical issues must be fixed before deployment

**Issues Found** (if any):
```
1. [Issue description]
2. [Issue description]
3. [Issue description]
```

**Comments**:
```
[Any additional feedback]
```

**Signature**: ______________________

---

## Scenario 2: Staging Verification

**Duration**: 15 minutes
**When**: After deployment to staging
**Who**: You or designated tester

### Staging Test Checklist

**Environment**: Staging (https://staging.example.com)

#### Test 1: Basic Functionality
- [ ] Log into staging environment
- [ ] Create test folder: "staging-test-$(date)"
- [ ] Archive the folder
- [ ] Verify folder moved to archive/
- [ ] Verify agent response correct

**Pass/Fail**: ☐ Pass ☐ Fail

---

#### Test 2: Performance Check
- [ ] Archive operation completes <2 seconds
- [ ] No noticeable lag or delays
- [ ] Agent responsive

**Pass/Fail**: ☐ Pass ☐ Fail

---

#### Test 3: Integration Check
- [ ] Other features still work (note creation, vault query, etc.)
- [ ] No regressions in existing functionality

**Pass/Fail**: ☐ Pass ☐ Fail

---

### Staging Sign-Off

**Result**: ☐ Approved for production ☐ Not approved (issues below)

**Issues**:
```
[Describe any issues]
```

**Signature**: ______________________ **Date**: ______________

---

## Scenario 3: Production Smoke Test (Day 1)

**Duration**: 10 minutes
**When**: Day 1 after production deployment
**Who**: You (recommended) or on-call engineer

### Production Smoke Test Steps

**⚠️ IMPORTANT**: Use a test vault, not your main production vault

1. **Health Check**
   - [ ] Navigate to https://app.example.com
   - [ ] Verify service is up and running
   - [ ] No error messages on dashboard

2. **Create Test Folder**
   - [ ] Create folder: "smoke-test-YYYYMMDD"
   - [ ] Add 1 test note to folder
   - [ ] Verify folder exists

3. **Archive Test Folder**
   - [ ] Ask agent: "Archive smoke-test-YYYYMMDD folder"
   - [ ] Verify agent uses correct tool
   - [ ] Verify folder moved to archive/
   - [ ] Verify agent reports success

4. **Verify No Regressions**
   - [ ] Create a note (test note_manage still works)
   - [ ] List folders (test list operation works)
   - [ ] Verify your existing folders unchanged

5. **Check Logs** (if accessible)
   - [ ] Open logging dashboard
   - [ ] Search for your archive operation
   - [ ] Verify no errors logged

---

### Production Smoke Test Result

**Result**: ☐ Success ☐ Failure (alert team immediately)

**If Failure**:
- [ ] Screenshot error
- [ ] Copy error message
- [ ] Note timestamp
- [ ] Alert on-call engineer: `@oncall Production smoke test failed`

---

## Scenario 4: Edge Case Testing (Optional)

**Duration**: 30 minutes
**When**: After UAT, if time permits
**Who**: QA engineer or you (optional)

### Edge Case Test 1: Large Folder
**Purpose**: Test with many files

**Steps**:
1. Create folder with 50+ notes
2. Add wikilinks to some notes
3. Archive the folder
4. Verify all notes moved
5. Verify wikilinks updated
6. Check performance (<1 minute for 50 notes)

**Pass/Fail**: ☐ Pass ☐ Fail

---

### Edge Case Test 2: Deep Nesting
**Purpose**: Test with nested folders

**Steps**:
1. Create structure: `projects/2025/q1/alpha/docs/`
2. Add notes at each level
3. Archive top-level: `projects`
4. Verify entire structure moved
5. Verify all notes present

**Pass/Fail**: ☐ Pass ☐ Fail

---

### Edge Case Test 3: Special Characters
**Purpose**: Test with special characters in names

**Steps**:
1. Create folders with names:
   - `test-folder` (hyphen)
   - `test_folder` (underscore)
   - `test folder` (space)
   - `test(folder)` (parentheses)
   - `项目` (unicode/Chinese)
2. Archive each
3. Verify all work correctly

**Pass/Fail**: ☐ Pass ☐ Fail

---

### Edge Case Test 4: Windows Reserved Names
**Purpose**: Test validation of reserved names

**Steps**:
1. Try to create folder named "CON"
2. Expected: Rejected with error
3. Try: "PRN", "AUX", "NUL"
4. All should be rejected

**Pass/Fail**: ☐ Pass ☐ Fail

---

## Scenario 5: Usability Testing

**Duration**: 15 minutes
**When**: During UAT
**Who**: You or representative user

### Usability Checklist

#### Discoverability
- [ ] Is it obvious how to use archive feature?
- [ ] Can you find documentation easily?
- [ ] Are error messages clear without documentation?

#### Learnability
- [ ] Can you use archive feature without training?
- [ ] Are defaults sensible?
- [ ] Do you understand what the feature does?

#### Efficiency
- [ ] Is archive faster than manual approach?
- [ ] Are there unnecessary steps?
- [ ] Can common tasks be done quickly?

#### Satisfaction
- [ ] Does feature feel polished?
- [ ] Are you confident using it?
- [ ] Would you recommend it to others?

**Overall Usability Score**: ☐ Excellent ☐ Good ☐ Acceptable ☐ Poor

**Improvement Suggestions**:
```
[Your suggestions]
```

---

## Manual Testing Schedule

### Pre-Deployment Phase
| Test | Who | Duration | When | Mandatory |
|------|-----|----------|------|-----------|
| UAT Test 1-5 | **You** | 30-60 min | After implementation | ✅ Yes |
| Edge Case Testing | QA (optional) | 30 min | After UAT | ❌ No |
| Usability Testing | **You** | 15 min | During UAT | ✅ Yes |

**Total Your Time**: 45-75 minutes

---

### Deployment Phase
| Test | Who | Duration | When | Mandatory |
|------|-----|----------|------|-----------|
| Staging Verification | **You or delegate** | 15 min | After staging deploy | ✅ Yes |
| Production Smoke Test | **You (recommended)** | 10 min | Day 1 production | ✅ Yes |

**Total Your Time**: 25 minutes

---

### Post-Deployment Phase
| Test | Who | Duration | When | Mandatory |
|------|-----|----------|------|-----------|
| Weekly Check-in | **You or delegate** | 10 min | Weeks 1-4 | ⚠️ Recommended |
| Monthly Review | Product Owner | 30 min | End of month | ❌ No (attend if possible) |

**Total Your Time**: 40 minutes (if you do all 4 weekly check-ins)

---

## Total Time Commitment

### Minimum (Must Do)
- UAT: 30 minutes
- Staging: 15 minutes
- Production Day 1: 10 minutes
**Total Minimum**: **55 minutes**

### Recommended (Should Do)
- UAT (thorough): 60 minutes
- Staging: 15 minutes
- Production Day 1: 10 minutes
- Weekly check-ins (4 weeks): 40 minutes
**Total Recommended**: **125 minutes (~2 hours)**

### Optional (Extra Diligence)
- Edge case testing: 30 minutes
- Monthly review attendance: 30 minutes
**Total Optional**: +60 minutes

---

## Testing Tools & Resources

### Tools You'll Need
- ✅ Access to Obsidian vault (test data)
- ✅ Access to staging environment (credentials)
- ✅ Access to production environment (credentials)
- ⚠️ Optional: Access to logging dashboard (for verification)
- ⚠️ Optional: Access to metrics dashboard (for monitoring)

### Test Data
**Provided**:
- Sample vault structure
- Test folders and notes
- Wikilink examples

**Location**: `/test-data/manual-testing/`

---

## Reporting Issues

### During UAT (Pre-Deployment)
**How to Report**:
1. Fill out UAT sign-off form (above)
2. Mark as "NOT APPROVED" if critical
3. List issues in detail
4. Send to development team

**Severity Levels**:
- 🔥 **Critical**: Feature completely broken, blocks deployment
- ⚠️ **High**: Major functionality issue, should fix before deployment
- ℹ️ **Medium**: Minor issue, can deploy but should fix soon
- 💡 **Low**: Nice-to-have, can fix later

---

### During Production (Post-Deployment)
**How to Report**:
1. Note timestamp and exact steps
2. Screenshot error if any
3. Copy error message verbatim
4. Report via:
   - Critical issues: Alert on-call engineer immediately
   - Non-critical: Create ticket in issue tracker

---

## FAQ for Manual Testers

**Q: Do I really need to do manual testing if there are 135+ automated tests?**

A: Yes, for these reasons:
- Automated tests can't verify **subjective quality** (is the feature useful?)
- Automated tests can't test **real user workflows** with actual data
- Automated tests can't validate **business requirements** (does it do what you asked for?)
- Your sign-off means "this is what I wanted"

---

**Q: Can I delegate my manual testing to someone else?**

A: Partially:
- ✅ **Can delegate**: Staging verification, weekly check-ins
- ❌ **Can't delegate**: UAT (you requested feature, must approve)
- ⚠️ **Should do yourself**: Production Day 1 smoke test

---

**Q: What if I find a bug during UAT?**

A: Mark UAT as "NOT APPROVED" and list the bug. Development team will fix and ask you to re-test.

---

**Q: What if I'm too busy for manual testing?**

A: Minimum required is 55 minutes total. If you can't commit this time:
- Delegate staging and weekly check-ins
- You must still do UAT (30 min) and Production Day 1 (10 min) = 40 minutes minimum

---

**Q: What happens if I skip manual testing?**

A: Risks:
- Feature might not meet your actual needs
- Bugs discovered after deployment (costly to fix)
- Feature might be rolled back due to issues
- Your time wasted explaining what's wrong post-deployment

Manual testing takes 1-2 hours. Fixing issues post-deployment takes 10x longer.

---

## Manual Testing Best Practices

### Do's ✅
- ✅ Test with realistic data (your actual vault structure)
- ✅ Test workflows you actually use
- ✅ Read error messages carefully
- ✅ Note both positive and negative feedback
- ✅ Compare to your original requirements
- ✅ Ask questions if unclear

### Don'ts ❌
- ❌ Rush through tests
- ❌ Test with fake/meaningless data
- ❌ Skip tests because "automated tests passed"
- ❌ Approve with known issues (unless documented)
- ❌ Test in production first (always staging first)

---

## Summary: Your Manual Testing Journey

### Step 1: UAT (30-60 minutes) - **REQUIRED**
- Test feature thoroughly
- Verify meets requirements
- Sign off on UAT form

### Step 2: Staging (15 minutes) - **REQUIRED**
- Verify works in staging
- Approve for production

### Step 3: Production Day 1 (10 minutes) - **REQUIRED**
- Smoke test in production
- Verify feature live

### Step 4: Weekly Check-ins (10 min/week × 4) - **RECOMMENDED**
- Monitor feature quality
- Provide feedback

**Total Time Investment**: 55-125 minutes for a major feature

**Return on Investment**: Feature that actually works and meets your needs!

---

**Version**: 1.0
**Last Updated**: 2025-01-22
**Contact**: For questions about manual testing, contact QA lead or development team
