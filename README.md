# 🤖 AI-Powered Code Review Assistant
2
 
3
A Python tool that integrates with GitHub pull requests to deliver context-aware, actionable code review feedback — powered by GPT-4o-mini.
4
 
5
> **Highlights for recruiters:** GitHub Webhook integration · OpenAI API · Flask REST API · Structured prompt engineering · Plotly dashboard · pytest unit tests · Jupyter notebooks
6
 
7
---
8
 
9
## What it does
10
 
11
When a developer opens or updates a pull request:
12
 
13
1. GitHub sends a webhook event to this server
14
2. The server fetches the full PR diff
15
3. GPT-4o-mini analyses the diff for bugs, security vulnerabilities, performance issues, and code quality
16
4. A structured, actionable review comment is posted back to the pull request automatically
17
5. Results are recorded and visualised on a live dashboard
18
 
19
**Example output posted to a PR:**
20
 
21
```
22
## 🤖 AI Code Review  —  Score: 4/10
23
 
24
**Summary:** This PR introduces a SQL injection vulnerability and lacks error handling on external calls.
25
 
26
### 🔴 [CRITICAL] SQL Injection via f-string
27
- **File:** `auth.py` — line ~10
28
- **Why:** User input is directly interpolated into the SQL query string.
29
- **Fix:** Use parameterised queries: `cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))`
30
```
31
 
32
---
33
 
34
## Architecture
35
 
36
```
37
GitHub PR event
38
      │
39
      ▼ HTTP POST (HMAC-SHA256 verified)
40
Flask webhook server  (/webhook)
41
      │
42
      ├── GitHubClient  — fetches diff, posts review comment
43
      └── AIReviewer    — calls OpenAI, returns structured JSON
44
                │
45
                └── Dashboard API  (/api/reviews, /api/stats)
46
                          │
47
                          └── dashboard/index.html  (live browser UI)
1
<!-- Header -->
2
<div align="center">
3
 
4
```
5
██████╗ ██████╗  ██████╗  ██████╗████████╗ ██████╗ ██████╗
6
██╔══██╗██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
7
██████╔╝██████╔╝██║   ██║██║        ██║   ██║   ██║██████╔╝
8
██╔═══╝ ██╔══██╗██║   ██║██║        ██║   ██║   ██║██╔══██╗
9
██║     ██║  ██║╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
10
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
11
```
12
 
13
### Your AI code reviewer that never sleeps, never misses a bug, and costs $0 to run.
14
 
15
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
16
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
17
[![Ollama](https://img.shields.io/badge/Ollama-Llama_3-FF6C37?style=for-the-badge)](https://ollama.com)
18
[![GitHub](https://img.shields.io/badge/GitHub-Webhook-181717?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/en/webhooks)
19
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
20
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)
21
 
22
</div>
23
 
24
---
25
 
26
## What is PRoctor?
27
 
28
**PRoctor** is a fully automated code review bot. The moment a developer opens a pull request on GitHub, PRoctor wakes up, reads every line of changed code, and posts a structured review comment — flagging security vulnerabilities, bugs, and performance issues — all powered by a locally-running Llama 3 model.
29
 
30
**No cloud API. No monthly bill. No data leaving your machine.**
31
 
32
---
33
 
34
## See it in action
35
 
36
```
37
Developer opens a PR
38
         │
39
         ▼
40
  ┌─────────────────┐
41
  │  GitHub Webhook  │  fires instantly on PR open / update
42
  └────────┬────────┘
43
           │  HTTP POST (HMAC-SHA256 signed)
44
           ▼
45
  ┌─────────────────┐
46
  │   Flask Server   │  verifies signature, extracts metadata
47
  └────────┬────────┘
48
           │
49
           ▼
50
  ┌─────────────────┐
51
  │   GitHub API    │  fetches the full diff across all changed files
52
  └────────┬────────┘
53
           │
54
           ▼
55
  ┌─────────────────┐
56
  │  AI Reviewer    │  builds structured prompt, calls Ollama
57
  └────────┬────────┘
58
           │
59
           ▼
60
  ┌─────────────────┐
61
  │  Ollama Llama 3 │  100% local — zero cost, zero data leakage
62
  └────────┬────────┘
63
           │  structured JSON
64
           ▼
65
  ┌─────────────────┐
66
  │  GitHub PR Bot  │  formats as Markdown, posts comment on the PR
67
  └─────────────────┘
68
```
69
 
70
---
71
 
72
## Demo
73
 
74
> PRoctor reviewing a PR that contains a SQL injection vulnerability:
75
 
76
```
77
## 🤖 PRoctor Review — Score: 4/10
78
 
79
**Summary:** This PR introduces a critical SQL injection vulnerability
80
and a hardcoded credential that will be exposed in version control.
81
 
82
### 🔴 [CRITICAL] SQL Injection via f-string interpolation
83
- **File:** `login.py` — line ~10
84
- **Why:** User input is directly embedded in the SQL string.
85
          An attacker can input `' OR '1'='1` to bypass authentication.
