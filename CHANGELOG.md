# Change Log

This document records all notable changes to Librarian.

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