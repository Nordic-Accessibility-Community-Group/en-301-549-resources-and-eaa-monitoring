# EAA sanctions PR check

Use this check for changes to `EAA sanctions.md` and its records in `research/sanctions/`. Follow the evidence principles in `verification.md` and the review separation in `pr.md`. The monitoring workflow's one-country limit does not apply to an explicitly authorised multi-country sanctions update.

1. Read the actual GitHub PR, its current head commit and diff. Confirm the repository, base branch, draft state and authorised file scope. Do not rely on a stale local branch.
2. Start a separate reviewer with no conversation-history fork. Give it the PR, public page, research records and this checklist. Keep this reviewer separate from the isolated language reviewer, who receives only the public wording and a neutral brief.
3. Check every changed legal claim against its recorded evidence and scope. Separate source provenance, source retrieval and claim verification. An official-looking link or a successful structural check does not verify a claim. Keep uncertain amounts Unknown or explicitly attributed to their source; keep essential scope limits visible.
4. Run `python3 .github/scripts/check-sanctions.py`. Record the result and reviewed commit or content hash. This is a consistency check, not a legal check. Do not use the events-calendar date check for sanctions.
5. Read the isolated language-check report. Confirm corrected final wording was rechecked. Distinguish readability, source-language fidelity and legal evidence review. Record unreviewed passages and unresolved questions honestly.
6. Rewrite the PR description around the final diff. Include changed file groups, the actual source-review limits, checks performed and their versions, resolved issues, and remaining publication blockers separately from non-blocking research gaps. Recheck after subsequent edits.
7. Record findings in `research/sanctions/pr-check.json`. State what was and was not checked. Do not claim CI ran without actual run results, or treat an AI review as maintainer approval.

A check is complete when findings and dispositions are recorded, not when all legal gaps have been researched. A complete check can return “changes needed.” Keep the PR in draft while material publication questions remain. Never merge, approve or enable auto-merge as part of this check.
