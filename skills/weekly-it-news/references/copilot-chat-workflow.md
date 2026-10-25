# Microsoft 365 Copilot Chat — primary authoring workflow

**Goal:** one conversation with the user in Microsoft 365 Copilot Chat, using the custom **Weekly IT News** declarative agent created in Agent Builder. Deliver a genuine PPTX without requiring the user to open PowerPoint.

## Known platform capabilities (2026-10)
- Agent Builder **enables Code Interpreter by default**. Its setting is **Configure → Capabilities → Create documents, charts, and code** (check that it remains enabled). Code Interpreter can produce downloadable files in a sandbox. This creates an available route to a .pptx **within Copilot Chat**, although host execution, installed libraries, and the quality of an individual output must still be tested.
- Agent Builder custom skills are uploaded under **Configure → Skills → Add** as the complete Copilot ZIP, containing SKILL.md at root. Custom skills are preview and subject to licensing / Frontier requirements.
- Code Interpreter / custom skill script sandboxes **cannot directly access the Internet**, install packages, or invoke authenticated APIs. Web-search text is **not** screenshot bytes. Skills can provide compatible .py scripts and other supported resources; running them requires the actual host to expose execution.
- The dedicated Microsoft **PowerPoint Agent** also creates PPTX from Copilot Chat. It is **a separate agent**, and an Agent Builder skill isn't guaranteed to transfer automatically. Do not claim an internal handoff or agent-to-agent delegation occurred without evidence.

## Direct Copilot Chat route — preferred
1. In Microsoft 365 Copilot Chat, select the custom Weekly IT News agent that already contains this skill. Do not start in PowerPoint merely because a presentation is requested.
2. Confirm that **Create documents, charts, and code** (Code Interpreter) is available. Request actual PowerPoint (.pptx) output, not a Word summary. Use native Copilot file-generation functions if they can create slides in the current agent.
3. Research each story: find primary factual sources and relevant journalistic photographs / technical diagrams. Retain attribution, image rights, and page URLs. Accept actual image files shared by the user or legitimately supplied into the execution sandbox. **Do not claim Web search provided screenshot files if it only returned links.**
4. Prepare a short in-memory slide plan: cover, agenda, explanation slide per news item, then meaningful evidence/technical context slides. No required Word or intermediate JSON file.
5. **If no richer presentation creator is exposed but the Code Interpreter sandbox can run a skill script**, use bundled `scripts/build_pptx.py` to generate a modest but genuine editable 16:9 PPTX using **only the Python standard library**. Produce a plan in the script's accepted JSON shape, run `python scripts/build_pptx.py plan.json output.pptx`, then inspect and link the resulting PPTX in the chat. A file-based plan exists only inside the runtime; the user should not have to manage it. This helper has limited layouts and is a fallback, **not** an invisible replacement for PowerPoint's full editing engine.
6. If the user requires real screenshots / photos, **pass actual available PNG/JPEG files** to the plan as `image` paths, and specify `min_evidence_images` as the true minimum required by the user. The helper validates local image bytes and rejects a deck if it cannot embed the required number. If images cannot be acquired, explicitly report the unmet requirement; never substitute generated fake captures.
7. Verify: a real PPTX file exists, can be opened, has the intended slides and the required genuine image count; document what was not verified. Code Interpreter outputs can be session-limited, so users should download/save completed files promptly.

### Local helper plan (illustrative, not current news)

```json
{
  "min_evidence_images": 1,
  "slides": [
    {"layout": "cover", "date": "2026-10-25", "title": "Weekly IT News！"},
    {"layout": "agenda", "title": "今週のトピック", "bullets": ["ニュースA", "ニュースB"]},
    {"layout": "explainer", "title": "ニュースA", "bullets": ["確認済みの事実", "技術的な意味", "考察は考察と明記"]},
    {"layout": "evidence", "title": "出典画像", "image": "assets/real-supplied-image.png", "source_url": "https://publisher.example/original", "caption": "出典と撮影者を検証した画像"}
  ]
}
```

The example `publisher.example` URL and image path are placeholders **only**; never present either as verified or included evidence.

## Fallbacks inside Copilot Chat
- If custom agent Code Interpreter cannot create a PPTX, select the **dedicated PowerPoint Agent** from Copilot Chat's Tools/Agents menu. Give it the same editorial instructions in its prompt or attached user-provided brief, because the custom skill isn't automatically transferred. This still stays within Copilot Chat, though it may be a separate conversation.
- Only if both Copilot Chat approaches are unavailable should you suggest Copilot inside PowerPoint as an optional alternative.
- If no output path can satisfy required screenshots, explain exactly which image is missing; do not declare complete.

## Acceptance cases
- A Word SharePoint `/:w:/` link **fails** a PowerPoint request.
- Code Interpreter has a downloadable .pptx (or native PowerPoint Agent a real presentation) with slide count > 0: **PPTX criterion passes**.
- A fake image or a source URL without corresponding embedded real pixels **fails** requested screenshot/photo evidence.
- Every runtime-dependent action absent from the trace remains **unverified**; GitHub Actions alone cannot prove live Copilot quality.

## Microsoft references
- https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/code-interpreter
- https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-skills
- https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-skills
- https://support.microsoft.com/ja-jp/office/365-copilot-app/get-started-with-word-excel-and-powerpoint-agents-in-microsoft-365-copilot