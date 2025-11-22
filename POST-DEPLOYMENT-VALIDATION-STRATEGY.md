# Post-Deployment Validation Strategy

**Related Documents**:
- Pre-Deployment: `PRE-DEPLOYMENT-VALIDATION-SUMMARY.md`
- Deployment: `DEPLOYMENT-VALIDATION-STRATEGY.md`
- Manual Testing: `MANUAL-TESTING-GUIDE.md`
- Full Suite: `TESTING-AND-VALIDATION-STRATEGY.md`

---

## Overview

**Purpose**: Validate feature performance and correctness in production after full deployment.

**When**: AFTER 100% production deployment completes, for continuous monitoring.

**Duration**: First 30 days post-deployment (intensive), then ongoing monitoring.

---

## Timeline

```
Day 1-7:    Intensive monitoring (every 4 hours)
Day 8-14:   Active monitoring (daily)
Day 15-30:  Standard monitoring (weekly)
Day 31+:    Continuous monitoring (monthly reviews)
```

---

## 1. Production Health Monitoring (Continuous)

### 1.1 System Health Metrics

**Check Every**: 5 minutes (automated)

#### Metric 1: Service Availability
```bash
# Automated health check
curl https://api.prod.example.com/health

# Expected response time: <100ms
# Expected status: 200 OK
# Uptime target: 99.9%
```

**Alerts**:
- ⚠️ Warning: Response time >200ms
- 🚨 Critical: Response time >500ms or non-200 status
- 🔥 Emergency: Service down >5 minutes

---

#### Metric 2: Request Error Rate
```sql
-- Query from monitoring database
SELECT
    DATE_TRUNC('hour', timestamp) as hour,
    COUNT(*) as total_requests,
    SUM(CASE WHEN status >= 500 THEN 1 ELSE 0 END) as errors,
    (SUM(CASE WHEN status >= 500 THEN 1 ELSE 0 END)::float / COUNT(*)) * 100 as error_rate
FROM request_logs
WHERE service = 'obsidian-agent'
    AND tool = 'obsidian_folder_manage'
    AND timestamp > NOW() - INTERVAL '24 hours'
GROUP BY hour
ORDER BY hour DESC;
```

**Baseline**: <0.5% error rate
**Target**: <1% error rate
**Alert Threshold**: >2% error rate

---

#### Metric 3: Request Latency
```sql
-- P50, P95, P99 latency by operation
SELECT
    operation,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY duration_ms) as p50_ms,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY duration_ms) as p95_ms,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY duration_ms) as p99_ms,
    COUNT(*) as count
FROM operation_logs
WHERE tool = 'obsidian_folder_manage'
    AND timestamp > NOW() - INTERVAL '1 hour'
GROUP BY operation;
```

**Targets**:
- CREATE: p95 <100ms
- RENAME: p95 <300ms
- MOVE: p95 <300ms
- DELETE: p95 <200ms
- LIST: p95 <100ms
- **ARCHIVE**: p95 <500ms (new operation)

**Alerts**:
- ⚠️ Warning: p95 exceeds target by 50%
- 🚨 Critical: p95 exceeds target by 100%

---

### 1.2 Feature-Specific Metrics

#### Metric 1: Archive Operation Success Rate
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
**Alert**: <95% success rate

---

#### Metric 2: Wikilink Update Success Rate
```sql
SELECT
    DATE_TRUNC('day', timestamp) as day,
    AVG(metadata->>'links_updated'::int) as avg_links_updated,
    COUNT(*) as operations_with_updates
FROM operation_logs
WHERE tool = 'obsidian_folder_manage'
    AND operation IN ('archive', 'rename', 'move')
    AND (metadata->>'links_updated')::int > 0
    AND timestamp > NOW() - INTERVAL '7 days'
GROUP BY day
ORDER BY day DESC;
```

**Monitor**: Average links updated per operation
**Alert**: Sudden drop to 0 (wikilink update failure)

---

#### Metric 3: Tool Selection Accuracy
```sql
-- Monitor tool confusion (wrong tool selected)
SELECT
    DATE_TRUNC('day', timestamp) as day,
    COUNT(*) as total_folder_operations,
    SUM(CASE WHEN error_message LIKE '%wrong tool%' OR error_message LIKE '%use obsidian_note_manage%' THEN 1 ELSE 0 END) as tool_confusion_errors,
    (SUM(CASE WHEN error_message LIKE '%wrong tool%' THEN 1 ELSE 0 END)::float / COUNT(*)) * 100 as confusion_rate
FROM operation_logs
WHERE tool = 'obsidian_folder_manage'
    AND timestamp > NOW() - INTERVAL '7 days'
GROUP BY day
ORDER BY day DESC;
```

