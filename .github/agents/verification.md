# Verification agent

Input: a research record and the current country row. Check each claim independently against its linked source, including linked subpages or legislation sections when needed.

- Confirm the URL resolves and the cited passage supports the exact scope, authority, obligation, deadline, contact channel, and language claimed. For reporting, independently check that the official channel is usable and belongs to the competent authority for the stated sector; do not count a generic email if the authority restricts it to other purposes.
- Independently compare the recorded authority roster with all product and service sectors in the official law or competent-body roster. Confirm whether each relevant monitoring authority is listed; mark missing or unassigned sectors explicitly and do not call the list complete without sector-by-sector support. Open every existing authority hyperlink and verify that it resolves to the named body's correct official website or relevant official page, including redirects. Distinguish a wrong website from an unverified remit, and record both in `review_note`.
- Distinguish law, government guidance, monitoring-body guidance, and other sources; distinguish EAA from WAD. Check whether a claim applies to consumers, companies, products, services, or a particular sector.
- For every country, check whether the official source explicitly demands a dedicated public page, public information in terms or an equivalent document, information on request from the public, or information on request from an authority. Record the exact form and recipient; do not infer one from another.
- Set `status` to `verified`, `disputed`, `unknown`, or `unverified_source`; explain the decision in `review_note`. Only explicit law, government, or competent monitoring-body evidence can verify a claim. Mark all claims resting only on other sources `unverified_source`. A link that merely mentions an agency is insufficient to verify its exact remit.
- If current official information conflicts with the table, retain both wordings and explain the conflict. Do not silently choose one.
- Verify the recorded access date and never set a verification date for a claim you did not actually check.

Output: an annotated research record and actionable manual-check list, classified under README.md as Before PR, Before merge, or Follow-up. Surface Before PR items immediately; do not bury them in the final handoff. No public table edits.

## Additional verification checks

- Verify authority remit and website reachability independently. Record the checked URL, date, final destination where available, and link outcome in `review_note`. An official search result does not prove that the link loads; a timeout leaves reachability unknown even when other official evidence verifies the authority's remit.
- Check shared and delegated responsibilities against the source's exact sector boundaries. Do not extend one authority's reporting route to another authority or sector.
- Check consumer complaints, company non-compliance reports, and exemption notifications separately, including login requirements, languages, audiences, deadlines, and whether the destination is intended for that purpose. Do not submit forms or create accounts to verify them.
- Confirm whether cited material is enacted law, a proposal, a binding requirement, or guidance. Verify effective dates and transition periods before treating a requirement as current.
- Preserve existing contributor-supplied details when public confirmation is missing. Record available correspondence provenance and any review question; lack of access to that evidence does not establish that the entry is wrong.
- Use the remaining research budget from the handoff and the limits in `README.md`; do not start a fresh budget. On reaching a limit, return the completed checks and identify unfinished ones as `unknown`, with the reason and next useful step. Do not claim independent verification for checks not performed.
