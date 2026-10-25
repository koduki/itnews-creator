# Platform adapter: ChatGPT Work, PowerPoint Copilot and M365 Copilot Chat

This is a **portable behavior specification** using the `SKILL.md` convention. It does not modify Microsoft/OpenAI built-in slide engines and cannot guarantee their exact internal tool selection. Availability and permissions can vary by tenant, account and date.

## ChatGPT / ChatGPT Work
- Use the custom ChatGPT skill/plugin where supported and available; ask the user to work in Work mode for extensive document creation/navigation tasks. Provide source PowerPoint or a derived template explicitly if the host cannot access it.
- Prefer native presentation/file-creation actions. Use real Web research and screenshots only when those tools are actually present. If native deck output is unavailable, explain the alternative rather than promising PPTX.
- ChatGPT Work’s file capabilities vary by configuration; do not assume that its desktop PowerPoint integration exists merely because it can make presentation deliverables.
- The repository's root `plugin.json` is for a separate ChatGPT plugin package; the portable SKILL.md is in `skills/weekly-it-news/`.

## Preferred Copilot Chat usage

**Do not introduce a mandatory outside workflow.** In the custom Agent Builder agent, use its available Code Interpreter to create a genuine PPTX directly, with the bundled `scripts/build_pptx.py` as an offline last-resort helper. Select the separate PowerPoint Agent **in Copilot Chat** only when that direct route fails; PowerPoint in-app editing remains optional. Source photos cannot be conjured by code from Web search links; report missing actual image bytes. See `copilot-chat-workflow.md`.

## Default: Copilot Chat with Agent Builder + Code Interpreter

Microsoft documents that **Code Interpreter is enabled by default in Agent Builder**, under the **Create documents, charts, and code** capability. It can produce downloadable files and may generate a PPTX without opening PowerPoint. For this skill, make a direct PPTX in the custom chat agent first; use available native presentation creation, or (when actual script execution works) the included standard-library `scripts/build_pptx.py` fallback. The latter has limited layouts and only embeds already-available local PNG/JPEG images; it is NOT a browser capture facility. See `copilot-chat-workflow.md`.

The separate PowerPoint Agent is the **second choice inside Copilot Chat**. It creates presentations but cannot be presumed to load this Agent Builder skill. Copilot inside PowerPoint is an **optional third path**, not the required primary entry point. Claims of completed PPTX or screenshots require inspection of actual file/images, not the presence of a skill ZIP.

## Microsoft 365 Copilot Chat (Agent Builder)
- As of Microsoft Learn documentation updated Sep 30, 2026, custom skills in declarative agents are **preview** and require a qualifying tenant enrolled in **Frontier Program**. Support depends on licenses, policies and admin settings; do not claim that all Copilot Chat users can upload a skill.
- Go to Copilot Chat → Agents & Skills → New agent → Agent Builder. Enable any necessary document/chart or image creation capabilities when available. On Configure → Skills → Add, upload the Microsoft-specific ZIP with `SKILL.md` at archive root and its `references/` and `templates/` directory. Skill instructions must be under **20,000 characters**, package <= **50 MB**. See: https://learn.microsoft.com/microsoft-365/copilot/extensibility/agent-builder-add-skills
- A declarative agent’s output may differ from PowerPoint Copilot’s direct-edit behavior. An uploaded SKILL.md does not by itself select a PowerPoint renderer or add screenshot extraction, but **Agent Builder Code Interpreter is enabled by default and can create downloadable files**. A real earlier trial produced a Word report instead of a requested PPTX; treat it as an acceptance failure and explicitly invoke/verify the PPTX generation path. If the custom agent cannot produce PPTX, offer the dedicated PowerPoint Agent *inside Copilot Chat* before opening PowerPoint. Genuine images from reputable news articles are welcome when traceable and permitted. A web search result or image URL is not proof the pixels were acquired or embedded.

## Copilot in PowerPoint
- In Copilot pane → + → Choose skills → Manage skills → Add skill, upload the skill files or enter text; custom skills are stored in a OneDrive Skills folder. A skill folder contains a `SKILL.md` with YAML `name` and `description`. Select it explicitly with @mention when testing. Source: https://support.microsoft.com/ja-jp/powerpoint/copilot/copilot-in-powerpoint-skills
- To install manually from the repository, copy the `skills/weekly-it-news` directory into the personal Skills folder where permitted. For pure prompt-based paste, copy only SKILL.md; supporting files won't be accessible unless also uploaded.
- Use native PowerPoint tools for diagrams, tables and chart edits where the Copilot environment permits, and use Brand Kit/templates when configured; explicitly test each operation in the target tenant.

## Mandatory runtime routing for PowerPoint requests

**Agent Builder custom agent ≠ the dedicated PowerPoint Agent ≠ Copilot in PowerPoint.** These are separate entry points, not interchangeable backends. A portable skill cannot automatically transfer itself to another host or force calls to an inaccessible PowerPoint editing tool.

Before attempting authoring in any host, explicitly check **(1) PPTX creation**, **(2) real Web screenshot capture**, **(3) embedding real images**, and **(4) final file verification**. Do not infer tool access from the agent name, license, skill installation or Web search alone.

**If Agent Builder returns Word**: This is a failed PowerPoint request, not a completed presentation. First confirm Code Interpreter and try generating PPTX in the **same custom agent**; if not supported, select the separate **PowerPoint Agent within Copilot Chat** under Tools/Agents. Opening the PowerPoint app is a further option, not the default. If the custom Agent Builder skill is unavailable within PowerPoint Agent, first transfer a structured research brief and image/source manifest and re-apply authoring rules in the PowerPoint environment. Treat that as a two-stage workaround, not automatic skill interoperability.

**Screenshot constraint**: Agent Builder scripts cannot reach the network; native search does not imply browser-screen capture. If the source has no permitted screenshot capture facility and the user requires real evidence screenshots, declare that requirement unfulfilled and use a separate verified screenshot-provisioning step. A screenshot-only slide must have source URL, original date or capture date, visual purpose and readable relevant content.

**Completion**: Confirm that a concrete `.pptx` was produced and can be opened; if not, report "PPTX output requirement unmet". Confirm screenshots are embedded from real pages, or report "screenshot evidence requirement unmet". Never mark a Word link `/:w:/` as a completed PPTX. See `copilot-runtime-diagnostics.md`.

## Capability matrix — expectations, not guarantees

| Feature | ChatGPT Work | M365 Copilot Chat Agent | Copilot in PowerPoint |
|---|---|---|---|
| Follow portable SKILL.md rules | Via installed custom skill/plugin if enabled | Via uploaded skill when eligible | Via user-added skill |
| Produce/edit presentations | Depends on available Work/file tools | Depends on agent capability and runtime | PowerPoint-native context |
| Native editable chart/table/shape | Test the host's output | Test the host's output | Prefer native functions; test |
| Browse/capture real website UI | Only when browsing/capture available | Don't assume actual screenshot access | Don't assume actual screenshot access |
| Same pixel-identical PPTX | **Not guaranteed** | **Not guaranteed** | **Not guaranteed** |

## Required cross-host verification
First perform negative regression checks: request PowerPoint and reject a Word document as final; request authentic journalistic/official pictures and reject a text-only deck as fully successful. Then test three scenarios in each target host: (1) compare three source-backed specifications in a table, (2) explain a 4-node architecture with native shape arrows, (3) insert an authentic attributed screenshot of a specified real page (or explicitly report impossible). Verify native editability, evidence notes and rendering. Never report integration complete until these pass in the actual account/tenant.