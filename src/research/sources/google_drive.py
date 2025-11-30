"""Google Drive document searcher (STUB).

Searches Google Drive for relevant documents (PDFs, DOCX, Google Docs).
This is a stub implementation that can be extended with Google Drive API.
"""

from src.research.schemas import Source, SourceType
from src.research.sources.base import BaseSourceCollector, ResearchDepth
from src.shared.logging import get_logger

logger = get_logger(__name__)


class GoogleDriveCollector(BaseSourceCollector):
    """Searches Google Drive for relevant documents.

    STUB IMPLEMENTATION: Returns empty list.
    To implement:
    1. Set up Google Drive API OAuth 2.0
    2. Search Drive for documents matching topic
    3. Extract text from PDFs, DOCX, Google Docs
    4. Return Source objects with document content

    Args:
        depth: Research depth level.
        timeout: Maximum time in seconds.
    """

    def _get_source_type(self) -> SourceType:
        """Get source type.

        Returns:
            SourceType.GOOGLE_DRIVE.
        """
        return SourceType.GOOGLE_DRIVE

    async def collect(self, topic: str) -> list[Source]:
        """Search Google Drive for documents.

        Args:
            topic: Research topic.

        Returns:
            Empty list (stub implementation).
        """
        logger.info(
            "google_drive_collector_stub",
            message="Google Drive collector is not yet implemented. Skipping Drive sources.",
            topic=topic,
        )

        # TODO: Implement Google Drive search
        # 1. Authenticate with Google Drive API (OAuth 2.0)
        # 2. Search for documents matching topic
        # 3. Extract text content from files
        # 4. Return Source objects

        return []
