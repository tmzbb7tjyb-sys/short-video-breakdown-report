---
name: 短视频框架拆解1.0
description: Analyze short-form or vertical videos and short-video performance/formula tables into reusable content breakdown reports with fixed PNG report layout, BGM beat/cut-point analysis, hooks, spoken copy, subtitles, high-light screenshots, timeline structure, optimization advice, HTML reports, PDF-ready assets, and cross-video selling-point grammar from .mp4/.mov videos or CSV/XLSX reference-video links. Use when the user asks to dissect,拆解,复盘, analyze, summarize, score, export, or generate a report for short videos/Vlogs/e-commerce/food/lifestyle clips or asks to study卖点公式/黄金公式/参考视频 tables.
---

# 短视频框架拆解1.0

Turn a video into an evidence-backed report that a creator, operator, or client can use to understand what works and how to remake it.

Do not rely on frames alone. Treat the video as combined **picture + speech + subtitles + timing + deliverable layout**.

When the input is a selling-point formula or performance table, treat it as **formula + keyword taxonomy + metrics + audience + reference links + accessible video evidence**. Do not flatten it into a generic keyword summary.

## Mandatory Layout Contract

- Default deliverable is a **1080px-wide PNG long image plus its source HTML**, not only an HTML report.
- If the user only asks to read a formula table, compare rows, or improve this skill, a structured Markdown/table summary is acceptable. Use the fixed PNG layout when the task includes analyzing one or more actual videos into a client-ready visual report.
- Always use `assets/fixed-report-template.html` as the base layout unless the user explicitly asks for a different layout. Do not invent a new visual structure by default.
- Preserve the fixed report anatomy:
  - newspaper-style 1240px `.page`
  - header with large H1, subtitle, meta tags, summary, and three right-side metric cards
  - `前三秒钩子诊断`
  - `字幕、音频与画面校准`
  - `高光截图`
  - `时间轴拆解`
- Keep the template's dense, table-based export style. The number of calibration cards, highlight figures, and timeline columns must change to match the video; the section order and overall layout stay fixed, not the item count.
- Fixed layout does **not** mean fixed 6-part analysis. Do not force the timeline into 6 columns, do not pad weak beats to reach 6, and do not merge real beats just to fit 6. Use the video's actual beats: very short clips may need 3-5 beats; longer剧情/带货 clips may need 7-10 beats; dense product proof videos may need more. If a template example shows 6 columns or 6 visual slots, treat it as placeholder only.
- When filling `[[TIMELINE_HEAD]]` and `[[TIMELINE_BODY]]`, rebuild the table from the real beat list every time. Add or remove `<th>`/`<td>` cells as needed instead of reusing a six-slot skeleton.
- Top metric cards should describe the actual structure, for example `7拍`, `8个内容拍点`, or `5个转化节点`; do not default to `6段` unless the video genuinely has six distinct beats.
- Save the HTML with a suffix such as `<slug>_video_analysis_report_fixed.html` or `<slug>_video_analysis_report_yesterday_style.html`.
- Render the PNG with `scripts/render_html_to_png.mjs` at 1080px wide. If the user asks for another width, use that width but keep the same template.

## Formula Table And Batch Learning Workflow

Use this workflow when the user provides a CSV/XLSX/Feishu export such as `卖点黄金公式`, `黄金公式`, `卖点公式`, `参考视频`, `CTR`, or `单素材平均消耗`.

1. **Read the table as structured data**
   - Detect the key columns: formula string, selling-point category keyword columns, spend/consumption, CTR/CVR when present, audience/persona, industry/category, and reference-video URLs.
   - Preserve row-level context. A formula row is not only a list of tags; it is a tested bundle of audience, claim modules, proof modules, and example materials.
   - Normalize numbers before comparing: strip commas from spend, strip `%` from rates, and keep the original displayed values in the summary.
   - Separate signal types:
     - high spend or high consumption means the material could scale or pass delivery filters, but it is not proof of creative quality by itself.
     - high CTR means the opening promise or curiosity trigger may be strong, but it is not proof of conversion quality.
     - formulas with high CTR but lower spend are useful for hook mining; formulas with high spend but moderate CTR are useful for scalable claim/proof patterns.
   - Do not claim causality from table metrics alone. Phrase findings as hypotheses unless video evidence or experiment metadata supports causality.

