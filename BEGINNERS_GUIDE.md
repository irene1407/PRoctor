# How to Build This — Simple Guide

Read this top to bottom. Do each step before moving to the next one.
Every step tells you exactly what to type and what should happen.

---

## Before anything else — what IS this project?

Imagine you write some code and push it to GitHub.
Normally a human teammate reads it and says "hey, this part looks buggy."
This project does that automatically — a robot reads your code and leaves a comment on GitHub.

The robot is powered by ChatGPT (the same AI you chat with).

---

## STAGE 1 — Set up your computer (do this once ever)

### 1.1 — Install Python

Python is the language this project is written in.

1. Go to https://www.python.org/downloads/
2. Click the big yellow "Download Python 3.11" button
3. Run the installer
4. **IMPORTANT:** Tick the box that says "Add Python to PATH" before clicking install

Check it worked — open a terminal and type:
```
python --version
```
You should see something like `Python 3.11.4`. If you see an error, go back and reinstall.

**What is a terminal?**
- On Windows: press the Windows key, type `cmd`, press Enter
- On Mac: press Cmd + Space, type `terminal`, press Enter

---

### 1.2 — Install Git

Git is what saves your code history and lets you push to GitHub.

1. Go to https://git-scm.com/downloads
2. Download and install for your OS
3. Check it worked:
```
git --version
```
You should see something like `git version 2.43.0`

---

### 1.3 — Create a GitHub account (if you don't have one)

Go to https://github.com and sign up. Choose a professional username — this is what employers will see.

---

## STAGE 2 — Get the project onto your computer

### 2.1 — Create a folder for your projects

In your terminal, type these one at a time and press Enter after each:
```
mkdir projects
cd projects
```

You just created a folder called "projects" and moved into it.

---

### 2.2 — Copy the project files

The project files live on Replit. You need to get them onto your own computer.

**Option A — Download as a ZIP (easiest)**

1. In the Replit left sidebar, right-click the `ai-code-reviewer` folder
2. Click **Download**
3. A ZIP file saves to your Downloads folder
4. Right-click the ZIP → **Extract All** (Windows) or double-click (Mac)
5. Move the extracted folder wherever you like (Desktop, Documents, etc.)

**Option B — Push straight to GitHub (recommended)**

1. Click the **Git** icon in the Replit left sidebar
2. Connect your GitHub account and click **Create a GitHub repository**
3. Make it Public → click **Push**
4. Then on your own computer, open a terminal and type:

```
git clone https://github.com/YOUR-USERNAME/ai-code-reviewer.git
cd ai-code-reviewer
```

Either way you end up with the folder on your computer and a terminal open inside it.

---

### 2.3 — Install the project's tools

Think of this like installing apps your project needs to run.
In the terminal (inside the ai-code-reviewer folder):
```
pip install -r requirements.txt
```

This will take 1-2 minutes. You'll see a lot of text scrolling — that's normal.
When it stops and you see your cursor again, it's done.

---

## STAGE 3 — Get your two secret keys

The project needs two "passwords" to talk to GitHub and ChatGPT.
These are called API keys — think of them as VIP passes.

### 3.1 — Get your OpenAI key (to use ChatGPT)

