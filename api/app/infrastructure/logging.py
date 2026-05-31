"""Centralised logging setup.

Replace `print()` calls with `logger = get_logger(__name__)` then
`logger.info(...) / .warning(...) / .error(...)`.

Why a logger over print:
  - Severity filtering (CloudWatch can alarm on ERROR-level only)
  - Structured prefix (timestamp, module name, level)
  - Per-module log level overrides (e.g., quiet a noisy library)
  - Doesn't compete with FastAPI/uvicorn's own log streams

In ECS / Fargate, all stdout is captured by CloudWatch Logs anyway, so
output destination doesn't change — only the format and filterability.
"""

from __future__ import annotations

import logging
import os
import sys

_LOG_FORMAT = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def configure_root_logging() -> None:
    """Idempotent root-logger setup. Safe to call from main.py at start-up."""
    if logging.getLogger().handlers:
        return  # already configured (e.g., uvicorn started us)
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Module-scoped logger. Use `get_logger(__name__)` at the top of each file."""
    return logging.getLogger(name)
