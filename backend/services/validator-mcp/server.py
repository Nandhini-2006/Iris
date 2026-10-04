from mcp.server.mcpserver import MCPServer

from tools.solution_verification import verify_python_solution

server = MCPServer(
    name="validator-mcp"
)

@server.tool()
def validate_solution(code: str) -> dict:
    """
    Execute the proposed Python fix in a sandbox
    and verify whether it runs successfully.
    """
    return verify_python_solution(code)


if __name__ == "__main__":
    server.run()