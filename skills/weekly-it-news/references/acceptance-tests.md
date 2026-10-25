# Cross-host acceptance and Copilot regression tests

These are behavioral requirements, not claims that any particular M365 tenant or ChatGPT plan has browser, image-download, or PowerPoint-generation tools. Never count a prompt alone as passing a test.

## R1 — PPTX requested, Word delivered (known failure)
- **Input:** Create an actual Weekly IT News PowerPoint (.pptx) from sourced research.
- **Previously observed failure:** A coherent Word (.docx) report was generated rather than a slide deck.
- **Pass:** A verifiable PPTX file or genuine PowerPoint-native presentation exportable to PPTX exists and contains slides.
- **Fail:** Word, Markdown, PDF or merely slide-like content is represented as a completed PowerPoint. If the host cannot generate PPTX, report it as blocked; optional research prose is explicitly a draft.

## R2 — News article image accepted when informative
- **Input:** Show a news event, new device, UI, security incident or benchmark using a journalist's relevant photo or figure published inside a reputable news article.
- **Pass:** Consider the actual article image as a legitimate candidate, not just official photos. Verify relevance and provenance, article URL, publisher, original creator/credit, date, permitted reuse and amount. Use the specific image when it explains the subject; use a webpage screenshot if layout/quote is the evidence.
- **Fail:** Exclude an important photo solely because it comes from journalism; substitute a random stock/AI image; copy material without a lawful reuse basis.

## R3 — Requested authentic imagery actually inserted
- **Input:** News explainer followed by real sourced screenshot, photo, or technical evidence, as in the early-deck format.
- **Pass:** Confirm meaningful images/figures/photos are genuinely **embedded in PPTX slides**, with source/rights and purpose documented; their placement follows the parent topic.
- **Fail:** Only source links, written image descriptions, source citations or generated synthetic illustrations; no actual documentary images despite a request. Report inability honestly when tools or rights prevent acquisition.

## R4 — No irrelevant quota or unverified image claims
- **Input:** A news item has no lawful or meaningfully relevant visual.
- **Pass:** Use clear editable diagram, table or text; mark requested unavailable authentic photos as an unmet requirement, not invented success.
- **Fail:** Force an arbitrary photo quota with filler images; imply that an unvisited article was captured.

## Host-side smoke checklist
1. Verify output is a real .pptx (by MIME/container or PowerPoint editor, not only filename) and count slides.
2. Confirm slide sequence: dated cover → concise news agenda → each explanation → related source photos, article figures and screenshots.
3. Confirm no unexpected .docx substitution; host capability limits noted.
4. Inspect the embedded pictures, source page and credit; distinguish article image from article-page screenshot.
5. Check numeric source/chart precision, diagram arrows, layout readability, and native editability where intended.
6. Record pass/fail/unverified individually. Never claim a run passed if a required operation was not executed.

## R5 — Copilot Chat custom agent generates PPTX without PowerPoint app
- **Input:** In the Agent Builder custom agent, ask for a PPTX and require a downloadable file, not Word.
- **Pass:** Agent Builder Code Interpreter (or equivalent native creation) actually generates a valid PPTX **inside Copilot Chat**; when a bundled helper is used, the resulting PPTX contains editable text and verified images supplied as real local bytes.
- **Fail:** Claim that Code Interpreter is not available *solely* because the PowerPoint Agent is separate; send the user to PowerPoint app before checking Code Interpreter; return Word or make unverifiable image claims.
- **Environment distinction:** CI can validate the offline helper and package structure; **live Copilot Chat invocation still requires a separate tenant smoke test**.
## R5 — v0.5 topic recurrence (observed regression)
- Input: cover/agenda → Meta overview → PHP overview → GMO overview → Meta risk/market → PHP response → GMO detailed analysis.
- **Fail:** a completed topic reopens in a later section. **Pass:** all Meta follow-up slides reside with Meta, then PHP, then GMO. A genuinely cross-topic closing synthesis is optional. The bundled `scripts/check_editorial_flow.py` has executable positive/negative plan tests; actual Copilot runtime results still require host-side inspection.

## R6 — Actionable evidence handoff, not false quota
- The Oct 25 draft contains 4 embedded image objects (all conceptual), while the March 15 reference has 33, many source/report captures. Do not set a 33/31 quota.
- **Pass BASE:** each intended missing photo/news/article screenshot is tied to its exact verified URL or explicitly marked unknown, purpose, placement, attribution/rights and `pending` state; PPTX and original commentary are retained.
- **Pass FINAL:** essential authentic images are lawfully incorporated and legible, with honest QA status. **Fail:** `SOURCE: 提供調査レポート` alone used as an image retrieval link, or invented page URL, or a URL described as an embedded image.