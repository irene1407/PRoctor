"""
Flask webhook server — receives GitHub PR events and triggers AI review.

Run locally:
    python -m flask --app app.webhook_handler run --port 5001

Expose with ngrok (for testing):
    ngrok http 5001
    # Then set your GitHub webhook URL to:  https://<ngrok-url>/webhook
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

# In-memory store for demo purposes (replace with a DB for production)
review_store: list[dict] = []


# ------------------------------------------------------------------
# Health check
# ------------------------------------------------------------------

@app.get("/health")
def health():
    return jsonify({"status": "ok"})


# ------------------------------------------------------------------
# Webhook endpoint
# ------------------------------------------------------------------

@app.post("/webhook")
def webhook():
    # 1. Verify GitHub signature
    sig = request.headers.get("X-Hub-Signature-256", "")
    if Config.GITHUB_WEBHOOK_SECRET:
        if not sig or not GitHubClient.verify_signature(request.data, sig, Config.GITHUB_WEBHOOK_SECRET):
            logger.warning("Invalid webhook signature")
            abort(403, "Invalid signature")

    event = request.headers.get("X-GitHub-Event", "")
    payload = request.get_json(force=True)

    # 2. Only process pull_request opened/synchronize events
    if event != "pull_request":
        return jsonify({"ignored": True, "event": event})

    action = payload.get("action", "")
    if action not in ("opened", "synchronize", "reopened"):
        return jsonify({"ignored": True, "action": action})

    pr = payload["pull_request"]
    repo = payload["repository"]
    owner = repo["owner"]["login"]
    repo_name = repo["name"]
    pr_number = pr["number"]
    head_sha = pr["head"]["sha"]

    logger.info(f"Reviewing PR #{pr_number} in {owner}/{repo_name}")

    try:
        files = github.get_pull_request_files(owner, repo_name, pr_number)
        diff = github.build_diff_context(files)

        review = reviewer.review_diff(
            diff=diff,
            pr_title=pr.get("title", ""),
            pr_description=pr.get("body", ""),
        )

        comment_body = AIReviewer.format_as_markdown(review)
        github.post_review(owner, repo_name, pr_number, comment_body)

        entry = {
            "repo": f"{owner}/{repo_name}",
            "pr_number": pr_number,
            "pr_title": pr.get("title", ""),
            "score": review.get("score", 0),
            "issue_count": len(review.get("issues", [])),
            "review": review,
        }
        review_store.append(entry)
        logger.info(f"Review posted for PR #{pr_number} — score {review.get('score')}/10")
        return jsonify({"ok": True, "score": review.get("score")})

    except Exception as exc:
        logger.error(f"Review failed: {exc}", exc_info=True)
        return jsonify({"error": str(exc)}), 500


# ------------------------------------------------------------------
# Dashboard API — consumed by the dashboard page
# ------------------------------------------------------------------

@app.get("/api/reviews")
def get_reviews():
    return jsonify(review_store)


@app.get("/api/stats")
def get_stats():
    if not review_store:
        return jsonify({"total": 0, "avg_score": 0, "total_issues": 0})
    scores = [r["score"] for r in review_store if r.get("score")]
    total_issues = sum(r["issue_count"] for r in review_store)
    return jsonify({
        "total": len(review_store),
        "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
        "total_issues": total_issues,
    })


# ------------------------------------------------------------------
# Manual review endpoint (for testing without a webhook)
# ------------------------------------------------------------------

@app.post("/api/review")
def manual_review():
    """
    POST /api/review
    Body: { "diff": "...", "pr_title": "...", "pr_description": "..." }
    Returns the structured review JSON.
    """
    body = request.get_json(force=True)
    diff = body.get("diff", "")
    if not diff:
        return jsonify({"error": "diff is required"}), 400

    review = reviewer.review_diff(
        diff=diff,
        pr_title=body.get("pr_title", ""),
        pr_description=body.get("pr_description", ""),
    )
    return jsonify({
        "review": review,
        "markdown": AIReviewer.format_as_markdown(review),
    })


if __name__ == "__main__":
    app.run(port=Config.PORT, debug=True)
