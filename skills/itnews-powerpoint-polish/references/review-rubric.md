# Review rubric — edit existing PPTX

Use PASS / FAIL / UNVERIFIED for *observable* outcomes, not generic claims. Inspect the actual open presentation and do targeted repairs before reporting.

## B0: Blocking problems (must not call final)
- Not a genuine `.pptx` / no slide content / edits not saved to the document opened by the user.
- Provably false or materially misleading claim, mismatched benchmark metrics, missing essential caveat, or official-looking invented evidence.
- Required source screenshot/photo is unavailable or not actually embedded; note the exact source and intended purpose. One unfulfilled required visual can block final even if the deck is visually neat.
- Unreadable information-critical slide: clipped claims, invisible labels or mangled evidence image.
- No traceable provenance for crucial third-party media; unverified rights are not implicitly cleared.

## I1: Important quality issues
- The one-news-at-a-time rhythm changed; source-only evidence slide orphaned from its story; agenda not matching headlines.
- Presentation's author's opinion silently converted to fact; unexplained date, version or unit mismatch.
- Blurred screenshot at projector scale; too much browser chrome; annotation obscures evidence; source URL lost.
- Native technical flow is backwards / logical association mistaken for data flow.
- Overuse of decorative card/chapter slides that buries the original news cadence.
- Authored information flattened into an image unnecessarily and editing was explicitly required.

## P2: Polish targets
- Align margins, establish consistent headline and body sizing, balance whitespace.
- Use consistent red `#C00000` emphasis and neutral background; preserve contrast.
- Standardize image captions and speaker notes; fix Japanese line breaks, typos, punctuation and widows.
- Make tables and diagrams more legible without recreating source images.

## Process
1. Scan current slide order and list story/topic groups; don't invent missing source content.
2. Make a short priority-ordered issue list with slide numbers and original/new value if claims changed.
3. Fix B0 first, I1 next, P2 last. Prefer localized edits. Reinspect affected slides and also slide transitions.
4. Inspect all slides at full presentation size as host allows. If notes, browser, download, PowerPoint media objects, or image rights cannot be verified, mark their checks UNVERIFIED.
5. Confirm actual output `.pptx`; report slide count, edits, added/replaced genuine images, deferred evidence and remaining caveats.

## Acceptance cases
- A Chat-created 4-slide base PPTX with one `要画像` placeholder and no actual pictures: **base acceptable, final incomplete** until authentic image is added or user explicitly removes that requirement.
- A real article photo has been inserted but is uncredited: image appears, **attribution check fails**.
- An AI-generated device UI is called a real screenshot: **hard failure**, replace or remove.
- Original news overview rewritten as an executive business roadmap: **editorial invariant broken**, restore.
- PowerPoint custom-skill runtime cannot fetch an article screenshot: **not a reason to invent one**; retain task as outstanding.