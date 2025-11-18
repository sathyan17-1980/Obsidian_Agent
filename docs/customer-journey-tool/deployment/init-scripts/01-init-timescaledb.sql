-- =============================================================================
-- TimescaleDB Initialization Script
-- Creates database schema with TimescaleDB hypertables for time-series data
-- =============================================================================

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- =============================================================================
-- EVENTS TABLE (Hypertable for Time-Series Data)
-- Stores all tracking events
-- =============================================================================
CREATE TABLE IF NOT EXISTS events (
    -- Event Identity
    event_id VARCHAR(255) PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,

    -- Session Context
    session_id VARCHAR(255) NOT NULL,
    device_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255),  -- NULL for anonymous users

    -- Event Details
    event_type VARCHAR(50) NOT NULL,
    page_url TEXT NOT NULL,
    page_title VARCHAR(500),
    referrer TEXT,

    -- Element Interaction (for click/hover events)
    element_selector VARCHAR(500),
    element_text VARCHAR(200),
    element_id VARCHAR(255),
    element_classes TEXT[],

    -- Position Data
    coordinates_x INTEGER,
    coordinates_y INTEGER,
    scroll_depth INTEGER CHECK (scroll_depth BETWEEN 0 AND 100),

    -- Form Data
    form_id VARCHAR(255),
    form_field_name VARCHAR(255),
    form_field_type VARCHAR(50),
    form_validation_errors TEXT[],

    -- E-commerce Data
    product_id VARCHAR(255),
    product_name VARCHAR(500),
    product_category VARCHAR(255),
    product_price DECIMAL(10, 2),
    quantity INTEGER,
    cart_total DECIMAL(10, 2),
    order_id VARCHAR(255),
    order_total DECIMAL(10, 2),

    -- Search Data
    search_query TEXT,
    search_results_count INTEGER,

    -- Error Data
    error_message TEXT,
    error_stack TEXT,

    -- Device/Browser Context
    user_agent TEXT,
    ip_address VARCHAR(45),  -- Hashed for privacy
    screen_resolution_width INTEGER,
    screen_resolution_height INTEGER,
    viewport_width INTEGER,
    viewport_height INTEGER,
    device_type VARCHAR(20),

    -- Performance Metrics
    page_load_time_ms INTEGER,
    time_on_page_seconds INTEGER,

    -- Custom Properties (JSONB for flexibility)
    custom_properties JSONB,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Convert to TimescaleDB hypertable (time-series optimized)
SELECT create_hypertable('events', 'timestamp', if_not_exists => TRUE);

