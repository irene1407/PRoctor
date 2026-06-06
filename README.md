<!-- Header -->
<div align="center">

```
██████╗ ██████╗  ██████╗  ██████╗████████╗ ██████╗ ██████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝██████╔╝██║   ██║██║        ██║   ██║   ██║██████╔╝
██╔═══╝ ██╔══██╗██║   ██║██║        ██║   ██║   ██║██╔══██╗
██║     ██║  ██║╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
```
### Your AI code reviewer that never sleeps, never misses a bug, and costs $0 to run.
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Ollama](https://img.shields.io/badge/Ollama-Llama_3-FF6C37?style=for-the-badge)](https://ollama.com)
[![GitHub](https://img.shields.io/badge/GitHub-Webhook-181717?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/en/webhooks)
[![GitHub Webhooks](https://img.shields.io/badge/GitHub-Webhook-181717?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/en/webhooks)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)
</div>
<h3>What is PRoctor?</h3>
<p>PRoctor is a fully automated code review bot. The moment a developer opens a pull request on GitHub, PRoctor wakes up, reads every line of changed code, and posts a structured review comment — flagging security vulnerabilities, bugs, and performance issues — all powered by a locally-running Llama 3 model.<br>
**No cloud API. No monthly bill. No data leaving your machine.**</p>
<h3>How it Works</h3> 

<div align="center">

<h4>Developer opens a PR</h4>
▼

<table>
<tr>
<td bgcolor="#161b22"><b>GitHub Webhook</b></td>
<td bgcolor="#161b22">fires instantly on PR open / update</td>
</tr>
</table>

<sub>HTTP POST (HMAC-SHA256 signed)</sub><br>
▼

<table>
<tr>
<td bgcolor="#161b22"><b>Flask Server</b></td>
<td bgcolor="#161b22">verifies signature, extracts metadata</td>
</tr>
</table>

▼

<table>
<tr>
<td bgcolor="#161b22"><b>GitHub API</b></td>
<td bgcolor="#161b22">fetches the full diff across all changed files</td>
</tr>
</table>

▼

<table>
<tr>
<td bgcolor="#161b22"><b>AI Reviewer</b></td>
<td bgcolor="#161b22">builds structured prompt, calls Ollama</td>
</tr>
</table>

▼

<table>
<tr>
<td bgcolor="#161b22"><b>Ollama Llama 3</b></td>
<td bgcolor="#161b22">100% local — zero cost, zero data leakage</td>
</tr>
</table>

<sub>structured JSON</sub><br>
▼

<table>
<tr>
<td bgcolor="#161b22"><b>GitHub PR Bot</b></td>
<td bgcolor="#161b22">formats as Markdown, posts comment on the PR</td>
</tr>
</table>

</div>

---

<h3>DEMO</h3>

See PRoctor in action reviewing a Pull Request containing a critical SQL injection vulnerability:

<div align="center">
  <img src="screenshots\pr-review.png" alt="PRoctor Code Review Demo" width="800px" />
</div>

---

<h3>System Architecture</h3>

PRoctor functions as a distributed local-first middleware system that bridges your secure local environment with GitHub's event ecosystem.

<div align="center">
  <img src="screenshots\architecture.png" alt="PRoctor System Architecture Diagram" width="800px" />
</div>

---

<h3>FEATURES</h3>

| Feature | Details |
| :--- | :--- |
| 🔒 **Security scanning** | SQL injection, hardcoded secrets, unsafe deserialization, XSS |
| 🐛 **Bug detection** | Logic errors, missing error handling, null pointer risks |
| ⚡ **Performance flags** | N+1 queries, unnecessary loops, blocking I/O |
| 📊 **Severity scoring** | Every issue rated Critical / High / Medium / Low |
| 💯 **Quality score** | Each PR gets a 1–10 score posted on the comment |
| 🏠 **100% local AI** | Runs on your machine via Ollama — no external API calls |
| 🔐 **Secure webhooks** | HMAC-SHA256 signature verification on every request |
| 📋 **Structured output** | Machine-parseable JSON → readable Markdown in one step |
| 🔄 **Auto-triggered** | Fires on PR open, update, and reopen — zero manual steps |
| 🧪 **Fully tested** | 22 unit tests with pytest covering all core modules |

---

<h3>TECH STACK</h3>

```text
Language      Python 3.11
Web server    Flask 3.0
AI engine     Ollama (Llama 3 — runs locally)
GitHub        REST API v3 + Webhooks
Tunnelling    ngrok (exposes local server during development)
Testing       pytest + unittest.mock
CI/CD         GitHub Actions (3 automated workflows)
```
---

<h3>PROJECT STRUCTURE</h3>
## PROJECT STRUCTURE

```text
PRoctor/
├── app/
│   ├── webhook_handler.py    # Flask server, webhook endpoint
│   ├── ai_reviewer.py        # Prompt engineering + response parser
│   ├── github_client.py      # GitHub API wrapper + HMAC verification
│   ├── config.py             # Environment config + system prompt
│   ├── data_collector.py     # Collects PR history for fine-tuning
│   ├── fine_tuner.py         # Fine-tuning pipeline manager
│   └── model_registry.py     # Auto-selects fine-tuned model if available
├── notebooks/
│   ├── 01_setup_and_exploration.ipynb
│   ├── 02_github_webhook_handler.ipynb
│   ├── 03_ai_review_engine.ipynb
│   ├── 04_dashboard.ipynb
│   └── 05_fine_tuning_pipeline.ipynb
├── scripts/
│   ├── retrain.py            # Weekly fine-tuning runner (GitHub Actions)
│   └── review_pr.py          # PR review runner (GitHub Actions)
├── .github/
│   └── workflows/
│       ├── tests.yml          # Run pytest on every push
│       ├── pr_review_bot.yml  # Auto-review every PR
│       └── weekly_retrain.yml # Retrain model every Sunday
├── dashboard/
│   └── index.html            # Live review dashboard (Chart.js)
├── tests/                    # 22 pytest unit tests
├── requirements.txt
├── .env.example
└── README.md
```
## Quick Start
### 1. Clone and install
```bash
git clone https://github.com/<your-username>/ai-code-reviewer.git
cd ai-code-reviewer
```
## Installation
### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com/download) installed
- A GitHub account + personal access token (`repo` scope)
- [ngrok](https://ngrok.com/download) (free account)
---
### — Clone the repo
```
bash
git clone https://github.com/YOUR-USERNAME/PRoctor.git
cd PRoctor
```

### — Install dependencies
```bash
pip install -r requirements.txt
```
### — Download the AI model
```bash
ollama pull llama3
```
### — Set up environment variables
```bash
cp .env.example .env
```
| Variable | Where to get it |
| :--- | :--- |
| `OPENAI_API_KEY` | [OpenAI API Keys](https://platform.openai.com/api-keys) |
| `GITHUB_TOKEN` | [GitHub Token Settings](https://github.com/settings/tokens) — requires **`repo`** scope |
| `GITHUB_WEBHOOK_SECRET` | You choose this — set the exact same value inside your GitHub repository webhook settings |

### 2. Run the server
Open `.env` and fill in:
```env
GITHUB_TOKEN=ghp_your_token_here
GITHUB_WEBHOOK_SECRET=pick_any_password
FLASK_SECRET_KEY=another_random_string
PORT=5001
```
### — Start the Flask server
```bash
python -m flask --app app.webhook_handler run --port 5001
```
### — Expose it with ngrok
```bash
ngrok http 5001
# Copy the https://xxxxx.ngrok-free.app URL
```
### 3.Webhook Configuration
Follow these steps to link your local server instance directly to your GitHub repository:
1. Navigate to your repository page on GitHub, then go to **Settings** → **Webhooks** → **Add webhook**.
2. Configure the configuration fields with the matching parameter metrics:
| Field | Value / Setting |
| **Payload URL** | Your active public tunnel address (e.g., `https://xxxxx.ngrok-free.app/webhook`) |
| **Content type** | `application/json` |
| **Secret** | The exact string sequence assigned to `GITHUB_WEBHOOK_SECRET` in your `.env` profile |
| **Trigger Events** | Select **Let me select individual events**, check **Pull requests**, and disable everything else. |

---
### 4. Open a Pull Request

**The bot will automatically post a review comment!**

---

## 5.Dashboard

Open `dashboard/index.html` in your browser while the server is running to view live metrics:
* **Score trends** across all reviewed PRs
* **Issues by severity** (Critical / High / Medium / Low)
* A **searchable list** of recent reviews

---

## 6.Fine-Tuning Pipeline

Train a custom model on your own team's PR history so reviews accurately match your codebase's specific patterns, terminology, and engineering standards.

```bash
# Open the fine-tuning workflow notebook
cd notebooks && jupyter notebook 05_fine_tuning_pipeline.ipynb
The pipeline:
1. **Collect** — fetches closed PRs and extracts human reviewer comments as training labels
2. **Filter** — removes bot-authored, generic ("LGTM"), and trivially short examples
3. **Format** — converts to OpenAI JSONL fine-tuning format (system / user / assistant)
4. **Estimate** — calculates token count and cost before any charges
5. **Train** — uploads data and starts a supervised fine-tuning job on `gpt-4o-mini`
6. **Activate** — saves the model ID; `AIReviewer` auto-detects and uses it immediately
7. **Compare** — side-by-side output comparison: base model vs fine-tuned model
New files added for this pipeline:
| File | Purpose |
```
### Fine-Tuning Pipeline Components

The underlying code tracking framework includes specialized pipeline infrastructure to support custom model fine-tuning jobs:

| Component File Path | Core Operational Responsibility |
| :--- | :--- |
| `app/data_collector.py` | Pulls GitHub PR history records and applies automated dataset quality filtering layers. |
| `app/fine_tuner.py` | Orchestrates and manages background OpenAI fine-tuning job submissions. |
| `app/model_registry.py` | Dynamically auto-selects your fine-tuned model variants whenever they are available. |
| `notebooks/05_fine_tuning_pipeline.ipynb` | Comprehensive walkthrough notebook detailing pipeline engineering with interactive cost estimation. |
| `tests/test_fine_tuner.py` | Dedicated test suite executing unit tests across all newly integrated pipeline modules. |
---
## 7.Jupyter Notebooks
Five step-by-step notebooks walk through every component:
```bash
cd notebooks
jupyter notebook
```
| Notebook | What you learn |
| `01_setup_and_exploration` | Fetch a real GitHub PR, explore the diff structure |
| `02_github_webhook_handler` | Webhooks, HMAC verification, n...
[truncated]
[truncated]
[truncated]
## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <strong>Built with Python, Flask, and Llama 3</strong> &nbsp;|&nbsp; <strong>Runs 100% locally</strong> &nbsp;|&nbsp; <strong>Zero API cost</strong>
</div>
