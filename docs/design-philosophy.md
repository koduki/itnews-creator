# Design philosophy — Weekly IT News authoring

This is a **content, evidence and editorial quality policy** for native slide tools, not a home-grown PowerPoint rendering engine. Its purpose is to make an AI-assisted weekly IT-news talk feel like its author's technical news show, while improving research accuracy, meaningful visual choices and readability.

## Origin and precedence

The early, pre-AI decks (**2026-01-25**, 21 slides; **2026-04-12**, 27 slides) represent the **canonical editorial structure**. Their uneven spacing or source screenshots with tiny text should **not** become a fidelity target. The later, AI-assisted decks (**2026-09-13**, 53 slides; **2026-10-12**, 34 slides) demonstrate optional visual structure and deeper technical comparisons. A well-designed result does **not** require a topic numbering system, chapter titles, fixed number of topics, lengthy executive summary, or rigid corporate deck narrative.

When instructions conflict: explicit user request > specific attached slide template > early-deck news sequence > later visual refinements > generic style guidelines.

## News is the unit of composition

Default order:

1. Dated cover / "Weekly IT News！".
2. Short "今週のトピック" list, with the real number of topics for that week.
3. **For each topic:** an authored news-explainer slide (what happened, technical background, why it matters, qualified editorial view), followed by zero or more *related evidence slides* showing official announcements, code/PR views, real products, stage presentations, architecture comparisons and specific figures. Then move to the next topic.
4. Cross-topic conclusions or deeper comparisons are **optional**, introduced only when they improve this week's story.

The explanation is the anchor; evidence slides need a **reason for inclusion**, not a separate one-line thesis. Do not blindly turn every source screenshot into prose or erase the presenter's individual point of view. Mark interpretation, prediction and firsthand impressions distinctly from documented facts.

## Visuals are evidence, not decoration

Choose medium by question: exact product specs → native table; time series or comparable numeric differences → editable chart; system relationships → editable architecture/sequence diagram; UI or actual product appearance → verified real screenshot/photo; documented launch or keynote moment → actual source image; editorial emphasis → often text alone. Do not fill every slide with a decorative image, or demand a chart where valid quantitative data do not exist.

The five acceptance dimensions are **relevance to claim, information gain, factual validity, provenance and permissible use, readability**. Review each on 0–2; 8/10 is a working preference, but a 0 for factual validity or provenance is a hard stop. Scores are heuristic and should never be treated as external verification.

Specific anti-patterns: fake stage/UI screenshots, invented benchmark values, promotional images implying a measured finding, unverifiable article fragments, low-resolution unreadable screenshots, and cherry-picked numerical comparisons with incompatible workloads. Reproduce real third-party content only when lawful and necessary; attribution is not by itself permission.

## Research and traceability

Prefer official product releases, documentation, papers, repository history or datasets for *what happened*. Use journalism and community interpretation for *why it might matter*. Record source URL, specific claim supported, original publication/event date, retrieval date if relevant, image permission/citation basis, and any limitation. News dates, slide dates and projected release dates are not interchangeable. Samples show **format**, not currently reliable product facts.

Native shapes/graphs are preferred for freshly authored representations because viewers may need to edit or question them. External source images stay genuine screenshots. A synthesized explanatory figure must be labeled as such; do not pass it off as a vendor diagram.

## Quality gates (not just a prompt)

1. **Editorial** — correct weekly order, topic-to-evidence grouping, authentic presenter commentary, no arbitrary fixed slide count.
2. **Evidence** — trace factual claims and numeric values to sources, check permissions and dates, clearly label uncertainty.
3. **Medium** — each illustration adds comprehension; native diagrams use valid arrow directions; charts show comparable units and methodologies.
4. **Design** — projectable, 16:9 white/red identity, no clipped text, overly small labels, wasted full-browser chrome or awkward alignment; split dense slides when needed.
5. **Final artifact** — render/open every slide when available; verify notes, sources, chart correctness and editability; disclose anything the host could not actually inspect.

Failures should trigger repair of the specific slides, not a total redesign or a fabricated "QA passed" label.

## Two-stage editorial workflow (v0.6.0)

The owner prefers **conversation-first creation, PowerPoint-native finishing** rather than asking a single assistant to do everything. The repository therefore has **two task-specialized skills**:

