# Short Video Breakdown Report

Codex skills for turning short-form or vertical videos into reusable content analysis reports.

This repository now contains two versions:

| Version | Path | Best For | Default Deliverable |
|---|---|---|---|
| 1.0 | repository root | Evidence-first video structure breakdown: hook, rhythm, transcript, OCR, screenshots, timeline, and remake advice | Fixed-layout HTML source plus 1080px PNG long image |
| 2.0 | `short-video-breakdown-report-2-0/` | Douyin/Juliang Yuntu-style single-video marketing content asset diagnosis | Single-page long-canvas PDF |

## 2.0 New Capabilities

`short-video-breakdown-report-2-0` keeps the 1.0 video evidence workflow and adds a marketing content asset layer:

- **巨量云图式链路诊断**: `选人 -> 做内容 -> 爆文识别 -> 加热放大 -> 搜索承接 -> 转化承接 -> 复盘沉淀`.
- **内容资产定位**: judge what audience the video influences, what seeding mechanism it uses, whether it is worth amplification, and what downstream path it should hand off to.
- **达人与TA匹配**: evaluate persona credibility, target-user overlap, content label fit, category fit, scene credibility, and risks.
- **音色/声线拆解**: analyze timbre, speed, breath, pause, fatigue, urgency, nasal tone, crying edge, excitement, calm authority, dialect, and ad-resistance effects.
- **证明链诊断**: inspect whether the clip builds `hook -> pain/scene -> product claim -> proof/sensory evidence -> trust cue -> search/conversion cue`.
- **量爆/质爆/加热判断**: separate creative potential from measured platform performance. Use labels such as `量爆信号`, `质爆潜力`, `小预算试热`, and `待核验` when data is incomplete.
- **搜索承接**: extract brand words, product words, function words, scene words, comparison words, and 小蓝词/comment-pin opportunities.
- **转化承接**: decide whether the next step should be product page, live room, brand search/brand zone, local store, form/private message, or follow-up content.
- **可复用brief**: end with the next creator type, voice requirement, opening formula, must-shoot frames, proof points, search words, CTA, monitoring metrics, and heat strategy.
- **干净版表格视觉**: white plus 8% gray alternating rows, low-saturation Mac-like tech styling, and sparse bold/color emphasis for key words in dense tables.
- **长画布PDF交付**: default to a single-page long-canvas PDF. HTML is only an internal render source by default. PNG is optional only when image delivery or preview is requested.
- **保留文本层压缩**: compress embedded screenshots before PDF rendering, not the whole PDF page, so report text remains sharp and copyable.

## Evidence Rules

Both versions are evidence-first:

- Do not invent video details, GMV, A3, search lift, spend, creator performance, conversion, or inaccessible-video observations.
- Separate `视频已验证`, `表格/平台信号`, and `待核验`.
- Do not call a video `质爆`, `量爆`, or `高转化` as fact without matching platform data.
- Do not force a fixed six-part timeline. Segment real content beats by function changes.
- Treat transcript, OCR, and platform tables as evidence sources with different confidence levels.

## Repository Layout

```text
short-video-breakdown-report/
├── SKILL.md                         # 1.0 skill entrypoint
├── README.md
├── agents/
├── assets/
├── docs/
│   └── 卖点黄金公式_20260707-20260713_食品饮料_梳理.md
├── references/
├── scripts/
└── short-video-breakdown-report-2-0/
    ├── SKILL.md                     # 2.0 skill entrypoint
    ├── agents/
    ├── assets/
    ├── references/
    │   ├── report-structure-1-0.md
    │   └── yuntu-single-video-framework.md
    └── scripts/
        ├── optimize_report_images.py
        ├── render_html_to_pdf.mjs
        └── ...
```

## Installation

Install 1.0:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/tmzbb7tjyb-sys/short-video-breakdown-report.git \
  ~/.codex/skills/short-video-breakdown-report
```

Install 2.0 from the same repository:

```bash
tmpdir="$(mktemp -d)"
git clone https://github.com/tmzbb7tjyb-sys/short-video-breakdown-report.git "$tmpdir/short-video-breakdown-report"
cp -R "$tmpdir/short-video-breakdown-report/short-video-breakdown-report-2-0" \
  ~/.codex/skills/short-video-breakdown-report-2-0
