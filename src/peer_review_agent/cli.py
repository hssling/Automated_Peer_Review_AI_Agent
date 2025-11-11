"""Command-line entry point for the Peer Review Agent."""

from __future__ import annotations

import argparse
from pathlib import Path

from . import get_version
from .orchestrator import process_articles


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Automate manuscript peer-review collateral creation.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Root directory containing article subfolders (default: current working directory).",
    )
    parser.add_argument(
        "--folder",
        type=Path,
        help="Process a single folder (overrides --root discovery).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate outputs even if files already exist.",
    )
    parser.add_argument(
        "--peer-review",
        action="store_true",
        help="Generate DOCX peer-review comments.",
    )
    parser.add_argument(
        "--annotate",
        action="store_true",
        help="Create annotated text with inline pseudo track-change comments.",
    )
    parser.add_argument(
        "--redline",
        action="store_true",
        help="Produce a redline-style DOCX with action items and suggestions.",
    )
    parser.add_argument("--version", action="version", version=f"peer-review-agent {get_version()}")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    process_articles(
        root=args.root,
        folder=args.folder,
        force=args.force,
        peer_review=args.peer_review,
        annotate=args.annotate,
        redline=args.redline,
    )


if __name__ == "__main__":  # pragma: no cover
    main()

