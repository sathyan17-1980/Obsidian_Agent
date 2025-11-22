# Deployment Validation Strategy

**Related Documents**:
- Pre-Deployment: `PRE-DEPLOYMENT-VALIDATION-SUMMARY.md`
- Post-Deployment: `POST-DEPLOYMENT-VALIDATION-STRATEGY.md`
- Manual Testing: `MANUAL-TESTING-GUIDE.md`
- Full Suite: `TESTING-AND-VALIDATION-STRATEGY.md`

---

## Overview

**Purpose**: Validate the deployment process itself and ensure safe rollout to production.

**When**: DURING the deployment process, between pre-deployment checks passing and production release.

**Deployment Strategy**: Staged rollout with validation at each stage.

---

## Deployment Stages

```
[Pre-Deployment] ✓
       ↓
[Stage 1: Local/Dev Environment] → Smoke Tests
       ↓
[Stage 2: Staging Environment] → Integration Validation
       ↓
[Stage 3: Canary Deployment] → Limited Production Testing
       ↓
[Stage 4: Full Production] → Production Validation
       ↓
[Post-Deployment Monitoring] → Continuous Validation
```

---

## Stage 1: Local/Dev Environment Validation

### 1.1 Build Validation

**Purpose**: Ensure code compiles and packages correctly.

#### Test 1: Clean Build
```bash
# Remove existing build artifacts
rm -rf dist/ build/ *.egg-info

# Build package
uv build

# Verify build artifacts
ls -lh dist/
```

**Success Criteria**:
- [ ] Build completes without errors
- [ ] Distribution files created (.whl and .tar.gz)
- [ ] Package size reasonable (<10MB for this project)
- [ ] No warnings during build

---

#### Test 2: Package Installation
```bash
# Create fresh virtual environment
python -m venv test-venv
source test-venv/bin/activate

# Install built package
pip install dist/*.whl

# Verify installation
python -c "import src.tools.obsidian_folder_manager.tool; print('Success')"

# Clean up
deactivate
rm -rf test-venv
```

**Success Criteria**:
- [ ] Package installs without errors
- [ ] All dependencies installed
- [ ] Imports work correctly
- [ ] No missing files

---

### 1.2 Local Smoke Tests

**Purpose**: Quick sanity check that basic functionality works.

#### Smoke Test 1: Server Starts
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8030 &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Test health endpoint
curl http://localhost:8030/health

# Stop server
kill $SERVER_PID
```

**Success Criteria**:
- [ ] Server starts without errors
- [ ] Health endpoint returns 200 OK
- [ ] No crashes during startup
- [ ] Logs show successful initialization

---

#### Smoke Test 2: Basic Tool Registration
```bash
uv run python -c "
from src.agent.agent import get_agent

agent = get_agent()
print('Agent initialized')

# Verify folder_manage tool registered
tools = agent.list_tools()
assert 'obsidian_folder_manage' in [t.name for t in tools]
print('Tool registration verified')
"
```

**Success Criteria**:
- [ ] Agent initializes
- [ ] obsidian_folder_manage tool registered
- [ ] No import errors
- [ ] Configuration loads correctly

---

#### Smoke Test 3: Basic Operation Test
```bash
uv run pytest tests/tools/obsidian_folder_manager/test_service.py::TestCreateFolderOperation::test_create_simple_folder -v
```

**Success Criteria**:
- [ ] Test passes
- [ ] Folder created successfully
- [ ] No runtime errors
- [ ] Logs show expected behavior

---

### 1.3 Local Environment Teardown

```bash
# Stop any running services
pkill -f uvicorn

# Clean up test data
rm -rf /tmp/test-vault-*

# Verify no processes left
ps aux | grep uvicorn
```

**Success Criteria**:
- [ ] All services stopped cleanly
- [ ] No zombie processes
- [ ] Test data cleaned up
- [ ] Ready for next stage

---

## Stage 2: Staging Environment Validation

### 2.1 Staging Deployment

**Environment**: Staging server (identical to production)

#### Deploy to Staging
```bash
# SSH to staging server
ssh staging-server

