import json
import requests
from app.config import Config
from app.model_registry import get_active_model


class AIReviewer:
    """Uses Ollama to analyse a PR diff and return structured feedback."""

    def __init__(self, api_key: str | None = None):
        pass

    # ------------------------------------------------------------------
    # Core review
    # ------------------------------------------------------------------

    def review_diff(
        self,
        diff: str,
        pr_title: str = "",
        pr_description: str = "",
    ) -> dict:
        """
        Send the diff to Ollama and return a parsed review dict.
        """

        user_content = self._build_user_message(
            diff,
            pr_title,
            pr_description,
        )

        prompt = f"""
You are a code review AI.

IMPORTANT RULES:
- Return ONLY valid JSON.
- Do NOT explain anything.
- Do NOT add markdown.
- Do NOT add text before or after the JSON.
- Output must start with {{
- Output must end with }}

Analyze the code diff and find:
1. Security issues
2. Bugs
3. Bad practices
4. Performance problems

Return exactly this structure:

{{
  "summary": "short summary",
  "issues": [
    {{
      "severity": "high",
      "file": "unknown",
      "line_hint": 1,
      "issue": "issue name",
      "explanation": "why it is a problem",
      "suggestion": "how to fix it"
    }}
  ],
  "score": 7
}}

Code Diff:

{user_content}
"""

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "system": """
You are a code review AI.

Return ONLY valid JSON.

Never explain.
Never chat.
Never add markdown.
Never add text before JSON.
Never add text after JSON.
""",
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=300,
            )

            response.raise_for_status()

            raw = response.json()["response"].strip()

            print("\n===== OLLAMA RESPONSE =====")
            print(raw)
            print("===========================\n")

            return self._parse_response(raw)

        except Exception as e:
            print(f"\nOLLAMA ERROR: {e}\n")

            return {
                "summary": f"Ollama error: {str(e)}",
                "issues": [],
                "score": 0,
            }

    # ------------------------------------------------------------------
    # Follow-up explanation
    # ------------------------------------------------------------------

    def explain_issue(
        self,
        issue: dict,
        code_snippet: str = "",
    ) -> str:
        return "Issue explanation handled by Ollama."

    # ------------------------------------------------------------------
    # Markdown formatter
    # ------------------------------------------------------------------

    @staticmethod
    def format_as_markdown(review: dict) -> str:
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🔵",
        }

        score = review.get("score", "N/A")

        lines = [
            f"## 🤖 AI Code Review — Score: {score}/10",
            "",
            f"**Summary:** {review.get('summary', 'No summary')}",
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

                lines.extend([
                    f"### {emoji} [{sev.upper()}] {issue.get('issue', '')}",
                    f"- **File:** {issue.get('file', 'unknown')}",
                    f"- **Line:** {issue.get('line_hint', '?')}",
                    f"- **Why:** {issue.get('explanation', '')}",
                    f"- **Fix:** {issue.get('suggestion', '')}",
                    "",
                ])

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_user_message(
        diff: str,
        pr_title: str,
        pr_description: str,
    ) -> str:
        parts = []

        if pr_title:
            parts.append(f"PR Title: {pr_title}")

        if pr_description:
            parts.append(
                f"PR Description: {pr_description[:500]}"
            )

        parts.append(f"\nDiff:\n{diff}")

        return "\n".join(parts)

    @staticmethod
    def _parse_response(raw: str) -> dict:
        try:
            return json.loads(raw)

        except json.JSONDecodeError:
            start = raw.find("{")
            end = raw.rfind("}") + 1

            if start != -1 and end > start:
                try:
                    return json.loads(raw[start:end])
                except json.JSONDecodeError:
                    pass

            return {
                "summary": raw,
                "issues": [],
                "score": 0,
                "_parse_error": True,
            }