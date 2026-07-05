# OpenGita

<p align="center">
  <a href="https://pypi.org/project/opengita/"><img src="https://img.shields.io/pypi/v/opengita.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/opengita/"><img src="https://img.shields.io/pypi/pyversions/opengita.svg" alt="Python versions"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
  <a href="https://github.com/MusaleTejas/OpenGita/actions"><img src="https://img.shields.io/github/actions/workflow/status/MusaleTejas/OpenGita/tests.yml?branch=main" alt="Build Status"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style"></a>
</p>

---

## Project Overview

**OpenGita** is a modern, high-performance, offline-first Python SDK for accessing Bhagavad Gita verses, chapters, translations, and commentaries. Designed for publication on GitHub and PyPI, OpenGita enables developers to build application integrations, educational platforms, and bots with structured Gita data.

The library uses a compiler-style build process where the raw dataset is parsed, validated, normalized, and pre-indexed. When installed, it loads the database exactly once into a thread-safe in-memory cache, offering zero-latency lookups without internet dependencies, databases, or API requirements.

---

## Features

- 📶 **100% Offline-First**: Built-in processed dataset. Zero network requests, databases, or cloud resources required.
- ⚡ **Zero IO Overhead**: The dataset is loaded and validated exactly once using a thread-safe singleton cache.
- 🛡️ **Pydantic v2 Types**: Strict compile-time and runtime type checking for all domain entities. No dictionaries or generic maps returned.
- 📚 **Rich Annotations**: Includes **18 chapters**, **701 canonical verses**, and **18 pushpikas (chapter colophons)**.
- ✍️ **Diverse Commentaries**: Leverages translations and commentaries from 22 distinct scholars (e.g. Adi Shankaracharya, Swami Sivananda, Ramanujacharya, and Swami Chinmayananda).
- 🔍 **Reverse Indexing**: Pre-built token-based inverted search index mapping words to verse boundaries.

---

## Why OpenGita?

Traditional Gita APIs require constant network connectivity, suffer from latency issues, and feature unstructured, error-prone JSON responses. OpenGita solves these problems:
1. **Developer Experience**: Auto-completion, docstrings, type hinting, and strict Pydantic schemas out of the box.
2. **Speed & Efficiency**: Ideal for serverless, edge computing, mobile, or offline applications, executing in sub-millisecond times.
3. **Data Quality**: Cleans whitespace, corrects numbering, and removes placeholder "did not comment" lines.

---

## Installation

Install OpenGita from PyPI:

```bash
pip install opengita
```

---

## Quick Start (Functional API)

OpenGita features a simple, beginner-friendly functional API at the top-level package. Functions return human-readable, pre-formatted strings directly.

```python
import opengita

# 1. Fetch a random canonical verse
print(opengita.get_random_verse())

# 2. Get a specific verse (Chapter 2, Verse 47)
print(opengita.get_verse(2, 47))

# 3. Get Chapter details
print(opengita.get_chapter(2))

# 4. Search verses containing a keyword
print(opengita.search("entitled"))

# 5. Get deterministic today's verse
print(opengita.today())

# 6. Get a random inspirational quote
print(opengita.get_random_quote())
```

---

## Command-Line Interface (CLI)

OpenGita includes a CLI tool when installed. Run commands directly from your terminal:

```bash
# Get a formatted random verse
opengita random

# Get today's verse
opengita today

# Get a specific verse
opengita verse 2 47

# Get chapter details
opengita chapter 2

# Search verses containing a keyword
opengita search karma
```

---

## Advanced API (Object-Oriented)

For programmatic access, integration, or custom formatting, you can use the object-oriented API which returns Pydantic data models.

### Initializing the Client
```python
from opengita import Gita

gita = Gita()
verse = gita.random() # Returns a Verse model object
```

### Verse Helper Methods
The `Verse` model exposes high-level helper methods for accessing translations, commentaries, and formatting options:

```python
# Get basic properties
print(verse.reference())               # Returns "Bhagavad Gita 10.32"
print(verse.sanskrit())                # Returns the raw Sanskrit text
print(verse.transliteration_text())    # Returns the English transliteration

# Get specific translations or commentaries with automatic preferred-author fallback
print(verse.translation("en"))         # Returns English translation
print(verse.translation("hi"))         # Returns Hindi translation
print(verse.commentary("en"))          # Returns English commentary

# List available metadata
print(verse.available_languages())     # e.g., ["en", "hi"]
print(verse.available_translators())   # List of translator names

# Export representations
print(verse.to_dict())                 # Returns a serializable Python dict
print(verse.to_json())                 # Returns a pretty-printed JSON string
print(verse.to_markdown())            # Returns a markdown formatted block
print(verse.to_html())                 # Returns an HTML structure
```

