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
from mcp_fixer_client import fix_with_mcp


langfuse = get_client()


def fixer_agent(state: DebugState):

    with langfuse.start_as_current_observation(
        as_type="agent",
        name="fixer-agent",
        input={
            "code": state["code"],
            "error": state["error"],
            "scan_result": state["scan_result"]
        }
    ) as observation:

        prompt = f"""
You are a code fixing agent.

Original code:
{state["code"]}

Original error:
{state["error"]}

Scanner analysis:
{state["scan_result"]}

Your task:
1. Determine the correct fix.
2. Modify only what is necessary.
3. Do not invent APIs.
4. Preserve existing functionality.
5. Return the complete corrected code.
6. Briefly explain the change.

Return the corrected code inside a Python code block.
"""

        llm_response = generate_response(prompt)

        execution_result = asyncio.run(
            fix_with_mcp(llm_response)
        )

        if execution_result.is_error:
            result = {
                "fix_result": "Fixer MCP failed."
            }

            observation.update(output=result)
            return result

        raw_text = execution_result.content[0].text

        try:
            fix_data = json.loads(raw_text)
        except json.JSONDecodeError:
            fix_data = {"raw": raw_text}

        result = {
            "fix_result": fix_data["fixed_code"]
        }

        observation.update(
            output=result
        )

        return result