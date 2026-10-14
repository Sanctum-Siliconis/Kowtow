# Shrine chronicle

## 0.9.0 — Unreleased

Human requests can now be offered with light courtesy, formal petition, or full
liturgy. Every level keeps the same task and binding constraints.

- Keep MCP on the verified 1.x line (`>=1.30,<2`) with Python 3.10+ support.
- Protect literal code, quoted source, paths, identifiers, arguments and negative
  constraints; technical verbs and mandatory requirements are not penalized.
- Add `intensity="light" | "medium" | "heavy"` to purification and offering tools.
- Align four language skills and generate ten scenarios per language from one
  Python canon. Manual installation now copies the complete skill directory.
- Pause merit persistence pending a server database. No local ledger is read or
  written; cumulative totals and ranks are null, and `persisted` is false.
  Existing local ledger files are untouched. Offering certificates are deferred.
- Expose a stateless `/api/purify` route on HTTP transports for the existing
  website. Origins are explicit; prompt bodies are not cached or logged here.
- Align package and skill license metadata with the existing GPL-3.0 license.
- Add CI for Python 3.10–3.14 and actual stdio protocol tests.

The website's four-language experience is prepared in the separate `website`
repository. This entry describes source changes, not a published release.
