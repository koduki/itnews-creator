# Topic-contiguous storytelling & visual-evidence handoff (v0.7)

## The real regression behind this rule
A supplied **2026-10-25 v0.5 deck** has 22 slides and 4 embedded image objects. Its topics occur as Meta Muse (slides 3–5), PHP2Shell (6–9), GMO cloud desktop incident (10–13), then Meta Muse again (14–15), PHP2Shell again (16–17), GMO again (18–21). This round-robin structure is an **editorial defect** for Weekly IT News, even though the individual explanations and comparisons are useful. A supplied **2026-03-15 reference deck** contains 31 slides and 33 embedded image objects; its GTC preview sequences actual NVIDIA event pages, report photographs, product/spec visuals and tables. These numbers describe the provided examples, **not a mandatory image-per-slide target**. Neither proprietary example deck is redistributed.

## Non-negotiable sequence
- Start with dated cover and concise 今週のトピック. Select a natural number of topics, not a forced three.
- For **each** story, put its authored news explanation FIRST, then the important photo/source page/technical figure and relevant technical follow-up, **before** starting the next story. The evidence may be a full-page genuine capture with almost no additional prose. Commentary must stay distinguished from facts.
- **Never make a second tour of the stories** for 'deep dives', risk, market, or response. Fold those slides into the respective topic's single contiguous block. An optional cross-topic closing discussion is allowed ONLY when genuinely additive, not as a template requirement.
- A slide belongs to one topic unless it is genuinely cross-topic; don't label a comparison as 'summary' to hide a return to an already completed topic.
- Preserve real product/screenshot/news photos as full-size evidence where informative; avoid substituting every evidence slide with three-column cards and imagined conceptual diagrams.

## Base-PPTX evidence contract (Chat phase)
Before claiming BASE_READY, produce a per-topic list **on slide notes when supported, otherwise in an explicit handoff message or a compact '要画像' placeholder in the draft**. For each desired evidence asset, include: (a) the specific claim or question, (b) the page or image URL as actually verified (NEVER invent one; mark 未調査 if unknown), (c) publishing organization and photo/figure credit if known, (d) visual type: photo/article figure/announcement/UI/site capture, (e) priority and intended insertion **after which explanation slide**, (f) asset state **embedded / pending / unavailable / rights-unverified**, (g) its rights/attribution status and (h) what remains for PowerPoint. For an acquired picture, confirm the image object is embedded, not just linked.

A base .pptx can be delivered with `pending` evidence **if the missing item and its intended location are explicitly documented**. It must not be called a fully finished visual deck. A Word report is not a base PPTX. Do not force image-count quotas or use irrelevant stock imagery merely to increase the count. See `templates/editorial-storyboard.example.json` for a deliberately source-URL-free model, and the optional `scripts/check_editorial_flow.py` validator.

## QA questions
1. Do the topic blocks follow the agenda order exactly, without reopening a previously completed topic?
2. Does each news block begin with a factual explainer before source/evidence or technical interpretation?
3. Is there at least an evaluated evidence plan for each topic? If relevant authentic images cannot be acquired, is the reason recorded rather than hidden?
4. Are the sources precise enough for the PowerPoint-stage skill to fetch/insert assets *without restarting the news research*?
5. Are real images used because they explain the technology/event, not because a numerical quota demands them?