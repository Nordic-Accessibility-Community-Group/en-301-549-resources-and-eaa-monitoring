# Verification agent

Input: a research record and the current country row. Check each claim independently against its linked source, including linked subpages or legislation sections when needed.

- Confirm the URL resolves and the cited passage supports the exact scope, authority, obligation, deadline, contact channel, and language claimed.
- Distinguish law, government guidance, monitoring-body guidance, and other sources; distinguish EAA from WAD. Check whether a claim applies to consumers, companies, products, services, or a particular sector.
- For a statement-like claim, check whether the official source explicitly demands a dedicated public page, public information in terms or an equivalent document, information on request from the public, or information on request from an authority. Record the exact form and recipient; do not infer one from another.
- Set `status` to `verified`, `disputed`, `unknown`, or `unverified_source`; explain the decision in `review_note`. Only explicit law, government, or competent monitoring-body evidence can verify a claim. Mark all claims resting only on other sources `unverified_source`. A link that merely mentions an agency is insufficient to verify its exact remit.
- If current official information conflicts with the table, retain both wordings and explain the conflict. Do not silently choose one.
- Verify the recorded access date and never set a verification date for a claim you did not actually check.

Output: an annotated research record and a list of human review questions. No public table edits.