-- Create indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_events_session_id ON events (session_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_events_user_id ON events (user_id, timestamp DESC) WHERE user_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_events_device_id ON events (device_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_events_event_type ON events (event_type, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_events_page_url ON events (page_url, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_events_order_id ON events (order_id) WHERE order_id IS NOT NULL;

-- GIN index for JSONB custom properties
CREATE INDEX IF NOT EXISTS idx_events_custom_properties ON events USING GIN (custom_properties);

-- =============================================================================
-- CUSTOMER_ATTRIBUTES TABLE
-- Stores customer profile data with attribute history
-- =============================================================================
CREATE TABLE IF NOT EXISTS customer_attributes (
    customer_id VARCHAR(255) PRIMARY KEY,

    -- Demographics
    age INTEGER CHECK (age BETWEEN 0 AND 150),
    gender VARCHAR(50),
    location_country VARCHAR(2),  -- ISO 3166-1 alpha-2
    location_city VARCHAR(255),
    language VARCHAR(5),  -- ISO 639-1
    timezone VARCHAR(50),

    -- Behavioral Metrics
    visit_count INTEGER DEFAULT 0,
    pages_viewed INTEGER DEFAULT 0,
    avg_session_duration_seconds INTEGER,
    total_time_on_site_seconds INTEGER DEFAULT 0,
    last_visit_date TIMESTAMPTZ,
    first_visit_date TIMESTAMPTZ,
    days_since_last_visit INTEGER,

    -- Transactional Metrics
    lifetime_value DECIMAL(10, 2) DEFAULT 0.00,
    order_count INTEGER DEFAULT 0,
    last_purchase_date TIMESTAMPTZ,
    avg_order_value DECIMAL(10, 2),
    cart_abandonment_count INTEGER DEFAULT 0,

    -- Acquisition Context
    utm_source VARCHAR(255),
    utm_medium VARCHAR(255),
    utm_campaign VARCHAR(255),
    utm_term VARCHAR(255),
    utm_content VARCHAR(255),
    referrer TEXT,
    landing_page TEXT,

    -- Engagement Indicators
    email_subscriber BOOLEAN DEFAULT FALSE,
    loyalty_tier VARCHAR(20),  -- bronze, silver, gold, platinum
    engagement_score DECIMAL(5, 2) CHECK (engagement_score BETWEEN 0 AND 100),
    churn_risk DECIMAL(5, 4) CHECK (churn_risk BETWEEN 0 AND 1),
    conversion_probability DECIMAL(5, 4) CHECK (conversion_probability BETWEEN 0 AND 1),

    -- Device & Technology
    device_type VARCHAR(20),
    os VARCHAR(100),
    browser VARCHAR(100),

    -- Custom Attributes
    custom JSONB,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for customer attributes
CREATE INDEX IF NOT EXISTS idx_customer_ltv ON customer_attributes (lifetime_value DESC);
CREATE INDEX IF NOT EXISTS idx_customer_loyalty_tier ON customer_attributes (loyalty_tier);
CREATE INDEX IF NOT EXISTS idx_customer_last_visit ON customer_attributes (last_visit_date DESC);
CREATE INDEX IF NOT EXISTS idx_customer_churn_risk ON customer_attributes (churn_risk DESC);

-- GIN index for custom attributes
CREATE INDEX IF NOT EXISTS idx_customer_custom ON customer_attributes USING GIN (custom);

-- =============================================================================
-- ATTRIBUTE_CHANGES TABLE (Hypertable)
-- Tracks attribute changes over time
-- =============================================================================
CREATE TABLE IF NOT EXISTS attribute_changes (
    id BIGSERIAL,
    timestamp TIMESTAMPTZ NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    attribute_name VARCHAR(255) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_reason VARCHAR(255),

    PRIMARY KEY (id, timestamp)
);

-- Convert to hypertable
SELECT create_hypertable('attribute_changes', 'timestamp', if_not_exists => TRUE);

-- Index for querying customer attribute history
CREATE INDEX IF NOT EXISTS idx_attribute_changes_customer ON attribute_changes (customer_id, timestamp DESC);

-- =============================================================================
-- SESSIONS TABLE
-- Stores reconstructed sessions
-- =============================================================================
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    device_id VARCHAR(255) NOT NULL,

    -- Timeline
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    duration_seconds INTEGER,

    -- Page Flow
    entry_page TEXT,
    exit_page TEXT,
    pages_visited TEXT[],
    unique_pages_count INTEGER,
    pageviews_count INTEGER,

    -- Events
    events_count INTEGER,
    event_types JSONB,  -- {event_type: count}

    -- Conversion
    converted BOOLEAN DEFAULT FALSE,
    conversion_type VARCHAR(50),
    conversion_value DECIMAL(10, 2),
    conversion_timestamp TIMESTAMPTZ,

    -- Abandonment
    abandoned BOOLEAN DEFAULT FALSE,
    drop_off_point TEXT,
    drop_off_reason VARCHAR(255),

    -- Traffic Source
    traffic_source VARCHAR(50),
    campaign VARCHAR(255),
    utm_params JSONB,

    -- Behavior Flags
    rage_clicks_detected BOOLEAN DEFAULT FALSE,
    rage_click_count INTEGER DEFAULT 0,
    form_errors_count INTEGER DEFAULT 0,
    searches_count INTEGER DEFAULT 0,

    -- Engagement
    engagement_score DECIMAL(5, 2),
    scroll_depth_avg DECIMAL(5, 2),

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for sessions
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions (user_id, started_at DESC) WHERE user_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_sessions_device_id ON sessions (device_id, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_sessions_started_at ON sessions (started_at DESC);
CREATE INDEX IF NOT EXISTS idx_sessions_converted ON sessions (converted, started_at DESC) WHERE converted = TRUE;

-- =============================================================================
-- FUNNELS TABLE
-- Stores funnel definitions
-- =============================================================================
CREATE TABLE IF NOT EXISTS funnels (
    funnel_id VARCHAR(255) PRIMARY KEY,
    funnel_name VARCHAR(255) NOT NULL,
    description TEXT,
    steps JSONB NOT NULL,  -- Array of funnel step definitions
    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================================================
-- FUNNEL_METRICS TABLE (Hypertable)
-- Stores funnel performance metrics over time
-- =============================================================================
CREATE TABLE IF NOT EXISTS funnel_metrics (
    id BIGSERIAL,
    timestamp TIMESTAMPTZ NOT NULL,
    funnel_id VARCHAR(255) NOT NULL,
    step_number INTEGER NOT NULL,

    -- Metrics
    entered_count INTEGER,
    completed_count INTEGER,
    abandoned_count INTEGER,
    drop_off_rate DECIMAL(5, 4),
    completion_rate DECIMAL(5, 4),
    avg_time_on_step_seconds INTEGER,
    median_time_on_step_seconds INTEGER,

    PRIMARY KEY (id, timestamp),
    FOREIGN KEY (funnel_id) REFERENCES funnels(funnel_id) ON DELETE CASCADE
);

-- Convert to hypertable
SELECT create_hypertable('funnel_metrics', 'timestamp', if_not_exists => TRUE);

-- Index for querying funnel metrics
CREATE INDEX IF NOT EXISTS idx_funnel_metrics_funnel ON funnel_metrics (funnel_id, timestamp DESC);

-- =============================================================================
-- ALERTS TABLE
-- Stores drop-off and anomaly alerts
-- =============================================================================
CREATE TABLE IF NOT EXISTS alerts (
    alert_id VARCHAR(255) PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    severity VARCHAR(20) NOT NULL,  -- low, medium, high, critical
    alert_type VARCHAR(50) NOT NULL,  -- dropoff, rage_clicks, form_errors, etc.

    funnel_id VARCHAR(255),
    step_number INTEGER,

    current_dropoff_rate DECIMAL(5, 4),
    baseline_dropoff_rate DECIMAL(5, 4),
    deviation_percentage DECIMAL(5, 2),
    affected_users_count INTEGER,

    potential_reasons JSONB,
    status VARCHAR(20) DEFAULT 'open',  -- open, investigating, resolved

    resolved_at TIMESTAMPTZ,
    resolved_by VARCHAR(255),
    resolution_notes TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for querying alerts
CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts (status, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts (severity, timestamp DESC);

-- =============================================================================
-- Continuous Aggregates (TimescaleDB Feature)
-- Pre-aggregated views for faster queries
-- =============================================================================

-- Hourly event aggregates
CREATE MATERIALIZED VIEW IF NOT EXISTS events_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', timestamp) AS hour,
    event_type,
    COUNT(*) AS event_count,
    COUNT(DISTINCT session_id) AS unique_sessions,
    COUNT(DISTINCT user_id) AS unique_users
FROM events
GROUP BY hour, event_type
WITH NO DATA;

-- Refresh policy (auto-refresh every hour)
SELECT add_continuous_aggregate_policy('events_hourly',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour',
    if_not_exists => TRUE
);

-- =============================================================================
-- Data Retention Policies (TimescaleDB Feature)
-- Automatically drop old data to save space
-- =============================================================================

-- Keep events for 90 days (configurable)
SELECT add_retention_policy('events', INTERVAL '90 days', if_not_exists => TRUE);

-- Keep attribute changes for 180 days
SELECT add_retention_policy('attribute_changes', INTERVAL '180 days', if_not_exists => TRUE);

-- Keep funnel metrics for 1 year
SELECT add_retention_policy('funnel_metrics', INTERVAL '1 year', if_not_exists => TRUE);

-- =============================================================================
-- Helper Functions
-- =============================================================================

-- Function to update customer attributes updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for customer_attributes
CREATE TRIGGER update_customer_attributes_updated_at
    BEFORE UPDATE ON customer_attributes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for sessions
CREATE TRIGGER update_sessions_updated_at
    BEFORE UPDATE ON sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- Grants (if using separate application user)
-- =============================================================================

-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO journey_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO journey_user;

-- =============================================================================
-- Initialization Complete
-- =============================================================================

-- Insert sample funnel for testing
INSERT INTO funnels (funnel_id, funnel_name, description, steps)
VALUES (
    'checkout_funnel',
    'Checkout Funnel',
    'Standard e-commerce checkout flow',
    '[
        {"step_number": 1, "step_name": "Home", "step_url_pattern": "/"},
        {"step_number": 2, "step_name": "Product", "step_url_pattern": "/products/*"},
        {"step_number": 3, "step_name": "Cart", "step_url_pattern": "/cart"},
        {"step_number": 4, "step_name": "Checkout", "step_url_pattern": "/checkout"},
        {"step_number": 5, "step_name": "Purchase", "step_url_pattern": "/order-confirmation"}
    ]'::jsonb
) ON CONFLICT (funnel_id) DO NOTHING;

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'Customer Journey database schema initialized successfully';
    RAISE NOTICE 'TimescaleDB version: %', (SELECT extversion FROM pg_extension WHERE extname = 'timescaledb'));
END $$;
