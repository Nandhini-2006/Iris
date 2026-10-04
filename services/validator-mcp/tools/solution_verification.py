import subprocess
import tempfile
import os


def verify_python_solution(code: str) -> dict:

    temp_file = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as file:

            file.write(code)
            temp_file = file.name

        result = subprocess.run(
            ["python", temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "passed": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:

        return {
            "passed": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": "Execution timed out"
        }

    finally:

        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)