# Research: Platform Migration Analysis Tool

## 1. Mission Statement

**Feature Name**: Platform Migration Analysis Tool

**Problem**: Companies modernizing platforms spend $50,000+ and 6-12 weeks manually mapping which modern systems replace legacy functionality, relying on expensive consultants to trace equivalence across tech stacks.

**Goal**: Automated AI agent that ingests platform metadata (OpenAPI, GraphQL, SQL schemas), maps functional equivalence with confidence scores, and generates migration guides—reducing cost by 99.99% and time from weeks to hours.

**Scope**:
- ✅ **Included**: Platform ingestion (OpenAPI, GraphQL, SQL), semantic/structural mapping, gap analysis, query interface ("Where is X?"), report generation (Markdown/JSON/CSV), confidence scoring
- ❌ **Excluded**: Code generation, performance benchmarking, cost estimation, CI/CD integration, real-time monitoring (defer to post-MVP)

---

## 2. Context Assessment

### Current State

**✅ What Already Exists and Works:**
- Obsidian_Agent architecture (vertical slices, FastAPI, Pydantic AI)
- Proven agent tool docstring patterns (Use this when / Do NOT use / Performance Notes)
- Type-safe schemas with strict mypy enforcement
- Structured logging framework (AI-optimized with Structlog)
- Testing infrastructure (unit/integration/security)
- OpenAPI parsers (multiple open-source libraries available)
- Neo4j graph database (proven for relationship mapping)
- Vector search (pgvector, Pinecone) for semantic queries

**⚠️ What Problems Exist:**
- Manual migration analysis costs $200-500/hour × 100s hours = $50k per 1000 endpoints
- Consultant knowledge lost when engagement ends
- Inconsistent mapping quality (human error, incomplete documentation)
- Platform metadata often outdated or missing descriptions
- No tooling for functional equivalence (only infrastructure migration tools exist)

**❌ What's Missing:**
- Automated functional mapping capability (greenfield opportunity)
- LLM-powered semantic understanding of endpoint functionality
- Confidence scoring for migration decisions
- Graph-based storage for system relationships
- Conversational agent interface for developers
- Real-world test dataset for mapping accuracy validation

### Architecture

**Proposed Structure** (mirrors Obsidian_Agent):
```
src/
├── agent/                    # Pydantic AI orchestration
├── api/                      # FastAPI + OpenAI-compatible endpoints
├── tools/                    # 5 independent vertical slices
│   ├── platform_ingest/      # Parse OpenAPI/GraphQL/SQL
│   ├── mapping_engine/       # Semantic + structural mapping
│   ├── query_handler/        # Answer "where is X?" queries
│   ├── gap_detector/         # Find unmapped functionality
│   └── report_generator/     # Export guides (MD/JSON/CSV)
└── shared/
    ├── config.py             # Settings, env vars
    ├── logging.py            # Structlog (AI-optimized)
    ├── storage.py            # Neo4j + pgvector clients
    └── validators.py         # Security, input validation

tests/
├── tools/                    # Unit tests (mirror src/)
├── integration/              # Multi-tool workflows
└── fixtures/                 # Real-world API specs for testing
```

### Dependencies

**Existing Obsidian_Agent Components to Reuse:**
- `src/shared/config.py` - Settings management pattern
- `src/shared/logging.py` - Structured logging with get_logger()
- `src/agent/schemas.py` - AgentDependencies injection pattern
- Testing patterns from `tests/conftest.py` - Fixtures and test structure

**New Libraries Required:**
- `neo4j` - Graph database driver for system relationships
- `pgvector` or `pinecone-client` - Vector search for semantic queries
- `openai` - Embeddings + LLM mapping (API client)
- `prance` or `openapi-spec-validator` - OpenAPI 2.0/3.0 parsing
- `graphql-core` - GraphQL schema parsing
- `sqlparse` - SQL DDL parsing for database schemas

**External Services:**
- Neo4j database (Docker for dev, managed service for prod)
- OpenAI API (embeddings + GPT-4 for semantic mapping)
- Optional: Pinecone (if not using pgvector)

---

## Problem Domain Analysis

### Manual Process (Status Quo)

**Discovery Phase** (2-4 weeks):
- Analysts interview stakeholders
- Read legacy system documentation (often outdated)
- Trace API calls through code
- Build spreadsheets mapping systems

**Analysis Phase** (4-8 weeks):
- Identify functional boundaries
- Map legacy→modern equivalence
- Document gaps and overlaps
- Create migration runbooks

**Issues**:
- Human-intensive (costly, slow)
- Inconsistent analysis quality
- Knowledge loss when consultants leave
- Difficult to update as platforms evolve

**Real-World Example:**
```
Legacy Platform (Monolith)
├── OrderService (SOAP API)
│   └── getOrderDetails(orderId) → XML
├── CustomerService (REST)
│   └── GET /customers/{id}
└── InventoryDB (Oracle)
    └── ITEMS table

Modern Platform (Microservices)
├── OrderManagementAPI (GraphQL)
│   └── query { order(id) { ... } }
├── CustomerDataAPI (REST)
│   └── GET /api/v2/customers/{id}
├── InventoryService (gRPC)
└── Product Catalog (PostgreSQL)

Question: "Where do I get order details in the new platform?"
Answer: "OrderManagementAPI.query.order + CustomerDataAPI for linked customer data"
```

### User Personas

**1. Migration Architect**
- Needs: High-level system mapping, gap analysis, risk assessment
- Pain: Manually documenting hundreds of endpoints/services
- Value: Automated architecture comparison, visual dependency graphs

**2. Application Developer**
- Needs: Specific API mappings (legacy endpoint → modern equivalent)
- Pain: "Which new service do I call? What changed in the schema?"
- Value: Code-level mappings with transformation examples

**3. QA Engineer**
- Needs: Test coverage verification (did we migrate all functionality?)
- Pain: Unknown unknowns—missed edge cases
- Value: Automated functional coverage reports

**4. Project Manager**
- Needs: Migration progress tracking, risk reporting
- Pain: No visibility into migration completeness
- Value: Dashboards showing mapped vs unmapped functionality

### Success Criteria

**Must Have:**
- ✅ Ingest legacy platform metadata (APIs, databases, configs)
- ✅ Ingest modern platform metadata (same sources)
- ✅ Map functional equivalence with confidence scores
- ✅ Answer queries: "Where is X functionality in the new platform?"
- ✅ Generate migration guides per functionality

**Should Have:**
- 🎯 Identify unmapped functionality (gaps)
- 🎯 Detect overlapping/redundant mappings
- 🎯 Suggest data transformation patterns
- 🎯 Track migration progress over time

**Could Have:**
- 💡 Generate migration code snippets
- 💡 Integrate with CI/CD for validation
- 💡 Compare performance characteristics (latency, throughput)
- 💡 Estimate migration effort (story points)

---

## Research: Existing Solutions

### Commercial Tools

