# Shared evidence intake and page updates

This workflow applies to all supplied correspondence, attachments, research discoveries and automated runs in the testing repository. Important evidence must be recorded even when it belongs to a different page than the current task. This supersedes page-specific instructions that would discard or indefinitely defer out-of-scope evidence. It does not authorize automatic merges, upstream writes or unsolicited correspondence.

## Intake and routing

1. Read the actual source. Record issuer, source/event dates separately, exact source URL or private-safe attachment reference, evidence passage or factual summary, source type, verification status, scope and unresolved questions. For attachments, retain a SHA-256 fingerprint where available; never commit the raw email, signatures, private addresses or credentials. An official email is distinct from a contributor's recollection or an industry representative's account.
2. Update the existing country research record before declaring the work complete. Preserve previous evidence and explicit supersession history. If the subject belongs elsewhere, add a traceable handoff to that page's research record now; never rely solely on a chat message, PR description or watcher state. Do not label a stored lead verified. Unanswered outgoing questions are not facts.
3. Assess every relevant destination in the registry below. Record one stable evidence ID with per-page dispositions in events.json: proposed, already_present, research_only, needs_evidence, blocked_by_open_pr or not_applicable. Include record paths, reason, next action and PR number when one exists. A single disposition must not hide unfinished destinations. No public edit is necessary when nothing relevant changed.
4. Compare current main AND open PR heads. If verified material information is missing or outdated, suggest a concrete PR in the same response: page, country, exact proposed change, evidence and unresolved limitations. When the user has authorized edits, prepare or update the appropriate draft. Add public wording only after evidence, isolated source-fidelity/readability and applicable validation gates pass. Coordinate overlapping files; do not overwrite another project's branch. One coherent evidence event may update several relevant pages/records; explain that scope. Retain separate infrastructure review where practical.
5. For a blocked destination, leave the evidence in its research record and a specific pending PR suggestion in the routing ledger. Do not report complete until each destination has an explicit disposition. Recheck pending suggestions after the blocking PR merges; never start a new country rollout.
6. Preserve exact distinctions: powers versus actions, complaints versus findings, plans versus completed remediation, conditional versus imposed/paid penalties, proposals versus adopted law, public users versus companies, and EAA versus other law. Missing reports do not establish no enforcement. A source's publication date is not the event date.

## Page registry

| Page | Research destination | Relevant information |
| --- | --- | --- |
| [Monitoring agencies](../../../monitoring-agencies-information.md) | ../research/<country>.json | Authorities and remits, public/company routes, languages, statement/public-information duties |
| [Enforcement tracking](../../../EAA%20enforcement%20tracking.md) | ../enforcement/research/<country>.json | Monitoring activity, actual proceedings, warnings/orders/penalties, statistics and outcomes |
| [Sanctions](../../../EAA%20sanctions.md) | ../research/sanctions/<country>.json | Statutory sanctions, maxima, conditions and competent powers; actual cases alone do not amend statutory maxima |
| Future page | Register its path, record format and check command here at project setup | Record evidence first; maintain a specific handoff until a destination exists |

Keep a canonical source reference and cross-links when the same evidence is relevant to multiple records; copy only the facts needed by the destination, retaining provenance and status. Do not make an unsupported record satisfy a publication checker by changing its status. Existing schemas remain distinct; add research notes/questions where no suitable claim field exists.

## Official correspondence

Direct correspondence from a competent authority supplied by the contributor can support an explicitly attributed factual statement after the original has been inspected, issuer/role and date checked, scope assessed, and exact publication wording reviewed. This is documentary verification of the supplied reply, not independent authentication or public publication. Record what remains unknown.

Enforcement sources use official_authority_correspondence with correspondence_review metadata: authority, source_date, document_sha256, reviewed_by, reviewed_on and scope_limit. Include a private-safe reference, relevant passage, access dates and provenance limitations. Generic contributor_correspondence and secondary accounts remain unverified unless separately corroborated. Never automatically upgrade historical correspondence just because the schema now permits this evidence route.

## Triggers and duplicate control

- New evidence provided in a chat: perform intake and page assessment in that same task, then suggest the missing PR(s). There is no supported webhook for arbitrary ChatGPT uploads; this is an agent instruction, not a claim of background access to other chats or email inboxes.
- Research/watcher run: perform the same steps before completing the run, even when the discovery is outside that page's scope. Keep existing country/research budgets; store unverified leads and do not broaden the research pass automatically.
- GitHub safety net: a separate PR-event automation examines opened, synchronized, ready-for-review and merged PRs in the testing repository. It filters actual changed files, reads relevant records and proposes missed research/page updates in ChatGPT. It does not send GitHub comments or duplicate the existing post-draft link-check automation. Ignore closed-unmerged and unrelated changes.
- Persistent notification state lives at .github/agents/evidence-routing/state.json on evidence-routing/state, never merged. Acquire a unique 30-minute lease using the current blob SHA; stop on an active foreign lease or write conflict. Recheck ownership before updating state; release only your lease. Deduplicate by evidence fingerprint, country, target page and proposed change, not merely PR number or delivery ID. Reassess changed evidence; do not repeat an unchanged suggestion. If state is unavailable, report the blocker without making writes or claiming a completed check.

Runtime state does not replace research records or events.json. A suggestion is resolved only after the corresponding change reaches main, is already present with matching scope, or has an explicit reviewed disposition. Never interpret a closed-unmerged PR as completed work. Keep triggers enabled after no-op runs.
