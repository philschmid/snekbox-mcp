import argparse
from fastmcp import FastMCP
from snekbox.snekio import FileAttachment

mcp = FastMCP(
    name="snekbox-mcp",
    instructions="This server provides a tool to execute Python code in a sandboxed environment.",
)

@mcp.tool
def execute(code: str) -> str:
    """
    Executes Python code in a sandboxed environment.
    """
    from snekbox.nsjail import NsJail
    nsjail = NsJail()
    files = [FileAttachment("main.py", code.encode("utf-8"))]
    result = nsjail.python3(
        ["main.py"],
        files=files,
    )
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description="Run Snekbox MCP Server.")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="streamable-http",
        help="Transport method to use (default: streamable-http)",
    )
    args = parser.parse_args()

    run_kwargs = {"transport": args.transport}

    if args.transport == "streamable-http":
        run_kwargs["host"] = "0.0.0.0"
        run_kwargs["port"] = 8000
        run_kwargs["path"] = "/mcp"

    mcp.run(**run_kwargs)


if __name__ == "__main__":
    main()
