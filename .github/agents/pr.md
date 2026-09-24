# Draft PR agent

Input: reviewed research record and the proposed one-country row diff.

1. Confirm the PR changes only that country's row and its research record. Check the diff against the record and check that each new factual assertion has primary evidence.
2. Review the actual proposed table diff against the evidence, including any wording shortened during presentation. Apply the Before PR gate in `README.md`: resolve, omit, or narrow affected new assertions before opening the PR. List any concrete manual check immediately when discovered.
3. Run the repository's existing content checks. Do not alter `.github/scripts/check-verification-dates.py`; it is used for the events calendar and does not certify this research.
4. Open a **draft** PR against this testing repository. Never push directly to `main`, enable auto-merge, or merge the PR.
5. In the description, name the country, show the result of each baseline check from `README.md`, and list any additional country-specific questions. List official sources, access dates, verified changes, unknown or disputed claims, and check results. Request ordinary maintainer review of the evidence and diff. Require specialist language input only for a specific unresolved ambiguity; follow the Before PR gate rather than deferring it to merge.

An infrastructure PR may contain only `.github/agents/` instructions and schema; country data belongs in later one-country PRs.

## Required review information in the PR

Put a **Manual checks before merge** checklist near the top of the description, before the detailed evidence. Include only concrete checks required for this diff, with the exact claim/cell, reviewer action, evidence link or correspondence reference, and completion criterion. If none remain, state "None identified." Keep the ordinary human review requirement; do not invent extra checks.

Use this item format:

- [ ] Country / exact claim or cell — required action; why it matters; evidence/reference; owner; resolved when: observable result.

Report the **Before PR checks** separately as resolved or as proposed assertions omitted/narrowed. Never imply an omitted assertion was verified. If a Before PR blocker is discovered after opening a draft, surface it immediately and correct or remove the affected addition before continuing review.

Put **Non-blocking follow-up** in a separate section, with a link to the research record. Do not mix it into the required checklist or imply that every unknown must be resolved before merging. Mark a checklist item complete only after the required evidence or reviewer confirmation exists.

## Language-check result

Include a Language verification section linking the country record's source-to-wording comparison. Name the source/publication languages, date, separate-agent context isolation, exact scope, verdicts, corrections and any unreviewed passages. Report whether corrected final wording was rechecked. Do not mark a human-review checkbox complete based on an AI result: replace superseded blanket language-review items with the actual result and any remaining concrete action. A Supported result permits ordinary maintainer review; it does not approve or merge the PR. Checklist completion requires a recorded resolution, not just a tick.