**1. AWS Migration Hub**
- **What it does**: Tracks cloud migration progress
- **Limitations**: AWS-centric, infrastructure-focused (not app logic)
- **Relevance**: Good for VM→cloud, not legacy→modern app mapping

**2. Cloudamize**
- **What it does**: Analyzes infrastructure for cloud readiness
- **Limitations**: Focuses on sizing/cost, not functional equivalence
- **Relevance**: Complementary, not competitive

**3. CAST Highlight**
- **What it does**: Source code analysis for complexity/risk
- **Limitations**: Code metrics, not system-to-system mapping
- **Relevance**: Could be data source for our tool

**4. Consulting Firms (Manual)**
- **Examples**: Deloitte, Accenture, ThoughtWorks
- **Approach**: Human analysts build spreadsheets
- **Cost**: $200-500/hour × 100s of hours
- **Our Advantage**: Automated, continuously updated, 10-100x cheaper

### Open Source / Academic

**1. Archie (Architecture Analysis)**
- **Focus**: Dependency extraction from codebases
- **Relevance**: Could feed our tool with legacy system structure

**2. Neo4j Graph Analysis**
- **Approach**: Model systems as graphs, query relationships
- **Relevance**: Excellent storage backend for our mappings

**3. API Blueprint / OpenAPI**
- **Approach**: Standardized API documentation
- **Relevance**: Input format for modern platform analysis

### Gap: No Automated Functional Mapping Tool

**Key Insight**: Existing tools focus on infrastructure or code quality, NOT functional equivalence mapping. This is a greenfield opportunity.

---

## Architecture Design (Vertical Slice Pattern)

### Application of Obsidian_Agent Principles

**1. Vertical Slice Architecture**
```
src/
├── agent/                    # Core orchestration (Pydantic AI)
├── api/                      # FastAPI endpoints (OpenAI-compatible)
├── tools/                    # Independent slices
│   ├── platform_ingest/      # Tool: Ingest platform metadata
│   ├── schema_analyzer/      # Tool: Analyze API schemas
│   ├── mapping_engine/       # Tool: Map legacy→modern
│   ├── gap_detector/         # Tool: Find unmapped functionality
│   ├── query_handler/        # Tool: Answer "where is X?" queries
│   └── report_generator/     # Tool: Generate migration guides
└── shared/                   # Cross-cutting concerns
    ├── config.py             # Settings, env vars
    ├── logging.py            # Structlog (AI-optimized)
    ├── storage.py            # Neo4j graph DB client
    └── validators.py         # Security, input validation
```

**2. Each Tool Follows Pattern**
```
tools/platform_ingest/
├── __init__.py
├── schemas.py        # Pydantic models (PlatformMetadata, IngestRequest)
├── service.py        # Business logic (parse APIs, extract schemas)
└── tool.py           # Agent tool registration (@agent.tool)
```

**3. Core Principles Applied**
- **TYPE SAFETY**: All functions typed, strict mypy
- **KISS**: Simple solutions over abstractions
- **YAGNI**: Build only what's needed for MVP
- **Agent-Optimized**: Tool docstrings guide LLM selection

### Data Models (Core Schemas)

**Platform Metadata Schema**
```python
from pydantic import BaseModel, Field
from enum import Enum

class TechStackType(str, Enum):
    REST_API = "rest_api"
    GRAPHQL = "graphql"
    GRPC = "grpc"
    SOAP = "soap"
    DATABASE = "database"
    MESSAGE_QUEUE = "message_queue"
    BATCH_JOB = "batch_job"

class EndpointMetadata(BaseModel):
    """Metadata for a single API endpoint or database operation."""
    id: str                          # Unique identifier
    name: str                        # e.g., "getOrderDetails"
    type: TechStackType
    http_method: str | None = None   # GET, POST, etc.
    path: str | None = None          # /api/orders/{id}
    request_schema: dict | None = None
    response_schema: dict | None = None
    description: str = ""
    tags: list[str] = Field(default_factory=list)  # ["orders", "legacy"]
    system_name: str                 # "OrderService"
    platform: str                    # "legacy" or "modern"

class PlatformMetadata(BaseModel):
    """Complete metadata for a platform (legacy or modern)."""
    platform_id: str
    platform_name: str               # "Legacy Monolith" or "Modern Microservices"
    platform_type: str               # "legacy" or "modern"
    endpoints: list[EndpointMetadata]
    databases: list[DatabaseMetadata]
    dependencies: dict[str, list[str]]  # System→[dependent systems]
    tech_stack_summary: dict[str, int]  # {"rest_api": 45, "soap": 12, ...}
    ingestion_date: str
    metadata_sources: list[str]      # ["swagger.json", "db_schema.sql"]
```

**Mapping Schema**
```python
class MappingConfidence(str, Enum):
    HIGH = "high"           # >90% confident (exact match)
    MEDIUM = "medium"       # 60-90% (similar, needs review)
    LOW = "low"            # <60% (possible match, verify)
    NONE = "none"          # No equivalent found

class FunctionalMapping(BaseModel):
    """Maps a legacy functionality to modern equivalent(s)."""
    mapping_id: str
    legacy_endpoint: EndpointMetadata
    modern_endpoints: list[EndpointMetadata]  # Can be 1:N mapping
    confidence: MappingConfidence
    reasoning: str          # LLM explanation of why mapped
    transformation_notes: str  # "XML→JSON, add auth header"
    data_changes: list[str]    # ["customer_id is now uuid", "status codes changed"]
    verification_status: str   # "pending", "verified", "rejected"
    mapped_by: str            # "ai-agent" or "human-user@example.com"
    mapped_at: str

class GapAnalysis(BaseModel):
    """Unmapped legacy functionality (migration risk)."""
    legacy_endpoint: EndpointMetadata
    gap_type: str          # "unmapped", "deprecated", "replaced_by_feature"
    impact_assessment: str # "high", "medium", "low"
    suggested_action: str  # "Migrate to ModernService.createOrder"
    stakeholder_notes: str
```

### Tool Interfaces (Agent-Facing)

