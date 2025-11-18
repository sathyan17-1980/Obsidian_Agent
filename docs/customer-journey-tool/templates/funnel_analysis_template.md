---
type: funnel_analysis
created: {{CREATED_TIMESTAMP}}
updated: {{UPDATED_TIMESTAMP}}
funnel_id: {{FUNNEL_ID}}
funnel_name: {{FUNNEL_NAME}}
tags:
  - customer-journey
  - funnel-analysis
  - conversion
status: published
analysis_start: {{ANALYSIS_START}}
analysis_end: {{ANALYSIS_END}}
total_entries: {{TOTAL_ENTRIES}}
total_completions: {{TOTAL_COMPLETIONS}}
conversion_rate: {{CONVERSION_RATE}}
---

# Funnel Analysis: {{FUNNEL_NAME}}

> [!info] Analysis Overview
> **Funnel:** {{FUNNEL_NAME}}
> **Period:** {{ANALYSIS_START}} to {{ANALYSIS_END}}
> **Status:** {{FUNNEL_STATUS}}

---

## Executive Summary

**{{SUMMARY_TEXT}}**

### Key Metrics

| Metric | Value |
|--------|-------|
| **Total Entries** | {{TOTAL_ENTRIES}} users |
| **Total Completions** | {{TOTAL_COMPLETIONS}} users |
| **Overall Conversion Rate** | {{CONVERSION_RATE}}% |
| **Avg Time to Convert** | {{AVG_TIME_TO_CONVERT}} |
| **Revenue Generated** | ${{REVENUE_GENERATED}} |

