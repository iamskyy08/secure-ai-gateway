import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger("secure_ai_gateway.audit")

def audit(event: str, subject: str, request_id: str, **metadata) -> None:
    # Never log prompts, completions, credentials, or raw tool arguments.
    logger.info(json.dumps({
        "event": event, "subject": subject, "request_id": request_id,
        "timestamp": datetime.now(timezone.utc).isoformat(), **metadata,
    }, separators=(",", ":")))
