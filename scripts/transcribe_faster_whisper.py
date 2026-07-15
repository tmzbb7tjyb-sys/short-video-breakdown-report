#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from faster_whisper import WhisperModel


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe audio with faster-whisper.")
    parser.add_argument("audio")
    parser.add_argument("out_dir")
    parser.add_argument("--model", default="small")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--prompt", default="这是一段中文短视频口播，可能包含方言、产品名、食物名、生活化表达和字幕文案。")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    args = parser.parse_args()

    audio = Path(args.audio)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    segments_iter, info = model.transcribe(
        str(audio),
        language=args.language,
        beam_size=5,
        vad_filter=True,
        initial_prompt=args.prompt,
    )

    segments = []
    for seg in segments_iter:
        text = seg.text.strip()
        if not text:
            continue
        item = {"start": round(seg.start, 2), "end": round(seg.end, 2), "text": text}
        segments.append(item)
        print(f"[{item['start']:07.2f} - {item['end']:07.2f}] {text}", flush=True)

    payload = {
        "language": info.language,
        "language_probability": info.language_probability,
        "duration": info.duration,
        "segments": segments,
    }
    (out_dir / "transcript_segments.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# 口播转写",
        "",
        f"- language: {info.language}",
        f"- language_probability: {info.language_probability:.4f}",
        f"- duration: {info.duration:.2f}s",
        "",
    ]
    for item in segments:
        lines.append(f"- `{item['start']:06.2f}-{item['end']:06.2f}` {item['text']}")
    (out_dir / "transcript.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
