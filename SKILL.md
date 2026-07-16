---
name: 短视频框架拆解1.0
description: Analyze short-form or vertical videos into reusable content breakdown reports. Use when the user asks to dissect,拆解,复盘, analyze, summarize, score, or export a short video/Vlog/e-commerce/food/lifestyle clip, especially when they need hooks, spoken copy, subtitles, high-light screenshots, timeline structure, optimization advice, HTML reports, PNG long images, or PDF-ready assets from .mp4/.mov videos.
---

# 短视频框架拆解1.0

Turn a video into an evidence-backed report that a creator, operator, or client can use to understand what works and how to remake it.

Do not rely on frames alone. Treat the video as combined **picture + speech + subtitles + timing + deliverable layout**.

## Default Workflow

1. **Create a task workspace**
   - Make a dedicated asset folder near the working files, for example `video_analysis_assets/<slug>/`.
   - Keep source video unchanged.

2. **Inspect video facts**
   - Capture duration, width, height, codec, and file size using `mdls`, `ffprobe`, or available platform tools.
   - Do not use evenly-spaced frames as the only evidence source. Even coverage is only the safety net; highlights usually appear at scene cuts, spoken turns, action peaks, subtitle changes, reaction frames, product reveals, or CTA endings.

3. **Build an evidence-first frame plan**
   - Extract or transcribe audio before final screenshot extraction whenever possible, because the strongest hook or high-light may be in speech rather than in the evenly-spaced visual sample.
   - Create a frame timestamp plan with `scripts/plan_frame_times.py` when `ffmpeg/ffprobe` is available:
     - dense intro coverage: every 0.5s from 0-3s
     - sparse full-video coverage by duration: `<=90s` every 5s, `90-240s` every 12s, `>240s` every 20s
     - visual scene-change candidates from ffmpeg scene detection
     - speech segment starts, ends, and midpoints from `transcript_segments.json`
     - keyword moments around hooks, reversals, product claims, sensory words, price/benefit proof, relationship conflict, surprises, and CTA language
     - action-impact moments around kinetic hooks and visual peaks: entering, opening, pulling, tearing, pouring, spraying, mist bursts, flipping, shaking, hitting, close body contact, strong reactions, or any gesture that creates stop-scrolling force
     - optional audio loudness peaks when ffmpeg audio filters are available
   - Save the generated plan as `frame_plan.json` and `frame_plan_seconds.txt`.
   - If the clip is action-heavy, especially in the first 0-8s, add a dense action pass at 0.25s-0.5s intervals around motion peaks. Generate an action contact sheet when useful so the strongest gestures are not missed.
   - If `plan_frame_times.py` is unavailable or ffmpeg is missing, manually make a two-pass list: baseline coverage first, then add targeted timestamps after transcript/OCR review and action review. Never stop at uniform sampling.
   - De-duplicate nearby timestamps, but keep the stronger candidate when two moments are close. Prefer a frame that has a clear function in the report over a merely pretty frame.

4. **Extract evidence**
   - Use `scripts/extract_frames.swift` for screenshots when AVFoundation is available, passing the timestamp CSV from the frame plan.
   - Extract audio with `avconvert` or any available ffmpeg/AV tool.
   - Transcribe audio with `scripts/transcribe_faster_whisper.py` if `faster-whisper` is installed; otherwise install it in a project-local venv if the user allows package installation or network use.
   - OCR planned frames with `scripts/ocr_subtitles.swift` to correct Whisper errors in subtitles, product names, and on-screen hooks.
   - After OCR, add a second-pass mini extraction if the first pass missed important on-screen text, a product reveal, a reaction peak, or a transition/twist mentioned in speech. Second-pass frames should be named and explained as targeted evidence, not mixed silently into the baseline set.
   - If strong physical actions are present, extract and name `action_frames/` or `action_highlights/` separately. Do not let clean static product frames replace stronger action-impact frames when the action is what creates the hook.