```

Then invoke 2.0 in Codex:

```text
Use $short-video-breakdown-report-2-0 to analyze this video and export a long-canvas PDF report.
```

## 1.0 Typical Workflow

1. Create a dedicated asset folder for the task.
2. Inspect video duration, resolution, codec, and file size.
3. Extract audio before final screenshot selection whenever possible.
4. Build an evidence-first frame plan from scene cuts, speech segment boundaries, keywords, BGM accents, action peaks, product reveals, reactions, subtitle changes, and CTA endings.
5. Extract planned frames and run OCR to correct subtitle/product-name transcription errors.
6. Run BGM/cut-point analysis.
7. Segment the video into real functional stages.
8. Select highlight screenshots by content function.
9. Generate fixed-layout HTML from `assets/fixed-report-template.html`.
10. Export the PNG long image and verify dimensions, image references, clipping, whitespace, and layout consistency.

## 2.0 Typical Workflow

1. Create a dedicated asset folder for the task.
2. Run the 1.0 evidence pass: video facts, transcript, OCR, frames, audio rhythm, screenshots, and real beat segmentation.
3. Add the 2.0 marketing layer:
   - content asset role
   - creator/TA fit
   - voice/timbre emotion
   - proof chain
   - viral and heat potential
   - search handoff
   - conversion handoff
   - reusable brief
4. Generate an internal HTML render source from `short-video-breakdown-report-2-0/assets/fixed-report-template.html`.
5. Export a single-page long-canvas PDF with `render_html_to_pdf.mjs`.
6. If size needs reduction, optimize embedded screenshots first and re-render PDF.
7. Verify page count, dimensions, image references, layout, file size, and text copyability.

## Script Usage

Plan frame timestamps:

```bash
scripts/plan_frame_times.py input.mp4 output/frame_plan.json \
  --segments output/transcript_segments.json
```

Extract frames:

```bash
swift scripts/extract_frames.swift input.mp4 output/frames "$(cat output/frame_plan_seconds.txt)"
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

Render a 1.0 PNG:

```bash
node scripts/render_html_to_png.mjs \
  output/<slug>_video_analysis_report_fixed.html \
  output/YYYYMMDD-<strongest-hook>-视频拆解.png \
  --width 1080
```

Render a 2.0 long-canvas PDF:

```bash
node short-video-breakdown-report-2-0/scripts/render_html_to_pdf.mjs \
  output/<slug>-视频框架拆解2.0.html \
  output/YYYYMMDD-<strongest-hook>-视频框架拆解2.0.pdf \
  --width 1080
```

Compress a 2.0 PDF while preserving copyable text:

```bash
python3 short-video-breakdown-report-2-0/scripts/optimize_report_images.py \
  output/<slug>-视频框架拆解2.0.html \
  output/<slug>-视频框架拆解2.0-optimized-source.html

node short-video-breakdown-report-2-0/scripts/render_html_to_pdf.mjs \
  output/<slug>-视频框架拆解2.0-optimized-source.html \
  output/YYYYMMDD-<strongest-hook>-视频框架拆解2.0-compressed.pdf \
  --width 1080
```

Do not compress by converting the whole PDF page into one JPEG/PNG and wrapping it back into PDF. That removes selectable text and makes zoomed text blurry.

## Dependencies

The workflow is optimized for macOS:

- Swift / AVFoundation for frame extraction
- Vision framework for OCR
- `avconvert` / `afconvert` for audio extraction and PCM conversion
- Python for frame planning, BGM energy accent detection, image optimization, and optional transcription helpers
- Chrome for HTML-to-PNG and HTML-to-PDF rendering
- optional `ffmpeg/ffprobe` for scene-change and audio-peak frame planning
- optional `faster-whisper` for local speech transcription

Set up the local Whisper environment:

```bash
cd ~/.codex/skills/short-video-breakdown-report
./scripts/setup_faster_whisper.sh .venv-whisper
```

## Notes

This repository contains reusable skills, report templates, references, and helper scripts only. It does not include analyzed videos, transcripts, screenshots, generated reports, or private project assets.
