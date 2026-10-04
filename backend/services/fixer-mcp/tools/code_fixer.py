import re


def extract_code(text: str) -> str:

    text = text.strip()

    match = re.search(
        r"```(?:python)?\s*(.*?)```",
        text,
        re.DOTALL | re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    text = re.sub(
        r"^\*\*Fixed code:\*\*\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^`python\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"`$",
        "",
        text
    )

    return text.strip()


def prepare_fix(fix_response: str) -> dict:

    fixed_code = extract_code(fix_response)

    return {
        "fixed_code": fixed_code,
        "message": "Fixed code extracted successfully."
    }