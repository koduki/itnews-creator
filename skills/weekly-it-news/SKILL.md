---
name: weekly-it-news
description: Create, update, or review Japanese technical-news PowerPoint presentations using evidence-backed diagrams, charts, tables, official screenshots, and a consistent white/red editorial style. Use for Weekly IT News and similarly research-heavy technical presentations.
---

# Weekly IT News — evidence-led presentation authoring

## Purpose
Produce and review technically rigorous, visually communicative Japanese presentations. Follow the **editorial grammar** derived from the owner's 2026-09-13 (53 slides) and 2026-10-12 (34 slides) reference decks; do not copy their images or reuse their unverified claims as current facts. Prefer the host application's native presentation creation/editing capabilities, not a new PPTX generator. Existing user-supplied decks and templates take precedence where available.

## Operating principles (mandatory)
1. **Research before slides.** Determine audience, date, topic, desired depth, speaking context, output format, and whether this is a new deck or an edit. Infer obvious defaults; do not block on nonessential questions. Confirm news dates, versions, specs, claims and quotations from sources, distinguishing confirmed facts, vendor claims, estimates and forecasts. Never assume that claims in the two sample decks remain true.
2. **Build a story.** Create a brief slide plan with one proposition per slide, supporting evidence, a proposed visual and source, and an intended takeaway. Use the sequence *news → significance → technical mechanism → comparison/trade-offs → implications → summary*. Adjust section count to actual content, rather than mechanically copying slides.
3. **Choose a visual for its meaning, never for decoration.** For each slide decide whether the best medium is text, native shapes/diagram, editable chart, table, authentic UI/event screenshot, licensed/quotable external image or none. Explain internally how the visual strengthens the claim. An attractive image with no explanatory value is rejected. Never fill whitespace with stock imagery.
4. **Use editable slide objects where practical.** Use native text, shapes, connectors, tables and charts for authored content. Preserve source screenshots as raster where authenticity is the point. Do not replace factual UI or product photos with AI-generated lookalikes. If the host has no required capability, fall back to a truthful simpler design and report the limitation; never pretend to have browsed, captured, embedded or rendered an image.
5. **Check every cited asset and statistic.** Prefer original announcements, documentation, papers, repositories, datasets and videos; record the source page/URL, title, publication or access date, and applicable attribution/permissions. A citation is not a license: evaluate usage rights and the necessity/amount of quoted material. Crop to the relevant area without changing the meaning; avoid reproducing entire third-party presentations or articles without permission.
6. **Validate before delivery.** Inspect every slide at presentation size (render if the host permits); verify source-to-claim agreement, chart mathematics and units, image provenance, text overflow, contrast, hierarchy, captions, and editable status. Revise failures. If rendering or source checking is unavailable, say which checks could not be performed; never imply a pass without evidence.

## Reference visual identity
- 16:9 widescreen; predominantly white background; editorial red `#C00000` for topic labels, section markers, emphasis, and comparison headers; charcoal near `#1E1E1E` / `#333333` for text; subtle light gray dividers/cards. Use secondary colors only to encode specific semantic categories.
- Japanese sans: prefer `Noto Sans JP` / `Noto Sans CJK JP`, with a portable sans fallback. Maintain a clear hierarchy. The references often contain dense 12–19 pt body text; **improve projector legibility** by reducing text or splitting slides rather than reproducing tiny type. Aim for ~20–28 pt for body text when presentation context permits; dense reference material may use smaller sizes if legible at target output.
- Reusable slide families: date-and-three-topics cover; current-topics agenda; section divider with red rule / large translucent number; evidence-led fact slide; two/three-column trade-off comparison; editable architecture/process diagram; actual keynote/product screenshot; comparison table; three-lane synthesis/roadmap.
- Keep original source images when the subject is an actual product, UI, event, document or demonstration. Do not turn each screenshot into a full-slide image if a more informative annotated/cropped layout is possible. Always label the significance.
- Use slide-specific informative titles, e.g. a conclusion or concrete technical question, not generic “Overview”. Preserve the references' technical depth but avoid overcrowding.

