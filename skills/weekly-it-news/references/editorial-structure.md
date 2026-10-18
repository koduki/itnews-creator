# Canonical editorial structure — pre-AI Weekly IT News

## Authority and scope

The owner explicitly identifies **20260125.pptx** and **20260412.pptx** as the intended *composition and news-show structure*. Layout imperfections predate AI assistance and **are not** mandatory design targets. The 20260913/20261012 decks illustrate possible **subsequent** graphical improvements. Use this document over any conflicting structure preference in the later examples. The uploaded PPTX files themselves contain numerous third-party screenshots, so they are deliberately excluded from the public repo/plugin archive.

## Evidence from the two original decks

| Document | Pages | News items | Pattern |
| --- | ---: | ---: | --- |
| 2026-01-25 | 21 | 4 | Date cover p1 → short "今週のトピック" p2 → one explanation per news item interleaved with original external screenshots and deeper technical illustrations |
| 2026-04-12 | 27 | 3 | Date cover p1 → short "今週のトピック" p2 → explanation followed by a run of first-party or external documentation/screenshots for each item |

The counts are from the PPTX and are **not** an instruction to reach any particular slide count. Neither deck contains a PowerPoint-native chart or table object; several **image screenshots** depict charts, comparison tables or diagrams. Preserve their editorial utility while preferring an editable native reconstruction **only when it is faithful and the original visual is not itself the evidence**.

### 2026-01-25: page sequence

- p1: date-led Weekly IT News cover; p2: simple four-item agenda.
- p3: jQuery 4.0 update explained in the presenter's voice → pp4–5 official release page and social announcement as immediate corroborating original-material pages.
- p6: Qwen3-TTS announcement and an evaluative remark on naturalness / cloning misuse; a concise news item does not need artificially extended filler.
- p7: Claude Code / CUDA→ROCm commentary and caveats → pp8–9 original community report and GitHub PR → pp10–13 related Triton/programming-model diagrams and comparison table. **Source claim → outside evidence → explanatory technical context** is a valid extended topic chain.
- p14: NVIDIA/Groq/CUDA Tile overview with interpretation → pp15–21 screenshots and technical visuals supporting the hardware/software narrative.

### 2026-04-12: page sequence

- p1 date-led Weekly IT News cover; p2 three-item agenda.
- p3 RISC-V GitHub Actions news, provider/OSS relevance → pp4–8 server specs and industry-primary-material screenshots.
- p9 Amazon S3 Files news, operational tradeoffs → pp10–14 cited architecture and storage-type reference diagrams, including URLs on some slides.
- p15 Gemma 4 news and licensing significance → pp16–18 benchmark/spec comparison imagery → pp19–27 adjacent-model/product news and screenshots as context. These later pages illustrate topical association; a future skill must **make each connection explicit** rather than silently merging unrelated news into a topic.

## Inferred canonical grammar (prioritized)

1. **Weekly editorial curation:** select a manageable set of noteworthy IT stories (three or four are observed; never hardcode a count). The speaker's point of view determines relevance.
2. **Cover and agenda first:** date, "Weekly IT News！", a direct "今週のトピック" list of concise actual headlines. Avoid mandatory nested agenda/chapter/summary pages.
3. **One editorial news explainer as each topic's anchor:** news facts; what technically changed; why the history, competing approaches or ecosystem matter; a short, qualified reaction or question where warranted. A news explainer can be bullet-led and reasonably dense if understandable.
4. **Evidence sequence next:** show official sites, press releases, release notes, real software UI, GitHub PRs, talks, social posts, architecture graphics or authentic comparison tables **in context**. Two or more successive evidence-only slides can be useful; they need no new headline when the link to the anchor is apparent.
5. **Deeper dives on demand:** add history, tradeoffs, system internals, prior attempts, architecture or data visualization **only as necessary** to make the specific story understandable. Use author-drawn editable visuals where sourced truth permits.
6. **Move directly to the next news item** when done. Do not force recap, big thesis, 3-act executive storytelling, symmetrical section lengths or a uniform number of evidence slides.
7. **Editorial opinion is distinct from reported fact:** firsthand impressions and skepticism are valuable; identify them as presenter observation, analysis or hypothesis. This is not a corporate PR presentation.

## Layout renovation without structural drift

- Keep 16:9, mostly white, black text and red heading/accent family. A plain large red topic headline is a better default than later numbered cards/giant chapter covers.
- Slides that primarily reproduce *authentic* content should show an appropriately cropped original and enough source/publisher/URL context in the notes or small footer; relevance must be justified. Remove social-page advertisements/chrome when irrelevant without altering message.
- Improve margins, readable fonts, title line breaks, image scale and density; do **not** replace the overall rhythm with elaborate forced infographics.
- Use a graph only when the **specific numerical comparison matters**, data are comparable and calculations verified. Use a native diagram when flow/relationship requires it; don't indiscriminately convert evidentiary images to shapes.

## Default storyboard unit

```
NEWS ITEM: headline, publication date, 1–3 primary sources, why selected
  A. Authored news explanation: facts + technical context + speaker's qualified take
  B. Evidence slide (0..n): authentic source or screenshot; what to notice; URL/rights
  C. Technical/context slide (0..n): faithful diagram, exact table, data chart or related history
  D. Optional insight/caution: only if not already stated and worth another slide
NEXT NEWS ITEM
```

The distinction between A, B and C is about *function*, not a forced visual template. Slides B and C can alternate, and topic length is flexible.