**Baseline**: 20% tool confusion (before deployment)
**Target**: <5% tool confusion (after deployment)
**Success**: Measure improvement over baseline

---

### 1.3 User Impact Metrics

#### Metric 1: User Adoption Rate
```sql
-- How many users are using archive operation
SELECT
    DATE_TRUNC('week', timestamp) as week,
    COUNT(DISTINCT user_id) as unique_users_archiving,
    COUNT(*) as total_archive_operations
FROM operation_logs
WHERE tool = 'obsidian_folder_manage'
    AND operation = 'archive'
    AND timestamp > NOW() - INTERVAL '30 days'
GROUP BY week
ORDER BY week DESC;
```

**Monitor**: Gradual increase in adoption
**Target**: 10% of active users try archive within 30 days

---

#### Metric 2: User Satisfaction (Indirect)
```sql
-- Monitor for repeated failures (user frustration indicator)
SELECT
    user_id,
    COUNT(*) as failed_attempts,
    MAX(timestamp) as last_failure
FROM operation_logs
WHERE tool = 'obsidian_folder_manage'
    AND success = false
    AND timestamp > NOW() - INTERVAL '7 days'
GROUP BY user_id
HAVING COUNT(*) > 5
ORDER BY failed_attempts DESC
LIMIT 20;
```

**Alert**: >5 failures per user in 7 days (investigate)

---

## 2. Production Smoke Tests (Daily)

### 2.1 Automated Production Smoke Tests

**Run**: Every 6 hours via scheduled job

```bash
#!/bin/bash
# production-smoke-tests.sh

echo "🔍 Running production smoke tests..."

# Test 1: Health check
echo "Test 1: Health check"
HEALTH=$(curl -s -w "%{http_code}" https://api.prod.example.com/health)
if [[ $HEALTH == *"200"* ]]; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed: $HEALTH"
    exit 1
fi

# Test 2: Tool availability
echo "Test 2: Tool availability"
TOOLS=$(curl -s https://api.prod.example.com/api/agent/tools | jq -r '.tools[]' | grep -c "obsidian_folder_manage")
if [[ $TOOLS -eq 1 ]]; then
    echo "✅ obsidian_folder_manage tool available"
else
    echo "❌ obsidian_folder_manage tool not found"
    exit 1
fi

# Test 3: Create operation (in test vault)
echo "Test 3: Create operation"
CREATE_RESULT=$(curl -s -X POST https://api.prod.example.com/api/agent/execute \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $SMOKE_TEST_TOKEN" \
    -d "{
        \"tool\": \"obsidian_folder_manage\",
        \"parameters\": {
            \"path\": \"smoke-test-$(date +%s)\",
            \"operation\": \"create\",
            \"vault\": \"test-vault\"
        }
    }")

if echo $CREATE_RESULT | jq -e '.success' > /dev/null; then
    echo "✅ Create operation passed"
else
    echo "❌ Create operation failed: $CREATE_RESULT"
    exit 1
fi

# Test 4: Archive operation (new feature)
echo "Test 4: Archive operation"
ARCHIVE_RESULT=$(curl -s -X POST https://api.prod.example.com/api/agent/execute \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $SMOKE_TEST_TOKEN" \
    -d "{
        \"tool\": \"obsidian_folder_manage\",
        \"parameters\": {
            \"path\": \"smoke-test-folder\",
            \"operation\": \"archive\",
            \"vault\": \"test-vault\"
        }
    }")

if echo $ARCHIVE_RESULT | jq -e '.success' > /dev/null; then
    ARCHIVE_PATH=$(echo $ARCHIVE_RESULT | jq -r '.new_path')
    if [[ $ARCHIVE_PATH == archive/* ]]; then
        echo "✅ Archive operation passed: $ARCHIVE_PATH"
    else
        echo "❌ Archive path format incorrect: $ARCHIVE_PATH"
        exit 1
    fi
else
    echo "❌ Archive operation failed: $ARCHIVE_RESULT"
    exit 1
fi

echo "✅ All production smoke tests passed"
```

