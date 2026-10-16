"""Loading and small helpers for SkillCorner tracking data (25 fps, feet, centre-court
origin). See docs/data-notes.md and the data dictionary in data/raw/opendata-basketball
for conventions and known traps (isDetected / predError, smoothing before derivatives).
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

GAME_DIR = Path("data/raw/opendata-basketball/data/matches")


def load_events(game_id: int) -> dict:
    """Return the full dynamic_events dict for one game (one array per event family)."""
    path = GAME_DIR / str(game_id) / f"{game_id}_dynamic_events.json"
    return json.loads(path.read_text())


def load_game_data(game_id: int) -> dict:
    """Return game metadata: teams, rosters, competition/season ids."""
    path = GAME_DIR / str(game_id) / f"{game_id}_game_data.json"
    return json.loads(path.read_text())


def roster_lookup(game_data: dict) -> dict[int, dict]:
    """playerId -> {name, jersey, teamId, teamName} across both rosters."""
    out = {}
    for side in ("homeTeam", "awayTeam"):
        team = game_data[side]
        for p in team["players"]:
            out[p["playerId"]] = {
                "name": f"{p['firstName']} {p['lastName']}",
                "jersey": p["jersey"],
                "teamId": team["teamId"],
                "teamName": team["teamName"],
            }
    return out


def load_tracking_range(game_id: int, start_frame: int, end_frame: int) -> list[dict]:
    """Read frames with frameIdx in [start_frame, end_frame] (inclusive) from the
    gzipped JSONL tracking file.

    TRAP: frameIdx is NOT the line number. Dead broadcast time between periods (and
    possibly elsewhere) is not written to the file at all, so line_index <= frameIdx
    always, with the gap growing through the game (measured on game 114243: 0 missing
    frames at the start of Q1, 592 by the start of Q2, 1,206 by Q3, 2,668 by Q4).
    Event records' startFrame/endFrame are frameIdx values, so slicing by line number
    silently returns the wrong, unrelated segment of the game — confirmed the hard way
    while building the first closeout animation (notes/journal.md, 2026-10-16).

    frameIdx is monotonically non-decreasing (verified across all 146,870 frames of
    game 114243), so a single forward scan is correct and sufficient. We read frameIdx
    out of the raw line via a cheap string split rather than a full json.loads for
    every skipped line, since the target frame can be 50k+ lines into the file.
    """
    path = GAME_DIR / str(game_id) / f"{game_id}_tracking_data.jsonl.gz"
    frames = []
    with gzip.open(path, "rt") as f:
        for line in f:
            frame_idx = int(line.split('"frameIdx": ', 1)[1].split(",", 1)[0])
            if frame_idx < start_frame:
                continue
            if frame_idx > end_frame:
                break
            frames.append(json.loads(line))
    return frames


def fmt_clock(seconds: float) -> str:
    """Game clock seconds -> M:SS, as shown on a scoreboard."""
    m, s = divmod(max(0, seconds), 60)
    return f"{int(m)}:{s:04.1f}"
