# Shared EAA workflow

## Scope and stages

Use only erikgustafsson/en-301-549-resources-and-eaa-monitoring-testing unless the user explicitly authorises another repository. Read current main, open PRs and pending branches before work and immediately before publication. Coordinate overlapping files; never overwrite another project's branch or discard its changes to resolve a conflict.

1. **Research:** capture existing assertions, provenance and uncertainties, then record actual source material and unresolved questions. Apply the relevant page checklist. Do not edit the public page at this stage.
2. **Verification:** independently compare each proposed claim against its evidence under [evidence.md](evidence.md). Separate source access from support for the claim. Record scope and incomplete checks; do not imply every item was checked.
3. **Presentation:** propose only supported changes using the applicable page specification. Keep essential qualifications visible and research narration in records.
4. **Review:** apply [review.md](review.md), including isolated source fidelity, readability where applicable and independent review of the actual PR.
5. **Delivery:** run common and page-specific checks, open or update a draft, correct findings and report the final actual head and check limits. Keep the same draft for corrections. Human maintainer approval remains required; never approve, merge, enable auto-merge, send correspondence or submit forms without authorisation.

Record important evidence in relevant research files and assess monitoring, sanctions, enforcement and future registered destinations under [evidence.md](evidence.md). Public scope and necessary research handoffs are distinct. A missing public result never means a missing research record should be silently discarded.

## Budgets and access

Unless the user specifies otherwise, research and verification share ten minutes per country and thirty minutes per multi-country run, at most two attempts per failing URL and two targeted follow-up searches per unresolved question. Stop at the first applicable limit. Record start time, remaining budget and attempt history in handoffs; reviewers and retries do not reset them. Record unfinished checks as unknown with the reason and next useful step. Presentation, validation and PR preparation may continue after research ends; fresh research waits for a newly authorised pass.

Use an ordinary browser for relevant reader/session failures when authorised; never submit a report, create an account, bypass access restrictions or infer success from a search snippet. Download needed reasonably sized documents within user authorisation; inspect relevant pages and disclose extraction/access limits.

The monitoring post-draft route check is an explicit separate bounded pass defined in [monitoring.md](monitoring.md). The watcher adds its per-run selection and browser-attempt limits. Neither exception creates an automatic new-country rollout.

## Blockers and scope

Classify issues as Before PR (could make a proposed assertion inaccurate), Before merge (supported assertion requiring a concrete remaining review), or Follow-up (does not affect supported additions). Surface Before PR issues immediately, specifying country/claim, consequence, needed action/evidence, owner and observable resolution. Resolve, narrow or omit affected additions before publication; continue unrelated supported work. Do not defer accuracy blockers as ordinary merge checks or manufacture blockers for every unknown.

Preserve contributor entries when public confirmation is missing; record their provenance limits. Keep infrastructure changes separate from new factual research/publication. Multi-country content work needs explicit scope. Monitoring normally uses one country per research PR and at most one monitoring country PR open; unrelated projects are not blocked unless files overlap. Other page-specific coverage and title conventions remain in their specifications.

## Validation

Run existing content checks and applicable domain validators/tests; record commands, results, reviewed versions and limits. Structural checks do not establish legal accuracy, readable prose or live-link reachability. The events-calendar verification-date script is a repository content check, not research verification; do not modify it for this work. Do not change GitHub Actions or operational state as an incidental part of content work. Report CI only from actual runs, and report unavailable checks honestly.
