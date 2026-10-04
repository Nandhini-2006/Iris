from typing import TypedDict


class DebugState(TypedDict, total=False):
    code: str
    error: str

    scan_result: str
    fix_result: str
    validation_result: str

    final_result: str