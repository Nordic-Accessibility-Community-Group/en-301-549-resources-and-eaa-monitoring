# Monitoring information agent prototype

These instructions govern experiments on `monitoring-agencies-information.md`. Run research, evidence verification, presentation, a separate language-fidelity check, and draft PR preparation in that order. A person reviews the evidence and diff before merging.

The pilot covers **Denmark, Sweden and Finland** as audits of fuller existing entries, and **Bulgaria and Hungary** as research into incomplete entries. Apply the same research and verification checklist to all five countries; the difference is how much existing content needs checking. Do one country per research PR so reviewers can assess each set of sources. Keep research notes under `.github/agents/research/` during the pilot, using the schema in `.github/agents/country-record.schema.json`. The visible country table stays in its current location.

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
4. Run the separate agent in `language-verification.md` on the proposed publication wording as described below. Apply corrections and have the corrected passages rechecked before PR preparation.
5. Apply `pr.md` to prepare a branch, diff, and draft PR. Include disputed and unknown claims as review questions instead of filling gaps by inference.
6. Compare audit outcomes for Denmark, Sweden and Finland with the discovery outcomes for Bulgaria and Hungary. Review accuracy, source coverage, unresolved questions, and the readability of proposed rows before changing the schema or automating the process.

## Separate language check for every country

Apply the same rule to every source language; do not require a fluent human reviewer by default. Translated claims and meaning-sensitive paraphrases receive a separate language-fidelity check after presentation, including wording shortened for the table.

The orchestrator starts a separate agent with no conversation-history fork (for example, `fork_turns="none"`). Give it only the neutral brief in `language-verification.md`, source passages with enough surrounding context and cross-references, source URLs/sections, and proposed publication wording. Do not pass research instructions, prior conclusions, evidence statuses, desired verdicts, PR comments or reasons for the proposed change. The language agent may retrieve source context; it must not inspect the research record or repository workflow. If isolation is unavailable, record the check as not performed; do not label a same-context self-review as separate.

Record the original excerpts, literal renderings, exact reviewed wording, verdicts and agent/date in the relevant claim's existing `review_note`, with public source references in `sources`. Keep comparisons in research records, not the public table. Language verdicts (Supported / Correction needed / Ambiguous) are distinct from claim evidence statuses.

Apply corrections and recheck the final changed wording. A material unresolved ambiguity is a Before PR issue: surface it immediately and resolve, narrow or omit the affected addition. Ask a human or authority a precise question only when needed; do not impose a blanket language-review gate. Do not send correspondence without authorization. Ordinary supported wording can proceed to maintainer review with the comparison available. Missing checks or budget expiry must be reported honestly; preserve existing contributor entries under the common rules.

A separate AI language check is not independent human verification, legal advice or proof that the authority list is complete. Evidence verification and maintainer approval remain separate. All passes share the existing research budget.

## Surface manual checks immediately

Apply this rule at every stage, as soon as an issue is discovered. Do not wait until the research ends or a PR is opened to tell the user about a concrete check that affects the proposed change.

Separate findings into:

- **Before PR:** a missing check could make a proposed table addition or correction inaccurate. Examples include an ambiguous translation that determines an authority's remit, a reporting form whose intended audience is unconfirmed, conflicting official evidence, or shortened wording that overstates its source.
- **Before merge:** the proposed wording has supporting evidence and no unresolved accuracy blocker, but a specific human review is still required. This must not be used to defer an unresolved Before PR issue.
- **Follow-up:** an unknown does not affect the supported changes being proposed, such as another sector's missing reporting route or a future process update. Keep it in research notes; it does not block unrelated work.

Immediately show Before PR items to the user as an unchecked checklist. Each item must identify the country and exact claim/cell, the uncertainty and its consequence, the specific action or evidence needed, who can resolve it (agent or contributor/reviewer), and what will count as resolved. Avoid vague requests such as "review translations" or "check legal scope."

Resolve agent-checkable issues within the existing research budget. Continue unrelated supported work. If human input is necessary, ask the concrete question immediately. Do not include the affected assertion in a PR until resolved; alternatively, omit or narrow that proposed addition and record why. Preserve existing manually gathered entries under the common rules.

Record the classification in the existing `questions` strings using `Before PR:`, `Before merge:`, or `Follow-up:`, with supporting detail in `review_note`. These priorities do not replace claim evidence statuses. Missing public confirmation alone is not a blocker for preserving a contributor-supplied entry. Do not manufacture blockers for every unknown.

## Research limits and evidence handling

Apply these checks to every country. Record authority remit and coverage separately from link reachability. An indexed search result can identify an official source, but does not establish that its URL opens successfully. Keep the URL, check date, final destination where available, and link outcome (`reachable`, `unreachable`, `unknown`, or `missing`) in `review_note`; these are link outcomes, not replacements for the claim's evidence status.

Separate consumer complaints, company non-compliance reports, and exemption notifications. Check the intended audience, sector, accepted languages, login requirements, and any officially stated deadline for each route. Record shared or delegated authority responsibilities and their boundaries. For requirements and guidance, record their legal status, effective date, and any sector-specific transition period.

Preserve contributor evidence from agency email or personal contact. Record its provenance and date when available, and flag missing public confirmation for review. Do not remove existing information merely because a public source cannot be found, or publish private correspondence or personal contact details without authorization.

Unless the user specifies another budget, allow at most two access attempts per failing URL (the initial attempt and one retry), two targeted follow-up searches per unresolved question, ten minutes of research and verification per country, and thirty minutes across a multi-country run. Stop when the first applicable limit is reached. Do not restart a budget on handoff between stages. Record unresolved checks as `unknown`, give the reason and next useful step in research feedback, and complete the handoff with the evidence already gathered. A failed URL does not by itself invalidate separately verified remit evidence. Never mark a country fully checked when required checks remain unfinished. Preparing the record and draft PR may continue after the research cutoff; further searching must wait for a new run.
