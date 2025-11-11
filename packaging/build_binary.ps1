@
param()

$ErrorActionPreference = "Stop"

python -m pip install --upgrade pip
python -m pip install .[binary]

pyinstaller packaging/peer_review_agent.spec --clean

Write-Host "Binary available under dist/peer-review-agent/"

