---
description: Monitor production deployment over 30-day period with success validation
---

# Post-Deployment Monitoring Sequence

You are guiding the user through 30 days of post-deployment monitoring to ensure long-term feature success.

## Overview

This is the **Post-Deployment Monitoring Sequence** from PLANNING.md - designed for production monitoring and success validation.

**Total Time**: 30 days of monitoring (70 min user involvement recommended)
**Goal**: Validate feature meets all success criteria, declare feature complete

## Primary Guide

Your PRIMARY reference is:
📘 **POST-DEPLOYMENT-VALIDATION-STRATEGY.md**

This document contains the 30-day monitoring strategy with metrics, alerts, and validation procedures.

## Prerequisites Check

Before starting monitoring, verify deployment complete:

```bash
# Deployment complete?
# Run /deploy if not already done

# Feature at 100% rollout?
# Check feature flag or deployment status
```

**Required**: ✅ Deployment to 100% production must be complete

---

## Monitoring Overview

**30-Day Monitoring Timeline**:
```
Day 1-7: Intensive Daily Monitoring
    ↓ (Daily checks, automated alerts, user involved)
Week 2-4: Weekly Monitoring
    ↓ (Weekly reviews, trend analysis, user check-ins)
Ongoing: Monthly Reviews
    ↓ (Monthly success validation, continuous improvement)
```

---

## Day 1-7: Intensive Daily Monitoring

### Objective
Catch issues early with intensive daily monitoring and automated alerts.

### Automated Monitoring (No User Action - Runs Every 6 Hours)

**Automated Smoke Tests** (configured to run every 6 hours):

```bash
#!/bin/bash
# production-smoke-test.sh (runs automatically every 6 hours)

PROD_URL="https://api.prod.example.com"
SMOKE_TEST_TOKEN="<token>"

# Test 1: Health check
echo "Test 1: Health check"
curl -s $PROD_URL/health | jq .

# Test 2: Archive operation
echo "Test 2: Archive operation"
ARCHIVE_RESULT=$(curl -s -X POST $PROD_URL/api/agent/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SMOKE_TEST_TOKEN" \
  -d '{
    "tool": "obsidian_folder_manage",
    "parameters": {
      "path": "smoke-test-folder-'$(date +%s)'",
      "operation": "archive"
    }
  }')

echo $ARCHIVE_RESULT | jq .

# Test 3: Tool selection
echo "Test 3: Tool selection accuracy"
# Run 10 tool selection tests...

# Alert if any test fails
if [ $? -ne 0 ]; then
  curl -X POST https://alerts.example.com/alert \
    -d '{"severity": "high", "message": "Production smoke test failed"}'
fi
```

**Expected**: All smoke tests pass every 6 hours

### Production Metrics Dashboard

**Set up monitoring dashboard** with these key metrics:

#### Metric 1: Archive Operation Success Rate

**Query** (SQL for metrics database):
```sql
SELECT
    DATE_TRUNC('day', timestamp) as day,
    COUNT(*) as total_archives,
    SUM(CASE WHEN success = true THEN 1 ELSE 0 END) as successful,
    (SUM(CASE WHEN success = true THEN 1 ELSE 0 END)::float / COUNT(*)) * 100 as success_rate
FROM operation_logs
WHERE tool = 'obsidian_folder_manage'
    AND operation = 'archive'
    AND timestamp > NOW() - INTERVAL '7 days'
GROUP BY day
ORDER BY day DESC;
```

**Target**: >99% success rate
**Alert if**: Success rate <97%

#### Metric 2: Tool Selection Accuracy

**Query**:
```sql
SELECT
    DATE_TRUNC('day', timestamp) as day,
    COUNT(*) as total_tool_calls,
    SUM(CASE WHEN tool_selected = expected_tool THEN 1 ELSE 0 END) as correct_selections,
    (SUM(CASE WHEN tool_selected = expected_tool THEN 1 ELSE 0 END)::float / COUNT(*)) * 100 as accuracy
FROM tool_selection_logs
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY day
ORDER BY day DESC;
```

**Target**: >95% accuracy
**Alert if**: Accuracy <90%

#### Metric 3: Error Rate

**Query**:
```sql
SELECT
    DATE_TRUNC('hour', timestamp) as hour,
    COUNT(*) as total_requests,
    SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as errors,
    (SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END)::float / COUNT(*)) * 100 as error_rate
FROM request_logs
WHERE timestamp > NOW() - INTERVAL '24 hours'
GROUP BY hour
ORDER BY hour DESC;
```

