# Automated Peer Review AI Agent

[![PyPI version](https://img.shields.io/pypi/v/peer-review-agent.svg)](https://pypi.org/project/peer-review-agent/)

An end-to-end automation toolkit that ingests research articles (PDF or DOCX), extracts text, performs heuristic quality checks, and produces a full peer-review packet for journal clubs or manuscript review boards.

## Key Features

- **Multiformat ingestion** – reads both PDF and DOCX sources.
- **Heuristic appraisal** – detects study design, sample size, statistical methods, and flags missing elements (power statements, limitations, precision, etc.).
- **Auto-generated collateral**:
  - Markdown critical analysis report.
  - Presentation-ready PPTX deck.
  - Structured peer-review DOCX (major/minor comments).
  - Annotated text file with inline pseudo track changes.
  - Redline-style DOCX with prioritized action items and section-specific rewrite suggestions (works for PDFs by embedding extracted text).
- **Batch orchestration** – scan a root directory or target a single project folder.
- **Extensible CLI** – toggle peer-review artifacts, annotations, and redlines independently.

## Installation & Distribution Options

1. **Local development (recommended)**  
   ```bash
   git clone https://github.com/hssling/Automated_Peer_Review_AI_Agent.git
   cd Automated_Peer_Review_AI_Agent
   python -m venv .venv && .venv\Scripts\activate  # or source .venv/bin/activate on *nix
   pip install -e .
   ```
   Editable installs make iterating on heuristics and outputs straightforward.

2. **PyPI / pip / pipx (published)**  
   Install the released package directly:
   ```bash
   pip install peer-review-agent        # global / venv install
   pipx install peer-review-agent       # isolated CLI install
   ```
   After installing, invoke `peer-review-agent --help`.

3. **Standalone binaries (new)**  
   Build a single-file executable with PyInstaller for users without Python:
   ```bash
   # Linux/macOS
   ./packaging/build_binary.sh

   # Windows PowerShell
   ./packaging/build_binary.ps1
   ```
   The resulting binary lives under `dist/peer-review-agent/`. Distribute this artifact directly or attach it to GitHub Releases.

4. **Containerization (suggested)**  
   For fully reproducible deployments (CI agents, on-prem review services), wrap the CLI in a lightweight Python container (e.g., Python 3.11-slim) and mount the articles directory. See “Future Enhancements” for ideas.

## CLI Usage

After installation, the CLI `peer-review-agent` becomes available.

```bash
peer-review-agent --root "/path/to/root" [--peer-review] [--annotate] [--redline] [--force]
```

Common workflows:

- **Single project folder**
  ```bash
  peer-review-agent --folder "D:/Journal club/TB cohort study" --peer-review --annotate --redline
  ```
- **Batch process every subfolder under a root directory**
  ```bash
  peer-review-agent --root "/data/articles" --peer-review --annotate
  ```

Flags:

- `--root PATH` – scan root subfolders for PDFs/DOCXs.
- `--folder PATH` – process a specific folder (overrides `--root` discovery).
- `--peer-review` – create structured DOCX peer-review memo.
- `--annotate` – emit annotated text with inline pseudo comments.
- `--redline` – generate redline-style DOCX with action plan and rewrite suggestions (works for PDF inputs via extracted text).
- `--force` – rebuild outputs even if files already exist.

## Output Artifacts

For each source article `<stem>` the agent produces (based on enabled flags):

- `<stem>.txt` – raw extracted text.
- `<stem>_auto_critical_analysis.md` – heuristic report with strengths/gaps.
- `<stem>_auto_appraisal.pptx` – slide deck summarizing findings.
- `<stem>_peer_review.docx` – major/minor comment log (when `--peer-review`).
- `<stem>_annotated_comments.txt` – inline comments (when `--annotate`).
- `<stem>_redline_review.docx` – prioritized action list + inline suggestions (when `--redline`).

Derived artifacts are automatically skipped during subsequent runs to avoid recursion.

## Requirements

- Python 3.9+
- Dependencies: `PyPDF2`, `python-docx`, `python-pptx`

Install via pip/venv:
```bash
pip install -r requirements.txt
```

## Continuous Integration

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs linting and unit tests on every push/pull request using Python 3.11. Extend the pipeline with packaging/publishing steps once ready to distribute wheels or Docker images.

## Tests

Unit tests live under `tests/`. Run:
```bash
pytest
```

## Roadmap / Future Enhancements

- Publish pre-built wheels to PyPI for `pip install peer-review-agent`.
- Add optional Docker image for air-gapped deployments.
- Integrate citation parsing and GRADE-style scoring.
- Support configurable templates (custom PPT branding, peer-review rubrics).

Contributions and issue reports are welcome!