**Success Criteria**: All tests pass
**Failure Action**: Alert on-call engineer

---

### 2.2 Manual Production Verification (Daily - Day 1-7)

**Performed By**: On-call engineer or QA

#### Test 1: Archive Operation with Real Vault
1. Log into production agent
2. Create test folder with 3 notes
3. Archive the folder
4. Verify:
   - Folder moved to `archive/YYYY-MM-DD/`
   - All 3 notes present in archive
   - Archive path returned correctly
   - Operation logged in database

**Duration**: 5 minutes
**Frequency**: Once daily for first 7 days

---

#### Test 2: Tool Selection Check
1. Send agent: "Create a folder called test-projects"
2. Verify agent uses `obsidian_folder_manage`
3. Send agent: "Create a note called test.md"
4. Verify agent uses `obsidian_note_manage` (not folder_manage)
5. Send agent: "Archive the old-drafts folder"
6. Verify agent uses `obsidian_folder_manage` with `operation=archive`

**Duration**: 5 minutes
**Frequency**: Once daily for first 7 days

---

## 3. User Feedback Collection

### 3.1 Active User Feedback (Week 1-2)

**Method**: Reach out to early adopters

#### Survey Questions
1. Have you used the archive folder feature?
   - [ ] Yes, multiple times
   - [ ] Yes, once
   - [ ] No, didn't know about it
   - [ ] No, don't need it

2. Was the agent able to correctly identify when you wanted to work with folders vs notes?
   - [ ] Always correct
   - [ ] Mostly correct
   - [ ] Sometimes confused
   - [ ] Often confused

3. Did the archive operation work as expected?
   - [ ] Yes, perfectly
   - [ ] Yes, but had minor issues
   - [ ] No, had problems (describe)
   - [ ] Haven't tried it yet

4. Were your wikilinks updated correctly after archiving?
   - [ ] Yes, all links work
   - [ ] Some links broken
   - [ ] Many links broken
   - [ ] Didn't check

5. Any suggestions or issues?
   - [Free text response]

**Target Responses**: 20-30 users
**Timeline**: Send Week 1, analyze Week 2

---

### 3.2 Passive Feedback Monitoring

**Monitor Channels**:
- Support tickets (search: "folder", "archive", "tool confusion")
- User forum (search: "can't archive", "wrong tool")
- Error logs (search: error patterns)
- Feature usage analytics

**Red Flags**:
- Multiple users reporting same issue
- "Archive didn't work" complaints
- "Agent is confused about folders/notes"
- Wikilink breakage reports

---

## 4. Performance Validation

### 4.1 Load Testing (Week 1)

**Purpose**: Ensure archive operation handles production load

#### Load Test Scenario
```bash
# Simulate 100 concurrent archive operations
artillery run load-test-archive.yml
```

**load-test-archive.yml**:
```yaml
config:
  target: 'https://api.prod.example.com'
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 300
      arrivalRate: 100
      name: "Sustained load"
    - duration: 60
      arrivalRate: 200
      name: "Peak load"

scenarios:
  - name: "Archive operation"
    flow:
      - post:
          url: "/api/agent/execute"
          headers:
            Authorization: "Bearer {{ $processEnvironment.LOAD_TEST_TOKEN }}"
          json:
            tool: "obsidian_folder_manage"
            parameters:
              path: "test-{{ $randomString() }}"
              operation: "archive"
              vault: "load-test-vault"
```

**Success Criteria**:
- p95 latency <500ms under sustained load
- p99 latency <1s under sustained load
- Error rate <1% under sustained load
- No memory leaks or resource exhaustion

---

### 4.2 Stress Testing (Week 2)

**Purpose**: Find breaking point

#### Stress Test Scenario
```bash
# Gradually increase load until failure
artillery run stress-test-archive.yml
```

**Monitors**:
- At what RPS (requests/sec) does latency spike?
- At what RPS does error rate increase?
- What resources are exhausted first? (CPU, memory, database connections)

**Action**: Document limits and set alerts before limits reached

---

## 5. Data Integrity Validation

### 5.1 Wikilink Integrity Check (Weekly)

```sql
-- Find broken wikilinks potentially caused by archive operation
SELECT
    note_path,
    wikilink,
    COUNT(*) as occurrences
FROM wikilinks_index
WHERE target_exists = false
    AND last_checked > NOW() - INTERVAL '7 days'
    AND wikilink LIKE 'archive/%'
GROUP BY note_path, wikilink
HAVING COUNT(*) > 5
ORDER BY occurrences DESC
LIMIT 20;
```

