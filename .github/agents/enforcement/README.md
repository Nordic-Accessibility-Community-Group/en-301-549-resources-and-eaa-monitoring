# Enforcement tracking specification

Follow [shared workflow](../workflow.md), [evidence](../evidence.md) and [review](../review.md). Public changes belong in EAA enforcement tracking.md within authorised scope; important evidence must also reach relevant cross-page research records. Use enforcement/ branches and `Audit EAA enforcement tracking: <scope>` for factual PRs; never use the monitoring title or trigger its post-draft research pass. Setup/infrastructure uses descriptive titles and separate PRs.

Cover actual monitoring activity, enforcement measures, civil cases and Commission proceedings. Publish a country only when supported relevant activity exists; no placeholder rows or eight-sector requirements. Preserve inherited entries pending evidence review. Current research covers 36 authorised jurisdictions; records do not require public entries. Creating a record never authorises new research. A multi-country pass needs explicit scope. A shared proceeding is stored once and referenced by affected countries.

[Record format](record-format.md) owns fields, dates, source types, correspondence metadata, claims/statistics and publication mapping. [Presentation](presentation.md) owns sections, ordering, stages and source labels. Preserve legal-basis, sector, case identifiers, exact event/procedural status and uncertainty. Distinguish aggregate counts from individual cases; record units, period, counting basis and overlap. Never infer totals from partial categories.

The frozen baseline preserves original entries; the current map binds reviewed rows to verified claims. An inherited exception never verifies an addition. Identify unchanged legacy assertions in mixed rows explicitly in the review report. Do not rehash a frozen baseline to silence a check. Reports under reviews/ identify exact versions, isolation and limits.

Run `python3 .github/agents/enforcement/check.py` and `python3 -m unittest discover -s .github/agents/enforcement -p 'test_*.py'`, plus shared content checks. These do not establish legal meaning or live reachability. Do not import the monitoring full-roster/intake checklist or the sanctions EU-27/seven-column public-table gate. Do not change watcher runtime state as an incidental content action. No new watcher or rollout is scheduled by these instructions.

Historical setup inventory/backlog remains in Git history and country questions; it is not a fresh research instruction.