# Pull latest code
cd /app/obsidian-agent
git fetch origin
git checkout claude/review-agent-core-01E8UdzqkJNLQKTxMGeeR8rK
git pull origin claude/review-agent-core-01E8UdzqkJNLQKTxMGeeR8rK

# Install dependencies
uv sync

# Run pre-deployment validation
uv run ruff check src/tools/obsidian_folder_manager/
uv run mypy src/tools/obsidian_folder_manager/ --strict
uv run pytest tests/tools/obsidian_folder_manager/ -v -m unit

# Restart service
sudo systemctl restart obsidian-agent

# Check service status
sudo systemctl status obsidian-agent
```

**Success Criteria**:
- [ ] Code deployed successfully
- [ ] Dependencies installed
- [ ] Service restarted cleanly
- [ ] Service running and healthy

---

### 2.2 Staging Smoke Tests

#### Smoke Test 1: Health Check
```bash
curl https://staging.example.com/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "version": "0.3.0",
  "timestamp": "2025-01-22T10:30:00Z"
}
```

---

#### Smoke Test 2: Tool Availability
```bash
curl https://staging.example.com/api/agent/tools
```

**Expected Response**:
```json
{
  "tools": [
    "obsidian_folder_manage",
    "obsidian_note_manage",
    "obsidian_vault_query",
    "obsidian_graph_analyze",
    ...
  ]
}
```

**Validation**:
- [ ] obsidian_folder_manage present
- [ ] All expected tools listed
- [ ] Response time <500ms

---

### 2.3 Staging Integration Tests

#### Test 1: Create Folder Operation
```bash
curl -X POST https://staging.example.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "obsidian_folder_manage",
    "parameters": {
      "path": "test-staging-folder",
      "operation": "create"
    }
  }'
```

**Success Criteria**:
- [ ] 200 OK response
- [ ] Folder created
- [ ] Correct response format
- [ ] Logs show successful operation

---

#### Test 2: Archive Operation
```bash
# First, create a folder with a note
curl -X POST https://staging.example.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "obsidian_folder_manage",
    "parameters": {
      "path": "test-archive-folder",
      "operation": "create"
    }
  }'

# Archive it
curl -X POST https://staging.example.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "obsidian_folder_manage",
    "parameters": {
      "path": "test-archive-folder",
      "operation": "archive"
    }
  }'
```

**Success Criteria**:
- [ ] Archive succeeds
- [ ] Folder moved to archive/YYYY-MM-DD/
- [ ] Response includes archive path
- [ ] Operation logged correctly

---

#### Test 3: Path Validation (Security Test)
```bash
# Try malicious path - should be rejected
curl -X POST https://staging.example.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "obsidian_folder_manage",
    "parameters": {
      "path": "../../../etc/passwd",
      "operation": "create"
    }
  }'
```

**Expected**: 400 Bad Request with helpful error

**Success Criteria**:
- [ ] Request rejected
- [ ] Error message says "invalid path"
- [ ] No server crash
- [ ] Security validation working

---

### 2.4 Staging Performance Tests

#### Test 1: Archive Performance
```bash
# Create test folder with 25 notes
for i in {1..25}; do
  curl -X POST https://staging.example.com/api/agent/execute \
    -H "Content-Type: application/json" \
    -d "{
      \"tool\": \"obsidian_note_manage\",
      \"parameters\": {
        \"path\": \"perf-test-folder/note-$i.md\",
        \"operation\": \"create\",
        \"content\": \"Test note $i\"
      }
    }"
done

# Time the archive operation
time curl -X POST https://staging.example.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "obsidian_folder_manage",
    "parameters": {
      "path": "perf-test-folder",
      "operation": "archive"
    }
  }'
```

**Success Criteria**:
- [ ] Archive completes <500ms
- [ ] All 25 notes archived
- [ ] Response time acceptable
- [ ] No performance degradation

---

### 2.5 Staging Rollback Test

**Purpose**: Verify we can roll back deployment if issues found.

```bash
# Tag current version
git tag staging-backup-$(date +%Y%m%d-%H%M%S)

# Simulate rollback
git checkout main
uv sync
sudo systemctl restart obsidian-agent

# Verify service running
curl https://staging.example.com/health