**Tool 1: Platform Ingestion**
```python
@agent.tool
async def platform_ingest(
    ctx: RunContext[AgentDependencies],
    platform_name: str,
    platform_type: str,  # "legacy" or "modern"
    metadata_sources: list[str],  # ["openapi.json", "database_schema.sql"]
    source_format: str = "auto",  # "openapi", "graphql_schema", "sql", "auto"
    response_format: str = "concise"
) -> str:
    """Ingest and parse platform metadata from various sources.

    Use this when you need to:
    - Load legacy or modern platform architecture for analysis
    - Parse API specifications (OpenAPI, GraphQL schemas)
    - Extract database schemas from SQL dumps or ORM definitions
    - Build the foundation for migration mapping

    Do NOT use this for:
    - Querying existing platform data (use platform_query instead)
    - Mapping functionality (use mapping_engine instead)
    - Generating reports (use report_generator instead)

    Args:
        platform_name: Human-readable name (e.g., "Legacy Monolith v2.1")
        platform_type: Must be "legacy" or "modern"
        metadata_sources: List of file paths or URLs to ingest
            Examples: ["./specs/legacy-api.yaml", "https://api.new.com/graphql"]
        source_format: Format hint for parsing
            - "auto": Detect from file extension/content (default)
            - "openapi": OpenAPI 2.0/3.0 spec
            - "graphql_schema": GraphQL SDL
            - "sql": Database schema dump
            - "postman": Postman collection
        response_format: Output verbosity
            - "minimal": Success/failure + endpoint count (~50 tokens)
            - "concise": Summary + sample endpoints (~200 tokens)
            - "detailed": Full parse results with warnings (~1000+ tokens)

    Returns:
        Ingestion summary with endpoint count, warnings, and platform_id.

    Performance Notes:
        - Minimal: ~50 tokens (use after initial ingestion)
        - Concise: ~200 tokens (default, good for verification)
        - Detailed: ~1000+ tokens (use for debugging parse errors)
        - Execution time: 2-10s for typical APIs (100-500 endpoints)
        - Max file size: 50MB (larger files need chunking)

    Examples:
        # Ingest legacy platform from OpenAPI spec
        platform_ingest(
            platform_name="Legacy Order System",
            platform_type="legacy",
            metadata_sources=["./legacy/openapi.yaml"],
            response_format="concise"
        )

        # Ingest modern GraphQL API from URL
        platform_ingest(
            platform_name="Modern Microservices",
            platform_type="modern",
            metadata_sources=["https://api.newplatform.com/graphql/schema"],
            source_format="graphql_schema",
            response_format="minimal"
        )

        # Ingest database schema for data migration
        platform_ingest(
            platform_name="Legacy Oracle DB",
            platform_type="legacy",
            metadata_sources=["./schemas/oracle_dump.sql"],
            source_format="sql"
        )
    """
```

**Tool 2: Mapping Engine**
```python
@agent.tool
async def map_functionality(
    ctx: RunContext[AgentDependencies],
    legacy_platform_id: str,
    modern_platform_id: str,
    mapping_strategy: str = "semantic",  # "semantic", "structural", "hybrid"
    confidence_threshold: float = 0.6,
    batch_mode: bool = True,
    response_format: str = "concise"
) -> str:
    """Map legacy platform functionality to modern platform equivalents.

    Use this when you need to:
    - Create initial mappings between legacy and modern systems
    - Identify which modern endpoints replace legacy ones
    - Generate confidence scores for each mapping
    - Build the foundation for migration planning

    Do NOT use this for:
    - Ingesting platforms (use platform_ingest first)
    - Querying specific mappings (use query_mapping instead)
    - Generating reports (use report_generator after mapping)

    Args:
        legacy_platform_id: ID from platform_ingest()
        modern_platform_id: ID from platform_ingest()
        mapping_strategy: How to determine equivalence
            - "semantic": LLM-based understanding of functionality (slower, accurate)
            - "structural": Path/schema similarity (fast, may miss renamed endpoints)
            - "hybrid": Combine both (balanced, recommended)
        confidence_threshold: Minimum confidence to return (0.0-1.0)
            - 0.9: Only near-certain matches
            - 0.6: Include probable matches (default)
            - 0.3: Show even weak possibilities (for gap analysis)
        batch_mode: Process all endpoints at once (True) or one-by-one (False)
        response_format: Output detail level
            - "minimal": Count of mappings created (~50 tokens)
            - "concise": Summary + confidence distribution (~300 tokens)
            - "detailed": Full mapping list with reasoning (~2000+ tokens)

    Returns:
        Mapping results with counts by confidence level, sample mappings.

    Performance Notes:
        - Minimal: ~50 tokens (use for progress tracking)
        - Concise: ~300 tokens (default, good overview)
        - Detailed: ~2000+ tokens (use for reviewing mappings)
        - Execution time:
            - Structural: 10-30s for 100 endpoints
            - Semantic: 2-5 min for 100 endpoints (LLM calls)
            - Hybrid: 3-6 min for 100 endpoints
        - Cost: Semantic strategy uses ~50k tokens per 100 endpoints

    Examples:
        # Quick structural mapping for initial pass
        map_functionality(
            legacy_platform_id="legacy-abc123",
            modern_platform_id="modern-xyz789",
            mapping_strategy="structural",
            response_format="concise"
        )

        # High-confidence semantic mapping for critical systems
        map_functionality(
            legacy_platform_id="legacy-abc123",
            modern_platform_id="modern-xyz789",
            mapping_strategy="semantic",
            confidence_threshold=0.9,
            response_format="detailed"
        )

        # Hybrid approach for production use
        map_functionality(
            legacy_platform_id="legacy-abc123",
            modern_platform_id="modern-xyz789",
            mapping_strategy="hybrid",
            confidence_threshold=0.6
        )
    """
```

**Tool 3: Query Handler**
```python
@agent.tool
async def query_mapping(
    ctx: RunContext[AgentDependencies],
    query: str,
    platform_id: str,
    query_type: str = "functionality",  # "functionality", "endpoint", "system"
    response_format: str = "concise"
) -> str:
    """Answer questions about functionality mapping across platforms.

    Use this when you need to:
    - Find modern equivalent of a legacy endpoint ("Where is getOrderDetails?")
    - Check if functionality is mapped or unmapped
    - Understand transformation requirements for migration
    - Verify mapping confidence and reasoning

    Do NOT use this for:
    - Creating mappings (use map_functionality instead)
    - Bulk analysis (use report_generator instead)
    - Platform ingestion (use platform_ingest instead)

    Args:
        query: Natural language question
            Examples:
            - "Where is the legacy getOrderDetails endpoint in the new platform?"
            - "Which modern services replaced the OrderService?"
            - "Show me all unmapped legacy endpoints"
        platform_id: Which platform context to search
        query_type: Type of query
            - "functionality": Search by what it does (semantic)
            - "endpoint": Search by name/path (exact match)
            - "system": Search by service/system name
        response_format: Output detail
            - "minimal": Direct answer only (~50 tokens)
            - "concise": Answer + transformation notes (~200 tokens)
            - "detailed": Full mapping with reasoning, examples (~800 tokens)

    Returns:
        Query answer with mapping details, confidence, transformation notes.

    Performance Notes:
        - Minimal: ~50 tokens (quick lookups)
        - Concise: ~200 tokens (default, includes context)
        - Detailed: ~800+ tokens (comprehensive migration guide)
        - Execution time: <1s for endpoint queries, 2-5s for semantic search
        - Uses vector search for functionality queries (requires embedding)

    Examples:
        # Quick endpoint lookup
        query_mapping(
            query="Where is getOrderDetails in the new platform?",
            platform_id="legacy-abc123",
            query_type="endpoint",
            response_format="concise"
        )

        # Semantic functionality search
        query_mapping(
            query="How do I get customer order history with payment details?",
            platform_id="legacy-abc123",
            query_type="functionality",
            response_format="detailed"
        )

        # Find all unmapped endpoints
        query_mapping(
            query="Show me unmapped legacy endpoints",
            platform_id="legacy-abc123",
            query_type="functionality",
            response_format="minimal"
        )
    """
```

