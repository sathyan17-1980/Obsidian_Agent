"""CLI interface for research-topic command.

Provides command-line interface for executing research workflows.
"""

import argparse
import asyncio
import sys
from pathlib import Path

from src.research.orchestrator import ResearchOrchestrator
from src.research.schemas import ResearchDepth, ResearchRequest
from src.shared.logging import get_logger

logger = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Research-Topic: Multi-source research for LinkedIn/Blog content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (moderate depth, 3 drafts)
  python -m src.research.cli "Neural Networks Part 1"

  # Deep research with 1 draft
  python -m src.research.cli "Neural Networks" --depth deep --drafts 1

  # Light research with 5 drafts
  python -m src.research.cli "Why learn embeddings" --depth light --drafts 5

Depth Levels:
  minimal   - Quick research (~60s, 1-3 queries/source, ~$0.14)
  light     - Basic research (~90s, 3-5 queries/source, ~$0.14)
  moderate  - Standard research (~120s, 5-8 queries/source, ~$0.18) [DEFAULT]
  deep      - Comprehensive (~180s, 8-12 queries/source, ~$0.20)
  extensive - Deep dive (~240s, 12+ queries/source, ~$0.22+)
        """,
    )

    parser.add_argument(
        "topic",
        type=str,
        help="Research topic or question",
    )

    parser.add_argument(
        "--depth",
        type=str,
        choices=["minimal", "light", "moderate", "deep", "extensive"],
        default="moderate",
        help="Research depth level (default: moderate)",
    )

    parser.add_argument(
        "--drafts",
        type=int,
        default=3,
        choices=[1, 2, 3, 4, 5],
        help="Number of draft variations per platform (default: 3)",
    )

    parser.add_argument(
        "--vault-path",
        type=str,
        help="Path to Obsidian vault (overrides OBSIDIAN_VAULT_PATH env var)",
    )

    parser.add_argument(
        "--voice-profile",
        type=str,
        help="Path to voice profile JSON",
    )

    return parser.parse_args()


async def run_research(args: argparse.Namespace) -> int:
    """Run research workflow.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    # Create research request
    request = ResearchRequest(
        topic=args.topic,
        depth=ResearchDepth(args.depth),
        num_drafts=args.drafts,
        voice_profile_path=args.voice_profile,
    )

    # Determine vault path
    import os
    vault_path = args.vault_path or os.getenv("OBSIDIAN_VAULT_PATH")

    if not vault_path:
        logger.error(
            "vault_path_required",
            message="OBSIDIAN_VAULT_PATH environment variable not set. "
            "Please set it or use --vault-path argument.",
        )
        return 1

    if not Path(vault_path).is_dir():
        logger.error("vault_path_invalid", vault_path=vault_path)
        return 1

    # Execute research
    try:
        orchestrator = ResearchOrchestrator(request, vault_path=vault_path)
        results = await orchestrator.execute()

        # Print summary
        print("\n" + "=" * 70)
        print(f"✅ Research Complete: {request.topic}")
        print("=" * 70)
        print(f"\nTopic: {request.topic}")
        print(f"Depth: {request.depth.value}")
        print(f"Execution Time: {results.execution_time_seconds:.2f} seconds")
        print(f"Estimated Cost: ${results.cost_usd:.2f}")
        print(f"\nSources Collected: {len(results.sources)}")

        for source_type, count in results.source_count_by_type.items():
            print(f"  - {source_type}: {count}")

        print(f"\nAverage Source Authority: {results.avg_source_authority:.2f}")
        print(f"Conflicts Detected: {len(results.conflicts)}")
        print(f"Conflicts Resolved: {results.conflicts_resolved_count}")

        print(f"\nGenerated Content:")
        print(f"  - LinkedIn drafts: {len(results.linkedin_drafts)}")
        print(f"  - Blog drafts: {len(results.blog_drafts)}")

        print("\n" + "=" * 70)

        return 0

    except Exception as e:
        logger.exception("research_failed", error=str(e))
        print(f"\n❌ Research failed: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """Main entry point.

    Returns:
        Exit code.
    """
    args = parse_args()
    return asyncio.run(run_research(args))


if __name__ == "__main__":
    sys.exit(main())
