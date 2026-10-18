# Visual evidence and image research policy

## Decide the communicative job
For each slide, write internally: “The audience should understand/compare/verify ______.” If the proposed visual cannot complete that statement, choose another medium or text-only.

| Job | Good representation | Reject |
|---|---|---|
| Compare throughput | Native bar/dot chart with same test conditions | A photo of a server rack, synthetic measured-looking values |
| Compare precise XR specs | Short editable table with units and source/date | Unsourced spec bingo or blurred full-page screenshot |
| Explain MLIR progressive lowering | Native stage/connector diagram with direction labels | Random abstract technology background |
| Show a newly announced device | Verified original manufacturer product photo | AI rendering passed off as the device |
| Show an app workflow | Authentic screenshot of relevant UI state with annotations | Fabricated UI, unrelated hero image |
| Quote a keynote slide | Minimal necessary crop, attribution and quotation context | Entire copyrighted keynote deck imported in bulk |
| Explain a forecast | Distinguish verified present vs explicit scenarios | Presentation of conjecture as a confirmed schedule |

## Source selection
1. First-party landing page, original press release, vendor docs or release notes.
2. Original paper, benchmark logs, cited experiment or verified repository.
3. Reputable independent reporting for critique or controversy; separate claims from first-party measurements.
4. Community anecdote only as labeled anecdote, not verified fact.

Collect: claim; source title; canonical URL; author or publisher; publication/date of event; checked date; asset URL or capture provenance; whether source directly supports the claim; permissions/licensing state (verified / restricted / unknown); proposed amount of material to reproduce; whether permission or a quotation exception is needed. Always separate factual applicability from copyright applicability.

## Image acquisition / screenshot constraints
- Prefer capture or download directly from original source when tools allow. Never silently substitute an unrelated image if the source is inaccessible.
- Screenshot the **specific claim-bearing portion** of a page, keep context enough to avoid misrepresenting it, and preserve essential labels.
- Sources with permission unknown: prefer attributed facts rendered as your own editable shapes/text; avoid copying image unless lawful reuse is established.
- No fabricated screenshots, fake official logos, fake live demo states, or invented citations.
- AI image generation is for clearly *illustrative* concepts only, labeled as conceptual; not a substitute for documentary evidence.
- If the tool cannot browse or screenshot, report the limitation and ask for/accept original images or create native, sourced alternatives. A pasted URL is not itself proof a page was accessed.

## Chart validation
- Check raw values, matching units, denominator, periods, benchmark configuration and sample counts. Compare same metric, not proxies.
- Use consistent scale and 0 baseline for ordinary bars unless a justified exception is labeled. Avoid 3D effects that distort values.
- Show uncertainty/small samples when relevant. Never imply a confidence interval, trend or rank that data do not support.
- Source data and as-of date should be documented in speaker notes or a source appendix.

## Diagram validation
- Distinguish data flow, control flow, causality and mere grouping. Label arrow types if different.
- Do not imply vendor-specific implementation details unless original architecture docs support them.
- If explanatory abstraction is invented by the author, explicitly label “模式図” and explain simplifications.

## Value-based image scoring (review heuristic)
Score 0–2 for claim relevance, information gain, factual fidelity, traceable rights/provenance, and projected readability (10 total); 8+ preferred. Any 0 in fidelity or provenance = reject. A score never overrides missing evidence or rights.