# Monitoring information agent prototype

These instructions govern experiments on `monitoring-agencies-information.md`. Run the four stages in order: research, independent verification, presentation, and draft PR preparation. A person reviews the evidence and diff before merging.

The pilot covers **Denmark and Sweden** as audits of fuller existing entries, and **Bulgaria and Hungary** as research into incomplete entries. Apply the same research and verification checklist to all four countries; the difference is how much existing content needs checking. Do one country per research PR so reviewers can assess each set of sources. Keep research notes under `.github/agents/research/` during the pilot, using the schema in `.github/agents/country-record.schema.json`. The visible country table stays in its current location.

The file `.github/scripts/check-verification-dates.py` validates dates for the events calendar. Do not change it or depend on it to verify this country research. Evidence review is a separate manual gate in this pilot.

## Common rules

- Prefer current primary sources: legislation, official gazettes, competent authorities, and government guidance. Record the exact URL and the date accessed for each claim.
- Keep European Accessibility Act (EAA) product and service duties separate from Web Accessibility Directive (WAD) public sector duties. An EAA service information obligation is not automatically a WAD-style accessibility statement. Record an authority's scope; do not assume one agency covers all sectors.
- For every country, research whether a government or competent monitoring body explicitly requires a public page comparable to a WAD accessibility statement, permits information in terms or another public document, makes it available to the public on request, or requires submission to an authority on request. Record each audience and delivery mode separately. A law alone does not establish a regulator's publication practice.
- Mark a claim `verified` only when explicit law, government, or competent monitoring-body text supports the exact claim. Other sources can be retained as leads with `source_type: other_unverified` and `status: unverified_source`; never publish their claim as established fact.
- Preserve existing Yes/No answers and contributor-supplied details unless explicit official evidence shows they are wrong. Some entries come from agency emails or personal contact and may lack public URLs. Record the claimed provenance or missing correspondence in `review_note`, seek the original evidence from the contributor, and distinguish it from independently checked public sources. Lack of a public source alone does not justify replacing an existing answer.
- Use `verified`, `disputed`, `unknown`, or `unverified_source` for each claim. `Unknown` means the research did not establish an answer, not that an obligation or reporting route does not exist.
- A verified reporting claim must identify the competent authority, its relevant sector, and at least one current official reporting route: a direct form, an accepted email address, or a postal/in-person address. A statutory right to complain without a usable route belongs in research notes, not the table's reporting cell. Verify whether a general form is intended for the relevant complaint; flag any uncertainty.
- Never invent legal interpretations, reporting channels, accepted languages, or deadlines. Escalate ambiguous translations and conflicting official sources for human review.
- Record the primary evidence in the research file before editing the table. Do not merge a PR or present a finding as legal advice.

## Baseline checks for every country

For each country, check and record a result (including `unknown` when unsupported) for: EAA scope and the relevant law; a dedicated public page comparable to a WAD statement; EAA information in terms or another public document; information available to the public on request; information supplied to an authority on request; responsible authorities with sector scope; whether the listed monitoring agencies cover every relevant product and service sector; whether each existing authority link points to the correct official agency website or relevant official page; public complaints; and company reporting. Check any existing extra claims, such as languages, deadlines, and contact details. Country-specific questions add to this baseline and never replace it.

## Pilot order

1. Copy the blank record at `.github/agents/research/template.json` for a country. Capture each existing table assertion as a claim, then find official evidence independently.
2. Apply `research.md` and then `verification.md`. A second pass checks URLs and whether each source actually supports the wording.
3. Apply `presentation.md` to the verified record. Keep the five existing columns and propose only supported changes.
4. Apply `pr.md` to prepare a branch, diff, and draft PR. Include disputed and unknown claims as review questions instead of filling gaps by inference.
5. Compare audit outcomes for Denmark and Sweden with the discovery outcomes for Bulgaria and Hungary. Review accuracy, source coverage, unresolved questions, and the readability of proposed rows before changing the schema or automating the process.
