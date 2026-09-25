# Enforcement record format (version 1)

The executable contract is [check.py](check.py); it uses the Python standard library. Copy [record-template.json](record-template.json) for a new jurisdiction and [claim-template.json](claim-template.json) for an actual researched assertion. The claim template contains blank fields, not an example of verified evidence. Fill its source URL (or a shareable correspondence reference) before adding it to a record; remove the placeholder source object if no source is known.

## Country records

Store one file named for the lowercase English country name under `research/`. Use Czechia as the record name; the inherited page's Czech Republic spelling stays unchanged. Require all 27 EU countries and preserve Norway, which already has a public entry. Other jurisdictions may be added when separately authorised. Do not add public rows to satisfy research coverage.

| Field | Meaning |
| --- | --- |
| `schema_version`, `country`, `jurisdiction_group` | Version 1, jurisdiction name, EU (Member State), EU territory (Åland), or non-EU |
| `created_on` | Administrative record creation date; never a source check |
| `research_state` | not_yet_researched, partially_researched or bounded_pass_completed |
| `search_result` | not_assessed, reportable_activity_found or no_reportable_activity_found_in_checked_sources |
| `attempted_on` | Most recent recorded research attempt, or null |
| `verified_on` | Latest verified claim date, or null; never implies all claims are verified |
| `knowledge_notes` | Current knowledge and limitations, including inherited material |
| `public_entry_ids` | IDs in public-map.json; empty is valid |
| `attempts` | Objects with attempted_on, scope, sources_checked (URLs), limitations and next_check |
| `claims` | Atomic evidence claims using the claim template; empty is valid |
| `questions` | Objects with priority, question, owner and resolved_when |

`not_yet_researched` describes work under this workflow, not all historical contributor activity. It requires empty claims/attempts and null attempt/verification dates. A bounded pass records exactly the sources and scope checked and its limitations; it never establishes exhaustive coverage. No-findings wording requires a completed scoped pass with checked sources. `reportable_activity_found` requires a verified claim; relevance still needs human/agent evidence review.

## Claims and sources

Use globally unique stable lowercase hyphenated IDs. Keep case identifiers from authorities/courts separately; do not invent them. Record one proceeding once, with multiple claims or country references as necessary. For a multi-country Commission claim, choose one affected country as the record owner and let the shared public-map entry reference its claim IDs. Other countries reference the shared entry rather than duplicating the claim. This ownership is storage only, not jurisdictional precedence.

Claim kinds are case, monitoring_activity, statistics and commission_proceeding. Record exact proposed text, authority_or_court, case_identifier (nullable), sectors, applicability (EAA/other_law/unknown), legal_basis, action_type, procedural_stage and stage_detail. Use stage_detail for exact Commission steps and conditions that do not fit the generic stage labels. Sectors use the canonical vocabulary/order in [presentation.md](presentation.md); empty means unestablished, not no sector applies.

Keep event_on, published_on and verified_on separate and nullable. These describe events/checks already observed and cannot be future dates. Future deadlines or conditional-penalty triggers belong in stage_detail with their source, not event_on. Record claim status as verified, disputed, unknown or unverified_source. Only verified claims have verified_on. Preserve uncertainty and next_check even when one aspect is verified.

Each source has url (nullable only for correspondence), source_type, reference (section/page or private-safe provenance reference), passage, attempted_on, retrieved_on, access_result and provenance_note. Access results are not_attempted, reachable, unreachable and unknown. Failed attempts do not create retrieval or verification dates. A verified claim requires a retrieved primary passage and section reference; this structural requirement does not decide whether that passage actually supports the wording. Correspondence and external reports preserve leads/provenance but cannot alone promote a new assertion to verified.

For statistics, set statistics to an object containing as_of, period, units, counting_basis and overlap_note. Otherwise use null. Explain whether categories overlap or whether this is unknown; do not infer totals. Individual cases and aggregate counts must remain distinct.

## Existing public entries and future edits

[baseline-map.json](baseline-map.json) freezes the setup's original row locations and SHA-256 fingerprints at its named main commit. Do not rewrite it after setup. [public-map.json](public-map.json) starts as the same mapping and tracks current rows. Hash the exact raw HTML row including its tr tags. Each entry has a stable id, affected countries, existing section heading, row_sha256, state, claim_ids and pinned snapshot_url. The checker compares every public data row against this map without requiring all countries on the public page.

Inherited entries start as `inherited_unreviewed` and must match their frozen baseline entry exactly. This exception preserves existing contributor material without calling it verified. It does not permit new unsupported text: any new or changed row must be mapped as `reviewed` with verified claim IDs and final review reports. The independent reviewer checks that every new factual assertion is supported; one verified ID cannot justify an unrelated addition to the same row. Retained unchanged legacy assertions in a mixed row must be identified explicitly in the review report rather than claimed verified. Add reciprocal public_entry_ids to affected country records. Remove stale current references when a public entry is deliberately removed, while preserving baseline history.

A fingerprint binds content to a record; it proves neither legal accuracy nor a completed review. Record language and PR outcomes under `reviews/` against the exact commit or text fingerprints. After a wording change, rerun affected reviews before updating fingerprints as reviewed. Do not relabel inherited entries merely to silence a failing check.

The frozen map is bound to the checker by a fixed checksum. An intentional baseline migration requires a separate reviewed infrastructure change; do not update that checksum to bypass an evidence review. The row-map check covers HTML data rows only. Prose outside tables and the substantive meaning of every change must be inspected by the independent PR reviewer.

The checker enforces claim references for reviewed rows, but final source-fidelity, readability and PR reports are a separate manual review gate in workflow.md. It does not automatically parse or certify those reports. Deliberate row removals also require PR review; absence from the current map cannot justify removing inherited contributor material.
