# 🤖 AI-Powered Code Review Assistant

A Python tool that integrates with GitHub pull requests to deliver context-aware, actionable code review feedback — powered by GPT-4o-mini.

> **Highlights for recruiters:** GitHub Webhook integration · OpenAI API · Flask REST API · Structured prompt engineering · Plotly dashboard · pytest unit tests · Jupyter notebooks

---

## What it does

When a developer opens or updates a pull request:

1. GitHub sends a webhook event to this server
2. The server fetches the full PR diff
3. GPT-4o-mini analyses the diff for bugs, security vulnerabilities, performance issues, and code quality
4. A structured, actionable review comment is posted back to the pull request automatically
5. Results are recorded and visualised on a live dashboard

**Example output posted to a PR:**

```
## 🤖 AI Code Review  —  Score: 4/10

**Summary:** This PR introduces a SQL injection vulnerability and lacks error handling on external calls.

### 🔴 [CRITICAL] SQL Injection via f-string
- **File:** `auth.py` — line ~10
- **Why:** User input is directly interpolated into the SQL query string.
- **Fix:** Use parameterised queries: `cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))`
```

---

## Architecture

```
GitHub PR event
      │
      ▼ HTTP POST (HMAC-SHA256 verified)
Flask webhook server  (/webhook)
      │
      ├── GitHubClient  — fetches diff, posts review comment
      └── AIReviewer    — calls OpenAI, returns structured JSON
                │
                └── Dashboard API  (/api/reviews, /api/stats)
                          │
                          └── dashboard/index.html  (live browser UI)
```

---

## Project Structure

```
ai-code-reviewer/
├── app/
│   ├── config.py           # Environment config & AI prompt
│   ├── github_client.py    # GitHub REST API wrapper + signature verification
│   ├── ai_reviewer.py      # OpenAI review engine + Markdown formatter
│   └── webhook_handler.py  # Flask server (webhook + dashboard API)
├── dashboard/
│   └── index.html          # Live review dashboard (Chart.js)
├── notebooks/
│   ├── 01_setup_and_exploration.ipynb   # Setup, fetch a real PR
│   ├── 02_github_webhook_handler.ipynb  # Webhooks, signatures, ngrok
│   ├── 03_ai_review_engine.ipynb        # Prompt engineering, OpenAI calls
│   └── 04_dashboard.ipynb               # Plotly charts, end-to-end demo
├── tests/
│   └── test_ai_reviewer.py  # pytest unit tests
├── .env.example
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/ai-code-reviewer.git
cd ai-code-reviewer
pip install -r requirements.txt
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env`:

| Variable | Where to get it |
|---|---|
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| `GITHUB_TOKEN` | https://github.com/settings/tokens — needs `repo` scope |
| `GITHUB_WEBHOOK_SECRET` | You choose this — set the same value in GitHub webhook settings |

### 3. Run the server

```bash
python -m flask --app app.webhook_handler run --port 5001
```

### 4. Expose locally with ngrok

```bash
ngrok http 5001
# Copy the https://xxxxx.ngrok-free.app URL
```

### 5. Set up the GitHub webhook

1. Go to `https://github.com/<org>/<repo>/settings/hooks`
2. Click **Add webhook**
3. Payload URL: `https://<ngrok-url>/webhook`
4. Content type: `application/json`
5. Secret: the value you set in `GITHUB_WEBHOOK_SECRET`
6. Events: select **Pull requests** only
7. Click **Add webhook**

### 6. Open a pull request

The bot will automatically post a review comment!

---

## Dashboard

Open `dashboard/index.html` in your browser while the server is running to see:
- Score trends across all reviewed PRs
- Issues by severity (critical / high / medium / low)
- A searchable list of recent reviews

---

## Fine-Tuning Pipeline

Train a custom model on your own team's PR history so reviews match your codebase's specific patterns, terminology, and standards.

```bash
# Open the fine-tuning notebook
cd notebooks && jupyter notebook 05_fine_tuning_pipeline.ipynb
```

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
|---|---|
| `app/data_collector.py` | GitHub PR history collector + quality filtering |
| `app/fine_tuner.py` | OpenAI fine-tuning job manager |
| `app/model_registry.py` | Auto-selects fine-tuned model when available |
| `notebooks/05_fine_tuning_pipeline.ipynb` | Full walkthrough with cost estimation |
| `tests/test_fine_tuner.py` | Unit tests for all new components |

---

## Jupyter Notebooks

Five step-by-step notebooks walk through every component:

```bash
cd notebooks
jupyter notebook
```

| Notebook | What you learn |
|---|---|
| `01_setup_and_exploration` | Fetch a real GitHub PR, explore the diff structure |
| `02_github_webhook_handler` | Webhooks, HMAC verification, ngrok setup |
| `03_ai_review_engine` | Prompt engineering, structured OpenAI output, real examples |
| `04_dashboard` | Plotly charts, end-to-end manual review, GitHub push checklist |
| `05_fine_tuning_pipeline` | Full ML lifecycle: data collection → training → deployment |

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Test Without a Webhook

Use the manual review endpoint directly:

```bash
curl -X POST http://localhost:5001/api/review \
  -H "Content-Type: application/json" \
  -d '{
    "diff": "### File: auth.py\n+password = \"admin123\"\n+query = f\"SELECT * FROM users WHERE name=\047{name}\047\"",
    "pr_title": "Add login"
  }'
```

---

## GitHub Actions (CI/CD)

Three automated workflows — no manual intervention needed once set up.

**Required GitHub Secrets** (Settings → Secrets → Actions):

| Secret | Value |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI key |
| `GH_TOKEN` | GitHub personal access token with `repo` scope |

### Workflows

| Workflow | Trigger | What it does |
|---|---|---|
| `tests.yml` | Every push & PR | Runs `pytest` and uploads coverage report |
| `pr_review_bot.yml` | Every pull request | Reviews the diff with AI and posts a comment |
| `weekly_retrain.yml` | Every Sunday 03:00 UTC | Collects new PR data and retrains the model |

The weekly retrain also commits the updated `model_id.txt` back to the repo, so the production server picks up the new model on next deploy.

You can also trigger retraining manually from the **Actions** tab → **Weekly Model Retrain** → **Run workflow**.

---

## Technical Challenges Solved

| Challenge | Solution |
|---|---|
| **Multi-file context** | Combine per-file patches into a single diff string with line-budget enforcement |
| **Non-generic feedback** | Structured JSON output with severity, file, line, explanation, and concrete suggestion fields |
| **Webhook security** | HMAC-SHA256 signature verification on every incoming request |
| **Hallucination control** | Low temperature (0.3) + strict JSON output format + negative instructions in system prompt |
| **Large diffs** | Truncation with per-file budget to stay within model context limits |
| **Continuous learning** | Scheduled fine-tuning pipeline collects new data and retrains weekly via GitHub Actions |

---

## Learning Outcomes

- **OpenAI API** — chat completions, prompt engineering, structured output parsing
- **GitHub REST API** — webhook handling, PR diff fetching, posting review comments
- **Flask** — REST API server, request validation, HMAC security middleware
- **Prompt engineering** — role assignment, output constraints, temperature tuning
- **Python tooling** — pytest, dotenv, Jupyter notebooks, Plotly

---

## License

MIT
