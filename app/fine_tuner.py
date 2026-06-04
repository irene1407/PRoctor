"""
OpenAI fine-tuning pipeline.

Steps:
    1. Format ReviewExample list → JSONL training file
    2. Upload the file to OpenAI
    3. Create a fine-tuning job
    4. Poll until complete
    5. Save the resulting model ID

Usage:
    from app.fine_tuner import FineTuner
    from app.data_collector import PRDataCollector

    examples = PRDataCollector().collect('my-org', 'my-repo', max_prs=50)
    ft = FineTuner()
    result = ft.run_pipeline(examples)
    print(result['fine_tuned_model'])
"""

import json
import time
import logging
import pathlib
from app.data_collector import ReviewExample
from app.config import Config

logger = logging.getLogger(__name__)

# Where fine-tuning artefacts are saved
FINETUNE_DIR = pathlib.Path("finetune_data")
TRAINING_FILE = FINETUNE_DIR / "training.jsonl"
VALIDATION_FILE = FINETUNE_DIR / "validation.jsonl"
MODEL_ID_FILE = FINETUNE_DIR / "model_id.txt"


class FineTuner:
    """Manages the full OpenAI fine-tuning lifecycle."""

    BASE_MODEL = "gpt-4o-mini-2024-07-18"
    MIN_EXAMPLES = 10

    def __init__(self, api_key: str | None = None):
        import openai
        self.client = openai.OpenAI(api_key=api_key or Config.OPENAI_API_KEY)
        FINETUNE_DIR.mkdir(exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_pipeline(
        self,
        examples: list[ReviewExample],
        validation_split: float = 0.15,
        n_epochs: int = 3,
    ) -> dict:
        """
        Full pipeline: format → upload → fine-tune → save model ID.

        Returns dict with keys: file_id, job_id, fine_tuned_model, status
        """
        if len(examples) < self.MIN_EXAMPLES:
            raise ValueError(
                f"Need at least {self.MIN_EXAMPLES} examples, got {len(examples)}. "
                "Collect more PR data first."
            )

        # 1. Split
        split = max(1, int(len(examples) * validation_split))
        train, val = examples[split:], examples[:split]
        logger.info(f"Split: {len(train)} train / {len(val)} validation")

        # 2. Format
        self.write_jsonl(train, TRAINING_FILE)
        self.write_jsonl(val, VALIDATION_FILE)
        logger.info(f"JSONL files written to {FINETUNE_DIR}/")

        # 3. Upload
        train_file_id = self._upload_file(TRAINING_FILE)
        val_file_id   = self._upload_file(VALIDATION_FILE)
        logger.info(f"Uploaded — train: {train_file_id}, val: {val_file_id}")

        # 4. Fine-tune
        job_id = self._create_job(train_file_id, val_file_id, n_epochs)
        logger.info(f"Fine-tuning job started: {job_id}")

        # 5. Poll
        result = self._wait_for_job(job_id)
        model_id = result.fine_tuned_model

        if model_id:
            MODEL_ID_FILE.write_text(model_id)
            logger.info(f"Fine-tuned model saved: {model_id}")

        return {
            "train_file_id": train_file_id,
            "val_file_id": val_file_id,
            "job_id": job_id,
            "fine_tuned_model": model_id,
            "status": result.status,
        }

    def list_jobs(self) -> list[dict]:
        """Return recent fine-tuning jobs."""
        jobs = self.client.fine_tuning.jobs.list(limit=20)
        return [
            {
                "id": j.id,
                "status": j.status,
                "model": j.fine_tuned_model,
                "created_at": j.created_at,
                "trained_tokens": j.trained_tokens,
            }
            for j in jobs.data
        ]

    def get_job_events(self, job_id: str) -> list[dict]:
        """Return training log events for a job."""
        events = self.client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id, limit=50)
        return [{"message": e.message, "level": e.level, "created_at": e.created_at}
                for e in events.data]

    # ------------------------------------------------------------------
    # JSONL formatting
    # ------------------------------------------------------------------

    def write_jsonl(self, examples: list[ReviewExample], path: pathlib.Path) -> None:
        """Convert examples to OpenAI fine-tuning JSONL format."""
        with open(path, "w", encoding="utf-8") as f:
            for ex in examples:
                record = self._to_chat_record(ex)
                f.write(json.dumps(record) + "\n")

    @staticmethod
    def _to_chat_record(ex: ReviewExample) -> dict:
        """
        Format one example as a chat completion fine-tuning record.

        Structure:
          system  → The same system prompt as Config.REVIEW_SYSTEM_PROMPT
          user    → PR title + diff (what the model sees at inference time)
          assistant → The human reviewer's comment (what we want the model to learn)
        """
        score_hint = ""
        if ex.score is not None:
            score_hint = f"\n\n(Reviewer gave a score hint: {ex.score}/10)"

        return {
            "messages": [
                {
                    "role": "system",
                    "content": Config.REVIEW_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": (
                        f"PR Title: {ex.pr_title}\n\n"
                        f"Diff:\n{ex.diff}"
                    ),
                },
                {
                    "role": "assistant",
                    "content": ex.review_body + score_hint,
                },
            ]
        }

    # ------------------------------------------------------------------
    # OpenAI API wrappers
    # ------------------------------------------------------------------

    def _upload_file(self, path: pathlib.Path) -> str:
        with open(path, "rb") as f:
            response = self.client.files.create(file=f, purpose="fine-tune")
        return response.id

    def _create_job(
        self,
        training_file_id: str,
        validation_file_id: str,
        n_epochs: int,
    ) -> str:
        job = self.client.fine_tuning.jobs.create(
            training_file=training_file_id,
            validation_file=validation_file_id,
            model=self.BASE_MODEL,
            hyperparameters={"n_epochs": n_epochs},
        )
        return job.id

    def _wait_for_job(self, job_id: str, poll_interval: int = 60, timeout_minutes: int = 120):
        """Block until the job succeeds or fails."""
        deadline = time.time() + timeout_minutes * 60
        while time.time() < deadline:
            job = self.client.fine_tuning.jobs.retrieve(job_id)
            logger.info(f"Job {job_id} status: {job.status}")
            if job.status in ("succeeded", "failed", "cancelled"):
                return job
            time.sleep(poll_interval)
        raise TimeoutError(f"Fine-tuning job {job_id} did not complete within {timeout_minutes} minutes")