**Action**: Investigate high-occurrence broken links
**Expected**: <0.1% broken wikilinks from archive operations

---

### 5.2 Archive Path Validation (Weekly)

```bash
#!/bin/bash
# validate-archive-paths.sh

echo "🔍 Validating archive folder structure..."

# Expected pattern: archive/YYYY-MM-DD/folder-name
find /vault/archive -mindepth 2 -maxdepth 2 -type d | while read folder; do
    # Check date format
    date_part=$(echo $folder | cut -d'/' -f3)
    if ! date -d "$date_part" >/dev/null 2>&1; then
        echo "⚠️  Invalid date format: $folder"
    fi
done

echo "✅ Archive path validation complete"
```

---

## 6. Rollback Readiness Validation

### 6.1 Rollback Trigger Criteria

**Trigger Rollback If**:
- Error rate >5% for >1 hour
- Critical bug affecting >10% of users
- Data corruption detected
- Security vulnerability discovered
- Performance degradation >50% baseline

---

### 6.2 Rollback Dry Run (Day 7)

**Purpose**: Verify rollback procedure works if needed

```bash
# On ONE canary server (not full production)
ssh canary-1.prod.example.com <<EOF
    cd /app/obsidian-agent

    # Backup current state
    git tag rollback-test-$(date +%Y%m%d)

    # Rollback to previous version
    git checkout main
    uv sync
    sudo systemctl restart obsidian-agent

    # Verify service healthy
    sleep 10
    curl http://localhost:8030/health

    # Verify archive operation NOT available (if it was main-only feature)
    # Or verify old behavior restored

    # Return to new version
    git checkout claude/review-agent-core-01E8UdzqkJNLQKTxMGeeR8rK
    uv sync
    sudo systemctl restart obsidian-agent

    # Verify service healthy again
    sleep 10
    curl http://localhost:8030/health
EOF
```

**Success**: Rollback and roll-forward both work without issues

---

## 7. Gradual Feature Enablement (Optional)

### 7.1 Feature Flag Strategy

**If implemented**, enable archive operation gradually:

**Week 1**: 10% of users
**Week 2**: 25% of users
**Week 3**: 50% of users
**Week 4**: 100% of users

```python
# Feature flag check
def is_archive_enabled(user_id: str) -> bool:
    # Gradual rollout based on user ID hash
    import hashlib
    hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    rollout_percentage = get_config("archive_rollout_percentage", default=100)
    return (hash_value % 100) < rollout_percentage
```

**Monitoring**: Compare metrics between enabled/disabled users

---

## 8. Long-Term Monitoring (Day 31+)

### 8.1 Monthly Health Check

**Performed**: First Monday of each month

#### Checklist
- [ ] Review error rate trends (should remain <1%)
- [ ] Review latency trends (should remain stable or improve)
- [ ] Review user adoption (should grow steadily)
- [ ] Review feature usage patterns
- [ ] Check for new edge cases or failure modes
- [ ] Review user feedback from past month
- [ ] Verify wikilink integrity
- [ ] Review archive path patterns
- [ ] Check for any security incidents
- [ ] Update runbooks based on incidents

**Duration**: 30 minutes
**Output**: Monthly health report

---

### 8.2 Quarterly Performance Review

**Performed**: End of each quarter

#### Analysis
1. **Feature Success Metrics**
   - Tool selection accuracy: Baseline 80% → Current ___%
   - Archive operation success rate: Target >99%, Current ___%
   - User adoption: Target 10% of users, Current ___%
   - User satisfaction: Measured via survey

2. **Performance Metrics**
   - Archive p95 latency: Target <500ms, Current ___ms
   - Error rate: Target <1%, Current ___%
   - Uptime: Target 99.9%, Current ___%

3. **Business Impact**
   - Reduced tool confusion support tickets: ___%
   - User productivity improvement (if measurable)
   - Time saved vs manual archiving

**Output**: Quarterly review report with recommendations

---

## 9. Post-Deployment Checklist

### Day 1 Checklist
- [ ] 100% production deployment complete
- [ ] All smoke tests passing
- [ ] Monitoring dashboards configured
- [ ] Alerts configured and tested
- [ ] On-call engineer briefed
- [ ] Rollback procedure documented and tested
- [ ] First metrics baseline captured

