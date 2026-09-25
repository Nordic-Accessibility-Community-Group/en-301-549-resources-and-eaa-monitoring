# Quality-check improvements

## Added in this PR

- An isolated B2 readability reviewer receives the public page, without conversation history or research conclusions. Corrected wording gets a targeted recheck.
- A separate [PR reviewer](../../sanctions-pr.md) checks the actual GitHub diff and description. It can read evidence records, unlike the readability reviewer.
- A local consistency check validates the exact EU-27 list, seven table columns, area labels, dates, local links, source URL agreement, balanced table HTML and public-row fingerprints. Run `python3 .github/scripts/check-sanctions.py` from the repository root.
- Reports name the reviewed commit or content hash and state their limits. Structural checks, readability and legal verification have separate outcomes.

These extend the monitoring workflow's existing evidence and isolated language-fidelity checks. They do not replace those checks or add a scheduled automation or GitHub Actions workflow.

## Recommended next improvements

1. **Claim-level evidence records.** Give each financial or enforcement claim an ID, exact provision, short source passage, EAA category, operator type, conditions and evidence status. Link public claims to those IDs. The current country notes preserve history but cannot reliably prove that each amount has supporting evidence.
2. **Separate research and verification dates.** Use `attempted_on` for research attempts and `verified_on` only for claims actually checked. Track source retrieval separately, including final URL and failure reason. Do not infer successful access from the current `last_checked` date.
3. **A sanctions-specific schema.** Validate claim statuses, source types, currency, amount/range, turnover base, offence category, repeat offences and scope. Do not force sanctions into the monitoring-agency schema or populate missing legal details by inference.
4. **Boundary-focused evidence checks.** Prioritise distinctions that can change a result: administrative versus criminal fines, individual versus legal person, medium/large-company exceptions, product versus service scope, dates triggering repeat payments, and market withdrawal versus advertising restrictions.
5. **Version-bound review results.** Associate source-fidelity verdicts with exact publication wording and invalidate them when that wording changes. A stored fingerprint detects a changed row but does not establish legal correctness.
6. **Generated PR summaries.** Build file counts, completed-check results and links from the final diff and reports. Keep human-written explanations for unresolved legal questions. This would prevent stale scope claims in descriptions.

Implement claim-level records and dates before adding automatic publication gates. Otherwise a gate could mistake migrated notes or located sources for verified evidence.
