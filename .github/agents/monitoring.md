# Monitoring agencies specification

Follow [workflow](workflow.md), [evidence](evidence.md) and [review](review.md). Publication: monitoring-agencies-information.md. Country records use research/countries/<country>.json, domains.monitoring; read the [shared storage contract](research/README.md). The [monitoring schema](country-record.schema.json) validates the expanded domain view. Use one-country drafts titled `Audit <country> EAA authorities and reporting routes`; keep at most one monitoring research PR open. Shared evidence handoffs may update other relevant research records without broadening the public edit. New country research requires explicit authorisation; historical five-country pilots do not authorise automatic rollout.

## Research and verification checklist

Research collects these items; verification independently checks the same items against their sources, records conflicts and scope, and uses the remaining shared budget. Record an answer, including unknown, for every baseline check. Fuller existing rows do not reduce the checklist.

1. Split the existing row into atomic assertions. Independently research every baseline check, even when the current row is silent. Record separate claims for a dedicated public page, other public document, public on-request access, and authority on-request submission; do not treat these as interchangeable.
2. Search for an explicit government or competent monitoring-body instruction about the form, audience, and location of the EAA information. Do not infer a public page from a law's general information duty, a WAD statement on an authority's own website, or the mere existence of a company's page. Add country-specific questions when local law or agencies require them.
3. Audit the Monitoring agencies column against the implementing law and official government or competent-body rosters. Map every covered product and service sector to its responsible monitoring authority, then compare that map with every agency already listed. Record missing agencies, unsupported sector assignments, and sectors whose authority is still unknown. Open each existing agency link and check that it resolves to the named authority's correct official website or relevant official page, including redirects; flag missing, outdated, or incorrect links separately from the authority's remit. Record one `authority` claim per authority and sector, plus a coverage conclusion and outstanding gaps in `review_note` or `questions`. Do not treat a partial roster as complete.
4. For each reporting claim, find the competent authority's own current instructions and a concrete form URL, accepted email address, or postal/in-person address. State the sector and whether the route is explicitly for EAA complaints or a general complaint channel. Do not use a contact email when the authority directs the public elsewhere.
5. Write one claim per item in `domains.monitoring` in `.github/agents/research/countries/<country>.json`. Include precise evidence URLs, short paraphrases or section references, access date, jurisdiction, directive context, and unresolved translation questions. Use `unknown` where evidence is absent.
6. Classify every source by type. Keep secondary or other sources only as `other_unverified` leads with `status: unverified_source`, clearly separate from evidence that can verify a claim. Hand off the record without editing the public table.


Also distinguish shared/delegated authority boundaries, link reachability versus remit, route audiences/purposes, accepted languages, login conditions and officially stated deadlines. Confirm enactment/effective dates and transition periods. Preserve correspondence provenance and existing contributor entries under shared evidence rules. Do not call a partial authority roster complete. Schema fields and free-text review_note/questions retain exact evidence and Before PR / Before merge / Follow-up priorities.

## Presentation



Propose a focused edit to that country's row in `monitoring-agencies-information.md`. Preserve the five existing columns, HTML table structure, accessible link text, and useful local names. Group agencies by their supported sector remits and distinguish public reporting from company obligations. Each published reporting claim must name its authority and relevant sector and link a concrete form or give a verified email/postal/in-person address. Mark other sectors unknown until a route is found. Place direct official sources near the claims they support.

Preserve existing Yes/No values and manually gathered entries unless explicit official evidence shows an error; document missing source provenance in the research record and PR. Keep detailed conclusions and context in the research record or PR feedback; add only essential reader-facing context to the last column, without replacing the existing answer. Only add new factual text supported by a `verified` claim from law, government, or a competent monitoring body. A legal right to report without a verified usable route is insufficient for the reporting cell. Do not put an `unverified_source` claim into the table as fact; it may appear in a clearly labelled PR review note. In the “Demands statement” cell, retain an existing answer unless official evidence shows it is wrong. Distinguish comparable public pages, other public documents, and information available on request in the research record; add a brief clarification to the last column only when needed to understand the table. For a new entry with no existing Yes/No, use `❓ Unknown` when the answer is unverified; keep the explanation in the research record and PR. If another field remains unresolved, use the same concise convention. Do not convert absence of evidence into “No.” If evidence contradicts an existing claim, surface that explicitly for the reviewer. Keep changes to other countries out of the diff.

For every listed jurisdiction, use the last column for a short `⚖️ EAA implementing law:` label and a descriptive link to the official national text. Place content outside an existing `<ul>` list in its own `<p>` element; do not use `<br>` to separate it. Cite more than one instrument when implementation is split by sector. If local implementation is not established or the jurisdiction is outside the EU/EEA, label that status explicitly, give an official applicability source where available, and do not present a draft or the EU directive itself as a local implementing law. Keep this reference separate from the statement Yes/No cell. An emoji supplements text; it never carries the meaning alone.

## Keep the page table minimal

- Publish only the concise information readers need: the authority and sector, a usable reporting route, relevant reporting languages, and the implementing-law link.
- Put a supported language statement such as “PTS accepts reporting in English 🇬🇧” in the reporting column. Do not repeat it in Additional information.
- Keep evidence excerpts, correspondence dates and provenance, verification history, detailed qualifications, monitoring-process descriptions, and unresolved research questions in `domains.monitoring` in `.github/agents/research/countries/<country>.json` or PR feedback.
- Do not add explanatory reporting paragraphs to Additional information merely because new evidence was found. Keep that column to useful links, the law reference, and essential brief context.
- Retain a short scope or prerequisite when omitting it would make an entry misleading. Concision must not broaden a claim beyond its evidence.
- Before handing off, remove repetition and research narration from the proposed row. Preserve useful manually gathered information and existing Yes/No answers under the rules above.

