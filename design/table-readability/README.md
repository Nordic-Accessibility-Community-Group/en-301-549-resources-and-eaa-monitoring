# Table readability proposal

This proposal covers all resource tables: top-align column headers, row headers and data cells; use clear horizontal separators; retain alternating backgrounds as an additional reading aid.

Open [the browser preview](preview.html) locally to review the design. It embeds a copy of [the proposed shared stylesheet](tables.css), so it also works when opened or downloaded on its own, and contains illustrative entries of different lengths, not country or legal data.

## Proposed appearance

- Left-align and top-align every header and data cell, with consistent padding and no extra margin above the first paragraph or list.
- Use solid 2 px horizontal separators in `#767676`.
- Alternate white (`#FFFFFF`) and blue-grey (`#E8EEF3`) body rows.
- Use `#1F2937` for text, including secondary text. Keep links underlined and check their contrast on both backgrounds.
- Preserve semantic tables, captions and header associations. Permit horizontal scrolling for wide tables without forcing the entire page to scroll.

Calculated sRGB contrast ratios, rounded here for reporting:

| Foreground | Background | Contrast |
| --- | --- | --- |
| Separator `#767676` | White `#FFFFFF` | 4.54:1 |
| Separator `#767676` | Blue-grey `#E8EEF3` | 3.88:1 |
| Text `#1F2937` | White `#FFFFFF` | 14.68:1 |
| Text `#1F2937` | Blue-grey `#E8EEF3` | 12.55:1 |

## WCAG 2.2 rationale

[SC 1.4.11 Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) requires at least 3:1 for graphical information required to understand content. This is not a blanket requirement for every decorative table line or alternating background. The proposal uses separators that exceed 3:1 against both adjoining row backgrounds, so row separation does not depend on the zebra shading.

[SC 1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) requires at least 4.5:1 for normal-sized text and 3:1 for large text. Text must meet its threshold on every background used, including interactive states.

Top alignment is a readability recommendation, not a separate WCAG success criterion. These colour calculations do not establish full WCAG conformance or confirm a failure in the current tables.

## Applying the design

The current repository publishes Markdown containing HTML tables and has no shared site stylesheet. GitHub controls the rendered appearance of those files. Adding this stylesheet to the repository alone does not restyle GitHub's Markdown view; inline CSS is not a dependable solution there.

For a website or documentation renderer that permits author CSS, load `tables.css` and apply the `resource-table` class to every resource table. The preview demonstrates this integration. Keep the document content, source links, captions and header relationships intact.

This PR is a reviewable design suggestion. It does not introduce a publishing system or claim to change the existing GitHub table rendering. Adopting the visual design throughout the published resources requires a renderer that supports the shared stylesheet.

## Review checks

Check long paragraphs, lists and short entries together; confirm their first lines align. Check the preview at narrow widths and browser zoom, including keyboard access to the scrollable table. In forced-colour mode, allow system colours and retain visible row borders. If dark mode is introduced later, define and measure a separate palette rather than inheriting untested backgrounds.
