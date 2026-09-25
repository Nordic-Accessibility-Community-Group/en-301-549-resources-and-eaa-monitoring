# Enforcement presentation conventions

## Coverage and ordering

Publish a country only when there is supported, relevant activity to report. Research records cover all EU countries; the public page does not. Never add placeholder country rows or empty sector lists. Preserve the current tables and inherited entries until their evidence is reviewed. These conventions govern future supported edits, not a wholesale reclassification during setup.

Keep EU agency/civil activity, Commission proceedings against Member States, and non-EU activity in separate existing sections. Within country sections, sort by country, then the shared sector order, then event date newest first (unknown dates last). Use a stable case ID to break ties. A multi-sector case appears once, with sectors listed in canonical order. Existing combined rows need not be split merely to satisfy this convention; record case-level detail in research first. In the Commission section, sort by event date newest first, with countries named alphabetically. Unknown applicability must remain explicit.

Use exactly the shared EAA labels, in this order:

1. Products
2. E-commerce
3. Banking
4. Electronic communications
5. Transport
6. Audiovisual access
7. E-books
8. 112 emergency calls

Keep narrower product/service boundaries beneath these labels. An empty `sectors` array in research means not established; use a concise Unknown only where needed to understand an actual public entry. Do not infer a sector or EAA applicability from accessibility language alone. General national transposition proceedings need not be forced into a sector.

## Source and status labels

| Research source type | Public source label |
| --- | --- |
| `official_law` | Official law |
| `official_authority_publication` | Official authority publication |
| `official_court_decision` | Official court decision |
| `european_commission_publication` | European Commission publication |
| `external_legal_analysis` | External — legal analysis |
| `external_party_statement` | External — party statement |
| `external_news_report` | External — news report |
| `contributor_correspondence` | Contributor correspondence (only a shareable attribution) |
| `other_unverified` | External — unverified source |

Source labels describe provenance, not a verification verdict. Keep `verified`, `disputed`, `unknown` and `unverified_source` in research separately from procedural stages. Proposed stage labels are Announced monitoring, Ongoing monitoring, Complaint lodged, Investigation, Warning, Order issued, Conditional penalty, Penalty imposed, Appeal pending, Final judgment, Closed and Unknown. Map them only from supporting evidence. Closed does not itself mean compliant, and a final judgment can reject a claim.

Keep Commission procedural wording in a separate `stage_detail` field: do not substitute a generic national stage for the Commission's actual step. Conditional penalties need trigger dates/conditions; imposed penalties need evidence of the measure. Payment is a separate fact. Statutory maximums belong on the sanctions page, not as case outcomes.

For statistics show the as-of date, units, sector and counting basis. Do not add categories together unless the source establishes non-overlap and a common period. Aggregate counts and individual cases must not be counted as additional separate outcomes for the same events.

## Keep public entries concise

Include the relevant authority/court, supported activity or outcome, essential limits, event date and descriptive source links. Put excerpts, retrieval failures, detailed provenance, research history and unresolved questions in research records. Keep event/publication dates separate from Date added/Date updated; editorial maintenance is not evidence verification.

Use relative links for repository navigation so links continue to work upstream. Historical snapshot links stay pinned to the original commit. Use accessible text labels; any emoji supplements rather than replaces text. Do not publish private correspondence or personal details.

For GitHub categorisation, use the existing repository label `eaa-enforcement` if available. It is optional routing metadata, not a readiness or evidence verdict; do not create a parallel country/sector label system. If absent, the enforcement PR title and file scope provide routing without blocking work. No GitHub label is created by this setup.