### Retrieving a Specific Commentary
```python
from opengita import Gita

gita = Gita()
v = gita.verse(1, 1)

commentary = next(
    (c.description for c in v.commentaries if c.author == "Swami Sivananda" and c.language == "en"),
    "No commentary found."
)
print(commentary)
```

### Retrieving Chapter Data
Get the original Sanskrit title and chapter meanings:
```python
from opengita import Gita

gita = Gita()
ch = gita.chapter(12)

print(f"Sanskrit title: {ch.name}")
print(f"English meaning: {ch.meaning['en']}")
print(f"Hindi meaning: {ch.meaning['hi']}")
```

---

## Project Architecture

### Folder Structure
```
OpenGita/
├── dataset/
│   ├── raw/                  # Raw unprocessed JSON files
│   └── processed/            # Generated JSON outputs (chapters, verses, metadata, search index)
├── packages/
│   └── python/
│       └── opengita/
│           ├── core/         # Settings & constants
│           ├── exceptions/   # SDK domain exceptions
│           ├── models/       # Pydantic v2 schemas
│           ├── data/         # Packaged processed dataset
│           ├── cache.py      # Singleton cached memory state
│           ├── loader.py     # Loader & validator
│           ├── randomizer.py # O(1) random verse selector
│           └── client.py     # Developer interface class (Gita)
├── scripts/                  # Normalization, validation & packaging scripts
└── tests/                    # Unit tests
```

### Dataset Pipeline
```
[raw/chapter] & [raw/slok]
         │
         ▼  (scripts/normalize_dataset.py)
[dataset/processed/*.json]
         │
         ▼  (scripts/validate_dataset.py)
[Integrity Verification Checks]
         │
         ▼  (scripts/package_data.py)
[opengita/data/*.json] (packaged local data)
```

### SDK Design
The SDK follows a clean architecture pattern:
1. **Client** (`Gita`): Exposes methods (`random`, `verse`, `chapter`, `statistics`) to users.
2. **DataLoader**: Manages file retrieval and deserialization into domain models.
3. **GitaCache**: A thread-safe singleton protecting in-memory dataset instances.
4. **Domain Models**: Immutable Pydantic v2 models representation.

---

## API Overview

### Gita Client Methods

- **`random() -> Verse`**: Returns a random canonical verse (excluding pushpikas).
- **`verse(chapter: int, verse: int) -> Verse`**: Lookups verse, raising `VerseNotFound` or `ChapterNotFound` if parameters are invalid.
- **`chapter(number: int) -> Chapter`**: Lookups chapter details, raising `ChapterNotFound` if out of bounds.
- **`statistics() -> GitaStatistics`**: Exposes statistical details about translators, commentators, and file counts.

---

## Example Output

Running `python examples/example.py` yields:

```text
Initializing OpenGita SDK...

1. Fetching Chapter 2...
┌───────────────────────────────── Chapter 2 ─────────────────────────────────┐
│ Sanskrit Title: सांख्ययोग                                                       │
│ Translation: Sankhya Yoga (Sānkhya Yog)                                     │
│ Meaning: Transcendental Knowledge                                           │
│ Verses Count: 72                                                            │
│                                                                             │
│ Summary (English): The second chapter of the Bhagavad Gita is Sankhya Yoga. │
│ This is the most important chapter of the Bhagavad Gita as Lord Krishna     │
│ condenses the teachings of the entire Gita in this chapter.                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Roadmap

- **v0.1.0 (Current)**: Core SDK lookup functions, singleton cache, dataset processing.
- **v0.2.0**: In-memory text search engine (exact, partial, keyword) using pre-built search index.
- **v0.3.0**: Developer CLI using Typer and Rich formatting.
- **v0.4.0**: Local web server API support via FastAPI.

---

## Contributing

We welcome contributions to OpenGita! Please see our [Contributing Guide](CONTRIBUTING.md) for setup details and code standards.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## FAQ

#### How is this offline?
The normalized JSON dataset is compiled and copied directly into the python package folder `opengita/data/`. When installed, it reads this packaged data using standard python `importlib.resources`.

#### Can I fetch pushpikas?
Yes! Standard verses are indexed 1 to `verses_count`. The chapter pushpika (colophon declaration) is available at `verses_count + 1`. Calling `verse(1, 48)` will return the pushpika for Chapter 1.

---

## Acknowledgements

- Traditional scholars whose translations and commentaries are indexed in the raw dataset.
- The open-source Python community.

---

## Author

- **Name**: Tejas Musale
- **GitHub**: [@MusaleTejas](https://github.com/MusaleTejas)
- **LinkedIn**: [Tejas Musale](https://www.linkedin.com/in/tejas-musale)
- **Email**: tejasmusale830@gmail.com
- **Repository**: [GitHub Repository](https://github.com/MusaleTejas/OpenGita.git)