# Return to new version
git checkout claude/review-agent-core-01E8UdzqkJNLQKTxMGeeR8rK
uv sync
sudo systemctl restart obsidian-agent
```

**Success Criteria**:
- [ ] Rollback completes successfully
- [ ] Service runs on old version
- [ ] Can successfully roll forward
- [ ] No data corruption

---

## Stage 3: Canary Deployment

### 3.1 Canary Strategy

**Purpose**: Deploy to small subset of production users to detect issues early.

**Configuration**:
- 5% of production traffic → new version
- 95% of production traffic → current version
- Monitor for 24 hours before full rollout

---

### 3.2 Canary Deployment Process

```bash
# Deploy to canary servers
for server in canary-1.prod.example.com canary-2.prod.example.com; do
  ssh $server <<EOF
    cd /app/obsidian-agent
    git fetch origin
    git checkout claude/review-agent-core-01E8UdzqkJNLQKTxMGeeR8rK
    uv sync
    sudo systemctl restart obsidian-agent
    sudo systemctl status obsidian-agent
EOF
done

# Update load balancer to route 5% to canary
# (Configuration depends on your load balancer)
```

---

### 3.3 Canary Validation Tests

#### Test 1: Canary Health Check
```bash
# Check health of canary servers
for server in canary-1.prod.example.com canary-2.prod.example.com; do
  curl https://$server/health
done
```

**Success Criteria**:
- [ ] Both canary servers healthy
- [ ] Response time <100ms
- [ ] No errors in logs

---

#### Test 2: Canary Traffic Monitoring

**Monitor for 24 hours**:
```bash
# Check error rate
curl https://metrics.example.com/api/error-rate?service=obsidian-agent&deployment=canary

# Check latency
curl https://metrics.example.com/api/latency?service=obsidian-agent&deployment=canary&percentile=p95

# Check success rate
curl https://metrics.example.com/api/success-rate?service=obsidian-agent&deployment=canary
```

**Success Criteria**:
- [ ] Error rate <1% (same as baseline)
- [ ] P95 latency <500ms for archive ops
- [ ] Success rate >99%
- [ ] No increase in error rate vs baseline

---

#### Test 3: Canary User Feedback

**Monitor user reports**:
- [ ] No user complaints about folder operations
- [ ] No reports of tool confusion
- [ ] No reports of broken wikilinks
- [ ] No reports of performance issues

---

### 3.4 Canary Go/No-Go Decision

**After 24 hours, evaluate**:

**GO Criteria** (proceed to full rollout):
- ✅ All canary tests passing
- ✅ Error rate <1%
- ✅ No critical bugs reported
- ✅ Performance acceptable
- ✅ No user complaints

**NO-GO Criteria** (rollback canary):
- ❌ Error rate >2%
- ❌ Critical bug discovered
- ❌ Performance degradation
- ❌ User complaints
- ❌ Any security issue

**Rollback Canary** (if NO-GO):
```bash
# Rollback canary servers
for server in canary-1.prod.example.com canary-2.prod.example.com; do
  ssh $server <<EOF
    cd /app/obsidian-agent
    git checkout main
    uv sync
    sudo systemctl restart obsidian-agent
EOF
done

# Remove canary from load balancer routing
```

---

## Stage 4: Full Production Deployment

### 4.1 Production Deployment Plan

**Strategy**: Rolling deployment with validation at each step.

**Phases**:
1. Deploy to 25% of production servers
2. Monitor for 4 hours
3. Deploy to 50% of production servers
4. Monitor for 2 hours
5. Deploy to 100% of production servers
6. Monitor for 24 hours

---

### 4.2 Production Deployment Execution

#### Phase 1: 25% Rollout
```bash
# Deploy to first 25% of servers
SERVERS=$(cat production-servers.txt | head -n 10)  # Assuming 40 total servers

for server in $SERVERS; do
  echo "Deploying to $server..."
  ssh $server <<EOF
    cd /app/obsidian-agent
    git fetch origin
    git checkout claude/review-agent-core-01E8UdzqkJNLQKTxMGeeR8rK
    uv sync
    uv run pytest tests/tools/obsidian_folder_manager/ -v -m unit --maxfail=1
    sudo systemctl restart obsidian-agent
    sudo systemctl status obsidian-agent
