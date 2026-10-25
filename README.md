# itnews-creator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Evidence-first IT news PowerPoint skill for ChatGPT Work and Microsoft 365 Copilot, with meaningful diagrams, authentic press and news-article imagery, strict PPTX output and slide QA.

A portable, evidence-led Japanese PowerPoint authoring skill, based on four user-supplied **Weekly IT News！** decks, with **2026-01-25 and 2026-04-12 as structural originals** and **2026-09-13 and 2026-10-12 as later optional visual refinements**.

The skill is not a new PowerPoint engine. It tells the available native ChatGPT / Microsoft 365 Copilot presentation tools **what to research, how to choose meaningful visuals, and what to validate**. Its core is shared across both hosts.

## What it does
- Preserves the original weekly format: **dated cover → short 今週のトピック → news explanation → authentic source screenshots/technical context → next news**. Later chapter dividers and summary slides are optional.
- Selects editable shape diagrams, numeric charts, tables, authentic official/event screenshots, **relevant credited photos and figures from news articles**, or no image as appropriate. Images are judged by information value, not whether they came from an official page.
- Rejects decorative filler, unverifiable claims, misleading comparisons and manufactured screenshots. Distinguishes an image within a news story from a screenshot of the whole webpage, with publisher/photographer credit and lawful reuse requirements.
- Uses a style family derived from the examples: 16:9, white, `#C00000` red, charcoal Japanese sans, simple agenda headlines, source-backed technical news explanations; optional numbered cards, chapter dividers and comparisons.
- Enforces a two-part review: source/rights validation plus slide-rendering/design QA when tools are available.

## Why the skill is designed this way

The four supplied PPTX examples represent **two different purposes**, not four equally authoritative templates. The January/April pre-AI decks express the author's intended *editorial form*: a dated cover, a short agenda, then **news explanation → multiple real-source slides → next news**, with technical context and presenter commentary. Their uneven layout is **not** a design requirement. The September/October AI-era decks offer optional technical diagrams, side-by-side comparisons and stronger visual organization; they must **not** displace that underlying news-first cadence.

Research and visuals have an **evidence role**: each table, chart, drawing, real screenshot or retrieved image must clarify a specific claim or technical mechanism. Native editable visuals are preferred for original explanation, whereas screenshots preserve the authentic state of external sources. Reject impressive-looking but irrelevant art, invented UI shots, numeric comparisons without compatible data, and unattributed or impermissibly reused content. "No image" is a valid decision. Confirm source accuracy and rights separately from the final layout review; do not report checks that the host cannot perform.

**Cross-host strategy:** one shared `SKILL.md` specifies storytelling, research, media choice and quality gates; ChatGPT Work and Microsoft 365 Copilot use their own **native** presentation engines subject to host-specific capabilities. We do not implement a separate PPTX generation engine or claim pixel-identical output. This is not a custom override of either product's built-in PowerPoint skill.

For the full reasoning, including slide archetypes, validation criteria, rights and deliberate non-goals, see **[Design philosophy](docs/design-philosophy.md)**. For the original-deck page references, see [Editorial structure](skills/weekly-it-news/references/editorial-structure.md).

## Copilot-native authoring (preferred)

**The regular workflow completes in Copilot in PowerPoint.** Open a new or existing .pptx, select `weekly-it-news` in the PowerPoint Copilot skills menu, and conduct slide planning, content creation, evidence insertion and revisions there. A dedicated PowerPoint Agent can generate presentations in Copilot Chat, but an Agent Builder custom skill is not automatically installed inside it.

The skill does **not** require a separate PPTX generator, Word intermediary, Python script or JSON handoff file for normal creation. Optional [Copilot-native workflow](skills/weekly-it-news/references/copilot-native-workflow.md) instructions explain when host-native features suffice and how to report genuine limitations.

Only when switching hosts or requesting a reproducible audit, use the [optional production handoff](skills/weekly-it-news/references/production-handoff.md) and [evidence manifest schema](schemas/evidence-manifest.schema.json). A [structural PPTX QA script](scripts/qa_pptx.py) can optionally inspect an already-generated PowerPoint; it is **not** part of the generation path and cannot judge visual legibility, photo rights or factual correctness.

Local optional QA: `python scripts/qa_pptx.py output.pptx --min-images 1 --manifest evidence.json` (only if genuine images were requested and the optional manifest is available).

## Documentary visuals and hard output contract

