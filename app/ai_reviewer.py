import json
import requests
from app.config import Config


class AIReviewer:
    """Uses Ollama to analyse PR diff and return structured JSON."""

    def __init__(self, api_key=None):
        pass

    # ----------------------------
    # Core review
    # ----------------------------
    def review_diff(self, diff: str, pr_title: str = "", pr_description: str = "") -> dict:

        user_content = self._build_user_message(diff, pr_title, pr_description)

        prompt = f"""
You are a code review AI.

Return ONLY valid JSON.

No explanation.
No markdown.
No extra text.

Return exactly:

{{
  "summary": "short summary",
  "issues": [
    {{
      "severity": "high",
      "file": "unknown",
      "line_hint": 1,
      "issue": "issue",
      "explanation": "why",
      "suggestion": "fix"
    }}
  ],
  "score": 7
}}

Code:
{user_content}
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )

        raw = response.json()["response"].strip()

        # Debug (optional)
        print("\n===== OLLAMA RESPONSE =====")
        print(raw)
        print("===========================\n")

        return self._parse_response(raw)

    # ----------------------------
    # Markdown ONLY for GitHub
    # ----------------------------
    @staticmethod
    def format_as_markdown(review: dict) -> str:
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🔵",
        }

        score = review.get("score", 0)

        lines = [
            f"## 🤖 AI Code Review — Score: {score}/10",
            "",
            f"**Summary:** {review.get('summary', '')}",
            "",
        ]

        issues = review.get("issues", [])

        if not issues:
            lines.append("✅ No issues found.")
        else:
            lines.append(f"**{len(issues)} issue(s) found:**")
            lines.append("")

            for issue in issues:
                sev = issue.get("severity", "low")
                emoji = severity_emoji.get(sev, "⚪")

                lines += [
                    f"### {emoji} [{sev.upper()}] {issue.get('issue','')}",
                    f"- File: {issue.get('file','unknown')}",
                    f"- Line: {issue.get('line_hint','?')}",
                    f"- Why: {issue.get('explanation','')}",
                    f"- Fix: {issue.get('suggestion','')}",
                    "",
                ]

        return "\n".join(lines)

    # ----------------------------
    # Helpers
    # ----------------------------
    @staticmethod
    def _build_user_message(diff, title, desc):
        parts = []
        if title:
            parts.append(f"Title: {title}")
        if desc:
            parts.append(f"Description: {desc[:300]}")
        parts.append(diff)
        return "\n".join(parts)

    @staticmethod
    def _parse_response(raw: str) -> dict:
        try:
            return json.loads(raw)
        except:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start != -1 and end != -1:
                try:
                    return json.loads(raw[start:end])
                except:
                    pass

        return {
            "summary": raw,
            "issues": [],
            "score": 0
        }