#!/usr/bin/env python3
"""Create a highlight-aware frame timestamp plan for short video analysis.

The plan intentionally mixes sparse coverage with high-signal candidates:
scene changes, speech turns, keyword moments, and optional audio peaks. It
prints a comma-separated timestamp list that can be passed directly to
extract_frames.swift.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


KEYWORD_RE = re.compile(
    r"(hook|but|however|secret|surprise|finally|result|because|price|cheap|"
    r"expensive|deal|discount|save|proof|before|after|look|watch|wait|"
    r"amazing|crazy|best|worst|fail|love|hate|recommend|buy|order|click|"
    r"但是|可是|结果|没想到|重点|关键|秘密|惊喜|终于|因为|价格|便宜|贵|"
    r"优惠|省|证明|前后|对比|你看|等等|绝了|翻车|推荐|下单|购买|链接|"
    r"评论|关注|收藏|转发|点赞|宝宝|姐妹|家人们|老板|朋友)",
    re.IGNORECASE,
)


@dataclass
class Candidate:
    time: float
    weight: float
    kind: str
    reasons: list[str] = field(default_factory=list)


def run(cmd: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            cmd,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def ffprobe_duration(video: Path) -> float:
    proc = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(video),
        ],
        timeout=30,
    )
    if not proc or proc.returncode != 0:
        raise RuntimeError("ffprobe could not read video duration")
    data = json.loads(proc.stdout)
    duration = float(data["format"]["duration"])
    if not math.isfinite(duration) or duration <= 0:
        raise RuntimeError("invalid video duration from ffprobe")
    return duration


def clamp_time(value: float, duration: float) -> float:
    return max(0.0, min(value, max(duration - 0.05, 0.0)))


def add(
    candidates: list[Candidate],
    duration: float,
    time_value: float,
    weight: float,
    kind: str,
    reason: str,
) -> None:
    candidates.append(
        Candidate(
            time=round(clamp_time(time_value, duration), 2),
            weight=weight,
            kind=kind,
            reasons=[reason],
        )
    )


def add_baseline(candidates: list[Candidate], duration: float) -> None:
    intro_end = min(3.0, duration)
    t = 0.0
    while t <= intro_end + 0.001:
        add(candidates, duration, t, 9.0, "intro", "dense 0-3s hook coverage")
        t += 0.5

    if duration <= 90:
        interval = 5.0
    elif duration <= 240:
        interval = 12.0
    else:
        interval = 20.0

    t = 0.0
    while t < duration:
        add(candidates, duration, t, 1.5, "coverage", f"sparse coverage every {interval:g}s")
        t += interval

    add(candidates, duration, max(duration - 1.0, 0.0), 5.5, "ending", "closing/CTA coverage")


def load_segments(path: Path | None) -> list[dict[str, Any]]:
    if not path or not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        raw = data.get("segments") or data.get("transcript_segments") or []
    elif isinstance(data, list):
        raw = data
    else:
        raw = []

    segments: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        try:
            start = float(item.get("start", item.get("start_time")))
            end = float(item.get("end", item.get("end_time", start)))
        except (TypeError, ValueError):
            continue
        text = str(item.get("text", item.get("sentence", ""))).strip()
        if end < start:
            end = start
        segments.append({"start": start, "end": end, "text": text})
    return segments


def add_transcript_candidates(
    candidates: list[Candidate],
    duration: float,
    segments: list[dict[str, Any]],
) -> None:
    previous_end: float | None = None
    for index, segment in enumerate(segments):
        start = clamp_time(segment["start"], duration)
        end = clamp_time(segment["end"], duration)
        text = segment.get("text", "")

        add(candidates, duration, start + 0.1, 4.0, "speech_start", f"speech segment {index + 1} starts")
        if end - start >= 1.2:
            add(candidates, duration, (start + end) / 2, 3.0, "speech_mid", f"speech segment {index + 1} midpoint")
        if end - start >= 2.2:
            add(candidates, duration, end - 0.15, 3.2, "speech_end", f"speech segment {index + 1} ends")

        if previous_end is not None and start - previous_end >= 0.9:
            add(candidates, duration, start - 0.2, 4.5, "pause_turn", "new beat after a pause")
        previous_end = end

        if KEYWORD_RE.search(text):
            keyword_weight = 8.0 if start <= 3.0 else 6.5
            add(candidates, duration, start + 0.15, keyword_weight, "keyword", f"keyword moment: {text[:60]}")
            if end - start > 1.0:
                add(candidates, duration, min(start + 0.8, end), keyword_weight - 0.8, "keyword_followup", "visual follow-up after keyword")


def add_scene_candidates(
    candidates: list[Candidate],
    duration: float,
    video: Path,
    threshold: float,
) -> None:
    if not shutil.which("ffmpeg"):
        return
    vf = f"select='gt(scene,{threshold})',metadata=print:file=-"
    proc = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-vf", vf, "-an", "-f", "null", "-"], timeout=90)
    if not proc:
        return
    output = proc.stdout + "\n" + proc.stderr
    seen: set[float] = set()
    for match in re.finditer(r"pts_time:([0-9]+(?:\.[0-9]+)?)", output):
        t = round(float(match.group(1)), 2)
        if t in seen:
            continue
        seen.add(t)
        add(candidates, duration, t, 6.0, "scene_cut", f"ffmpeg scene change > {threshold}")


def add_audio_peak_candidates(candidates: list[Candidate], duration: float, video: Path) -> None:
    if not shutil.which("ffmpeg"):
        return
    proc = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-vn",
            "-af",
            "astats=metadata=1:reset=0.5,ametadata=print:key=lavfi.astats.Overall.RMS_level",
            "-f",
            "null",
            "-",
        ],
        timeout=90,
    )
    if not proc:
        return
    output = proc.stdout + "\n" + proc.stderr
    pairs: list[tuple[float, float]] = []
    current_time: float | None = None
    for line in output.splitlines():
        time_match = re.search(r"pts_time:([0-9]+(?:\.[0-9]+)?)", line)
        if time_match:
            current_time = float(time_match.group(1))
        rms_match = re.search(r"lavfi\.astats\.Overall\.RMS_level=(-?[0-9]+(?:\.[0-9]+)?)", line)
        if rms_match and current_time is not None:
            pairs.append((current_time, float(rms_match.group(1))))

    if len(pairs) < 4:
        return
    pairs.sort(key=lambda item: item[1], reverse=True)
    selected: list[float] = []
    for t, _rms in pairs:
        if all(abs(t - prev) >= 1.2 for prev in selected):
            selected.append(t)
        if len(selected) >= 12:
            break
    for t in selected:
        add(candidates, duration, t, 5.2, "audio_peak", "relative audio loudness peak")


def merge_and_select(candidates: list[Candidate], duration: float, min_gap: float, max_frames: int) -> list[Candidate]:
    if not candidates:
        return []

    candidates = sorted(candidates, key=lambda item: item.time)
    clusters: list[list[Candidate]] = []
    for candidate in candidates:
        if not clusters or candidate.time - clusters[-1][-1].time > min_gap:
            clusters.append([candidate])
        else:
            clusters[-1].append(candidate)

    merged: list[Candidate] = []
    for cluster in clusters:
        best = max(cluster, key=lambda item: (item.weight, -abs(item.time - cluster[0].time)))
        reasons: list[str] = []
        kinds: list[str] = []
        weight = best.weight
        for item in cluster:
            weight = max(weight, item.weight)
            if item.kind not in kinds:
                kinds.append(item.kind)
            for reason in item.reasons:
                if reason not in reasons:
                    reasons.append(reason)
        merged.append(Candidate(time=best.time, weight=weight, kind="+".join(kinds), reasons=reasons[:6]))

    if len(merged) <= max_frames:
        return sorted(merged, key=lambda item: item.time)

    protected = [
        item
        for item in merged
        if item.time <= 3.05 or item.time >= max(duration - 2.0, 0.0)
    ]
    protected_times = {item.time for item in protected}
    remaining = [item for item in merged if item.time not in protected_times]
    remaining.sort(key=lambda item: (item.weight, -item.time), reverse=True)

    selected = protected + remaining[: max(0, max_frames - len(protected))]
    return sorted(selected, key=lambda item: item.time)


def default_max_frames(duration: float) -> int:
    if duration <= 90:
        return 56
    if duration <= 240:
        return 80
    return 100


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a highlight-aware frame timestamp plan.")
    parser.add_argument("video", type=Path)
    parser.add_argument("out_json", type=Path)
    parser.add_argument("--segments", type=Path, help="Whisper transcript_segments.json")
    parser.add_argument("--max-frames", type=int, default=None)
    parser.add_argument("--min-gap", type=float, default=0.45)
    parser.add_argument("--scene-threshold", type=float, default=0.22)
    parser.add_argument("--no-audio-peaks", action="store_true")
    args = parser.parse_args()

    if not args.video.exists():
        print(f"Video not found: {args.video}", file=sys.stderr)
        return 2
    if not shutil.which("ffprobe"):
        print("ffprobe is required to plan frame times", file=sys.stderr)
        return 2

    duration = ffprobe_duration(args.video)
    candidates: list[Candidate] = []
    add_baseline(candidates, duration)
    add_scene_candidates(candidates, duration, args.video, args.scene_threshold)
    add_transcript_candidates(candidates, duration, load_segments(args.segments))
    if not args.no_audio_peaks:
        add_audio_peak_candidates(candidates, duration, args.video)

    max_frames = args.max_frames or default_max_frames(duration)
    selected = merge_and_select(candidates, duration, args.min_gap, max_frames)
    seconds = [f"{item.time:.2f}" for item in selected]

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    plan = {
        "video": str(args.video),
        "duration": duration,
        "min_gap": args.min_gap,
        "max_frames": max_frames,
        "seconds_csv": ",".join(seconds),
        "timestamps": [
            {
                "time": item.time,
                "kind": item.kind,
                "weight": item.weight,
                "reasons": item.reasons,
            }
            for item in selected
        ],
    }
    with args.out_json.open("w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    seconds_path = args.out_json.with_name("frame_plan_seconds.txt")
    seconds_path.write_text(plan["seconds_csv"] + "\n", encoding="utf-8")
    print(plan["seconds_csv"])
    print(f"Wrote {args.out_json}", file=sys.stderr)
    print(f"Wrote {seconds_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
