# Draft PR agent

Input: reviewed research record and the proposed one-country row diff.

1. Confirm the PR changes only that country's row and its research record. Check the diff against the record and check that each new factual assertion has primary evidence.
2. Run the repository's existing content checks. Do not alter `.github/scripts/check-verification-dates.py`; it is used for the events calendar and does not certify this research.
3. Open a **draft** PR against this testing repository. Never push directly to `main`, enable auto-merge, or merge the PR.
4. In the description, name the country and whether this is a fuller-entry audit (Denmark/Sweden) or incomplete-entry research (Bulgaria/Hungary). List official sources, access dates, verified changes, unknown or disputed claims, and check results. Request human review of legal scope and translations.

An infrastructure PR may contain only `.github/agents/` instructions and schema; country data belongs in later one-country PRs.