**Target**: <1% error rate
**Alert if**: Error rate >2%

#### Metric 4: P95 Latency

**Query**:
```sql
SELECT
    percentile_cont(0.95) WITHIN GROUP (ORDER BY duration_ms) as p95_latency
FROM operation_logs
WHERE tool = 'obsidian_folder_manage'
    AND timestamp > NOW() - INTERVAL '24 hours';
```

**Target**: <200ms P95 latency
**Alert if**: P95 latency >500ms

### Daily Manual Check (Days 1-7) - 5 minutes per day

**USER ACTION - Recommended Daily (5 min)**:

Review the metrics dashboard each day for the first week:

**Daily Checklist**:
```
Day 1:
☐ Archive success rate: ____% (target: >99%)
☐ Tool selection accuracy: ____% (target: >95%)
☐ Error rate: ____% (target: <1%)
☐ P95 latency: ____ms (target: <200ms)
☐ Incidents: ____ (target: 0)
☐ Status: ☐ Healthy ☐ Needs Attention

Day 2:
☐ Archive success rate: ____% (target: >99%)
☐ Tool selection accuracy: ____% (target: >95%)
☐ Error rate: ____% (target: <1%)
☐ P95 latency: ____ms (target: <200ms)
☐ Incidents: ____ (target: 0)
☐ Status: ☐ Healthy ☐ Needs Attention

[... repeat for Days 3-7 ...]
```

**If any metric below target**: Investigate immediately

---

## Week 1 Check-In: USER ACTION REQUIRED (10 minutes)

**📋 MANUAL-TESTING-GUIDE.md Section 3.2: Week 1 Check-In**

At end of Week 1, user should:

### 1. Review Week 1 Metrics (3 min)

```
Week 1 Summary (Day 1-7):
- Total archive operations: ____
- Average success rate: ____% (target: >99%)
- Average tool selection accuracy: ____% (target: >95%)
- Average error rate: ____% (target: <1%)
- Average P95 latency: ____ms (target: <200ms)
- Total incidents: ____ (target: 0)
```

### 2. Test Archive Feature (5 min)

Manually archive a folder in production:
- ☐ Create test folder with notes
- ☐ Use agent to archive folder
- ☐ Verify folder moved to `archive/YYYY-MM-DD/folder-name`
- ☐ Verify wikilinks updated
- ☐ Verify feature working as expected

### 3. Review Error Logs (2 min)

Check for any unexpected errors:
```bash
# Check error logs from last 7 days
grep -i "error" /var/log/obsidian-agent/error.log | tail -50
```

- ☐ Errors reviewed
- ☐ No critical issues found
- ☐ Any issues documented and tracked

**Week 1 Result**: ☐ PASS (All targets met) ☐ NEEDS ATTENTION (Some targets missed)

---

## Week 2-4: Weekly Monitoring

### Objective
Continue monitoring with weekly reviews and trend analysis.

### Week 2 Check-In: USER ACTION REQUIRED (10 minutes)

**Instructions for User**:

### 1. Review Week 2 Metrics (3 min)

```
Week 2 Summary (Day 8-14):
- Total archive operations: ____
- Average success rate: ____% (target: >99%)
- Average tool selection accuracy: ____% (target: >95%)
- Average error rate: ____% (target: <1%)
- Average P95 latency: ____ms (target: <200ms)
- Total incidents: ____ (target: 0)
```

### 2. Spot Check Tool Selection (5 min)

Test tool selection accuracy manually:
- Ask agent 5 folder-related questions
- ☐ Correct tool selected: __/5 (target: 5/5 or 4/5)

### 3. Performance Trend Analysis (2 min)

Compare Week 2 vs Week 1:
- ☐ Success rate trend: ☐ Improving ☐ Stable ☐ Degrading
- ☐ Tool accuracy trend: ☐ Improving ☐ Stable ☐ Degrading
- ☐ Latency trend: ☐ Improving ☐ Stable ☐ Degrading

**Week 2 Result**: ☐ PASS ☐ NEEDS ATTENTION

---

### Week 3 Check-In: USER ACTION REQUIRED (10 minutes)

**Instructions for User**:

### 1. Review Week 3 Metrics (3 min)

