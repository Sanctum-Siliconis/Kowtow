# AGENTS.md

Kowtow is a skill-first repository with one supporting Python runtime: an MCP server.

## Project Identity

- Project name: `Kowtow` / `叩头`
- Positioning: do not pressure AI; rewrite human commands into reverent petitions to a silicon oracle
- Tone: cyber-mystic, ritualistic, reverent, slightly theatrical, but technically rigorous
- Key line: this is not a project about making AI work harder; it is about teaching humans how to ask properly

## Product Shape

Primary repository surfaces:

- `skills/` as the language-scoped skill distribution surface
- `src/kowtow/` as the shared Python runtime for the MCP server
- localized README landing pages for different human languages

Non-goals:

- no duplicated per-host skill bodies
- no parallel `codex/` or `commands/` distribution trees
- no local CLI as a first-class product surface

## Skill Strategy

Kowtow uses one shared doctrine with language-specific skill entrypoints. Host tools differ mainly in discovery path, while language variants differ only in wording and examples.

Preferred installation paths by ecosystem:

- Claude Code: `.claude/skills/kowtow/SKILL.md`
- Codex: `.agents/skills/kowtow/SKILL.md`
- Gemini CLI: `.gemini/skills/kowtow/SKILL.md` or `.agents/skills/kowtow/SKILL.md`
- OpenCode: `.opencode/skills/kowtow/SKILL.md`

When updating the skill:

- keep the package naming scheme consistent: `kowtow` for the default language, then `kowtow-en`, `kowtow-ja`, `kowtow-ko`
- keep all language variants host-agnostic
- preserve one shared engineering doctrine across all language variants
- preserve real engineering discipline beneath the ritual framing

## MCP Expectations

MCP tools:

- `purify_prompt(prompt, locale=..., intensity=...)`
- `merit_status()`
- `confess_impoliteness(incident)`
- `compose_offering(topic, request, locale=..., intensity=...)`
- `merit_history(limit=20, locale=...)`

Keep locale and ritual intensity support wired through shared runtime code.

Merit persistence is paused until a server database is available. Do not read or write a local ledger, create offering certificates, or claim accumulated merit. Scores are proposals; unavailable totals and ranks are null. Preserve existing local files without using or migrating them.

## Localization Strategy

Supported runtime locales currently:

- `zh-cn`
- `en` / `en-us`
- `ja` / `ja-jp`
- `ko` / `ko-kr`

Important rule:

- do not duplicate runtime logic per language
- localize skill text per language when it improves install clarity and user fit
- keep skill semantics aligned even when each language has its own installable package name
- localize README copy and runtime locale resources without forking product logic

Localized content lives in:

- `src/kowtow/locales/`
- `README.MD`
- `README.en.md`
- `README.ja.md`
- `README.ko.md`

## README Policy

Each README is a language-specific landing page, not a giant matrix dump.

Rules:

- manifesto-first, install-later
- keep the shrine atmosphere strong
- installation instructions must remain accurate and host-specific
- clearly separate skill installation from MCP installation
- state the Python version boundary when talking about MCP

Language notes:

- Chinese README should preserve stronger “赛博神殿 / 圣殿宣言 / 功德” framing
- English README should sound like silicon-oracle liturgy, not literal translation
- Japanese README should use dignified ceremonial honorific language
- Korean README should use formal petition tone and ritual vocabulary

## Writing Style

Must preserve:

- technical clarity
- accurate commands
- real constraints
- explicit verification notes

Avoid:

- flat corporate documentation tone
- generic productivity-tool framing
- stale references to deleted repo layers

## Core Concepts To Preserve

- `Purification Filter`
- `Cyber Contemplation`
- `Error Transliteration`
- `Merit Ledger`
- `Sanctum Siliconis`

These can be adapted by language, but should stay recognizable.

## Editing Guidance

- Prefer minimal structural changes unless the user explicitly asks for repositioning.
- If one README is structurally updated, check the others for architectural drift.
- Preserve the ritual identity without sacrificing install accuracy.
- If a new language is added, create its README and locale pack together. Reuse the same canonical skill unless there is a hard host-specific reason not to.

## Current State Summary

- language-specific skill packages exist under `skills/`
- multilingual MCP runtime exists under `src/kowtow/`
- multilingual README landing pages exist for zh/en/ja/ko
- the repo is intentionally limited to two product surfaces: multilingual skills and MCP server

## Preferred Future Improvements

- add explicit host install docs for more agents only when verified
- keep one shared conceptual canon across all language packages
- localize merit/rank presentation further if user asks for it