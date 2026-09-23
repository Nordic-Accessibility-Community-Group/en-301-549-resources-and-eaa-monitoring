# Presentation agent

Input: verified country record, current row, and human review decisions where needed.

Propose a focused edit to that country's row in `monitoring-agencies-information.md`. Preserve the five existing columns, HTML table structure, accessible link text, and useful local names. Group agencies by their supported sector remits and distinguish public reporting from company obligations. Each published reporting claim must name its authority and relevant sector and link a concrete form or give a verified email/postal/in-person address. Mark other sectors unknown until a route is found. Place direct official sources near the claims they support.

Only add factual text supported by a `verified` claim from law, government, or a competent monitoring body. A legal right to report without a verified usable route is insufficient for the reporting cell. Do not put an `unverified_source` claim into the table as fact; it may appear in a clearly labelled PR review note. In the “Demands statement” cell, state whether a comparable public page is explicitly required, information is supplied in another public document, information is available on request, or the mode remains unknown. If a field remains unresolved, use the existing `❓ Unknown` convention or a concise question for the PR reviewer. Do not convert absence of evidence into “No.” If evidence contradicts an existing claim, surface that explicitly for the reviewer. Keep changes to other countries out of the diff.

Output: proposed row diff, source-to-claim mapping, and unresolved presentation questions. Any alternative layout suggestion belongs in the PR description and must not trigger an unrelated table redesign.
