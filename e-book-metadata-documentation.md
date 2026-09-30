# E-book metadata
For the user it is very important that the metadata is available on each individual book and as filters to search for. The metadata needs to be in an easy to understand format, not only WCAG levels or technical labels.
## E-books in the EAA
### Definition of E-Books in the EAA
> <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019L0882#anx_VI:~:text=consumer%20banking%20transactions.-,(41),E%2Dbook,-files%20are%20based" hreflang="en">(41) E-book files</a> are based on a electronic computer coding that enables the circulation and consultation of a mostly textual and graphical intellectual work. The degree of precision of this coding determines the accessibility of e-book files, in particular regarding the qualification of the different constitutive elements of the work and the standardised description of its structure. The interoperability in terms of accessibility should optimise the compatibility of those files with the user agents and with current and future assistive technologies. Specific features of special volumes like comics, children’s books and art books should be considered in the light of all applicable accessibility requirements. Divergent accessibility requirements in Member States would make it difficult for publishers and other economic operators to benefit from the advantages of the internal market, could create interoperability problems with e-readers and would limit the access for consumers with disabilities. In the context of e-books, the concept of a service provider could include publishers and other economic operators involved in their distribution.
### Demands on E-books in the EAA
<a href="https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019L0882#anx_VI:~:text=(f)-,E%2Dbooks%3A,-(i)" hreflang="en">(f) E-books:</a>

> - (i) ensuring that, when an e-book contains audio in addition to text, it then provides synchronised text and audio;
> - (ii) ensuring that e-book digital files do not prevent assistive technology from operating properly;
> - (iii) ensuring access to the content, the navigation of the file content and layout including dynamic layout, the provision of the structure, flexibility and choice in the presentation of the content;
> - (iv) allowing alternative renditions of the content and its interoperability with a variety of assistive technologies, in such a way that it is perceivable, understandable, operable and robust;
> - (v) making them discoverable by providing information through metadata about their accessibility features;
> - (vi) ensuring that digital rights management measures do not block accessibility features.
  
## Actors on the market
Some examples of different actors on the market.
1. E-book providers
    - Services
      - [Bookbeat](https://bookbeat.com/)
      - [Storytel](https://www.storytel.com/) 
    - E-commerce actors
      - [Bokus.com](https://www.bokus.com/e-bocker)
      - [Rakuten kobo book store](https://www.kobo.com/gb/en/search?query=accessibility&fclanguages=en)
    - E-book readers
      - [Kobo](https://www.kobo.com/se/sv)
      - <a href="https://pocketbook.se/se-se" hreflang="sv">Pocketbook</a>
      - <a href="https://read.amazon.com/landing" hreflang="en">Amazon kindle</a>
3. E-book Publishers
    - Private publishers
    - Libraries (such as [Celia](https://www.celia.fi/sv/bocker-och-material/elektroniska-bocker/), [Biblio](https://biblio.app/library))
  
## How to document
If you use statement and data as Finland proposes, you could assume to be covered for all other countries - even if they differ a bit. Seems so far that Finland is the only country being both clear and strict.

If you construct a table of metadata it should be enough. Who would use a statement based on ONIX data? That does not make sense..

In the directive it says you ensure that it works for everyone using accessibility tools and that it is flexible in use, and more.

1. On site level and app level you need to present an accessibility statement for the service accessibility.
2. On a product (book) level you need to have the metadata for the book embedded.
3. In search and filters you need to be able to use the metadata.
4. On the presentation page for the book, display metadata visually.

## Meta-data resources

<a href="https://ns.editeur.org/onix/en/196" hreflang="en">ONIX codelists Issue 69</a> – list 196  ONIX-format
<a href="https://schema.org/Book" hreflang="en">Book - Schema.org Type</a>  Schema.org-format (with <a href="https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/#accessibilityControl-vocabulary" hreflang="en">referenced vocabulary</a>)

For guidance on presenting accessibility metadata, see the <a href="https://www.w3.org/publishing/a11y/metadata-display-guide/guidelines/" hreflang="en">Accessibility Metadata Display Guide for Digital Publications 2.1</a>.

Recommended metadata to send to publishers <a href="https://www.w3.org/TR/epub-a11y-11/" hreflang="en">EPUB Accessibility 1.1</a>

### Example of metadata

See the [W3C example of accessibility metadata in an EPUB package document](https://w3c.github.io/publ-a11y/package-metadata-authoring-guide/#examples).

### Accessible E-book example
[The Death of Shame ebook by Ambrose Parry - Rakuten Kobo](https://www.kobo.com/gb/en/ebook/the-death-of-shame) where they present the metadata in clear language.

Kobo currently has a "Yes/ No" filter for accessibility with a plan to expand the filters soon.
