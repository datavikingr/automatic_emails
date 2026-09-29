import time
from pathlib import Path
from typing import List, Dict
import logging

from mailjet_rest import Client as MailjetClient

from logger import get_logger

log = get_logger("mailer")

class Email:
    def __init__(self, to: str, subject: str, body: str):
        self.to = to
        self.subject = subject
        self.body = body


def _chunk(iterable: List[Email], size: int) -> List[List[Email]]:
    return [iterable[i:i+size] for i in range(0, len(iterable), size)]


def send_batch(emails: List[Email], api_key: str, secret: str,
                attempts: int = 10, chunk_size: int = 200) -> None:
    """Send emails via Mailjet.
    Retries on failure up to *attempts* with exponential back‑off.
    Logs each individual failure with stacktrace.
    """
    client = MailjetClient(auth=(api_key, secret))
    chunks = _chunk(emails, chunk_size)

    for idx, batch in enumerate(chunks, 1):
        payload = {
            'Messages': [
                {
                    'From': {'Email': email.from_email if hasattr(email, "from_email") else None},
                    'To': [{'Email': email.to}],
                    'Subject': email.subject,
                    'TextPart': email.body
                } for email in batch
            ]
        }
        # Remove None From addresses to avoid API errors
        payload['Messages'] = [msg for msg in payload['Messages'] if msg['From']['Email']]

        attempt = 0
        while attempt < attempts:
            try:
                response = client.send.create(data=payload)
                if response.status_code == 200 or response.status_code == 201:
                    log.info(f"Batch {idx}/{len(chunks)} sent successfully.")
                    break
                else:
                    raise Exception(f"Mailjet error: {response.status_code} - {response.json()}")
            except Exception as exc:
                attempt += 1
                log.error(
                    f"Error sending batch {idx}/{len(chunks)} (attempt {attempt}/{attempts}): {exc}",
                    exc_info=True,
                )
                if attempt < attempts:
                    time.sleep(2 ** attempt)  # exponential back‑off
        else:
            log.error(f"Batch {idx}/{len(chunks)} failed after {attempts} attempts.")
