# itnews-creator

A portable, evidence-led Japanese PowerPoint authoring skill, based on four user-supplied **Weekly IT News！** decks, with **2026-01-25 and 2026-04-12 as structural originals** and **2026-09-13 and 2026-10-12 as later optional visual refinements**.

The skill is not a new PowerPoint engine. It tells the available native ChatGPT / Microsoft 365 Copilot presentation tools **what to research, how to choose meaningful visuals, and what to validate**. Its core is shared across both hosts.

## What it does
- Preserves the original weekly format: **dated cover → short 今週のトピック → news explanation → authentic source screenshots/technical context → next news**. Later chapter dividers and summary slides are optional.
- Selects editable shape diagrams, numeric charts, structured tables, authentic official/product UI screenshots or no image as appropriate.
- Rejects decorative filler, unverifiable claims, misleading comparisons and manufactured screenshots.
- Uses a style family derived from the examples: 16:9, white, `#C00000` red, charcoal Japanese sans, simple agenda headlines, source-backed technical news explanations; optional numbered cards, chapter dividers and comparisons.
- Enforces a two-part review: source/rights validation plus slide-rendering/design QA when tools are available.

## Repository layout

```text
plugin.json                           # ChatGPT plugin manifest
skills/weekly-it-news/SKILL.md        # Portable core instructions
skills/weekly-it-news/references/     # Design, visual rights, QA, platform nuances
skills/weekly-it-news/templates/      # Slide storyboard
README.md
```

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

## Reference decks and rights
The four originals `20260125.pptx`, `20260412.pptx`, `20260913.pptx`, and `20261012.pptx` **are not committed** because they include external product, press and keynote images. See [canonical editorial structure](skills/weekly-it-news/references/editorial-structure.md) and [style lineage](skills/weekly-it-news/references/style-from-samples.md) for source-slide indices. Slides and graphics aren't automatically free to redistribute merely because sources are attributed. Reuse original private deck as a template by attaching it in the target assistant, when permissions allow.

## Compatibility references
- Microsoft: [Agent Builder skills](https://learn.microsoft.com/microsoft-365/copilot/extensibility/agent-builder-add-skills), [PowerPoint custom skills](https://support.microsoft.com/ja-jp/powerpoint/copilot/copilot-in-powerpoint-skills).
- OpenAI: [Working with presentations in ChatGPT Work](https://help.openai.com/en/articles/20001278-creating-and-editing-documents-spreadsheets-and-presentations-with-chatgpt-work).

## Release notes
- **0.2.0**: original pre-AI narrative structure takes precedence over later polished layouts.

## Known limits
- The skill cannot modify built-in slide generation engines, force use of a specific hidden tool, guarantee live website screenshot capture, or ensure identical pixel output in different hosts.
- Existing PPTX native charts are not present in any of the four reference decks (though editable tables and native shape diagrams are); chart guidance is an enhancement, not a sample-derived convention.
- Cross-host actual invocation and output quality must be tested in each account/tenant after installation. No promise of auto-screenshot availability.