"""Base class for research source collectors.

All source collectors must inherit from this base class and implement
the collect() method.
"""

from abc import ABC, abstractmethod
from typing import Optional

from src.research.schemas import ResearchDepth, Source, SourceType
from src.shared.logging import get_logger

logger = get_logger(__name__)


class BaseSourceCollector(ABC):
    """Abstract base class for source collectors.

    Each source collector is responsible for:
    1. Querying its specific data source
    2. Extracting relevant content
    3. Returning Source objects with proper metadata

    Args:
        depth: Research depth level (affects number of queries).
        timeout: Maximum time to spend on this source (seconds).
    """

    def __init__(self, depth: ResearchDepth, timeout: int = 60) -> None:
        """Initialize source collector.

        Args:
            depth: Research depth level.
            timeout: Maximum execution time in seconds.
        """
        self.depth = depth
        self.timeout = timeout
        self.source_type = self._get_source_type()

    @abstractmethod
    def _get_source_type(self) -> SourceType:
        """Get the source type for this collector.

        Returns:
            SourceType enum value.
        """
        pass

    @abstractmethod
    async def collect(self, topic: str) -> list[Source]:
        """Collect sources for the given topic.

        Args:
            topic: Research topic or question.

        Returns:
            List of Source objects collected from this source.

        Raises:
            Exception: If collection fails after retries.
        """
        pass

    def _get_query_count(self) -> int:
        """Get number of queries based on depth level.

        Returns:
            Number of queries to perform.
        """
        query_counts = {
            ResearchDepth.MINIMAL: 2,
            ResearchDepth.LIGHT: 4,
            ResearchDepth.MODERATE: 6,
            ResearchDepth.DEEP: 10,
            ResearchDepth.EXTENSIVE: 15,
        }
        return query_counts.get(self.depth, 6)

    def _calculate_authority_score(self, domain: Optional[str] = None) -> float:
        """Calculate authority score based on domain.

        Args:
            domain: Domain name (e.g., "arxiv.org", "github.com").

        Returns:
            Authority score between 0.0 and 1.0.
        """
        if not domain:
            return 0.50  # Default score

        domain_lower = domain.lower()

        # High authority domains
        if any(
            d in domain_lower for d in ["arxiv.org", ".edu", "acm.org", "ieee.org"]
        ):
            return 0.95

        if any(
            d in domain_lower
            for d in [
                "openai.com",
                "google.com/research",
                "deepmind.com",
                "anthropic.com",
            ]
        ):
            return 0.90

        if "github.com" in domain_lower:
            return 0.85

        # Medium authority
        if any(
            d in domain_lower
            for d in ["medium.com", "towards", "kdnuggets", "machinelearning"]
        ):
            return 0.60

        # Lower authority (but still valid)
        if any(d in domain_lower for d in ["reddit.com", "news.ycombinator.com"]):
            return 0.50

        # Default for unknown domains
        return 0.60

    async def collect_with_error_handling(self, topic: str) -> list[Source]:
        """Collect sources with error handling and logging.

        Args:
            topic: Research topic.

        Returns:
            List of collected sources (empty if failed).
        """
        logger.info(
            "source_collection_started",
            source_type=self.source_type.value,
            topic=topic,
            depth=self.depth.value,
        )

        try:
            sources = await self.collect(topic)
            logger.info(
                "source_collection_completed",
                source_type=self.source_type.value,
                count=len(sources),
            )
            return sources

        except Exception as e:
            logger.exception(
                "source_collection_failed",
                source_type=self.source_type.value,
                error=str(e),
            )
            return []  # Return empty list, don't fail entire research
