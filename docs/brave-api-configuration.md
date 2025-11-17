# Brave Search API Configuration

## Overview

The AI Research Agent uses the Brave Search API to perform web research for content generation. We maintain two API keys with different tier levels to optimize cost and performance based on research requirements.

## API Key Tiers

### Free Tier (`BRAVE_API_KEY_FREE`)
- **Rate Limit**: 2,000 queries/month
- **Use Cases**:
  - Quick topic validation
  - Initial topic exploration
  - Single-topic research (1-3 queries per session)
  - LinkedIn post generation (minimal research)
  - Testing and development

### Pro Tier (`BRAVE_API_KEY_PRO`)
- **Rate Limit**: Higher query volume and rate limits
- **Use Cases**:
  - Extensive multi-topic research
  - Blog article generation (comprehensive research)
  - Deep topic exploration (10+ queries per session)
  - Multi-source validation
  - Production workloads with high volume

## Configuration

### Environment Variables

Add the following to your `.env` file:

```bash
# Brave Search API Keys
BRAVE_API_KEY_FREE=BSAfhmAUjm78j3TKqPkDlByE0ecpRt7
BRAVE_API_KEY_PRO=BSAwntGzdRA-yo5lL0O4eoDrSgr2nBk
```

### Access in Code

The API keys are automatically loaded via `src/shared/config.py`:

```python
from src.shared.config import settings

# Access free tier key
free_key = settings.brave_api_key_free

# Access pro tier key
pro_key = settings.brave_api_key_pro
```

## Usage Strategy

### Decision Matrix: When to Use Which Key

| Research Depth | Output Type | Queries Needed | API Key to Use |
|----------------|-------------|----------------|----------------|
| Minimal | LinkedIn Post | 1-3 | **FREE** |
| Light | Short Blog (500w) | 3-5 | **FREE** |
| Moderate | Standard Blog (800w) | 5-8 | **PRO** |
| Deep | Long Blog (1500w) | 8-12 | **PRO** |
| Extensive | Multi-topic Research | 12+ | **PRO** |

### Implementation Pattern

```python
from src.shared.config import settings

def get_brave_api_key(research_depth: str) -> str:
    """Select appropriate Brave API key based on research depth.

    Args:
        research_depth: One of "minimal", "light", "moderate", "deep", "extensive"

    Returns:
        Appropriate Brave API key for the research depth.

    Examples:
        # LinkedIn post generation (1-3 queries)
        key = get_brave_api_key("minimal")  # Uses FREE tier

        # Standard blog article (5-8 queries)
        key = get_brave_api_key("moderate")  # Uses PRO tier

        # Extensive multi-topic research (12+ queries)
        key = get_brave_api_key("extensive")  # Uses PRO tier
    """
    if research_depth in ("minimal", "light"):
        return settings.brave_api_key_free
    else:  # moderate, deep, extensive
        return settings.brave_api_key_pro
```

### Agent Tool Parameter Design

When designing agent tools, include a `research_depth` parameter to control API key selection:

```python
@agent.tool
async def web_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    research_depth: str = "minimal",
    max_results: int = 10
) -> str:
    """Search the web using Brave Search API.

    Args:
        query: Search query string.
        research_depth: Research intensity level.
            - "minimal": Quick search (1-3 queries, FREE tier)
            - "light": Basic research (3-5 queries, FREE tier)
            - "moderate": Standard research (5-8 queries, PRO tier)
            - "deep": Comprehensive research (8-12 queries, PRO tier)
            - "extensive": Multi-topic deep dive (12+ queries, PRO tier)
        max_results: Maximum search results to return (1-20).

    Performance Notes:
        - FREE tier: 2,000 queries/month, use for minimal/light research
        - PRO tier: Higher limits, use for moderate/deep/extensive research
        - Query cost: ~$0.005 per query (PRO tier pricing)
        - Execution time: 2-5 seconds per query
    """
    api_key = get_brave_api_key(research_depth)
    # ... implementation
```

## Cost Optimization

### Monthly Budget Allocation

| Tier | Monthly Queries | Estimated Cost | Use Case |
|------|----------------|----------------|----------|
| FREE | 2,000 | $0 (free tier) | Development, testing, light production use |
| PRO | Variable | $0.005/query | Production workloads, extensive research |

### Cost Per Research Session

**LinkedIn Post** (minimal depth):
- Queries: 1-3
- API Key: FREE
- Cost: $0

**Standard Blog** (moderate depth):
- Queries: 5-8
- API Key: PRO
- Cost: ~$0.025-$0.040

**Comprehensive Blog** (deep depth):
- Queries: 8-12
- API Key: PRO
- Cost: ~$0.040-$0.060

### Best Practices

1. **Default to FREE tier** for development and testing
2. **Use PRO tier** only when research depth requires it
3. **Cache research results** to avoid redundant queries
4. **Set query limits** in agent configurations to prevent runaway costs
5. **Monitor usage** by logging API key selection decisions

## Error Handling

### Rate Limit Exceeded

If the FREE tier hits the 2,000 query/month limit:

1. **Automatic Fallback**: Agent should fall back to PRO tier for critical requests
2. **User Notification**: Inform user that FREE tier quota is exhausted
3. **Graceful Degradation**: Reduce research depth or use cached results

```python
async def web_search_with_fallback(query: str, research_depth: str) -> dict:
    """Web search with automatic fallback to PRO tier on rate limit."""
    try:
        # Try FREE tier first for minimal/light research
        api_key = get_brave_api_key(research_depth)
        result = await brave_search(query, api_key)
        return result
    except RateLimitError as e:
        if research_depth in ("minimal", "light"):
            # Fall back to PRO tier
            logger.warning(
                "brave_free_tier_exhausted",
                falling_back_to="pro_tier",
                research_depth=research_depth
            )
            api_key = settings.brave_api_key_pro
            result = await brave_search(query, api_key)
            return result
        else:
            raise
```

## Monitoring and Logging

### Log API Key Selection

Always log which API key tier is being used:

```python
logger.info(
    "brave_search_initiated",
    query=query[:50],  # Truncate for privacy
    research_depth=research_depth,
    api_key_tier="free" if api_key == settings.brave_api_key_free else "pro",
    max_results=max_results
)
```

### Track Usage Metrics

Monitor these metrics to optimize API key usage:

- Total queries per tier (daily/weekly/monthly)
- Average queries per research depth
- Rate limit hit frequency
- Cost per content type (LinkedIn vs Blog)

## Security Considerations

1. **Never log full API keys** - Always mask with `api_key[:8] + "..."`
2. **Environment variables only** - Never hardcode API keys in source code
3. **Gitignore .env file** - Ensure `.env` is in `.gitignore` (already configured)
4. **Rotate keys periodically** - Update keys every 90 days or after exposure
5. **Separate dev/prod keys** - Use different keys for development and production

## References

- [Brave Search API Documentation](https://brave.com/search/api/)
- [Brave Search API Pricing](https://brave.com/search/api/pricing/)
- Project Configuration: `src/shared/config.py`
- Environment Template: `.env.example`
