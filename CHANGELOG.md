# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.8.0] - 2025-12-12

### Added
- Add docstring, format code and solve pylint warnings
- update imports and improve type annotations across multiple modules
- refactor color type handling in backend and kinematics2d modules
- enhance game configuration validation and update imports in __init__.py
- add VerticalBounce class for vertical collision handling and integrate Bounds2D
- add movement control methods to Velocity2D class
- add RectCollider class for 2D collision detection and integrate into entity system
- implement entity management methods in Scene class
- add Size2D import and define scene size in Scene class
- add Entity import and define entities list in Scene class
- add 2D geometry, physics, and kinematics classes for improved entity handling

### Changed
- clean up import statements in test files
- remove deprecated properties from SpriteEntity and KinematicEntity

### Other
- Refactor tests and implement new test cases for game backend, scene management, and 2D physics
- Merge release/0.7 into develop

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
