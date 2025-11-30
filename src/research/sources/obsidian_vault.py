"""Obsidian vault searcher.

Searches the user's Obsidian vault for relevant notes using
keyword matching and optional semantic search with embeddings.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.research.schemas import Source, SourceType
from src.research.sources.base import BaseSourceCollector, ResearchDepth
from src.shared.logging import get_logger

logger = get_logger(__name__)


class ObsidianVaultCollector(BaseSourceCollector):
    """Searches Obsidian vault for relevant notes.

    Uses keyword-based search (semantic search can be added later).
    This is a MANDATORY source - research cannot proceed without vault access.

    Args:
        depth: Research depth level.
        timeout: Maximum time in seconds (not used for file search).
        vault_path: Path to Obsidian vault.
    """

    def __init__(
        self, depth: ResearchDepth, timeout: int = 60, vault_path: Optional[str] = None
    ) -> None:
        """Initialize Obsidian vault collector.

        Args:
            depth: Research depth level.
            timeout: Maximum time (not used for file search).
            vault_path: Path to Obsidian vault.

        Raises:
            ValueError: If vault path is not configured or doesn't exist.
        """
        super().__init__(depth, timeout)

        self.vault_path = vault_path or os.getenv("OBSIDIAN_VAULT_PATH")

        if not self.vault_path:
            raise ValueError(
                "OBSIDIAN_VAULT_PATH not configured. "
                "Set environment variable or pass vault_path parameter."
            )

        if not Path(self.vault_path).is_dir():
            raise ValueError(f"Obsidian vault not found at: {self.vault_path}")

    def _get_source_type(self) -> SourceType:
        """Get source type.

        Returns:
            SourceType.OBSIDIAN.
        """
        return SourceType.OBSIDIAN

    async def collect(self, topic: str) -> list[Source]:
        """Search Obsidian vault for relevant notes.

        Args:
            topic: Research topic to search for.

        Returns:
            List of Source objects from vault notes.
        """
        search_terms = self._generate_search_terms(topic)
        results_count = self._get_results_count()

        logger.info(
            "obsidian_search_started",
            vault_path=self.vault_path,
            search_terms=search_terms,
        )

        sources: list[Source] = []
        vault_dir = Path(self.vault_path)

        # Search markdown files
        markdown_files = list(vault_dir.rglob("*.md"))

        for md_file in markdown_files:
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Simple keyword matching (can be replaced with semantic search)
                relevance_score = self._calculate_relevance(content, search_terms)

                if relevance_score > 0:
                    sources.append(self._create_source(md_file, content, relevance_score))

            except Exception as e:
                logger.warning(
                    "obsidian_file_read_error", file=str(md_file), error=str(e)
                )
                continue

        # Sort by relevance and take top N
        sources.sort(key=lambda s: s.metadata.get("relevance_score", 0), reverse=True)
        sources = sources[:results_count]

        logger.info("obsidian_search_complete", found=len(sources))

        return sources

    def _generate_search_terms(self, topic: str) -> list[str]:
        """Generate search terms from topic.

        Args:
            topic: Research topic.

        Returns:
            List of search terms.
        """
        # Simple tokenization (can be improved with NLP)
        terms = topic.lower().split()

        # Remove common stop words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"}
        terms = [t for t in terms if t not in stop_words and len(t) > 2]

        return terms

    def _calculate_relevance(self, content: str, search_terms: list[str]) -> float:
        """Calculate relevance score for content.

        Args:
            content: Note content.
            search_terms: List of search terms.

        Returns:
            Relevance score (0.0 to 1.0).
        """
        content_lower = content.lower()

        # Count term occurrences
        term_counts = sum(content_lower.count(term) for term in search_terms)

        if term_counts == 0:
            return 0.0

        # Normalize by content length and number of terms
        score = min(term_counts / (len(search_terms) * 5), 1.0)

        return score

    def _get_results_count(self) -> int:
        """Get number of results to return based on depth.

        Returns:
            Number of results.
        """
        counts = {
            ResearchDepth.MINIMAL: 3,
            ResearchDepth.LIGHT: 5,
            ResearchDepth.MODERATE: 8,
            ResearchDepth.DEEP: 12,
            ResearchDepth.EXTENSIVE: 15,
        }
        return counts.get(self.depth, 8)

    def _create_source(
        self, file_path: Path, content: str, relevance_score: float
    ) -> Source:
        """Create Source object from vault note.

        Args:
            file_path: Path to markdown file.
            content: File content.
            relevance_score: Calculated relevance score.

        Returns:
            Source object.
        """
        # Extract frontmatter if present (simplified)
        title = file_path.stem
        tags: list[str] = []

        # Try to extract tags from content
        if "tags:" in content:
            # Very simple tag extraction
            for line in content.split("\n"):
                if line.strip().startswith("tags:"):
                    tags = line.replace("tags:", "").strip().strip("[]").split(",")
                    tags = [t.strip() for t in tags]
                    break

        # Get file modification time
        stat = file_path.stat()
        modified_date = datetime.fromtimestamp(stat.st_mtime)

        return Source(
            source_id=f"obsidian_{hash(str(file_path))}",
            source_type=SourceType.OBSIDIAN,
            title=title,
            url=None,
            content=content[:5000],  # Limit content size
            author="Personal Vault",
            publication_date=modified_date,
            authority_score=0.70,  # Personal notes have medium-high authority
            metadata={
                "file_path": str(file_path.relative_to(self.vault_path)),
                "tags": tags,
                "relevance_score": relevance_score,
                "word_count": len(content.split()),
            },
        )
