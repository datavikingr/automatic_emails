import logging
import logging.handlers
from pathlib import Path
import os

# Global log level can be overridden per-client in config.yaml
DEFAULT_LOG_LEVEL = logging.INFO


def get_logger(name: str, client_dir: Path | None = None) -> logging.Logger:
    """Return a logger that writes to a per‑client rotating file.
    If *client_dir* is None, logs are written to the root of the project.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured

    log_level_str = os.getenv("LOG_LEVEL", "INFO")
    try:
        log_level = getattr(logging, log_level_str.upper())
    except AttributeError:
        log_level = DEFAULT_LOG_LEVEL
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if client_dir:
        log_file = client_dir / "logs" / f"{client_dir.name}.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
    else:
        log_file = Path("automatic_emails.log")

    handler = logging.handlers.RotatingFileHandler(
        filename=str(log_file), maxBytes=10_000_000, backupCount=5, encoding="utf-8"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Also log to console at INFO level for debugging during cron runs
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger
