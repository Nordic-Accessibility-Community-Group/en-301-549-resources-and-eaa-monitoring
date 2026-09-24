# Reporting-label consistency pass — 24 September 2026

Scope: the contributor approved a full-column editorial pass using audience + purpose. Baseline: Luxembourg PR #30, commit `5eb836a0734fb727c854e8cef40309bc2bc36b78`. This is a shared editorial change, not another country research audit. Historical evidence, exact excerpts and earlier language-review records remain unchanged.

## Presentation decision

Use Public complaints, Public reports, Public enquiries, Public enforcement requests, Company non-compliance and Company exemptions. Use Company non-compliance / exemptions only for a verified shared route. Keep sector, authority, scope, prerequisites, languages and destinations. The new Company exemptions label supersedes the earlier instruction to use bare Exemptions.

Public/Company are navigation labels, not exhaustive legal eligibility definitions. For example, Luxembourg's source categories remain natural persons and legal persons (including associations). Germany's formal consumer enforcement procedure remains separate from barrier reports and retains its consumer restriction.

All 36 reporting cells reviewed; 32 changed. Portugal, Romania, Slovakia and Spain retain their existing reporting text pending the classification checks below. No statement values, authorities, law references, other table cells, reporting destinations or correspondence facts changed. Unknown reporting routes do not establish EAA applicability outside the EU/EEA or create an obligation to report.

## Mapping to existing evidence

- Czechia: existing public inspection-submission and service-provider notification routes become Public reports and Company non-compliance. See `czechia.json`.
- Denmark: the existing public reporting form for self-service terminals receives Public reports (self-service terminals). No channel change.
- Estonia: `estonia.json` explicitly limits the company non-compliance email evidence to product economic operators. Label: Company non-compliance (products); no extension to service-provider notices.
- France: consumer problem reports become Public reports; business self-reporting becomes Company non-compliance. DGCCRF and the routes remain explicit.
- Germany: `germany.json` distinguishes a barrier report from a formal section 32 administrative application. Labels: Public reports and Public enforcement requests (consumers). Both forms remain separate.
- Ireland: `ireland.json` supports CCPC/ComReg public complaints, CnaM public reports, Central Bank public complaints, and NTA provider non-compliance notification. ComReg's company route remains confined to electronic communications, not 112. CCPC's inherited company email is not newly certified for either statutory purpose.
- Lithuania: `lithuania.json` records unsigned RRT enquiries whose replies are not the official RRT position. Label: Public enquiries, retaining the existing qualification. VVTAT Company reports remains broad; it is not relabelled as an exemption channel.
- Luxembourg: `luxembourg.json` preserves the formal eligibility categories and MyGuichet purpose evidence. Labels: Public reports, Company non-compliance and Company exemptions.
- Netherlands: the existing linked non-compliance instructions and public reporting guidance receive Company non-compliance and Public reports. Existing deadlines are retained; this pass does not reverify them.
- Sweden: `sweden.json` records PTS's conditional company email fallback. Company reporting email remains conditional on inability to use the e-service; it is not broadened to public complaints or newly certified for each statutory purpose.
- Slovenia: the existing text explicitly names both audiences. Public and company reporting preserves the broad scope without inferring complaint, non-compliance or exemption intake.

## Follow-up classification tasks

These do not block the supported wording changes. Preserve existing contributor information until specific official evidence establishes the classification; do not mark a route verified merely by checking a box.

- [ ] Italy / existing AgID portal — identify its audience and whether it accepts EAA public complaints, company non-compliance or exemption notifications. Resolve with official procedure instructions or authority correspondence naming the portal and each supported purpose. Owner: research agent/contributor.
- [ ] Romania / registratura@anpd.gov.ro — establish public/company eligibility and supported purposes from authority guidance or correspondence. Retain the existing email and language claim meanwhile. Owner: research agent/contributor.
- [ ] Slovakia / info@soi.sk — establish public/company eligibility and supported purposes from authority guidance or correspondence. Retain the existing email and language claim meanwhile. Owner: research agent/contributor.
- [ ] Spain / utac@dsca.gob.es — establish the audience and whether this is an enquiry contact or filing route, including which purposes it supports. Resolve with explicit official guidance/correspondence. Owner: research agent/contributor.
- [ ] Slovenia / gp.irsid@gov.si and postal route — both audiences are already stated; confirm separately whether complaints, company non-compliance and exemptions are accepted. Resolve per purpose with official instructions/correspondence. Owner: research agent/contributor.
- [ ] Ireland / access@ccpc.ie — obtain contributor correspondence or explicit CCPC confirmation of the purposes accepted by email. Existing evidence publicly confirms queries; inherited company-reporting information is preserved without extending it to both statutory purposes. Owner: contributor/research agent.
- [ ] Lithuania / VVTAT general route — distinguish broad company accessibility reports from non-compliance notices and Article 14 exemption notifications. Resolve each purpose through VVTAT instructions/correspondence; retain Company reports and Company exemptions: Unknown meanwhile. Owner: research agent/contributor.
- [ ] Portugal / dated absence-of-procedures statement — recheck current official procedures in the country audit; do not silently convert the dated claim into Unknown or extend it to a particular audience. Owner: research agent.

## Validation

Targeted checks preserve all 36 country rows, five cells per row, every reporting URL in order, and every cell outside the reporting column byte-for-byte. Tag inventory is preserved except paragraph wrappers for previously bare Unknown cells. No br tags added; git diff whitespace check passed. No GitHub Actions workflow or calendar date script changed.

This pass does not reverify government pages, form operation, accepted languages, deadlines or legal duties. Existing source verification and original-language reviews remain in the country records; the editorial comparison is separately scoped below.

## Isolated editorial review

Reviewer `/root/reporting_wording_review`, 24 September 2026, no history fork. Inputs were only before/after English cells; the reviewer did not receive workflow instructions, evidence statuses, conclusions or PR discussion. It confirmed retention of routes, conditions and language qualifications. This is English editorial comparison, not a new original-source language check or factual certification.

Corrections retained explicit inspection submissions for Czechia, consumer problems and self-reporting for France, consumer barrier reports for Germany, and service scope for RRTV. Final labels keep the common vocabulary while these details follow the label or appear in parentheses.

The baseline-only comparison could not establish audiences or purposes omitted from earlier labels. Those observations were checked against the existing records: Estonia product-economic-operator self-reporting; RRTV service-provider notification; Germany section 32 administrative application; Ireland NTA provider notification and Central Bank complaints; Luxembourg's purpose-specific MyGuichet procedures; and the official PTS company email fallback. The evidence mappings above support retaining the more explicit labels. The previous bare Exemptions label was replaced under the contributor's explicit cross-country presentation decision; no new exemption route was added. Historical eligibility restrictions remain in the country records and linked procedures.

The reviewer suggested deleting the PTS company label based solely on the old paragraph's placement. The official correspondence and its recorded company-reporting context support that label; the fallback condition remains intact. No claim is made that this editorial review rechecked original-language government sources. Ordinary maintainer review remains required.

Final corrected qualifiers rechecked by the same isolated reviewer: Supported for ČOI inspection purpose, France consumer problems/self-reporting, Germany consumer barriers and RRTV service scope. RRTV company audience remains unestablished by the old English cell alone; its existing country record supplies the provider-notification evidence. Full rendered HTML validation remains unavailable because `tidy` is not installed; targeted HTML checks passed.