2. **Map formulas into content functions**
   - Translate each formula component into the job it plays in the video:
     - `痛点`: viewer problem, risk, embarrassment, unmet need, or friction.
     - `身份认同` / `人群`: who should self-identify and why the claim is meant for them.
     - `成分配方原料`: what makes the product technically believable.
     - `功效功能`: the promised outcome or relief.
     - `市场地位和权威背书`: trust shortcut, certification, ranking, expert, test, or institutional proof.
     - `品牌调性和故事`: history, origin story, national brand, old brand, founder, or emotional legitimacy.
     - `风味口味`: taste promise and appetite trigger.
     - `使用感受和服务体验`: texture, mouthfeel, convenience, aftertaste, service, or sensory proof.
     - `使用场景`: when/where the product enters life.
     - `原产地`: place-based trust, freshness, specialty, or scarcity.
     - `包装`: portability, freshness lock, gifting, single-serve, family pack, or visual recognizability.
     - `运输`: delivery speed, freshness guarantee, cold chain, free shipping, or service reassurance.
     - `工艺科技`: process, patent, extraction, fermentation, preservation, or production craft.
     - `产品代名词`: nickname, color name, category shorthand, iconic package, or memory anchor.
   - Identify the likely lead module for each row. The first formula component is often the opening hook, but verify against video evidence when available.
   - Identify the proof chain: hook -> product/ingredient -> proof/backing -> sensory or scene evidence -> conversion cue.
   - Look for missing links: a strong ingredient without a felt benefit, a strong pain point without proof, a strong taste promise without visible sensory evidence, or a strong authority claim without viewer relevance.

3. **Prioritize reference videos for learning**
   - Do not try to open every link first. Sample deliberately:
     - top spend rows for scalable delivery patterns.
     - top CTR rows for opening hooks and curiosity mechanisms.
     - rows that combine high spend and high CTR for best-practice candidates.
     - one or two low-CTR or low-spend contrast rows when useful.
     - at least one sample per major audience cluster if the table has audience fields.
   - For each sampled row, keep a small trace: row number, formula, spend, CTR, audience, chosen URL, access result, and what evidence was actually visible.

4. **Access reference links with evidence boundaries**
   - If a reference URL can be opened, analyze it like any other short video: transcript, OCR, frames, beat/cut points, hook, timeline, proof chain, and CTA.
   - If a platform returns a login wall, empty player, redirect, expired link, 403, or no `video`/media source, say so explicitly. Do not invent scenes, spoken copy, frames, brands, or claims from the link.
   - If only table keywords are accessible, limit the analysis to formula-level and keyword-level hypotheses.
   - When using browser automation for reference pages, prefer an isolated browser context/session for the task and avoid using or disturbing the user's active tabs.

5. **Synthesize cross-video selling-point grammar**
   - Produce a compact table or notes with:
     - formula archetype
     - audience
     - metric signal
     - likely hook type
     - proof mechanism
     - visual/sensory mechanism to look for
     - conversion risk or compliance risk
     - remake prompt/template
   - Compare component co-occurrence rather than only raw frequency. For example, `成分配方原料 + 痛点`, `成分配方原料 + 市场地位和权威背书`, or `功效功能 + 使用场景` mean different creative jobs.
   - Keep table-derived learnings separate from video-verified learnings. Mark them as `表格信号`, `视频已验证`, or `待视频验证`.

## Food, Beverage, And Health-Food Content Lens

Use this domain lens for food/drink/snack/nutrition/health-food tables or videos.

