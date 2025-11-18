# Customer Journey Analysis Tool - Design Artifacts

## Overview

This directory contains the complete design artifacts for the Customer Journey Analysis Tool, including Pydantic schemas for all 4 agents and Obsidian vault templates for data visualization.

**Status:** ✅ Design Complete - Ready for Implementation
**Created:** 2025-01-18
**Version:** 1.0

---

## Directory Structure

```
docs/customer-journey-tool/
├── README.md                                  # This file
├── schemas.py                                 # Complete Pydantic schemas for all 4 agents
├── obsidian-vault-structure.md               # Vault organization specification
└── templates/                                 # Markdown templates for Obsidian
    ├── daily_report_template.md              # Daily journey summary
    ├── customer_profile_template.md          # Individual customer profile
    ├── funnel_analysis_template.md           # Conversion funnel analysis
    └── dropoff_alert_template.md             # Drop-off alert notification
```

---

## Deliverable 1: Pydantic Schemas (`schemas.py`)

### Overview

Complete, production-ready Pydantic schemas for all 4 specialized agents with strict type safety, comprehensive validation, and agent-optimized documentation.

### Schemas Included

#### 1. Core Event Tracking
- **`EventType`** (Enum): 20+ event types (page_view, click, purchase, etc.)
- **`DeviceType`** (Enum): Device categories
- **`TrackingEvent`**: Atomic interaction event with full context
- **`BatchTrackingRequest`**: Batch event ingestion (up to 100 events)

#### 2. Customer Attributes
- **`CustomerAttributes`**: Comprehensive customer profile
  - Demographics (age, gender, location)
  - Behavioral metrics (visit count, session duration)
  - Transactional data (LTV, order count, avg order value)
  - Acquisition context (UTM parameters, referrer)
  - Engagement indicators (loyalty tier, churn risk, engagement score)
  - Device/tech context
  - Custom business attributes
- **`AttributeChange`**: Attribute evolution tracking
- **`LoyaltyTier`** (Enum): Bronze, Silver, Gold, Platinum tiers

#### 3. Sessions & Journeys
- **`CustomerSession`**: Reconstructed session with metrics
  - Timeline (start, end, duration)
  - Page flow and navigation
  - Events aggregation
  - Conversion/abandonment status
  - Behavioral flags (rage clicks, form errors)
- **`CustomerJourney`**: Complete multi-session customer lifecycle
  - All sessions and events
  - Attribute evolution over time
  - Journey outcome (converted/abandoned)
  - Predictive insights

#### 4. Funnel Analysis
- **`FunnelStep`**: Single funnel step definition
- **`FunnelDefinition`**: Complete funnel with validation
- **`FunnelStepMetrics`**: Per-step performance data
- **`FunnelAnalysisResult`**: Complete funnel analysis
  - Overall metrics
  - Step-by-step breakdown
  - Drop-off hotspots
  - Segment performance
- **`DropOffAlert`**: Abnormal drop-off detection
- **`FunnelStepStatus`** (Enum): Entered, Completed, Abandoned

#### 5. Heatmaps
- **`HeatmapDataPoint`**: Single interaction point
- **`HeatmapData`**: Aggregated heatmap for a page

#### 6. Tool Responses
- **`OperationResult`**: Generic agent tool response
- **`ResponseFormat`** (Enum): Minimal, Concise, Detailed

### Key Features

✅ **Strict Type Safety**: All fields fully typed, mypy-compliant
✅ **Comprehensive Validation**: Field validators for data quality
✅ **Model Validators**: Cross-field validation logic
✅ **Google-Style Docstrings**: Clear, actionable documentation
✅ **Agent-Optimized**: Field descriptions guide AI decision-making
✅ **Privacy-Aware**: Email hashing, PII protection
✅ **Cross-Platform**: Works on Windows, macOS, Linux

### Usage Example

```python
from datetime import datetime
from schemas import TrackingEvent, CustomerAttributes, EventType, DeviceType

# Create a tracking event
event = TrackingEvent(
    event_id="evt_12345",
    timestamp=datetime.utcnow(),
    session_id="sess_abc123",
    device_id="dev_xyz789",
    event_type=EventType.ADD_TO_CART,
    page_url="https://example.com/products/widget",
    page_title="Premium Widget - Buy Now",
    element_selector="#add-to-cart-btn",
    element_text="Add to Cart",
    coordinates=(450, 320),
    user_agent="Mozilla/5.0...",
    screen_resolution=(1920, 1080),
    viewport_size=(1440, 900),
    device_type=DeviceType.DESKTOP,
    product_id="prod_456",
    product_name="Premium Widget",
    product_price=99.99,
    customer_attributes=CustomerAttributes(
        customer_id="cust_789",
        visit_count=3,
        ltv=245.00,
        device_type=DeviceType.DESKTOP,
        location_country="US",
        engagement_score=75.5,
    ),
)

# Validation happens automatically
print(f"Valid event: {event.event_id}")
```

