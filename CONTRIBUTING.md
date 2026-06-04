# Contributing to AI Code Review Assistant

Thank you for your interest in contributing! This document covers everything you need to get started.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Running Tests](#running-tests)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/ai-code-reviewer.git
   cd ai-code-reviewer
   ```
3. Add the upstream remote so you can pull future updates:
   ```bash
   git remote add upstream https://github.com/<original-owner>/ai-code-reviewer.git
   ```

---

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Copy environment config
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and GITHUB_TOKEN

# Verify everything works
pytest tests/ -v
```

---

## How to Contribute

### Fixing a bug

1. Check the [Issues](../../issues) page to see if it is already reported
2. If not, open a new bug report using the **Bug Report** template
3. Create a branch: `git checkout -b fix/short-description`
4. Make your changes and add a test that covers the bug
5. Open a pull request

### Adding a feature

1. Open a [Feature Request](../../issues/new?template=feature_request.md) issue first to discuss the idea
2. Wait for maintainer feedback before writing code — this avoids wasted effort
3. Create a branch: `git checkout -b feat/short-description`
4. Implement the feature with tests
5. Update the relevant notebook(s) if the feature affects the learning flow
6. Open a pull request

### Improving docs or notebooks

Branch name: `docs/short-description`

No issue required for small doc fixes — open a PR directly.

---

## Pull Request Process

1. **Keep PRs focused** — one logical change per PR
2. **Tests required** — all new code must have corresponding tests in `tests/`
3. **CI must pass** — the `tests.yml` workflow runs automatically; fix any failures before requesting review
4. **Update the README** if you add a new module, script, or workflow
5. Fill in the PR template completely — this speeds up review

Your PR will be reviewed within a few days. Maintainers may request changes; please respond promptly.

---

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for formatting
- Use type hints on all function signatures
- Docstrings for every public function and class (one-line OK for simple helpers)
- No `print()` in library code — use `logging` instead
- Keep functions short and single-purpose

Run a quick style check before pushing:
```bash
python -m py_compile app/*.py scripts/*.py
```

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=app --cov-report=term-missing

# Single file
pytest tests/test_ai_reviewer.py -v
```

Tests must pass before a PR can be merged. If you are adding a new module, add a corresponding `tests/test_<module>.py` file.

---

## Reporting Bugs

Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) template. Please include:

- What you expected to happen
- What actually happened (with the full error message/traceback)
- Steps to reproduce
- Your Python version and OS

---

## Suggesting Features

Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template. Describe:

- The problem you are trying to solve
- Your proposed solution
- Any alternatives you considered

---

## Questions?

Open a [Discussion](../../discussions) rather than an issue for general questions.
