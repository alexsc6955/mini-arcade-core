# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.7.5] - 2025-12-05

### Fixed
- handle exceptions in image saving process in Game class

## [0.7.4] - 2025-12-05

### Added
- add BMP to image conversion method in Game class and update dependencies
- enhance documentation with type hints and parameter descriptions across multiple modules

### Other
- Merge branch 'release/0.7' of https://github.com/alexsc6955/mini-arcade-core into release/0.7
- Merge branch 'release/0.7' of https://github.com/alexsc6955/mini-arcade-core into release/0.7

## [0.7.3] - 2025-12-05

### Added
- enhance documentation with type hints and parameter descriptions across multiple modules

### Other
- Merge branch 'release/0.7' of https://github.com/alexsc6955/mini-arcade-core into release/0.7

## [0.7.2] - 2025-12-05

### Added
- implement overlay management methods in Scene class

## [0.7.1] - 2025-12-05

### Added
- add capture_frame method to Backend protocol and implement screenshot method in Game class

## [0.7.0] - 2025-12-05

### Added
- add set_clear_color method to Backend protocol and update Game to use background_color
- add draw_text method to Backend protocol for rendering text

### Other
- Merge pull request #6 from alexsc6955/develop
- Merge pull request #5 from alexsc6955/feature/text_support
- Merge release/0.6 into develop

## [0.6.1] - 2025-12-04

### Added
- implement game loop and scene management in Game class

### Other
- Merge pull request #4 from alexsc6955/feature/game_loop
- Merge release/0.5 into develop
- Merge release/0.5 into main

## [0.5.3] - 2025-12-04

### Changed
- simplify version retrieval logic in __init__.py

### Other
- Merge branch 'release/0.5' of https://github.com/alexsc6955/mini-arcade-core into release/0.5

## [0.5.2] - 2025-12-04

### Changed
- enhance logging in get_version function and add logging configuration

### Other
- Merge branch 'release/0.5' of https://github.com/alexsc6955/mini-arcade-core into release/0.5

## [0.5.1] - 2025-12-04

### Fixed
- add print statement to indicate package not found in get_version function

## [0.5.0] - 2025-12-03

### Added

- add version retrieval function and handle exceptions gracefully

### Fixed

- improve docstring for get_version function to clarify return type and exceptions

## [0.4.0] - 2025-12-03

### Added

- Initial documented release. Earlier versions (0.1.0–0.3.0) are not listed here.
