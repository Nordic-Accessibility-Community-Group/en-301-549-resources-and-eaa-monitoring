# Shared language and PR review

## Isolated source fidelity

After presentation, translated or meaning-sensitive new wording receives an independent source-to-wording check in every source language, including shortened wording. Start a separate reviewer with no conversation-history fork (`fork_turns="none"`). Give only [the neutral brief](language-verification.md), original passages with sufficient surrounding context/cross-references, source URLs/sections and exact proposed wording. Exclude workflow/research instructions, records, evidence statuses, conclusions, PR discussions and desired verdicts. The reviewer may retrieve necessary context within the remaining budget.

Record excerpts, literal renderings, exact reviewed wording, source references, Supported / Correction needed / Ambiguous verdicts, reviewer/date and limits. Recheck corrected final wording. Material ambiguity is a Before PR issue: resolve, narrow or omit the affected addition. Do not demand a fluent human by default. A Supported language verdict does not verify legal applicability, change evidence status or approve a PR. If isolation is unavailable, record not performed rather than a same-context self-review.

## Isolated readability

Sanctions and enforcement public wording receives a separate no-history B2 readability review. Give only the proposed public text and a neutral brief to identify exact unclear wording and suggest corrections without adding facts. Do not include research records or prior findings. Recheck corrections; meaning-sensitive changes return to source fidelity. Monitoring retains its source-fidelity requirement and concise presentation checks; this consolidation does not add a new mandatory reviewer to that workflow.

Source-fidelity/readability reviews are not applicable to process-only changes without public wording. Reviewers remain distinct even if their results share one version-bound report. Historical reports are not overwritten or combined into an implied current verdict.

## PR review and description

Open drafts against the testing repository, never main writes. Before PR creation resolve accuracy blockers, or omit/narrow affected assertions. Put Manual checks before merge near the top: only concrete checks identifying country/claim, action, reason, evidence, owner and resolution criterion; otherwise state None identified beyond ordinary maintainer review. Separately report resolved/omitted Before PR items and Non-blocking follow-up linked to records. A tick requires evidence of resolution, not an AI approval claim.

Describe the final diff: actual file groups, scope, sources/dates, supported changes, inherited/unreviewed material, review results and validation limits. Include source/publication languages, reviewer isolation, exact reviewed text/version, corrections and rechecks where applicable. Do not claim completed human review or CI from an AI result. Rewrite stale descriptions after scope changes.

Enforcement and sanctions require a separate no-history PR reviewer given the actual GitHub PR/head/diff, evidence records, this checklist, domain specification and completed review reports. It may read research conclusions and must be different from language reviewers. Check claim-to-evidence mapping, final wording, authorised scope, blockers, preserved history, tests and description. For infrastructure, check behaviour, fixtures, instructions and preservation; no new legal research. Monitoring follows its existing draft evidence/diff review and one-time post-draft check; do not silently add an independent-agent gate there.

Store version-bound reports with reviewer isolation, exact scope, findings/dispositions and unreviewed material. Existing monitoring comparisons live in review_note; sanctions reports and enforcement reviews retain their current locations until a storage migration. A completed review may return changes needed. Read the actual head again after publication; evidence/wording changes invalidate affected reviews, while a report-only follow-up does not require retranslating unchanged text. Human maintainer review remains required; never approve, merge or enable auto-merge.
