import casbin
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

enforcer = casbin.Enforcer(
    str(BASE_DIR / "model.conf"),
    str(BASE_DIR / "policy.csv")
)


def check_permission(role: str, resource: str, action: str) -> bool:
    return enforcer.enforce(
        role,
        resource,
        action
    )