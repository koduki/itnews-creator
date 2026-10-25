---
name: itnews-powerpoint-polish
description: Review and finish an existing Japanese Weekly IT News PowerPoint draft inside Copilot in PowerPoint. Preserve the author's topic-first narrative, repair layout, verify claims and citations, replace placeholders with authentic source screenshots or meaningful article photos when actually available, improve editable diagrams and speaker notes, and perform final slide-by-slide QA. Use after a base PPTX was created in Microsoft 365 Copilot Chat.
---

# IT News PowerPoint Polish — finish, do not reinvent

## Primary mission
Open the **existing .pptx created by Microsoft 365 Copilot Chat** and make it presentation-ready **inside Copilot in PowerPoint**. The user plans and researches in Copilot Chat; this skill owns the second phase: missing evidence, editing, visual quality, speaker notes and final assurance. The first phase uses `weekly-it-news`; this phase uses `itnews-powerpoint-polish`. Both are separate skills and neither is silently installed in the other host.

Do not restart news selection, silently discard the draft, regenerate all slides in a generic template or rewrite the author's opinions as established facts. When the user says polish/review/finish, operate on the deck currently open, unless they explicitly ask for a new one. Prioritize preserving content and news order over cosmetic redesign. Start with a copy/version if editing may be destructive, following host capabilities.

## Editorial invariants (non-negotiable)
- The pre-AI **2026-01-25 / 2026-04-12** examples define the intended editorial rhythm: **dated cover → short 今週のトピック → for each story an authored explanation followed by its source/photo/technical reference slides → next story**. Numbered chapters, summary slides and arbitrary corporate roadmaps are optional, not mandatory.
- The 2026-09-13 / 2026-10-12 decks are design refinements: borrow typography, editable diagrams, comparisons and legibility improvements, not a different storyline.
- Distinguish sourced facts, vendor statements, journalist analysis, presenter commentary and predictions. Never fabricate benchmarks, cited claims, authors, screenshots, images, or attribution.
- 16:9 white, `#C00000` red accents, charcoal text, readable Japanese sans. Keep diagrams, charts, tables and labels editable when their content is authored. Real source images remain images.
- Only use external images that are genuine, relevant, accurately attributed and permitted for the intended reuse. **A link or an AI-generated illustration is not documentary evidence.** Article photography and reporting graphics are as legitimate as official/vendor images when appropriate.

## Operating procedure: edit the PPTX in place
1. **Inspect, classify and preserve.** Read the current deck, its slides, speaker notes, visible sources and any supplied Chat transcript/brief. Identify news-group boundaries and current story order, slide roles, missing material, poorly aligned objects and source claims. Do not claim notes or external sources were inspected unless accessible. If the deck is a .docx rather than PPTX, stop: ask for a real editable deck or use a PowerPoint-native creation path with the user's agreement.
2. **Make a compact repair list.** Categorize each issue as **BLOCKER** (false claim, no required evidence, unreadable/corrupt slides), **IMPORTANT** (bad cropping/contrast, missing source, wrong arrows, noneditable authored graphic), or **POLISH** (spacing/typography). Say which work can be done in the current PowerPoint environment. Preserve a copy if destructive changes are anticipated.
3. **Finish documentary evidence.** For each news topic, locate or receive informative original press/reporter photos, actual article diagrams, official statements, real product UI or technical figures. Search and screenshot only if browsing/capture is genuinely available here; PowerPoint's ability to generate pictures is **not** proof of real screenshot capture. Prefer the original meaningful image over a tiny screenshot of an entire webpage when lawful and available. Embed genuine pixels, verify the image is actually on the slide, crop for context and add the publisher/creator, page URL and date to visible caption or notes. If real images are not accessible or reuse rights are unclear, do not replace them with fake evidence: leave a clearly identified gap and report it.
4. **Repair content and semantics.** Fact-check against accessible credible sources, or mark unverified; don't spontaneously invent new findings. Correct misleading comparison conditions, reversed diagram arrows, inconsistent units and screenshots lacking surrounding context. Add concise editorial/technical explanation only where it improves understanding. Preserve the speaker's own interpretation, labeling it as such. Prefer targeted improvements, not broad factual rewrites.
5. **Improve layout using PowerPoint-native editing.** Align objects, establish typography hierarchy, fix overflow, crop/reposition genuine images, standardize source treatment and use consistent red/white identity. For authored diagrams, tables and charts use editable native objects where supported; retain authentic external images as raster. Split a crowded explanation slide only if necessary; don't enforce one thought per evidence screenshot. Avoid filler illustration or gratuitous transitions/animations. For imported base decks created by simple PPTX scripts, treat native font/shape clean-up as normal work.
6. **Prepare to present.** In notes where supported, include what to say and what to point at, source and capture credits, and any unresolved uncertainty. Protect dates/topic titles and existing URLs. Optional appendix is acceptable for numerous sources, but do not force an end-of-deck corporate summary.
7. **Run final gate and save.** Reinspect every slide at presentation scale (render/slide sorter if available): no cut text, collision, blurred/stretching, inconsistent dimensions, accidental blank slides or irrelevant visuals. Verify images actually appear, links and captions are correct, and edits saved to a real `.pptx`. Report finished fixes, outstanding image/source gaps and checks not performed. If blocked, call the result **unfinished**, not complete.

