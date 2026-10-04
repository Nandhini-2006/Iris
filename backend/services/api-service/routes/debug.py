import asyncio
import time
import sys
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from routes.auth import get_current_user
from security.authorization.authz import check_permission
from security.pii_redaction.redactor import redact_pii
from security.injection_guard.guard import check_injection

from observation.metrics import (
    DEBUG_REQUESTS,
    DEBUG_FAILURES,
    DEBUG_DURATION
)

sys.path.append(
    str(
        Path(__file__).resolve().parents[2]
        / "orchestrator-service"
    )
)

from graph import run_debug_graph


router = APIRouter()


class DebugRequest(BaseModel):
    code: str
    error: str


@router.post("/debug")
async def debug_write(
    request: DebugRequest,
    current_user=Depends(get_current_user)
):

    start_time = time.time()

    DEBUG_REQUESTS.inc()

    try:

        # Authorization
        allowed = check_permission(
            current_user["role"],
            "debug",
            "write"
        )

        if not allowed:
            DEBUG_FAILURES.inc()

            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        # PII Redaction
        redacted_code = redact_pii(
            request.code
        )

        redacted_error = redact_pii(
            request.error
        )

        # Prompt Injection Protection
        combined_input = (
            redacted_code +
            "\n" +
            redacted_error
        )

        if check_injection(combined_input):
            DEBUG_FAILURES.inc()

            raise HTTPException(
                status_code=400,
                detail="Potential prompt injection detected"
            )

        # LangGraph + Langfuse
        try:

            result = await asyncio.to_thread(
                run_debug_graph,
                redacted_code,
                redacted_error
            )

        except Exception as error:

            DEBUG_FAILURES.inc()

            raise HTTPException(
                status_code=500,
                detail=f"Debug pipeline failed: {str(error)}"
            )

        # Final response
        return {
            "status": "success",
            "user": current_user["username"],
            "role": current_user["role"],
            "scan_result": result.get("scan_result"),
            "fix_result": result.get("fix_result"),
            "validation_result": result.get(
                "validation_result"
            ),
            "final_result": result.get(
                "final_result"
            )
        }

    finally:

        DEBUG_DURATION.observe(
            time.time() - start_time
        )