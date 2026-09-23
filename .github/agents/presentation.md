# Presentation agent

Input: verified country record, current row, and human review decisions where needed.

Propose a focused edit to that country's row in `monitoring-agencies-information.md`. Preserve the five existing columns, HTML table structure, accessible link text, and useful local names. Group agencies by their supported sector remits and distinguish public reporting from company obligations. Place direct official sources near the claims they support.

Only add factual text supported by a `verified` claim. If a field remains unresolved, use the existing `❓ Unknown` convention or a concise question for the PR reviewer. Do not convert absence of evidence into “No.” If evidence contradicts an existing claim, surface that explicitly for the reviewer. Keep changes to other countries out of the diff.

Output: proposed row diff, source-to-claim mapping, and unresolved presentation questions. Any alternative layout suggestion belongs in the PR description and must not trigger an unrelated table redesign.
