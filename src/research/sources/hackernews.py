"""HackerNews discussion collector.

Searches HackerNews API for relevant discussions and extracts
top comments and insights.
"""

import asyncio
from datetime import datetime
from typing import Any
from urllib.parse import quote

import aiohttp

from src.research.schemas import Source, SourceType
from src.research.sources.base import BaseSourceCollector, ResearchDepth
from src.shared.logging import get_logger

logger = get_logger(__name__)


class HackerNewsCollector(BaseSourceCollector):
    """Collects discussions from HackerNews.

    Uses the Algolia HN Search API to find relevant threads
    and extracts top comments for insights.

    Args:
        depth: Research depth level.
        timeout: Maximum time in seconds.
    """

    BASE_URL = "https://hn.algolia.com/api/v1"

    def _get_source_type(self) -> SourceType:
        """Get source type.

        Returns:
            SourceType.HACKERNEWS.
        """
        return SourceType.HACKERNEWS

    async def collect(self, topic: str) -> list[Source]:
        """Collect HackerNews discussions.

        Args:
            topic: Research topic to search for.

        Returns:
            List of Source objects with HN threads and comments.

        Raises:
            aiohttp.ClientError: If API request fails.
        """
        query_count = self._get_query_count()
        search_queries = self._generate_search_queries(topic, query_count)

        sources: list[Source] = []

        async with aiohttp.ClientSession() as session:
            tasks = [
                self._search_hackernews(session, query) for query in search_queries
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    logger.warning(
                        "hn_search_failed", error=str(result), query=search_queries[0]
                    )
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
            "hn_collection_complete",
            total=len(unique_sources),
            queries=len(search_queries),
        )

        return unique_sources[:15]  # Limit to top 15

    def _generate_search_queries(self, topic: str, count: int) -> list[str]:
        """Generate search query variations.

        Args:
            topic: Main research topic.
            count: Number of query variations to generate.

        Returns:
            List of search query strings.
        """
        # Start with main topic
        queries = [topic]

        # Add variations with common keywords
        tech_terms = [
            "tutorial",
            "explained",
            "guide",
            "introduction",
            "how does",
            "what is",
        ]

        for term in tech_terms:
            if len(queries) >= count:
                break
            queries.append(f"{topic} {term}")

        return queries[:count]

    async def _search_hackernews(
        self, session: aiohttp.ClientSession, query: str
    ) -> list[Source]:
        """Search HackerNews for a specific query.

        Args:
            session: aiohttp client session.
            query: Search query string.

        Returns:
            List of Source objects from search results.
        """
        url = f"{self.BASE_URL}/search?query={quote(query)}&tags=story&hitsPerPage=5"

        try:
            async with session.get(url, timeout=self.timeout) as response:
                response.raise_for_status()
                data = await response.json()

                sources: list[Source] = []

                for hit in data.get("hits", []):
                    source = self._parse_hit(hit)
                    if source:
                        sources.append(source)

                        # Also fetch top comments for this story
                        if comments := await self._fetch_comments(
                            session, hit.get("objectID")
                        ):
                            sources.append(comments)

                return sources

        except Exception as e:
            logger.warning("hn_api_error", error=str(e), query=query)
            return []

    def _parse_hit(self, hit: dict[str, Any]) -> Optional[Source]:
        """Parse a HN search hit into a Source.

        Args:
            hit: Search result from Algolia API.

        Returns:
            Source object or None if parsing fails.
        """
        try:
            object_id = hit.get("objectID", "")
            title = hit.get("title", "Untitled")
            url = hit.get("url") or f"https://news.ycombinator.com/item?id={object_id}"
            author = hit.get("author", "unknown")
            created_at = hit.get("created_at")

            # Extract text content
            text = hit.get("story_text", "") or ""

            return Source(
                source_id=f"hn_{object_id}",
                source_type=SourceType.HACKERNEWS,
                title=title,
                url=url,
                content=text if text else f"HackerNews discussion: {title}",
                author=author,
                publication_date=(
                    datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    if created_at
                    else None
                ),
                authority_score=0.50,  # HN is medium authority
                metadata={
                    "points": hit.get("points", 0),
                    "num_comments": hit.get("num_comments", 0),
                },
            )

        except Exception as e:
            logger.warning("hn_parse_error", error=str(e), hit_id=hit.get("objectID"))
            return None

    async def _fetch_comments(
        self, session: aiohttp.ClientSession, story_id: Optional[str]
    ) -> Optional[Source]:
        """Fetch top comments for a story.

        Args:
            session: aiohttp client session.
            story_id: HN story ID.

        Returns:
            Source object with aggregated comments or None.
        """
        if not story_id:
            return None

        url = f"{self.BASE_URL}/items/{story_id}"

        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()

                # Extract top 10 comments
                comments = []
                for child in data.get("children", [])[:10]:
                    if text := child.get("text"):
                        comments.append(text)

                if not comments:
                    return None

                comment_text = "\n\n".join(comments)

                return Source(
                    source_id=f"hn_{story_id}_comments",
                    source_type=SourceType.HACKERNEWS,
                    title=f"Comments on: {data.get('title', 'HN Story')}",
                    url=f"https://news.ycombinator.com/item?id={story_id}",
                    content=comment_text,
                    author="HackerNews Community",
                    publication_date=None,
                    authority_score=0.50,
                    metadata={"comment_count": len(comments), "story_id": story_id},
                )

        except Exception as e:
            logger.warning("hn_comments_error", error=str(e), story_id=story_id)
            return None
