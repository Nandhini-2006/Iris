import re


def redact_pii(text: str) -> str:
    if not text:
        return text

    # Email addresses
    text = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        '[REDACTED_EMAIL]',
        text
    )

    # Phone numbers
    text = re.sub(
        r'(?<!\d)(?:\+91[-\s]?)?[6-9]\d{9}(?!\d)',
        '[REDACTED_PHONE]',
        text
    )

    # Credit card numbers
    text = re.sub(
        r'\b(?:\d[ -]*?){13,19}\b',
        '[REDACTED_CARD]',
        text
    )

    return text