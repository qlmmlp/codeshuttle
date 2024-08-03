# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Simplified project structure by consolidating all core functionality into a single `codeshuttle.py` file.
- Removed separate `cli.py`, `file_change.py`, `file_handler.py`, `logger.py`, and `parser.py` files.
- Integrated `FileChange`, `Parser`, `FileHandler`, and `Logger` classes directly into `codeshuttle.py`.
- Updated `__init__.py` to import all classes from `codeshuttle.py`.
- Simplified `setup.py` to use `codeshuttle.codeshuttle:main` as the entry point.

### Removed
- Removed support for clipboard input (`pb` option) and related `pyperclip` dependency.
- Removed `--output` option for generating change reports.
- Removed extensive error handling and file system checks.

### Added
- Added `sample_changes.txt` in `tests/data/` for testing purposes.

## [0.1.5] - 2023-12-01
### Added
- Improved error handling for file operations.
- Added support for relative file paths in input.

### Changed
- Updated documentation to reflect new usage patterns.
- Refactored internal file parsing logic for better performance.

### Fixed
- Fixed a bug where empty lines in input would cause parsing errors.

## [0.1.0] - 2023-07-15
### Added
- Initial release of CodeShuttle

[Unreleased]: https://github.com/username/codeshuttle/compare/v0.1.5...HEAD
[0.1.5]: https://github.com/username/codeshuttle/compare/v0.1.0...v0.1.5
[0.1.0]: https://github.com/username/codeshuttle/releases/tag/v0.1.0