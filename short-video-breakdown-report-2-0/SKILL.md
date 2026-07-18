---
name: short-video-breakdown-report-2-0
description: Analyze a single short-form or vertical video as a Douyin/Juliang Yuntu-style marketing content asset, combining the 1.0 evidence-first video breakdown workflow with creator fit, TA, selling-point proof chain, quantity/quality viral potential, heat/amplification value, search intent, conversion handoff, reusable content assets, and default long-canvas PDF export. Use when the user asks for 视频框架拆解2.0, 短视频拆解2.0, 单条视频内容资产诊断, 巨量云图内容分析, 星推搜直复盘, 达人内容复盘, 搜索承接, 加热建议, or wants to upgrade a 1.0 short-video report without modifying the original 1.0 skill.
---

# 视频框架拆解2.0

Use this skill to analyze one short video as a complete marketing content asset, not only as a creative clip. 2.0 keeps the 1.0 evidence-first video workflow and fixed report deliverables, then adds a Juliang Yuntu-style layer: `选人 -> 做内容 -> 爆文识别 -> 加热放大 -> 搜索承接 -> 转化承接 -> 复盘沉淀`.

This skill is independent from `短视频框架拆解1.0`. Do not edit or depend on the 1.0 folder at runtime. Use the copied scripts, assets, and references bundled in this 2.0 skill.

## Non-Negotiable 1.0 Preservation Rule

2.0 is **1.0 full evidence breakdown + marketing asset layer**. It is not a shortened, summarized, or strategy-only replacement for 1.0.

- Never compress, omit, or flatten the 1.0 analysis layer merely to make room for 2.0 modules.
- Preserve the 1.0 capability by default: hook diagnosis, transcript/OCR calibration, audio/voice calibration, high-signal screenshots, content-function timeline, action/visual proof, strengths, risks, and remake advice.
- 2.0 modules must be additive: `内容资产定位`, `星推搜直诊断`, `搜索承接`, `转化承接`, `加热建议`, and `可复用brief` are added after or around the evidence layer; they do not replace it.
- If the report becomes long, extend the long-canvas page height. Do not reduce screenshot count, merge real beats, remove calibration cards, or make the timeline coarser just to keep the report visually shorter.
- In batch mode, still produce each video's full 1.0 evidence layer. Do not apply a fixed "6 screenshots + short timeline" pattern across videos.
- If a prior 1.0 report or screenshot reference is supplied, use it as the evidence-detail floor: the 2.0 report should be at least as specific on hook, screenshots, calibration, and timeline, then add marketing diagnosis.

## Core Difference From 1.0

- 1.0 answers: what is the video's hook, rhythm, script, visual proof, timeline, and remake advice?
- 2.0 additionally answers: who does this content influence, what asset does it create, whether it is worth amplifying, what search/conversion path it should hand off to, and what can be reused in the next brief.
- 1.0 evidence rules still apply: do not force six beats, do not invent scenes or metrics, separate table/platform signals from video-verified findings, and verify exported long-canvas PDF reports.

## Default Output

When analyzing an actual video, default to a client-ready **single-page long-canvas PDF**:

- PDF long canvas rendered from `assets/fixed-report-template.html` through `scripts/render_html_to_pdf.mjs`
- transcript, OCR, frame plan, highlights, and audio/BGM artifacts when available

Generate HTML internally as a temporary or working source when needed, but do not present HTML as a default deliverable unless the user explicitly asks for it. Generate PNG only when the user asks for image delivery or preview.

When the user only asks to create a strategic diagnosis or planning note, a Markdown report is acceptable.

## Evidence Boundary

- Use video, transcript, subtitles, OCR, frames, audio rhythm, and visible page/table data as evidence.
- Treat unverified platform metrics such as A3, search, 泛进店, CTR, spend, or GMV as `待核验` unless the user supplies actual data.
- Do not call a video `质爆`, `量爆`, or `高转化` as fact without matching platform data. Use `质爆潜力`, `量爆信号`, or `搜索激发假设` when only creative evidence is available.
- If a linked video cannot be opened because of login walls, expired links, redirects, or missing media, state the access limitation and restrict conclusions to accessible text/table signals.

## Workflow

1. **Create the evidence workspace**
   - Make a task-local folder such as `video_analysis_assets/<slug>/`.
   - Keep the source video unchanged.
   - Save facts, transcript, OCR, frames, audio, and report outputs in that folder.

2. **Run the 1.0 evidence pass**
   - Inspect duration, resolution, codec, and file size.
   - Extract or transcribe audio before final screenshot selection whenever possible.
   - Build a frame plan with intro density, scene cuts, speech turns, voice/timbre shifts, subtitle changes, action peaks, product reveals, proof moments, sensory moments, CTA, and BGM accents.
   - Use `scripts/plan_frame_times.py`, `scripts/extract_frames.swift`, `scripts/ocr_subtitles.swift`, `scripts/analyze_audio_beats.py`, and `scripts/transcribe_faster_whisper.py` when available.
   - Segment the real content beats. Do not pad or compress to six segments.
   - Select as many calibration cards and screenshots as the video actually needs. A dense 25s e-commerce video may need 9-12 screenshots and 8-10 beats; a longer narrative may need more or a grouped-but-still-complete structure.
   - Preserve concrete 1.0 observations: exact hook wording, visible subtitles, spoken claims, product/package proof, hand/body/fluid/action moments, sensory descriptions, price/specification cues, CTA, and every major weakness.
   - Do not skip the 1.0 evidence layer because a 2.0 marketing layer will be added later.

3. **Add the 2.0 marketing asset layer**
   - Identify the content's job in the chain: `星` creator/TA match, `推` viral/amplification, `搜` search stimulation, `直` live/product handoff, `复盘` reusable asset.
   - Diagnose creator fit: TA overlap, persona credibility, vocal/emotional fit, content label, product/category fit, and risk.
   - Diagnose voice and timbre as content evidence: note whether the speaker sounds tired, urgent, intimate, excited, restrained, expert-like, nasal, hoarse, whispery, tearful, amused, or broadcast-like, and explain how that changes emotion, trust, TA filtering, and ad resistance.
   - Diagnose the proof chain: hook -> pain/scene -> product claim -> proof/sensory evidence -> search or conversion cue.
   - Diagnose viral potential:
     - `量爆信号`: stop-scrolling hook, visual impact, rhythm, share/comment trigger, entertainment or novelty.
     - `质爆信号`: clear target user, strong product relevance, believable proof, A3/seed-user potential, search/进店 reason.
   - Diagnose amplification value: whether paid heat would amplify useful people and intent, not just playback.
   - Diagnose search handoff: brand words, product words, function words, scene words, comparison words, and whether a 小蓝词/comment pin/search landing page should exist.
   - Diagnose conversion handoff: whether the content should connect to product page, live room, brand zone, lead form, local store, or follow-up content.

4. **Write the single-video diagnosis**
   - Start with one clear judgment: what asset this video creates and whether it is worth reuse/amplification.
   - Keep the full 1.0 hook diagnosis, not only its conclusion: language hook, visual/action hook, rhythm, proof gap, scores, and P0/P1 optimization. Then add `voice/timbre emotion`, `TA filter`, and `search/conversion promise`.
   - Add a compact `星推搜直复盘` card or table.
   - In the timeline, include real beats from the 1.0 pass. Include rows for content function, spoken point, visual action, proof, search cue, conversion cue, strength, risk, and optimization when relevant.
   - Use the 1.0 evidence detail as the minimum detail level. 2.0 should not turn concrete observations into generic labels such as "proof chain complete" without preserving the underlying evidence.
   - In dense tables, highlight only the key words or decisive clauses, not whole cells. Use `<strong class="key-blue">...</strong>` for search, handoff, actions, and strategy; use `<strong class="key-green">...</strong>` for strong fit, reusable assets, and positive signals; use `<strong class="key-dark">...</strong>` for neutral but important nouns. Keep emphasis sparse so the report stays clean.
   - Scores must explain penalties. A clever hook loses points if proof appears too late, the target user is unclear, search terms are absent, or conversion handoff is weak.

