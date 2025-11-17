# Research Prompt: Platform Migration Analysis Tool

## Task Description

You are tasked with conducting comprehensive research for a new platform migration analysis tool idea. This is a **research-only task** - do NOT implement code, only analyze feasibility, design architecture, and document findings.

---

## Problem Statement

**Core Idea**: Build an AI agent-powered platform migration analysis tool that helps companies modernizing their platforms by automatically mapping functionality between legacy and modern tech stacks.

**User Need**: Currently, companies spend $50,000+ and 6-12 weeks using expensive consultants to manually trace which modern systems replace legacy functionality. For example:
- **Legacy**: System A provides `getOrderDetails(orderId)` via SOAP
- **Modern**: Which system/endpoint provides the same functionality?
- **Expected Output**: Tool should identify that `OrderManagementAPI.query.order` (GraphQL) is the modern equivalent, with transformation notes

**Scope**:
- Analyze both legacy and modern platform architectures
- Map functional equivalence across different tech stacks (REST→GraphQL, SOAP→REST, etc.)
- Provide confidence scores for mappings
- Identify gaps (unmapped legacy functionality)
- Generate migration guides

---

## Research Standards & Templates

Your research MUST align with the following standards and templates:

### 1. Coding Standards (Base Architecture)

**Source**: `coding-generic-agent.md` from the Obsidian_Agent repository
**Location**: `https://github.com/sathyan17-1980/Obsidian_Agent/blob/main/coding-generic-agent.md`

**Key Requirements**:
- Use vertical slice architecture (each tool is independent: `tool.py`, `schemas.py`, `service.py`)
- All code must have strict type safety (Pydantic models, mypy strict mode)
- Structured logging optimized for AI debugging (Structlog with keyword arguments)
- Agent-centric tool docstrings with specific sections:
  - "Use this when you need to:" (affirmative guidance)
  - "Do NOT use this for:" (negative guidance pointing to alternative tools)
  - Performance Notes (token costs, execution time, resource limits)
  - Realistic examples (not foo/bar, use actual paths/scenarios)
- Testing mirrors source structure (every `src/` file has `tests/` equivalent)

### 2. Global Rules (Core Principles)

**Source**: `CLAUDE.md` from the AI repository
**Location**: `https://github.com/sathyan17-1980/AI/blob/main/agentic-coding-course/module_3/4_exercise/CLAUDE.md`

**Key Principles**:
1. **TYPE SAFETY IS NON-NEGOTIABLE**: All functions/methods/variables MUST have type annotations, strict mypy enforcement
2. **KISS & YAGNI**: Simple solutions over abstractions, avoid building unrequired features
3. **Vertical Slice Architecture**: Organize as independent slices with schemas, services, tools
4. **Agent Tool Docstrings**: Guide LLM reasoning during tool selection (critical for agent performance)
5. **Structured Logging**: AI-comprehensible logs with descriptive event names, debugging context, masked sensitive data

### 3. Research Document Template

**Source**: `planning.md` command from Obsidian_Agent
**Location**: `.claude/commands/core_commands/planning.md`

