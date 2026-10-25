# Slide quality gates

Run as a staged review, not a self-congratulatory checklist. Record pass, fail or unverified for every significant check.

## Gate 0 — Deliverable and capability acceptance (hard blockers)
- Default execution is the **Agent Builder custom agent in Microsoft 365 Copilot Chat**, using Code Interpreter / native file generation to produce PPTX; no mandatory Word, handoff JSON, QA CLI outside the chat or separate render service. PowerPoint Agent in Copilot Chat is the second option; the PowerPoint app is optional.
- A PowerPoint request requires a **real editable `.pptx`**. Verify filename, existence and slides. Word `.docx`, `/:w:/` SharePoint link, PDF and prose outlines do not count unless expressly authorized.
- Screenshot-required slides require authentic captured or uploaded source images **actually embedded** in the deck, with topic, URL, and relevance recorded. Search result text, thumbnails and generated illustrations are not real screenshots.
- Preflight the current Copilot Chat host for its **Create documents, charts, and code** capability, a PowerPoint generator or executable bundled `scripts/build_pptx.py`, browser screenshot facility, image embedding, and file inspection. When a mandatory capability is missing, report the requirement unmet, not success.
- Microsoft Agent Builder skills do not automatically inherit the dedicated PowerPoint Agent capabilities. A host handoff must be explicit.
- Mark deliverables incomplete if requested PPTX or essential screenshot evidence is missing, even when research is excellent.

## Gate A — Source and claims
- Each nontrivial technical/news claim has an actual supporting source. Distinguish established facts, vendor promises, rumors, forecasts and editorial analysis.
- Product/benchmark numbers are transcribed accurately, unit-checked and as-of-dated. Quotes preserve intended context. Potentially conflicting sources are reconciled or acknowledged.
- Avoid stale news presented as fresh. The date of a presentation is not the publication date of a source.
- All external visuals, including journalistic photographs, news-article diagrams and page captures, are attributed and assessed for permissible reuse; unknown rights cannot be treated as approval.

## Gate B0 — Faithfulness to the intended news format
- The deck contains a dated Weekly IT News cover and a concise agenda of the real selected topics, except when the user explicitly requests another format.
- Each selected news item has an authored explanation before its evidence sequence; adjacent screenshots/technical charts remain connected to that news item. It must be possible to trace every evidence slide to its anchor topic.
- Speaker analysis, skepticism and firsthand impressions remain clearly different from sourced claims.
- There is no forced three-topic limit, standalone thesis on every evidence slide, section-divider quota, mandatory end summary, or fixed length per news item.
- The new deck improves pre-AI legibility without replacing early-deck structure with later-deck layout conventions.

## Gate B — Choice of medium
- Each image/diagram/chart/table has a slide-specific informational purpose. Meaningful news photographs and article figures are legitimate; official provenance is not a requirement.
- Charts use comparable values; tables are chosen for exact numbers; arrows accurately indicate relationships; screenshots are authentic if framed as evidence.
- Decorative stock/photos, duplicate screenshots, and invented images masquerading as evidence are removed.

## Gate C — Visual design
- Keep 16:9, editorial white/red/charcoal scheme and consistent typographic hierarchy, without sacrificing contrast.
- No overlaps, clipped text, undersized captions, low-resolution stretched screenshots or overflowing shapes.
- Display labels, axes, legends and footnotes at readable size at the expected projection distance. Split overcrowded content rather than shrink indefinitely.
- Use native editable shapes/charts/tables wherever possible. Genuine external screenshots are inherently raster; do not claim editable text inside them.
- Consistent alignment, spacing, section styles and purposeful use of red.

## Gate D — Final render and functional checks
- If supported, render **every** slide and inspect output, with focused manual review of densest, most visual and most data-heavy pages. Detect overflow and crop mistakes; rework and render again.
- Inspect speaker notes/appendix for citations, source URLs, interpretation warnings and numeric calculation provenance.
- Open/view resulting presentation when the host supports it; verify PPTX not corrupted. Confirm the target file was actually produced and can be edited where expected.
- If platform tools do not support full rendering, screenshot, or verification, mark those checks *unverified* and describe the limitation in final handoff.

## Minimum delivered audit summary
- Slide count and verified output format (.pptx not .docx); style; number/types of charts, native diagrams/tables, authentic article photos/figures and screenshots actually embedded rather than merely linked.
- Claims verified vs unresolved; attribution log location.
- Editable elements and what remains raster.
- QA passed, QA failed and QA not executed due to tool limits.

## Rework loop
Revise only the slides that fail, not random restyling of the deck. Prioritize factual errors, provenance/rights issues and misleading charts before cosmetic issues. Stop when all important verifiable checks pass, or when a blocker is explicitly disclosed.