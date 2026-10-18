# Style study — user-provided example presentations

Source material is two uploaded decks, **20260913.pptx** (53 slides, 2026-09-13) and **20261012.pptx** (34 slides, 2026-10-12). They are style references, not evidence for current factual assertions, and are not redistributed in this repository because they contain third-party press and product/event imagery.

## Quantified observations

| Observation | 2026-09-13 | 2026-10-12 |
| --- | ---: | ---: |
| Pages | 53 | 34 |
| Page size | 13.333 × 7.5 in (16:9) | 13.333 × 7.5 in (16:9) |
| Slides containing picture shapes | 32 | 13 |
| Native chart shapes | 0 | 0 |
| Slides containing native tables | 3 | 1 |
| Main Japanese fonts | Noto Sans JP | Noto Sans CJK JP |
| Main accent | #C00000 | #C00000 |
| Body colors | #464646 / #1E1E1E | #333333 / #1E1E1E |

*Counts are from PPTX shape inspection, not a claim about every visual's origin. Some diagrams are made from editable shapes and some embedded images are screenshots containing tables or charts.*

## Layout families to preserve
1. **Cover** — date + “Weekly IT News！” and three topics, white base/red headings; Sept slide 1 and Oct slide 1. The presenter avatar exists in the references; don't reuse/reproduce the avatar without permission.
2. **Agenda** — three topic cards, red numbered markers; both slide 2. Oct slide 3 expands to a more detailed chapter roadmap; use when the presentation is genuinely long.
3. **Section divider** — left red rule, sparse title and giant pale chapter numeral; Sept slides 3, 22, 34; Oct slides 10, 16, 19, 23, 29. This pacing gives dense material breathing room.
4. **Investigative evidence** — headline, primary content and first-party screenshot/image. Sept slides 5–9, 17–21 and Oct slides 4–8 show external material and event/product evidence.
5. **Comparative technical illustration** — authored native shapes and balanced multi-column boxes. Sept slides 10–11 (LLVM vs MLIR), 26 (HBM/NVHBM), Oct slides 27–28 (compute hierarchy), 32–33 (vendor/OS comparison and roadmap).
6. **Spec trade-offs** — aligned tables and structured two-column explanation. Oct slide 11 compares XR products; Sept slide 36 provides tabular news comparison.
7. **Synthesis** — multi-column summary with red framing; Sept slide 53 and Oct slide 34.

## What to improve rather than imitate
- **Legibility**: Sept relies heavily on compact body text, and Oct has several dense multi-column screens. The skill should split slides and enlarge information hierarchy where a presenter will project slides.
- **Purposeful imagery**: Sept contains clusters of large event screenshots; every screenshot needs a documented explanatory point. Use “image shows X” captions or short annotations when factual interpretation is non-obvious.
- **More editable charts**: Both decks contain comparison illustrations and tables but no native chart shapes. Promote numeric data to native charts only when measures share definitions, units and methodology.
- **Evidence metadata**: Use explicit source URL/publication date and uncertain-versus-confirmed labels for high-volatility technology claims; don't silently copy sample statements into new decks.
- **Avoid filler**: The use of images should follow an informational purpose, never a quota.

## Design implementation notes
- Emphasize hierarchy: 3–4 major topical sections per weekly edition is typical, but allow more or fewer based on meaningful subject clusters.
- Wide 16:9 decks; thin red vertical bars as section markers; red comparison/table headers; white or lightly tinted cards with generous padding.
- Headlines in Japanese with English product and technical terms left unmodified; ensure line breaks preserve readability.
- Bold red for established category names or contrast, not for every claim. Keep audience-facing definitions for specialized acronyms.
- Use editable diagrams for architecture and roadmaps; keep authentic first-party screenshots/photographs where identity is essential.