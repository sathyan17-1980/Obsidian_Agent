"""Main research orchestrator.

Coordinates the entire research workflow from source collection
through content generation and file output.
"""

import asyncio
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.research.schemas import (
    ResearchDepth,
    ResearchRequest,
    ResearchResults,
    Source,
)
from src.research.sources.article_extractor import ArticleExtractor
from src.research.sources.brave_search import BraveSearchCollector
from src.research.sources.google_drive import GoogleDriveCollector
from src.research.sources.hackernews import HackerNewsCollector
from src.research.sources.obsidian_vault import ObsidianVaultCollector
from src.research.sources.youtube import YouTubeCollector
from src.shared.logging import get_logger

logger = get_logger(__name__)


class ResearchOrchestrator:
    """Orchestrates the complete research workflow.

    Manages:
    1. Parallel source collection (6 sources)
    2. Deduplication and aggregation
    3. Conflict detection
    4. Content generation
    5. File output to Obsidian vault
    6. PDF generation
    7. Git operations

    Args:
        request: Research request parameters.
        vault_path: Path to Obsidian vault.
    """

    def __init__(self, request: ResearchRequest, vault_path: Optional[str] = None) -> None:
        """Initialize research orchestrator.

        Args:
            request: Research request with topic, depth, etc.
            vault_path: Path to Obsidian vault (required).

        Raises:
            ValueError: If vault_path is not provided.
        """
        self.request = request
        self.vault_path = vault_path

        if not self.vault_path:
            raise ValueError("vault_path is required for Obsidian integration")

    async def execute(self) -> ResearchResults:
        """Execute the complete research workflow.

        Returns:
            ResearchResults with all collected sources and generated content.
        """
        start_time = time.time()

        logger.info(
            "research_started",
            topic=self.request.topic,
            depth=self.request.depth.value,
            num_drafts=self.request.num_drafts,
        )

        # Step 3: Execute multi-source research (parallel)
        all_sources = await self._collect_sources()

        # Step 4: Aggregate and deduplicate
        unique_sources = self._deduplicate_sources(all_sources)

        # Step 4.2 & 4.3: Conflict detection (simplified - skip for now)
        conflicts = []

        # Step 5: Generate content (simplified - to be implemented)
        linkedin_drafts = []
        blog_drafts = []

        # Calculate execution time and cost
        execution_time = time.time() - start_time
        cost = self._estimate_cost(len(unique_sources), self.request.num_drafts)

        results = ResearchResults(
            request=self.request,
            sources=unique_sources,
            conflicts=conflicts,
            linkedin_drafts=linkedin_drafts,
            blog_drafts=blog_drafts,
            execution_time_seconds=execution_time,
            cost_usd=cost,
        )

        logger.info(
            "research_completed",
            sources=len(unique_sources),
            execution_time=f"{execution_time:.2f}s",
            cost=f"${cost:.2f}",
        )

        return results

    async def _collect_sources(self) -> list[Source]:
        """Collect sources from all 6 sources in parallel.

        Returns:
            List of all collected sources.
        """
        logger.info("source_collection_started", sources=6)

        # Initialize collectors
        collectors = [
            HackerNewsCollector(self.request.depth),
            BraveSearchCollector(self.request.depth),
            ObsidianVaultCollector(self.request.depth, vault_path=self.vault_path),
            YouTubeCollector(self.request.depth),  # Stub
            GoogleDriveCollector(self.request.depth),  # Stub
        ]

        # Collect from all sources in parallel
        tasks = [
            collector.collect_with_error_handling(self.request.topic)
            for collector in collectors
        ]

        results = await asyncio.gather(*tasks)

        # Flatten results
        all_sources: list[Source] = []
        for source_list in results:
            all_sources.extend(source_list)

        # Now extract full articles from web sources
        web_sources = [s for s in all_sources if s.source_type.value == "web"]
        if web_sources:
            article_extractor = ArticleExtractor(
                self.request.depth, sources_to_extract=web_sources
            )
            article_sources = await article_extractor.collect(self.request.topic)
            all_sources.extend(article_sources)

        logger.info("source_collection_completed", total=len(all_sources))

        return all_sources

    def _deduplicate_sources(self, sources: list[Source]) -> list[Source]:
        """Deduplicate sources by URL.

        Args:
            sources: List of sources to deduplicate.

        Returns:
            Deduplicated list of sources.
        """
        seen_urls: set[str] = set()
        unique_sources: list[Source] = []

        for source in sources:
            if source.url:
                url = str(source.url)
                if url not in seen_urls:
                    seen_urls.add(url)
                    unique_sources.append(source)
            else:
                # No URL (e.g., Obsidian notes), include it
                unique_sources.append(source)

        logger.info(
            "deduplication_complete",
            original=len(sources),
            unique=len(unique_sources),
            removed=len(sources) - len(unique_sources),
        )

        return unique_sources

    def _estimate_cost(self, num_sources: int, num_drafts: int) -> float:
        """Estimate research cost.

        Args:
            num_sources: Number of sources collected.
            num_drafts: Number of drafts per platform.

        Returns:
            Estimated cost in USD.
        """
        # Simplified cost estimation
        depth_costs = {
            ResearchDepth.MINIMAL: 0.14,
            ResearchDepth.LIGHT: 0.14,
            ResearchDepth.MODERATE: 0.18,
            ResearchDepth.DEEP: 0.20,
            ResearchDepth.EXTENSIVE: 0.22,
        }

        return depth_costs.get(self.request.depth, 0.18)