### Validation Examples

```python
# Automatic validation
try:
    event = TrackingEvent(
        event_id="test",
        page_url="invalid-url",  # ❌ Must start with http:// or https://
        # ... other fields
    )
except ValueError as e:
    print(f"Validation error: {e}")

# Attribute validation
attrs = CustomerAttributes(
    age=200  # ❌ Must be 0-150
)
# Raises: ValueError: Age must be between 0 and 150

# Model-level validation
funnel = FunnelDefinition(
    funnel_id="checkout",
    funnel_name="Checkout Funnel",
    steps=[
        FunnelStep(step_number=1, step_name="Cart", ...),
        FunnelStep(step_number=3, step_name="Payment", ...),  # ❌ Gap in sequence
    ]
)
# Raises: ValueError: Step numbers must be sequential starting from 1
```

---

## Deliverable 2: Obsidian Vault Templates

### Overview

Complete markdown templates and vault structure specification for storing customer journey analytics in Obsidian, enabling powerful visualization and knowledge graph integration.

### Files Included

#### 1. `obsidian-vault-structure.md`
Comprehensive specification including:
- Folder structure (7 main categories)
- File naming conventions
- Frontmatter standards
- Wikilink guidelines
- Mermaid diagram standards
- Metadata table formats
- Callout block examples
- Dataview query examples
- Archive strategy
- Backup recommendations

#### 2. `templates/daily_report_template.md`
Daily journey summary template with:
- Executive summary with key metrics
- Traffic source breakdown
- Device performance comparison
- Journey flow visualization (Mermaid)
- Drop-off analysis with severity callouts
- Customer segment performance
- Behavioral insights (rage clicks, form errors)
- Top customer journeys
- Actionable recommendations
- Data quality metrics

**Token Estimate:** ~2-5 KB (500-1500 words)

#### 3. `templates/customer_profile_template.md`
Individual customer profile with:
- Complete customer attributes
- Acquisition context
- Journey timeline (Mermaid)
- Session-by-session history
- Journey visualization (Sankey diagram)
- Purchase history
- Behavioral patterns
- Friction points detection
- Attribute evolution over time
- Predictive insights (ML-based)
- Cohort comparison
- Custom business attributes

**Token Estimate:** ~3-8 KB (800-2000 words)

#### 4. `templates/funnel_analysis_template.md`
Conversion funnel analysis with:
- Executive summary
- Funnel visualization (waterfall + Sankey)
- Step-by-step detailed analysis
  - Performance metrics
  - Drop-off reasons
  - Segment performance
  - Optimization recommendations
- Drop-off distribution
- Time-based analysis
- Segment comparison (device, traffic source, customer type)
- Success vs abandonment paths
- A/B test results
- Benchmarking (industry + historical)
- Revenue impact analysis
- Action plan (immediate, short-term, long-term)

**Token Estimate:** ~4-10 KB (1000-2500 words)

#### 5. `templates/dropoff_alert_template.md`
Real-time drop-off alert with:
- Severity-based callouts (low, medium, high, critical)
- Critical metrics comparison
- Visual before/after comparison (Mermaid)
- Root cause analysis (AI-detected)
- Supporting data:
  - Rage clicks
  - Form errors
  - Performance issues
  - JavaScript errors
- Affected user segments
- Revenue impact estimation
- Sample abandoned sessions
- Immediate actions required
- Recommended fixes with code examples
- Historical context
- Monitoring checklist
- Resolution tracking

**Token Estimate:** ~1-3 KB (300-800 words)

### Template Features

✅ **YAML Frontmatter**: Structured metadata for Obsidian features
✅ **Wikilinks**: Cross-references between related reports
✅ **Mermaid Diagrams**: Timeline, flowchart, and Sankey visualizations
✅ **Callout Blocks**: Warning, tip, success, alert callouts
✅ **Tables**: Metrics, comparisons, segment breakdowns
✅ **Dataview Ready**: Compatible with Dataview plugin queries
✅ **Action Items**: Checkboxes for task tracking
✅ **Navigation**: Prev/next links, breadcrumbs

### Vault Folder Structure

```
customer_journeys/
├── _index.md                    # Main navigation hub
├── daily_reports/               # Automated daily summaries
├── customer_profiles/           # Individual journey maps
├── funnel_analysis/             # Conversion funnel reports
├── dropoff_alerts/              # Abnormal behavior alerts
├── insights/                    # AI-generated insights
├── heatmaps/                    # Interaction heatmap analysis
└── segments/                    # Customer segment reports
```

