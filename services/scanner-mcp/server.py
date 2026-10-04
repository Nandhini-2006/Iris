from mcp.server.mcpserver import MCPServer

from tools.code_scanner import scan_python_code


server = MCPServer(
    name="scanner-mcp"
)


@server.tool()
def scan_code(code: str) -> dict:
    """
    Analyze Python code and detect syntax issues.
    """
    return scan_python_code(code)


if __name__ == "__main__":
    server.run()