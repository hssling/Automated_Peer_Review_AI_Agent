# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-11-11

### Added
- Initial release of the automated peer-review agent with:
  - PDF/DOCX ingestion and heuristic study appraisal.
  - Markdown report, PPTX deck, peer-review DOCX, annotated text, and redline reviewer output.
  - CLI (`peer-review-agent`) with `--peer-review`, `--annotate`, `--redline`, and `--force` toggles.
  - Packaging via `pyproject.toml`, `requirements.txt`, and editable install support.
  - GitHub Actions CI (lint + pytest) plus basic unit tests.
- Documentation covering installation, CLI usage, and roadmap.
- Published package to PyPI (`pip install peer-review-agent` / `pipx install peer-review-agent`).

