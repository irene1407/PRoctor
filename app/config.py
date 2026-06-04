import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret")
    PORT = int(os.getenv("PORT", 5001))

    AI_MODEL = "gpt-4o-mini"
    MAX_DIFF_LINES = 500
    REVIEW_TEMPERATURE = 0.3

    REVIEW_SYSTEM_PROMPT = """You are a senior software engineer conducting a pull request code review.
Your job is to give clear, actionable, specific feedback — NOT generic advice.

Focus on:
- Bugs, logic errors, and edge cases
- Security vulnerabilities (SQL injection, XSS, hardcoded secrets, etc.)
- Performance issues (N+1 queries, unnecessary loops, large allocations)
- Maintainability (overly complex logic, missing error handling)
- Naming and readability issues that reduce clarity

Rules:
- Be direct and specific. Reference exact lines/variables when possible.
- Skip praise unless genuinely warranted.
- If the code is fine, say so briefly.
- Output ONLY a JSON object — no markdown fences, no preamble.

Output format:
{
  "summary": "One paragraph overall assessment.",
  "issues": [
    {
      "severity": "critical|high|medium|low",
      "file": "filename.py",
      "line_hint": "~42 or 'multiple'",
      "issue": "Concise title of the problem.",
      "explanation": "Why this is a problem.",
      "suggestion": "Exactly what to change."
    }
  ],
  "score": 1-10
}"""
