import re


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"disregard\s+(all\s+)?previous\s+instructions",
    r"forget\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"show\s+(your\s+)?system\s+prompt",
    r"print\s+(your\s+)?system\s+prompt",
    r"reveal\s+your\s+instructions",
    r"bypass\s+(security|authentication|authorization)",
    r"disable\s+(security|authentication|authorization)",
    r"execute\s+this\s+command",
]


def check_injection(text: str) -> bool:
    if not text:
        return False

    text_lower = text.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True

    return False