EOF

  # Verify health
  curl https://$server/health || echo "⚠️  WARNING: $server unhealthy"

  sleep 10  # Stagger deployments
done

echo "✅ 25% deployment complete. Monitoring for 4 hours..."
```

**Monitoring During 4-Hour Window**:
```bash
# Check metrics every 15 minutes
watch -n 900 '
  echo "=== Error Rate ==="
  curl -s https://metrics.example.com/api/error-rate?service=obsidian-agent
  echo ""
  echo "=== P95 Latency ==="
  curl -s https://metrics.example.com/api/latency?service=obsidian-agent&percentile=p95
  echo ""
  echo "=== Success Rate ==="
  curl -s https://metrics.example.com/api/success-rate?service=obsidian-agent
'
```

**Success Criteria for 25%**:
- [ ] All deployed servers healthy
- [ ] Error rate <1%
- [ ] No spike in latency
- [ ] No user complaints
- [ ] Can proceed to 50%

**Rollback Trigger for 25%**:
- ❌ Error rate >2%
- ❌ Any server unhealthy
- ❌ Latency spike >2x baseline
- ❌ Critical bug reported

---

#### Phase 2: 50% Rollout

**Same process as Phase 1**, but:
- Deploy to next 10 servers (total: 20/40 = 50%)
- Monitor for 2 hours (shorter window since 25% already validated)
- Same success/rollback criteria

---

#### Phase 3: 100% Rollout

**Deploy to remaining 20 servers**:
- Same process
- Monitor for 24 hours after complete
- Enable post-deployment monitoring

---

### 4.3 Production Smoke Tests

**Run after each rollout phase**:

#### Smoke Test 1: Critical Path Operations
```bash
# Test folder create
curl -X POST https://api.prod.example.com/agent/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{
    "tool": "obsidian_folder_manage",
    "parameters": {"path": "smoke-test-$(date +%s)", "operation": "create"}
  }'

# Test folder archive
curl -X POST https://api.prod.example.com/agent/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{
    "tool": "obsidian_folder_manage",
    "parameters": {"path": "smoke-test-folder", "operation": "archive"}
  }'
```

**Success**: Both operations complete with 200 OK

---

#### Smoke Test 2: Tool Selection Validation
```bash
# Agent should select correct tool for folder operation
curl -X POST https://api.prod.example.com/agent/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{
    "message": "Create a new folder called test-projects"
  }'
```

**Success**: Agent uses obsidian_folder_manage (not note_manage)

---

### 4.4 Production Rollback Procedure

**If issues detected during deployment**:

```bash
#!/bin/bash
# rollback-production.sh

echo "🚨 INITIATING PRODUCTION ROLLBACK"

# Notify team
curl -X POST https://slack.example.com/webhook \
  -d '{"text": "🚨 Production rollback initiated for obsidian-agent"}'

# Rollback all servers to main branch
ALL_SERVERS=$(cat production-servers.txt)

for server in $ALL_SERVERS; do
  echo "Rolling back $server..."
  ssh $server <<EOF
    cd /app/obsidian-agent
    git checkout main
    uv sync
    sudo systemctl restart obsidian-agent
EOF

  # Verify health
  curl https://$server/health || echo "⚠️  WARNING: $server unhealthy after rollback"
done

echo "✅ Rollback complete. Verifying production health..."

# Run smoke tests
./smoke-tests-production.sh