- **`weekly-it-news` in Microsoft 365 Copilot Chat**: explore candidate news conversationally, verify technical sources, preserve presenter interpretation, and produce an actual editable **base PPTX**. If documentary images or layout polish remain unresolved, deliver as a clearly labeled **BASE DRAFT**, with exact source URLs and what still needs completing. A base deck with disclosed gaps is acceptable in this intentionally two-stage workflow; it is not a finished, fully evidence-backed presentation.
- **`itnews-powerpoint-polish` in Copilot in PowerPoint**: edit that existing file, protect the original news-to-evidence order, insert authentic sourced images where capabilities and rights permit, repair cropping, typography, native diagrams, speaker notes and source credits, then perform final visual checks. This phase should not restart the research or transform a technical news show into a generic corporate slide deck.

The **PPTX itself** is the minimum handoff between separate Copilot environments. Slide notes and citations are preferred for traceability; a compact follow-up brief can supply missing links or image requests. Automatic sharing of an Agent Builder skill, its conversation history, or a user's browser capabilities into PowerPoint is **not assumed**. A Word file, fabricated screenshot or source URL without image pixels cannot substitute for the expected artifact.

In this design, a skill is an **editing policy**, not a replacement presentation engine. Each Microsoft host uses only features it actually exposes; a restricted host must disclose an unmet requirement rather than invent a tool result. The PowerPoint editing skill is packaged **separately** from the Chat authoring skill; both share the editorial philosophy rather than an automatically connected runtime.

## v0.7: field-test-driven topic order and evidence handoff

The real 2026-10-25 v0.5 output contained 22 slides and 4 embedded image objects. It explained three topics in sequence and then revisited the same three in a second thematic round. The 2026-03-15 presenter-made example contained 31 slides and 33 image objects, with actual NVIDIA event pages, news photography and technical graphics. These counts are **observations, not mandatory image quotas**; the desired difference is the **authentic source-led editorial flow**.

Copilot Chat must finish the story **one topic at a time**: an authored explanation, its evidence or named image gaps, its technical analysis, then the next story. It must not create a broad first pass across topics followed by second passes for risks, markets or implications. A genuinely useful single cross-topic ending is optional.

For each desired real-source visual, the base-PPTX stage must give PowerPoint a precise handoff: the evidence's purpose, verified URL when actually known, image publisher/creator credit, exact intended position, rights status and **embedded/pending/unavailable** state. A URL is not a picture; when a source has not been found, mark the gap and do not invent a link. A base .pptx with explicit pending images can be **BASE DRAFT**, but not final. The PowerPoint skill repairs any reopened topic blocks first, then improves actual images, diagram clarity, layout, notes and citation. Preserve the author's analysis and original news cadence, not decorative image quotas.

`check_editorial_flow.py` is a dependency-free *optional* storyboard validator. Its synthetic v0.5-style regression test rejects reopened topic blocks and incomplete image handoff fields; it does **not** by itself prove the Copilot editor obeys the skill in a Microsoft 365 tenant. See `references/story-continuity.md` and `references/topic-repair.md` in their respective skill trees.

## Cross-host architecture

Keep two task-specific portable skills (`skills/weekly-it-news/` and `skills/itnews-powerpoint-polish/`) plus their respective supporting references and templates. Let **ChatGPT Work** and **Microsoft 365 Copilot Chat / PowerPoint Copilot** use their own available presentation engines; a custom skill does not replace hidden native tools or guarantee an identical rendering. Screenshot capture and external browsing can differ significantly by account/tenant. Never claim unperformed external fetches or unavailable edits.

The build produces **three archives** from one checked-in source (without executing a native presentation generator):

- ChatGPT plugin archive: root `plugin.json`, `README.md`, and **both** skill folders.
- Microsoft Copilot Chat authoring skill archive: the `weekly-it-news` skill contents at ZIP root.
- Microsoft Copilot in PowerPoint finishing skill archive: the `itnews-powerpoint-polish` skill contents at ZIP root.

Neither package contains the source PPTX examples, their screenshots, or downloaded third-party art. Versioned tag and manifest version must match at release time.

## Distribution versus installation

CI should check metadata and missing skill references, create *reproducible* ZIPs, and attach the three packages to each push/PR run as GitHub Actions Artifacts. Tags such as `v0.7.0` also publish downloadable assets on GitHub Releases. Publishing a ZIP **does not auto-install** or synchronize the private ChatGPT plugin, and does not deploy a skill to a Microsoft 365 tenant. Those are separately authorized host actions.

### Intentional non-goals

- Rebuilding PowerPoint with a new rendering engine when a usable native host exists.
- Making every slide a polished consultancy-style "one claim per slide" card.
- Treating AI-made illustrations as photographic or screenshot evidence.
- Pixel-equivalence between ChatGPT and Microsoft Copilot.
- Shipping proprietary or third-party images publicly solely because they once appeared in a personal presentation.