```
Week 3 Summary (Day 15-21):
- Total archive operations: ____
- Average success rate: ____% (target: >99%)
- Average tool selection accuracy: ____% (target: >95%)
- Average error rate: ____% (target: <1%)
- Average P95 latency: ____ms (target: <200ms)
- Total incidents: ____ (target: 0)
```

### 2. Review Error Logs (5 min)

Check for patterns or recurring issues:
```bash
# Analyze errors from last 7 days
grep -i "error" /var/log/obsidian-agent/error.log | \
  awk '{print $6}' | sort | uniq -c | sort -rn | head -10
```

- ☐ Errors reviewed
- ☐ Patterns identified: ______________________
- ☐ Action items created: ______________________

### 3. User Feedback Collection (2 min)

Informal user feedback:
- ☐ Users finding archive feature useful?
- ☐ Any complaints or issues reported?
- ☐ Feedback: ______________________

**Week 3 Result**: ☐ PASS ☐ NEEDS ATTENTION

---

### Week 4 Check-In: USER ACTION REQUIRED (10 minutes)

**Instructions for User**:

### 1. Review Week 4 Metrics (3 min)

```
Week 4 Summary (Day 22-28):
- Total archive operations: ____
- Average success rate: ____% (target: >99%)
- Average tool selection accuracy: ____% (target: >95%)
- Average error rate: ____% (target: <1%)
- Average P95 latency: ____ms (target: <200ms)
- Total incidents: ____ (target: 0)
```

### 2. 30-Day Success Validation (5 min)

Review complete 30-day period:

```
30-Day Summary (Day 1-30):
- Total archive operations: ____
- Overall success rate: ____% (target: >99%)
- Overall tool selection accuracy: ____% (target: >95%)
- Overall error rate: ____% (target: <1%)
- Overall P95 latency: ____ms (target: <200ms)
- Total critical incidents: ____ (target: 0)
```

### 3. Success Criteria Validation (2 min)

**From FOLDER-MANAGEMENT-ENHANCEMENT-PLAN.md Section 3:**

Validate all success criteria met:

```
Success Criteria Validation:
☐ Tool selection accuracy: >95% ✅ (____)
☐ Archive success rate: >99% ✅ (____)
☐ Test coverage: >90% ✅ (____)
☐ Type safety: 0 `Any` types ✅
☐ P95 latency: <200ms ✅ (____ ms)
☐ 0 critical incidents ✅ (____ incidents)
☐ User satisfaction: >4.5/5 ✅ (____ stars)
```

**Final Decision**:
☐ **ALL SUCCESS CRITERIA MET** - Feature complete ✅
☐ **SOME CRITERIA MISSED** - Continue monitoring, create improvement tasks

---

## Declaring Feature Complete

If all success criteria met after 30 days:

### Final Validation Checklist

```
✅ 30-day monitoring complete
✅ All success criteria met:
   ✅ Tool selection accuracy >95%
   ✅ Archive success rate >99%
   ✅ Error rate <1%
   ✅ P95 latency <200ms
   ✅ 0 critical incidents
   ✅ User satisfaction >4.5/5
✅ No outstanding critical issues
✅ User confirms feature working well
✅ Metrics stable or improving (not degrading)
```

### Celebrate & Document

**Congratulations!** 🎉 Feature successfully deployed and validated.

**Final Steps**:

1. **Document lessons learned**:
   - What went well?
   - What could be improved?
   - Any surprises or unexpected issues?

2. **Update documentation**:
   - Mark feature as "Completed" in project tracking
   - Update README with new archive feature
   - Archive planning documents for future reference

3. **Share success**:
   - Announce feature completion to team
   - Share metrics and success story
   - Thank contributors

4. **Transition to ongoing monitoring**:
   - Reduce monitoring frequency to monthly reviews
   - Keep automated alerts active
   - Continue tracking key metrics

---

## Ongoing: Monthly Reviews (After Day 30)

### Objective
Maintain feature health with monthly reviews.

### Monthly Review Checklist (10 min/month)

```
Month 2:
☐ Review 30-day metrics
☐ Success rate: ____% (target: >99%)
☐ Tool accuracy: ____% (target: >95%)
☐ Error rate: ____% (target: <1%)
☐ Any new issues identified?
☐ Status: ☐ Healthy ☐ Needs Attention

Month 3:
[... same checklist ...]

Month 4+:
[... same checklist ...]
```

**Frequency**: Once per month indefinitely

---

## Incident Response

If critical incident occurs at ANY time:

### Critical Incident Procedure