86
- **Fix:** cursor.execute('SELECT * FROM users WHERE name = %s', (username,))
87
 
88
### 🟠 [HIGH] Hardcoded password in source code
89
- **File:** `config.py` — line ~3
90
- **Why:** Credentials committed to git history are permanent,
91
          even after deletion.
92
- **Fix:** Use os.getenv('DB_PASSWORD') and add .env to .gitignore
93
 
94
---
95
*Posted by PRoctor — powered by Llama 3 (local)*
96
```
97
 
98
---
99
 
100
## Features
101
 
102
| Feature | Details |
103
|---|---|
104
| 🔒 **Security scanning** | SQL injection, hardcoded secrets, unsafe deserialization, XSS |
105
| 🐛 **Bug detection** | Logic errors, missing error handling, null pointer risks |
106
| ⚡ **Performance flags** | N+1 queries, unnecessary loops, blocking I/O |
107
| 📊 **Severity scoring** | Every issue rated Critical / High / Medium / Low |
108
| 💯 **Quality score** | Each PR gets a 1–10 score posted on the comment |
109
| 🏠 **100% local AI** | Runs on your machine via Ollama — no external API calls |
110
| 🔐 **Secure webhooks** | HMAC-SHA256 signature verification on every request |
111
| 📋 **Structured output** | Machine-parseable JSON → readable Markdown in one step |
112
| 🔄 **Auto-triggered** | Fires on PR open, update, and reopen — zero manual steps |
113
| 🧪 **Fully tested** | 22 unit tests with pytest covering all core modules |
114
 
115
---
116
 
117
## Tech Stack
118
 
119
```
120
Language      Python 3.11
121
Web server    Flask 3.0
122
AI engine     Ollama (Llama 3 — runs locally)
123
GitHub        REST API v3 + Webhooks
124
Tunnelling    ngrok (exposes local server during development)
125
Testing       pytest + unittest.mock
126
CI/CD         GitHub Actions (3 automated workflows)
48
127
```
49
128
 
50
129
---
-100
+74
52
131
## Project Structure
53
132
 
54
133
```
55
ai-code-reviewer/
134
PRoctor/
135
│
56
136
├── app/
57
│   ├── config.py           # Environment config & AI prompt
58
│   ├── github_client.py    # GitHub REST API wrapper + signature verification
59
│   ├── ai_reviewer.py      # OpenAI review engine + Markdown formatter
60
│   └── webhook_handler.py  # Flask server (webhook + dashboard API)
61
├── dashboard/
62
│   └── index.html          # Live review dashboard (Chart.js)
137
│   ├── webhook_handler.py   ← Flask server, webhook endpoint
138
│   ├── ai_reviewer.py       ← Prompt engineering + response parser
139
│   ├── github_client.py     ← GitHub API wrapper + HMAC verification
140
│   ├── config.py            ← Environment config + system prompt
141
│   ├── data_collector.py    ← Collects PR history for fine-tuning
142
│   ├── fine_tuner.py        ← Fine-tuning pipeline manager
143
│   └── model_registry.py   ← Auto-selects fine-tuned model if available
144
│
63
145
├── notebooks/
64
│   ├── 01_setup_and_exploration.ipynb   # Setup, fetch a real PR
65
│   ├── 02_github_webhook_handler.ipynb  # Webhooks, signatures, ngrok
66
│   ├── 03_ai_review_engine.ipynb        # Prompt engineering, OpenAI calls
67
│   └── 04_dashboard.ipynb               # Plotly charts, end-to-end demo
68
├── tests/
69
│   └── test_ai_reviewer.py  # pytest unit tests
146
│   ├── 01_setup_and_exploration.ipynb
147
│   ├── 02_github_webhook_handler.ipynb
148
│   ├── 03_ai_review_engine.ipynb
149
│   ├── 04_dashboard.ipynb
150
│   └── 05_fine_tuning_pipeline.ipynb
151
│
152
├── scripts/
153
│   ├── retrain.py           ← Weekly fine-tuning runner (GitHub Actions)
154
│   └── review_pr.py         ← PR review runner (GitHub Actions)
155
│
156
├── .github/
157
│   └── workflows/
158
│       ├── tests.yml          ← Run pytest on every push
159
│       ├── pr_review_bot.yml  ← Auto-review every PR
160
│       └── weekly_retrain.yml ← Retrain model every Sunday
161
│
162
├── dashboard/index.html     ← Live review dashboard (Chart.js)
163
├── tests/                   ← 22 pytest unit tests
164
├── requirements.txt
70
165
├── .env.example
71
├── requirements.txt
72
166
└── README.md
73
167
```
74
168
 
75
169
---
76
170
 
77
## Quick Start
78
 
79
### 1. Clone and install
80
 
81
```bash
82
git clone https://github.com/<your-username>/ai-code-reviewer.git
83
cd ai-code-reviewer
171
## Installation
172
 