Output: proposed row diff, source-to-claim mapping, and unresolved presentation questions. Any alternative layout suggestion belongs in the PR description and must not trigger an unrelated table redesign.


## Consistent sector structure in both columns

Use the same sector-first structure in Monitoring agencies and Reporting tools for every country. Use the canonical sector labels/order in [registry.json](registry.json). Country-specific subcategories add precision beneath a label rather than replace the common vocabulary.

In Monitoring agencies, use `<p><strong>Sector:</strong></p>` followed by a `<ul>` of responsible authorities linked to their verified official websites. An authority name alone is insufficient unless its sector heading states the full relevant remit. Add only essential scope limits or delegation details to each list item. Preserve local names. Do not imply every authority listed under a sector supervises the entire sector; retain banking subsets, transport elements, product boundaries and delegated responsibilities. Clearly distinguish statutory authority classes from identified offices.

In Reporting tools, use matching sector labels, identify the responsible authority and use the audience-and-purpose labels below. Preserve channel prerequisites, relevant languages and existing contributor information. When all channels for a sector are unestablished, use one concise `Public and company reporting: ❓ Unknown.` item. Unknown authority and unknown reporting channel are different findings.

Group sectors only when they share the listed authority or reporting routes; otherwise list them separately. A shared channel never expands an authority's remit. Prefer grouping over repeated long addresses, but keep sector-to-authority mapping explicit. Use paragraph labels and lists, never `<br>`. Keep evidence narration in research notes/PR feedback.

Check both columns against the recorded sector-to-authority mapping before handoff. Reusing existing supported names and scopes is a layout change; new, translated or meaning-sensitive scope wording still requires the evidence and isolated language checks. An unknown channel must not erase a known authority.

## Shared audience-and-purpose labels

Use `Public` or `Company` plus the purpose for every established reporting route:

- `Public complaints:` for complaint procedures.
- `Public reports:` for barrier or suspected non-compliance reports; do not imply a formal complaint procedure.
- `Public enquiries:` for consultations and questions, distinct from complaints or statutory filings.
- `Public enforcement requests:` for a distinct formal enforcement procedure; preserve eligibility conditions.
- `Company non-compliance:` for companies reporting their own non-compliance.
- `Company exemptions:` for exemption notifications.
- `Company non-compliance / exemptions:` only when the same verified route supports both purposes.

Keep sector and authority headings above the routes. Put a narrower scope in parentheses when needed. Put the form, email or postal channel after the purpose label, not in place of it. Use `Public and company reporting: ❓ Unknown.` when all routes are unestablished; this does not establish applicability or a reporting obligation. Where some purposes are known, show unknown purposes separately.

Do not infer audience or statutory purpose from a general contact address or a form title alone. Preserve contributor-supplied generic reporting entries while recording the exact missing classification as a research follow-up. `Company reporting email:` and `Company reports:` are temporary broad labels when company reporting is established but its precise purpose is not. Do not turn them into non-compliance or exemption routes without evidence. Keep source-specific eligibility in research and any essential restriction in the table; Public/Company navigation labels are not exhaustive legal definitions.

This vocabulary supersedes the former bare `Exemptions:` label. Keep historical source excerpts and review records intact; they describe the wording reviewed at that time.

## Shared exemption label

Use exactly `Company exemptions:` as the standalone reporting label for every country, or `Company non-compliance / exemptions:` for a verified shared route. Do not append wording such as “invoking derogation grounds” to the label. Keep the nature, conditions and scope of the local notification route in the research record. The shared legal reference is [EAA Article 14](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019L0882) (fundamental alteration and disproportionate burden), particularly Article 14(8) for notification to authorities. That notification provision excludes microenterprises; do not infer a universal filing obligation. The EAA reference does not replace the national implementing law or official evidence of a usable local channel.

## One-time post-draft route check



After opening a draft country research PR, the separate PR-opened research task checks that it is an open draft country PR and reads the PR description, the country research record and these instructions. It reruns only concrete unfinished checks that an agent can perform, especially official URLs and intake forms that failed in a text reader. For portal or session errors, make at most one fresh ordinary-browser attempt per destination; observe the relevant form and login condition without submitting, signing in, or creating an account. Check the authority, sector, audience, purpose and exact official source before marking a route verified. The pass happens after the initial bounded research stage and does not reset that stage's attempt history.

Record each result and date in the same research record and draft PR. If an official route is confirmed, update only that country's concise row and rerun isolated no-history language review and targeted structural checks when its wording changes. If it remains inaccessible or its purpose is uncertain, keep the table value Unknown and state the exact remaining check in the research record and PR. Preserve existing Yes/No and contributor correspondence unless explicit official evidence warrants correction. Never submit a report, send messages, change workflows or the events-calendar date script, open a second country PR, or merge a PR.

Run this pass once for a newly opened draft. Commit and comment events and a change from draft to ready for review must not repeat it. For a draft that predates the automated trigger, perform the same pass once manually.


This separate follow-up pass remains bounded by the shared ten-minute-country/thirty-minute-run limits. Its explicit extra access allowance is at most one fresh ordinary-browser attempt per previously failed destination; retain the initial attempt history. Do not recursively trigger another pass on its commits or treat it as a new-country authorisation.
