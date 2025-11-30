"""YouTube transcript collector (STUB).

Searches for educational videos and extracts transcripts.
This is a stub implementation that can be extended with youtube-transcript-api.
"""

from src.research.schemas import Source, SourceType
from src.research.sources.base import BaseSourceCollector, ResearchDepth
from src.shared.logging import get_logger

logger = get_logger(__name__)


class YouTubeCollector(BaseSourceCollector):
    """Collects YouTube video transcripts.

    STUB IMPLEMENTATION: Returns empty list.
    To implement:
    1. Install youtube-transcript-api
    2. Search YouTube Data API for videos
    3. Extract transcripts for relevant videos
    4. Focus on curated channels: 3Blue1Brown, Two Minute Papers, etc.

    Args:
        depth: Research depth level.
        timeout: Maximum time in seconds.
    """

    CURATED_CHANNELS = [
        "3Blue1Brown",  # https://www.3blue1brown.com/
        "Two Minute Papers",
        "Lex Fridman",
        "Andrew Ng",
        "Andrej Karpathy",
    ]

    def _get_source_type(self) -> SourceType:
        """Get source type.

        Returns:
            SourceType.YOUTUBE.
        """
        return SourceType.YOUTUBE

    async def collect(self, topic: str) -> list[Source]:
        """Collect YouTube transcripts.

        Args:
            topic: Research topic.

        Returns:
            Empty list (stub implementation).
        """
        logger.info(
            "youtube_collector_stub",
            message="YouTube collector is not yet implemented. Skipping YouTube sources.",
            topic=topic,
        )

        # TODO: Implement YouTube search and transcript extraction
        # 1. Use YouTube Data API to search for videos
        # 2. Filter by curated channels
        # 3. Use youtube-transcript-api to get transcripts
        # 4. Return Source objects with transcript content

        return []