The reference decks put important **real-source visuals after each news explanation**. These need not be limited to manufacturer announcements. Reputable news reporting may contain a better photo of a device in use, on-site event/incident photograph, technical diagram, annotated comparison, or evidence-bearing figure. The skill evaluates these sources by **relevance, factual fidelity, publisher/photographer provenance, permitted reuse, crop and on-slide readability**. When the image itself is important, prefer the actual credited image over a tiny screenshot of the whole article; when the article's wording or page context is the subject, capture the relevant part of the real page. Neither a URL nor an AI-generated illustration is documentary evidence.

**A request for PowerPoint must result in an actual .pptx (or PowerPoint-native deck verifiably exportable to .pptx).** The previous Copilot Chat experiment generated a Word document without the requested screenshots. That is a failed deliverable, not an acceptable alternative: the skill now checks the file format and whether authentic images were truly embedded. Agent Builder custom skills cannot grant unavailable browser or presentation capabilities. If the host cannot produce the requested result, it should disclose this rather than calling Word “done.” See [Copilot runtime diagnosis](skills/weekly-it-news/references/copilot-runtime-diagnostics.md) and [cross-host acceptance tests](skills/weekly-it-news/references/acceptance-tests.md).

## Build, CI and distribution

Two packages are **built automatically from exactly the same skill source**:

- **ChatGPT:** `itnews-creator-chatgpt-plugin-vX.Y.Z.zip`, with `plugin.json` and `skills/weekly-it-news/SKILL.md`.
- **Microsoft 365 Copilot:** `itnews-creator-copilot-skill-vX.Y.Z.zip`, with `SKILL.md` at ZIP root.

GitHub Actions workflow [`.github/workflows/package.yml`](.github/workflows/package.yml) runs on **pull requests**, **pushes to `main`**, and manual dispatch. It runs validation and packaging tests, creates both ZIPs, writes `SHA256SUMS`, and saves them as **GitHub Actions Artifacts (30-day retention)**. On a push of a `vX.Y.Z` tag it additionally publishes the same ZIPs and checksums as **GitHub Release assets**, requiring the tag to match `plugin.json`'s `version`. A release run for a mismatched tag fails rather than publishing misversioned archives. The build uses Python's standard library and fixed ZIP member metadata for reproducibility.

To build and verify locally:

```bash
python tests/test_package.py
python -m unittest discover -s tests -p 'test_build_packages.py' -v
python scripts/build_packages.py --out-dir dist
# For a tagged release: python scripts/build_packages.py --out-dir dist --tag v0.3.0
```

