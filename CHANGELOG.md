# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-05

### Added
- **Core SDK**: Main `Gita` client exposing thread-safe local Bhagavad Gita verse, chapter, random, and statistical data.
- **Data Models**: Strict type checking via Pydantic v2 schemas: `Chapter`, `Verse`, `Translation`, `Commentary`, and `GitaStatistics`.
- **Memory Caching**: Thread-safe singleton cache class `GitaCache` loading and parsing datasets exactly once.
- **O(1) Randomizer**: Fast random canonical verse extraction `GitaRandomizer` excluding colophon/pushpika verses.
- **Normalization Pipeline**: Pre-compilation processing script `normalize_dataset.py` supporting key normalization, stable ID generation (`BG{chapter}.{verse}`), and lowercase token-based reverse indexing.
- **Sanity Validation**: Verification script `validate_dataset.py` verifying chapter counts (18), canonical verse counts (701), pushpika counts (18), and Pydantic model serialization.
- **Packaging Pipeline**: Setup script `package_data.py` moving processed dataset files inside the Python package under `opengita/data/`.
- **Test Suites**: Pytest coverage for data loader, models validation, Gita client, and random verse distributions.
- **Aesthetic Example**: Custom `example.py` formatting Gita verses with colors and boxes using the `Rich` framework.
- **Community Health**: Introduced `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and clean `.gitignore`.
