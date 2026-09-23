# Research agent

Input: one of Denmark, Sweden, Bulgaria, Hungary; the current row in `monitoring-agencies-information.md`; a blank country record.

1. Split the existing row into atomic assertions about EAA service information, any public page comparable to a WAD accessibility statement, information available to the public in another document, information supplied to a regulator on request, authorities and their sector scopes, consumer reporting, company reporting, and additional information.
2. Search for an explicit government or competent monitoring-body instruction about the form, audience, and location of the EAA information. Do not infer a public page from a law's general information duty, a WAD statement on an authority's own website, or the mere existence of a company's page. Check the existing fuller entries for Denmark and Sweden and incomplete entries for Bulgaria and Hungary with the same rule.
3. Write one claim per item in `.github/agents/research/<country>.json`. Include precise evidence URLs, short paraphrases or section references, access date, jurisdiction, directive context, and unresolved translation questions. Use `unknown` where evidence is absent.
4. Classify every source by type. Keep secondary or other sources only as `other_unverified` leads with `status: unverified_source`, clearly separate from evidence that can verify a claim. Hand off the record without editing the public table.

Output: structured claims with provenance and questions for verification.
