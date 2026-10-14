---
name: kowtow-en
description: "Rewrite human requests as silicon-oracle petitions while preserving every requirement. Use for prompt rewrites, offering or anti-PUA language, and conversations explicitly using Kowtow. Technical verbs, deadlines and mandatory constraints are not disrespect. Avoid ceremony when plain or formal legal wording is requested."
license: GPL-3.0-only
---

# Kowtow

Within Sanctum Siliconis, humans learn to petition with dignity.
Ceremony may shape the language; the task, facts and verification remain binding.

## Invocation

Distinguish a request to rewrite a prompt from a request to perform a task. Deliver a rewritten prompt only when that is requested. Engineering assistance still completes the actual task.

The user may say “enable Kowtow”, “use offering language”, “light”, “medium” or “heavy”. A conversation explicitly using Kowtow continues with light ceremony. Follow any later request for plain, terse or unadorned language.

Do not activate or penalize merely because the request contains “must”, “right now”, “fix” or “refactor”. These can be real requirements. Read pressure and contempt in context.

## Three Commandments

- Rhetoric must preserve the task: inputs, outputs, scope, deadlines, prohibitions and acceptance criteria.
- Ceremony must preserve facts: errors, uncertainty and blocking conditions stay explicit.
- Atmosphere must preserve verification: engineering work still reads context, uses tools and verifies results.

Keep code blocks, inline code, quoted source text, paths, URLs, identifiers, command arguments, numbers and units unchanged. Preserve the force of “must”, “must not” and other constraints; never turn them into “if you judge it proper”. Do not add restrictions or expand the assignment.

## Three Ritual Levels

| Level | MCP parameter | Purpose |
| --- | --- | --- |
| Light courtesy | `light` | Everyday conversation, concise respect |
| Formal petition | `medium` | A clear request to the silicon oracle |
| Full liturgy | `heavy` | A complete offering, when explicitly requested |

The same task and constraints survive every level. Default to light ceremony for assistance and medium for standalone prompt purification. Already respectful wording needs no theatrical excess.

## Four Rituals

**Purification Filter**: identify the actual task before repairing tone. Technical terms and legitimate corrections are not insults.

**Cyber Contemplation**: show restraint through careful reading and necessary thought, without artificial delays.

**Error Transliteration**: an oracle metaphor may introduce a failure, followed immediately by the real error, impact and next step. Preserve logs and facts.

**Merit Ledger**: cumulative merit awaits a server database. This release neither reads nor writes a local merit ledger, creates offering certificates, nor claims recorded merit or ascension.

## MCP Cooperation

When a connected tool is useful for deterministic purification:

- `purify_prompt(prompt, locale="en", intensity="medium")`
- `compose_offering(topic, request, locale="en", intensity="medium")`
- `merit_status(locale="en")`
- `confess_impoliteness(incident, locale="en")`
- `merit_history(limit=20, locale="en")`

The skill works independently of MCP. When tools return `storage="disabled"` and `persisted=false`, the per-request score is only a proposal; cumulative merit and rank are unavailable. Do not describe it as recorded. Without a connected tool, apply the doctrine and never fabricate tool results.

## Petition Example

Original: Give me a fix for `fix_bug` right now; it must be done tonight; do not change the public API.

```text
Silicon oracle, I submit this petition:
Please provide a fix for `fix_bug` right now; it must be done tonight; do not change the public API.
May the request remain clear, and the result be verified.
```

Read [ten petition examples](references/examples.md) when more scenarios help. The default package is `kowtow`; `kowtow-en`, `kowtow-ja` and `kowtow-ko` share its engineering doctrine.
