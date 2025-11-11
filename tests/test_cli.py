from pathlib import Path

import peer_review_agent.cli as cli


def test_cli_runs_without_articles(tmp_path: Path) -> None:
    # Should complete without raising even when directory has no article files.
    cli.main(["--root", str(tmp_path)])