To retrieve an ordinary build, open **[Actions → Build skill packages](https://github.com/koduki/itnews-creator/actions/workflows/package.yml)**, choose a successful run, and download `itnews-creator-packages-<run ID>` under Artifacts. For durable, versioned downloads, use **[Releases](https://github.com/koduki/itnews-creator/releases)** after pushing the corresponding tag.

**Building and publishing archives is not installation or deployment.** It does not automatically update the existing private ChatGPT plugin, nor upload a skill into a Microsoft 365 tenant; those are separate host-specific steps.

## Repository layout

```text
plugin.json                           # ChatGPT plugin manifest
skills/weekly-it-news/SKILL.md        # Portable core instructions
skills/weekly-it-news/references/     # Design, visual rights, QA, platform nuances
skills/weekly-it-news/templates/      # Slide storyboard
scripts/build_packages.py            # Reproducible dual ZIP builder
tests/                             # Skill and distribution tests
.github/workflows/package.yml      # Build + Artifacts + tag Release
docs/design-philosophy.md          # Editorial and validation rationale
README.md
```

## Copilot Chat runtime requirements and observed failure

The initial Agent Builder field test produced a **Word** SharePoint document rather than the requested **PowerPoint .pptx**, with no genuine Web-page screenshots. This is a failed acceptance test, not evidence that the skill can autonomously create slides in every Copilot host. The actual Word document was not accessible for content inspection, so the precise tool-selection cause is unconfirmed.

**New in v0.3.0:** the portable skill performs a capability preflight before drafting. A PowerPoint request is **complete only** with an actual `.pptx`; `.docx`, PDF, presentation plans and Word SharePoint `/:w:/` links are intermediate at most. If the current agent cannot create a PPTX, it must say so and direct the user to **Copilot in PowerPoint** (skill applied in that host) or the **dedicated PowerPoint Agent** (with research handoff; not automatic skill sharing).

Authentic screenshot-backed slides require images captured from real pages or provided as actual files, embedded and attributed. Web search is not screenshot capture. If required screenshots cannot be sourced, the deck remains **incomplete**, and the agent must report that blocker rather than silently omit them.

See the [Copilot runtime diagnostic and remediation guide](skills/weekly-it-news/references/copilot-runtime-diagnostics.md) for the capability matrix, recommended host choice and explicit output/screenshot validation checklist.

## Installation

### ChatGPT
Install the plugin archive generated from this repository when plugin installation is available in your workspace. The portable skill is `skills/weekly-it-news/SKILL.md`. Availability in ChatGPT / Work depends on account settings and enabled tools. Ask for a presentation *using the weekly-it-news skill* and attach a template if exact styling is desired.

### Microsoft 365 Copilot Chat Agent Builder
For organizations eligible for custom skills (Frontier preview as documented Sep 2026): zip the **contents** of `skills/weekly-it-news/` with `SKILL.md` at the archive root, then upload to Agent Builder → Configure → Skills. Don't use the root ChatGPT plugin ZIP for Agent Builder.

### Copilot in PowerPoint
Add `skills/weekly-it-news/SKILL.md` and its support folder through PowerPoint Copilot's custom skill workflow or personal OneDrive Skills folder, depending on the UI available to you. You can @mention the skill. Use native Brand Kits when available.

## Example requests
> 「Weekly IT Newsのスキルを使って、今週のMojo/MLIRニュースを一次ソースで調査し、20枚の技術プレゼンを作って。図解が有効なら編集可能なPowerPoint図形にし、出典を残して。」

> 「このPPTXをレビューし、意味のない画像、比較条件が異なるグラフ、文字はみ出しを修正して。公式資料スクショには出典を付けて。」

> 「ニュース記事の画面を引用するなら、その画像が示す具体的な根拠を説明して。適切な画面を取得できないなら無理に貼らないで。」

## License

The original source code, portable agent-skill instructions, build scripts, and
repository documentation are released under the **MIT License**. See [LICENSE](LICENSE).

**Scope:** MIT covers content owned by this repository's author only. The four
reference PowerPoint decks are **not distributed or relicensed** here. External
product imagery, news/article screenshots, logos, third-party technical figures,
and other cited material retain their respective rights and reuse requirements.
A citation alone is not permission to redistribute someone else's work.

## Reference decks and rights
The four originals `20260125.pptx`, `20260412.pptx`, `20260913.pptx`, and `20261012.pptx` **are not committed** because they include external product, press and keynote images. See [canonical editorial structure](skills/weekly-it-news/references/editorial-structure.md) and [style lineage](skills/weekly-it-news/references/style-from-samples.md) for source-slide indices. Slides and graphics aren't automatically free to redistribute merely because sources are attributed. Reuse original private deck as a template by attaching it in the target assistant, when permissions allow.

## Compatibility references
- Microsoft: [Agent Builder skills](https://learn.microsoft.com/microsoft-365/copilot/extensibility/agent-builder-add-skills), [PowerPoint custom skills](https://support.microsoft.com/ja-jp/powerpoint/copilot/copilot-in-powerpoint-skills).
- OpenAI: [Working with presentations in ChatGPT Work](https://help.openai.com/en/articles/20001278-creating-and-editing-documents-spreadsheets-and-presentations-with-chatgpt-work).

## Release notes
- **CI/CD:** dual-package reproducible build, PR/main Artifacts and tag-based GitHub Releases; documented editorial/design rationale.
- **0.4.0**: prioritize Copilot-in-PowerPoint one-session creation; optional evidence audit / cross-host brief; offline PPTX structural QA and regression tests; deduplicate quality gates.
- **0.3.0**: enforce actual PPTX output (Word is not a substitute); accept meaningful, traceable journalist photographs and graphics inside news articles as well as official images; distinguish an article image from a full-page capture; check that requested images are actually embedded; add Copilot regression cases and runtime routing notes.
- **0.2.0**: original pre-AI narrative structure takes precedence over later polished layouts.

## Known limits
- The skill cannot modify built-in slide generation engines, force use of a specific hidden tool, guarantee live website screenshot capture, or ensure identical pixel output in different hosts.
- Existing PPTX native charts are not present in any of the four reference decks (though editable tables and native shape diagrams are); chart guidance is an enhancement, not a sample-derived convention.
- Cross-host actual invocation and output quality must be tested in each account/tenant after installation. No promise of auto-screenshot availability.