**Tool 4: Gap Detector**
```python
@agent.tool
async def detect_gaps(
    ctx: RunContext[AgentDependencies],
    legacy_platform_id: str,
    modern_platform_id: str,
    min_confidence: float = 0.6,
    include_low_confidence: bool = True,
    response_format: str = "concise"
) -> str:
    """Identify unmapped legacy functionality (migration gaps and risks).

    Use this when you need to:
    - Find legacy endpoints with no modern equivalent
    - Identify low-confidence mappings needing human review
    - Assess migration risk and completeness
    - Prioritize migration work by impact

    Do NOT use this for:
    - Creating mappings (use map_functionality instead)
    - Querying specific functionality (use query_mapping instead)
    - Generating full reports (use report_generator instead)

    Args:
        legacy_platform_id: Legacy platform to analyze
        modern_platform_id: Modern platform to compare against
        min_confidence: Threshold below which mappings are flagged
        include_low_confidence: Include weak mappings or only unmapped?
            - True: Show unmapped + low confidence (comprehensive)
            - False: Only show completely unmapped (high priority)
        response_format: Output detail
            - "minimal": Count of gaps by priority (~50 tokens)
            - "concise": Summary + top 10 gaps (~400 tokens)
            - "detailed": Full gap list with impact analysis (~1500+ tokens)

    Returns:
        Gap analysis with unmapped endpoints, risk assessment, suggestions.

    Performance Notes:
        - Minimal: ~50 tokens (dashboard view)
        - Concise: ~400 tokens (planning meetings)
        - Detailed: ~1500+ tokens (comprehensive review)
        - Execution time: 5-15s (depends on platform size)
        - Includes impact scoring (usage frequency × business criticality)

    Examples:
        # Quick gap count for status reporting
        detect_gaps(
            legacy_platform_id="legacy-abc123",
            modern_platform_id="modern-xyz789",
            response_format="minimal"
        )

        # Comprehensive gap analysis for planning
        detect_gaps(
            legacy_platform_id="legacy-abc123",
            modern_platform_id="modern-xyz789",
            include_low_confidence=True,
            response_format="detailed"
        )

        # High-priority gaps only
        detect_gaps(
            legacy_platform_id="legacy-abc123",
            modern_platform_id="modern-xyz789",
            min_confidence=0.9,
            include_low_confidence=False
        )
    """
```

**Tool 5: Report Generator**
```python
@agent.tool
async def generate_migration_report(
    ctx: RunContext[AgentDependencies],
    legacy_platform_id: str,
    modern_platform_id: str,
    report_type: str = "full",  # "full", "gaps", "mappings", "executive"
    output_format: str = "markdown",  # "markdown", "json", "csv"
    response_format: str = "concise"
) -> str:
    """Generate comprehensive migration analysis reports.

    Use this when you need to:
    - Create documentation for migration planning
    - Export mappings for stakeholder review
    - Generate executive summaries for leadership
    - Produce CSV for import into project management tools

    Do NOT use this for:
    - Interactive queries (use query_mapping instead)
    - Real-time gap detection (use detect_gaps instead)
    - Platform ingestion (use platform_ingest instead)

    Args:
        legacy_platform_id: Source platform
        modern_platform_id: Target platform
        report_type: What to include
            - "full": Everything (mappings, gaps, stats, recommendations)
            - "gaps": Only unmapped/low-confidence items
            - "mappings": Only confirmed mappings
            - "executive": High-level summary for leadership
        output_format: Export format
            - "markdown": Human-readable docs (default)
            - "json": Machine-readable for tooling
            - "csv": Spreadsheet for PM tools (Jira, etc.)
        response_format: Agent response verbosity
            - "minimal": Report generated, link only (~50 tokens)
            - "concise": Summary stats + link (~200 tokens)
            - "detailed": Full preview + link (~1000+ tokens)

    Returns:
        Report summary with download link, key statistics.

    Performance Notes:
        - Minimal: ~50 tokens (batch reporting)
        - Concise: ~200 tokens (default)
        - Detailed: ~1000+ tokens (includes report preview)
        - Execution time: 10-60s (depends on platform size)
        - Report files saved to: ./reports/{platform_id}/migration-{date}.{format}

    Examples:
        # Full migration guide in Markdown
        generate_migration_report(
            legacy_platform_id="legacy-abc123",
            modern_platform_id="modern-xyz789",
            report_type="full",
            output_format="markdown"
        )

        # Gap analysis CSV for Jira import
        generate_migration_report(
            legacy_platform_id="legacy-abc123",
            modern_platform_id="modern-xyz789",
            report_type="gaps",
            output_format="csv",
            response_format="minimal"
        )

        # Executive summary for stakeholders
        generate_migration_report(
            legacy_platform_id="legacy-abc123",
            modern_platform_id="modern-xyz789",
            report_type="executive",
            output_format="markdown"
        )
    """
```

---

## Technical Implementation Strategy

### Phase 1: Foundation (Week 1-2)

**Goal**: Set up project structure with core infrastructure

**Tasks**:
1. **Project Scaffolding**
   - Initialize with `uv` + FastAPI + Pydantic AI
   - Configure mypy strict mode
   - Set up Ruff linting
   - Add structlog for logging
   - Create vertical slice directory structure

2. **Data Storage Layer**
   - Evaluate Neo4j vs PostgreSQL + pgvector
   - Implement graph storage for system relationships
   - Design schema for platforms, endpoints, mappings
   - Add migration scripts

3. **Security & Validation**
   - Input validation (prevent injection attacks)
   - Rate limiting for API endpoints
   - Authentication (API keys initially)
   - Audit logging

4. **Testing Infrastructure**
   - Unit test framework (pytest)
   - Integration test setup
   - Mock platform data generators
   - Test fixtures for common scenarios

**Validation**:
```bash
uv run mypy src/           # Type checking passes
uv run ruff check src/      # Linting passes
uv run pytest tests/ -v     # All tests pass
```

### Phase 2: Platform Ingestion (Week 3-4)

**Goal**: Ingest and parse legacy/modern platform metadata

**Implementation**:
1. **OpenAPI Parser**
   - Parse OpenAPI 2.0/3.0 specs
   - Extract endpoints, schemas, descriptions
   - Handle references ($ref resolution)
   - Validate spec completeness

2. **GraphQL Schema Parser**
   - Parse SDL (Schema Definition Language)
   - Extract queries, mutations, types
   - Map to common EndpointMetadata format

3. **Database Schema Parser**
   - Parse SQL DDL (CREATE TABLE, etc.)
   - Extract tables, columns, relationships
   - Identify stored procedures as "endpoints"

4. **Generic Metadata Extractor**
   - Postman collections
   - HAR files (HTTP Archive)
   - Swagger UI scraping (fallback)