### Example Vault State

After 1 week:
- ~89 files
- ~404 KB total
- Fully searchable via Obsidian
- Graph view shows customer → funnel → alert connections

After 1 month:
- ~300 files
- ~1.5 MB total
- Still very manageable!

---

## Implementation Roadmap

### Phase 1: Schema Integration (Week 1)
1. **Copy `schemas.py` to project:**
   ```bash
   cp docs/customer-journey-tool/schemas.py src/tools/customer_journey/schemas.py
   ```

2. **Add imports to relevant modules:**
   ```python
   from src.tools.customer_journey.schemas import (
       TrackingEvent,
       CustomerAttributes,
       CustomerSession,
       CustomerJourney,
       FunnelDefinition,
       FunnelAnalysisResult,
       DropOffAlert,
   )
   ```

3. **Implement service layer using schemas:**
   - `src/tools/customer_journey/interaction_tracking_service.py`
   - `src/tools/customer_journey/dropoff_analysis_service.py`
   - `src/tools/customer_journey/journey_mapping_service.py`
   - `src/tools/customer_journey/attributes_service.py`

4. **Write unit tests for schema validation:**
   ```bash
   tests/tools/customer_journey/test_schemas.py
   ```

### Phase 2: Obsidian Integration (Week 2)
1. **Create base vault structure:**
   ```bash
   # Run from project root
   mkdir -p /path/to/ObsidianVault/customer_journeys/{daily_reports,customer_profiles,funnel_analysis,dropoff_alerts,insights,heatmaps,segments}
   ```

2. **Copy templates:**
   ```bash
   cp docs/customer-journey-tool/templates/*.md /path/to/ObsidianVault/templates/customer_journey_templates/
   ```

3. **Implement report generators:**
   ```python
   # src/tools/customer_journey/report_generators.py
   class DailyReportGenerator:
       def generate(self, data: dict) -> str:
           # Use daily_report_template.md
           # Replace {{PLACEHOLDERS}} with actual data
           pass
   ```

4. **Configure vault sync:**
   ```python
   # src/shared/config.py
   OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")
   JOURNEY_REPORTS_PATH = f"{OBSIDIAN_VAULT_PATH}/customer_journeys"
   ```

### Phase 3: Agent Tools (Weeks 3-4)
1. **Implement 4 agent tools:**
   - `obsidian_track_interaction` (Interaction Tracking Agent)
   - `obsidian_analyze_dropoff` (Drop-off Analysis Agent)
   - `obsidian_map_journey` (Journey Mapping Agent)
   - `obsidian_manage_attributes` (Customer Attributes Agent)

2. **Follow coding guidelines:**
   - Google-style docstrings
   - "Use this when" / "Do NOT use" sections
   - Performance notes
   - Realistic examples
   - Structured logging

3. **Write comprehensive tests:**
   ```bash
   tests/tools/customer_journey/test_interaction_tracking.py
   tests/tools/customer_journey/test_dropoff_analysis.py
   tests/tools/customer_journey/test_journey_mapping.py
   tests/tools/customer_journey/test_attributes_management.py
   ```

---

## Alignment with Coding Standards

### From `coding-generic-agent.md`

✅ **Type Safety Non-Negotiable**
- All schemas have strict type annotations
- No `Any` types without justification
- Mypy-compliant

✅ **Documentation Standards**
- Google-style docstrings throughout
- Field descriptions explain purpose and constraints
- Model validators documented

✅ **Logging Standards**
- Schemas support structured logging
- All operations will use `get_logger(__name__)`
- Error context captured in validation

✅ **Testing Requirements**
- Schemas designed for testability
- Validation logic isolated
- Cross-platform compatible

✅ **Performance Standards**
- Response format tiers (minimal, concise, detailed)
- Token estimates in templates
- Efficient data structures

### From `coding-agent.md`

✅ **Obsidian Integration**
- Vault structure follows Obsidian best practices
- Wikilinks for cross-referencing
- Frontmatter for metadata
- Mermaid diagrams for visualization

✅ **Tool Separation**
- 4 distinct agents with clear boundaries
- No overlap in responsibilities
- Clear "Use this when" / "Do NOT use" guidance

✅ **Path Validation**
- Vault paths handled with pathlib
- Cross-platform compatibility
- Security validation patterns ready

---

## Testing the Schemas

### Run Schema Validation Tests

