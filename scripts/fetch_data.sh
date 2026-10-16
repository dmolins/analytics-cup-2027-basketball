#!/usr/bin/env bash
# Fetch the SkillCorner ACB open-data repo over plain HTTPS — no git, no git-lfs.
#
# Why: this repo's tracking_data.jsonl.gz files are stored via Git LFS, but GitHub
# serves LFS content directly from media.githubusercontent.com using the same path as
# the repo tree. That means curl can pull everything without the git-lfs client, which
# matters in network environments (like sandboxes) where Git's LFS smudge filter can't
# reach GitHub's LFS API but plain HTTPS to github.com works fine.
#
# Usage:
#   ./scripts/fetch_data.sh                 # docs + aggregates + metadata + 1 game (114243)
#   ./scripts/fetch_data.sh 114243 114234    # docs + aggregates + metadata + these games
#   ./scripts/fetch_data.sh --all            # every one of the 10 sample games (~400 MB)
set -euo pipefail
cd "$(dirname "$0")/.."

REPO="SkillCorner/opendata-basketball"
REF="main"
RAW="https://raw.githubusercontent.com/$REPO/$REF"
MEDIA="https://media.githubusercontent.com/media/$REPO/$REF"
DEST="data/raw/opendata-basketball"
ALL_GAMES=(114243 114234 114169 114099 114086 178442 179612 184439 188630 191313)

if [[ "${1:-}" == "--all" ]]; then
  GAMES=("${ALL_GAMES[@]}")
elif [[ $# -gt 0 ]]; then
  GAMES=("$@")
else
  GAMES=(114243)
fi

mkdir -p "$DEST"/{docs/data_dictionary,data/aggregates,data/matches}

fetch() { # fetch <repo-relative-path>
  local path="$1" out="$DEST/$1"
  mkdir -p "$(dirname "$out")"
  if [[ -s "$out" ]]; then
    echo "  skip (exists): $path"
  else
    echo "  -> $path"
    curl -sL --fail "$RAW/$path" -o "$out"
  fi
}

fetch_lfs() { # fetch_lfs <repo-relative-path>  (pulls via media host, falls back to raw)
  local path="$1" out="$DEST/$1"
  mkdir -p "$(dirname "$out")"
  if [[ -s "$out" ]] && ! grep -q "git-lfs.github.com" "$out" 2>/dev/null; then
    echo "  skip (exists): $path"
    return
  fi
  echo "  -> $path (LFS)"
  curl -sL --fail "$MEDIA/$path" -o "$out"
  if grep -q "git-lfs.github.com" "$out" 2>/dev/null; then
    echo "     media host returned a pointer, retrying via raw host"
    curl -sL --fail "$RAW/$path" -o "$out"
  fi
}

echo "==> docs"
# Full data dictionary, one file per event family (as of 2026-10-11 — if SkillCorner
# adds a table later, add its filename here or just re-run `git ls-remote`/the API tree).
DICT_FILES=(
  README chance_players chances closeouts dribbles drives fouls free_throws game_data
  handoffs isolations matchups off_ball_screens passes picks possessions posts rebounds
  shots timeouts touches tracking_data turnovers
)
for f in README.md docs/PRIMER.md docs/KNOWN_ISSUES.md docs/aggregates_columns.md; do
  fetch "$f" || echo "     (not found, skipping: $f)"
done
for f in "${DICT_FILES[@]}"; do
  fetch "docs/data_dictionary/$f.md" || echo "     (not found, skipping: $f)"
done

echo "==> metadata + aggregates"
fetch "data/matches.json"
fetch "data/player_id_aliases.csv"
for f in acb_shotsaggregates_20252026 acb_drivesaggregates_20252026 acb_picksaggregates_20252026; do
  fetch "data/aggregates/$f.csv"
done

echo "==> games: ${GAMES[*]}"
for g in "${GAMES[@]}"; do
  echo "-- game $g --"
  fetch "data/matches/$g/${g}_game_data.json"
  fetch "data/matches/$g/${g}_dynamic_events.json"
  fetch_lfs "data/matches/$g/${g}_tracking_data.jsonl.gz"
done

echo
echo "Done. Verify a tracking file is real gzip (not an LFS pointer) with, e.g.:"
echo "    file $DEST/data/matches/${GAMES[0]}/${GAMES[0]}_tracking_data.jsonl.gz"