**Required Sections** (in order):
1. **Mission Statement**:
   - Feature Name: [One line]
   - Problem: [One sentence describing the problem]
   - Goal: [One sentence describing what should be achieved]
   - Scope:
     - ✅ **Included**: [Bullet list of what's in scope]
     - ❌ **Excluded**: [Bullet list of what's explicitly out of scope]

2. **Context Assessment**:
   - **Current State**:
     - ✅ What already exists and works?
     - ⚠️ What problems exist?
     - ❌ What's missing?
   - **Architecture**: Proposed structure diagram
   - **Dependencies**: What components can be reused? What's needed?

3. **Problem Domain Analysis**:
   - Current manual process (status quo)
   - User personas and their needs
   - Real-world examples
   - Success criteria (Must Have / Should Have / Could Have)

4. **Architecture Design**:
   - Application of vertical slice pattern
   - Data models (Pydantic schemas with full type annotations)
   - Tool interfaces (agent-facing tools with comprehensive docstrings)
   - Storage architecture (database design)

5. **Technical Implementation Strategy**:
   - Phase-by-phase breakdown (Foundation → Core Features → Integration)
   - Each phase with: Goal, Tasks, Testing approach, Validation commands

6. **Cost & Performance Analysis**:
   - Cost breakdown (LLM API costs, infrastructure, etc.)
   - Performance targets (latency, throughput, scalability)
   - Comparison to manual/existing solutions

7. **Risk Assessment & Mitigation**:
   - Technical risks (with impact, likelihood, mitigation)
   - Business risks (with impact, likelihood, mitigation)

8. **Common Pitfalls to Avoid**:
   - ❌ **Don't** [anti-pattern] - [explanation and what to do instead]
   - Organize by category (Ingestion, Mapping, Storage, Security, etc.)
   - 40+ specific pitfalls covering implementation mistakes

9. **Success Criteria Template**:
   - ✅ **Functional Requirements**: [Checkboxes for each feature]
   - ✅ **Non-Functional Requirements**: [Performance, Type Safety, Logging, Security]
   - ✅ **Documentation Requirements**: [README, API docs, deployment guides]
   - ✅ **Testing Requirements**: [Unit, Integration, Validation tests]
   - ✅ **Deployment Requirements**: [Docker, config, health checks]

10. **Conclusion**:
    - Summary of key strengths
    - Risks with mitigations
    - Go/No-Go decision criteria
    - Recommendation (next steps)

---

## Reference Architecture

**Base Project**: Obsidian AI Agent
**Repository**: `https://github.com/sathyan17-1980/Obsidian_Agent`

**Key Patterns to Reuse**:
- FastAPI + Pydantic AI for agent orchestration
- OpenAI-compatible API endpoints
- Vertical slice architecture in `src/tools/`
- Shared utilities in `src/shared/` (config, logging, security)
- Testing patterns from `tests/` with pytest markers (@pytest.mark.unit, @pytest.mark.integration)

**Example Tool Structure** (from Obsidian_Agent):
```
src/tools/obsidian_note_manager/
├── __init__.py
├── schemas.py          # Pydantic models (NoteOperation enum, ManageNoteRequest, NoteResult)
├── service.py          # Business logic (async functions, error handling, logging)
└── tool.py             # Agent registration (@agent.tool with comprehensive docstring)

tests/tools/obsidian_note_manager/
├── test_schemas.py     # Schema validation tests
├── test_service.py     # Service layer unit tests
└── test_tool.py        # Tool integration tests
```

---

## Specific Requirements for This Research

### Core Functionality to Research

1. **Platform Ingestion**:
   - How to parse OpenAPI 2.0/3.0 specifications
   - How to parse GraphQL schemas (SDL)
   - How to parse SQL DDL (database schemas)
   - How to handle incomplete/malformed specs
   - Performance: Target 1000 endpoints in <10 seconds

2. **Mapping Engine**:
   - Structural mapping (path/schema similarity)
   - Semantic mapping (LLM-based functional understanding)
   - Hybrid approach (combining both strategies)
   - Confidence scoring (high/medium/low)
   - Performance: 1000 endpoint pairs in <6 minutes
   - Cost: Target <$5 per 1000 endpoints

3. **Query Interface**:
   - Natural language queries ("Where is getOrderDetails in new platform?")
   - Vector search for semantic similarity
   - Response formats (minimal/concise/detailed for token efficiency)

4. **Gap Detection**:
   - Identify unmapped legacy functionality
   - Prioritize by impact (usage frequency × business criticality)
   - Generate risk reports

5. **Report Generation**:
   - Markdown migration guides
   - CSV exports for project management tools
   - Executive summaries

### Technical Decisions to Research

1. **Storage Architecture**:
   - Neo4j graph database vs PostgreSQL + pgvector
   - How to model system relationships
   - How to store mappings with confidence scores
   - Cypher query patterns for finding equivalents

2. **AI/LLM Strategy**:
   - Which LLM for semantic mapping (GPT-4, Claude, etc.)
   - How to structure prompts for accuracy
   - How to validate mapping quality (precision/recall)
   - How to handle hallucination risk

3. **Performance & Cost Optimization**:
   - When to use structural vs semantic mapping
   - How to cache embeddings/mappings
   - Batch processing strategies
   - Token efficiency techniques

4. **Security & Privacy**:
   - How to handle sensitive platform metadata
   - On-premise vs SaaS deployment
   - Input validation to prevent injection attacks
   - Audit logging requirements

### Business Viability to Assess

1. **Market Analysis**:
   - Existing solutions (AWS Migration Hub, Cloudamize, CAST Highlight, consulting firms)
   - Competitive advantages
   - Greenfield opportunities

2. **Pricing Strategy**:
   - Freemium model (free up to X endpoints)
   - Pay-as-you-go pricing
   - Enterprise licensing
   - ROI vs manual consulting ($50k per 1000 endpoints)

3. **Go-to-Market**:
   - Target customers (startups, mid-size companies, enterprise)
   - Distribution channels
   - Partnerships (consultants as customers, not competitors)

4. **Risk Assessment**:
   - Technical risks (LLM accuracy, performance, incomplete metadata)
   - Business risks (market adoption, data privacy, consultant competition)
   - Mitigations for each risk

---

## Expected Deliverables

### Primary Output: Research Document

**File**: `platform-migration-analysis.md`
**Location**: `plans/` directory
**Length**: 1500-2000 lines (comprehensive)

**Must Include**:
1. Mission Statement (Problem/Goal/Scope with ✅/❌ format)
2. Context Assessment (✅/⚠️/❌ current state, architecture, dependencies)
3. Problem Domain Analysis (manual process, user personas, examples)
4. Architecture Design (vertical slices, data models, tool docstrings)
5. Implementation Strategy (6 phases with tasks/testing/validation)
6. Storage Architecture (Neo4j schema, Cypher queries, vector search)
7. Cost & Performance Analysis (breakdown per 1000 endpoints, targets)
8. Risk Assessment (technical + business with mitigations)
9. Common Pitfalls (40+ anti-patterns organized by category)
10. Success Criteria Template (functional, non-functional, docs, testing)
11. Conclusion (strengths, risks, go/no-go criteria, recommendation)

### Tool Docstrings (5 Required)

For each agent tool, provide **complete docstring** following this template:

```python
@agent.tool
async def tool_name(
    ctx: RunContext[AgentDependencies],
    param1: str,
    param2: str = "default",
    response_format: str = "concise"
) -> str:
    """[One-line summary of what this tool does].

    Use this when you need to:
    - [Specific scenario 1 where this tool is the right choice]
    - [Specific scenario 2]
    - [Specific scenario 3]
    - [Specific scenario 4]
    - [Specific scenario 5]

    Do NOT use this for:
    - [Scenario where OTHER_TOOL should be used instead] (use other_tool instead)
    - [Scenario where ANOTHER_TOOL should be used] (use another_tool instead)
    - [Anti-pattern or common misuse]

    Args:
        param1: [Standard description].
            [WHY you'd choose different values for this parameter]
        param2: [Standard description].
            - "option1": [Description] (use when [scenario])
            - "option2": [Description] (use when [scenario])
            - "option3": [Description] (use when [scenario])
        response_format: Control output verbosity and token usage.
            - "minimal": [Description] (~50 tokens, use when [scenario])
            - "concise": [Description] (~150 tokens, default, balanced)
            - "detailed": [Description] (~1500+ tokens, use sparingly when [scenario])

    Returns:
        [Description of return value].
        Format: [Structure/format details that help agent parse result].

    Performance Notes:
        - Minimal format: ~50 tokens (use for [scenario])
        - Concise format: ~150 tokens (default, good for most cases)
        - Detailed format: ~1500+ tokens (only when full content needed)
        - Typical execution time: [duration] for [scenario]
        - Max [resource limit]: [value] ([what happens if exceeded])
        - Cost: [API cost estimate if applicable]

    Examples:
        # [Brief description of what this example shows]
        tool_name(
            param1="realistic/example/path.yaml",
            param2="option1",
            response_format="minimal"
        )

        # [Description of complex case]
        tool_name(
            param1="another/realistic/example.graphql",
            param2="option2",
            response_format="detailed"
        )

        # [Description of edge case or important variation]
        tool_name(
            param1="edge/case/example.sql",
            param2="option3",
            response_format="concise"
        )
    """
```

**Required Tools** (at minimum):
1. `platform_ingest` - Ingest platform metadata (OpenAPI, GraphQL, SQL)
2. `map_functionality` - Map legacy→modern with confidence scores
3. `query_mapping` - Answer "where is X?" queries
4. `detect_gaps` - Find unmapped functionality
5. `generate_migration_report` - Export analysis results

### Data Models (Pydantic Schemas)

Provide complete Pydantic models with:
- Strict type annotations (no `Any` without justification)
- Field descriptions
- Validation logic (@model_validator where needed)
- Enums for categorical values

**Required Models**:
- `PlatformMetadata` (complete platform description)
- `EndpointMetadata` (single API endpoint/operation)
- `FunctionalMapping` (legacy→modern mapping with confidence)
- `GapAnalysis` (unmapped functionality)
- `MappingConfidence` (enum: HIGH, MEDIUM, LOW, NONE)

---

## Quality Criteria

Your research will be evaluated on:

### Completeness (40%)
- [ ] All 11 required sections present
- [ ] 5 tool docstrings with all subsections
- [ ] Data models with complete type annotations
- [ ] 40+ common pitfalls documented
- [ ] 60+ success criteria checkboxes

### Alignment with Templates (30%)
- [ ] Mission Statement in exact format (Problem/Goal/Scope)
- [ ] Context Assessment with ✅/⚠️/❌ symbols
- [ ] Common Pitfalls section present
- [ ] Success Criteria Template at end
- [ ] Follows coding-generic-agent.md structure

### Technical Depth (20%)
- [ ] Architecture design is specific (not generic/hand-wavy)
- [ ] Cost analysis has actual numbers (not "TBD")
- [ ] Performance targets are measurable
- [ ] Risk mitigations are actionable
- [ ] Implementation phases have clear deliverables

### Actionability (10%)
- [ ] Can transition directly to implementation
- [ ] Validation commands are exact (not "run tests")
- [ ] Examples use realistic data (not foo/bar)
- [ ] Go/No-Go criteria are clear
- [ ] Recommendation includes specific next steps

---

## Constraints & Guidelines

### What to DO:
✅ Research existing solutions (AWS Migration Hub, CAST Highlight, consulting firms)
✅ Provide realistic cost estimates (LLM API costs, infrastructure, labor savings)
✅ Design complete data models (Pydantic with all fields)
✅ Document 40+ common pitfalls (implementation mistakes to avoid)
✅ Create 60+ success criteria (validation checklist)
✅ Include real-world examples (Stripe API, GitHub API, e-commerce platforms)
✅ Calculate ROI vs manual consulting ($50k baseline)
✅ Consider security & privacy (on-premise, data retention, audit logging)

### What NOT to DO:
❌ Do NOT write implementation code (research only)
❌ Do NOT use vague placeholders ("TBD", "to be determined")
❌ Do NOT skip sections from the template
❌ Do NOT use toy examples (foo/bar/test.md)
❌ Do NOT ignore performance constraints (must have targets)
❌ Do NOT forget token efficiency (minimal/concise/detailed formats)
❌ Do NOT omit risk mitigations (every risk needs mitigation plan)
❌ Do NOT assume 100% LLM accuracy (document confidence scoring approach)

---

## Research Process Recommendations

### Phase 1: Understand the Domain (30 minutes)
1. Research existing migration tools (AWS, Cloudamize, CAST)
2. Understand manual consulting process (interviews, spreadsheets, runbooks)
3. Identify user personas (Migration Architect, Developer, QA, PM)
4. Document real-world example (legacy SOAP → modern GraphQL)

### Phase 2: Design Architecture (60 minutes)
1. Apply vertical slice pattern from Obsidian_Agent
2. Design 5 core tools (ingest, map, query, gaps, reports)
3. Create data models (platform, endpoint, mapping, gap)
4. Design storage (Neo4j graph schema, vector search)

### Phase 3: Technical Analysis (45 minutes)
1. Research OpenAPI/GraphQL/SQL parsing libraries
2. Evaluate Neo4j vs PostgreSQL+pgvector
3. Determine LLM strategy (structural pre-filter + semantic)
4. Calculate costs (embeddings, LLM calls, storage)
5. Set performance targets (latency, throughput)

### Phase 4: Risk & Viability (30 minutes)
1. Identify technical risks (LLM hallucination, incomplete metadata, performance)
2. Identify business risks (market adoption, data privacy, consultant competition)
3. Define mitigations for each risk
4. Calculate ROI (AI tool cost vs $50k consulting baseline)

### Phase 5: Documentation (60 minutes)
1. Write all 11 required sections in order
2. Create 40+ common pitfalls (organized by category)
3. Create 60+ success criteria (functional, non-functional, docs, testing)
4. Write comprehensive tool docstrings (5 tools × 200 lines each)
5. Proofread for template compliance

---

## Success Indicators

You've completed the research successfully when:

1. ✅ **Template Compliance**: All sections from coding-generic-agent.md present
2. ✅ **Principle Adherence**: TYPE SAFETY, KISS, YAGNI, vertical slices mentioned
3. ✅ **Completeness**: 1500+ lines covering all required topics
4. ✅ **Specificity**: Numbers, not hand-waving ("$5 per 1000 endpoints", not "cheap")
5. ✅ **Actionability**: Another agent could implement from your research alone
6. ✅ **Realistic Examples**: Real APIs (Stripe, GitHub), not foo/bar
7. ✅ **Tool Docstrings**: All 5 tools have complete agent-centric documentation
8. ✅ **Data Models**: Full Pydantic schemas with strict types
9. ✅ **Common Pitfalls**: 40+ anti-patterns documented
10. ✅ **Success Criteria**: 60+ validation checkboxes

---

## Example Output Reference

A completed research document following this template can be found at:
**Repository**: `https://github.com/sathyan17-1980/Obsidian_Agent`
**Branch**: `claude/research-migration-analysis-01GDKpncveccPyrS4GDdxSen`
**File**: `plans/platform-migration-analysis.md`

This example demonstrates:
- Exact Mission Statement format
- Context Assessment with ✅/⚠️/❌ symbols
- 40+ common pitfalls organized by category
- 60+ success criteria checkboxes
- 5 complete tool docstrings (1000+ lines total)
- Full data models with Pydantic
- Cost analysis with specific numbers ($5 vs $50k)
- 6-phase implementation strategy

---

## Submission Format

### File Naming
- Primary document: `platform-migration-analysis.md`
- Save to: `plans/` directory (or as specified by user)

### Document Structure
```markdown
# Research: Platform Migration Analysis Tool

## 1. Mission Statement
[Problem/Goal/Scope with ✅/❌]

## 2. Context Assessment
[✅/⚠️/❌ current state, architecture, dependencies]

## 3. Problem Domain Analysis
[Manual process, user personas, examples]

## 4. Architecture Design
[Vertical slices, data models, tool interfaces]

[... continue through all 11 sections ...]

## 11. Conclusion
[Summary, risks, go/no-go criteria, recommendation]
```

### Commit Message Format (if applicable)
```
Add comprehensive research for platform migration analysis tool

Research document covers:
- Problem domain analysis (legacy→modern platform mapping)
- Architecture design using vertical slice pattern
- 5 core agent tools (ingest, map, query, gap detect, report)
- Data models and Neo4j graph schema
- Cost analysis (99.99% savings vs consultants)
- Implementation strategy (6 phases over 12 weeks)
- Risk assessment and go-to-market strategy

Key insights:
- Applies Obsidian_Agent patterns to enterprise migration
- LLM-powered semantic mapping with confidence scores
- Estimated $5 per 1000 endpoints vs $50k manual analysis
- Target: 80%+ mapping accuracy in technical spike

Status: Research complete, pending go/no-go decision
```

---

## Questions to Answer Through Research

Your research should definitively answer:

1. **Feasibility**: Can this be built with current LLM technology? (Target: 80%+ accuracy)
2. **Architecture**: What's the optimal design? (Vertical slices, Neo4j, hybrid mapping)
3. **Cost**: What's the total cost per 1000 endpoints? (Target: <$10)
4. **Performance**: Can it meet targets? (1000 endpoints in 6 minutes)
5. **Viability**: Is there a market? (vs AWS, consultants, CAST)
6. **Risks**: What can go wrong? (LLM hallucination, incomplete metadata, adoption)
7. **Go/No-Go**: Should this be built? (Based on accuracy spike results)

---

## Final Checklist

Before submitting research, verify:

- [ ] Mission Statement uses exact template format
- [ ] Context Assessment has ✅/⚠️/❌ symbols
- [ ] All 5 tool docstrings have 8 required subsections
- [ ] Data models use Pydantic with strict types
- [ ] Common Pitfalls section has 40+ anti-patterns
- [ ] Success Criteria section has 60+ checkboxes
- [ ] Cost analysis includes specific numbers
- [ ] Performance targets are measurable
- [ ] Examples use realistic data (not foo/bar)
- [ ] Conclusion includes go/no-go criteria
- [ ] Document is 1500+ lines
- [ ] All sections from template present

---

**Begin research now. Focus on depth, specificity, and actionability. This research should enable an implementation decision without further investigation.**