```python
# tests/tools/customer_journey/test_schemas.py
import pytest
from datetime import datetime
from src.tools.customer_journey.schemas import (
    TrackingEvent,
    CustomerAttributes,
    EventType,
    DeviceType,
)

class TestTrackingEvent:
    """Tests for TrackingEvent schema."""

    def test_valid_tracking_event(self):
        """Test creating a valid tracking event."""
        event = TrackingEvent(
            event_id="evt_123",
            timestamp=datetime.utcnow(),
            session_id="sess_abc",
            device_id="dev_xyz",
            event_type=EventType.PAGE_VIEW,
            page_url="https://example.com",
            page_title="Home",
            user_agent="Mozilla/5.0...",
            screen_resolution=(1920, 1080),
            viewport_size=(1440, 900),
            device_type=DeviceType.DESKTOP,
            customer_attributes=CustomerAttributes(
                device_type=DeviceType.DESKTOP
            ),
        )

        assert event.event_id == "evt_123"
        assert event.event_type == EventType.PAGE_VIEW

    def test_invalid_page_url(self):
        """Test validation rejects invalid URLs."""
        with pytest.raises(ValueError, match="must start with http"):
            TrackingEvent(
                event_id="evt_123",
                page_url="invalid-url",  # Missing protocol
                # ... other required fields
            )

    def test_element_text_truncation(self):
        """Test element text is truncated to 200 chars."""
        long_text = "a" * 300
        event = TrackingEvent(
            # ... required fields ...
            element_text=long_text,
        )

        assert len(event.element_text) == 203  # 200 + "..."
        assert event.element_text.endswith("...")
```

---

## Next Steps

### For Implementation Team

1. **Review schemas:**
   - Read `schemas.py` thoroughly
   - Understand validation logic
   - Identify custom business attributes needed

2. **Review templates:**
   - Read all 4 template files
   - Customize placeholders for your business
   - Decide which sections to keep/remove

3. **Set up development environment:**
   ```bash
   # Install dependencies
   uv sync

   # Set environment variables
   export OBSIDIAN_VAULT_PATH="/path/to/vault"
   export ANTHROPIC_API_KEY="your-key"

   # Run tests
   uv run pytest tests/tools/customer_journey/ -v
   ```

4. **Start with Phase 1:**
   - Copy schemas to project
   - Write service layer
   - Write tests
   - Validate with linters

5. **Move to Phase 2:**
   - Set up Obsidian vault
   - Implement report generators
   - Test template rendering

6. **Complete with Phase 3:**
   - Implement 4 agent tools
   - Write comprehensive tests
   - Deploy and monitor

---

## FAQs

### Q: Can I modify the schemas?
**A:** Yes! The schemas are designed to be extensible. Add custom fields to `custom` dictionaries or extend base classes.

### Q: Do I need all 4 templates?
**A:** No. Start with `daily_report` and `customer_profile`. Add `funnel_analysis` and `dropoff_alert` as needed.

### Q: How do I handle PII (Personally Identifiable Information)?
**A:** The schemas include privacy features:
- Email hashing validation
- IP address hashing
- Custom data encryption hooks
- Follow GDPR/CCPA guidelines

### Q: Can I use a different storage backend instead of Obsidian?
**A:** Yes. The schemas are storage-agnostic. Replace Obsidian integration with:
- PostgreSQL + TimescaleDB
- MongoDB
- Elasticsearch
- S3 + Athena
- Your preferred database

### Q: How do I scale beyond 10K events/day?
**A:** See main planning document for medium/large scale architecture:
- Horizontal scaling (multiple app servers)
- Dedicated database server
- Redis cluster for caching
- Message queue (Kafka/Redis Streams)

---

## Support & Resources

### Documentation
- **Main Planning Doc:** `../../REFINED_PLAN.md` (if created)
- **Coding Standards:** `../../CLAUDE.md`
- **Generic Agent Guide:** `../../coding-generic-agent.md`
- **Obsidian Agent Guide:** `../../coding-agent.md`

### Tools
- **Pydantic Docs:** https://docs.pydantic.dev/
- **Obsidian Docs:** https://help.obsidian.md/
- **Mermaid Docs:** https://mermaid.js.org/
- **FastAPI Docs:** https://fastapi.tiangolo.com/

---

## Changelog

### Version 1.0 (2025-01-18)
- ✅ Initial release
- ✅ Complete Pydantic schemas for 4 agents
- ✅ 4 Obsidian markdown templates
- ✅ Vault structure specification
- ✅ Implementation roadmap
- ✅ Testing examples

---

## License

This design is part of the Obsidian Agent project and follows the same license.

---

**Created by:** Claude (Anthropic)
**For:** sathyan17-1980/Obsidian_Agent
**Date:** 2025-01-18
**Status:** ✅ Ready for Implementation
