---
type: customer_journey_report
report_type: daily_summary
created: {{TIMESTAMP}}
updated: {{TIMESTAMP}}
date: {{DATE}}
tags:
  - customer-journey
  - analytics
  - daily-report
status: published
total_sessions: {{TOTAL_SESSIONS}}
total_conversions: {{TOTAL_CONVERSIONS}}
conversion_rate: {{CONVERSION_RATE}}
related_alerts: {{RELATED_ALERTS_LIST}}
---

# Customer Journey Summary - {{DATE}}

> [!info] Report Generated
> **Date:** {{DATE}}
> **Generated At:** {{TIMESTAMP}}
> **Analysis Period:** Last 24 hours

---

## Executive Summary

**{{SUMMARY_TEXT}}**

### Key Metrics

| Metric | Value | Change |
|--------|-------|--------|
| **Total Sessions** | {{TOTAL_SESSIONS}} | {{SESSION_CHANGE}} |
| **Conversions** | {{TOTAL_CONVERSIONS}} | {{CONVERSION_CHANGE}} |
| **Conversion Rate** | {{CONVERSION_RATE}}% | {{CONV_RATE_CHANGE}} |
| **Avg Session Duration** | {{AVG_SESSION_DURATION}} | {{DURATION_CHANGE}} |
| **Bounce Rate** | {{BOUNCE_RATE}}% | {{BOUNCE_CHANGE}} |
| **Revenue** | ${{TOTAL_REVENUE}} | {{REVENUE_CHANGE}} |

---

## Traffic Overview

### Traffic Sources

```mermaid
pie title Traffic Distribution
    "Organic Search" : {{ORGANIC_COUNT}}
    "Direct" : {{DIRECT_COUNT}}
    "Paid Ads" : {{PAID_COUNT}}
    "Referral" : {{REFERRAL_COUNT}}
    "Social" : {{SOCIAL_COUNT}}
```

| Source | Sessions | Conversions | Conv Rate |
|--------|----------|-------------|-----------|
{{TRAFFIC_SOURCE_TABLE}}

### Device Breakdown

| Device | Sessions | Conv Rate | Avg Time |
|--------|----------|-----------|----------|
| Desktop | {{DESKTOP_SESSIONS}} | {{DESKTOP_CONV_RATE}}% | {{DESKTOP_AVG_TIME}} |
| Mobile | {{MOBILE_SESSIONS}} | {{MOBILE_CONV_RATE}}% | {{MOBILE_AVG_TIME}} |
| Tablet | {{TABLET_SESSIONS}} | {{TABLET_CONV_RATE}}% | {{TABLET_AVG_TIME}} |

