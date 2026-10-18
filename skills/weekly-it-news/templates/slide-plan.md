# Topic-first Weekly IT News storyboard

Plan **news items first, slides second**. The canonical early-deck structure is described in `../references/editorial-structure.md`. Planning fields belong in working notes, not as mandatory visible slide furniture.

## Deck
- Edition date and presenter/audience:
- Weekly news items (headline + why selected; count need not be 3):
- Source list and freshness checks:
- PPTX reference for cover/color only, if permitted:
- Explicitly requested depth (ordinary weekly talk vs extended deep dive):

## Repeat for each NEWS ITEM
- **Headline and actual event/publication date**:
- **Editorial lead / angle**: what happened, what changed, why it matters:
- **Facts / vendor claims / interpretation** (separately identified):
- **One anchor explanation slide**: short red title, concise bullets, optional qualified presenter opinion:
- **Supporting evidence slide(s), 0..n**:
  - Purpose: what the audience should notice in this original source:
  - Source: publisher, URL, page/date and checked date:
  - Asset: authentic screenshot, press photo, official diagram, GitHub PR, relevant table, etc.:
  - Rights/provenance: permission, attribution, necessity and amount:
  - Link back to anchor claim:
  - Caption/notes: may carry context while visible slide remains source-only:
- **Technical expansion slide(s), 0..n**:
  - Need: what is hard to understand without the diagram/table/chart?
  - Representation and why this representation:
  - Source data, verification, native shape editability and uncertainty:
- **Transition to next news item**: no mandatory section divider or thematic conclusion.

## Every slide: quality checkpoint
- Slide role: cover | short agenda | explanatory news anchor | authentic evidence | technical context | optional conclusion
- Parent news item:
- Claim and factual status; if evidence-only, explain its **purpose**, not an invented stand-alone claim:
- Value of visual; could it be removed without losing understanding?
- Attribution/right to reuse; exact source URL, access time and editorial crop:
- Native editable elements vs authentic raster asset:
- Viewability/cropping/legibility/overflow; verified, failed or unverified:

## Example (illustrative only)
- Topic headline: “New GPU language feature changes compilation options.”
- Anchor: outline announcement, affected ecosystem, tradeoff, speaker's hypothesis clearly identified.
- Evidence 1: screenshot of actual vendor announcement, linked in notes.
- Evidence 2: architecture diagram from a paper, only if essential and fairly cropped/cited.
- Native extra: redraw a simple translation pipeline as editable shapes if it improves comprehension without misrepresenting source.
- Move to next topic when nothing further is needed. No obligatory chart or summary.