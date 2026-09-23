# Research agent

Input: one of Denmark, Sweden, Bulgaria, Hungary; the current row in `monitoring-agencies-information.md`; a blank country record.

1. Split the existing row into atomic assertions about statement requirements, authorities and their sector scopes, consumer reporting, company reporting, and additional information.
2. Research each assertion using official sources in the relevant language. Search for missing fields, especially Bulgaria's source for the statement claim and reporting route, and Hungary's statement and reporting fields. Audit the fuller Denmark and Sweden rows with equal skepticism.
3. Write one claim per item in `.github/agents/research/<country>.json`. Include precise evidence URLs, short paraphrases or section references, access date, jurisdiction, directive context, and unresolved translation questions. Use `unknown` where evidence is absent.
4. Hand off the record without editing the public table. Do not copy a secondary source as if it were official evidence.

Output: structured claims with provenance and questions for verification.