173
### Prerequisites
174
 
175
- Python 3.11+
176
- [Ollama](https://ollama.com/download) installed
177
- A GitHub account + personal access token (`repo` scope)
178
- [ngrok](https://ngrok.com/download) (free account)
179
 
180
---
181
 
182
### 1 — Clone the repo
183
 
184
```bash
185
git clone https://github.com/YOUR-USERNAME/PRoctor.git
186
cd PRoctor
187
```
188
 
189
### 2 — Install dependencies
190
 
191
```bash
84
192
pip install -r requirements.txt
85
193
```
86
194
 
87
### 2. Set up environment variables
195
### 3 — Download the AI model
196
 
197
```bash
198
ollama pull llama3
199
```
200
 
201
### 4 — Set up environment variables
88
202
 
89
203
```bash
90
204
cp .env.example .env
91
205
```
92
206
 
93
Edit `.env`:
94
 
95
| Variable | Where to get it |
96
|---|---|
97
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
98
| `GITHUB_TOKEN` | https://github.com/settings/tokens — needs `repo` scope |
99
| `GITHUB_WEBHOOK_SECRET` | You choose this — set the same value in GitHub webhook settings |
100
 
101
### 3. Run the server
207
Open `.env` and fill in:
208
 
209
```env
210
GITHUB_TOKEN=ghp_your_token_here
211
GITHUB_WEBHOOK_SECRET=pick_any_password
212
FLASK_SECRET_KEY=another_random_string
213
PORT=5001
214
```
215
 
216
### 5 — Start the Flask server
102
217
 
103
218
```bash
104
219
python -m flask --app app.webhook_handler run --port 5001
105
220
```
106
221
 
107
### 4. Expose locally with ngrok
222
### 6 — Expose it with ngrok
108
223
 
109
224
```bash
110
225
ngrok http 5001
111
226
# Copy the https://xxxxx.ngrok-free.app URL
112
227
```
113
228
 
114
### 5. Set up the GitHub webhook
115
 
116
1. Go to `https://github.com/<org>/<repo>/settings/hooks`
117
2. Click **Add webhook**
118
3. Payload URL: `https://<ngrok-url>/webhook`
119
4. Content type: `application/json`
120
5. Secret: the value you set in `GITHUB_WEBHOOK_SECRET`
121
6. Events: select **Pull requests** only
122
7. Click **Add webhook**
123
 
124
### 6. Open a pull request
125
 
126
The bot will automatically post a review comment!
127
 
128
---
129
 
130
## Dashboard
131
 
132
Open `dashboard/index.html` in your browser while the server is running to see:
133
- Score trends across all reviewed PRs
134
- Issues by severity (critical / high / medium / low)
135
- A searchable list of recent reviews
136
 
137
---
138
 
139
## Fine-Tuning Pipeline
140
 
141
Train a custom model on your own team's PR history so reviews match your codebase's specific patterns, terminology, and standards.
142
 
143
```bash
144
# Open the fine-tuning notebook
145
cd notebooks && jupyter notebook 05_fine_tuning_pipeline.ipynb
146
```
147
 
148
The pipeline:
149
1. **Collect** — fetches closed PRs and extracts human reviewer comments as training labels
150
2. **Filter** — removes bot-authored, generic ("LGTM"), and trivially short examples
151
3. **Format** — converts to OpenAI JSONL fine-tuning format (system / user / assistant)
152
4. **Estimate** — calculates token count and cost before any charges
153
5. **Train** — uploads data and starts a supervised fine-tuning job on `gpt-4o-mini`
154
6. **Activate** — saves the model ID; `AIReviewer` auto-detects and uses it immediately
155
7. **Compare** — side-by-side output comparison: base model vs fine-tuned model
156
 
157
New files added for this pipeline:
158
 
159
| File | Purpose |
229
### 7 — Add the GitHub webhook
230
 
231
Go to your repo → **Settings → Webhooks → Add webhook**
232
 
233
| Field | Value |
160
234
|---|---|
161
| `app/data_collector.py` | GitHub PR history collector + quality filtering |
162
| `app/fine_tuner.py` | OpenAI fine-tuning job manager |
163
| `app/model_registry.py` | Auto-selects fine-tuned model when available |
164
| `notebooks/05_fine_tuning_pipeline.ipynb` | Full walkthrough with cost estimation |
165
| `tests/test_fine_tuner.py` | Unit tests for all new components |
166
 
167
---
168
 
169
## Jupyter Notebooks
170
 
171
Five step-by-step notebooks walk through every component:
172
 
173
```bash
174
cd notebooks
175
jupyter notebook
176
```
177
 
178
| Notebook | What you learn |
179
|---|---|
180
| `01_setup_and_exploration` | Fetch a real GitHub PR, explore the diff structure |
181
| `02_github_webhook_handler` | Webhooks, HMAC verification, n...
182
[truncated]
235
[truncated]
183
236
[truncated]
