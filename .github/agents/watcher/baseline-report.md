# Initial watcher baseline — 25 September 2026

Repository baseline: `5766de5ca2e633197b510a173e8009f9975d3986` in the testing repository. Countries: Denmark, Sweden, Ireland, Italy and Portugal. This is watcher setup and observations only; country records and the table were not revised.

## Coverage

The inventory registers 68 distinct country-record URLs plus three discovered leads (71 total). The initial pass attempted ten selected record sources, two per country, and three discovery URLs. Twelve pages were readable through the web reader; the AgID news URL returned 403. The remaining 58 URLs are pending, not verified. Reader crawl metadata is recorded; freshness at the origin was not independently established. Visible form controls were observed without submitting, logging in or creating accounts.

Denmark: authority roster and company notification guidance read. The notification page's rendered mailbox mixes `mo@erst.dk` and `sik@sik.dk`; verify the actual destination before proposing a correction. Preserve the existing record.

Sweden: PTS service-information guidance and MTM supervision overview read. PTS distinguishes general terms/equivalent information from recommended website links. The MTM page links onward to reporting; that alone does not certify the intake.

Ireland: CCPC authority roster and company notification form read. The form states non-compliance/exemption purposes, while `access@ccpc.ie` is described for queries. This does not independently confirm the inherited email-reporting claim.

Italy: AgID FAQ and enquiry contact page read. The information mailbox is not proof of statutory reporting. A discovered official news URL was inaccessible (403); its search-result description remains an unverified lead.

Portugal: original Decree-Law 82/2022 and IDiPD complaint intake read. The public form requires a prior unresolved complaint to the supplier/provider. It does not establish company non-compliance/exemption filing. Later amendments and all sector-specific routes remain separate checks.

## Discovery results and limits

The initial searches exercised discovery in all five countries, but results for Denmark, Ireland and Portugal were insufficiently relevant; those passes remain partial. Italy produced leads but the news page was blocked. No complete monthly discovery cycle is claimed. Next run must refine the incomplete queries, inspect official news sections and work through pending source coverage.

Two readable Swedish news leads are queued for comparison with the research record. These publications predate initialization; they are not claimed to have changed since the previous audit:

- [PTS banking supervision](https://pts.se/nyheter-och-pressmeddelanden/pts-inleder-tillsyn-av-banktjanster/), published 8 September 2026: announced the start of the first banking-service supervision under the accessibility law, with the review running during 2026–2027.
- [PTS proposed language amendment](https://www.pts.se/nyheter-och-pressmeddelanden/pts-foreslar-andrade-sprakkrav-i-foreskrifter-om-vissa-produkters-tillganglighet/), published 23 June 2026: proposed Swedish or English information in product market-surveillance cases, with entry into force planned for October 2026. Final adoption and effective date remain to be checked; this is not proof of changed service-reporting language rules.

Isolated Swedish-to-English review by `/root/watcher_news_language`, no history fork, 25 September 2026: both observation summaries Supported. Source 1 short excerpt: “Granskningen av banktjänster kommer att pågå under 2026-2027.” Literal: the review of banking services will run during 2026–2027. Source 2 short excerpt: “Föreskriftsändringen planeras träda i kraft i oktober 2026.” Literal: the amendment to the regulations is planned to enter into force in October 2026. The reviewer noted that final-adoption caution is a scope qualification, not a direct translation. No country-table wording was introduced by these observations.

## Evaluation

Initial live source check: 13 attempted / 71 registered; 12 readable; one failed; 58 deferred. Confirmed material changes since a prior watcher snapshot: not measurable on initialization. Duplicate-alert and evidence-preservation behavior is tested locally with synthetic inputs; live false-positive and missed-change rates require subsequent runs and a comparison review. These limits are part of the pilot result, not completed verification boxes.
