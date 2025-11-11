#!/usr/bin/env bash
set -euo pipefail

# Usage: ./packaging/build_binary.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python -m pip install --upgrade pip
python -m pip install .[binary]

pyinstaller packaging/peer_review_agent.spec --clean

echo "Binary available under dist/peer-review-agent/"
