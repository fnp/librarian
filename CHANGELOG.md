# Change Log

This document records all notable changes to Librarian.


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