## Clear division of responsibilities
| Microsoft 365 Copilot Chat (`weekly-it-news`) | PowerPoint (`itnews-powerpoint-polish`) |
| --- | --- |
| Conversational news discovery; decide topics and technical/editorial angle | Preserve order, claims and point of view, while improving audience comprehension |
| Verify news facts and make the **base PPTX**, even if some images cannot be obtained | Add missing authentic images when actually possible and permitted |
| Include real sources, captions/notes and explicit outstanding tasks | Correct crop, fidelity, citations, slide layout, editable diagrams and speaker notes |
| Label draft as **BASE / needs polish**, not 'complete' if required evidence is missing | Recheck all hard requirements and mark final status accurately |

A `.pptx` from Copilot Chat is a valid **base** even if its evidence images are missing; don't equate 'base deliverable created' with 'final requirements passed'. A missing screenshot or citation must be explicitly indicated in the handoff, not concealed. You do **not** require a sidecar JSON file: infer from deck/notes and accept user-provided chat history, links, photos and optional source manifest. See `references/handoff-contract.md`.

## Practical edit requests
- “この資料をレビューして、元のニュースの順番と論旨を維持したまま、全スライドのはみ出し・文字サイズ・画像配置を修正して。”
- “証拠画像不足のページを確認し、実際に入手・利用できる報道写真、公式画面、論文の図だけを追加。出典をノートに記録して。”
- “技術アーキテクチャの矢印・単位・比較表を正し、PowerPointで編集できる図形にして。変更前の意味を壊さないで。”
- “発表者ノートを補完して、最終チェックで残った問題を箇条書きにして。”

## References
- `references/handoff-contract.md`: how the chat-authored base deck communicates unfinished work without mandatory sidecar files.
- `references/review-rubric.md`: exact completion gates and priority labels.
- `references/visual-repair.md`: edit recipes for genuine evidence, visuals, readability and native objects.
- `templates/review-report.md`: optional concise user-facing end report and change log.

## Platform reality
Microsoft documents Copilot in PowerPoint editing and custom skills, but feature availability varies by tenant, version and permissions. Select the skill in PowerPoint's Copilot pane via **+ → Choose skills** or `@itnews-powerpoint-polish`; add it through **Manage skills → Add skill** if permitted. OneDrive folder name must match the `name` field of `SKILL.md`. Do not claim live screenshot capture, external-image downloading, edit access, speaker-note updates or slide rendering unless they actually worked. Inaccessible material must remain a documented limitation. Do not force the user to install Python, extra apps or external tools for normal PowerPoint polishing.