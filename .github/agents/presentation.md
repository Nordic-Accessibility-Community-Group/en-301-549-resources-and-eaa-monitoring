# Presentation agent

Input: verified country record, current row, and human review decisions where needed.

Propose a focused edit to that country's row in `monitoring-agencies-information.md`. Preserve the five existing columns, HTML table structure, accessible link text, and useful local names. Group agencies by their supported sector remits and distinguish public reporting from company obligations. Each published reporting claim must name its authority and relevant sector and link a concrete form or give a verified email/postal/in-person address. Mark other sectors unknown until a route is found. Place direct official sources near the claims they support.

Preserve existing Yes/No values and manually gathered entries unless explicit official evidence shows an error; document missing source provenance in the research record and PR. Keep detailed conclusions and context in the research record or PR feedback; add only essential reader-facing context to the last column, without replacing the existing answer. Only add new factual text supported by a `verified` claim from law, government, or a competent monitoring body. A legal right to report without a verified usable route is insufficient for the reporting cell. Do not put an `unverified_source` claim into the table as fact; it may appear in a clearly labelled PR review note. In the “Demands statement” cell, retain an existing answer unless official evidence shows it is wrong. Distinguish comparable public pages, other public documents, and information available on request in the research record; add a brief clarification to the last column only when needed to understand the table. For a new entry with no existing Yes/No, use `❓ Unknown` when the answer is unverified; keep the explanation in the research record and PR. If another field remains unresolved, use the same concise convention. Do not convert absence of evidence into “No.” If evidence contradicts an existing claim, surface that explicitly for the reviewer. Keep changes to other countries out of the diff.

For every listed jurisdiction, use the last column for a short `⚖️ EAA implementing law:` label and a descriptive link to the official national text. Place content outside an existing `<ul>` list in its own `<p>` element; do not use `<br>` to separate it. Cite more than one instrument when implementation is split by sector. If local implementation is not established or the jurisdiction is outside the EU/EEA, label that status explicitly, give an official applicability source where available, and do not present a draft or the EU directive itself as a local implementing law. Keep this reference separate from the statement Yes/No cell. An emoji supplements text; it never carries the meaning alone.

## Keep the page table minimal

- Publish only the concise information readers need: the authority and sector, a usable reporting route, relevant reporting languages, and the implementing-law link.
- Put a supported language statement such as “PTS accepts reporting in English 🇬🇧” in the reporting column. Do not repeat it in Additional information.
- Keep evidence excerpts, correspondence dates and provenance, verification history, detailed qualifications, monitoring-process descriptions, and unresolved research questions in `.github/agents/research/<country>.json` or PR feedback.
- Do not add explanatory reporting paragraphs to Additional information merely because new evidence was found. Keep that column to useful links, the law reference, and essential brief context.
- Retain a short scope or prerequisite when omitting it would make an entry misleading. Concision must not broaden a claim beyond its evidence.
- Before handing off, remove repetition and research narration from the proposed row. Preserve useful manually gathered information and existing Yes/No answers under the rules above.

Output: proposed row diff, source-to-claim mapping, and unresolved presentation questions. Any alternative layout suggestion belongs in the PR description and must not trigger an unrelated table redesign.

## Language handoff

Send the final proposed translated or meaning-sensitive wording, source passages and section references to the isolated language check specified in `README.md`. Keep research conclusions out of that handoff. Apply supported corrections without expanding the public table with translation commentary. Recheck changed passages after shortening or correction; retain exact comparisons in the country record.

## Consistent sector structure in both columns

Use the same sector-first structure in Monitoring agencies and Reporting tools for every country. Use these shared labels where applicable: Products, E-commerce, Banking, Electronic communications, Transport, Audiovisual access, E-books, and 112 emergency calls. Country-specific subcategories add precision beneath a label rather than replace the common vocabulary.

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
