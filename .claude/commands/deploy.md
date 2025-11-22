---
description: Deploy folder management enhancement through staged rollout
---

# Deployment Sequence: Safe Production Rollout

You are guiding the user through a 4-stage deployment process with validation at each stage.

## Overview

This is the **Deployment Sequence** from PLANNING.md - designed for safe production rollout with incremental validation.

**Total Time**: 3-5 days for full rollout
**Goal**: Feature successfully deployed to 100% production traffic with no incidents

## Primary Guide

Your PRIMARY reference is:
📘 **DEPLOYMENT-VALIDATION-STRATEGY.md**

This document contains the complete 4-stage deployment process with validation, monitoring, and rollback procedures.

## Prerequisites Check

Before starting deployment, verify:

```bash
# Pre-deployment validation passed?
# Run /pre-deployment if not already done

# All tests passing?
uv run pytest tests/ -v --tb=short

# All changes committed?
git status

# On correct branch?
git branch --show-current
```

**Required**: ✅ All pre-deployment validation must pass before deployment

---

## Stage 1: Local/Dev Environment (30 minutes)

### Objective
Verify feature works in local development environment with smoke tests.

### 1.1 Deploy to Local Environment

```bash
# Ensure latest code
git pull origin <your-branch>

# Sync dependencies
uv sync --frozen

# Start local server
uv run uvicorn src.main:app --host 0.0.0.0 --port 8030 --reload
```

**Success Criteria**: ✅ Server starts without errors

### 1.2 Run Local Smoke Tests

Open a new terminal and run:

```bash
# Test 1: Health check
curl http://localhost:8030/health

# Expected: {"status": "healthy"}
```

```bash
# Test 2: Archive operation (new feature)
curl -X POST http://localhost:8030/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "obsidian_folder_manage",
    "parameters": {
      "path": "test-folder",
      "operation": "archive"
    }
  }'

# Expected: Success response with archive path
```

```bash
# Test 3: Folder management operations
curl -X POST http://localhost:8030/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "obsidian_folder_manage",
    "parameters": {
      "path": "test-new-folder",
      "operation": "create"
    }
  }'

# Expected: Success response
```

**Success Criteria**:
- ✅ All 3 smoke tests pass
- ✅ No errors in server logs
- ✅ Archive operation creates correct path structure

### 1.3 Verify Logs

Check server logs for:
- ✅ No error-level logs
- ✅ Structured logging working correctly
- ✅ Archive operations logged with duration_ms

**Stage 1 Result**: ☐ PASS ☐ FAIL

**If FAIL**: Fix issues locally, do not proceed to Stage 2

---

## Stage 2: Staging Environment (1 day)

### Objective
Deploy to staging environment for integration validation and user acceptance testing.

### 2.1 Deploy to Staging

```bash
# Merge to staging branch (or deploy current branch to staging)
git checkout staging
git merge <your-feature-branch>
git push origin staging

# SSH to staging server and deploy
ssh staging-server
cd /app/obsidian-agent
git pull origin staging
uv sync --frozen
sudo systemctl restart obsidian-agent
sudo systemctl status obsidian-agent
```

**Success Criteria**: ✅ Service restarted successfully, status shows "active (running)"

### 2.2 Run Staging Smoke Tests

```bash
# Set staging URL
STAGING_URL="https://staging.example.com"  # Replace with actual staging URL

# Test 1: Health check
curl $STAGING_URL/health

# Test 2: Archive operation
curl -X POST $STAGING_URL/api/agent/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $STAGING_TOKEN" \
  -d '{
    "tool": "obsidian_folder_manage",
    "parameters": {
      "path": "staging-test-folder",
      "operation": "archive"
    }
  }'

# Test 3: Integration validation
# Run full integration test suite against staging
uv run pytest tests/integration/ -v --base-url=$STAGING_URL
```

**Success Criteria**:
- ✅ All smoke tests pass
- ✅ Integration tests pass against staging
- ✅ No errors in staging logs

### 2.3 USER ACTION REQUIRED: Staging Verification (15 minutes)

**📋 MANUAL-TESTING-GUIDE.md Section 3.1: Staging Verification**

The user must now manually test the feature in staging:

**Instructions for User**:

1. **Test Archive Operation** (5 min):
   - Create a test folder in staging vault
   - Use agent to archive the folder
   - Verify folder moved to `archive/YYYY-MM-DD/folder-name`
   - Verify all files present in archive

