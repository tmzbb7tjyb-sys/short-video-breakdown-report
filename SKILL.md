---
name: short-video-breakdown-report
description: Analyze short-form or vertical videos into reusable content breakdown reports. Use when the user asks to dissect,拆解,复盘, analyze, summarize, score, or export a short video/Vlog/e-commerce/food/lifestyle clip, especially when they need hooks, spoken copy, subtitles, high-light screenshots, timeline structure, optimization advice, HTML reports, PNG long images, or PDF-ready assets from .mp4/.mov videos.
---

# Short Video Breakdown Report

Turn a video into an evidence-backed report that a creator, operator, or client can use to understand what works and how to remake it.

Do not rely on frames alone. Treat the video as combined **picture + speech + subtitles + timing + deliverable layout**.

## Default Workflow

1. **Create a task workspace**
   - Make a dedicated asset folder near the working files, for example `video_analysis_assets/<slug>/`.
   - Keep source video unchanged.

2. **Inspect video facts**
   - Capture duration, width, height, codec, and file size using `mdls`, `ffprobe`, or available platform tools.
   - Decide frame sampling interval from duration:
     - `<=90s`: full video every 5s, intro every 0.5s from 0-3s.
     - `90-240s`: full video every 10-15s, intro every 0.5s.
     - `>240s`: full video every 15-30s, plus targeted extra frames after transcript review.

3. **Extract evidence**
   - Use `scripts/extract_frames.swift` for screenshots when AVFoundation is available.
   - Extract audio with `avconvert` or any available ffmpeg/AV tool.
   - Transcribe audio with `scripts/transcribe_faster_whisper.py` if `faster-whisper` is installed; otherwise install it in a project-local venv if the user allows package installation or network use.
   - OCR sampled frames with `scripts/ocr_subtitles.swift` to correct Whisper errors in subtitles, product names, and on-screen hooks.

4. **Read the video before designing**
   - Build a working transcript from Whisper plus OCR.
   - Correct obvious mishears using on-screen subtitles and visual context. Examples: dialect, brand names, food names, relationship hooks.
   - Identify the actual core promise. It may be in speech rather than the image.

5. **Analyze**
   - Produce a 3-second hook diagnosis.
   - Segment the full video into content stages with timestamps.
   - Pick high-light screenshots by function, not just appearance.
   - Write optimization advice for editing, opening hook, picture, subtitles, BGM/sound, and remake structure.
   - See `references/report-structure.md` for the recommended report anatomy and scoring dimensions.

6. **Generate deliverables**
   - Default: HTML report with local image references.
   - Optional: PNG long image at requested width, using `scripts/render_html_to_png.mjs`.
   - Optional: single-page or paginated PDF. If exporting PDF, render it back to PNG and check for clipping, blank right/bottom space, broken images, and unreadable text.

## Output Conventions

- Save generated reports with descriptive names, for example `<slug>_video_analysis_report.html`.
- Save transcript artifacts:
  - `transcript.md`
  - `transcript_segments.json`
  - `ocr_*.json`
- Save screenshots under `highlights/` and name them with index, function, and time, for example `03_first_bite_16s.png`.
- For export images, use the user's requested width. If unspecified, use 1080px wide long PNG.

## Quality Rules

- Use the strongest content hook as the title, not a generic title such as "video analysis report".
- Do not include horizontal scroll containers in output intended for PNG/PDF export.
- Keep color systems simple and consistent: two or three tones are usually enough.
- Verify local image references before presenting HTML.
- Verify exported PNG dimensions with `sips` or PIL.
- For PDF, verify page count and page size with `pdfinfo`; render a preview with `pdftoppm` before final delivery.

## Bundled Scripts

- `scripts/extract_frames.swift <video> <out_dir> <seconds_csv>`: export PNG frames at exact timestamps.
- `scripts/ocr_subtitles.swift <frames_dir> <out_json>`: run Vision OCR on frame subtitles/product text.
- `scripts/transcribe_faster_whisper.py <audio> <out_dir> [--model small] [--prompt "..."]`: transcribe audio and write Markdown/JSON.
- `scripts/render_html_to_png.mjs <input.html> <output.png> [--width 1080]`: render a full-page HTML report to a long PNG.
- `scripts/setup_faster_whisper.sh [venv_dir]`: optional helper to create a local `faster-whisper` environment.

Read or patch scripts only when necessary. Prefer running them directly.