5. **Generate report deliverables**
   - Use `assets/fixed-report-template.html` as the base layout unless the user asks for a different layout.
   - Keep 1.0 section order, but add 2.0 modules inside the report: `内容资产定位`, `星推搜直诊断`, `搜索承接`, and `可复用brief`.
   - Export a single-page long-canvas PDF at 1080px-equivalent width unless the user asks otherwise.
   - Let the long-canvas PDF grow vertically when the evidence layer is dense. Long page height is preferred over losing 1.0 detail.
   - If the PDF is too large, compress only the embedded report images with `scripts/optimize_report_images.py`, then re-render the PDF. Do not rasterize the entire PDF page into one JPEG/PNG because that makes text blurry when zoomed and removes copyable text.
   - Keep HTML as an internal render source only; do not list it as a final output unless requested.
   - Verify local image paths before export, then verify PDF page count, PDF dimensions/preview, no horizontal overflow, no clipped text, no broken images, final file size when requested, and text extraction/copyability when compression was used.

## 2.0 Report Sections

Use this section order for a full client-ready report:

1. **Hero**: strongest hook as title, video facts, and one-line content asset judgment.
2. **内容资产定位**: marketing target, TA, creator fit, chain role, and evidence level.
3. **前三秒钩子诊断**: voice/timbre, language/persona/action/BGM hook plus TA filter and search/conversion promise.
4. **字幕、音频与画面校准**: keep the 1.0 calibration detail. Use as many cards as needed for distinct hook lines, claims, product proof, sensory descriptions, price/specification cues, scenarios, and CTAs.
5. **高光截图**: each screenshot must prove a content function. Screenshot count follows evidence needs, not a fixed compact quota; do not reduce high-signal action/proof frames to make room for 2.0.
6. **时间轴拆解**: real beats only, with 1.0 content function detail plus 2.0 marketing handoff.
7. **星推搜直诊断**: creator fit, viral signal, heat value, search handoff, conversion handoff.
8. **优化与复用brief**: next creator type, script skeleton, search words, CTA, and monitoring plan.

## Diagnostic Template

Read `references/yuntu-single-video-framework.md` when writing a detailed 2.0 diagnosis, report table, or planning brief.

## Quality Rules

- Do not overwrite or patch `/Users/tendays/.codex/skills/short-video-breakdown-report`.
- Do not present a creative hypothesis as measured business impact.
- Do not fabricate GMV, A3, spend, search lift, creator performance, or inaccessible video details.
- Do not use a fixed six-part timeline. Beat count follows real content functions.
- Do not reduce the 1.0 analysis layer when producing a 2.0 report. 2.0 must preserve or exceed 1.0 detail for hook, calibration, screenshots, timeline, strengths, risks, and optimization.
- Do not default batch reports to a compact pattern such as 6 screenshots or a shortened timeline. Batch mode changes throughput, not evidence standards.
- Do not collapse specific video evidence into generic marketing labels. For every 2.0 conclusion, keep the visible/spoken/audio evidence that supports it.
- Do not force a shorter PDF by deleting calibration cards, screenshots, timeline columns, or risk/optimization rows. Extend the long canvas instead.
- Do not flatten spoken delivery into plain copy. For口播 videos, explicitly analyze voice/timbre differences such as fatigue, urgency, crying edge, nasal tone, excitement, calm authority, dialect, speed, pause, breath, and volume; explain what emotion or trust shift they create.
- Do not leave dense table text visually flat. Bold and color only the most important words or clauses using the report template's emphasis classes; avoid highlighting more than 1-2 phrases per cell.
- Do not shrink PDF size by rendering the whole page as an image. Preserve selectable/vector text and optimize only local video screenshots or other embedded raster assets.
- Separate `视频已验证`, `表格/平台信号`, and `待核验`.
- Make recommendations actionable: creator choice, opening remake, proof shot, search word, CTA, heat decision, and monitoring metric.

## Bundled Resources

- `assets/fixed-report-template.html`: copied fixed-layout report template from 1.0.
- `references/report-structure-1-0.md`: copied 1.0 report anatomy and scoring reference.
- `references/yuntu-single-video-framework.md`: 2.0 marketing content asset framework and reusable templates.
- `scripts/`: copied 1.0 scripts for frame planning, frame extraction, OCR, audio beats, transcription, HTML-to-PNG rendering, plus 2.0 long-canvas PDF rendering.
