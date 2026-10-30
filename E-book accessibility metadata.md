# E-book accessibility metadata

Accessibility metadata describes an e-book's features and limitations so readers can decide whether it meets their needs. This page connects the European Accessibility Act (EAA) requirements with practical guidance for publishers, distributors, booksellers and libraries.

## E-books in the EAA

The <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019L0882" hreflang="en">EAA, Articles 2 and 3</a> covers consumer e-book services, including dedicated software, from 28 June 2025. Article 3(41) defines that service; dedicated e-reader devices have a separate product definition. Scope, exemptions and transitional provisions matter, including the exemption for microenterprises providing services in Article 4(5).

Annex I, Section IV(f) requires:

- Synchronised text and audio when both are present.
- Files that do not prevent assistive technology from operating properly.
- Access to content, navigation, layout (including dynamic layout) and structure, with flexibility and choice in presentation.
- Allowing alternative renditions and interoperability with varied assistive technologies, so that content is perceivable, understandable, operable and robust.
- Metadata about accessibility features to make e-books discoverable.
- Digital rights management (DRM) that does not block accessibility features.

These e-book requirements supplement the general service requirements in Annex I, Section III. Metadata alone does not establish that the book or service meets all applicable requirements.

## Service information and book metadata

Article 13(2) and Annex V require providers of covered services to explain how the service meets the applicable requirements. Information must be public in accessible written and oral formats. Annex V places it in the general terms and conditions or an equivalent document.

For a national example, <a href="https://saavutettavuusvaatimukset.fi/en/service-specific-requirements-and-obligations" hreflang="en">Traficom's Finnish guidance</a> explains additional accessibility-statement content for covered consumer digital services, including e-books: a service description, relevant information about products needed to use it, and an explanation of how the service-specific requirements are met. This guidance describes Finland's requirements; it does not establish compliance in other countries.

Book metadata serves a different purpose: it describes the particular publication. Keep service information and book information consistent, and check the national requirements that apply to the service.

## EPUB and ONIX: where the information goes

- **Inside the EPUB:** package metadata travels with the publication. <a href="https://www.w3.org/TR/epub-a11y-11/" hreflang="en">EPUB Accessibility 1.1</a> specifies accessibility metadata for EPUB publications, including those that do not meet its content-accessibility requirements.
- **Through the supply chain:** ONIX records convey information from publishers to sales, subscription and lending platforms, including before publication. They complement the metadata inside the book. See the <a href="https://www.w3.org/community/reports/publishingcg/CG-FINAL-onix-techniques-20251222/" hreflang="en">ONIX techniques for the display guide</a>.
- **On the book's page and in search:** turn metadata into understandable descriptions and useful filters. The <a href="https://www.w3.org/community/reports/publishingcg/CG-FINAL-a11y-display-guidelines-20251222/" hreflang="en">Accessibility Metadata Display Guide 2.1</a> gives practical guidance.

The <a href="https://www.w3.org/community/reports/publishingcg/CG-FINAL-crosswalk-20260128/" hreflang="en">Accessibility Metadata Crosswalk</a> helps map between vocabularies. Mappings are not always reversible: converting between formats can lose detail.

## Recording metadata in EPUB

Under EPUB Accessibility 1.1, the following package metadata is required or recommended:

| Property | Status in EPUB Accessibility 1.1 | What it describes |
| --- | --- | --- |
| `schema:accessMode` | Required | Perceptual or cognitive modes needed to process the content, such as textual, visual, auditory or tactile. |
| `schema:accessibilityFeature` | Required | Accessibility features provided by the publication. |
| `schema:accessibilityHazard` | Required | Potential hazards, such as flashing, motion simulation or sound. |
| `schema:accessModeSufficient` | Recommended | A mode, or combination of modes, sufficient to consume the content without significant loss of information. |
| `schema:accessibilitySummary` | Recommended | Human-readable information that complements the other metadata, including known limitations. |

A linked ONIX record alone does not satisfy EPUB Accessibility 1.1's package-metadata requirements. If a publication claims conformance to EPUB Accessibility 1.1, use the specified `dcterms:conformsTo` expression and identify the evaluator with `a11y:certifiedBy`. The evaluator may be the publisher; this field does not by itself mean independent certification.

For syntax and examples, use <a href="https://www.w3.org/community/reports/publishingcg/CG-FINAL-package-metadata-authoring-guide-20260827/" hreflang="en">Expressing Accessibility Metadata in the EPUB Package Document 1.0</a>, published on 27 August 2026.

**Version note, checked 20 October 2026:** EPUB Accessibility 1.1 is a W3C Recommendation. <a href="https://www.w3.org/TR/2026/CRD-epub-a11y-12-20260912/" hreflang="en">EPUB Accessibility 1.2, dated 12 September 2026</a>, is a Candidate Recommendation Draft. Among its proposed changes, `accessModeSufficient` becomes required and `accessMode` becomes recommended. Keep implementation guidance tied to the version being used.

For ONIX records, use EDItEUR's <a href="https://ns.editeur.org/onix/en/196" hreflang="en">List 196: E-publication Accessibility Details</a>. Its structured codes distinguish accessibility features, conformance claims, summaries and unknown information. A free-text summary complements the structured data.

For vocabulary reference, see <a href="https://schema.org/Book" hreflang="en">schema.org's Book type</a> and the <a href="https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/" hreflang="en">Accessibility Discovery Vocabulary</a>.

## Helping readers choose

The display guide recommends:

1. Make clear that the information describes the publisher's declarations.
2. Explain useful capabilities, such as visual adjustments and nonvisual reading, in clear language.
3. Treat missing metadata as unavailable information, rather than a negative accessibility claim.
4. Offer search filters for specific capabilities. The guide's minimum recommendation is positive filters for visual adjustments and nonvisual reading.
5. Refresh the displayed information when updated metadata arrives.

These are implementation recommendations from a W3C Community Group report. The display guide, ONIX techniques, crosswalk and package-metadata authoring guide are not W3C Recommendations.

For a retailer example, <a href="https://www.kobo.com/blog/kobos-spring-2025-update-on-new-features-and-fixes" hreflang="en">Kobo announced storefront accessibility information and search filtering in April 2025</a>. The previously contributed <a href="https://www.kobo.com/gb/en/ebook/the-death-of-shame" hreflang="en">The Death of Shame listing</a> is retained as a retailer reference, not an independently assessed accessible-book example.

## Checking the book and its metadata

Use <a href="https://kb.daisy.org/publishing/docs/epub/validation/overview.html" hreflang="en">DAISY's EPUB validation guidance</a> to combine structural checks with EPUBCheck, automated accessibility checks with Ace, and manual evaluation. Automated tools cannot establish every accessibility requirement, including whether alternative text is appropriate. Record metadata that reflects the evaluated publication.

## Other organisations and services

These previously contributed links provide examples of organisations and services in the e-book ecosystem. Inclusion is not an accessibility assessment.

- [BookBeat](https://bookbeat.com/)
- [Storytel](https://www.storytel.com/)
- [Bokus](https://www.bokus.com/e-bocker)
- [Kobo book search](https://www.kobo.com/gb/en/search?query=accessibility&fclanguages=en)
- [Kobo Sweden](https://www.kobo.com/se/sv)
- <a href="https://pocketbook.se/se-se" hreflang="sv">PocketBook</a>
- <a href="https://read.amazon.com/landing" hreflang="en">Amazon Kindle</a>
- [Celia](https://www.celia.fi/sv/bocker-och-material/elektroniska-bocker/)
- [Biblio](https://biblio.app/library)