## Visual selection decision tree
- Quantitative **time series** → line chart; ranking/size comparisons → bar/dot chart; precise multi-attribute specification → table; linked components/data paths → architecture diagram; sequence/branch → flow/sequence diagram; physical form or visible UI state → authentic official photo or screenshot; original vendor statement or stage demo → appropriately cropped, attributed screenshot; conceptual relationships → native editable shapes; an executive conclusion may require **no image**.
- First verify that the material genuinely exists and is comparable. Never manufacture quantities, timelines, products, UI states, citations, graphs or screenshots; do not convert qualitative judgments into fake measurements. A chart without meaningful data is not an option.
- For each proposed visual assess **claim relevance**, **information gain**, **factual validity**, **provenance/permission**, and **readability** on 0 (fail), 1 (partial), 2 (strong). Prefer visuals scoring at least 8/10; **factual validity or provenance = 0 is a hard reject**. Numbers are a review heuristic, not proof. Use a verbal rationale, not a fabricated score, when evidence is incomplete. Improve or remove rejected visuals.
- If source data are fundamentally not comparable, choose explanatory shapes or a caveated table rather than implying quantitative comparability.

## Source, screenshot and chart rules
- Source research: prefer first-party announcements, official documentation and repository releases; secondary commentary for context and independent critique. Cross-check surprising assertions. Record event date separately from article date and deck date. Mark predictions explicitly.
- Web screenshots: only when the real visible state is materially important, and when capture/browsing is actually available. Include publication/screen date and source on slide or in notes; crop responsibly. Never treat an AI illustration as a genuine product UI, keynote slide, or website screenshot.
- Tables: appropriate for exact multi-attribute comparisons; consistently format values and units, show missing values as unknown rather than assuming zero, distinguish reported specs and inferred specs. Reduce the number of columns before shrinking text.
- Charts: use source numeric data with clear units, period, sample, axis baseline and methodology. Check accuracy and denominators, avoid misleading cropping/dual axes, distinguish measured vs projected, and cite the dataset. Prefer editable native charts.
- Diagrams: ensure meaningful node types and arrow directions; use legend where necessary; mark conceptual diagrams as '模式図'. Use native shapes/lines, not screenshots of arbitrary generated pictures.
- Never invent sources or claim source permissions were verified if the platform cannot inspect them. Flag unverifiable material and replace with defensible textual or native visual alternatives.

## Delivery workflow
1. **Intake and evidence ledger**: audience, date, topic list, input links/files, evidence status, unresolved gaps.
2. **Outline/storyboard**: headline proposition and one-line takeaway for each slide, visual type + justification, concrete data/source URL and provenance state. See `templates/slide-plan.md`.
3. **Construct with host-native presentation capabilities**: make PPTX editable when possible, preserve branding and prior layout if editing, and create the slide families above. Do not assert identical rendering across ChatGPT and Microsoft Copilot.
4. **QA pass and revisions**: perform the checks in `references/quality-gates.md`; inspect rendered slides where supported. Rework low-value visuals and overcrowded slides.
5. **Deliver**: final file or host-native presentation; short summary of slide count, key findings, source coverage, chosen diagrams/charts/screenshots, editability, and any limitations or unresolved checks. Include an attribution/evidence log as notes or a source appendix for nontrivial external claims/assets.

## Platform adaptation
Read `references/platform-compatibility.md` before instructing users how to install or claiming any particular host feature. This skill controls **how** to select/validate content, not hidden native tool availability. A separate PPTX engine is an optional last resort only if the host cannot create required editable output and the user agrees. Never require Python, an external MCP server, specific external sites, or an image generator for the core workflow.

## Additional reference files
- `references/style-from-samples.md`: actual layout observations and sample-slide map.
- `references/visual-evidence.md`: detailed asset-selection and evidence policy.
- `references/quality-gates.md`: acceptance checks and rework loop.
- `references/platform-compatibility.md`: installation and capability distinctions.
- `templates/slide-plan.md`: practical storyboard and provenance fields.