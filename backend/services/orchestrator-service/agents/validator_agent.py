import sys
import asyncio
import json
from pathlib import Path

from langfuse import get_client

sys.path.append(
    str(Path(__file__).resolve().parents[2] / "llm-service")
)

from nvidia_client import generate_response
from state import DebugState
from mcp_client import validate_with_mcp


langfuse = get_client()


def validator_agent(state: DebugState):

    with langfuse.start_as_current_observation(
        as_type="agent",
        name="validator-agent",
        input={
            "code": state["code"],
            "error": state["error"],
            "fix_result": state["fix_result"]
        }
    ) as observation:

        validation_prompt = f"""
You are a code validation agent.

Original code:
{state["code"]}

Original error:
{state["error"]}

Scanner analysis:
{state["scan_result"]}

Proposed fix:
{state["fix_result"]}

Determine the corrected code from the proposed fix.

Return ONLY the corrected code.
Do not include markdown fences.
"""

        fixed_code = generate_response(validation_prompt)

        execution_result = asyncio.run(
            validate_with_mcp(fixed_code)
        )

        if execution_result.is_error:

            final_result = {
                "status": "FAIL",
                "message": "Validator MCP failed.",
                "execution": str(execution_result)
            }

            result = {
                "validation_result": str(execution_result),
                "final_result": final_result
            }

            observation.update(output=result)

            return result

        raw_text = execution_result.content[0].text

        try:
            execution_data = json.loads(raw_text)
        except json.JSONDecodeError:
            execution_data = {"raw": raw_text}

        if execution_data.get("passed"):

            final_result = {
                "status": "PASS",
                "message": "The proposed fix was executed successfully.",
                "execution": execution_data
            }

        else:

            final_result = {
                "status": "FAIL",
                "message": "The proposed fix failed during execution.",
                "execution": execution_data
            }

        result = {
            "validation_result": execution_data,
            "final_result": final_result
        }

        observation.update(
            output=result
        )

        return result