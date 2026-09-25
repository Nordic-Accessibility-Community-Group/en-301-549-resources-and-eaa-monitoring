# EAA sanctions research notes

These notes support the [EAA sanctions table](../../../../EAA%20sanctions.md). They use the monitoring research pattern of one JSON file per country, in a separate sanctions folder.

Each record keeps the original `last_checked` date and the complete `review_note` moved from the table. Each source keeps its URL, label, source type and original table description in `sources[].review_note`. These descriptions include research notes removed from the Sources column, such as access problems and unfinished checks. `source_snapshot` links to the version before the notes were moved.

This move does not add a new source check. A review date is not proof that every link was opened or every claim was confirmed. Access problems, partial checks and unresolved questions remain in `review_note` and in the source descriptions. Sources listed here include unverified leads; their presence does not confirm a claim.

These are review-note records, not monitoring-agency claim records, so `country-record.schema.json` does not apply. Keep the monitoring records in the parent folder unchanged. When updating sanctions research, preserve unresolved notes and update the country record and table date together only when a new review has taken place.

## Editorial reviews

`editorial_reviews` preserves previous public wording by column, the replacement text and a link to the original version. This includes research instructions, unfinished checks and historical amounts removed from the table. Editorial changes do not update `last_checked` or confirm a legal claim.

## Workflow and validation

Follow [shared workflow](../../workflow.md), [evidence](../../evidence.md) and [review](../../review.md), including distinct isolated source-fidelity/readability and independent actual-PR review. Sanctions covers statutory powers, conditions and maxima, not proof of actual enforcement. Distinguish administrative/criminal amounts, natural/legal persons, product/service scope, repeat or turnover conditions and coercive versus punitive payments. Explicitly authorised multi-country work is allowed; monitoring's one-country restriction and post-draft intake pass do not apply.

Run `python3 .github/scripts/check-sanctions.py` and `python3 .github/scripts/test-sanctions.py`. The public table retains EU-27 alphabetical coverage, seven columns, canonical sector labels, source agreement, dates and row fingerprints. Each country's public_row_sha256 changes only after review; editorial changes do not create new last_checked dates. These checks do not certify legal claims. Store review reports here against exact commits/content hashes, with distinct verdicts and limits; preserve historical reports.

[Quality recommendations](quality-checks.md) describe future storage work, not current publication evidence. Shared evidence intake updates relevant research across pages; no unsupported public update follows automatically.

## Countries

- [Austria](austria.json)
- [Belgium](belgium.json)
- [Bulgaria](bulgaria.json)
- [Croatia](croatia.json)
- [Cyprus](cyprus.json)
- [Czechia](czechia.json)
- [Denmark](denmark.json)
- [Estonia](estonia.json)
- [Finland](finland.json)
- [France](france.json)
- [Germany](germany.json)
- [Greece](greece.json)
- [Hungary](hungary.json)
- [Ireland](ireland.json)
- [Italy](italy.json)
- [Latvia](latvia.json)
- [Lithuania](lithuania.json)
- [Luxembourg](luxembourg.json)
- [Malta](malta.json)
- [Netherlands](netherlands.json)
- [Poland](poland.json)
- [Portugal](portugal.json)
- [Romania](romania.json)
- [Slovakia](slovakia.json)
- [Slovenia](slovenia.json)
- [Spain](spain.json)
- [Sweden](sweden.json)