### Week 1 Checklist
- [ ] Daily manual verification complete (7 days)
- [ ] Error rate <1%
- [ ] No critical bugs reported
- [ ] User feedback collection started
- [ ] Load testing complete
- [ ] Wikilink integrity validated
- [ ] Rollback dry run successful

### Week 2 Checklist
- [ ] Stress testing complete
- [ ] User feedback analyzed (20+ responses)
- [ ] Tool selection accuracy validated (>95%)
- [ ] Archive adoption measured (baseline)
- [ ] Any issues from Week 1 resolved

### Week 4 Checklist
- [ ] Monthly health check complete
- [ ] User adoption tracked
- [ ] Performance trends analyzed
- [ ] No rollback required
- [ ] Feature considered stable

### Day 90 Checklist
- [ ] Quarterly performance review complete
- [ ] Feature success metrics documented
- [ ] User satisfaction measured
- [ ] Business impact assessed
- [ ] Recommendations for future improvements
- [ ] Close post-deployment validation phase

---

## 10. Incident Response

### 10.1 Incident Severity Levels

**P0 - Critical** (Response: Immediate)
- Service down
- Data corruption
- Security breach
- Error rate >10%

**P1 - High** (Response: <1 hour)
- Error rate 5-10%
- Performance degradation >100% baseline
- Feature completely broken

**P2 - Medium** (Response: <4 hours)
- Error rate 2-5%
- Performance degradation 50-100%
- Feature partially broken

**P3 - Low** (Response: <24 hours)
- Error rate 1-2%
- Minor performance degradation
- Edge case failure

---

### 10.2 Incident Response Playbook

#### For P0/P1 Incidents

1. **Acknowledge** (0-5 minutes)
   - Acknowledge alert
   - Notify team in incident channel

2. **Assess** (5-15 minutes)
   - Check monitoring dashboards
   - Review recent changes
   - Determine scope and impact

3. **Mitigate** (15-60 minutes)
   - **Option A**: Rollback deployment
   - **Option B**: Disable feature via feature flag
   - **Option C**: Apply hotfix
   - **Option D**: Scale resources if load issue

4. **Resolve** (1-4 hours)
   - Fix root cause
   - Test fix in staging
   - Deploy fix to production
   - Verify resolution

5. **Document** (4-24 hours)
   - Write incident report
   - Document root cause
   - Create preventive action items
   - Update runbooks

---

## 11. Success Criteria

**Post-deployment validation successful when**:

### Immediate Success (Week 1)
- ✅ All smoke tests passing
- ✅ Error rate <1%
- ✅ No P0/P1 incidents
- ✅ Archive operation working correctly
- ✅ Wikilink updates working correctly

### Short-Term Success (Month 1)
- ✅ Tool selection accuracy >95%
- ✅ Archive p95 latency <500ms
- ✅ User adoption >5% of active users
- ✅ Positive user feedback (>80% satisfied)
- ✅ No rollback required

### Long-Term Success (Quarter 1)
- ✅ Feature stable and reliable
- ✅ User adoption >10% of active users
- ✅ Tool confusion reduced by >50%
- ✅ Business impact measurable and positive
- ✅ No outstanding critical issues

---

## 12. Communication & Reporting

### Daily Status Updates (Week 1)
**Sent To**: Development team, stakeholders
**Format**: Slack/Email
```
📊 Post-Deployment Status - Day X

✅ Production health: Normal
📈 Error rate: 0.3% (target: <1%)
⚡ Archive p95: 245ms (target: <500ms)
👥 Archive usage: 127 operations today
🎯 Tool selection: 97% accurate

Issues: None
Next check: Tomorrow 9am
```

### Weekly Reports (Week 2-4)
**Sent To**: Leadership, stakeholders
**Format**: Document/Email

**Includes**:
- Key metrics summary
- User feedback highlights
- Issues encountered and resolved
- Adoption trends
- Performance trends

### Monthly Reports (Month 2+)
**Sent To**: Leadership, stakeholders
**Format**: Presentation + Document

**Includes**:
- Monthly health check results
- Feature success metrics
- User satisfaction scores
- Business impact assessment
- Recommendations

---

**Version**: 1.0
**Last Updated**: 2025-01-22
**Owner**: Development Team
