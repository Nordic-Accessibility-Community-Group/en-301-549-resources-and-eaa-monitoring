# Shared country research storage (version 2)

One canonical file per authorised jurisdiction lives in countries/<lowercase country>.json. [registry.json](../registry.json) owns jurisdiction classification and sector labels/order. [country.schema.json](country.schema.json) describes the storage envelope. Monitoring, sanctions and enforcement retain distinct domain contracts and verification semantics; no country-wide verified flag exists.

## Evidence and domains

The root owns country identity, jurisdiction_group, evidence, domains and deliveries. Domains contain monitoring, sanctions or enforcement only when a corresponding record exists. Do not invent missing domains or turn unavailable evidence into a public placeholder. Each domain preserves its original dates, claims, questions and legacy notes. Sanctions review notes are not converted into verified claims. Monitoring claims gain stable administrative IDs; enforcement IDs remain unchanged.

Evidence is a country-local pool of exact recorded source objects. source_refs preserves source order and duplicates where meaningful. Identical complete source objects share an ID; different passages, source types, dates or provenance remain distinct even when URLs match. IDs are content fingerprints: editing evidence creates a new ID and requires deliberate reference updates. A shared object is not a shared verification verdict. Source shapes remain compatible with their domain projections; this mechanical migration does not reinterpret legacy correspondence prose or standardise unlike observations by inference.

Edit canonical domains directly, retaining claim IDs across reordering. country_records.py expands a read-only legacy-compatible domain view for existing validators and external readers. Its save_domain helper is for fixtures/explicit adapters; monitoring claims must be edited canonically to retain stable IDs when reordering. Old paths in historical notes/reports are provenance, resolved with migration-manifest.json and the original commit; never create new files at those paths. Relative historical source_snapshot/language_check references retain their original folder context recorded by the manifest.

## Publication and routing

Country deliveries is canonical. Generate evidence-routing/events.json with `python3 .github/scripts/generate-routing-index.py --write`; it is a compatibility projection for existing PR-event readers. Destination domain identifies monitoring, sanctions or enforcement in the shared file. An absent domain retains a null record and explicit not_applicable reason. A truly multi-country event needs one owner with references, not duplicate event IDs. Keep current public mappings and frozen baselines separate; reverse references remain validated until a separately reviewed map simplification.

Do not edit historical review reports to imply they reviewed the migrated version. Public factual wording stays unchanged; the Estonia research link and current row hash change only to point at the canonical record. Frozen baseline bytes remain unchanged.

## Validation and migration acceptance

Install `.github/scripts/requirements-research.txt` into a development environment. Run `python3 .github/scripts/check-country-records.py` for schema/reference/routing checks plus existing sanctions/enforcement contracts. Run `python3 .github/scripts/test-country-records.py`, the domain regression suites and watcher tests. These do not verify legal meaning or source availability.

`--migration` additionally compares every expanded domain against the frozen migration-manifest fingerprints and rejects remaining writable legacy country files. Use this flag for migration acceptance only, not future authorised factual updates. Five pre-existing monitoring claims have six old-schema violations: exact claim/error fingerprints in legacy-schema-exceptions.json preserve them without asserting new verification. New or altered claims cannot inherit these exceptions. The checker pins the exception file digest; changing it requires an explicit reviewed migration, never an ad hoc check bypass.

The original monitoring schema validates expanded monitoring data. Existing enforcement and sanctions validators now read expanded domain views, preserving their distinct rejection rules. The shared schema owns storage rather than replacing domain evidence gates. Templates describe domain views; initialise a new canonical record deliberately using these contracts, not by copying an old path.

## Runtime migration boundary

Repository readers, links, inventory and instructions are migrated together. Watcher and PR-event runtime state/leases and history are unchanged. The original setup conversation confirms Fridays at 09:00 Europe/Stockholm from 2 October 2026 for Denmark, Sweden, Ireland, Italy and Portugal. The watcher runtime branch was read successfully with baseline-2026-09-25 and no active lease. The deployed cloud task prompts are outside this repository and could not be inspected or changed through the available controls. Before merging the migration, the automation owner must verify/update those prompts to read current main instructions, shared record_path/domain, and canonical deliveries, then run a read-only smoke check. Do not claim the external runtime migration completed solely because repository tests passed. The generated ledger retains its events array to reduce compatibility risk; it does not authorise duplicate writable records.
