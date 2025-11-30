"""Brave Search API collector.

Uses Brave Search API to find high-quality web articles and resources.
Supports both FREE and PRO tier selection based on research depth.
"""

import asyncio
import os
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

import aiohttp

from src.research.schemas import Source, SourceType
from src.research.sources.base import BaseSourceCollector, ResearchDepth
from src.shared.logging import get_logger

logger = get_logger(__name__)


class BraveSearchCollector(BaseSourceCollector):
    """Collects web search results from Brave Search API.

    Automatically selects FREE or PRO tier based on research depth.
    Performs multiple query variations for comprehensive coverage.

    Args:
        depth: Research depth level.
        timeout: Maximum time in seconds.
    """

    BASE_URL = "https://api.search.brave.com/res/v1/web/search"

    def __init__(self, depth: ResearchDepth, timeout: int = 60) -> None:
        """Initialize Brave Search collector.

        Args:
            depth: Research depth level.
            timeout: Maximum execution time.
        """
        super().__init__(depth, timeout)

        # Select API key based on depth
        if depth in [ResearchDepth.DEEP, ResearchDepth.EXTENSIVE]:
            self.api_key = os.getenv("BRAVE_API_KEY_PRO")
            self.tier = "PRO"
        else:
            self.api_key = os.getenv("BRAVE_API_KEY_FREE")
            self.tier = "FREE"

        if not self.api_key:
            # Fallback to any available key
            self.api_key = os.getenv("BRAVE_API_KEY_FREE") or os.getenv(
                "BRAVE_API_KEY_PRO"
            )
            self.tier = "FALLBACK"

        if not self.api_key:
            logger.warning(
                "brave_api_key_missing",
                message="No Brave API key found. Set BRAVE_API_KEY_FREE or BRAVE_API_KEY_PRO",
            )

    def _get_source_type(self) -> SourceType:
        """Get source type.

        Returns:
            SourceType.WEB.
        """
        return SourceType.WEB

    async def collect(self, topic: str) -> list[Source]:
        """Collect web search results.

        Args:
            topic: Research topic.

        Returns:
            List of Source objects from web search.

        Raises:
            ValueError: If no API key is configured.
        """
        if not self.api_key:
            logger.error("brave_api_key_not_configured")
            return []

        query_count = self._get_query_count()
        search_queries = self._generate_search_queries(topic, query_count)

        sources: list[Source] = []

        async with aiohttp.ClientSession() as session:
            tasks = [
                self._search_brave(session, query) for query in search_queries
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    logger.warning("brave_search_failed", error=str(result))
                    continue

                if result:
                    sources.extend(result)

        # Deduplicate by URL
        seen_urls: set[str] = set()
        unique_sources: list[Source] = []

        for source in sources:
            if source.url and str(source.url) not in seen_urls:
                seen_urls.add(str(source.url))
                unique_sources.append(source)

        logger.info(
            "brave_collection_complete",
            total=len(unique_sources),
            tier=self.tier,
            queries=len(search_queries),
        )

        return unique_sources[:15]  # Return top 15

    def _generate_search_queries(self, topic: str, count: int) -> list[str]:
        """Generate diverse search queries.

        Args:
            topic: Main research topic.
            count: Number of queries to generate.

        Returns:
            List of search query strings.
        """
        queries = [topic]

        # Add targeted variations
        variations = [
            f"{topic} tutorial",
            f"{topic} explained",
            f"{topic} guide",
            f"how to {topic}",
            f"what is {topic}",
            f"{topic} examples",
            f"{topic} best practices",
            f"{topic} documentation",
            f"understanding {topic}",
            f"{topic} introduction",
        ]

        for variation in variations:
            if len(queries) >= count:
                break
            queries.append(variation)

        return queries[:count]

    async def _search_brave(
        self, session: aiohttp.ClientSession, query: str
    ) -> list[Source]:
        """Execute a Brave Search query.

        Args:
            session: aiohttp client session.
            query: Search query string.

        Returns:
            List of Source objects from search results.
        """
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key,
        }

        params = {"q": query, "count": 10, "text_decorations": False}

        try:
            async with session.get(
                self.BASE_URL, headers=headers, params=params, timeout=self.timeout
            ) as response:
                if response.status == 429:
                    logger.warning("brave_rate_limit_hit", tier=self.tier)
                    return []

                response.raise_for_status()
                data = await response.json()

                sources: list[Source] = []

                for result in data.get("web", {}).get("results", []):
                    if source := self._parse_result(result):
                        sources.append(source)

                return sources

        except Exception as e:
            logger.warning("brave_api_error", error=str(e), query=query)
            return []

    def _parse_result(self, result: dict) -> Optional[Source]:
        """Parse a Brave Search result into a Source.

        Args:
            result: Search result dictionary.

        Returns:
            Source object or None if parsing fails.
        """
        try:
            url = result.get("url", "")
            if not url:
                return None

            domain = urlparse(url).netloc
            title = result.get("title", "Untitled")
            description = result.get("description", "")

            # Get publication date if available
            pub_date = result.get("age")
            publication_date = None
            if pub_date:
                try:
                    publication_date = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
                except:
                    pass

            return Source(
                source_id=f"web_{hash(url)}",
                source_type=SourceType.WEB,
                title=title,
                url=url,
                content=description,  # Snippet only, full extraction done separately
                author=domain,
                publication_date=publication_date,
                authority_score=self._calculate_authority_score(domain),
                metadata={
                    "domain": domain,
                    "extra_snippets": result.get("extra_snippets", []),
                },
            )

        except Exception as e:
            logger.warning("brave_parse_error", error=str(e))
            return None
