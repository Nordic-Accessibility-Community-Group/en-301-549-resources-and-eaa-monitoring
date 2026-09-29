# Public link-language audit — 27 September 2026

## Scope and outcome

Audited 567 links across all 11 public Markdown pages on main at `6e182119eb73d17e06599236a5f3b413bca67374`: monitoring agencies, sanctions, enforcement, standards adoption, README, statement template, e-book documentation, overlay examples and the three Understanding EN documents. Nine pages need markup changes; two have no links. The audit covers raw HTML and inline Markdown links, including balanced parentheses in destinations.

397 link occurrences receive supported destination-language hints. 134 occurrences remain explicitly unresolved or are template placeholders; 36 mail actions are not document-language links. These are coverage counts, not a claim that all destinations were reachable. The canonical audit at `../../link-language-audit.json` records 425 distinct document destinations, evidence, retrieval failures, language decisions and reasons for omissions. It replaces guessing from country domains. Existing link-text `lang="de"` on the German MLBF name is correct and retained.

Retrieved HTML language declarations and page titles were inspected. Conflicts or missing declarations received a second text-sample check. 18 PDFs were downloaded (each under 10 MB), and first-page/second-page text was inspected to establish language; no legal content was reverified. Language negotiation, mixed-language content, JavaScript-only forms, failed retrievals and anti-bot responses remain unresolved where a reliable destination language was not established. The original URLs are preserved, including links that redirected. No reports/forms were submitted.

Notable safeguards: Swedish PocketBook content uses `sv`, not its erroneous `se-se` declaration; Swedish Vivant and T-Meeting content is not labelled English based on incorrect declarations. Radware/verification responses do not turn Swedish source links into English links. The English-interface/French-content declaration form, English-request/Finnish-shell Traficom forms and Maltese shell around an English-law URL remain explicit review items.

## Presentation and preservation

Shared presentation rules require `hreflang` for established destination languages and distinguish it from visible-text `lang`; page/workflow entry points reference that rule. An offline coverage checker detects unassessed links, missing/wrong tags and unsupported tags on documented unresolved destinations. It does not claim to retrieve or authenticate external content.

Public visible wording and URLs are unchanged. Markdown links with known destination languages use equivalent HTML anchors. Three pre-existing blank-line boundaries inside reviewed Finland, France and Ireland enforcement rows were removed because Markdown otherwise exposed some cell HTML as code instead of rendering the links. Rendered comparison across all 11 pages, with those pre-existing boundaries normalised on the baseline side, confirms unchanged text, destinations and document structure apart from `hreflang`.

Sanctions reviewed-row hashes and enforcement reviewed-row hashes are refreshed without changing legal verification dates, evidence or claims. Frozen baselines and inherited statuses are untouched. A shared digest helper permits only added `hreflang` attributes when removing them restores the exact previously accepted row bytes; altered text, href, lang or other attributes do not qualify. Adoption uses the same helper so historical evidence/wording reports are not rewritten as fresh reviews. The independent reviewer confirmed this narrow preservation rule.

## Open PRs and final-batch follow-up

- PR #72 at `54efec62d3ab3a76c4deadf74c865a2e13e630b4`: all three new German strategy links already use correct `hreflang="de"` with English labels. The existing German monitoring-update link is covered by this main-page audit. No factual wording change is needed in #72.
- PR #70 at `677cf326f96552e5884fb19a6a5c3219154a901a`: no public-page changes. It overlaps check_adoption.py; preserve its work when refreshing either branch.
- PR #71 at `aa8bd1923b1169424ad3c93e8dae42256f6e6ffa`: all 67 changed files inspected by path; no public-page changes. It modifies country records also receiving sanctions presentation hashes here, so combine both sets of fields rather than replacing whole records.

The user requested a final pass after the active Analyze EN 301 549 updates task completes its last batch. A coordination request was delivered to that task. Heartbeat `final-en-link-language-audit` is active, checks hourly, stays quiet during research/unchanged state, and pauses after the requested final audit. It must inspect actual final PR heads rather than treating this snapshot as the last batch.

Before merge, the task preparing this PR for merge must refresh against any merged #70/#71/#72 changes, preserve all evidence and regenerate only generated indexes where needed. Completion requires resolving overlapping fields, rerunning the applicable validators and link-language check, and recording the resulting head and results in the PR. The final-batch heartbeat owns the later #71 link-language recheck; it does not approve a merge. Documented unresolved destinations are nonblocking follow-up unless a specific omission is shown to prevent publication. This PR does not merge anything, change facts or change watcher runtime state.

## Validation

Shared country/schema/domain/routing validation passes: 44 countries, 749 claims, 52 events. Link-language coverage check passes with the explicit unresolved counts above. Enforcement: 28 tests; sanctions: 5; adoption: 22; link-language parser/coverage: 2; current-storage tests: 8 — all pass. The separate frozen migration test rejects the intentionally updated sanctions row hashes; it is an original-migration acceptance test, not a factual/editorial-update check. Its frozen manifest is unchanged.

Markdownlint and verification-date checks pass. Rendered preservation and whitespace checks pass. GitHub CI and the independent actual-PR review are reported separately after publication. No translation of new factual wording was introduced, so isolated source-to-wording and B2 reviews are not applicable; destination-language evidence is recorded in the audit.

## Independent actual-head review

An independent reviewer inspected GitHub PR #73 at `f9c64b5c47427a29a4d3fb49606ba234099b2bda`, tree `b537046a0aea4222adc4b595bca1428d49f22da0`, and found no blocking issues. The remote tree matched the reviewed local tree. All 567 destinations and decoded labels were preserved across 11 pages; other text was unchanged after whitespace normalization. Country-record changes were limited to sanctions row hashes. Link-language (2), enforcement (28) and adoption (22) tests and all three domain validators passed independently. The reviewer confirmed supported language decisions remain separate from retrieval failures and other explicit gaps.

The current parser covers inline Markdown links and double-quoted HTML anchors, not reference-style Markdown or other HTML attribute quoting. All current public-page links were accounted for; future syntax expansion must extend coverage before claiming a complete audit. This is a presentation/infrastructure review, not renewed legal research or live revalidation of every source. GitHub reported zero check runs at the reviewed head, so GitHub CI remains unconfirmed. This review-record follow-up changes only this report.