1. Go to https://platform.openai.com/api-keys
2. Sign in (create an account if needed — you'll need to add $5 credit)
3. Click "Create new secret key"
4. Give it a name like "code-reviewer"
5. Copy the key — it starts with `sk-`
6. **Save it somewhere safe — you only see it once**

### 3.2 — Get your GitHub token (to read/write to GitHub)

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name like "code-reviewer"
4. Set expiration to 90 days
5. Tick the box next to "repo" (this gives it permission to access your repos)
6. Scroll down and click "Generate token"
7. Copy the token — it starts with `ghp_`
8. **Save it somewhere safe — you only see it once**

---

### 3.3 — Put your keys in the project

In the terminal, inside the ai-code-reviewer folder, type:
```
cp .env.example .env
```

This creates a file called `.env`. Open it with any text editor (Notepad on Windows, TextEdit on Mac).

Replace the placeholder text so it looks like this:
```
OPENAI_API_KEY=sk-your-actual-key-goes-here
GITHUB_TOKEN=ghp_your-actual-token-goes-here
GITHUB_WEBHOOK_SECRET=pick-any-password-you-want
FLASK_SECRET_KEY=another-random-string
PORT=5001
```

Save the file.

---

## STAGE 4 — Run the project for the first time

### 4.1 — Start the server

In the terminal:
```
python -m flask --app app.webhook_handler run --port 5001
```

You should see:
```
 * Running on http://127.0.0.1:5001
```

Leave this terminal open. The server only works while this is running.

---

### 4.2 — Test it's working

Open a **new** terminal window (keep the server one open) and type:
```
curl http://localhost:5001/health
```

You should see: `{"status": "ok"}`

If you see that — congratulations! The server is running.

---

### 4.3 — Test the AI reviewer

Still in the new terminal, type this (copy the whole thing):
```
curl -X POST http://localhost:5001/api/review \
  -H "Content-Type: application/json" \
  -d "{\"diff\": \"### File: login.py\\n+password = 'admin123'\\n+query = f\\\"SELECT * FROM users WHERE name='{username}'\\\"\", \"pr_title\": \"Add login\"}"
```

After 5-10 seconds you should see a JSON response with a code review.
The AI found the password and SQL injection — that's it working!

---

## STAGE 5 — Learn how each piece works (Jupyter notebooks)

Instead of guessing how things work, you can run the notebooks.
They're like interactive textbooks where you run code step by step.

### 5.1 — Start Jupyter

In a new terminal (inside the ai-code-reviewer folder):
```
cd notebooks
jupyter notebook
```

A browser window opens automatically. You'll see 5 notebooks listed.

### 5.2 — Work through the notebooks in order

Open **01_setup_and_exploration.ipynb** first.

Inside each notebook:
- Read the text explanation
- Click on a code cell (the grey boxes)
- Press **Shift + Enter** to run it
- Read the output
- Move to the next cell

Do not skip cells — each one builds on the previous.

**Order to follow:**
1. `01` — Fetches a real GitHub PR and shows you what the data looks like
2. `02` — Shows you how GitHub webhooks work (how GitHub calls your server)
3. `03` — Shows you the AI reviewing real vulnerable code live
4. `04` — Shows charts and runs an end-to-end test
5. `05` — The advanced fine-tuning notebook (do this last)

---

## STAGE 6 — Connect to a real GitHub pull request

This is where it gets real — your server will automatically review code.

### 6.1 — Install ngrok

ngrok creates a temporary public URL for your local server.
(Your server is on your laptop — ngrok makes GitHub able to reach it.)

1. Go to https://ngrok.com/download
2. Sign up for a free account
3. Download and install ngrok
4. Run:
```
ngrok http 5001
```

You'll see something like:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:5001
```

Copy that `https://abc123.ngrok-free.app` URL.

---

### 6.2 — Tell GitHub where to send events

1. Go to any GitHub repo you own
2. Click Settings → Webhooks → Add webhook
3. Fill in:
   - **Payload URL:** `https://abc123.ngrok-free.app/webhook`
   - **Content type:** `application/json`
   - **Secret:** the same value as `GITHUB_WEBHOOK_SECRET` in your `.env`
4. Under "Which events" — select "Let me select individual events"
5. Untick everything, then tick only **Pull requests**
6. Click "Add webhook"

### 6.3 — Open a test pull request

In that same GitHub repo, make any small change to any file and open a pull request.
Within 10-30 seconds, the bot will post a review comment automatically.

---

## STAGE 7 — Put it on GitHub (so employers can see it)

### 7.1 — Create a new GitHub repo

1. Go to https://github.com/new
2. Name it `ai-code-reviewer`
3. Make it **Public** (so employers can see it)
4. Do NOT tick "Add README" — you already have one
5. Click "Create repository"

### 7.2 — Push your code

In the terminal inside your project folder:
```
git init
git add .
git commit -m "Initial commit: AI Code Review Assistant"
git remote add origin https://github.com/YOUR-USERNAME/ai-code-reviewer.git
git push -u origin main
```

Your project is now live on GitHub!

---

## STAGE 8 — Set up GitHub Actions (fully automated)

This makes everything run without you doing anything.

### 8.1 — Add your secrets to GitHub

1. Go to your repo on GitHub
2. Click Settings → Secrets and variables → Actions
3. Click "New repository secret" and add:
   - Name: `OPENAI_API_KEY` → Value: your OpenAI key
   - Name: `GH_TOKEN` → Value: your GitHub token

### 8.2 — Watch it work

Open a pull request on your repo. GitHub Actions will:
1. Run your tests automatically
2. Post an AI code review comment

Every Sunday, it will also automatically collect new data and retrain the AI.

---

## STAGE 9 — Fine-tuning (most advanced part)

This teaches the AI to give reviews that match YOUR coding style specifically.

Open notebook `05_fine_tuning_pipeline.ipynb` in Jupyter.

Read through the whole thing first, then:
1. Run cells 1-4 to collect data and estimate cost
2. Check the cost estimate (usually under $1 for a small repo)
3. Uncomment Step 5 and run it to start training
4. Training takes 15-60 minutes — you can close Jupyter and come back
5. Once done, the model automatically upgrades — no other changes needed

---

## If something goes wrong

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| `Connection refused` on port 5001 | Your Flask server stopped — restart it |
| GitHub webhook shows red X | Check your ngrok URL is still active (it expires) |
| OpenAI error | Check your `.env` file has the correct key |
| `git push` asks for password | Use your GitHub token as the password |

---

## Congratulations — you built a real AI tool!

To summarise what you made:
- A Python server that listens for GitHub events
- An AI that reads code and finds real bugs
- A dashboard to visualise results
- An automated pipeline that trains a custom AI on your own code
- A fully automated CI/CD system on GitHub

This is production-grade software. Put it on your resume.
