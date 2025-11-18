---
type: dropoff_alert
created: {{TIMESTAMP}}
alert_id: {{ALERT_ID}}
tags:
  - customer-journey
  - alert
  - dropoff
  - {{SEVERITY}}
status: {{ALERT_STATUS}}
severity: {{SEVERITY}}
funnel_id: {{FUNNEL_ID}}
step_number: {{STEP_NUMBER}}
dropoff_rate: {{CURRENT_DROPOFF_RATE}}
deviation: {{DEVIATION_PERCENTAGE}}
affected_users: {{AFFECTED_USERS_COUNT}}
related_funnel: "[[customer_journeys/funnel_analysis/{{FUNNEL_ID}}]]"
---

# Drop-off Alert: {{STEP_NAME}}

> [!{{SEVERITY_CALLOUT}}] {{SEVERITY_LABEL}} Alert
> **Alert ID:** {{ALERT_ID}}
> **Triggered:** {{TIMESTAMP}}
> **Severity:** {{SEVERITY_LABEL}}

---

## Alert Summary

**{{ALERT_SUMMARY}}**

---

## Critical Metrics

| Metric | Value |
|--------|-------|
| **Affected Funnel** | [[customer_journeys/funnel_analysis/{{FUNNEL_ID}}|{{FUNNEL_NAME}}]] |
| **Problem Step** | Step {{STEP_NUMBER}}: {{STEP_NAME}} |
| **Current Drop-off Rate** | {{CURRENT_DROPOFF_RATE}}% |
| **Baseline Drop-off Rate** | {{BASELINE_DROPOFF_RATE}}% |
| **Deviation** | +{{DEVIATION_PERCENTAGE}}% |
| **Affected Users** | {{AFFECTED_USERS_COUNT}} users |
| **Time Window** | Last {{TIME_WINDOW}} hours |

---

## Visual Comparison

### Before vs After

```mermaid
graph LR
    subgraph Baseline
    A1[Users: 1000] --> B1[Step {{STEP_NUMBER}}: {{BASELINE_COMPLETION}}]
    B1 --> C1[Completed: {{BASELINE_COMPLETED}}]
    end

    subgraph Current
    A2[Users: 1000] --> B2[Step {{STEP_NUMBER}}: {{CURRENT_COMPLETION}}]
    B2 --> C2[Completed: {{CURRENT_COMPLETED}}]
    end

    style B2 fill:#FFB6C1
    style C2 fill:#FFB6C1
```

### Drop-off Trend

{{DROPOFF_TREND_CHART}}

---

## Root Cause Analysis

### Primary Causes (AI-Detected)