2. **Test Tool Selection** (5 min):
   - Ask agent to "manage folders" → verify correct tool selected
   - Ask agent to "manage notes" → verify note tool selected (not folder tool)
   - Ask agent to "archive old project" → verify archive operation used

3. **Test Error Handling** (2 min):
   - Try to archive non-existent folder → verify clear error message
   - Try to use folder tool on a file → verify error redirects to note tool

4. **Test Integration** (3 min):
   - Archive folder containing notes with wikilinks
   - Verify wikilinks updated correctly

**User Sign-Off**:
☐ Archive operation works correctly
☐ Tool selection accurate (>95% in manual tests)
☐ Error messages clear and helpful
☐ Wikilink updates working
☐ **APPROVED FOR PRODUCTION DEPLOYMENT**

**If user does NOT approve**: Fix issues, redeploy to staging, re-test

**Stage 2 Result**: ☐ PASS (User Approved) ☐ FAIL (Needs Work)

---

## Stage 3: Canary Deployment - 5% Traffic (1 day)

### Objective
Deploy to 5% of production traffic, monitor for 24 hours before full rollout.

### 3.1 Deploy to Canary (5% Traffic)

**Option A: Feature Flag Approach** (Recommended)
```bash
# Enable feature for 5% of users via feature flag
# Update configuration
curl -X POST https://config.prod.example.com/feature-flags \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "feature": "archive_folder",
    "enabled": true,
    "rollout_percentage": 5
  }'
```

**Option B: Load Balancer Approach**
```bash
# Deploy to canary servers (5% of traffic)
ssh canary-server-1
cd /app/obsidian-agent
git pull origin main  # After merging feature branch to main
uv sync --frozen
sudo systemctl restart obsidian-agent
```

**Success Criteria**: ✅ Canary deployment successful, 5% traffic routing to new version

### 3.2 Monitor Canary (24 hours)

**Set up monitoring dashboard** to track:

**Key Metrics**:
- Archive operation success rate: Target >99%
- Tool selection accuracy: Target >95%
- Error rate: Target <1%
- P95 latency: Target <200ms
- Total requests processed

**Monitoring Commands**:
```bash
# Check error logs
ssh canary-server-1
tail -f /var/log/obsidian-agent/error.log

# Check success rate (from metrics database)
# Query last 24 hours of archive operations
curl https://metrics.prod.example.com/query?metric=archive_success_rate&period=24h
```

**Alerting**:
Set up alerts for:
- 🚨 Error rate >2%
- 🚨 Archive success rate <97%
- 🚨 P95 latency >500ms

### 3.3 24-Hour Canary Review

After 24 hours, review metrics:

**Canary Metrics** (24-hour window):
- Archive operations: ____ (count)
- Success rate: ____% (target: >99%)
- Tool selection accuracy: ____% (target: >95%)
- Error rate: ____% (target: <1%)
- P95 latency: ____ms (target: <200ms)
- Critical incidents: ____ (target: 0)

**Decision Point**:
☐ **PROCEED to Stage 4** - All metrics meet targets, no incidents
☐ **ROLLBACK** - Metrics below target or incidents occurred

**If ROLLBACK needed**: See "Rollback Procedure" section below

**Stage 3 Result**: ☐ PASS (Proceed to 100%) ☐ FAIL (Rollback)

---

## Stage 4: Full Production Rollout (2-3 days)

### Objective
Gradually rollout to 100% of production traffic: 25% → 50% → 100%

### 4.1 Deploy to 25% Traffic (Day 1)

**Feature Flag Approach**:
```bash
curl -X POST https://config.prod.example.com/feature-flags \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "feature": "archive_folder",
    "rollout_percentage": 25
  }'
```

**Monitor for 24 hours**:
- Same metrics as canary
- Review at end of 24 hours

**Decision**: ☐ Proceed to 50% ☐ Rollback

### 4.2 Deploy to 50% Traffic (Day 2)

```bash
curl -X POST https://config.prod.example.com/feature-flags \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "feature": "archive_folder",
    "rollout_percentage": 50
  }'
```

**Monitor for 24 hours**:
- Same metrics as canary
- Review at end of 24 hours

**Decision**: ☐ Proceed to 100% ☐ Rollback

### 4.3 Deploy to 100% Traffic (Day 3)

