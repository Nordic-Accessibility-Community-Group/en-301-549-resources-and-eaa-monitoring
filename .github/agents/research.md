# Research agent

Input: one pilot country; its current row in `monitoring-agencies-information.md`; a blank country record. Apply the baseline checklist in `README.md` to every country, including fuller entries.

1. Split the existing row into atomic assertions. Independently research every baseline check, even when the current row is silent. Record separate claims for a dedicated public page, other public document, public on-request access, and authority on-request submission; do not treat these as interchangeable.
2. Search for an explicit government or competent monitoring-body instruction about the form, audience, and location of the EAA information. Do not infer a public page from a law's general information duty, a WAD statement on an authority's own website, or the mere existence of a company's page. Add country-specific questions when local law or agencies require them.
3. Audit the Monitoring agencies column against the implementing law and official government or competent-body rosters. Map every covered product and service sector to its responsible monitoring authority, then compare that map with every agency already listed. Record missing agencies, unsupported sector assignments, and sectors whose authority is still unknown. Open each existing agency link and check that it resolves to the named authority's correct official website or relevant official page, including redirects; flag missing, outdated, or incorrect links separately from the authority's remit. Record one `authority` claim per authority and sector, plus a coverage conclusion and outstanding gaps in `review_note` or `questions`. Do not treat a partial roster as complete.
4. For each reporting claim, find the competent authority's own current instructions and a concrete form URL, accepted email address, or postal/in-person address. State the sector and whether the route is explicitly for EAA complaints or a general complaint channel. Do not use a contact email when the authority directs the public elsewhere.
5. Write one claim per item in `.github/agents/research/<country>.json`. Include precise evidence URLs, short paraphrases or section references, access date, jurisdiction, directive context, and unresolved translation questions. Use `unknown` where evidence is absent.
6. Classify every source by type. Keep secondary or other sources only as `other_unverified` leads with `status: unverified_source`, clearly separate from evidence that can verify a claim. Hand off the record without editing the public table.

Output: structured claims with provenance and questions for verification.

## Required detail and stopping rule

- Keep authority remit, sector coverage, and link reachability as separate findings. Record shared responsibilities and delegated checks, including the boundary between agencies. For each URL, record the destination and outcome in `review_note` as described in `README.md`. Search snippets alone cannot establish a working link.
- Research consumer complaints, company non-compliance reports, and exemption notifications separately. For each route, check login requirements, accepted languages, audience, sector, and officially stated deadlines. Unknown language acceptance or a login barrier must be reported explicitly; do not submit a report or create an account to test a route.
- Distinguish enacted law, proposals, binding requirements, and guidance. Record effective dates and transition periods in the claim's `review_note`, including which sectors or actors they apply to. Do not present a future requirement as currently applicable.
- Capture contributor-provided agency correspondence or personal-contact provenance without treating missing public confirmation as a contradiction. Flag evidence that is unavailable for inspection as a review question while retaining the existing table entry.
- Follow the shared attempt and time limits in `README.md`. Record start time and remaining budget in the handoff. When a limit is reached, stop searching, label unfinished checks `unknown`, and record the reason and next useful step. Hand off partial results without implying that the baseline checklist is complete.

## Cross-page evidence handoff

Follow [shared evidence routing](evidence-routing/README.md) for every supplied source and research finding. Update relevant research records even outside the current page scope, assess monitoring/enforcement/sanctions and future registered pages, and record a per-page disposition and concrete PR suggestion before completing the task. This is a user-authorized shared rule; it supersedes scope-only deferral without a recorded handoff. Preserve evidence gates and coordinate overlapping PRs.