{{#if CONVERSION_TREND}}
**Trend:** {{CONVERSION_TREND_DIRECTION}} ({{CONVERSION_TREND_CHANGE}} vs previous period)
{{/if}}

---

## Funnel Visualization

### Step-by-Step Flow

```mermaid
graph TD
{{FUNNEL_MERMAID_DIAGRAM}}
```

### Conversion Funnel (Waterfall)

```mermaid
graph LR
{{WATERFALL_DIAGRAM}}
```

---

## Step-by-Step Analysis

{{#each STEPS}}

### Step {{this.step_number}}: {{this.step_name}}

**URL Pattern:** `{{this.url_pattern}}`

#### Metrics

| Metric | Value |
|--------|-------|
| **Users Entered** | {{this.entered_count}} |
| **Users Completed** | {{this.completed_count}} |
| **Users Abandoned** | {{this.abandoned_count}} |
| **Completion Rate** | {{this.completion_rate}}% |
| **Drop-off Rate** | {{this.drop_off_rate}}% |
| **Avg Time on Step** | {{this.avg_time}} |
| **Median Time on Step** | {{this.median_time}} |

#### Performance Assessment

{{#if this.is_problematic}}
> [!warning] Performance Issue Detected
> **Drop-off Rate:** {{this.drop_off_rate}}% ({{this.vs_baseline}})
>
> **Problem Severity:** {{this.severity}}
>
> **Impact:** {{this.impact_description}}
{{else}}
> [!success] Step Performing Well
> Drop-off rate ({{this.drop_off_rate}}%) is within acceptable range.
{{/if}}

#### Time Distribution

{{this.time_distribution_chart}}

#### Drop-off Reasons

{{#each this.dropoff_reasons}}
{{this.rank}}. **{{this.reason}}** ({{this.percentage}}% of abandonments)
   - Affected users: {{this.count}}
   - Evidence: {{this.evidence}}
{{/each}}

#### User Segments Performance

| Segment | Entered | Completed | Conv Rate | Drop-off Rate |
|---------|---------|-----------|-----------|---------------|
{{#each this.segment_performance}}
| {{this.segment_name}} | {{this.entered}} | {{this.completed}} | {{this.conv_rate}}% | {{this.dropoff_rate}}% |
{{/each}}

{{#if this.segment_insight}}
**Insight:** {{this.segment_insight}}
{{/if}}

#### Optimization Recommendations

{{#each this.recommendations}}
- [ ] **{{this.title}}**
  - Priority: {{this.priority}}
  - Expected Impact: {{this.impact}}
  - Implementation Effort: {{this.effort}}
  - Details: {{this.details}}
{{/each}}

---

{{/each}}

---

## Drop-off Analysis

### Overall Drop-off Distribution

{{DROPOFF_PIE_CHART}}

### Critical Drop-off Points

{{#each CRITICAL_DROPOFF_POINTS}}

#### {{this.rank}}. {{this.step_name}} ({{this.drop_off_rate}}% drop-off)

> [!alert] Critical Drop-off
> **Users Lost:** {{this.users_lost}}
> **Revenue Impact:** ${{this.revenue_impact}} (estimated)
>
> **Primary Causes:**
{{#each this.causes}}
> - {{this}}
{{/each}}
>
> **Immediate Actions Required:**
{{#each this.actions}}
> - [ ] {{this}}
{{/each}}

{{/each}}

---

## Time-Based Analysis

### Conversion Time Distribution

{{CONVERSION_TIME_CHART}}

| Time to Convert | Users | Percentage |
|-----------------|-------|------------|
| **< 5 minutes** | {{CONV_UNDER_5}} | {{CONV_UNDER_5_PCT}}% |
| **5-30 minutes** | {{CONV_5_30}} | {{CONV_5_30_PCT}}% |
| **30 min - 1 hour** | {{CONV_30_60}} | {{CONV_30_60_PCT}}% |
| **1-24 hours** | {{CONV_1_24}} | {{CONV_1_24_PCT}}% |
| **1+ days** | {{CONV_1_PLUS}} | {{CONV_1_PLUS_PCT}}% |

**Median Time to Convert:** {{MEDIAN_TIME_TO_CONVERT}}

{{#if DELAYED_CONVERSION_INSIGHT}}
> [!tip] Delayed Conversion Pattern
> {{DELAYED_CONVERSION_INSIGHT}}
{{/if}}

### Hourly Performance

| Hour (UTC) | Entries | Conversions | Conv Rate |
|------------|---------|-------------|-----------|
{{HOURLY_PERFORMANCE_TABLE}}

**Best Performing Hours:** {{BEST_HOURS}}
**Worst Performing Hours:** {{WORST_HOURS}}

### Daily Performance Trend

{{DAILY_TREND_CHART}}

---

## Segment Comparison

### By Device Type

| Device | Entries | Conv Rate | Drop-off Rate | Avg Time |
|--------|---------|-----------|---------------|----------|
| Desktop | {{DESKTOP_ENTRIES}} | {{DESKTOP_CONV}}% | {{DESKTOP_DROPOFF}}% | {{DESKTOP_TIME}} |
| Mobile | {{MOBILE_ENTRIES}} | {{MOBILE_CONV}}% | {{MOBILE_DROPOFF}}% | {{MOBILE_TIME}} |
| Tablet | {{TABLET_ENTRIES}} | {{TABLET_CONV}}% | {{TABLET_DROPOFF}}% | {{TABLET_TIME}} |

{{#if DEVICE_DISPARITY}}
> [!warning] Device Performance Disparity
> {{DEVICE_DISPARITY_TEXT}}
>
> **Recommendation:** {{DEVICE_RECOMMENDATION}}
{{/if}}

### By Traffic Source

| Source | Entries | Conv Rate | Avg Order Value | Total Revenue |
|--------|---------|-----------|-----------------|---------------|
{{TRAFFIC_SOURCE_TABLE}}

**Best Performing Source:** {{BEST_SOURCE}}
**Worst Performing Source:** {{WORST_SOURCE}}

### By Customer Type

| Type | Entries | Conv Rate | Drop-off Rate | Notes |
|------|---------|-----------|---------------|-------|
| New Visitors | {{NEW_ENTRIES}} | {{NEW_CONV}}% | {{NEW_DROPOFF}}% | {{NEW_NOTES}} |
| Returning Customers | {{RET_ENTRIES}} | {{RET_CONV}}% | {{RET_DROPOFF}}% | {{RET_NOTES}} |
| High-Value Customers | {{HV_ENTRIES}} | {{HV_CONV}}% | {{HV_DROPOFF}}% | {{HV_NOTES}} |

---

## Success Paths vs Abandonment Paths

### Successful Journey Patterns

{{#each SUCCESS_PATHS}}
{{this.rank}}. **{{this.path_description}}** ({{this.occurrences}}x)

**Path:**
```
{{this.path_detail}}
```

**Characteristics:**
- Avg time: {{this.avg_time}}
- Avg order value: ${{this.avg_order_value}}
- Common attributes: {{this.common_attributes}}

{{/each}}

### Common Abandonment Patterns

{{#each ABANDONMENT_PATHS}}
{{this.rank}}. **Abandoned at {{this.abandonment_point}}** ({{this.occurrences}}x)

**Path Before Abandonment:**
```
{{this.path_detail}}
```

**Abandonment Triggers:**
{{#each this.triggers}}
- {{this}}
{{/each}}

**Recovery Potential:** {{this.recovery_potential}}

{{/each}}

---

## A/B Test Results

{{#if AB_TESTS_ACTIVE}}

{{#each AB_TESTS}}
### Test: {{this.test_name}}

**Hypothesis:** {{this.hypothesis}}

| Variant | Entries | Conversions | Conv Rate | Lift |
|---------|---------|-------------|-----------|------|
| Control (A) | {{this.control_entries}} | {{this.control_conversions}} | {{this.control_rate}}% | - |
| Variant (B) | {{this.variant_entries}} | {{this.variant_conversions}} | {{this.variant_rate}}% | {{this.lift}}% |

**Statistical Significance:** {{this.significance}}
**Winner:** {{this.winner}}

{{#if this.is_significant}}
> [!success] Significant Result
> Variant {{this.winner}} shows {{this.lift}}% improvement ({{this.confidence}}% confidence).
> **Recommendation:** {{this.recommendation}}
{{else}}
> [!note] Inconclusive
> More data needed to reach statistical significance.
{{/if}}

{{/each}}

{{else}}

> [!note] No A/B Tests Running
> Consider setting up A/B tests for steps with high drop-off rates.

{{/if}}

---

## Benchmarking

### Industry Comparison

| Metric | This Funnel | Industry Avg | Performance |
|--------|-------------|--------------|-------------|
| Overall Conv Rate | {{CONVERSION_RATE}}% | {{INDUSTRY_CONV_RATE}}% | {{CONV_PERFORMANCE}} |
| Avg Time to Convert | {{AVG_TIME_TO_CONVERT}} | {{INDUSTRY_AVG_TIME}} | {{TIME_PERFORMANCE}} |
| Drop-off Rate | {{AVG_DROPOFF_RATE}}% | {{INDUSTRY_DROPOFF_RATE}}% | {{DROPOFF_PERFORMANCE}} |

### Historical Comparison

| Period | Conv Rate | Change |
|--------|-----------|--------|
| **Current** | {{CURRENT_CONV_RATE}}% | - |
| Last Week | {{LAST_WEEK_CONV_RATE}}% | {{WEEK_CHANGE}} |
| Last Month | {{LAST_MONTH_CONV_RATE}}% | {{MONTH_CHANGE}} |
| Last Quarter | {{LAST_QUARTER_CONV_RATE}}% | {{QUARTER_CHANGE}} |

---

## Revenue Impact Analysis

### Current Performance

| Metric | Value |
|--------|-------|
| **Revenue Generated** | ${{REVENUE_GENERATED}} |
| **Revenue per Entry** | ${{REVENUE_PER_ENTRY}} |
| **Revenue per Conversion** | ${{REVENUE_PER_CONVERSION}} |

### Opportunity Analysis

{{#each OPPORTUNITIES}}
#### {{this.opportunity_name}}

**Current State:** {{this.current_state}}

**If drop-off at Step {{this.step_number}} reduced by {{this.improvement_percent}}%:**
- Additional conversions: {{this.additional_conversions}}
- Additional revenue: ${{this.additional_revenue}}
- ROI potential: {{this.roi_potential}}

**Implementation cost:** {{this.implementation_cost}}
**Payback period:** {{this.payback_period}}

{{/each}}

---

## Action Plan

### Immediate Actions (This Week)

{{#each IMMEDIATE_ACTIONS}}
- [ ] **{{this.action}}**
  - Owner: {{this.owner}}
  - Impact: {{this.impact}}
  - Effort: {{this.effort}}
  - Deadline: {{this.deadline}}
{{/each}}

### Short-term Improvements (This Month)

{{#each SHORT_TERM_ACTIONS}}
- [ ] **{{this.action}}**
  - Impact: {{this.impact}}
  - Effort: {{this.effort}}
{{/each}}

### Long-term Optimization (This Quarter)

{{#each LONG_TERM_ACTIONS}}
- [ ] **{{this.action}}**
  - Impact: {{this.impact}}
  - Investment required: {{this.investment}}
{{/each}}

---

## Related Reports

### Daily Reports with Funnel Data
{{#each RELATED_DAILY_REPORTS}}
- [[customer_journeys/daily_reports/{{this.filename}}|{{this.date}} Summary]]
{{/each}}

### Related Alerts
{{#each RELATED_ALERTS}}
- [[customer_journeys/dropoff_alerts/{{this.filename}}|{{this.title}}]]
{{/each}}

### Customer Segments
{{#each RELATED_SEGMENTS}}
- [[customer_journeys/segments/{{this.segment_id}}|{{this.segment_name}}]]
{{/each}}

---

## Methodology Notes

### Funnel Definition

{{#each STEP_DEFINITIONS}}
**Step {{this.step_number}}:** {{this.step_name}}
- URL Pattern: `{{this.url_pattern}}`
- Required Event: {{this.required_event}}
- Min Time: {{this.min_time}}
- Max Time: {{this.max_time}}
{{/each}}

### Analysis Parameters

- **Time Range:** {{ANALYSIS_START}} to {{ANALYSIS_END}}
- **Total Days:** {{ANALYSIS_DURATION_DAYS}}
- **Session Timeout:** 30 minutes
- **Attribution Model:** Last-touch
- **Currency:** USD
- **Timezone:** UTC

### Data Quality

| Metric | Value |
|--------|-------|
| Events Analyzed | {{EVENTS_ANALYZED}} |
| Sessions Analyzed | {{SESSIONS_ANALYZED}} |
| Users Analyzed | {{USERS_ANALYZED}} |
| Data Completeness | {{DATA_COMPLETENESS}}% |

{{#if DATA_QUALITY_ISSUES}}
> [!warning] Data Quality Notes
{{#each DATA_QUALITY_ISSUES}}
> - {{this}}
{{/each}}
{{/if}}

---

**Report Generated by Customer Journey Analysis Tool**
*Powered by Pydantic AI + FastAPI*

---

## Navigation

[[customer_journeys/_index|Journey Index]] | [[customer_journeys/funnel_analysis/|All Funnels]]
