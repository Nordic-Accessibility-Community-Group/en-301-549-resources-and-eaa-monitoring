# EAA sanctions research notes

These notes support the [EAA sanctions table](../../../../EAA%20sanctions.md). They use the monitoring research pattern of one JSON file per country, in a separate sanctions folder.

Each record keeps the original `last_checked` date and the complete `review_note` moved from the table. Each source keeps its URL, label, source type and original table description in `sources[].review_note`. These descriptions include research notes removed from the Sources column, such as access problems and unfinished checks. `source_snapshot` links to the version before the notes were moved.

This move does not add a new source check. A review date is not proof that every link was opened or every claim was confirmed. Access problems, partial checks and unresolved questions remain in `review_note` and in the source descriptions. Sources listed here include unverified leads; their presence does not confirm a claim.

These are review-note records, not monitoring-agency claim records, so `country-record.schema.json` does not apply. Keep the monitoring records in the parent folder unchanged. When updating sanctions research, preserve unresolved notes and update the country record and table date together only when a new review has taken place.

## Editorial reviews

`editorial_reviews` preserves previous public wording by column, the replacement text and a link to the original version. This includes research instructions, unfinished checks and historical amounts removed from the table. Editorial changes do not update `last_checked` or confirm a legal claim.

## Independent language check

Run a separate reviewer after editing the public page, with no conversation-history fork (`fork_turns="none"`). Give the reviewer only the public page and a neutral brief to check B2-level English, clarity and ambiguity. Do not provide research records, earlier conclusions, PR discussions or reasons for the changes.

The reviewer should identify the exact wording, explain the problem and suggest a correction without adding legal claims. Record the reviewed version, findings, changes and remaining questions in a language-check report in this folder. Recheck corrected wording before completing the review. Keep the source-review dates unchanged.

This readability check is separate from translation fidelity and legal verification. If a wording change depends on the meaning of a source, use the isolated source-to-wording process in [language-verification.md](../../language-verification.md) with original passages and enough context.

## PR and consistency checks

Follow the [sanctions PR check](../../sanctions-pr.md). Run `python3 .github/scripts/check-sanctions.py` from the repository root after edits. Each country’s `public_row_sha256` binds its record to the current row; update it only after reviewing the change. This does not certify legal accuracy.

See the [language report](language-check.json), [PR report](pr-check.json) and [quality-check recommendations](quality-checks.md).

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
