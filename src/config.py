import os
from pathlib import Path
import yaml

DEFAULT_RETRY_ATTEMPTS = 10
DEFAULT_CHUNK_SIZE = 200

def _expand_env(value: str) -> str:
    """Replace ${VAR} with environment variable value."""
    if not isinstance(value, str):
        return value
    start = value.find("${")
    while start != -1:
        end = value.find("}", start)
        if end == -1:
            break
        var_name = value[start+2:end]
        env_val = os.getenv(var_name, "")
        value = value[:start] + env_val + value[end+1:]
        start = value.find("${", start + len(env_val))
    return value

def load_config(client_dir: Path) -> dict:
    cfg_path = client_dir / "config.yaml"
    if not cfg_path.is_file():
        raise FileNotFoundError(f"Config file missing: {cfg_path}")
    with open(cfg_path, "r", encoding="utf-8") as f:
        raw_cfg = yaml.safe_load(f) or {}
    # Expand env vars
    for k, v in list(raw_cfg.items()):
        if isinstance(v, str):
            raw_cfg[k] = _expand_env(v)
    # Apply defaults
    raw_cfg.setdefault("retry_attempts", DEFAULT_RETRY_ATTEMPTS)
    raw_cfg.setdefault("chunk_size", DEFAULT_CHUNK_SIZE)
    return raw_cfg
