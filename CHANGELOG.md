# Change Log

This document records all notable changes to Librarian.

## 24.9

- Remove old API for HTML, TXT generators. Move to new API.
- The HTML format is changed:
    - text-elements now have 'wl' class and id attribute,
    - magic 'secN' ids are removed
    - 'a.target' elements removed
    - numbering anchors class changed to wl-num
- Removed all code related to art gallery.
- Drop Python 3.7.

## 24.5

- Smaller images in EPUB (600px width instead of 1200px).
- Convert PNG to JPEGs if too large in EPUBs.

## 24.4

- Add fundraising inserts in PDF.

## 24.1

- Added cover logos support.

## 23.12

- Added debug version for epub and epubcheck utility.

## 23.10

- Remove direct verse styling from HTML.

## 23.08

- Move statistics counter to L2 WLgit lDocument.

## 23.07.1

- Add <category.thema.main>.
- Support Python 3.7--3.11.

## 2.6.1

- Fix for better ignoring <extra>.

## 2.6

- Change default cover to marquise.
- Add support for full predesigned covers to marquise.
- Remove support for changing actual cover class via coverClass.

## 2.5.1

- Bugfix release.

## 2.5

- Add html-snippet builder.
- Remove DateValue class.
- Fix some texts and tests.
- Drop Python < 3.6. Up to 3.9 is supported.

## 2.4.13

- Added thema meta field.

## 2.4.12

- Fix for marquise cover: allow scaling title text in all layouts.

## 2.4.11.1

- Added assigning and preserving id attribute .

## 2.4.10

- Added <wers_srodek>, <tab>, <rownlolegle> and <blok>.

## 2.4.9

- Added verse counters to document statistics.

## 2.4.8 (2022-07-23)

# Changed
- Shortening authors and translators list on new cover.
- Update lxml.


## 2.4.7 (2022-07-18)

# Added
- Metadata types.

# Fixed
- Don't validate comment contents.
- Ignore translators on new cover if too long.


## 2.4.6 (2022-07-15)

# Fixed:
- Bug in reading child books.


## 2.4.5 (2022-07-08)

# Fixed
- Bug in reading picture XML.
- Bug in setting WLURI.slug


## 2.4.4 (2022-07-07)

### Fixed
- Packaging error.


## 2.4.3 (2022-06-07)

### Fixed
- Fix for new cover with custom size.


## 2.4.2 (2022-05-23)

### Fixed
- Error reporting on metadata parse error.


## 2.4.1 (2022-05-12)

### Added
- `category.legimi` metadata field

### Changed
- Fix PDF support for 'Geometric shapes' characters.
- Explicitly ignore unknown elements in v2 elements API.


## 2.4 (2022-05-06)

### Added
- New 'marquise' cover style.
- 'Factory' cover style with a QR code.


## 2.3.5 (2022-04-07)

### Fixed
- Support for www tag.
- Support for mat with inline text.


## 2.3.4 (2022-02-28)

### Fixed:
- Document stats totaling bug.
- Legimi cover background position.


## 2.3.3 (2021-12-23)

### Added:
- Line numbering reset with numeracja.


## 2.3.2 (2021-12-21)

### Fixed:
- Legimi cover colors.
- EPUB/MOBI TOC styling.


## 2.3.1 (2021-12-20)

### Fixed:
- Additional logos order.


## 2.3 (2021-12-20)

### Added:
- New MOBI builder.
- Document statistics.
- Legimi cover classes.

### Changed
- Default licensing info.


## 2.2 (2021-10-07)

### Added
- Support for block annotations.
- Option to use endnotes in PDF.

### Fixed
- Avoid hanging conjunctions on covers.


## 2.1 (2021-07-08)

### Added
- Basic document structure validation.
- Support for headers inside quotes in epub.


## 2.0 (2021-07-08)

### Added
- New Document API.
- New EPUB builder.
- New `librarian` entry point for converters.


## 1.15 (2021-03-02)

### Fixed
- Epub: translator marked with MARC Relators role 'trl'.
- Epub: authors and translators dc:creator elements had duplicate `id`.
- Epub: 'Start' element in TOC was added inconsistently and in wrong order.


## 1.14 (2021-02-05)

### Changed
- Image sources are now URLs. This changes the API: instead of paths
  given as `ilustr_path`, `transform` functions now accept
  a new `base_url` parameter.
- Size limits introduced for images in all formats.


## 1.13 (2021-01-27)

### Changed
- Responsive images in HTML. This changes the html.transform API.


## 1.12 (2021-01-27)

### Added
- Content warnings.


## 1.11.3 (2021-01-25)

### Fixed
- Missing items in EPUB TOC.


## 1.11.2 (2020-12-18)

### Fixed
- MathML in EPUBs.
- Subchapters without chapters in EPUBs.


## 1.11 (2020-12-09)

### Added

- Experimental DAISY builder.


## 1.10 (2020-11-09)

### Added

- Support for `ref` tags in HTML.


## 1.9 (2020-10-08)

### Added

- Experimental class-based builders for HTML and TXT.


### Changed

- Upgraded to EPUB 3, using ebooklib.



## 1.8.3 (2020-05-28)

### Fixed
- XML entities in MathML breaking PDF generation.
- Regression: verse numbering was lost.


## 1.8.2 (2020-04-03)

### Changed
- New Ebookpoint logo.


## 1.8.1 (2020-02-18)

### Changed
- Multiple authors on cover are now split into lines.


## 1.8 (2020-02-12)

### Added
- Support for tags: podtytul_*.
- Swappable CSS for HTML preview (as --css).
- First version of a test file in tests/uat.

### Changed
- Verses in HTML are now generated as div, not p, to prevent blank lines on copying.


## 1.7.8 (2020-02-05)

### Added
- Preliminary support for new tag: animacja.


## 1.7.7 (2019-12-31)

### Changed
- Allow multiple source.URL fields.

## 1.7.6 (2019-10-01)

### Changed
- Epub: only attach images referenced in the text.


## 1.7.5 (2019-08-19)

### Changed
- Updated information on the back of EPUB and PDF files.


## 1.7.4 (2019-08-01)

### Fixed
- `html.tranform_abstract` bytes vs text confusion.
- Tests.


## 1.7.3 (2019-07-31)

### Added
- Support for wl:coverLogoUrl, for adding cover logos.


## 1.7.2 (2019-03-12)

### Fixed
- Fix for Picture in Python 3: open image in binary mode.


## 1.7.1 (2019-03-01)

### Fixed
- Bug in cover generation.


## 1.7 (2019-02-27)

### Added
- Python 3.4+ support, to existing Python 2.7 support.
- `coverter_path` argument in `mobi.transform`.
- Proper packaging info.
- This changelog.
- Tox configuration for tests.

### Changed
- `from_bytes` methods replaced all `from_string` methods,
   i.e. on: OutputFile, WorkInfo, BookInfo, WLDocument, WLPicture.
- `get_bytes` replaced `get_string` on OutputFile.

### Removed
- Shims for Python < 2.7.