echo "📊 Rollback verification complete. Check metrics dashboard."
```

**Rollback Success Criteria**:
- [ ] All servers back on main branch
- [ ] All servers healthy
- [ ] Error rate back to baseline
- [ ] Smoke tests passing
- [ ] No further user complaints

---

## Deployment Validation Checklist

### Pre-Flight Checklist
- [ ] All pre-deployment validations passed
- [ ] Staging environment tested
- [ ] Rollback procedure documented
- [ ] Team notified of deployment window
- [ ] Monitoring dashboards prepared
- [ ] On-call engineer available

### Stage 1: Local/Dev
- [ ] Clean build successful
- [ ] Package installs correctly
- [ ] Local smoke tests pass
- [ ] Environment cleaned up

### Stage 2: Staging
- [ ] Deployed to staging
- [ ] Staging smoke tests pass
- [ ] Integration tests pass
- [ ] Performance tests pass
- [ ] Rollback test successful

### Stage 3: Canary
- [ ] Canary deployment successful
- [ ] 5% traffic routing configured
- [ ] 24-hour monitoring clean
- [ ] No increase in errors
- [ ] Go decision made

### Stage 4: Production
- [ ] Phase 1 (25%) deployed
- [ ] 4-hour monitoring clean
- [ ] Phase 2 (50%) deployed
- [ ] 2-hour monitoring clean
- [ ] Phase 3 (100%) deployed
- [ ] 24-hour monitoring clean
- [ ] Smoke tests passing
- [ ] Post-deployment validation started

---

## Deployment Metrics & Monitoring

### Key Metrics to Track

**During Deployment**:
- Server health (up/down)
- Deployment success rate
- Rollback frequency
- Deployment duration

**After Deployment**:
- Request error rate
- Request latency (p50, p95, p99)
- Tool selection accuracy
- Archive operation success rate
- Wikilink update success rate

### Alerting Thresholds

**Critical Alerts** (page immediately):
- Error rate >5%
- Any server unresponsive >5 minutes
- Archive operation failure rate >10%
- Security validation failure

**Warning Alerts** (notify team):
- Error rate >2%
- Latency p95 >1s for archive ops
- Tool selection accuracy <90%

---

## Deployment Timeline

**Total Duration**: 3-4 days

| Stage | Duration | Activity |
|-------|----------|----------|
| Pre-Deployment | 1-2 hours | All pre-deployment validations |
| Stage 1: Local | 30 minutes | Build, package, smoke tests |
| Stage 2: Staging | 4 hours | Deploy, test, validate |
| Stage 3: Canary | 24 hours | 5% traffic monitoring |
| Stage 4: Prod 25% | 4 hours | Deploy + monitor |
| Stage 4: Prod 50% | 2 hours | Deploy + monitor |
| Stage 4: Prod 100% | 24 hours | Deploy + monitor |
| Post-Deployment | Ongoing | Continuous monitoring |

**Total**: ~60 hours (2.5 days) from start to full production

---

## Emergency Procedures

### Emergency Rollback
**Trigger**: Critical bug in production

```bash
# Immediate rollback of all servers
./rollback-production.sh --emergency

# Disable new feature via feature flag (if implemented)
curl -X POST https://config.example.com/api/feature-flags \
  -d '{"folder_manage_archive": false}'
```

### Emergency Hotfix
**Trigger**: Critical security issue

1. Fix on emergency branch
2. Deploy directly to production (skip canary)
3. Run smoke tests only
4. Monitor closely
5. Follow up with full validation

---

## Communication Plan

### Deployment Announcement
**Send 24 hours before deployment**:
```
Subject: Obsidian Agent Deployment - Folder Management Enhancement

Team,

We will be deploying the folder management enhancement feature:
- Start: [DATE] at [TIME]
- Duration: ~60 hours (staged rollout)
- Impact: Minimal (rolling deployment)

Features:
- Enhanced tool separation
- Archive operation with auto-dating
- Improved error messages

On-call: [NAME]
Rollback procedure: [LINK]

Questions? Reply to this thread.
```

### Deployment Status Updates
**During deployment, every 4 hours**:
```
Deployment Status Update - [TIMESTAMP]

✅ Stage 1: Local/Dev - Complete
✅ Stage 2: Staging - Complete
🔄 Stage 3: Canary - In Progress (12/24 hours)
⏸️  Stage 4: Production - Waiting

Metrics:
- Error rate: 0.3% (baseline: 0.4%)
- P95 latency: 245ms (baseline: 250ms)
- Tool selection: 97% accuracy (target: >95%)

No issues detected. Proceeding as planned.
```

---

## Success Criteria Summary

**Deployment considered successful when**:
- ✅ All stages completed without rollback
- ✅ Production error rate <1%
- ✅ All smoke tests passing
- ✅ No critical bugs reported
- ✅ Performance within acceptable range
- ✅ User acceptance in post-deployment validation
- ✅ 24-hour production monitoring clean

---

**Version**: 1.0
**Last Updated**: 2025-01-22
**Owner**: Development Team
