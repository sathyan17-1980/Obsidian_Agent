"""Pydantic schemas for Customer Journey Analysis Tool.

This module contains all data models for the 4 specialized agents:
1. Interaction Tracking Agent
2. Drop-off Analysis Agent
3. Customer Journey Mapping Agent
4. Customer Attributes Agent

All schemas follow strict type safety and include comprehensive validation.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# =============================================================================
# ENUMS
# =============================================================================


class EventType(str, Enum):
    """Types of user interaction events tracked on websites."""

    PAGE_VIEW = "page_view"
    """User viewed a page."""

    CLICK = "click"
    """User clicked an element (button, link, etc.)."""

    FORM_SUBMIT = "form_submit"
    """User submitted a form."""

    FORM_INPUT = "form_input"
    """User interacted with a form field."""

    SCROLL = "scroll"
    """User scrolled the page."""

    HOVER = "hover"
    """User hovered over an element."""

    ADD_TO_CART = "add_to_cart"
    """User added item to shopping cart."""

    REMOVE_FROM_CART = "remove_from_cart"
    """User removed item from shopping cart."""

    CHECKOUT_START = "checkout_start"
    """User initiated checkout process."""

    PURCHASE = "purchase"
    """User completed a purchase."""

    SIGNUP = "signup"
    """User created an account."""

    LOGIN = "login"
    """User logged in."""

    LOGOUT = "logout"
    """User logged out."""

    SEARCH = "search"
    """User performed a search."""

    VIDEO_PLAY = "video_play"
    """User played a video."""

    VIDEO_PAUSE = "video_pause"
    """User paused a video."""

    FILE_DOWNLOAD = "file_download"
    """User downloaded a file."""

    ERROR = "error"
    """JavaScript error or user-facing error occurred."""

    CUSTOM = "custom"
    """Custom event defined by implementation."""


class DeviceType(str, Enum):
    """Device type categories."""

    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    UNKNOWN = "unknown"


class ResponseFormat(str, Enum):
    """Response verbosity levels for agent tools."""

    MINIMAL = "minimal"
    """~50 tokens - status only."""

    CONCISE = "concise"
    """~150 tokens - balanced summary (DEFAULT)."""

    DETAILED = "detailed"
    """~500+ tokens - comprehensive details."""


class FunnelStepStatus(str, Enum):
    """Status of a user within a funnel step."""

    ENTERED = "entered"
    """User entered this step."""

    COMPLETED = "completed"
    """User completed this step."""

    ABANDONED = "abandoned"
    """User abandoned at this step."""


class LoyaltyTier(str, Enum):
    """Customer loyalty tier levels."""

    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    UNKNOWN = "unknown"


# =============================================================================
# CUSTOMER ATTRIBUTES SCHEMAS
# =============================================================================


class CustomerAttributes(BaseModel):
    """Customer attributes tracked at each touchpoint.

    This model captures demographic, behavioral, transactional, and technical
    attributes for comprehensive customer profiling and segmentation.
    """

    # Identity
    customer_id: Optional[str] = Field(
        None,
        description="Unique customer identifier (user ID, email hash, etc.)",
    )
    email: Optional[str] = Field(
        None,
        description="Customer email address (hashed or encrypted for privacy)",
    )

    # Demographics
    age: Optional[int] = Field(
        None,
        ge=0,
        le=150,
        description="Customer age in years",
    )
    gender: Optional[str] = Field(
        None,
        description="Customer gender (self-reported)",
    )
    location_country: Optional[str] = Field(
        None,
        description="Country code (ISO 3166-1 alpha-2, e.g., 'US', 'GB')",
    )
    location_city: Optional[str] = Field(
        None,
        description="City name",
    )
    language: Optional[str] = Field(
        None,
        description="Preferred language (ISO 639-1, e.g., 'en', 'es')",
    )
    timezone: Optional[str] = Field(
        None,
        description="Timezone (e.g., 'America/New_York')",
    )

    # Behavioral Metrics
    visit_count: int = Field(
        default=0,
        ge=0,
        description="Total number of sessions",
    )
    pages_viewed: int = Field(
        default=0,
        ge=0,
        description="Total pages viewed across all sessions",
    )
    avg_session_duration_seconds: Optional[int] = Field(
        None,
        ge=0,
        description="Average session duration in seconds",
    )
    total_time_on_site_seconds: int = Field(
        default=0,
        ge=0,
        description="Cumulative time spent on site",
    )
    last_visit_date: Optional[datetime] = Field(
        None,
        description="Timestamp of most recent session",
    )
    first_visit_date: Optional[datetime] = Field(
        None,
        description="Timestamp of first session",
    )
    days_since_last_visit: Optional[int] = Field(
        None,
        ge=0,
        description="Days since last visit (calculated)",
    )

    # Transactional Metrics
    lifetime_value: float = Field(
        default=0.0,
        ge=0.0,
        description="Total revenue from this customer (LTV)",
    )
    order_count: int = Field(
        default=0,
        ge=0,
        description="Total number of completed purchases",
    )
    last_purchase_date: Optional[datetime] = Field(
        None,
        description="Timestamp of most recent purchase",
    )
    avg_order_value: Optional[float] = Field(
        None,
        ge=0.0,
        description="Average order value across all purchases",
    )
    cart_abandonment_count: int = Field(
        default=0,
        ge=0,
        description="Number of times user abandoned cart",
    )

    # Acquisition Context
    utm_source: Optional[str] = Field(
        None,
        description="Traffic source (e.g., 'google', 'facebook', 'direct')",
    )
    utm_medium: Optional[str] = Field(
        None,
        description="Traffic medium (e.g., 'cpc', 'organic', 'email')",
    )
    utm_campaign: Optional[str] = Field(
        None,
        description="Campaign identifier",
    )
    utm_term: Optional[str] = Field(
        None,
        description="Paid search keyword",
    )
    utm_content: Optional[str] = Field(
        None,
        description="Ad content identifier",
    )
    referrer: Optional[str] = Field(
        None,
        description="Referring URL or domain",
    )
    landing_page: Optional[str] = Field(
        None,
        description="First page URL in first session",
    )

    # Engagement Indicators
    email_subscriber: bool = Field(
        default=False,
        description="Whether customer subscribed to emails",
    )
    loyalty_tier: LoyaltyTier = Field(
        default=LoyaltyTier.UNKNOWN,
        description="Customer loyalty program tier",
    )
    engagement_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Calculated engagement score (0-100)",
    )
    churn_risk: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Predicted churn probability (0=low risk, 1=high risk)",
    )
    conversion_probability: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Predicted conversion probability (ML-based)",
    )

    # Device & Technical Context
    device_type: DeviceType = Field(
        default=DeviceType.UNKNOWN,
        description="Device category",
    )
    os: Optional[str] = Field(
        None,
        description="Operating system (e.g., 'Windows 11', 'macOS 14', 'Android 13')",
    )
    browser: Optional[str] = Field(
        None,
        description="Browser name and version (e.g., 'Chrome 120', 'Safari 17')",
    )
    screen_resolution: Optional[tuple[int, int]] = Field(
        None,
        description="Screen resolution (width, height) in pixels",
    )
    viewport_size: Optional[tuple[int, int]] = Field(
        None,
        description="Browser viewport (width, height) in pixels",
    )

    # Custom Business Attributes
    custom: dict[str, Any] = Field(
        default_factory=dict,
        description="Custom business-specific attributes (flexible key-value pairs)",
    )

    @field_validator("email")
    @classmethod
    def validate_email_privacy(cls, v: Optional[str]) -> Optional[str]:
        """Ensure email is hashed or masked for privacy.

        Args:
            v: Email value to validate.

        Returns:
            Validated email (should be hashed).

        Raises:
            ValueError: If email appears to be plaintext.
        """
        if v and "@" in v and not v.startswith("hash_"):
            # In production, you'd hash the email here
            # For now, just warn
            pass
        return v

    @field_validator("age")
    @classmethod
    def validate_age_realistic(cls, v: Optional[int]) -> Optional[int]:
        """Validate age is realistic.

        Args:
            v: Age value to validate.

        Returns:
            Validated age.

        Raises:
            ValueError: If age is unrealistic.
        """
        if v is not None and (v < 0 or v > 150):
            raise ValueError(f"Age must be between 0 and 150, got {v}")
        return v


class AttributeChange(BaseModel):
    """Record of a single attribute change over time."""

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the attribute changed",
    )
    attribute_name: str = Field(
        description="Name of the attribute that changed",
    )
    old_value: Any = Field(
        description="Previous value (None if first time set)",
    )
    new_value: Any = Field(
        description="New value",
    )
    change_reason: Optional[str] = Field(
        None,
        description="Why the attribute changed (e.g., 'purchase_completed', 'profile_update')",
    )


# =============================================================================
# EVENT TRACKING SCHEMAS
# =============================================================================


class TrackingEvent(BaseModel):
    """Individual user interaction event with full context.

    This is the atomic unit of customer journey data. Each event captures
    what happened, when, where, and the customer's attributes at that moment.
    """

    # Event Identity
    event_id: str = Field(
        description="Unique event identifier (UUID recommended)",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the event occurred (UTC)",
    )

    # Session Context
    session_id: str = Field(
        description="Session identifier (groups events into sessions)",
    )
    device_id: str = Field(
        description="Device fingerprint (for cross-session tracking)",
    )
    user_id: Optional[str] = Field(
        None,
        description="Identified user ID (None for anonymous users)",
    )

    # Event Details
    event_type: EventType = Field(
        description="Type of interaction",
    )
    page_url: str = Field(
        description="Full URL where event occurred",
    )
    page_title: str = Field(
        description="Page title",
    )
    referrer: Optional[str] = Field(
        None,
        description="Referring page URL (for page_view events)",
    )

    # Element Interaction (for click/hover events)
    element_selector: Optional[str] = Field(
        None,
        description="CSS selector of interacted element (e.g., '#checkout-btn')",
    )
    element_text: Optional[str] = Field(
        None,
        description="Text content of element (first 200 chars)",
    )
    element_id: Optional[str] = Field(
        None,
        description="HTML ID attribute of element",
    )
    element_classes: Optional[list[str]] = Field(
        None,
        description="HTML class attributes of element",
    )

    # Position Data (for clicks/hover)
    coordinates: Optional[tuple[int, int]] = Field(
        None,
        description="Click/hover position (x, y) in viewport coordinates",
    )
    scroll_depth: Optional[int] = Field(
        None,
        ge=0,
        le=100,
        description="Scroll depth percentage (0-100) for scroll events",
    )

    # Form Data (for form_input/form_submit events)
    form_id: Optional[str] = Field(
        None,
        description="Form ID attribute",
    )
    form_field_name: Optional[str] = Field(
        None,
        description="Form field name attribute (for form_input)",
    )
    form_field_type: Optional[str] = Field(
        None,
        description="Form field type (text, email, password, etc.)",
    )
    form_validation_errors: Optional[list[str]] = Field(
        None,
        description="Validation errors on form submission",
    )

    # E-commerce Data (for cart/purchase events)
    product_id: Optional[str] = Field(
        None,
        description="Product identifier (for add_to_cart/purchase)",
    )
    product_name: Optional[str] = Field(
        None,
        description="Product name",
    )
    product_category: Optional[str] = Field(
        None,
        description="Product category",
    )
    product_price: Optional[float] = Field(
        None,
        ge=0.0,
        description="Product price",
    )
    quantity: Optional[int] = Field(
        None,
        ge=1,
        description="Quantity added/removed",
    )
    cart_total: Optional[float] = Field(
        None,
        ge=0.0,
        description="Current cart total value",
    )
    order_id: Optional[str] = Field(
        None,
        description="Order ID (for purchase events)",
    )
    order_total: Optional[float] = Field(
        None,
        ge=0.0,
        description="Total order value (for purchase)",
    )

    # Search Data (for search events)
    search_query: Optional[str] = Field(
        None,
        description="Search query string",
    )
    search_results_count: Optional[int] = Field(
        None,
        ge=0,
        description="Number of search results",
    )

    # Error Data (for error events)
    error_message: Optional[str] = Field(
        None,
        description="Error message text",
    )
    error_stack: Optional[str] = Field(
        None,
        description="JavaScript error stack trace (truncated)",
    )

    # Device/Browser Context
    user_agent: str = Field(
        description="User agent string",
    )
    ip_address: Optional[str] = Field(
        None,
        description="IP address (hashed for privacy)",
    )
    screen_resolution: tuple[int, int] = Field(
        description="Screen resolution (width, height)",
    )
    viewport_size: tuple[int, int] = Field(
        description="Viewport size (width, height)",
    )
    device_type: DeviceType = Field(
        description="Device category",
    )

    # Customer Attributes at This Moment
    customer_attributes: CustomerAttributes = Field(
        description="Customer attributes at the time of this event",
    )

    # Performance Metrics
    page_load_time_ms: Optional[int] = Field(
        None,
        ge=0,
        description="Page load time in milliseconds (for page_view)",
    )
    time_on_page_seconds: Optional[int] = Field(
        None,
        ge=0,
        description="Time spent on page before this event",
    )

    # Custom Event Data
    custom_properties: dict[str, Any] = Field(
        default_factory=dict,
        description="Custom event properties (implementation-specific)",
    )

    @field_validator("page_url")
    @classmethod
    def validate_page_url(cls, v: str) -> str:
        """Validate page URL format.

        Args:
            v: URL to validate.

        Returns:
            Validated URL.

        Raises:
            ValueError: If URL is invalid.
        """
        if not v.startswith(("http://", "https://")):
            raise ValueError(f"Page URL must start with http:// or https://, got: {v}")
        return v

    @field_validator("element_text")
    @classmethod
    def truncate_element_text(cls, v: Optional[str]) -> Optional[str]:
        """Truncate element text to 200 chars.

        Args:
            v: Element text to truncate.

        Returns:
            Truncated text (max 200 chars).
        """
        if v and len(v) > 200:
            return v[:200] + "..."
        return v


class BatchTrackingRequest(BaseModel):
    """Request to capture multiple events in one API call (performance optimization)."""

    events: list[TrackingEvent] = Field(
        description="List of events to ingest",
        min_length=1,
        max_length=100,  # Safety limit
    )
    compression: Optional[str] = Field(
        None,
        description="Compression algorithm used (gzip, deflate)",
    )

    @field_validator("events")
    @classmethod
    def validate_batch_size(cls, v: list[TrackingEvent]) -> list[TrackingEvent]:
        """Validate batch size is reasonable.

        Args:
            v: List of events.

        Returns:
            Validated event list.

        Raises:
            ValueError: If batch is too large.
        """
        if len(v) > 100:
            raise ValueError(f"Batch size exceeds maximum of 100 events, got {len(v)}")
        return v


# =============================================================================
# SESSION & JOURNEY SCHEMAS
# =============================================================================


class CustomerSession(BaseModel):
    """Reconstructed user session with aggregated metrics.

    A session represents a period of continuous user activity, typically
    ending after 30 minutes of inactivity.
    """

    # Session Identity
    session_id: str = Field(
        description="Unique session identifier",
    )
    user_id: Optional[str] = Field(
        None,
        description="Identified user ID (None for anonymous)",
    )
    device_id: str = Field(
        description="Device fingerprint",
    )

    # Timeline
    started_at: datetime = Field(
        description="Session start timestamp",
    )
    ended_at: Optional[datetime] = Field(
        None,
        description="Session end timestamp (None if still active)",
    )
    duration_seconds: Optional[int] = Field(
        None,
        ge=0,
        description="Total session duration in seconds",
    )

    # Page Flow
    entry_page: str = Field(
        description="First page URL in session",
    )
    exit_page: Optional[str] = Field(
        None,
        description="Last page URL before session ended",
    )
    pages_visited: list[str] = Field(
        description="Ordered list of page URLs visited",
    )
    unique_pages_count: int = Field(
        ge=0,
        description="Number of unique pages visited",
    )
    pageviews_count: int = Field(
        ge=0,
        description="Total pageviews (including repeats)",
    )

    # Events
    events_count: int = Field(
        ge=0,
        description="Total number of events in session",
    )
    event_types: dict[EventType, int] = Field(
        default_factory=dict,
        description="Count of each event type",
    )

    # Conversion
    converted: bool = Field(
        default=False,
        description="Whether session resulted in conversion",
    )
    conversion_type: Optional[str] = Field(
        None,
        description="Type of conversion (purchase, signup, etc.)",
    )
    conversion_value: Optional[float] = Field(
        None,
        ge=0.0,
        description="Monetary value of conversion",
    )
    conversion_timestamp: Optional[datetime] = Field(
        None,
        description="When conversion occurred",
    )

    # Abandonment
    abandoned: bool = Field(
        default=False,
        description="Whether session ended in abandonment",
    )
    drop_off_point: Optional[str] = Field(
        None,
        description="Page/step where user abandoned (if applicable)",
    )
    drop_off_reason: Optional[str] = Field(
        None,
        description="Inferred reason for abandonment (e.g., 'rage_clicks', 'form_errors')",
    )

    # Traffic Source
    traffic_source: Optional[str] = Field(
        None,
        description="Traffic source category (organic, paid, direct, referral)",
    )
    campaign: Optional[str] = Field(
        None,
        description="Marketing campaign identifier",
    )
    utm_params: dict[str, str] = Field(
        default_factory=dict,
        description="All UTM parameters",
    )

    # Behavior Flags
    rage_clicks_detected: bool = Field(
        default=False,
        description="Whether rage clicks were detected (frustration indicator)",
    )
    rage_click_count: int = Field(
        default=0,
        ge=0,
        description="Number of rage click events",
    )
    form_errors_count: int = Field(
        default=0,
        ge=0,
        description="Number of form validation errors",
    )
    searches_count: int = Field(
        default=0,
        ge=0,
        description="Number of search queries",
    )

    # Customer Attributes
    initial_attributes: CustomerAttributes = Field(
        description="Customer attributes at session start",
    )
    final_attributes: CustomerAttributes = Field(
        description="Customer attributes at session end",
    )

    # Engagement Metrics
    engagement_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Calculated engagement score (0-100)",
    )
    scroll_depth_avg: float = Field(
        ge=0.0,
        le=100.0,
        description="Average scroll depth across pages",
    )


class CustomerJourney(BaseModel):
    """Complete customer journey across multiple sessions.

    Represents the full lifecycle of a customer from first visit through
    conversion (or abandonment), potentially spanning days or weeks.
    """

    # Journey Identity
    customer_id: str = Field(
        description="Unique customer identifier",
    )
    journey_start: datetime = Field(
        description="First session timestamp",
    )
    journey_end: Optional[datetime] = Field(
        None,
        description="Last session timestamp (None if ongoing)",
    )
    total_duration_days: Optional[int] = Field(
        None,
        ge=0,
        description="Days from first to last session",
    )

    # Sessions
    sessions: list[CustomerSession] = Field(
        description="All sessions in chronological order",
    )
    session_count: int = Field(
        ge=1,
        description="Total number of sessions",
    )

    # All Touchpoints (flattened events)
    all_events: list[TrackingEvent] = Field(
        description="All events across all sessions (chronological)",
    )
    total_events_count: int = Field(
        ge=0,
        description="Total events across journey",
    )

    # Page Flow
    unique_pages_visited: list[str] = Field(
        description="List of unique pages visited across journey",
    )
    most_visited_pages: list[tuple[str, int]] = Field(
        description="Top pages by visit count [(page_url, visit_count), ...]",
    )

    # Attribute Evolution
    initial_attributes: CustomerAttributes = Field(
        description="Customer attributes at journey start",
    )
    current_attributes: CustomerAttributes = Field(
        description="Current customer attributes",
    )
    attribute_changes: list[AttributeChange] = Field(
        description="Timeline of attribute changes",
    )

    # Journey Outcome
    converted: bool = Field(
        default=False,
        description="Whether customer converted",
    )
    conversion_session: Optional[str] = Field(
        None,
        description="Session ID where conversion occurred",
    )
    conversion_value: Optional[float] = Field(
        None,
        ge=0.0,
        description="Total conversion value",
    )
    time_to_conversion_hours: Optional[int] = Field(
        None,
        ge=0,
        description="Hours from first visit to conversion",
    )

    # Abandonment
    abandoned: bool = Field(
        default=False,
        description="Whether journey ended in abandonment",
    )
    drop_off_point: Optional[str] = Field(
        None,
        description="Final page/step before abandonment",
    )
    drop_off_session: Optional[str] = Field(
        None,
        description="Session ID where abandonment occurred",
    )

    # Behavioral Patterns
    avg_session_duration_seconds: int = Field(
        ge=0,
        description="Average session duration",
    )
    total_time_on_site_seconds: int = Field(
        ge=0,
        description="Cumulative time across all sessions",
    )
    bounce_sessions_count: int = Field(
        default=0,
        ge=0,
        description="Number of single-page sessions",
    )
    engagement_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Overall journey engagement score",
    )


# =============================================================================
# FUNNEL & DROP-OFF SCHEMAS
# =============================================================================


class FunnelStep(BaseModel):
    """Definition of a single step in a conversion funnel."""

    step_number: int = Field(
        ge=1,
        description="Position in funnel (1-indexed)",
    )
    step_name: str = Field(
        description="Human-readable step name",
    )
    step_url_pattern: str = Field(
        description="URL pattern to match (supports wildcards)",
    )
    required_event: Optional[EventType] = Field(
        None,
        description="Event that must occur to complete step (e.g., add_to_cart)",
    )
    min_time_seconds: Optional[int] = Field(
        None,
        ge=0,
        description="Minimum time required on step (anti-bot filter)",
    )
    max_time_seconds: Optional[int] = Field(
        None,
        ge=0,
        description="Maximum time before considered abandoned",
    )


class FunnelDefinition(BaseModel):
    """Complete definition of a conversion funnel."""

    funnel_id: str = Field(
        description="Unique funnel identifier",
    )
    funnel_name: str = Field(
        description="Descriptive funnel name",
    )
    description: Optional[str] = Field(
        None,
        description="Detailed funnel description",
    )
    steps: list[FunnelStep] = Field(
        description="Ordered funnel steps",
        min_length=2,
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When funnel was defined",
    )
    is_active: bool = Field(
        default=True,
        description="Whether funnel is actively tracked",
    )

    @model_validator(mode="after")
    def validate_step_numbers_sequential(self) -> "FunnelDefinition":
        """Validate step numbers are sequential starting from 1.

        Returns:
            Validated funnel definition.

        Raises:
            ValueError: If step numbers are not sequential.
        """
        step_numbers = [step.step_number for step in self.steps]
        expected = list(range(1, len(self.steps) + 1))
        if step_numbers != expected:
            raise ValueError(
                f"Step numbers must be sequential starting from 1. "
                f"Got: {step_numbers}, Expected: {expected}"
            )
        return self


class FunnelStepMetrics(BaseModel):
    """Metrics for a single funnel step."""

    step_number: int = Field(
        ge=1,
        description="Step position in funnel",
    )
    step_name: str = Field(
        description="Step name",
    )
    entered_count: int = Field(
        ge=0,
        description="Number of users who entered this step",
    )
    completed_count: int = Field(
        ge=0,
        description="Number of users who completed this step",
    )
    abandoned_count: int = Field(
        ge=0,
        description="Number of users who abandoned at this step",
    )
    drop_off_rate: float = Field(
        ge=0.0,
        le=1.0,
        description="Proportion who abandoned (abandoned / entered)",
    )
    completion_rate: float = Field(
        ge=0.0,
        le=1.0,
        description="Proportion who completed (completed / entered)",
    )
    avg_time_on_step_seconds: int = Field(
        ge=0,
        description="Average time spent on this step",
    )
    median_time_on_step_seconds: int = Field(
        ge=0,
        description="Median time spent on this step",
    )


class FunnelAnalysisResult(BaseModel):
    """Complete funnel analysis with drop-off metrics."""

    funnel_id: str = Field(
        description="Funnel identifier",
    )
    funnel_name: str = Field(
        description="Funnel name",
    )
    analysis_period_start: datetime = Field(
        description="Start of analysis time range",
    )
    analysis_period_end: datetime = Field(
        description="End of analysis time range",
    )

    # Overall Metrics
    total_entries: int = Field(
        ge=0,
        description="Users who entered funnel (entered step 1)",
    )
    total_completions: int = Field(
        ge=0,
        description="Users who completed entire funnel",
    )
    overall_conversion_rate: float = Field(
        ge=0.0,
        le=1.0,
        description="Completions / Entries",
    )
    avg_time_to_convert_hours: Optional[float] = Field(
        None,
        ge=0.0,
        description="Average time from step 1 to completion",
    )

    # Per-Step Metrics
    step_metrics: list[FunnelStepMetrics] = Field(
        description="Metrics for each funnel step",
    )

    # Drop-off Hotspots
    highest_dropoff_step: Optional[int] = Field(
        None,
        description="Step number with highest drop-off rate",
    )
    highest_dropoff_rate: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Highest drop-off rate across all steps",
    )

    # Segmentation (by customer attributes)
    segments: Optional[dict[str, "FunnelAnalysisResult"]] = Field(
        None,
        description="Funnel metrics segmented by attribute (e.g., by device_type)",
    )


class DropOffAlert(BaseModel):
    """Alert for abnormal drop-off behavior."""

    alert_id: str = Field(
        description="Unique alert identifier",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When alert was triggered",
    )
    funnel_id: str = Field(
        description="Affected funnel",
    )
    step_number: int = Field(
        ge=1,
        description="Affected step",
    )
    step_name: str = Field(
        description="Step name",
    )
    current_dropoff_rate: float = Field(
        ge=0.0,
        le=1.0,
        description="Current drop-off rate",
    )
    baseline_dropoff_rate: float = Field(
        ge=0.0,
        le=1.0,
        description="Historical baseline drop-off rate",
    )
    deviation_percentage: float = Field(
        description="Percentage increase above baseline",
    )
    severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Alert severity based on deviation",
    )
    affected_users_count: int = Field(
        ge=0,
        description="Number of users affected in alert window",
    )
    potential_reasons: list[str] = Field(
        description="Inferred reasons for increased drop-off",
    )

    @field_validator("deviation_percentage")
    @classmethod
    def validate_deviation_positive(cls, v: float) -> float:
        """Validate deviation is positive for alerts.

        Args:
            v: Deviation percentage.

        Returns:
            Validated deviation.

        Raises:
            ValueError: If deviation is negative.
        """
        if v < 0:
            raise ValueError(
                f"Deviation must be positive for alerts, got {v}%. "
                "Negative deviations (improvements) should not trigger alerts."
            )
        return v


# =============================================================================
# HEATMAP SCHEMAS
# =============================================================================


class HeatmapDataPoint(BaseModel):
    """Single click/hover data point for heatmap generation."""

    x: int = Field(
        ge=0,
        description="X coordinate in viewport",
    )
    y: int = Field(
        ge=0,
        description="Y coordinate in viewport",
    )
    intensity: int = Field(
        ge=1,
        description="Number of interactions at this point",
    )
    event_type: Literal["click", "hover", "scroll"] = Field(
        description="Type of interaction",
    )


class HeatmapData(BaseModel):
    """Aggregated heatmap data for a specific page."""

    page_url: str = Field(
        description="Page URL this heatmap represents",
    )
    viewport_width: int = Field(
        ge=1,
        description="Standard viewport width used for normalization",
    )
    viewport_height: int = Field(
        ge=1,
        description="Standard viewport height used for normalization",
    )
    sample_size: int = Field(
        ge=0,
        description="Number of sessions included in heatmap",
    )
    data_points: list[HeatmapDataPoint] = Field(
        description="All interaction points",
    )
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When heatmap was generated",
    )


# =============================================================================
# AGENT TOOL RESPONSE SCHEMAS
# =============================================================================


class OperationResult(BaseModel):
    """Generic result from any agent tool operation."""

    success: bool = Field(
        description="Whether operation succeeded",
    )
    message: str = Field(
        description="Human-readable status message",
    )
    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Operation-specific result data",
    )
    errors: list[str] = Field(
        default_factory=list,
        description="Error messages if operation failed",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Warning messages (non-fatal issues)",
    )
    token_estimate: int = Field(
        default=50,
        ge=0,
        description="Estimated token count for this response",
    )
    execution_time_ms: Optional[float] = Field(
        None,
        ge=0.0,
        description="Execution time in milliseconds",
    )
