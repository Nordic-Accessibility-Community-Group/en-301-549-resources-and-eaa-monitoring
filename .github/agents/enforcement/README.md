# EAA enforcement tracking project

## Purpose and scope

Maintain and verify [EAA enforcement tracking](../../../EAA%20enforcement%20tracking.md) in `erikgustafsson/en-301-549-resources-and-eaa-monitoring-testing`.
This is a separate project from the monitoring-agency watcher and sanctions research.
It covers actual monitoring activity, enforcement measures, civil proceedings and European Commission infringement proceedings already listed on the page, plus subsequently verified developments.
This setup does not schedule a new automation or authorize edits to the original repository.

## Working boundaries

- Use separate `enforcement/` branches and draft PRs based on current main. Check open PRs, pending branches and overlapping files before starting and before publishing.
- Keep instructions and research under `.github/agents/enforcement/`. Public updates belong only in `EAA enforcement tracking.md` unless an additional change is explicitly authorized.
- Use [workflow.md](workflow.md) for the review sequence and [presentation.md](presentation.md) for shared labels and sorting. Shared guidance supplies evidence principles, not the monitoring page's reporting-route checklist or table layout.
- Do not modify watcher state, sanctions research, other pages, GitHub Actions or `.github/scripts/check-verification-dates.py`. Never merge or send correspondence.
- Do not use the country-authority audit PR title: use `Audit EAA enforcement tracking: <scope>` so the unrelated country post-draft automation is not invoked.
- Preserve contributor/correspondence facts and record missing provenance; missing public confirmation does not disprove an existing claim. Do not publish private messages or personal data.

## Evidence and presentation

For each claim record country, authority or court, sector, action/case identifier if available, action type, procedural stage, event date, publication date, verification date, exact source URL and supporting passage, provenance, evidence status, uncertainty and next check.
Use verified, disputed, unknown or unverified_source as evidence statuses, separately from procedural stages.

Prefer regulator publications and court decisions. Distinguish court documents from a litigant's interpretation, and official evidence from industry reports. Secondary sources are leads until checked; retain attribution where needed.
Read the primary document before asserting an outcome. Distinguish complaints, announced monitoring, investigations, warnings, orders, imposed penalties, conditional daily penalties, appeals and final judgments.
A legal power to sanction does not establish that a sanction was imposed. A statutory maximum belongs to sanctions research, not a reported case outcome.
Check the actual legal basis: do not equate all accessibility enforcement with EAA enforcement, including non-EU cases. Keep Commission proceedings against Member States separate from enforcement against businesses.
Never interpret absence of reports as absence of enforcement.

Keep source dates, event dates and table maintenance dates separate.
Record the as-of date, units, sector and counting basis for statistics; do not combine complaints, reports, inspections and cases or infer totals from partial subtotals.
Preserve the existing table structure initially. Apply the vocabulary in [presentation.md](presentation.md) only after mapping each affected claim to evidence; this setup does not reclassify existing entries.
Apply isolated no-history language review to new translated or meaning-sensitive publication wording, then targeted table, date and link checks. Report checks that could not run.

## First audit backlog

These are observations about the current page, not findings that the underlying claims are false.
Baseline inspected: 2026-09-25, main commit `a82f3d72a8e2aaf9b138e3714e65367d0388654e`.

1. Inventory existing assertions and their source/provenance, including contributor correspondence. Capture originals before proposing edits.
2. Germany: the row classified as Civil action describes testing-centre commentary about overlays. Establish whether any actual civil proceeding supports that classification; otherwise propose a supported classification or relocation after review.
3. Czech Republic and Ireland: retrieve official support for the quoted secondary reporting; distinguish planned publication of lists from completed enforcement and complaints from adjudicated breaches.
4. Austria, Denmark, Finland, Slovenia and Sweden: identify the provenance of unlinked activity/statistics claims. Preserve correspondence-based facts while requesting exact dated support where absent.
5. Denmark: clarify the counting basis for 179 online inspections and listed sector subtotals; do not infer that the listed categories are exhaustive or inconsistent.
6. Finland: reconcile statistics dated 2026-09-09 with Date updated 2026-08-14; confirm what the maintenance-date column represents before editing.
7. France: verify court documents, operative dates, remedies, conditional penalties and appeal status; distinguish litigants' criticism from the court's ruling.
8. Commission section: verify publication and procedural stage against the linked official decision; do not treat Date added as the decision date.
9. Norway: verify the named authority, applicable law, app name, correction deadline and whether the daily fine was conditional or actually imposed. Do not assume EAA applicability.
10. Sweden and Netherlands: verify source dates, sector scope, ongoing versus completed monitoring, and distinguish statistics from individual outcomes.

## Delivery sequence

First prepare a claim/source inventory and prioritize evidence gaps. Then research a bounded scope, verify evidence, prepare concise wording, run the required isolated language and local checks, and open a draft PR with concrete unresolved questions.
Use at most ten minutes of research/verification per country and thirty minutes per pass, with at most two access attempts per failed URL and two targeted follow-up searches per unresolved question. Record deferred checks honestly.
Separate accuracy blockers from nonblocking follow-ups; omit or narrow unsupported new assertions. Human review remains required.
A recurring enforcement watcher can be designed after this baseline audit; no schedule is created by these instructions.

## Public coverage and research coverage

Add a country to the public page only when there is supported, relevant activity to report. Never add empty country rows, eight-sector placeholders, or a claim that no enforcement exists merely because nothing was found. Preserve existing contributor entries pending evidence review.

Keep one JSON record for every EU country in [research/](research/README.md), whether or not it has a public entry. Keep records for other jurisdictions already covered, currently Norway. A Commission proceeding has one shared record, referenced by affected countries; it is not duplicated as business enforcement. Creating a record does not authorize research or a public entry.

The initial records capture only the existence and location of existing repository entries and the setup backlog. All countries start as `not_yet_researched` in this enforcement workflow, with no attempts or verification dates. This does not deny earlier contributor research. The frozen public-entry map preserves original locations and fingerprints without confirming any claim.

Follow [record-format.md](record-format.md) and the [record template](record-template.json). Research states are `not_yet_researched`, `partially_researched`, and `bounded_pass_completed`; a separately recorded result may be `not_assessed`, `reportable_activity_found`, or `no_reportable_activity_found_in_checked_sources`. A completed bounded pass never proves exhaustive country coverage or absence of enforcement.

## Local checks

Run from the repository root:

```sh
python3 .github/agents/enforcement/check.py
python3 -m unittest discover -s .github/agents/enforcement -p 'test_*.py'
```

The standard-library checker validates record structure, complete EU research coverage, allowed sector and source labels, date semantics, IDs and references, and exact public-row mappings. It does not verify legal meaning, source reachability, readability or translation. It permits countries with no public entry and enforces no EU-27 public table or fixed sector coverage.

Run the existing repository content checks too; do not duplicate their workflow or reuse the sanctions validator. The events-calendar date check is unrelated to enforcement verification. External sources require a separate bounded evidence check. No new watcher, schedule, automatic post-draft research trigger or GitHub Actions workflow is introduced.