{{#if DEVICE_INSIGHT}}
> [!tip] Device Insight
> {{DEVICE_INSIGHT}}
{{/if}}

---

## Customer Journey Flow

### Overall Journey Visualization

```mermaid
graph LR
    A[Entry: {{ENTRY_COUNT}}] --> B[Product Pages: {{PRODUCT_COUNT}}]
    B --> C[Add to Cart: {{CART_COUNT}}]
    C --> D[Checkout: {{CHECKOUT_COUNT}}]
    D --> E[Purchase: {{PURCHASE_COUNT}}]

    style A fill:#90EE90
    style E fill:#90EE90
    {{#if HIGHEST_DROPOFF_STEP}}
    style {{HIGHEST_DROPOFF_STEP}} fill:#FFB6C1
    {{/if}}
```

### Journey Metrics

| Stage | Visitors | Drop-off Rate | Notes |
|-------|----------|---------------|-------|
{{JOURNEY_METRICS_TABLE}}

---

## Drop-off Analysis

### Critical Drop-off Points

{{#each DROPOFF_POINTS}}
#### {{this.step_name}}

> [!warning] High Drop-off: {{this.dropoff_rate}}%
> **Affected Users:** {{this.affected_count}}
> **Compared to Baseline:** {{this.vs_baseline}}
>
> **Likely Reasons:**
{{#each this.reasons}}
> - {{this}}
{{/each}}
>
> **Recommended Actions:**
{{#each this.recommendations}}
> - {{this}}
{{/each}}

{{/each}}

{{#if NO_DROPOFF_ISSUES}}
> [!success] No Critical Drop-offs Detected
> All funnel steps are performing within normal parameters.
{{/if}}

---

## Customer Segments Performance

### High-Value Customers (LTV > $500)

| Metric | Value |
|--------|-------|
| Sessions Today | {{HV_SESSIONS}} |
| Conversions | {{HV_CONVERSIONS}} |
| Conversion Rate | {{HV_CONV_RATE}}% |
| Revenue | ${{HV_REVENUE}} |
| Avg Session Time | {{HV_AVG_TIME}} |

**Common Journey Pattern:**
{{HV_JOURNEY_PATTERN}}

**Profile Link:** [[customer_journeys/segments/high_ltv_customers|High-Value Customer Segment]]

### New Visitors

| Metric | Value |
|--------|-------|
| Sessions Today | {{NEW_SESSIONS}} |
| Conversions | {{NEW_CONVERSIONS}} |
| Conversion Rate | {{NEW_CONV_RATE}}% |
| Bounce Rate | {{NEW_BOUNCE_RATE}}% |
| Top Entry Page | {{NEW_TOP_ENTRY}} |

**Common Drop-off:** {{NEW_COMMON_DROPOFF}}

### Returning Customers

| Metric | Value |
|--------|-------|
| Sessions Today | {{RET_SESSIONS}} |
| Conversions | {{RET_CONVERSIONS}} |
| Conversion Rate | {{RET_CONV_RATE}}% |
| Avg Orders | {{RET_AVG_ORDERS}} |

---

## Behavioral Insights

### Rage Clicks Detected

{{#if RAGE_CLICKS_DETECTED}}
> [!alert] User Frustration Indicators
> **Total Rage Click Events:** {{RAGE_CLICK_COUNT}}
> **Affected Pages:**
{{#each RAGE_CLICK_PAGES}}
> - {{this.page}} ({{this.count}} incidents)
>   - Elements: {{this.elements}}
{{/each}}
{{else}}
✅ No significant rage clicks detected today.
{{/if}}

### Form Errors

{{#if FORM_ERRORS_DETECTED}}
| Form | Error Type | Occurrences | Impact |
|------|------------|-------------|--------|
{{FORM_ERRORS_TABLE}}

**Recommendation:** {{FORM_ERROR_RECOMMENDATION}}
{{else}}
✅ No significant form errors detected today.
{{/if}}

### Search Behavior

| Metric | Value |
|--------|-------|
| Total Searches | {{SEARCH_COUNT}} |
| Unique Queries | {{UNIQUE_QUERIES}} |
| Zero-Result Searches | {{ZERO_RESULT_COUNT}} ({{ZERO_RESULT_PERCENT}}%) |

**Top Search Queries:**
{{TOP_SEARCH_QUERIES_LIST}}

{{#if HIGH_ZERO_RESULTS}}
> [!warning] High Zero-Result Rate
> {{ZERO_RESULT_PERCENT}}% of searches returned no results.
> Consider adding products or improving search relevance.
{{/if}}

---

## Page Performance

### Most Visited Pages

| Page | Views | Avg Time | Bounce Rate | Conv Rate |
|------|-------|----------|-------------|-----------|
{{TOP_PAGES_TABLE}}

### Slowest Pages (Performance Issue)

{{#if SLOW_PAGES}}
| Page | Avg Load Time | Impact |
|------|---------------|--------|
{{SLOW_PAGES_TABLE}}

> [!tip] Performance Optimization
> Pages loading slower than 3 seconds significantly increase bounce rate.
{{/if}}

---

## Top Customer Journeys Today

### Highest Value Conversions

{{#each TOP_CONVERSIONS}}
#### {{this.rank}}. [[customer_journeys/customer_profiles/customer_{{this.customer_id}}|Customer #{{this.customer_id}}]]

- **Order Value:** ${{this.order_value}}
- **Journey Duration:** {{this.journey_duration}}
- **Touchpoints:** {{this.touchpoint_count}}
- **Path:** {{this.journey_path}}

{{/each}}

### Notable Abandonment Cases

{{#each NOTABLE_ABANDONMENTS}}
#### {{this.rank}}. Cart Value: ${{this.cart_value}} - [[customer_journeys/customer_profiles/customer_{{this.customer_id}}|Customer #{{this.customer_id}}]]

- **Abandoned At:** {{this.abandoned_at_step}}
- **Reason:** {{this.inferred_reason}}
- **Journey:** {{this.journey_summary}}
- **Recovery Opportunity:** {{this.recovery_suggestion}}

{{/each}}

---

## Recommendations

{{#each RECOMMENDATIONS}}
### {{this.priority}} Priority: {{this.title}}

{{this.description}}

**Expected Impact:** {{this.expected_impact}}

**Action Items:**
{{#each this.action_items}}
- [ ] {{this}}
{{/each}}

**Related:**
{{#each this.related_links}}
- {{this}}
{{/each}}

---

{{/each}}

---

## Related Reports

### Alerts Triggered Today
{{#each RELATED_ALERTS}}
- [[customer_journeys/dropoff_alerts/{{this.filename}}|{{this.title}}]]
{{/each}}

### Funnel Reports
- [[customer_journeys/funnel_analysis/checkout_funnel_weekly|Weekly Checkout Funnel]]
- [[customer_journeys/funnel_analysis/signup_funnel_daily|Daily Signup Funnel]]

### Segments
- [[customer_journeys/segments/high_ltv_customers|High-Value Customers]]
- [[customer_journeys/segments/cart_abandoners|Cart Abandoners]]
- [[customer_journeys/segments/mobile_users|Mobile Users]]

---

## Data Quality Notes

| Metric | Value |
|--------|-------|
| Events Captured | {{EVENTS_CAPTURED}} |
| Sessions Reconstructed | {{SESSIONS_RECONSTRUCTED}} |
| Data Completeness | {{DATA_COMPLETENESS}}% |
| Processing Errors | {{PROCESSING_ERRORS}} |

{{#if DATA_QUALITY_ISSUES}}
> [!warning] Data Quality Issues
{{#each DATA_QUALITY_ISSUES}}
> - {{this}}
{{/each}}
{{/if}}

---

## Appendix

### Methodology
- **Analysis Period:** {{DATE}} 00:00:00 to 23:59:59 (UTC)
- **Session Timeout:** 30 minutes of inactivity
- **Conversion Definition:** Completed purchase event
- **Bounce Definition:** Single-page session < 10 seconds
- **Attribution:** Last-touch attribution model

### Glossary
- **LTV:** Lifetime Value - total revenue from a customer
- **Rage Click:** 3+ rapid clicks on same element (frustration indicator)
- **Drop-off Rate:** Percentage of users who abandon at a specific step
- **Engagement Score:** Calculated from time, pages viewed, interactions

---

**Report Generated by Customer Journey Analysis Tool**
*Powered by Pydantic AI + FastAPI*

---

## Navigation

← [[customer_journeys/daily_reports/{{PREV_DATE}}-journey-summary|Previous Day]] | [[customer_journeys/_index|Journey Index]] | [[customer_journeys/daily_reports/{{NEXT_DATE}}-journey-summary|Next Day]] →