```bash
curl -X POST https://config.prod.example.com/feature-flags \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "feature": "archive_folder",
    "rollout_percentage": 100
  }'
```

**Monitor for 48 hours**:
- Intensive monitoring for first 48 hours
- Automated smoke tests every 6 hours

### 4.4 USER ACTION REQUIRED: Production Day 1 Smoke Test (10 minutes)

**📋 MANUAL-TESTING-GUIDE.md Section 3.2: Production Day 1**

**Instructions for User** (within 24 hours of 100% rollout):

1. **Verify Archive Feature Works** (5 min):
   - Archive a real folder in production vault
   - Verify folder moved correctly
   - Verify agent can find archived folders

2. **Check Error Logs** (3 min):
   - Review error logs for any issues
   - Verify no unexpected errors

3. **Spot Check Tool Selection** (2 min):
   - Ask agent several folder-related questions
   - Verify correct tool selected consistently

**User Sign-Off**:
☐ Archive feature working in production
☐ No errors in logs
☐ Tool selection accurate
☐ **PRODUCTION DEPLOYMENT SUCCESSFUL**

**Stage 4 Result**: ☐ PASS (100% Deployed Successfully) ☐ FAIL (Issues Found)

---

## Rollback Procedure

If issues are detected at ANY stage:

### Immediate Rollback Steps

**Feature Flag Rollback** (Fastest - 2 minutes):
```bash
# Disable feature immediately
curl -X POST https://config.prod.example.com/feature-flags \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "feature": "archive_folder",
    "enabled": false
  }'
```

**Code Rollback** (If needed - 10 minutes):
```bash
#!/bin/bash
# rollback-production.sh

echo "🚨 INITIATING PRODUCTION ROLLBACK"

# Revert to previous version
for server in $PRODUCTION_SERVERS; do
  ssh $server <<EOF
    cd /app/obsidian-agent
    git checkout main
    git revert HEAD --no-edit
    uv sync --frozen
    sudo systemctl restart obsidian-agent
EOF
done

echo "✅ Rollback complete"
```

### Post-Rollback Actions

1. **Notify stakeholders** - Deployment rolled back, investigating issues
2. **Analyze root cause** - What went wrong?
3. **Fix issues** - Update code, tests, validation
4. **Re-run pre-deployment** - Ensure fix works
5. **Schedule re-deployment** - Start from Stage 1 again

---

## Deployment Checklist

Track your progress through deployment stages:

```
☐ Pre-deployment validation complete (all tests pass)
☐ Stage 1: Local/Dev (30 min)
  ☐ Local smoke tests pass
  ☐ No errors in logs
☐ Stage 2: Staging (1 day)
  ☐ Staging deployment successful
  ☐ Integration tests pass
  ☐ User acceptance testing complete
  ☐ User approved for production
☐ Stage 3: Canary 5% (1 day)
  ☐ Canary deployment successful
  ☐ 24-hour monitoring complete
  ☐ All metrics meet targets
  ☐ 0 critical incidents
  ☐ Decision: Proceed to Stage 4
☐ Stage 4: Full Production (2-3 days)
  ☐ 25% rollout (monitor 24h)
  ☐ 50% rollout (monitor 24h)
  ☐ 100% rollout (monitor 48h)
  ☐ User Day 1 smoke test complete
  ☐ Production deployment successful
```

---

## Success Criteria Summary

**Deployment is successful when**:
- ✅ 100% traffic routing to new version
- ✅ Archive success rate >99%
- ✅ Tool selection accuracy >95%
- ✅ Error rate <1%
- ✅ P95 latency <200ms
- ✅ 0 critical incidents
- ✅ User confirms feature working

---

## What's Next?

When deployment is complete and successful:

**Run `/monitor`** to begin post-deployment monitoring and validation.

This starts the 30-day intensive monitoring period to ensure long-term success.

---

## Important Notes

**⏱️ Deployment Timeline**:
- Minimum: 3 days (if all goes perfectly)
- Typical: 4-5 days (with normal validation pauses)
- Maximum: 1-2 weeks (if issues found and fixed)

**🚨 When to Rollback**:
- Error rate >2%
- Success rate <97%
- Critical incident
- User reports blocking issues
- Metrics degrading over time

**✅ When to Proceed**:
- All metrics meet targets
- No critical incidents
- User confirms feature working
- Monitoring period complete

**Good luck with deployment!** 🚀
