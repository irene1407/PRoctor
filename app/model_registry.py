"""
Select which model to use for reviews.

Priority order:
  1. Fine-tuned model saved in finetune_data/model_id.txt
  2. Config.AI_MODEL (gpt-4o-mini by default)

This lets the AIReviewer automatically upgrade to your fine-tuned model
once fine-tuning is complete, with zero code changes required.
"""

import pathlib
import logging

logger = logging.getLogger(__name__)

MODEL_ID_FILE = pathlib.Path("finetune_data/model_id.txt")


def get_active_model(default: str) -> str:
    """Return the fine-tuned model ID if one exists, else the default."""
    if MODEL_ID_FILE.exists():
        model_id = MODEL_ID_FILE.read_text().strip()
        if model_id:
            logger.info(f"Using fine-tuned model: {model_id}")
            return model_id
    return default


def set_active_model(model_id: str) -> None:
    """Manually override the active model."""
    MODEL_ID_FILE.parent.mkdir(exist_ok=True)
    MODEL_ID_FILE.write_text(model_id)
    logger.info(f"Active model set to: {model_id}")


def clear_fine_tuned_model() -> None:
    """Revert to the default model."""
    if MODEL_ID_FILE.exists():
        MODEL_ID_FILE.unlink()
        logger.info("Fine-tuned model cleared — using default.")
