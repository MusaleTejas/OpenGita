# Contributing to OpenGita

Thank you for your interest in contributing to OpenGita! As an open-source project, we welcome contributions of all forms, including bug reports, documentation improvements, feature suggestions, and code changes.

Please read through the guidelines below to ensure a smooth and productive collaboration.

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to the project maintainer at `tejasmusale830@gmail.com`.

---

## How to Contribute

### 1. Reporting Bugs
- Search the existing issues to ensure the bug hasn't already been reported.
- Create a new issue describing the problem, steps to reproduce, and environment details (Python version, OS, installed packages).

### 2. Suggesting Features
- Open an issue describing the proposed feature, use case, and potential API design.
- Wait for feedback from maintainers before starting work.

### 3. Submitting Code Changes

#### Setup Local Environment
1. Fork the repository on GitHub: `https://github.com/MusaleTejas/OpenGita`
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/OpenGita.git
   cd OpenGita
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```
4. Install dependencies and the package in editable mode:
   ```bash
   pip install -r requirements.txt  # If requirements.txt exists, or just build deps
   pip install -e .[dev]           # Or simply: pip install -e .
   ```

#### Developing the Pipeline
If you make changes to the raw dataset or normalization logic:
1. Run dataset normalization:
   ```bash
   python scripts/normalize_dataset.py
   ```
2. Verify integrity:
   ```bash
   python scripts/validate_dataset.py
   ```
3. Package data:
   ```bash
   python scripts/package_data.py
   ```

#### Code Style & Linting
We use **Ruff** for styling, formatting, and lint checks. Please run Ruff before submitting code:
```bash
ruff check .
```
You can automatically fix errors by running:
```bash
ruff check . --fix
```

#### Running Tests
Verify your changes by running the test suite:
```bash
python -m pytest
```
Ensure all tests pass before making a pull request.

---

## Pull Request Guidelines

1. Create a descriptive branch name (e.g. `feature/search-index` or `bugfix/verse-boundary`).
2. Keep your commits atomic and write clear, standard commit messages (prefer conventional commits, e.g. `feat: ...` or `fix: ...`).
3. Update unit tests to cover new behaviors.
4. Ensure the build passes and Ruff lint checks are clean.
5. Submit your pull request to the `main` branch.