- **Taste and appetite**: identify flavor words, first-bite moments, chewing/pouring/cracking/sizzling sounds, texture close-ups, and whether the video makes the viewer feel taste rather than only read taste.
- **Ingredient and formula trust**: connect ingredient names to a viewer-understandable benefit. Avoid leaving the analysis at "has VC/Omega-3/GABA/probiotics"; ask what problem the ingredient resolves in the video.
- **Pain point and audience fit**: distinguish children, moms, office workers, older adults, small-town middle-aged users, silver-haired users, Gen Z, and new white-collar users. The same ingredient should be framed differently for different groups.
- **Authority and compliance**: treat certifications, rankings, expert names, blue-hat marks, tests, old-brand history, and institutions as proof cues. Do not upgrade them into medical certainty. Flag unsupported or risky medical-style claims.
- **Scenario entry**: name the life scene that makes the product necessary now: breakfast, after meal, overtime, late night, hot pot, travel, gifting, fitness, sleep, family care, children's nutrition, or elder care.
- **Origin, packaging, and delivery**: for fresh food, snacks, and local specialties, analyze origin and shipping as part of the promise. `顺丰`, `包邮`, cold-chain, independent packs, sealing, and small packs often reduce purchase anxiety rather than merely describe logistics.
- **Nickname and memory hook**: product代名词 such as color bottles, "小粉", "小绿瓶", "液体黄金", or package nicknames should be analyzed as memory anchors and CTA shorthand.
- **Sensory proof gap**: if a formula contains `风味口味` or `使用感受和服务体验`, the video should ideally show/produce sensory evidence. Penalize reports where taste, texture, or convenience is only asserted in subtitles.

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
   - For any video with an audio track, extract or convert audio to PCM WAV and run BGM beat/cut-point analysis:
     - Example: `avconvert --source input.mp4 --preset PresetAppleM4A --output audio.m4a --replace --disableMetadataFilter`
     - Example: `afconvert -f WAVE -d LEI16 audio.m4a audio.wav`
     - Run `scripts/analyze_audio_beats.py audio.wav audio_beat_candidates.json`.
     - Compare beat candidates against visual cut points, object changes, action peaks, subtitle changes, product reveals, and reaction frames. Treat the result as rhythm evidence, not perfect music transcription.
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
   - Mine BGM rhythm hooks as carefully as language and action hooks. Ask whether cuts, object swaps, subtitle pops, zooms, gestures, reveals, or reactions land on BGM accents. If the video is visibly edited to music, name the mechanism explicitly, for example "BGM重拍像切换按钮，每一拍换一只盘子".

6. **Analyze**
   - Produce a 3-second hook diagnosis.
   - Explain the hook mechanism, not just the hook text. If a hook works because of a role cue, different voice, mock interview, internal-source framing, contrast between speakers, or "said by someone unexpected" device, call that out explicitly.
   - Explain action-impact mechanisms when present. Name the specific movement and why it works, for example "language filters the target user, while entering the dorm bed and pulling the curtain create physical immediacy".
   - Explain BGM/cut-point mechanisms when present. Include the strongest beat-aligned moments in the diagnosis, calibration cards, highlight captions, or timeline. If the clip is cut to music, do not reduce the mechanism to "fast pacing"; call it "BGM卡点", "重拍切换", "节拍推进", or equivalent.
   - Segment the full video into content stages with timestamps.
   - Do not force Transcript Calibration or Timeline Breakdown into a fixed number of blocks. Let the number of cards/columns follow the video's actual content beats, spoken turns, product claims, proof points, sensory moments, scene changes, and CTA structure.
   - Before writing the final timeline, name the real beat count in plain language and sanity-check it against the evidence. If the answer is "six" only because the template, a previous report, or the screenshot grid has six visual slots, revise it. Split only when the content function changes; merge only when adjacent moments perform the same function.
   - Calibrate scores against execution gaps, not just idea quality. A strong hook mechanism should still lose points if the proof chain is weak, the price or CTA is unclear, the claim is only subjective, key evidence appears too late, or the visual action distracts from the product promise. Scores should explain what was penalized.
   - Pick high-light screenshots by function, not just appearance. Use a priority order when applicable: action-impact frames first, hook/persona evidence second, product/proof frames third, conversion/CTA frames last. A clear package frame is not automatically better than a blurry but high-impact action peak.
   - If action impact is central to the video, include it in the timeline as its own row or field, separate from static visual evidence.
   - Use the frame plan reasons and OCR/transcript evidence to justify high-light picks. If a chosen screenshot came from uniform coverage only, verify manually that it is still the best evidence for that moment.
   - Write optimization advice for editing, opening hook, picture, subtitles, BGM/sound, and remake structure.
   - See `references/report-structure.md` for the recommended report anatomy and scoring dimensions.

