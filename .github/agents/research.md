# Research agent

Input: one pilot country; its current row in `monitoring-agencies-information.md`; a blank country record. Apply the baseline checklist in `README.md` to every country, including fuller entries.

1. Split the existing row into atomic assertions. Independently research every baseline check, even when the current row is silent. Record separate claims for a dedicated public page, other public document, public on-request access, and authority on-request submission; do not treat these as interchangeable.
2. Search for an explicit government or competent monitoring-body instruction about the form, audience, and location of the EAA information. Do not infer a public page from a law's general information duty, a WAD statement on an authority's own website, or the mere existence of a company's page. Add country-specific questions when local law or agencies require them.
3. Write one claim per item in `.github/agents/research/<country>.json`. Include precise evidence URLs, short paraphrases or section references, access date, jurisdiction, directive context, and unresolved translation questions. Use `unknown` where evidence is absent.
4. Classify every source by type. Keep secondary or other sources only as `other_unverified` leads with `status: unverified_source`, clearly separate from evidence that can verify a claim. Hand off the record without editing the public table.

Output: structured claims with provenance and questions for verification.
