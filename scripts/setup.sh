#!/usr/bin/env bash
# One-command setup. Safe to re-run.
#
# Uses plain python3 -m venv + pip, and scripts/fetch_data.sh (HTTPS, no git-lfs) for the
# dataset. This machine's Homebrew can't reach the bottle CDN, which makes `brew install
# uv`/`git-lfs` fall back to compiling cmake/openssl/etc from source — very slow. If your
# machine *can* reach Homebrew's bottles, swapping back to `uv venv` + `uv pip install`
# and real `git`+`git-lfs` is fine; this path just doesn't assume it.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> python env"
python3 -m venv .venv
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/pip install -q -e ".[dev]"

echo "==> SkillCorner basketball open data (one game: 114243)"
./scripts/fetch_data.sh 114243

echo
echo "Done. Activate with:  source .venv/bin/activate"
echo "Pull more games with: ./scripts/fetch_data.sh <gameId> [<gameId> ...]"
echo "Pull all 10 games with (~400 MB): ./scripts/fetch_data.sh --all"
