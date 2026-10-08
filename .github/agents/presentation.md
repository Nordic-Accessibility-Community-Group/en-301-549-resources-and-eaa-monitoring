# Shared presentation rules

These rules apply to every public page, including monitoring agencies, sanctions, enforcement tracking and standards adoption. Follow [workflow](workflow.md), [evidence](evidence.md), [review](review.md) and the relevant page specification. Historical task prompts that refer here remain supported.

## Punctuation

Do not use em dashes in public-facing text, including headings, table cells and link labels. Use commas, colons, parentheses or separate sentences as appropriate. For separators in standard titles, use a colon or a hyphen. Preserve the wording and meaning, and do not change URLs or identifiers.

## Link language

Add `hreflang` to links when the language of the linked resource is established. Use a valid BCP 47 tag, such as `en`, `de`, `fr` or `pt-BR`. The value describes the destination, not the country, authority, link label, available translation menu or languages accepted by a reporting channel. Check the exact linked language version, including redirects and PDF content. Preserve the original URL unless a destination change is independently justified.

Use `lang` only when needed to identify the language of the visible link text. A German authority name linking to a German page may correctly have both `lang="de"` and `hreflang="de"`. An English description of that page uses `hreflang="de"` without `lang="de"`. Destination hints do not replace a document's own language metadata or guarantee a particular browser or screen-reader behaviour.

Markdown links cannot carry these HTML attributes: use equivalent HTML anchors when necessary, preserving their visible content, accessible name and destination. For relative links, inspect the target document; fragment links inherit the current document's language. Do not add a document-language hint to `mailto:`, `tel:` or other non-document actions.

If a destination is unavailable, language-negotiated without a stable version, multilingual without a clear primary language, or otherwise uncertain, record the unresolved link in the audit and omit an unsupported tag. Do not infer language from a country-code domain alone. Do not treat error/challenge-page language as the destination language.

Before publication, check all added or changed links on the actual PR head. After the last research batch, repeat the check against the final batch/PR heads. Review both existing attributes and missing attributes, and keep link-language maintenance separate from factual verification dates.

Reference: [MDN: HTMLAnchorElement.hreflang](https://developer.mozilla.org/en-US/docs/Web/API/HTMLAnchorElement/hreflang).
