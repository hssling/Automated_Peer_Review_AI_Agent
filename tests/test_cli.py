from pathlib import Path

import peer_review_agent.cli as cli


def test_cli_runs_without_articles(tmp_path: Path) -> None:
    cli.main(["--root", str(tmp_path)])


def test_cli_accepts_custom_config(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        """
{
  "design_keywords": [
    {"keyword": "custom", "label": "Custom Design"}
  ]
}
""".strip()
    )
    cli.main(["--root", str(tmp_path), "--config", str(config_path)])
