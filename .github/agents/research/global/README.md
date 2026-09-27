# Worldwide discovery and future legal mapping

[worldwide-index.json](worldwide-index.json) is the shared country-and-area inventory and research intake file authorised on 27 September 2026. It covers the UN M49 list plus two explicitly identified supplementary jurisdictions. It is a research index, not a public legal or adoption conclusion.

## This discovery round

The 13 country rows already in the adoption page link to their canonical JSON records and are excluded from this round. The EU-wide record is separate. Countries present only in monitoring, sanctions or enforcement research remain eligible for EN discovery. Existing files are preserved; EU membership alone does not establish national adoption.

All other entries start as pending and not researched. Empty findings mean no research has been recorded. Use the structured attempt, source and finding fields described in the JSON. A bounded unsuccessful search may be labelled no_reference_found_in_checked_sources, never proof of non-adoption. Retain failed access, uncertainty and next actions. No national law searches were performed during inventory creation.

## Evidence ownership

Until an explicit EN 301 549 connection is supported, keep EN leads and incidental discrimination/accessibility law findings in the entry's shared research object. Do not create a country file for a law-only finding in this project. An existing country file for another authorised domain remains intact and is listed separately as existing_repository_record.

When a source establishes an explicit connection, create or reuse research/countries/<country>.json, following the [shared storage contract](../README.md) and [adoption contract](../../adoption/README.md). Update the jurisdiction registry only as needed. A reference, draft or translation must retain that relationship; it is not automatically an adoption or binding law. Link the exact country path, domain and supporting claim IDs from the index. Preserve claim-level status and source provenance.

Transfer shared history into the canonical record without duplicating writable findings; after transfer set research to null in the index. Do not silently add a legal domain to the strict country schema. Until a legal contract is approved, incidental law sources and follow-up questions in linked adoption records can be preserved in their existing evidence/questions fields. Any structured legal-domain extension needs a separate reviewed change; it must preserve all collected findings. Keep inventory identifiers, task membership and source provenance stable.

## Deferred legal mapping

The JSON task global-legal-mapping-existing-adoption-countries explicitly lists all 13 excluded country IDs for later discrimination and accessibility law research. This is a repository backlog item, not an active automation or a claim that the legal mapping is complete. No schedule is configured. It will support a future global accessibility law page after verification and review.

For every law finding record the official title, jurisdiction, type, official source, relevant provisions, scope, status and event-labelled dates. Distinguish enacted, in-force and proposed instruments. Discovery links and excerpts are leads until checked; legal applicability needs its own evidence. Include discrimination law even when it does not mention EN 301 549.

## Research and publication boundaries

Follow the [common workflow](../../workflow.md): 30 minutes per run, 10 minutes per jurisdiction, access/search limits, actual timing logs and explicit unresolved work. The shared JSON is research intake; a country pointer does not itself authorise a public row or a verified legal claim. Public additions require the applicable evidence, isolated language review and validation. Keep setup/process work separate from factual publication.

This index is outside the canonical countries directory so existing country validators do not mistake unresearched inventory entries for country evidence. On edits check unique country IDs/codes, source coverage, valid country/claim pointers, the explicit exclusion set and deferred-task membership. Recalculate scope counts if entries or round statuses change. Never merge, approve, enable auto-merge or write main.
