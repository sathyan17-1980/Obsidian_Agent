"""Pydantic schemas for research workflow.

This module defines all data models used throughout the research pipeline.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, HttpUrl


class ResearchDepth(str, Enum):
    """Research depth levels."""

    MINIMAL = "minimal"
    LIGHT = "light"
    MODERATE = "moderate"
    DEEP = "deep"
    EXTENSIVE = "extensive"


class DraftStrategy(str, Enum):
    """Content generation strategy."""

    TECHNICAL = "technical"
    STORY = "story"
    BALANCED = "balanced"


class SourceType(str, Enum):
    """Types of research sources."""

    HACKERNEWS = "hackernews"
    WEB = "web"
    ARTICLE = "article"
    OBSIDIAN = "obsidian"
    GOOGLE_DRIVE = "google_drive"
    YOUTUBE = "youtube"


class ConflictType(str, Enum):
    """Types of conflicts between sources."""

    FACTUAL = "factual"
    TEMPORAL = "temporal"
    DEFINITIONAL = "definitional"
    OPINION = "opinion"


class ConflictSeverity(str, Enum):
    """Severity levels for conflicts."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ResearchRequest(BaseModel):
    """Request parameters for research."""

    topic: str = Field(..., description="Research topic or question")
    depth: ResearchDepth = Field(
        default=ResearchDepth.MODERATE, description="Research depth level"
    )
    num_drafts: int = Field(
        default=3, ge=1, le=5, description="Number of draft variations per platform"
    )
    voice_profile_path: Optional[str] = Field(
        default=None, description="Path to voice profile JSON"
    )


class Source(BaseModel):
    """A single research source."""

    source_id: str = Field(..., description="Unique source identifier")
    source_type: SourceType = Field(..., description="Type of source")
    title: str = Field(..., description="Source title")
    url: Optional[HttpUrl] = Field(default=None, description="Source URL")
    content: str = Field(..., description="Extracted content")
    author: Optional[str] = Field(default=None, description="Author name")
    publication_date: Optional[datetime] = Field(
        default=None, description="Publication date"
    )
    authority_score: float = Field(
        ..., ge=0.0, le=1.0, description="Source authority score"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class Conflict(BaseModel):
    """A detected conflict between sources."""

    conflict_type: ConflictType = Field(..., description="Type of conflict")
    severity: ConflictSeverity = Field(..., description="Severity level")
    description: str = Field(..., description="Brief description of conflict")
    sources: list[str] = Field(..., description="Source IDs involved")
    resolution: Optional[str] = Field(
        default=None, description="Resolution if resolved"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Resolution confidence"
    )
    resolved: bool = Field(default=False, description="Whether conflict is resolved")


class ContentDraft(BaseModel):
    """A generated content draft."""

    platform: Literal["linkedin", "blog"] = Field(..., description="Target platform")
    strategy: DraftStrategy = Field(..., description="Generation strategy")
    content: str = Field(..., description="Generated content")
    word_count: int = Field(..., description="Word count")
    voice_match_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Voice matching score"
    )
    seo_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="SEO score (blog only)"
    )
    plagiarism_check_passed: bool = Field(
        default=False, description="Plagiarism check result"
    )
    citations: list[str] = Field(
        default_factory=list, description="Citation source IDs used"
    )
    hashtags: list[str] = Field(
        default_factory=list, description="Suggested hashtags (LinkedIn)"
    )


class ResearchResults(BaseModel):
    """Complete research results."""

    request: ResearchRequest = Field(..., description="Original request")
    sources: list[Source] = Field(
        default_factory=list, description="All collected sources"
    )
    conflicts: list[Conflict] = Field(
        default_factory=list, description="Detected conflicts"
    )
    linkedin_drafts: list[ContentDraft] = Field(
        default_factory=list, description="LinkedIn post drafts"
    )
    blog_drafts: list[ContentDraft] = Field(
        default_factory=list, description="Blog article drafts"
    )
    execution_time_seconds: float = Field(..., description="Total execution time")
    cost_usd: float = Field(..., description="Estimated cost")
    vault_path: Optional[str] = Field(
        default=None, description="Path in Obsidian vault"
    )

    @property
    def source_count_by_type(self) -> dict[str, int]:
        """Get source counts by type.

        Returns:
            Dictionary mapping source type to count.
        """
        counts: dict[str, int] = {}
        for source in self.sources:
            source_type = source.source_type.value
            counts[source_type] = counts.get(source_type, 0) + 1
        return counts

    @property
    def avg_source_authority(self) -> float:
        """Calculate average source authority.

        Returns:
            Average authority score across all sources.
        """
        if not self.sources:
            return 0.0
        return sum(s.authority_score for s in self.sources) / len(self.sources)

    @property
    def conflicts_resolved_count(self) -> int:
        """Count resolved conflicts.

        Returns:
            Number of conflicts that were resolved.
        """
        return sum(1 for c in self.conflicts if c.resolved)


class VoiceProfile(BaseModel):
    """User's writing style profile."""

    sentence_length_avg: float = Field(..., description="Average sentence length")
    vocabulary_complexity: float = Field(
        ..., ge=0.0, le=1.0, description="Vocabulary complexity score"
    )
    formality_score: float = Field(
        ..., ge=0.0, le=1.0, description="Formality level"
    )
    common_phrases: list[str] = Field(
        default_factory=list, description="Frequently used phrases"
    )
    transition_words: list[str] = Field(
        default_factory=list, description="Common transition words"
    )
    tone_markers: dict[str, float] = Field(
        default_factory=dict, description="Tone characteristics"
    )
    structural_patterns: dict[str, Any] = Field(
        default_factory=dict, description="Structural patterns"
    )
