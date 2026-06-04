"""
Flask webhook server — receives GitHub PR events and triggers AI review.
"""

import json
import logging
from flask import Flask, request, jsonify, abort

from app.config import Config
from app.github_client import GitHubClient
from app.ai_reviewer import AIReviewer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY

github = GitHubClient()
reviewer = AIReviewer()

# In-memory store (demo only)
review_store = []


# ----------------------------
# Health check
# ----------------------------
@app.get("/health")
def health():
    return jsonify({"status": "ok"})


# ----------------------------
# Webhook endpoint
# ----------------------------
@app.post("/webhook")
def webhook():
    event = request.headers.get("X-GitHub-Event", "")
    payload = request.get_json(force=True)

    if event != "pull_request":
        return jsonify({"ignored": True})

    action = payload.get("action", "")
    if action not in ("opened", "synchronize", "reopened"):
        return jsonify({"ignored": True})

    pr = payload["pull_request"]
    repo = payload["repository"]

    owner = repo["owner"]["login"]
    repo_name = repo["name"]
    pr_number = pr["number"]

    logger.info(f"Reviewing PR #{pr_number}")

    try:
        files = github.get_pull_request_files(owner, repo_name, pr_number)
        diff = github.build_diff_context(files)

        review = reviewer.review_diff(
            diff=diff,
            pr_title=pr.get("title", ""),
            pr_description=pr.get("body", ""),
        )

        # Markdown ONLY here
        comment_body = AIReviewer.format_as_markdown(review)
        github.post_review(owner, repo_name, pr_number, comment_body)

        review_store.append({
            "repo": f"{owner}/{repo_name}",
            "pr_number": pr_number,
            "review": review
        })

        return jsonify({"ok": True, "score": review.get("score", 0)})

    except Exception as e:
        logger.error(f"Webhook failed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# ----------------------------
# Manual test endpoint
# ----------------------------
@app.post("/api/review")
def manual_review():
    body = request.get_json(force=True)
    diff = body.get("diff", "")

    if not diff:
        return jsonify({"error": "diff required"}), 400

    review = reviewer.review_diff(
        diff=diff,
        pr_title=body.get("pr_title", ""),
        pr_description=body.get("pr_description", ""),
    )

    # 🔥 IMPORTANT: JSON ONLY (NO MARKDOWN HERE)
    return jsonify({
        "review": review
    })


# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run(port=Config.PORT, debug=True)