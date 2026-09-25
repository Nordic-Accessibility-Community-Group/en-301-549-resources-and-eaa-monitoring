# Draft PR agent

Input: reviewed research record and the proposed one-country row diff.

1. Confirm the PR changes only that country's row and its research record. Check the diff against the record and check that each new factual assertion has primary evidence.
2. Review the actual proposed table diff against the evidence, including any wording shortened during presentation. Apply the Before PR gate in `README.md`: resolve, omit, or narrow affected new assertions before opening the PR. List any concrete manual check immediately when discovered.
3. Run the repository's existing content checks. Do not alter `.github/scripts/check-verification-dates.py`; it is used for the events calendar and does not certify this research.
4. Open a **draft** PR against this testing repository. Never push directly to `main`, enable auto-merge, or merge the PR.
5. In the description, name the country, show the result of each baseline check from `README.md`, and list any additional country-specific questions. List official sources, access dates, verified changes, unknown or disputed claims, and check results. Request ordinary maintainer review of the evidence and diff. Require specialist language input only for a specific unresolved ambiguity; follow the Before PR gate rather than deferring it to merge.

An infrastructure PR may contain `.github/agents/` instructions, schema, watcher helpers, source inventory and operational baseline observations. It must not change country research claims or table rows. Follow `watcher/README.md` for operational state on the dedicated testing-repository branch. Country data changes belong in separate one-country PRs.

## Required review information in the PR

Put a **Manual checks before merge** checklist near the top of the description, before the detailed evidence. Include only concrete checks required for this diff, with the exact claim/cell, reviewer action, evidence link or correspondence reference, and completion criterion. If none remain, state "None identified." Keep the ordinary human review requirement; do not invent extra checks.

Use this item format:

- [ ] Country / exact claim or cell — required action; why it matters; evidence/reference; owner; resolved when: observable result.

Report the **Before PR checks** separately as resolved or as proposed assertions omitted/narrowed. Never imply an omitted assertion was verified. If a Before PR blocker is discovered after opening a draft, surface it immediately and correct or remove the affected addition before continuing review.

Put **Non-blocking follow-up** in a separate section, with a link to the research record. Do not mix it into the required checklist or imply that every unknown must be resolved before merging. Mark a checklist item complete only after the required evidence or reviewer confirmation exists.

## Language-check result

Include a Language verification section linking the country record's source-to-wording comparison. Name the source/publication languages, date, separate-agent context isolation, exact scope, verdicts, corrections and any unreviewed passages. Report whether corrected final wording was rechecked. Do not mark a human-review checkbox complete based on an AI result: replace superseded blanket language-review items with the actual result and any remaining concrete action. A Supported result permits ordinary maintainer review; it does not approve or merge the PR. Checklist completion requires a recorded resolution, not just a tick.

## Automated post-draft verification pass

After opening a draft country research PR, the separate PR-opened research task checks that it is an open draft country PR and reads the PR description, the country research record and these instructions. It reruns only concrete unfinished checks that an agent can perform, especially official URLs and intake forms that failed in a text reader. For portal or session errors, make at most one fresh ordinary-browser attempt per destination; observe the relevant form and login condition without submitting, signing in, or creating an account. Check the authority, sector, audience, purpose and exact official source before marking a route verified. The pass happens after the initial bounded research stage and does not reset that stage's attempt history.

Record each result and date in the same research record and draft PR. If an official route is confirmed, update only that country's concise row and rerun isolated no-history language review and targeted structural checks when its wording changes. If it remains inaccessible or its purpose is uncertain, keep the table value Unknown and state the exact remaining check in the research record and PR. Preserve existing Yes/No and contributor correspondence unless explicit official evidence warrants correction. Never submit a report, send messages, change workflows or the events-calendar date script, open a second country PR, or merge a PR.

Run this pass once for a newly opened draft. Commit and comment events and a change from draft to ready for review must not repeat it. For a draft that predates the automated trigger, perform the same pass once manually.
