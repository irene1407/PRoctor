"""
Unit tests for AIReviewer — run with:  pytest tests/
"""
import json
import pytest
from unittest.mock import MagicMock, patch
from app.ai_reviewer import AIReviewer


MOCK_REVIEW = {
    "summary": "This PR introduces a SQL injection vulnerability and lacks error handling.",
    "issues": [
        {
            "severity": "critical",
            "file": "db.py",
            "line_hint": "~12",
            "issue": "SQL Injection via f-string",
            "explanation": "User input is directly interpolated into the SQL query.",
            "suggestion": "Use parameterised queries: cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))",
        },
        {
            "severity": "medium",
            "file": "api.py",
            "line_hint": "~34",
            "issue": "Missing error handling on network call",
            "explanation": "requests.get() can raise ConnectionError or Timeout.",
            "suggestion": "Wrap in try/except requests.RequestException.",
        },
    ],
    "score": 4,
}


@pytest.fixture
def reviewer():
    return AIReviewer(api_key="test-key")


def test_parse_valid_json(reviewer):
    raw = json.dumps(MOCK_REVIEW)
    result = reviewer._parse_response(raw)
    assert result["score"] == 4
    assert len(result["issues"]) == 2


def test_parse_json_embedded_in_text(reviewer):
    raw = f"Here is the review:\n{json.dumps(MOCK_REVIEW)}\nEnd of review."
    result = reviewer._parse_response(raw)
    assert result["score"] == 4


def test_parse_invalid_returns_fallback(reviewer):
    result = reviewer._parse_response("not json at all")
    assert "_parse_error" in result
    assert result["issues"] == []


def test_format_as_markdown_contains_score():
    md = AIReviewer.format_as_markdown(MOCK_REVIEW)
    assert "Score: 4/10" in md
    assert "SQL Injection" in md
    assert "CRITICAL" in md


def test_format_as_markdown_no_issues():
    review = {"summary": "Looks good.", "issues": [], "score": 9}
    md = AIReviewer.format_as_markdown(review)
    assert "No issues found" in md


@patch("app.ai_reviewer.openai.OpenAI")
def test_review_diff_calls_openai(mock_openai_cls, reviewer):
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client
    reviewer.client = mock_client

    choice = MagicMock()
    choice.message.content = json.dumps(MOCK_REVIEW)
    mock_client.chat.completions.create.return_value = MagicMock(choices=[choice])

    result = reviewer.review_diff("diff --git a/db.py ...", pr_title="Fix login")
    assert result["score"] == 4
    mock_client.chat.completions.create.assert_called_once()
