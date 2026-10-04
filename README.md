# Iris

A multi-agent code debugger. Submit code and an error; Iris finds what is wrong, proposes a fix, and checks the fix by actually running it.

Built on NVIDIA Nemotron 3.5 Lightning, LangGraph, MCP and FastAPI.

## How it works

```
User → FastAPI → Auth (JWT) → Authorization (Casbin) → PII redaction → Injection guard
     → LangGraph:  Scanner Agent → Fixer Agent → Validator Agent
                       │               │               │
                  Scanner MCP     Fixer MCP      Validator MCP
                (static analysis) (extract fix)  (sandboxed run)
     → Result
```

| Agent | Job | Output |
|---|---|---|
| Scanner | Finds what is wrong, using static-analysis evidence | Error list |
| Fixer | Writes a minimal correction | Proposed fix |
| Validator | Runs the fixed code and reports PASS or FAIL | Validator feedback |

The agents share one state (`code`, `error`, `scan_result`, `fix_result`, `validation_result`, `final_result`) and pass it to each other in order.

## Tech stack

| Area | Tool |
|---|---|
| LLM | NVIDIA NIM, `nvidia/nemotron-3.5-lightning-30b-a3b` |
| Orchestration | LangGraph |
| Tools | MCP (FastMCP) |
| API | FastAPI |
| Security | JWT, Casbin, PII redaction, prompt-injection guard |
| Observability | Langfuse, Prometheus, Grafana, Jaeger (OpenTelemetry) |

## Project structure

```
backend/
├── observation/      # metrics and tracing
├── security/         # authentication, authorization, PII redaction, injection guard
├── services/
│   ├── api-service/          # FastAPI gateway
│   ├── orchestrator-service/ # LangGraph workflow and agents
│   ├── scanner-mcp/          # bug detection
│   ├── fixer-mcp/            # fix extraction
│   └── validator-mcp/        # sandboxed execution
├── session/          # Redis session store
└── requirements.txt
```

## Setup

**Requirements:** Python 3.10+, an NVIDIA API key from [build.nvidia.com](https://build.nvidia.com).

```bash
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
NVIDIA_API_KEY=your-nvidia-api-key
JWT_SECRET_KEY=your-secret-key

# optional: Langfuse tracing
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

Never commit `.env`.

## Run

From the `backend` directory:

```bash
python -m uvicorn main:app --reload --app-dir services/api-service
```

- API docs: http://127.0.0.1:8000/docs
- Metrics: http://127.0.0.1:8000/metrics

## Usage

1. Open `/docs` and call `POST /auth/login` to get a token, then click **Authorize**.
2. Call `POST /debug`:

```json
{
  "code": "print(x)",
  "error": "NameError: name 'x' is not defined"
}
```

Example response:

```json
{
  "status": "success",
  "scan_result": "Undefined variable x",
  "fix_result": "x = 0\nprint(x)",
  "validation_result": { "passed": true, "exit_code": 0, "stdout": "0\n", "stderr": "" },
  "final_result": { "status": "PASS" }
}
```

## Limitations

- Validation checks that the fixed code runs, not that it is logically correct.
- The sandbox uses a temporary file and a subprocess timeout. It is not container-isolated.
- Scanner and validator currently support Python only.
- Development credentials are for local testing only. Change them before any deployment.

## License

Add a license before publishing.