**Testing**:
- Unit tests with real-world OpenAPI examples
- GraphQL schema from GitHub, Shopify, etc.
- SQL dumps from sample databases
- Edge cases: malformed specs, missing descriptions

**Validation**:
```python
# Test platform ingestion
result = await platform_ingest_service(
    platform_name="Test Legacy",
    sources=["./fixtures/petstore-openapi.yaml"]
)
assert result.endpoint_count == 20
assert result.warnings == []
```

### Phase 3: Mapping Engine (Week 5-7)

**Goal**: Core AI-powered mapping functionality

**Implementation**:

**1. Structural Mapping (Baseline)**
```python
async def structural_map(
    legacy: EndpointMetadata,
    modern_endpoints: list[EndpointMetadata]
) -> list[tuple[EndpointMetadata, float]]:
    """Map based on path/method/schema similarity."""
    scores = []
    for modern in modern_endpoints:
        score = 0.0

        # Path similarity (0-0.4)
        if legacy.path and modern.path:
            score += path_similarity(legacy.path, modern.path) * 0.4

        # Method match (0-0.2)
        if legacy.http_method == modern.http_method:
            score += 0.2

        # Schema similarity (0-0.4)
        if legacy.response_schema and modern.response_schema:
            score += schema_overlap(
                legacy.response_schema,
                modern.response_schema
            ) * 0.4

        scores.append((modern, score))

    return sorted(scores, key=lambda x: x[1], reverse=True)
```

**2. Semantic Mapping (LLM-Based)**
```python
async def semantic_map(
    legacy: EndpointMetadata,
    modern_endpoints: list[EndpointMetadata],
    llm_client: PydanticAI
) -> list[tuple[EndpointMetadata, float, str]]:
    """Map based on functional understanding."""

    # Create prompt for LLM
    prompt = f"""
    Legacy Endpoint:
    - Name: {legacy.name}
    - Description: {legacy.description}
    - Path: {legacy.path}
    - Request Schema: {legacy.request_schema}
    - Response Schema: {legacy.response_schema}

    Modern Endpoints (candidates):
    {format_candidates(modern_endpoints)}

    Task: Which modern endpoint(s) provide equivalent functionality?
    Return JSON: [
        {{"modern_id": "...", "confidence": 0.0-1.0, "reasoning": "..."}}
    ]
    """

    result = await llm_client.run(prompt, response_format=MappingResult)
    return [(find_endpoint(m.modern_id), m.confidence, m.reasoning)
            for m in result.mappings]
```

**3. Hybrid Strategy**
- Run structural mapping first (fast pre-filter)
- Use semantic mapping for top N candidates
- Combine scores with weighted average
- Cache LLM results to reduce cost

**Testing**:
- Create 20+ known good/bad mapping pairs
- Measure precision/recall for each strategy
- Test edge cases: renamed endpoints, combined/split services
- Validate confidence scores match human judgment

### Phase 4: Query & Gap Detection (Week 8-9)

**Goal**: Answer user queries and identify unmapped functionality

**Implementation**:

**1. Vector Search for Semantic Queries**
```python
# Use pgvector or Pinecone for similarity search
embeddings = await embed_endpoints(all_endpoints)
store_in_vector_db(embeddings)

async def query_by_functionality(query: str) -> list[EndpointMetadata]:
    query_embedding = await embed_text(query)
    results = vector_db.search(query_embedding, top_k=10)
    return results
```

**2. Gap Analysis**
```python
async def detect_gaps(
    legacy_platform_id: str,
    modern_platform_id: str,
    threshold: float
) -> GapAnalysis:
    # Get all mappings
    mappings = await get_mappings(legacy_platform_id, modern_platform_id)

    # Find unmapped
    legacy_endpoints = await get_endpoints(legacy_platform_id)
    mapped_ids = {m.legacy_endpoint.id for m in mappings}
    unmapped = [e for e in legacy_endpoints if e.id not in mapped_ids]

    # Find low-confidence
    low_conf = [m for m in mappings if m.confidence < threshold]

    return GapAnalysis(
        unmapped=unmapped,
        low_confidence=low_conf,
        total_legacy=len(legacy_endpoints),
        coverage_pct=(len(mapped_ids) / len(legacy_endpoints)) * 100
    )
```

**Testing**:
- Test query variations (synonyms, different phrasing)
- Verify gap detection catches all unmapped items
- Test impact scoring logic
- Validate prioritization algorithms

### Phase 5: Report Generation (Week 10)

**Goal**: Export analysis results in multiple formats

**Implementation**:
- Markdown templates (Jinja2)
- JSON export (Pydantic.model_dump_json())
- CSV export (pandas DataFrame)
- Executive summary generator (LLM-based)

**Report Types**:

**1. Full Migration Guide**
```markdown
# Migration Guide: Legacy System → Modern Platform

## Overview
- Total Legacy Endpoints: 145
- Mapped: 128 (88%)
- Unmapped: 17 (12%)
- Confidence Distribution:
  - High (>0.9): 95 (74%)
  - Medium (0.6-0.9): 33 (26%)
  - Low (<0.6): 0 (0%)

## Mappings
### OrderService.getOrderDetails
**Modern Equivalent**: OrderManagementAPI.query.order
**Confidence**: 0.95 (High)
**Transformation Notes**:
- Change from REST to GraphQL
- Add authentication header: `Authorization: Bearer {token}`
- Response format: XML → JSON
...
```

**2. Gap Analysis CSV**
```csv
legacy_endpoint,system,description,status,suggested_action,priority
CustomerService.getLegacyProfile,CustomerService,Get customer profile,UNMAPPED,Use CustomerDataAPI.getProfile,HIGH
...
```

### Phase 6: Agent Interface (Week 11-12)

**Goal**: Conversational AI interface for developers

**Implementation**:
- FastAPI + Pydantic AI agent
- OpenAI-compatible API (drop-in replacement)
- Streaming responses for long reports
- Tool registration with agent

**Example Conversation**:
```
User: "I'm migrating the OrderService. Where do I get order details in the new platform?"

Agent: Let me check the migration mappings...
[Uses query_mapping tool]

Agent: The legacy OrderService.getOrderDetails endpoint maps to:
**OrderManagementAPI.query.order** (GraphQL)

**Confidence**: 95% (High)

**Changes**:
- Protocol: REST → GraphQL
- Auth: Basic → Bearer token
- Response: XML → JSON

**Example Query**:
```graphql
query {
  order(id: "12345") {
    id
    status
    items { ... }
    customer { ... }
  }
}
```

**Data Transformations**:
- `order_id` (integer) → `id` (UUID string)
- `status_code` (enum) → `status` (lowercase string)

Need help with the migration?
```

---

## Storage Architecture

### Graph Database (Neo4j)

**Why Neo4j?**
- Natural fit for system relationships
- Powerful query language (Cypher)
- Efficient for "where does this lead?" queries
- Supports graph algorithms (shortest path, centrality)

