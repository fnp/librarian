# Change Log

This document records all notable changes to Librarian.


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
