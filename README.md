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
- optional `faster-whisper` for local speech transcription

Set up the local Whisper environment:

```bash
cd ~/.codex/skills/short-video-breakdown-report
./scripts/setup_faster_whisper.sh .venv-whisper
```

## Script Usage

Extract frames:

```bash
swift scripts/extract_frames.swift input.mp4 output/frames "0,0.5,1,1.5,2,2.5,3"
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
3. Extract intro frames at 0.5s intervals for the first 3 seconds.
4. Extract full-video structure frames at 5s, 10s, 15s, or 30s intervals depending on length.
5. Extract audio and transcribe spoken copy.
6. Run OCR on sampled frames to correct subtitle/product-name transcription errors.
7. Identify the actual content hook.
8. Segment the video into functional stages.
9. Select high-light screenshots by role, not only by aesthetics.
10. Generate an HTML report.
11. Optionally export PNG/PDF and verify dimensions, clipping, broken images, and whitespace.

## Report Principles

- Use the strongest content hook as the title.
- Include a three-second hook diagnosis.
- Summarize spoken copy by timestamp range.
- Use wrapped image grids, not horizontal scrollbars.
- Keep color systems simple and consistent.
- Treat OCR and Whisper output as evidence, not unquestioned truth.
- Correct obvious dialect, subtitle, product-name, and brand-name misreads.

## Notes

This repository contains the reusable skill and helper scripts only. It does not include analyzed videos, transcripts, screenshots, or generated reports from any private project.