**Schema**:
```cypher
// Nodes
(:Platform {id, name, type, ingestion_date})
(:System {id, name, platform_id})
(:Endpoint {id, name, path, method, type, description})
(:Schema {id, structure})

// Relationships
(:Endpoint)-[:BELONGS_TO]->(:System)
(:System)-[:PART_OF]->(:Platform)
(:Endpoint)-[:HAS_SCHEMA]->(:Schema)
(:Endpoint)-[:DEPENDS_ON]->(:Endpoint)

// Mappings
(:Endpoint)-[:MAPS_TO {confidence, reasoning, verified}]->(:Endpoint)
(:Endpoint)-[:NO_MAPPING {reason}]->(:Platform)
```

**Example Query**:
```cypher
// Find modern equivalent of legacy endpoint
MATCH (legacy:Endpoint {id: $legacy_id})-[:MAPS_TO]->(modern:Endpoint)
RETURN modern, mapping.confidence, mapping.reasoning
ORDER BY mapping.confidence DESC
```

### Vector Store (pgvector or Pinecone)

**Purpose**: Semantic search for functionality queries

**Schema**:
```sql
CREATE TABLE endpoint_embeddings (
    endpoint_id UUID PRIMARY KEY,
    embedding VECTOR(1536),  -- OpenAI ada-002 dimension
    metadata JSONB,
    platform_id UUID
);

CREATE INDEX ON endpoint_embeddings USING ivfflat (embedding vector_cosine_ops);
```

**Usage**:
```python
# Find similar endpoints by functionality
similar = await vector_db.search(
    query_embedding=embed("get customer order history"),
    top_k=10,
    filter={"platform_id": modern_platform_id}
)
```

---

## Cost & Performance Analysis

### Cost Breakdown (Per 1000 Endpoints)

**1. Platform Ingestion**
- LLM Cost: $0 (structural parsing only)
- Storage: ~10 MB in Neo4j
- Time: 5-10 seconds
- **Total**: ~$0 per 1000 endpoints

**2. Structural Mapping**
- LLM Cost: $0 (rule-based)
- Compute: Minimal (O(N²) comparison)
- Time: 30 seconds for 1000 endpoints
- **Total**: ~$0

**3. Semantic Mapping (LLM)**
- Embeddings: $0.13 (1000 endpoints × 500 tokens avg × $0.0001/1k tokens)
- LLM Mapping: $5.00 (1000 comparisons × 1000 tokens × $0.005/1k tokens)
- Time: 3-5 minutes (parallel API calls)
- **Total**: ~$5.13 per 1000 endpoints

**4. Queries**
- Vector Search: <$0.001 per query (pgvector)
- LLM Refinement: $0.01 per query (if needed)
- Time: <1 second per query
- **Total**: ~$0.01 per query

**Comparison to Manual Analysis**:
- Consultant Rate: $200/hour
- Time per Endpoint: 15 minutes (discovery + mapping)
- Cost for 1000 Endpoints: $200 × (1000 × 15min / 60min) = **$50,000**
- **AI Tool Cost**: ~$5 (for semantic mapping)
- **Savings**: 99.99% ($49,995 per 1000 endpoints)

### Performance Targets

**Ingestion**:
- ✅ 100 endpoints/second (structural parsing)
- ✅ <10 seconds for typical API spec (50-200 endpoints)

**Mapping**:
- ✅ Structural: 1000 endpoints in <30 seconds
- ✅ Semantic: 1000 endpoints in <5 minutes (parallel)
- ✅ Hybrid: 1000 endpoints in <6 minutes

**Queries**:
- ✅ Exact match: <100ms
- ✅ Semantic search: <1 second
- ✅ Gap analysis: <5 seconds

**Scalability**:
- ✅ Support platforms with 10,000+ endpoints
- ✅ Handle multiple concurrent users
- ✅ Cache frequently accessed mappings

---

## Risk Assessment & Mitigation

### Technical Risks

**Risk 1: LLM Hallucination (Incorrect Mappings)**
- **Impact**: High (bad migration decisions)
- **Likelihood**: Medium
- **Mitigation**:
  - Always show confidence scores
  - Require human verification for medium/low confidence
  - Implement feedback loop (users mark mappings as correct/wrong)
  - Use ensemble approach (multiple LLM calls, majority vote)
  - Conservative default: Flag as "needs review" if confidence < 0.8

**Risk 2: Incomplete Platform Metadata**
- **Impact**: High (gaps in analysis)
- **Likelihood**: High
- **Mitigation**:
  - Support multiple input formats (OpenAPI, GraphQL, Postman, etc.)
  - Allow manual metadata enrichment
  - Warn users about missing descriptions/schemas
  - Provide data quality score (% of endpoints with descriptions)

**Risk 3: Performance Issues at Scale**
- **Impact**: Medium (slow analysis)
- **Likelihood**: Medium
- **Mitigation**:
  - Use async I/O throughout
  - Batch LLM calls (GPT-4 batch API)
  - Cache embeddings and mappings
  - Implement progressive loading (show results as available)

**Risk 4: Schema Complexity (Nested, Polymorphic)**
- **Impact**: Medium (inaccurate schema comparisons)
- **Likelihood**: High
- **Mitigation**:
  - Normalize schemas to simplified format
  - Flatten nested structures for comparison
  - Use LLM for complex schema understanding
  - Allow users to provide schema mapping hints

### Business Risks

