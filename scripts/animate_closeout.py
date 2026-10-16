#!/usr/bin/env python
"""Animate one `closeouts` event on a FIBA court, from the catch through the shot.

Usage:
    .venv/bin/python scripts/animate_closeout.py [closeout_id] [--game 114243]

With no id, picks a clear example: a long closeout (defender starts far, closes to a
tight contest) that ends in a direct shot. Saves a GIF to outputs/clips/.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from mplbasketball.court import Court

from acb.tracking import fmt_clock, load_events, load_game_data, load_tracking_range, roster_lookup

OFFENSE_COLOR = "#d1495b"   # team with the ball
DEFENSE_COLOR = "#2b6a99"   # team closing out
BALL_COLOR = "#e0a500"
MUTED_ALPHA = 0.35
PREROLL_FRAMES = 20   # ~0.8s before the touch, so the catch is visible
POSTROLL_FRAMES = 15  # ~0.6s after the shot, to see it resolve


def pick_closeout(events: dict, closeout_id: str | None) -> dict:
    closeouts = events["closeouts"]
    if closeout_id:
        return next(c for c in closeouts if c["id"] == closeout_id)
    # Default: biggest gap closed (startDistance - endDistance), among direct shots only.
    candidates = [c for c in closeouts if c["direct"] and c["bhrAction"] == "shot"]
    return max(candidates, key=lambda c: c["startDistance"] - c["endDistance"])


def matching_shot(events: dict, chance_id: str) -> dict | None:
    return next((s for s in events["shots"] if s["chanceId"] == chance_id), None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("closeout_id", nargs="?", default=None)
    ap.add_argument("--game", type=int, default=114243)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    game_id = args.game
    events = load_events(game_id)
    game_data = load_game_data(game_id)
    roster = roster_lookup(game_data)

    co = pick_closeout(events, args.closeout_id)
    shot = matching_shot(events, co["chanceId"])

    start_frame = co["touchFrame"] - PREROLL_FRAMES
    end_frame = (shot["endFrame"] if shot else co["endFrame"]) + POSTROLL_FRAMES
    frames = load_tracking_range(game_id, start_frame, end_frame)

    bh = roster[co["ballhandlerId"]]
    df = roster[co["ballhandlerDefId"]]
    off_team_id, def_team_id = co["offTeamId"], co["defTeamId"]

    print(f"Closeout {co['id']}  |  {bh['name']} ({bh['teamName']}) vs "
          f"{df['name']} ({df['teamName']})")
    print(f"  distance: touch {co['touchDistance']:.1f} ft -> start {co['startDistance']:.1f} ft "
          f"-> end {co['endDistance']:.1f} ft, over {(co['endFrame']-co['startFrame'])/25:.1f}s")
    if shot:
        made = "MADE" if shot["outcome"] else "missed"
        print(f"  outcome: {'3PT' if shot['three'] else '2PT'} {shot['shotType']} jumper, {made}, "
              f"shot quality (model) {shot.get('shotQuality', float('nan')):.0f}, "
              f"closest defender at release {shot.get('closestDefDist', float('nan')):.1f} ft "
              f"({shot.get('contestLevel')})")

    # ---- figure / court -----------------------------------------------------------
    court = Court(court_type="fiba", origin="center", units="ft")
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    court.draw(ax=ax, orientation="h", court_color="none", line_color="#9aa0a6", line_width=1.2)
    ax.set_facecolor("#0e1117" if plt.rcParams["figure.facecolor"] != "white" else "white")

    # Zoom to the half of the court where the action happens. Deliberately computed
    # from the RAW tracking positions we are about to plot, not from the closeout's
    # own location/startLoc/endLoc fields: those event-table fields are normalized so
    # the offense always attacks negative x, while raw tracking_data xyz stays fixed
    # to the physical camera frame — the two are NOT directly comparable (confirmed by
    # comparing startLoc to the raw xyz at the same frame/player; see
    # docs/data-notes.md). Using event fields here silently zoomed into the wrong half
    # for some events and left the real dots off-canvas.
    bh_xs = [p["xyz"][0] for f in frames for p in f["homePlayers"] + f["awayPlayers"]
             if p["playerId"] == co["ballhandlerId"]]
    court_half = court.court_parameters["court_dims"][0] / 2
    if np.mean(bh_xs) < 0:
        ax.set_xlim(-court_half - 2, 2)
    else:
        ax.set_xlim(-2, court_half + 2)
    ax.set_ylim(-court.court_parameters["court_dims"][1] / 2 - 2,
                court.court_parameters["court_dims"][1] / 2 + 2)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    n_players = 10
    player_dots = [ax.plot([], [], "o", ms=10, mew=1.2, zorder=3)[0] for _ in range(n_players)]
    player_labels = [ax.text(0, 0, "", ha="center", va="center", fontsize=6.5,
                              fontweight="bold", color="white", zorder=4) for _ in range(n_players)]
    ball_dot, = ax.plot([], [], "o", ms=7, color=BALL_COLOR, zorder=5,
                         markeredgecolor="#5c3c00", mew=0.8)
    link_line, = ax.plot([], [], "--", lw=1.3, color="white", alpha=0.8, zorder=2)
    dist_text = ax.text(0, 0, "", fontsize=8, color="white", ha="center", zorder=6,
                         bbox=dict(boxstyle="round,pad=0.2", fc="black", ec="none", alpha=0.55))
    clock_text = ax.text(0.01, 0.98, "", transform=ax.transAxes, fontsize=9, va="top",
                          color="white", family="monospace")
    phase_text = ax.text(0.99, 0.98, "", transform=ax.transAxes, fontsize=10, va="top",
                          ha="right", color="white", fontweight="bold")
    n_text = ax.text(0.5, 0.02, "", transform=ax.transAxes, fontsize=7.5, color="#9aa0a6",
                      ha="center")
    fig.patch.set_facecolor("#0e1117")

    n_frames = len(frames)
    n_text.set_text(f"n = {n_frames} frames shown (25 fps) · game {game_id} · "
                     f"SkillCorner broadcast tracking, ACB 2025/26")

    # Note: startFrame (defender begins sprinting out) can be *before* touchFrame (the
    # catch) — closeouts start anticipating the pass, not just reacting to the catch.
    def phase_for(frame_idx: int) -> str:
        if frame_idx < min(co["startFrame"], co["touchFrame"]):
            return "approach"
        if frame_idx < co["touchFrame"]:
            return "closing out"
        if frame_idx <= co["endFrame"]:
            return "CLOSEOUT (ball live)"
        if shot and frame_idx <= shot["endFrame"]:
            return "SHOT"
        return "result"

    def update(i):
        frame = frames[i]
        all_players = frame["homePlayers"] + frame["awayPlayers"]
        for dot, lbl in zip(player_dots, player_labels):
            dot.set_data([], [])
            lbl.set_text("")
        bh_xy = df_xy = None
        for j, p in enumerate(all_players[:n_players]):
            x, y, _ = p["xyz"]
            dot, lbl = player_dots[j], player_labels[j]
            pid = p["playerId"]
            is_bh = pid == co["ballhandlerId"]
            is_df = pid == co["ballhandlerDefId"]
            team_in_home = any(hp.get("playerId") == pid for hp in frame["homePlayers"])
            team_id = game_data["homeTeam"]["teamId"] if team_in_home else game_data["awayTeam"]["teamId"]
            base_color = OFFENSE_COLOR if team_id == off_team_id else DEFENSE_COLOR
            if is_bh or is_df:
                dot.set_data([x], [y])
                dot.set_markerfacecolor(base_color)
                dot.set_markeredgecolor("white")
                dot.set_alpha(1.0)
                dot.set_ms(13)
                lbl.set_position((x, y))
                lbl.set_text(p.get("jersey", ""))
                if is_bh:
                    bh_xy = (x, y)
                else:
                    df_xy = (x, y)
            else:
                dot.set_data([x], [y])
                dot.set_markerfacecolor(base_color)
                dot.set_markeredgecolor("none")
                dot.set_alpha(MUTED_ALPHA)
                dot.set_ms(9)
                lbl.set_text("")
        ball = frame.get("ball") or {}
        if ball:
            bx, by = ball["xyz"][0], ball["xyz"][1]
            ball_dot.set_data([bx], [by])
        else:
            ball_dot.set_data([], [])

        if bh_xy and df_xy:
            link_line.set_data([bh_xy[0], df_xy[0]], [bh_xy[1], df_xy[1]])
            d_ft = float(np.hypot(bh_xy[0] - df_xy[0], bh_xy[1] - df_xy[1]))
            mx, my = (bh_xy[0] + df_xy[0]) / 2, (bh_xy[1] + df_xy[1]) / 2
            dist_text.set_position((mx, my + 1.6))
            dist_text.set_text(f"{d_ft:.1f} ft")
        else:
            link_line.set_data([], [])
            dist_text.set_text("")

        clock_text.set_text(f"Q{frame['period']}  {fmt_clock(frame['gameClock'])}")
        phase_text.set_text(phase_for(frame["frameIdx"]))
        return player_dots + player_labels + [ball_dot, link_line, dist_text, clock_text, phase_text]

    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000 / 25, blit=False)

    out = Path(args.out) if args.out else Path("outputs/clips") / f"closeout_{game_id}_{co['id'].split('-')[-2]}-{co['id'].split('-')[-1]}.gif"
    out.parent.mkdir(parents=True, exist_ok=True)
    anim.save(out, writer=PillowWriter(fps=25))
    plt.close(fig)
    print(f"\nSaved {out}  ({out.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
