# Change Log

This document records all notable changes to Librarian.

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