**Risk 5: Market Adoption (Companies Prefer Consultants)**
- **Impact**: High (no customers)
- **Likelihood**: Low-Medium
- **Mitigation**:
  - Target smaller companies (can't afford consultants)
  - Position as consultant augmentation tool (not replacement)
  - Freemium model (free for <100 endpoints)
  - Case studies showing time/cost savings

**Risk 6: Data Privacy (Customer Platform Metadata)**
- **Impact**: High (legal liability)
- **Likelihood**: Low (if addressed early)
- **Mitigation**:
  - On-premise deployment option
  - End-to-end encryption
  - No data retention (process and delete)
  - SOC 2 compliance for SaaS version
  - Open-source core (build trust)

---

## Go-to-Market Strategy

### MVP Feature Set (3 Months)

**Must Have**:
- ✅ Ingest OpenAPI specs (legacy + modern)
- ✅ Structural + semantic mapping
- ✅ Query interface ("Where is X?")
- ✅ Markdown report generation
- ✅ Confidence scores
- ✅ Gap analysis

**Nice to Have**:
- GraphQL schema support
- Database schema ingestion
- CSV export
- Human feedback loop

**Explicitly Out of Scope**:
- Code generation
- Performance comparison
- Cost estimation
- CI/CD integration

### Target Customers (Initial)

**Tier 1: Early Adopters** (Month 1-3)
- Startups modernizing legacy MVP
- Open-source projects (migration guides)
- Individual consultants (productivity tool)

**Tier 2: Growth** (Month 4-12)
- Mid-size companies ($10-100M revenue)
- Companies with documented APIs (OpenAPI/GraphQL)
- Platform teams in larger enterprises

**Tier 3: Enterprise** (Month 12+)
- Fortune 500 platform migrations
- Multi-year transformation programs
- Require: SOC 2, on-premise, custom integrations

### Pricing Model

**Freemium**:
- Free: Up to 100 endpoints total
- Pay-as-you-go: $0.05 per endpoint (semantic mapping)
- Pro: $500/month (unlimited endpoints, priority support)
- Enterprise: Custom pricing (on-premise, SLA, custom features)

**Example**:
- Small API (200 endpoints): $10 one-time
- Medium API (1000 endpoints): $50 one-time
- Large Platform (10,000 endpoints): $500 one-time OR Pro subscription

**Revenue Model**:
- Year 1: 100 customers × $500 avg = $50k MRR
- Year 2: 1000 customers × $500 avg = $500k MRR
- Year 3: Target enterprise contracts ($50k-500k each)

---

## Next Steps (If Moving to Implementation)

### Pre-Implementation Research

1. **Competitive Analysis Deep Dive**
   - Evaluate all existing tools (not just surface level)
   - Identify exact differentiation points
   - Talk to 10 potential users (problem validation)

2. **Technical Spikes**
   - Prototype LLM mapping accuracy (build test harness)
   - Test Neo4j vs PostgreSQL performance
   - Evaluate vector DB options (pgvector, Pinecone, Weaviate)
   - Benchmark OpenAPI parsing libraries

3. **User Research**
   - Interview migration architects (5-10 people)
   - Shadow a migration project (observe pain points)
   - Validate assumptions (do they want this tool?)

### Week 1-2 Tasks (If Greenlit)

1. **Project Setup**
   - Clone Obsidian_Agent structure
   - Replace Obsidian tools with migration tools
   - Set up Neo4j + pgvector
   - Configure CI/CD

2. **First Vertical Slice**
   - Implement `platform_ingest` tool (OpenAPI only)
   - Add unit tests
   - Deploy locally
   - Ingest 2 real-world APIs (Stripe, GitHub)

3. **Success Metric**:
   - Parse Stripe OpenAPI spec (500+ endpoints)
   - Store in Neo4j
   - Query via Cypher
   - Time: <10 seconds
   - Zero parsing errors

---

## Appendix: Alternative Approaches Considered

### Approach 1: Rule-Based System (No LLM)

**Pros**:
- Deterministic, explainable
- No API costs
- Fast

**Cons**:
- Requires extensive rule engineering
- Brittle (breaks on renamed endpoints)
- Can't handle semantic equivalence (e.g., "getUser" vs "fetchCustomer")

**Decision**: Rejected. LLM approach more robust.

### Approach 2: Manual Mapping UI Only

**Pros**:
- Simpler implementation
- No LLM accuracy concerns
- Full human control

**Cons**:
- Doesn't solve the manual labor problem
- Just digitizing spreadsheets
- No competitive advantage

**Decision**: Rejected. Automation is key value prop.

### Approach 3: Static Code Analysis

**Pros**:
- Catches runtime patterns (not just declared APIs)
- Can trace actual usage

**Cons**:
- Requires source code access (not always available)
- Language-specific (need parsers for Java, Python, Go, etc.)
- Complex implementation

**Decision**: Considered for Phase 2 enhancement, not MVP.

### Approach 4: SaaS-Only (No On-Premise)

**Pros**:
- Simpler deployment
- Easier to support
- Better unit economics

**Cons**:
- Enterprise customers require on-prem
- Data privacy concerns
- Limits addressable market

**Decision**: Hybrid (SaaS for SMB, on-prem option for enterprise).

---

## Common Pitfalls to Avoid

Based on risk analysis and technical considerations, avoid these implementation mistakes:

### Platform Ingestion Pitfalls

❌ **Don't** assume OpenAPI specs have complete descriptions - Many legacy specs lack descriptions (use structural mapping as fallback)
❌ **Don't** fail hard on malformed specs - Parse what you can, warn about gaps, allow manual enrichment
❌ **Don't** load entire spec into memory - Stream large files (>50MB) to prevent OOM errors
❌ **Don't** skip $ref resolution - Unresolved references break schema comparison
❌ **Don't** ignore spec versioning - OpenAPI 2.0 vs 3.0 have different structures (detect and handle both)

### Mapping Engine Pitfalls

❌ **Don't** use semantic mapping without structural pre-filter - Costs explode (filter to top N candidates first)
❌ **Don't** skip confidence thresholds - Low-confidence mappings (<0.6) need human review
❌ **Don't** assume 1:1 mappings - Legacy endpoints often split/merge into multiple modern endpoints
❌ **Don't** ignore schema normalization - Nested objects must be flattened for comparison
❌ **Don't** use synchronous LLM calls - Blocks event loop (use async + batch API)
❌ **Don't** forget to cache embeddings - Re-embedding same endpoints wastes money
❌ **Don't** trust LLM reasoning blindly - Always show confidence + reasoning to users

### Query & Gap Detection Pitfalls

❌ **Don't** use exact string matching for queries - "get order" should match "getOrderDetails" (use embeddings)
❌ **Don't** ignore partial mappings - Flag 1:N mappings as "complex migration" not "unmapped"
❌ **Don't** calculate gaps without filtering test endpoints - Exclude /health, /metrics from unmapped counts
❌ **Don't** skip impact scoring - All gaps aren't equal (prioritize by usage frequency)

### Storage & Performance Pitfalls

❌ **Don't** store full schemas in graph nodes - Store references, full schemas in separate store
❌ **Don't** run N+1 queries - Batch Cypher queries with UNWIND
❌ **Don't** skip vector index creation - Similarity search is unusable without proper indexing
❌ **Don't** use Cypher for full-text search - Use dedicated search (Elasticsearch) or vector search
❌ **Don't** forget connection pooling - Neo4j connections are expensive

### Security & Privacy Pitfalls

❌ **Don't** log full platform metadata - May contain sensitive business logic (log summaries only)
❌ **Don't** store API keys in mappings - Strip auth headers during ingestion
❌ **Don't** expose raw LLM prompts to users - May leak other customers' platform names
❌ **Don't** skip input validation - Malicious OpenAPI specs can cause DoS (file size limits, timeout parsing)

### Agent Interface Pitfalls

❌ **Don't** use vague error messages - "Mapping failed" → "Mapping failed: No description in legacy endpoint, try manual enrichment"
❌ **Don't** return full mappings for large platforms - Paginate results (max 50 per response)
❌ **Don't** forget token estimates - Users need to know response_format impact on costs
❌ **Don't** block on long-running operations - Use async tasks + polling for reports

### Business & Go-to-Market Pitfalls

❌ **Don't** promise 100% accuracy - LLMs hallucinate (promise "80%+ accuracy with confidence scores")
❌ **Don't** ignore consultant partnerships - They're customers not competitors (offer white-label)
❌ **Don't** skip data quality scoring - Warn users: "Only 30% of endpoints have descriptions - results may be low confidence"
❌ **Don't** forget feedback loop - Let users mark mappings as correct/incorrect (improves model)

---

## Success Criteria Template

After implementation, validate against these criteria:

### ✅ Functional Requirements

**Platform Ingestion**:
- [ ] Ingest OpenAPI 2.0/3.0 specs with >95% endpoint extraction rate
- [ ] Ingest GraphQL SDL schemas with query/mutation/type extraction
- [ ] Ingest SQL DDL with table/column/relationship extraction
- [ ] Handle malformed specs gracefully (parse what's possible, warn about rest)
- [ ] Support file upload and URL ingestion
- [ ] Complete ingestion of 1000 endpoints in <10 seconds

**Mapping Engine**:
- [ ] Structural mapping achieves >60% precision on renamed endpoints
- [ ] Semantic mapping achieves >80% precision on functional equivalence
- [ ] Hybrid strategy combines both with configurable weights
- [ ] Confidence scores correlate with human judgment (validate on test set)
- [ ] Detect 1:N and N:1 mappings correctly
- [ ] Process 1000 endpoint pairs in <6 minutes (hybrid strategy)

**Query & Gap Detection**:
- [ ] Natural language queries return correct mappings (>80% accuracy)
- [ ] Vector search finds semantically similar endpoints in <1 second
- [ ] Gap analysis identifies all unmapped endpoints
- [ ] Impact scoring prioritizes gaps correctly
- [ ] Pagination works for large result sets

**Report Generation**:
- [ ] Generate Markdown migration guides with all mappings
- [ ] Export gap analysis to CSV for Jira/PM tools
- [ ] Executive summary highlights key stats (coverage %, high-risk gaps)
- [ ] Reports include transformation notes (protocol changes, schema diffs)
- [ ] Report generation completes in <60 seconds for 1000 endpoints

### ✅ Non-Functional Requirements

**Performance**:
- [ ] API response time <200ms for queries (p95)
- [ ] Concurrent users supported (min 10 simultaneous analyses)
- [ ] Database queries optimized (no N+1, proper indexing)
- [ ] Memory usage <2GB for 10,000 endpoint platform
- [ ] Graceful degradation under load (rate limiting, queue)

**Type Safety & Code Quality**:
- [ ] All functions have type annotations (strict mypy passes)
- [ ] No `Any` types without justification
- [ ] Pydantic models validate all inputs
- [ ] 90%+ test coverage on service layer
- [ ] 80%+ overall test coverage
- [ ] Linters pass: `ruff check` and `mypy` with zero errors

**Logging & Observability**:
- [ ] Structured logging for all operations (entry, exit, errors)
- [ ] Performance metrics logged (duration_ms for key operations)
- [ ] Correlation IDs for request tracing
- [ ] Error logs include actionable context (what failed, why, how to fix)
- [ ] No sensitive data in logs (API keys, customer data masked)

**Security**:
- [ ] Input validation prevents injection attacks
- [ ] API authentication required (API keys minimum)
- [ ] Rate limiting prevents abuse
- [ ] File upload size limits enforced (max 50MB)
- [ ] Parsing timeout prevents DoS (max 30s per spec)
- [ ] Audit logging for all data access

**Agent Tool Quality**:
- [ ] Tool docstrings follow template (Use this when / Do NOT use / Performance Notes / Examples)
- [ ] Token efficiency implemented (minimal/concise/detailed response formats)
- [ ] Error messages clear and actionable
- [ ] Examples use realistic data (not foo/bar)
- [ ] Performance characteristics documented

### ✅ Documentation Requirements

- [ ] README with architecture overview and quick start
- [ ] Tool usage examples for all 5 tools
- [ ] API documentation (OpenAPI spec for FastAPI endpoints)
- [ ] Deployment guide (Docker Compose for dev, production setup)
- [ ] Environment variables documented (.env.example)
- [ ] Testing guide (how to run unit/integration tests)
- [ ] Performance benchmarks documented

### ✅ Testing Requirements

**Unit Tests**:
- [ ] All service functions tested (90%+ coverage)
- [ ] All Pydantic schemas validated (edge cases, validation errors)
- [ ] Mock LLM calls to avoid API costs in tests
- [ ] Fixture data for common scenarios (Stripe API, GitHub API)

**Integration Tests**:
- [ ] End-to-end workflow: ingest → map → query → report
- [ ] Cross-tool integration (query uses mappings from mapping_engine)
- [ ] Database integration (Neo4j, pgvector)
- [ ] Error handling across tool boundaries

**Validation Tests**:
- [ ] Test on 3 real-world API pairs (known good mappings)
- [ ] Measure precision/recall vs human-labeled ground truth
- [ ] Target: >80% precision, >70% recall on semantic mappings

### ✅ Deployment Requirements

- [ ] Docker Compose for local development (FastAPI + Neo4j + pgvector)
- [ ] Environment-based configuration (dev/staging/prod)
- [ ] Health check endpoint (/health)
- [ ] Graceful shutdown (finish in-flight requests)
- [ ] Logging to stdout (12-factor app compatible)

---

## Conclusion

### Summary

The **Platform Migration Analysis Tool** applies the proven vertical slice architecture and AI agent patterns from Obsidian_Agent to solve a high-value enterprise problem: mapping functionality across legacy and modern platforms.

**Key Strengths**:
1. **Clear Value Prop**: 99.99% cost reduction vs manual analysis ($5 vs $50,000 per 1000 endpoints)
2. **Technical Feasibility**: Proven patterns (Pydantic AI, FastAPI, Neo4j)
3. **Scalable Architecture**: Vertical slices enable incremental development
4. **AI-Optimized**: Tool docstrings guide LLM for accurate tool selection
5. **Template-Compliant**: Follows coding-generic-agent.md and Global Rules exactly

**Risks** (with mitigations):
1. LLM hallucination → Confidence scores + human verification + feedback loop
2. Market adoption → Freemium model + consultant partnerships
3. Data privacy → On-premise option + no data retention
4. Incomplete metadata → Multi-format support + manual enrichment
5. Performance at scale → Async I/O + caching + batch processing

**Go/No-Go Decision Criteria**:
- ✅ Can we achieve >80% mapping accuracy on test dataset?
- ✅ Can we ingest 1000 endpoints in <5 minutes?
- ✅ Do 10 potential users validate the problem?

**Recommendation**: Proceed with 2-week technical spike to validate LLM mapping accuracy. If >80% precision/recall on known good mappings, build MVP.

---

## Research Artifacts Created

This research document itself serves as the foundational artifact. Next steps:

1. **If pursuing**: Create `/execute` plan following `planning.md` format
2. **If pausing**: Save this as knowledge base for future evaluation
3. **If pivoting**: Extract reusable patterns (architecture, tool design) for other ideas

**Document Status**: RESEARCH COMPLETE (Implementation pending go/no-go decision)
