import jinja2
from pathlib import Path

def render_copy(template_path: Path, row: dict) -> str:
    """Render a plain‑text copy using Jinja2.
    Uses a sandboxed environment and disables autoescape.
    """
    if not template_path.is_file():
        raise FileNotFoundError(f"Template file missing: {template_path}")

    env = jinja2.Environment(
        loader=jinja2.BaseLoader(),
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=False,
    )
    template_source = template_path.read_text(encoding="utf-8")
    tmpl = env.from_string(template_source)
    return tmpl.render(**row)
