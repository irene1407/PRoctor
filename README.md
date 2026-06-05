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
1
# 🤖 PRoctor
12
2
 
13
3
### Your AI code reviewer that never sleeps, never misses a bug, and costs $0 to run.
14
4
 
15
5
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
16
6
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
17
7
[![Ollama](https://img.shields.io/badge/Ollama-Llama_3-FF6C37?style=for-the-badge)](https://ollama.com)
18
[![GitHub](https://img.shields.io/badge/GitHub-Webhook-181717?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/en/webhooks)
8
[![GitHub Webhooks](https://img.shields.io/badge/GitHub-Webhook-181717?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/en/webhooks)
19
9
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
20
10
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)
21
11
 
22
</div>
23
 
24
12
---
25
13
 
26
14
## What is PRoctor?
27
15
 
28
**PRoctor** is a fully automated code review bot. The moment a developer opens a pull request on GitHub, PRoctor wakes up, reads every line of changed code, and posts a structured review comment — flagging security vulnerabilities, bugs, and performance issues — all powered by a locally-running Llama 3 model.
16
PRoctor is a fully automated code review bot. The moment a developer opens a pull request on GitHub, PRoctor wakes up, reads every line of changed code, and posts a structured review comment — flagging security vulnerabilities, bugs, and performance issues — all powered by a **locally-running Llama 3 model**.
29
17
 
30
18
**No cloud API. No monthly bill. No data leaving your machine.**
31
19
 
32
20
---
33
21
 
34
## See it in action
22
## How it works
35
23
 
36
24
```
37
25
Developer opens a PR
38
26
         │
39
27
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
28
  GitHub Webhook  ──────  fires instantly on PR open / update
29
         │
30
         ▼
31
  Flask Server  ──────────  verifies HMAC-SHA256 signature
32
         │
33
         ▼
34
  GitHub API  ────────────  fetches the full diff across all changed files
35
         │
36
         ▼
37
  AI Reviewer  ───────────  builds structured prompt, sends to Ollama
38
         │
39
         ▼
40
  Ollama (Llama 3)  ──────  100% local — zero cost, zero data leakage
41
         │
42
         ▼  structured JSON
43
  GitHub PR Comment  ──────  formatted Markdown posted back to the PR
68
44
```
69
45
 
70
46
---
71
47
 
72
48
## Demo
73
49
 
74
> PRoctor reviewing a PR that contains a SQL injection vulnerability:
50
PRoctor reviewing a PR that contains a SQL injection vulnerability:
75
51
 
76
52
```
77
53
## 🤖 PRoctor Review — Score: 4/10
-3
+3
82
58
### 🔴 [CRITICAL] SQL Injection via f-string interpolation
83
59
- **File:** `login.py` — line ~10
84
60
- **Why:** User input is directly embedded in the SQL string.
85
          An attacker can input `' OR '1'='1` to bypass authentication.
61
           An attacker can input ' OR '1'='1 to bypass login entirely.
86
62
- **Fix:** cursor.execute('SELECT * FROM users WHERE name = %s', (username,))
87
63
 
88
64
### 🟠 [HIGH] Hardcoded password in source code
89
65
- **File:** `config.py` — line ~3
90
66
- **Why:** Credentials committed to git history are permanent,
91
          even after deletion.
67
           even after deletion.
92
68
- **Fix:** Use os.getenv('DB_PASSWORD') and add .env to .gitignore
93
69
 
94
70
---
95
*Posted by PRoctor — powered by Llama 3 (local)*
71
Posted by PRoctor — powered by Llama 3 (local)
96
72
```
97
73
 
98
74
---
-11
+23
105
81
| 🐛 **Bug detection** | Logic errors, missing error handling, null pointer risks |
106
82
| ⚡ **Performance flags** | N+1 queries, unnecessary loops, blocking I/O |
107
83
| 📊 **Severity scoring** | Every issue rated Critical / High / Medium / Low |
108
| 💯 **Quality score** | Each PR gets a 1–10 score posted on the comment |
84
| 💯 **Quality score** | Each PR gets a 1–10 score posted in the comment |
109
85
| 🏠 **100% local AI** | Runs on your machine via Ollama — no external API calls |
110
86
| 🔐 **Secure webhooks** | HMAC-SHA256 signature verification on every request |
111
| 📋 **Structured output** | Machine-parseable JSON → readable Markdown in one step |
87
| 📋 **Structured output** | Machine-parseable JSON converted to readable Markdown |
112
88
| 🔄 **Auto-triggered** | Fires on PR open, update, and reopen — zero manual steps |
113
89
| 🧪 **Fully tested** | 22 unit tests with pytest covering all core modules |
114
90
 
115
91
---
116
92
 
93
## Why this beats a linter
94
 
95
| Linter | PRoctor |
96
|---|---|
97
| Checks syntax and style rules | Understands the *meaning* of the code |
98
| Flags missing semicolons | Explains *why* a pattern is dangerous |
99
| Generic error codes | Specific, contextual fix suggestions |
100
| Can't detect logic bugs | Catches business logic errors |
101
| Rules written by humans | Reasoning generated by an LLM |
102
 
103
---
104
 
117
105
## Tech Stack
118
106
 
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
127
```
107
| Layer | Technology |
108
|---|---|
109
| Language | Python 3.11 |
110
| Web server | Flask 3.0 |
111
| AI engine | Ollama · Llama 3 (runs locally) |
112
| GitHub | REST API v3 + Webhooks |
113
| Tunnelling | ngrok (exposes local server for webhook) |
114
| Testing | pytest + unittest.mock |
115
| CI/CD | GitHub Actions (3 automated workflows) |
128
116
 
129
117
---
130
118
 
-1
+1
134
122
PRoctor/
135
123
│
136
124
├── app/
137
│   ├── webhook_handler.py   ← Flask server, webhook endpoint
125
│   ├── webhook_handler.py   ← Flask server + webhook endpoint
138
126
│   ├── ai_reviewer.py       ← Prompt engineering + response parser
139
127
│   ├── github_client.py     ← GitHub API wrapper + HMAC verification
140
128
│   ├── config.py            ← Environment config + system prompt
-8
+8
150
138
│   └── 05_fine_tuning_pipeline.ipynb
151
139
│
152
140
├── scripts/
153
│   ├── retrain.py           ← Weekly fine-tuning runner (GitHub Actions)
154
│   └── review_pr.py         ← PR review runner (GitHub Actions)
141
│   ├── retrain.py            ← Weekly fine-tuning runner (GitHub Actions)
142
│   └── review_pr.py          ← PR review runner (GitHub Actions)
155
143
│
156
144
├── .github/
157
145
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
146
│       ├── tests.yml           ← Run pytest on every push
147
│       ├── pr_review_bot.yml   ← Auto-review every PR
148
│       └── weekly_retrain.yml  ← Retrain model every Sunday
149
│
150
├── dashboard/index.html      ← Live review dashboard (Chart.js)
151
├── tests/                    ← 22 pytest unit tests
164
152
├── requirements.txt
165
153
├── .env.example
166
154
└── README.md
-10
+10
173
161
### Prerequisites
174
162
 
175
163
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
164
- [Ollama](https://ollama.com/download) installed and running
165
- A GitHub account + personal access token with `repo` scope
166
- [ngrok](https://ngrok.com/download) free account
167
 
168
---
169
 
170
### Step 1 — Clone the repo
183
171
 
184
172
```bash
185
173
git clone https://github.com/YOUR-USERNAME/PRoctor.git
186
174
cd PRoctor
187
175
```
188
176
 
189
### 2 — Install dependencies
177
### Step 2 — Install dependencies
190
178
 
191
179
```bash
192
180
pip install -r requirements.txt
193
181
```
194
182
 
195
### 3 — Download the AI model
183
### Step 3 — Download the AI model
196
184
 
197
185
```bash
198
186
ollama pull llama3
199
187
```
200
188
 
201
### 4 — Set up environment variables
189
### Step 4 — Set up environment variables
202
190
 
203
191
```bash
204
192
cp .env.example .env
-7
+8
206
194
 
207
195
Open `.env` and fill in:
208
196
 
209
```env
197
```
210
198
GITHUB_TOKEN=ghp_your_token_here
211
199
GITHUB_WEBHOOK_SECRET=pick_any_password
212
200
FLASK_SECRET_KEY=another_random_string
213
201
PORT=5001
214
202
```
215
203
 
216
### 5 — Start the Flask server
204
### Step 5 — Start the Flask server
217
205
 
218
206
```bash
219
207
python -m flask --app app.webhook_handler run --port 5001
220
208
```
221
209
 
222
### 6 — Expose it with ngrok
210
### Step 6 — Expose it with ngrok
223
211
 
224
212
```bash
225
213
ngrok http 5001
226
# Copy the https://xxxxx.ngrok-free.app URL
227
```
228
 
229
### 7 — Add the GitHub webhook
214
```
215
 
216
Copy the `https://xxxxx.ngrok-free.app` URL.
217
 
218
### Step 7 — Add the GitHub webhook
230
219
 
231
220
Go to your repo → **Settings → Webhooks → Add webhook**
232
221
 
-4
+4
234
223
|---|---|
235
224
| Payload URL | `https://xxxxx.ngrok-free.app/webhook` |
236
225
| Content type | `application/json` |
237
| Secret | same value as `GITHUB_WEBHOOK_SECRET` in `.env` |
226
| Secret | same value as `GITHUB_WEBHOOK_SECRET` in your `.env` |
238
227
| Events | Pull requests only |
239
228
 
240
### 8 — Open a pull request
241
 
242
PRoctor posts the review automatically. That's it.
229
### Step 8 — Open a pull request
230
 
231
PRoctor posts the review automatically.
243
232
 
244
233
---
245
234
 
-14
+9
248
237
```bash
249
238
curl -X POST http://localhost:5001/api/review \
250
239
  -H "Content-Type: application/json" \
251
  -d '{
252
    "diff": "### File: login.py\n+query = f\"SELECT * FROM users WHERE name='"'"'{username}'"'"'\"",
253
    "pr_title": "Add login endpoint"
254
  }'
255
```
256
 
257
---
258
 
259
## GitHub Actions (zero-touch automation)
260
 
261
Add two secrets to your repo (**Settings → Secrets → Actions**):
240
  -d '{"diff": "### File: login.py\n+query = f\"SELECT * FROM users WHERE name={username}\"", "pr_title": "Add login"}'
241
```
242
 
243
---
244
 
245
## GitHub Actions
246
 
247
Add this secret to your repo — **Settings → Secrets → Actions**:
262
248
 
263
249
| Secret | Value |
264
250
|---|---|
265
251
| `GH_TOKEN` | Your GitHub personal access token |
266
252
 
267
Then every push runs tests, every PR gets reviewed, and the model retrains every Sunday — automatically.
253
Every push runs tests, every PR gets reviewed, and the model retrains every Sunday — fully automated.
268
254
 
269
255
---
270
256
 
271
257
## Jupyter Notebooks
272
 
273
Step-by-step notebooks that explain every component:
274
258
 
275
259
```bash
276
260
cd notebooks && jupyter notebook
-5
+5
278
262
 
279
263
| # | Notebook | What it covers |
280
264
|---|---|---|
281
| 01 | Setup & Exploration | Fetch a real GitHub PR, explore the diff structure |
282
| 02 | Webhook Handler | HMAC signing, event parsing, ngrok setup |
283
| 03 | AI Review Engine | Prompt engineering, live analysis of vulnerable code |
284
| 04 | Dashboard | Plotly charts, end-to-end flow |
285
| 05 | Fine-Tuning | Train a custom model on your own PR history |
265
| 01 | Setup & Exploration | Fetch a real GitHub PR, explore the diff |
266
| 02 | Webhook Handler | HMAC signing, event parsing, ngrok |
267
| 03 | AI Review Engine | Prompt engineering, live code analysis |
268
| 04 | Dashboard | Plotly charts, end-to-end demo |
269
| 05 | Fine-Tuning | Train a custom model on your PR history |
286
270
 
287
271
---
288
272
 
-12
+0
291
275
```bash
292
276
pytest tests/ -v --cov=app --cov-report=term-missing
293
277
```
294
 
295
---
296
 
297
## Why This is Different from a Linter
298
 
299
| Linter | PRoctor |
300
|---|---|
301
| Checks syntax and style rules | Understands the *meaning* of the code |
302
| Flags missing semicolons | Explains *why* a pattern is dangerous |
303
| Generic error codes | Specific, contextual suggestions |
304
| Can't detect logic bugs | Catches business logic errors |
305
| Rules written by humans | Reasoning generated by an LLM |
306
278
 
307
279
---
308
280
 
-6
+0
326
298
## License
327
299
 
328
300
MIT — see [LICENSE](LICENSE)
329
 
330
---
331
 
332
<div align="center">
333
Built with Python, Flask, and Llama 3 &nbsp;|&nbsp; Runs 100% locally &nbsp;|&nbsp; Zero API cost
334
</div>
