# Short Video Breakdown Report

A Codex skill for turning short-form or vertical videos into reusable content breakdown reports.

It combines frame extraction, audio/BGM rhythm analysis, speech transcription, subtitle OCR, hook diagnosis, highlight screenshots, timeline structure, optimization advice, and a fixed export-ready HTML/PNG report layout.

## What It Does

This skill helps analyze videos such as:

- food review and food-making clips
- lifestyle Vlogs
- e-commerce product seeding videos
- creator reference videos
- vertical social videos that need hook, rhythm, and structure analysis

The workflow is designed around one principle:

> Do not rely on frames alone. Read the video as picture + speech + subtitles + timing + BGM rhythm + deliverable layout.

## Default Deliverable

The default output is not a free-form web page. It is:

- a fixed-layout HTML report based on `assets/fixed-report-template.html`
- a 1080px-wide PNG long image rendered from that HTML

The fixed report layout includes:

- large title/header area
- subtitle, meta tags, and core judgment paragraph
- three right-side metric cards
- `前三秒钩子诊断`
- `字幕、音频与画面校准`
- `高光截图`
- `时间轴拆解`

Only change the layout when the user explicitly asks for a different format.

## Typical Outputs

- `<slug>_video_analysis_report_fixed.html`
- `YYYYMMDD-<strongest-hook>-视频拆解.png`
- optional PDF-ready report
- high-light screenshots under `highlights/`
- action frames under `action_frames/` or `action_highlights/` when action impact matters
- `transcript.md`
- `transcript_segments.json`
- `ocr_*.json`
- `frame_plan.json`
- `frame_plan_seconds.txt`
- `audio.m4a` or equivalent extracted audio
- `audio.wav` when used for beat analysis
- `audio_beat_candidates.json`

## Skill Contents

```text
short-video-breakdown-report/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── fixed-report-template.html
├── references/
│   └── report-structure.md
└── scripts/
    ├── analyze_audio_beats.py
    ├── extract_frames.swift
    ├── ocr_subtitles.swift
    ├── plan_frame_times.py
    ├── render_html_to_png.mjs
    ├── setup_faster_whisper.sh
    └── transcribe_faster_whisper.py
```

## Installation

Clone or copy this folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/tmzbb7tjyb-sys/short-video-breakdown-report.git \
  ~/.codex/skills/short-video-breakdown-report
```

Then invoke it in Codex with:

```text
Use $short-video-breakdown-report to analyze this video and export the fixed-layout PNG report.
```

## Dependencies

The core workflow is optimized for macOS:

- Swift / AVFoundation for frame extraction
- Vision framework for OCR
- `avconvert` / `afconvert` for audio extraction and PCM conversion
- Python for frame planning, BGM energy accent detection, and optional transcription helpers
- Chrome for HTML-to-PNG rendering
- optional `ffmpeg/ffprobe` for scene-change and audio-peak frame planning
- optional `faster-whisper` for local speech transcription

Set up the local Whisper environment:

```bash
cd ~/.codex/skills/short-video-breakdown-report
./scripts/setup_faster_whisper.sh .venv-whisper
```

## Script Usage

Plan frame timestamps from baseline coverage plus scene cuts, speech turns, keywords, action peaks, and audio peaks:

```bash
scripts/plan_frame_times.py input.mp4 output/frame_plan.json \
  --segments output/transcript_segments.json
```

Extract frames:

```bash
swift scripts/extract_frames.swift input.mp4 output/frames "$(cat output/frame_plan_seconds.txt)"
```

Extract audio and run lightweight BGM accent detection:

```bash
avconvert --source input.mp4 --preset PresetAppleM4A \
  --output output/audio.m4a --replace --disableMetadataFilter

afconvert -f WAVE -d LEI16 output/audio.m4a output/audio.wav

scripts/analyze_audio_beats.py output/audio.wav output/audio_beat_candidates.json
```

OCR subtitles and product text:

```bash
swift scripts/ocr_subtitles.swift output/frames output/ocr_frames.json
```

Transcribe audio:

```bash
.venv-whisper/bin/python scripts/transcribe_faster_whisper.py output/audio.m4a output \
  --prompt "This is a Chinese short video with spoken copy, subtitles, products, and lifestyle content."
```

Render the fixed-layout HTML report to a 1080px-wide PNG:

```bash
node scripts/render_html_to_png.mjs \
  output/<slug>_video_analysis_report_fixed.html \
  output/YYYYMMDD-<strongest-hook>-视频拆解.png \
  --width 1080
```

## Recommended Workflow

1. Create a dedicated asset folder for the task.
2. Inspect video duration, resolution, codec, and file size.
3. Extract audio before final screenshot selection whenever possible.
4. Build an evidence-first frame plan; use even coverage only as the safety net.
5. Add high-signal candidates from scene cuts, speech segment boundaries, keyword moments, BGM accents, action peaks, product reveals, reactions, subtitle changes, and CTA endings.
6. Extract planned frames and run OCR to correct subtitle/product-name transcription errors.
7. Run BGM/cut-point analysis and compare beat candidates with visual cuts, object swaps, gestures, reveals, and subtitle pops.
8. Add targeted second-pass frames when OCR/transcript/rhythm review exposes a missed high-light.
9. Identify the actual content hook, including language, action, role/voice, and BGM rhythm mechanisms.
10. Segment the video into functional stages.
11. Select high-light screenshots by content function, not only by aesthetics.
12. Generate fixed-layout HTML using `assets/fixed-report-template.html`.
13. Export the PNG long image and verify dimensions, image references, clipping, whitespace, and layout consistency.

## Analysis Principles

- Use the strongest content hook as the title.
- Explain the hook mechanism, not just the hook text.
- If the video is visibly cut to music, call out `BGM卡点`, `重拍切换`, or `节拍推进`; do not flatten it to "fast pacing".
- Mine action hooks as carefully as language hooks.
- Do not present evenly spaced screenshots as high-lights unless they survive functional selection.
- Every high-light screenshot should prove a specific content function.
- Calibrate scores against execution gaps such as weak proof chain, unclear price/CTA, subjective-only claims, late evidence, or action distracting from the promise.
- Keep transcript/OCR outputs as evidence, not unquestioned truth.
- Correct obvious dialect, subtitle, product-name, and brand-name misreads.

## Layout Rules

- Use `assets/fixed-report-template.html` by default.
- Keep the fixed section order.
- Keep the dense newspaper-style table layout for PNG export.
- Vary the number of calibration cards, highlight figures, and timeline columns only when the video content requires it.
- Do not add horizontal-scroll containers.
- Do not invent a new report style unless the user explicitly asks.

## Notes

This repository contains the reusable skill, fixed report template, and helper scripts only. It does not include analyzed videos, transcripts, screenshots, or generated reports from private projects.