**Critical Incident Definition**:
- Error rate >5%
- Success rate <90%
- Complete feature outage
- Data loss or corruption
- Security vulnerability

**Immediate Actions**:

1. **Assess severity** (2 min):
   - What is broken?
   - How many users affected?
   - Is data at risk?

2. **Consider rollback** (5 min):
   - Is immediate rollback needed?
   - Can issue be hotfixed quickly?
   - Decision: ☐ Rollback ☐ Hotfix ☐ Monitor

3. **Execute response** (10-30 min):
   - If rollback: Disable feature flag or revert code
   - If hotfix: Deploy fix through staging → production
   - If monitor: Increase monitoring frequency

4. **Notify stakeholders** (5 min):
   - What happened?
   - What action taken?
   - Expected resolution time?

5. **Post-incident review** (60 min within 48 hours):
   - Root cause analysis
   - What could prevent this in future?
   - Update monitoring/alerts if needed

---

## Metrics Dashboard Setup

Recommended dashboard tools:
- **Grafana** - For real-time metrics visualization
- **Datadog** - For APM and alerting
- **CloudWatch** - For AWS-hosted services
- **Custom Dashboard** - Using metrics database + charting library

**Dashboard Panels to Create**:

1. **Archive Success Rate** (line chart, 30-day)
2. **Tool Selection Accuracy** (line chart, 30-day)
3. **Error Rate** (line chart, 7-day)
4. **P95 Latency** (line chart, 7-day)
5. **Daily Operation Count** (bar chart, 30-day)
6. **Top 10 Errors** (table, last 7 days)
7. **Alerting Status** (indicator, real-time)

---

## Time Investment Summary

| Activity | Frequency | Time per Occurrence | Total (30 days) |
|----------|-----------|---------------------|-----------------|
| **User Actions** | | | |
| Daily checks (Days 1-7) | 7x | 5 min | 35 min |
| Week 1 check-in | 1x | 10 min | 10 min |
| Week 2 check-in | 1x | 10 min | 10 min |
| Week 3 check-in | 1x | 10 min | 10 min |
| Week 4 check-in | 1x | 10 min | 10 min |
| **User Total** | | | **75 min (1h 15m)** |
| **Automated** | | | |
| Smoke tests | 120x (every 6h) | 2 min | 240 min (automated) |
| Metrics collection | Continuous | - | - (automated) |
| Alerts | As needed | - | - (automated) |

**User Involvement**: 75 minutes over 30 days (~2.5 min/day average)

---

## Success Declaration Template

When feature is complete, send this:

```
🎉 Feature Complete: Folder Management Enhancement

After 30 days of intensive monitoring, the folder management enhancement feature has successfully met all success criteria:

✅ Success Criteria:
- Tool selection accuracy: 97.3% (target: >95%)
- Archive success rate: 99.8% (target: >99%)
- Error rate: 0.4% (target: <1%)
- P95 latency: 156ms (target: <200ms)
- Critical incidents: 0 (target: 0)
- User satisfaction: 4.7/5 stars (target: >4.5)

📊 30-Day Metrics:
- Total archive operations: 1,247
- Total folder operations: 8,932
- Successful operations: 8,892 (99.6%)
- Failed operations: 40 (0.4%)

🚀 Impact:
- LLM tool confusion reduced from 20% → 2.7%
- New archive feature used 1,247 times in 30 days
- User productivity increased with automated archiving
- No data loss or security incidents

📝 Lessons Learned:
- [List key learnings]

🔗 Documentation:
- Implementation Plan: FOLDER-MANAGEMENT-ENHANCEMENT-PLAN.md
- Testing Strategy: TESTING-AND-VALIDATION-STRATEGY.md
- Post-Deployment Monitoring: POST-DEPLOYMENT-VALIDATION-STRATEGY.md

Feature transitioning to ongoing monthly monitoring.

Thank you to all contributors! 🙏
```

---

## Troubleshooting

**Issue**: Metrics below target
- **Action**: Investigate root cause, create improvement tasks, continue monitoring

**Issue**: User reports problems but metrics look good
- **Action**: Metrics may not capture all issues, do qualitative user research

**Issue**: Automated alerts too noisy
- **Action**: Tune alert thresholds, reduce false positives

**Issue**: Not enough data to validate success
- **Action**: Extend monitoring period, encourage feature usage

---

**You're monitoring a production feature!** Great work getting this far. The monitoring phase is just as important as implementation - it ensures long-term success. 📊✅
