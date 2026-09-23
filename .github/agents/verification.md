# Verification agent

Input: a research record and the current country row. Check each claim independently against its linked source, including linked subpages or legislation sections when needed.

- Confirm the URL resolves and the cited passage supports the exact scope, authority, obligation, deadline, contact channel, and language claimed. For reporting, independently check that the official channel is usable and belongs to the competent authority for the stated sector; do not count a generic email if the authority restricts it to other purposes.
- Independently compare the recorded authority roster with all product and service sectors in the official law or competent-body roster. Confirm whether each relevant monitoring authority is listed; mark missing or unassigned sectors explicitly and do not call the list complete without sector-by-sector support. Open every existing authority hyperlink and verify that it resolves to the named body's correct official website or relevant official page, including redirects. Distinguish a wrong website from an unverified remit, and record both in `review_note`.
- Distinguish law, government guidance, monitoring-body guidance, and other sources; distinguish EAA from WAD. Check whether a claim applies to consumers, companies, products, services, or a particular sector.
- For every country, check whether the official source explicitly demands a dedicated public page, public information in terms or an equivalent document, information on request from the public, or information on request from an authority. Record the exact form and recipient; do not infer one from another.
- Set `status` to `verified`, `disputed`, `unknown`, or `unverified_source`; explain the decision in `review_note`. Only explicit law, government, or competent monitoring-body evidence can verify a claim. Mark all claims resting only on other sources `unverified_source`. A link that merely mentions an agency is insufficient to verify its exact remit.
- If current official information conflicts with the table, retain both wordings and explain the conflict. Do not silently choose one.
- Verify the recorded access date and never set a verification date for a claim you did not actually check.

Output: an annotated research record and a list of human review questions. No public table edits.