{{#each POTENTIAL_REASONS}}
{{this.rank}}. **{{this.reason}}** ({{this.confidence}}% confidence)

**Evidence:**
{{#each this.evidence}}
- {{this}}
{{/each}}

**Impact:** {{this.impact}}

{{/each}}

### Supporting Data

#### Rage Clicks

{{#if RAGE_CLICKS}}
> [!warning] User Frustration Detected
> **Rage click events:** {{RAGE_CLICK_COUNT}}
> **Affected elements:**
{{#each RAGE_CLICK_ELEMENTS}}
> - `{{this.selector}}` ({{this.count}}x) - "{{this.text}}"
{{/each}}
{{else}}
✅ No significant rage clicks detected.
{{/if}}

#### Form Errors

{{#if FORM_ERRORS}}
> [!alert] Form Validation Issues
> **Total errors:** {{FORM_ERROR_COUNT}}
> **Most common errors:**
{{#each TOP_FORM_ERRORS}}
> - {{this.error_type}}: {{this.count}}x ({{this.field}})
{{/each}}

**Sample error messages:**
{{#each SAMPLE_ERROR_MESSAGES}}
> - "{{this}}"
{{/each}}
{{else}}
✅ No unusual form errors detected.
{{/if}}

#### Performance Issues

{{#if PERFORMANCE_ISSUES}}
> [!warning] Page Performance Problems
> **Avg load time:** {{AVG_LOAD_TIME}}ms (baseline: {{BASELINE_LOAD_TIME}}ms)
> **Slowest resources:**
{{#each SLOW_RESOURCES}}
> - {{this.resource}}: {{this.load_time}}ms
{{/each}}
{{else}}
✅ No performance degradation detected.
{{/if}}

#### JavaScript Errors

{{#if JS_ERRORS}}
> [!alert] Client-Side Errors
> **Error count:** {{JS_ERROR_COUNT}}
> **Top errors:**
{{#each TOP_JS_ERRORS}}
> - `{{this.error}}` ({{this.count}}x)
>   - Stack: {{this.stack_preview}}
{{/each}}
{{else}}
✅ No JavaScript errors detected.
{{/if}}

---

## Affected User Segments

### Segment Breakdown

| Segment | Affected Users | Drop-off Rate | Baseline Rate | Deviation |
|---------|----------------|---------------|---------------|-----------|
{{#each AFFECTED_SEGMENTS}}
| {{this.segment_name}} | {{this.affected_count}} | {{this.current_rate}}% | {{this.baseline_rate}}% | +{{this.deviation}}% |
{{/each}}

### Most Impacted Segment

> [!warning] {{MOST_IMPACTED_SEGMENT}} Most Affected
> **Current drop-off:** {{MOST_IMPACTED_RATE}}%
> **Baseline:** {{MOST_IMPACTED_BASELINE}}%
> **Deviation:** +{{MOST_IMPACTED_DEVIATION}}%
>
> **Segment characteristics:**
{{#each MOST_IMPACTED_CHARACTERISTICS}}
> - {{this}}
{{/each}}

---

## Revenue Impact

### Estimated Loss

| Metric | Value |
|--------|-------|
| **Lost Conversions** | {{LOST_CONVERSIONS}} orders |
| **Estimated Revenue Loss** | ${{ESTIMATED_REVENUE_LOSS}} |
| **Loss per Hour** | ${{LOSS_PER_HOUR}} |
| **Projected Daily Loss** | ${{PROJECTED_DAILY_LOSS}} |

{{#if HIGH_REVENUE_IMPACT}}
> [!danger] High Revenue Impact
> If this issue persists for 24 hours, estimated loss: **${{PROJECTED_DAILY_LOSS}}**
> **Immediate action required!**
{{/if}}

---

## Affected Customer Examples

### Sample Abandoned Sessions

{{#each SAMPLE_SESSIONS}}
#### [[customer_journeys/customer_profiles/customer_{{this.customer_id}}|Customer #{{this.customer_id}}]]

- **Cart Value:** ${{this.cart_value}}
- **Session Start:** {{this.session_start}}
- **Abandoned At:** {{this.abandoned_at}}
- **Time on Step:** {{this.time_on_step}}
- **Device:** {{this.device_type}}

**Journey Path:**
```
{{this.journey_path}}
```

**Abandonment Trigger:** {{this.trigger}}

{{#if this.recovery_possible}}
> [!tip] Recovery Opportunity
> {{this.recovery_suggestion}}
{{/if}}

---

{{/each}}

---

## Immediate Actions Required

### Critical (Do Now)

{{#each CRITICAL_ACTIONS}}
- [ ] **{{this.action}}**
  - Owner: {{this.owner}}
  - Deadline: {{this.deadline}}
  - Impact: {{this.impact}}
  - Steps:
{{#each this.steps}}
    - {{this}}
{{/each}}
{{/each}}

### High Priority (Today)

{{#each HIGH_PRIORITY_ACTIONS}}
- [ ] **{{this.action}}**
  - Expected result: {{this.expected_result}}
  - Time required: {{this.time_required}}
{{/each}}

### Investigation Needed

{{#each INVESTIGATION_TASKS}}
- [ ] **{{this.task}}**
  - Tools needed: {{this.tools}}
  - Questions to answer: {{this.questions}}
{{/each}}

---

## Recommended Fixes

{{#each RECOMMENDED_FIXES}}
### {{this.priority}}: {{this.fix_title}}

**Problem:** {{this.problem}}

**Solution:** {{this.solution}}

**Implementation:**
```{{this.code_language}}
{{this.code_example}}
```

**Expected Impact:** {{this.expected_impact}}

**Effort:** {{this.effort}} ({{this.time_estimate}})

**Rollback Plan:** {{this.rollback_plan}}

---

{{/each}}

---

## Historical Context

### Similar Past Incidents

{{#if PAST_INCIDENTS}}

{{#each PAST_INCIDENTS}}
#### [[customer_journeys/dropoff_alerts/{{this.filename}}|{{this.date}} - {{this.title}}]]

- **Severity:** {{this.severity}}
- **Cause:** {{this.cause}}
- **Resolution:** {{this.resolution}}
- **Time to resolve:** {{this.time_to_resolve}}

**Lessons learned:** {{this.lessons}}

---

{{/each}}

{{else}}

> [!note] First Occurrence
> This is the first time this specific drop-off pattern has been detected.

{{/if}}

---

## Alert Timeline

{{#each ALERT_TIMELINE}}
- **{{this.timestamp}}:** {{this.event}}
{{/each}}

---

## Monitoring & Next Steps

### What to Monitor

- [ ] Drop-off rate for Step {{STEP_NUMBER}} (target: < {{TARGET_DROPOFF_RATE}}%)
- [ ] Rage click frequency (target: < {{TARGET_RAGE_CLICKS}} per hour)
- [ ] Form error rate (target: < {{TARGET_ERROR_RATE}}%)
- [ ] Page load time (target: < {{TARGET_LOAD_TIME}}ms)
- [ ] Revenue impact (current: -${{CURRENT_REVENUE_IMPACT}}/hour)

### Success Criteria

This alert can be closed when:
{{#each SUCCESS_CRITERIA}}
- {{this}}
{{/each}}

### Escalation Path

{{#if ESCALATION_NEEDED}}
> [!warning] Escalation Required
> **Escalate to:** {{ESCALATION_TO}}
> **If not resolved by:** {{ESCALATION_DEADLINE}}
> **Contact:** {{ESCALATION_CONTACT}}
{{/if}}

---

## Related Resources

### Documentation
{{#each RELATED_DOCS}}
- {{this}}
{{/each}}

### Team Contacts
- **Product Owner:** {{PRODUCT_OWNER}}
- **Engineering Lead:** {{ENGINEERING_LEAD}}
- **UX Designer:** {{UX_DESIGNER}}
- **On-Call:** {{ONCALL_ENGINEER}}

### External Resources
{{#each EXTERNAL_RESOURCES}}
- [{{this.title}}]({{this.url}})
{{/each}}

---

## Communication Log

### Notifications Sent

{{#each NOTIFICATIONS}}
- **{{this.timestamp}}:** {{this.channel}} - {{this.recipients}}
  - Message: {{this.message}}
{{/each}}

### Comments & Updates

{{#each COMMENTS}}
---

**{{this.timestamp}}** - {{this.author}}

{{this.comment}}

{{/each}}

---

## Resolution

{{#if RESOLVED}}

### Resolution Summary

> [!success] Alert Resolved
> **Resolved At:** {{RESOLVED_AT}}
> **Resolution Time:** {{RESOLUTION_DURATION}}
> **Resolved By:** {{RESOLVED_BY}}

**Root Cause:** {{ROOT_CAUSE}}

**Fix Applied:** {{FIX_APPLIED}}

**Outcome:**
- Drop-off rate: {{FINAL_DROPOFF_RATE}}% (target: < {{TARGET_DROPOFF_RATE}}%)
- Users recovered: {{USERS_RECOVERED}}
- Revenue recovered: ${{REVENUE_RECOVERED}}

**Post-Mortem:** [[customer_journeys/post_mortems/{{POST_MORTEM_FILE}}|View Post-Mortem]]

{{else}}

> [!note] Alert Status: {{ALERT_STATUS}}
> **Open since:** {{TIMESTAMP}}
> **Elapsed time:** {{ELAPSED_TIME}}

{{/if}}

---

## Metadata

| Attribute | Value |
|-----------|-------|
| **Alert ID** | {{ALERT_ID}} |
| **Created** | {{TIMESTAMP}} |
| **Last Updated** | {{LAST_UPDATED}} |
| **Status** | {{ALERT_STATUS}} |
| **Severity** | {{SEVERITY}} |
| **Assignee** | {{ASSIGNEE}} |
| **Tags** | {{TAGS}} |

---

**Alert Generated by Customer Journey Analysis Tool**
*Powered by Pydantic AI + FastAPI*

---

## Navigation

[[customer_journeys/_index|Journey Index]] | [[customer_journeys/dropoff_alerts/|All Alerts]] | [[customer_journeys/funnel_analysis/{{FUNNEL_ID}}|Related Funnel]]
