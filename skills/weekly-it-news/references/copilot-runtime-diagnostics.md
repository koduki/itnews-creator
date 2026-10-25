# Copilot runtime diagnosis — Word output or missing real screenshots

## What this means
Agent Builder declarative agents and their custom skills are **not the same execution
environment** as Microsoft's dedicated PowerPoint Agent or Copilot **inside**
PowerPoint. Uploading `SKILL.md` adds workflow instructions, and does **not** automatically route requests to the PowerPoint Agent. However Agent Builder **normally enables Code Interpreter**, which can create downloadable files and provides a potential direct **PPTX generation path inside the custom Copilot Chat agent**. The bundled `scripts/build_pptx.py` offers a tested offline fallback if skill-script execution is supported. None of this provides browser capture or downloaded article images automatically.

A URL with `:w:` is a Word document link, not evidence that a PowerPoint file
was generated. Without access to the actual document or agent transcript, do not
assert why the agent chose Word or that a particular skill was invoked.

## Strict output contract
- When the user requests slides or a PowerPoint, the primary deliverable is
  **an actual editable .pptx**, not Word (.docx), a prose outline, PDF, or a
  screenshot of slides, unless the user explicitly agrees to an alternative.
- Preflight available presentation/file-generation tools; if none can write a
  valid .pptx, explain the **blocking capability**. A storyboard, Word research
  brief, or source list can be offered as a clearly labeled *intermediate
  artifact*, never as task completion.
- Verify the file type and presence of real slides before claiming success.
  When possible, open/render the generated presentation and validate content.
- In Copilot Chat, the dedicated PowerPoint Agent is selected separately from
  an Agent Builder custom agent. Copilot in PowerPoint can also create a new
  presentation and reuse a referenced PPTX or Word research document.

## Photographs and article figures count as documentary evidence
The user may prefer an important photo, news-article technical figure or actual event image, not a website screenshot. Do not limit research to official vendor pages. Search reputable news articles as well as original announcements, verify what the particular image explains, and preserve publisher/photographer credits, publication URL, date and permission/quotation rationale. If the photo is the informative subject, inserting the credited photo is usually better than a tiny full-page news screenshot; if the page or reported quote itself is the subject, capture the relevant actual page. A URL or generated illustration is not a captured documentary image. A real-source visual request is satisfied only if its meaningful image appears in the final PPTX, or its absence is reported.

## Screenshot evidence contract
- Web search results, URLs, generated images and article summaries **are not
  screenshots**. A real screenshot must be captured from an actual page or
  provided by the user, verified as an actual source image, and have attribution.
- Make a per-news-item evidence inventory (source URL, why shown, screenshot
  present/absent, rights status, capture date, crop/readability).
- Before promising screenshots, determine whether the runtime can actually
  browse and capture the visible source page; **skills' script sandbox cannot
  access the network**. Having Web search does not imply screen capture.
- If the user asks for screenshot-backed slides and the capture tool is absent,
  state **"screenshot requirement unmet"** and ask for user-provided source
  screenshots or propose a separate browser-capable workflow. Do not silently
  omit the evidence pages and claim the slide deck is complete.
- Native diagram/chart/table slides may complement genuine screenshots but do
  not replace evidence when the screenshot itself is necessary.

## Copilot Chat-first choices and an optional editor
1. **Microsoft 365 Copilot Chat custom Agent Builder agent (default)**: check
   its Code Interpreter capability; use it to generate a real downloadable PPTX
   in the same chat, optionally through the bundled stdlib helper.
2. **Microsoft 365 Copilot Chat PowerPoint Agent (secondary)**:
   Select the dedicated **PowerPoint** agent in the Tools/Agents menu. If the
   custom Agent Builder skill is not available within this agent, transfer the
   approved outline, visual plan and citations to it. Test PowerPoint output.
   Never imply that Agent Builder-installed skills automatically run in this
   separate agent.

3. **Copilot inside PowerPoint (optional)**: open a .pptx there only when
   the user prefers app-based editing or Copilot Chat cannot finish.

A two-pass research/evidence -> native PowerPoint generation workflow is acceptable
but must preserve the required screenshots and sources. If the first stage only
created Word, report it as a **research draft**, not a completed PowerPoint.

## Verification checklist
1. Is the user-visible output a real **.pptx** with multiple slides?
2. Did a native PowerPoint creation tool execute, or was another file generated?
3. For each requested evidence screenshot, which real URL was captured and is it
   embedded in the resulting PPTX?
4. Did the source image retain readable relevant content with provenance?
5. Are authored diagrams and data charts editable, and are visuals nondecorative?
6. If any mandatory requirement fails, mark the task **incomplete** and provide
   a concrete host-switch/repair path.

## Microsoft references (as of 2026-10)
- Agent Builder skills and limits:
  https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-skills
- Custom skill script sandbox:
  https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-skills
- Dedicated Word/Excel/PowerPoint Agents:
  https://support.microsoft.com/en-us/office/365-copilot-app/get-started-with-word-excel-and-powerpoint-agents-in-microsoft-365-copilot
- Native PowerPoint skills:
  https://support.microsoft.com/en-us/powerpoint/copilot/copilot-in-powerpoint-skills
- New presentation in PowerPoint:
  https://support.microsoft.com/en-us/powerpoint/copilot/create-a-new-presentation-with-copilot-in-powerpoint

- Agent Builder Code Interpreter: https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/code-interpreter