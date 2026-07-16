# Short Video Breakdown Report

A Codex skill for turning short-form or vertical videos into reusable content breakdown reports.

It combines frame extraction, speech transcription, subtitle OCR, hook analysis, highlight screenshots, timeline structure, and export-ready HTML/PNG/PDF assets.

## What It Does

This skill helps analyze videos such as:

- short-form food review clips
- lifestyle Vlogs
- e-commerce product seeding videos
- creator reference videos
- vertical social videos that need hook and structure analysis

The workflow is designed around one principle:

> Do not rely on frames alone. Read the video as picture + speech + subtitles + timing + deliverable layout.

## Outputs

Typical outputs include:

- HTML analysis report
- 1080px-wide PNG long image
- optional PDF-ready report
- high-light screenshots
- `transcript.md`
- `transcript_segments.json`
- `ocr_*.json`
- `frame_plan.json`
- `frame_plan_seconds.txt`
- timeline and hook diagnosis
- optimization suggestions for remake/editing

## Skill Contents

```text
short-video-breakdown-report/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── report-structure.md
└── scripts/
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
Use $short-video-breakdown-report to analyze this video into an HTML report with transcript, hooks, highlights, and export-ready assets.
```

## Dependencies

The core workflow is optimized for macOS:

- Swift / AVFoundation for frame extraction
- Vision framework for OCR
- Chrome for HTML-to-PNG rendering
- Python for Whisper transcription
- optional `ffmpeg/ffprobe` for highlight-aware frame planning
- optional `faster-whisper` for local speech transcription

Set up the local Whisper environment:

```bash
cd ~/.codex/skills/short-video-breakdown-report
./scripts/setup_faster_whisper.sh .venv-whisper
```

## Script Usage

Plan frame timestamps from baseline coverage plus scene cuts, speech turns, keywords, and audio peaks:

```bash
scripts/plan_frame_times.py input.mp4 output/frame_plan.json \
  --segments output/transcript/transcript_segments.json
```

Extract frames:

```bash
swift scripts/extract_frames.swift input.mp4 output/frames "$(cat output/frame_plan_seconds.txt)"
```

OCR subtitles and product text:

```bash
swift scripts/ocr_subtitles.swift output/frames output/ocr.json
```

Transcribe audio:

```bash
.venv-whisper/bin/python scripts/transcribe_faster_whisper.py audio.m4a output/transcript \
  --prompt "This is a Chinese short video with spoken copy, subtitles, products, and lifestyle content."
```

Render an HTML report to a 1080px-wide PNG:

```bash
node scripts/render_html_to_png.mjs report.html report.png --width 1080
```

## Recommended Workflow

1. Create a dedicated asset folder for the task.
2. Inspect video duration, resolution, and codec.
3. Extract audio and transcribe spoken copy when possible.
4. Build an evidence-first frame plan; use even coverage only as the safety net.
5. Add high-signal candidates from scene cuts, speech segment boundaries, keyword moments, audio peaks, product reveals, reactions, and CTA endings.
6. Extract planned frames and run OCR to correct subtitle/product-name transcription errors.
7. Add targeted second-pass frames when OCR/transcript review exposes a missed high-light.
8. Identify the actual content hook.
9. Segment the video into functional stages.
10. Select high-light screenshots by role, not only by aesthetics.
11. Generate an HTML report.
12. Optionally export PNG/PDF and verify dimensions, clipping, broken images, and whitespace.

## Report Principles

- Use the strongest content hook as the title.
- Do not present evenly-spaced screenshots as high-lights unless they survive the functional selection pass.
- Every high-light screenshot should prove a specific content function.
- Include a three-second hook diagnosis.
- Summarize spoken copy by timestamp range.
- Use wrapped image grids, not horizontal scrollbars.
- Keep color systems simple and consistent.
- Treat OCR and Whisper output as evidence, not unquestioned truth.
- Correct obvious dialect, subtitle, product-name, and brand-name misreads.

## Notes

This repository contains the reusable skill and helper scripts only. It does not include analyzed videos, transcripts, screenshots, or generated reports from any private project.
