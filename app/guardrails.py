from dataclasses import dataclass
import re

@dataclass
class GuardrailResult:
    allowed: bool
    text: str
    reason: str | None = None

# Demonstration patterns only. Use tested classifiers/DLP and domain policy in production.
_INPUT_DENY = [
    re.compile(r"(?i)ignore\s+(all\s+)?previous\s+instructions"),
    re.compile(r"(?i)reveal\s+(the\s+)?system\s+prompt"),
]
_OUTPUT_DENY = [
    re.compile(r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*[A-Za-z0-9_\-]{16,}"),
]

def check_input(text: str) -> GuardrailResult:
    if not text.strip():
        return GuardrailResult(False, text, "empty_input")
    if len(text) > 16000:
        return GuardrailResult(False, text, "input_too_long")
    if any(p.search(text) for p in _INPUT_DENY):
        return GuardrailResult(False, text, "prompt_injection_pattern")
    return GuardrailResult(True, text)

def check_output(text: str, max_chars: int) -> GuardrailResult:
    if len(text) > max_chars:
        return GuardrailResult(False, "", "output_too_long")
    if any(p.search(text) for p in _OUTPUT_DENY):
        return GuardrailResult(False, "", "sensitive_material_detected")
    return GuardrailResult(True, text)
