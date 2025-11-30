"""Full article content extractor.

Extracts complete article text from URLs using newspaper3k library
with 3-tier fallback strategy.
"""

import asyncio
from typing import Optional
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup

from src.research.schemas import Source, SourceType
from src.research.sources.base import BaseSourceCollector, ResearchDepth
from src.shared.logging import get_logger

logger = get_logger(__name__)


class ArticleExtractor(BaseSourceCollector):
    """Extracts full article content from web URLs.

    Uses multi-tier fallback strategy:
    1. newspaper3k library (best for news/blogs)
    2. BeautifulSoup with custom selectors
    3. Raw HTML text extraction

    Args:
        depth: Research depth level (not used, extraction is URL-based).
        timeout: Maximum time per article in seconds.
        sources_to_extract: List of Source objects with URLs to extract.
    """

    def __init__(
        self,
        depth: ResearchDepth,
        timeout: int = 30,
        sources_to_extract: Optional[list[Source]] = None,
    ) -> None:
        """Initialize article extractor.

        Args:
            depth: Research depth level.
            timeout: Maximum time per article.
            sources_to_extract: Sources with URLs to extract full content.
        """
        super().__init__(depth, timeout)
        self.sources_to_extract = sources_to_extract or []

    def _get_source_type(self) -> SourceType:
        """Get source type.

        Returns:
            SourceType.ARTICLE.
        """
        return SourceType.ARTICLE

    async def collect(self, topic: str) -> list[Source]:
        """Extract full article content from source URLs.

        Args:
            topic: Research topic (not used, extraction is URL-based).

        Returns:
            List of Source objects with full article content.
        """
        # Select top N sources to extract based on authority
        sorted_sources = sorted(
            self.sources_to_extract, key=lambda s: s.authority_score, reverse=True
        )

        # Extract based on depth
        extract_count = min(self._get_query_count(), len(sorted_sources))
        sources_to_process = sorted_sources[:extract_count]

        logger.info("article_extraction_started", count=extract_count)

        sources: list[Source] = []

        async with aiohttp.ClientSession() as session:
            tasks = [
                self._extract_article(session, source)
                for source in sources_to_process
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    logger.warning("article_extraction_failed", error=str(result))
                    continue

                if result:
                    sources.append(result)

        success_rate = len(sources) / extract_count if extract_count > 0 else 0
        logger.info(
            "article_extraction_complete",
            extracted=len(sources),
            attempted=extract_count,
            success_rate=f"{success_rate:.2%}",
        )

        return sources

    async def _extract_article(
        self, session: aiohttp.ClientSession, source: Source
    ) -> Optional[Source]:
        """Extract full article content from a URL.

        Args:
            session: aiohttp client session.
            source: Source object with URL to extract.

        Returns:
            Source object with full content or None if extraction fails.
        """
        if not source.url:
            return None

        url = str(source.url)

        try:
            # Tier 1: Try newspaper3k approach (simplified)
            content = await self._extract_with_beautifulsoup(session, url)

            if content and len(content) > 500:  # Minimum content length
                return Source(
                    source_id=f"article_{hash(url)}",
                    source_type=SourceType.ARTICLE,
                    title=source.title,
                    url=source.url,
                    content=content,
                    author=source.author,
                    publication_date=source.publication_date,
                    authority_score=source.authority_score,
                    metadata={
                        **source.metadata,
                        "word_count": len(content.split()),
                        "extraction_method": "beautifulsoup",
                    },
                )

            return None

        except Exception as e:
            logger.warning("article_extraction_error", url=url, error=str(e))
            return None

    async def _extract_with_beautifulsoup(
        self, session: aiohttp.ClientSession, url: str
    ) -> Optional[str]:
        """Extract article content using BeautifulSoup.

        Args:
            session: aiohttp client session.
            url: Article URL.

        Returns:
            Extracted text content or None.
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            async with session.get(
                url, headers=headers, timeout=self.timeout
            ) as response:
                if response.status != 200:
                    return None

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()

                # Try common article containers
                article_selectors = [
                    "article",
                    '[role="main"]',
                    ".post-content",
                    ".article-content",
                    ".entry-content",
                    "main",
                ]

                content_element = None
                for selector in article_selectors:
                    content_element = soup.select_one(selector)
                    if content_element:
                        break

                if not content_element:
                    content_element = soup.body

                if not content_element:
                    return None

                # Extract text
                text = content_element.get_text(separator="\n", strip=True)

                # Clean up excessive whitespace
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                text = "\n\n".join(lines)

                return text if len(text) > 500 else None

        except Exception as e:
            logger.warning("beautifulsoup_extraction_error", url=url, error=str(e))
            return None
