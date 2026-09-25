# PR-event evidence routing

Read [shared evidence](../evidence.md), [workflow](../workflow.md) and [review](../review.md). Intake, page registry, correspondence and publication rules are owned there. This file owns PR-event trigger/state operations only.

## Triggers and duplicate control

- New evidence provided in a chat: perform intake and page assessment in that same task, then suggest the missing PR(s). There is no supported webhook for arbitrary ChatGPT uploads; this is an agent instruction, not a claim of background access to other chats or email inboxes.
- Research/watcher run: perform the same steps before completing the run, even when the discovery is outside that page's scope. Keep existing country/research budgets; store unverified leads and do not broaden the research pass automatically.
- GitHub safety net: a separate PR-event automation examines opened, synchronized, ready-for-review and merged PRs in the testing repository. It filters actual changed files, reads relevant records and proposes missed research/page updates in ChatGPT. It does not send GitHub comments or duplicate the existing post-draft link-check automation. Ignore closed-unmerged and unrelated changes.
- Persistent notification state lives at .github/agents/evidence-routing/state.json on evidence-routing/state, never merged. Acquire a unique 30-minute lease using the current blob SHA; stop on an active foreign lease or write conflict. Recheck ownership before updating state; release only your lease. Deduplicate by evidence fingerprint, country, target page and proposed change, not merely PR number or delivery ID. Reassess changed evidence; do not repeat an unchanged suggestion. If state is unavailable, report the blocker without making writes or claiming a completed check.

Runtime state does not replace research records or events.json. A suggestion is resolved only after the corresponding change reaches main, is already present with matching scope, or has an explicit reviewed disposition. Never interpret a closed-unmerged PR as completed work. Keep triggers enabled after no-op runs.

## Storage version 2

Read [shared storage](../research/README.md). The events.json file is generated from country deliveries and retains the events array for existing readers. Edit deliveries in research/countries/<country>.json, then run `python3 .github/scripts/generate-routing-index.py --write`; do not edit the index independently. Each destination has an explicit domain. Null still means no applicable domain record; do not create placeholder domains to satisfy routing. Runtime state and notification history remain on the existing dedicated branch.
