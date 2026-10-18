# Platform adapter: ChatGPT Work, PowerPoint Copilot and M365 Copilot Chat

This is a **portable behavior specification** using the `SKILL.md` convention. It does not modify Microsoft/OpenAI built-in slide engines and cannot guarantee their exact internal tool selection. Availability and permissions can vary by tenant, account and date.

## ChatGPT / ChatGPT Work
- Use the custom ChatGPT skill/plugin where supported and available; ask the user to work in Work mode for extensive document creation/navigation tasks. Provide source PowerPoint or a derived template explicitly if the host cannot access it.
- Prefer native presentation/file-creation actions. Use real Web research and screenshots only when those tools are actually present. If native deck output is unavailable, explain the alternative rather than promising PPTX.
- ChatGPT Work’s file capabilities vary by configuration; do not assume that its desktop PowerPoint integration exists merely because it can make presentation deliverables.
- The repository's root `plugin.json` is for a separate ChatGPT plugin package; the portable SKILL.md is in `skills/weekly-it-news/`.

## Microsoft 365 Copilot Chat (Agent Builder)
- As of Microsoft Learn documentation updated Sep 30, 2026, custom skills in declarative agents are **preview** and require a qualifying tenant enrolled in **Frontier Program**. Support depends on licenses, policies and admin settings; do not claim that all Copilot Chat users can upload a skill.
- Go to Copilot Chat → Agents & Skills → New agent → Agent Builder. Enable any necessary document/chart or image creation capabilities when available. On Configure → Skills → Add, upload the Microsoft-specific ZIP with `SKILL.md` at archive root and its `references/` and `templates/` directory. Skill instructions must be under **20,000 characters**, package <= **50 MB**. See: https://learn.microsoft.com/microsoft-365/copilot/extensibility/agent-builder-add-skills
- A declarative agent’s output may differ from PowerPoint Copilot’s direct-edit behavior. The skill may guide which charts/screenshots to use but cannot summon nonexistent browsing/screenshot capabilities.

## Copilot in PowerPoint
- In Copilot pane → + → Choose skills → Manage skills → Add skill, upload the skill files or enter text; custom skills are stored in a OneDrive Skills folder. A skill folder contains a `SKILL.md` with YAML `name` and `description`. Select it explicitly with @mention when testing. Source: https://support.microsoft.com/ja-jp/powerpoint/copilot/copilot-in-powerpoint-skills
- To install manually from the repository, copy the `skills/weekly-it-news` directory into the personal Skills folder where permitted. For pure prompt-based paste, copy only SKILL.md; supporting files won't be accessible unless also uploaded.
- Use native PowerPoint tools for diagrams, tables and chart edits where the Copilot environment permits, and use Brand Kit/templates when configured; explicitly test each operation in the target tenant.

## Capability matrix — expectations, not guarantees

| Feature | ChatGPT Work | M365 Copilot Chat Agent | Copilot in PowerPoint |
|---|---|---|---|
| Follow portable SKILL.md rules | Via installed custom skill/plugin if enabled | Via uploaded skill when eligible | Via user-added skill |
| Produce/edit presentations | Depends on available Work/file tools | Depends on agent capability and runtime | PowerPoint-native context |
| Native editable chart/table/shape | Test the host's output | Test the host's output | Prefer native functions; test |
| Browse/capture real website UI | Only when browsing/capture available | Don't assume actual screenshot access | Don't assume actual screenshot access |
| Same pixel-identical PPTX | **Not guaranteed** | **Not guaranteed** | **Not guaranteed** |

## Required cross-host verification
Test three scenarios in each target host: (1) compare three source-backed specifications in a table, (2) explain a 4-node architecture with native shape arrows, (3) insert an authentic attributed screenshot of a specified real page (or explicitly report impossible). Verify native editability, evidence notes and rendering. Never report integration complete until these pass in the actual account/tenant.