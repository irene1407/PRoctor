# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

- Persistent storage backend (PostgreSQL) to replace the in-memory review store
- Slack/email notifications when a critical-severity issue is found
- Support for reviewing GitHub Gist diffs

---

## [1.3.0] — 2025-05-29

### Added
- `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md` for open-source project standards
- GitHub issue templates (Bug Report, Feature Request) and PR template
- `CODEOWNERS` file for automatic review assignment on pull requests

---

## [1.2.0] — 2025-05-29

### Added
- **GitHub Actions CI/CD** — three automated workflows:
  - `tests.yml` — runs `pytest` with coverage on every push and PR
  - `pr_review_bot.yml` — posts AI review comment on every pull request
  - `weekly_retrain.yml` — collects new PR data and retrains the model every Sunday
- `scripts/retrain.py` — standalone retraining entry point for the Actions runner
- `scripts/review_pr.py` — standalone review entry point for the Actions runner

---

## [1.1.0] — 2025-05-29

### Added
- **Fine-tuning pipeline** — trains a custom `gpt-4o-mini` model on your repo's PR history
- `app/data_collector.py` — fetches closed PRs, extracts human review comments, filters noise
- `app/fine_tuner.py` — manages the full OpenAI fine-tuning lifecycle (upload → train → poll → save)
- `app/model_registry.py` — auto-selects the fine-tuned model when one is available; falls back to base model
- `notebooks/05_fine_tuning_pipeline.ipynb` — step-by-step walkthrough with cost estimation
- `tests/test_fine_tuner.py` — 14 unit tests covering data filtering, JSONL formatting, and registry

### Changed
- `app/ai_reviewer.py` — now calls `get_active_model()` so it automatically upgrades to the fine-tuned model with zero config

---

## [1.0.0] — 2025-05-29

### Added
- **Webhook server** (`app/webhook_handler.py`) — Flask app that listens for GitHub `pull_request` events
- **AI review engine** (`app/ai_reviewer.py`) — calls OpenAI with structured JSON output (severity, file, line, explanation, suggestion, score)
- **GitHub client** (`app/github_client.py`) — fetches PR diffs, posts review comments, verifies HMAC-SHA256 webhook signatures
- **Configuration** (`app/config.py`) — environment-based config with a carefully engineered system prompt
- **Dashboard** (`dashboard/index.html`) — live Chart.js dashboard showing score trends and severity breakdown
- **Manual review API** (`POST /api/review`) — test the reviewer without a webhook
- **Jupyter notebooks** — five notebooks covering setup, webhooks, AI analysis, dashboard, and fine-tuning
- **Unit tests** (`tests/test_ai_reviewer.py`) — covers JSON parsing, Markdown formatting, and OpenAI integration

[Unreleased]: https://github.com/OWNER/REPO/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/OWNER/REPO/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/OWNER/REPO/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/OWNER/REPO/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/OWNER/REPO/releases/tag/v1.0.0