5. **Read the video before designing**
   - Build a working transcript from Whisper plus OCR.
   - Correct obvious mishears using on-screen subtitles and visual context. Examples: dialect, brand names, food names, relationship hooks.
   - Identify the actual core promise. It may be in speech rather than the image.
   - Mine the key hook before writing the report. Look beyond literal words: inspect speaker identity, role framing, voice/timbre changes, interview or dialogue posture, visual setting, subtitle labels, information gaps, reversals, and why the viewer should believe the claim. Do not flatten a distinctive hook into a generic category such as "discount", "product reveal", or "food close-up" if the execution has a sharper mechanism.
   - Mine action hooks as carefully as language hooks. Ask what motion makes the viewer stop: a person entering the scene, a hand opening/pulling/tearing, food being poured or mixed, liquid or mist bursting out, a body-contact moment, a sharp camera move, or a reaction that changes emotional temperature.

6. **Analyze**
   - Produce a 3-second hook diagnosis.
   - Explain the hook mechanism, not just the hook text. If a hook works because of a role cue, different voice, mock interview, internal-source framing, contrast between speakers, or "said by someone unexpected" device, call that out explicitly.
   - Explain action-impact mechanisms when present. Name the specific movement and why it works, for example "language filters the target user, while entering the dorm bed and pulling the curtain create physical immediacy".
   - Segment the full video into content stages with timestamps.
   - Do not force Transcript Calibration or Timeline Breakdown into a fixed number of blocks. Let the number of cards/columns follow the video's actual content beats, spoken turns, product claims, proof points, sensory moments, scene changes, and CTA structure.
   - Pick high-light screenshots by function, not just appearance. Use a priority order when applicable: action-impact frames first, hook/persona evidence second, product/proof frames third, conversion/CTA frames last. A clear package frame is not automatically better than a blurry but high-impact action peak.
   - If action impact is central to the video, include it in the timeline as its own row or field, separate from static visual evidence.
   - Use the frame plan reasons and OCR/transcript evidence to justify high-light picks. If a chosen screenshot came from uniform coverage only, verify manually that it is still the best evidence for that moment.
   - Write optimization advice for editing, opening hook, picture, subtitles, BGM/sound, and remake structure.
   - See `references/report-structure.md` for the recommended report anatomy and scoring dimensions.

7. **Generate deliverables**
   - Default: HTML report with local image references.
   - Optional: PNG long image at requested width, using `scripts/render_html_to_png.mjs`.
   - Optional: single-page or paginated PDF. If exporting PDF, render it back to PNG and check for clipping, blank right/bottom space, broken images, and unreadable text.

## Output Conventions

- Save generated reports with descriptive names, for example `<slug>_video_analysis_report.html`.
- Save transcript artifacts:
  - `transcript.md`
  - `transcript_segments.json`
  - `ocr_*.json`
- Save frame planning artifacts:
  - `frame_plan.json`
  - `frame_plan_seconds.txt`
- Save screenshots under `highlights/` and name them with index, function, and time, for example `03_first_bite_16s.png`.
- For export images, use the user's requested width. If unspecified, use 1080px wide long PNG.

## Quality Rules

- Use the strongest content hook as the title, not a generic title such as "video analysis report".
- Do not present evenly-spaced screenshots as "highlights" unless they survive the functional high-light selection pass.
- Every highlighted screenshot should answer: what content function does this frame prove?
- Do not include horizontal scroll containers in output intended for PNG/PDF export.
- Keep color systems simple and consistent: two or three tones are usually enough.
- Verify local image references before presenting HTML.
- Verify exported PNG dimensions with `sips` or PIL.
- For PDF, verify page count and page size with `pdfinfo`; render a preview with `pdftoppm` before final delivery.

## Bundled Scripts

- `scripts/plan_frame_times.py <video> <out_json> [--segments transcript_segments.json] [--max-frames 80]`: create a timestamp plan from baseline coverage plus scene cuts, speech segments, keywords, and audio peaks. Prints a seconds CSV for `extract_frames.swift`.
- `scripts/extract_frames.swift <video> <out_dir> <seconds_csv>`: export PNG frames at exact timestamps.
- `scripts/ocr_subtitles.swift <frames_dir> <out_json>`: run Vision OCR on frame subtitles/product text.
- `scripts/transcribe_faster_whisper.py <audio> <out_dir> [--model small] [--prompt "..."]`: transcribe audio and write Markdown/JSON.
- `scripts/render_html_to_png.mjs <input.html> <output.png> [--width 1080]`: render a full-page HTML report to a long PNG.
- `scripts/setup_faster_whisper.sh [venv_dir]`: optional helper to create a local `faster-whisper` environment.

Read or patch scripts only when necessary. Prefer running them directly.
