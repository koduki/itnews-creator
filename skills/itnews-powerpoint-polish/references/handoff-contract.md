# Chat → PowerPoint: lightweight two-stage handoff

## User journey
1. In Microsoft 365 Copilot Chat, use **weekly-it-news** to discuss news choices, context, primary sources and editorial opinions. Generate a **real editable base .pptx**.
2. Save/open that exact .pptx in PowerPoint. Invoke **itnews-powerpoint-polish** there. The deck itself is the handoff, not a Word report or mandatory JSON file.
3. The PowerPoint skill reviews the base slide-by-slide, keeps the story and technical substance, fills what the PowerPoint host actually can fill, and reports remaining blockers before calling it final.

## Minimum handoff for a useful base deck
- Dated title cover, agenda, topic explanations and one or more evidence/technical context slides as available.
- Exact source URLs, as-of dates and publisher/creator credits on slide or in speaker notes where supported.
- Explicit **base vs final** status and specific TODOs for unavailable evidence: e.g. `要画像：ソースURL／その画像で示したい事実／必要な利用条件`. A *visible* placeholder is allowed **only in a draft**, not in a final deck.
- Claims and vendor assertions separated from presenter opinion, interpretation and projection.
- Native editable text/shapes, so PowerPoint can repair layout. Preserve existing images rather than flattening the whole PPTX into slide-sized screenshots.

## Hand-off caveats
- A PowerPoint skill cannot automatically read another Copilot Chat conversation or custom Agent Builder skill. Never claim automatic conversation memory/shared skill execution. The `.pptx`, its notes, any user-shared news links and optionally a brief are the explicit handoff.
- If Chat cannot attach sources as notes, it can place small source captions or an optional sources slide; no need to change file type or force a Word handoff.
- If chat generated a *basic but genuine* PPTX while missing source screenshots, call it a **BASE draft**; users explicitly chose to make PowerPoint the finishing stage. Do not call the whole job completed yet.
- Existing picture in PPTX does not prove the source is genuine. Verify pixels and provenance before counting evidence as fulfilled.
- Don't require `evidence-manifest.json` or a fresh browser session just to begin polishing. Optional manifests help repeatability but do not control whether editing is possible.

## User prompt for the PowerPoint stage
`@itnews-powerpoint-polish このCopilot Chatで作った下書きPPTXを仕上げて。ニュースの順番・技術的主張・私の考察を保持し、スライド全体の可読性、図表の正確さ、画像の裁ち落とし、出典と発表者ノートをレビューして修正して。画像未取得の箇所は、取得可能で利用条件が確認できる実画像だけで補完し、無理なら残課題として報告して。`