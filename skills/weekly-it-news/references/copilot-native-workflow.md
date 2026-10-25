# Copilot-native PowerPoint workflow (default)

The objective is an end-to-end PowerPoint authoring experience **within Microsoft Copilot**, preferably Copilot **inside PowerPoint**. This skill supplies editorial instructions, not a replacement PowerPoint renderer. A Word, PDF, HTML or outline response is not completed slide generation.

## 1. Choose the right host BEFORE authoring

1. **Preferred — Copilot in PowerPoint:** open/new `.pptx`, invoke `@weekly-it-news` from the PowerPoint Copilot skills menu, create and refine slides **in that same session**. This is the primary path and must not require a script, a JSON handoff file, or a second service.
2. **Alternative — dedicated PowerPoint Agent in Microsoft 365 Copilot Chat:** create the `.pptx` there; test whether the same custom skill is actually available. Do not assume Agent Builder skills carry over; if not, use the skill's authoring rules as instructions, including visual source requirements.
3. **Agent Builder custom agent:** it may help with research and storyboard planning, but skill installation alone does not provide PowerPoint creation, web-page capture or PowerPoint Agent delegation. If a PPTX creator is not actually available, disclose that and recommend opening PowerPoint; do **not** claim a Word document is success.

## 2. Native single-session workflow

1. Inspect actual capabilities: native PowerPoint creation/editing, permitted web research, image search, authentic page screenshot capture, image insertion, notes and final review.
2. Research topics and independently verify nontrivial factual claims. Select relevant official and journalistic photographs and article figures; evaluate permissible reuse. Prefer evidence-bearing visuals over decorative images.
3. Keep a compact **internal storyboard and evidence checklist** during the session; create no Word or JSON artifact unless the user requests one or a host switch becomes necessary.
4. Create slides in the original order: dated cover → short news agenda → news-explainer slide → useful genuine evidence images / editable technical diagrams → next news.
5. Use native PowerPoint text, charts, tables, shapes and speaker notes when available. Insert actual source photos/figures only when the source can be retrieved and reuse is lawful. If a real screenshot is mandatory and capture is unavailable, name the unmet requirement explicitly.
6. Inspect the final actual slide deck and report which output/media requirements were verified or could not be verified.

## 3. Handoff is a FALLBACK, not a dependency

Only when the current host cannot finish or the user deliberately switches apps, prepare the concise portable brief described in `production-handoff.md`. Retain slide order, evidence URLs, article/photo creator credits, selected media status and unverified items. Never assume another agent will read an unshared Word document or import a JSON file. The user may convey the brief directly in the PowerPoint Agent conversation.

## 4. Tests of success

- An actual, openable PPTX with the expected slide families exists.
- Meaningful photographs, article figures or page captures expressly requested are *embedded*, not only cited as URLs or described in prose.
- Each genuine photograph has a traceable publisher/creator and reuse basis; non-official visual sources are accepted when appropriate.
- Charts and authored diagrams remain editable to the extent supported.
- No invented proof, no hidden substitution of Word, no unverified 'screenshot captured' assertions.

## Official guidance
- https://support.microsoft.com/ja-jp/powerpoint/copilot/copilot-in-powerpoint-skills
- https://support.microsoft.com/ja-jp/powerpoint/copilot/create-a-new-presentation-with-copilot-in-powerpoint
- https://support.microsoft.com/ja-jp/office/365-copilot-app/get-started-with-word-excel-and-powerpoint-agents-in-microsoft-365-copilot