7. **Generate deliverables**
   - Default: fixed-layout HTML report using `assets/fixed-report-template.html` with local image references.
   - Default: PNG long image at 1080px wide, using `scripts/render_html_to_png.mjs`.
   - Optional: single-page or paginated PDF. If exporting PDF, render it back to PNG and check for clipping, blank right/bottom space, broken images, and unreadable text.

## Output Conventions

- Save generated reports with descriptive names, for example `<slug>_video_analysis_report.html`.
- Save exported PNG long images with a date prefix in `YYYYMMDD-` format, for example `20260716-<strongest-hook>-视频拆解.png`. Use the current local date unless the user specifies another date.
- Save transcript artifacts:
  - `transcript.md`
  - `transcript_segments.json`
  - `ocr_*.json`
- Save frame planning artifacts:
  - `frame_plan.json`
  - `frame_plan_seconds.txt`
- Save audio rhythm artifacts when audio exists:
  - `audio.m4a` or equivalent extracted audio
  - `audio.wav` when used for beat analysis
  - `audio_beat_candidates.json`
- Save screenshots under `highlights/` and name them with index, function, and time, for example `03_first_bite_16s.png`.
- For export images, use the user's requested width. If unspecified, use 1080px wide long PNG.

## Quality Rules

- Use the strongest content hook as the title, not a generic title such as "video analysis report".
- Do not present evenly-spaced screenshots as "highlights" unless they survive the functional high-light selection pass.
- Every highlighted screenshot should answer: what content function does this frame prove?
- Do not include horizontal scroll containers in output intended for PNG/PDF export.
- Do not change the fixed report layout unless the user explicitly asks for a different layout. Content may vary; the section order and export style should not.
- Do not treat fixed report layout as a fixed six-step framework. The timeline column count and metric labels must reflect the actual video structure; the report should never be padded, truncated, or renamed to match six template slots.
- Keep color systems simple and consistent: two or three tones are usually enough.
- Verify local image references before presenting HTML.
- Verify exported PNG dimensions with `sips` or PIL.
- Visually inspect or screenshot-check the exported PNG before final delivery. Reject outputs with broken images, obvious blank space, clipped text, hidden horizontal overflow, or a layout that does not match the fixed template.
- For PDF, verify page count and page size with `pdfinfo`; render a preview with `pdftoppm` before final delivery.

## Bundled Scripts

- `scripts/plan_frame_times.py <video> <out_json> [--segments transcript_segments.json] [--max-frames 80]`: create a timestamp plan from baseline coverage plus scene cuts, speech segments, keywords, and audio peaks. Prints a seconds CSV for `extract_frames.swift`.
- `scripts/extract_frames.swift <video> <out_dir> <seconds_csv>`: export PNG frames at exact timestamps.
- `scripts/ocr_subtitles.swift <frames_dir> <out_json>`: run Vision OCR on frame subtitles/product text.
- `scripts/analyze_audio_beats.py <audio.wav> <out_json> [--window-ms 50]`: detect lightweight RMS energy accents for BGM/cut-point analysis. Use after converting extracted audio to 16-bit PCM WAV.
- `scripts/transcribe_faster_whisper.py <audio> <out_dir> [--model small] [--prompt "..."]`: transcribe audio and write Markdown/JSON.
- `scripts/render_html_to_png.mjs <input.html> <output.png> [--width 1080]`: render a full-page HTML report to a long PNG.
- `scripts/setup_faster_whisper.sh [venv_dir]`: optional helper to create a local `faster-whisper` environment.

Read or patch scripts only when necessary. Prefer running them directly.
