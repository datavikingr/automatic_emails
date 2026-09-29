import argparse
from pathlib import Path
import sys
import logging
import jinja2

from .config import load_config, DEFAULT_RETRY_ATTEMPTS, DEFAULT_CHUNK_SIZE
from .parser import parse_file
from .template import render_copy
from .mailer import send_batch, Email
from .logger import get_logger

log = get_logger("main")

BASE_DIR = Path(__file__).resolve().parent.parent
CLIENTS_DIR = BASE_DIR / "clients"

def list_clients():
    return [p.name for p in CLIENTS_DIR.iterdir() if p.is_dir()]

def run_client(client_name: str, template_name: str | None):
    client_dir = CLIENTS_DIR / client_name
    if not client_dir.exists():
        log.error(f"Client directory not found: {client_dir}")
        sys.exit(1)

    cfg = load_config(client_dir)
    data_file = next((p for p in client_dir.iterdir() if p.suffix.lower() in {".csv", ".xlsx"}), None)
    if not data_file:
        log.error("No CSV or XLSX file found in client directory.")
        sys.exit(1)

    rows = parse_file(data_file)
    copy_dir = client_dir / "copy"
    template_path = (copy_dir / f"{template_name}.txt") if template_name else (copy_dir / "default.txt")
    if not template_path.is_file():
        log.error(f"Template file missing: {template_path}")
        sys.exit(1)

    emails: list[Email] = []
    subject_template = cfg.get("subject_template", "")
    from_email = cfg.get("from_email") or cfg.get("mailjet_from_email")
    for row in rows:
        body = render_copy(template_path, row)
        # Render subject separately
        subj_env = {
            k: v for k, v in row.items()
        }
        try:
            subject = jinja2.Environment(autoescape=False).from_string(subject_template).render(**subj_env)
        except Exception as e:
            log.warning(f"Subject rendering failed for {row.get('email')}: {e}")
            subject = subject_template
        email_obj = Email(to=row["email"], subject=subject, body=body)
        if from_email:
            setattr(email_obj, "from_email", from_email)
        emails.append(email_obj)

    send_batch(
        emails,
        api_key=cfg.get("mailjet_api_key"),
        secret=cfg.get("mailjet_secret"),
        attempts=cfg.get("retry_attempts", DEFAULT_RETRY_ATTEMPTS),
        chunk_size=cfg.get("chunk_size", DEFAULT_CHUNK_SIZE),
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatic Email Sender")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    add_parser = subparsers.add_parser("add-client", help="Interactively add a new client.")
    run_parser = subparsers.add_parser("run", help="Run email campaign for a client.")
    run_parser.add_argument("--client", required=True, help="Client name (directory under clients/")
    run_parser.add_argument("--template", help="Copy file name without extension")

    args = parser.parse_args()

    if args.cmd == "add-client":
        # Interactive client creation – not yet implemented; placeholder
        print("Client addition workflow is a work in progress.")
    elif args.cmd == "run":
        run_client(args.client, args.template)
