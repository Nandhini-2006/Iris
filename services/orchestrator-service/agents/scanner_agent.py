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
from mcp_scanner_client import scan_with_mcp


langfuse = get_client()


def scanner_agent(state: DebugState):

    with langfuse.start_as_current_observation(
        as_type="agent",
        name="scanner-agent",
        input={
            "code": state["code"],
            "error": state["error"]
        }
    ) as observation:

        code = state["code"]
        error = state["error"]

        execution_result = asyncio.run(
            scan_with_mcp(code)
        )

        if execution_result.is_error:
            result = {
                "scan_result": "Scanner MCP failed."
            }

            observation.update(output=result)
            return result

        raw_text = execution_result.content[0].text

        try:
            scan_data = json.loads(raw_text)
        except json.JSONDecodeError:
            scan_data = {"raw": raw_text}

        analysis_prompt = f"""
You are a code debugging scanner agent.

Original code:
{code}

Reported error:
{error}

Static analysis result from Scanner MCP:
{json.dumps(scan_data, indent=2)}

Your task:

1. Determine whether a real bug exists.
2. Identify the problematic location.
3. Identify the root cause.
4. Use evidence from the code and Scanner MCP result.
5. Do not invent APIs, errors, or code behavior.
6. Do not assume an issue exists if there is insufficient evidence.

Return a concise technical analysis.
"""

        llm_analysis = generate_response(analysis_prompt)

        result = {
            "scan_result": llm_analysis
        }

        observation.update(
            output=result
        )

        return result