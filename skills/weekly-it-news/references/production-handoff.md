# Optional production handoff for cross-host recovery (FALLBACK only)

**Default:** stay inside the Agent Builder custom agent in Copilot Chat; do not write intermediate files simply because this reference exists. The brief below is useful only when a host switch, user review, or reproducible audit is actually necessary.

## Minimum human-readable handoff
- Intended output: actual `.pptx` and its target location, not Word.
- Edition date and approved news headlines.
- Story order: dated cover → agenda → each news explanation → authentic evidence slides.
- For each slide: heading, short content, parent news topic, source claim/citation, suitable visual and why it matters, notes/credits.
- For each image: actual article/asset URL, publisher, creator credit, rights/citation basis, source date, image category, availability and actual insertion status.
- Outstanding blocks: no available PPTX generator; screenshots inaccessible; rights uncertain; image not embedded; final deck not inspected.

Prefer a concise Markdown table or natural-language summary readable by a second Copilot agent; do not require it to parse JSON. `schemas/evidence-manifest.schema.json` and `examples/handoff/evidence-manifest.json` specify an **optional machine-readable audit** for the QA CLI, not a dependency for normal Copilot production.

## Important invariants
- Do not label the handoff "the PowerPoint".
- A claim can be verified via original technical documentation while its illustrative image comes from credited news reporting.
- `embedded: true` means *validated as present on an actual PPTX slide*, not merely planned.
- If `sha256` is supplied, compute it from the exact bytes of the embedded media, so independent QA can correlate the photograph with the slide.
- If no valid visual rights or source pixels are available, mark a missing requirement rather than invent a screenshot.