import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Bash MCP")


@mcp.tool()
async def bash(command: str) -> dict:
    """Pass command to bash to execute in Terminal.

    Args:
        command: The command to execute

    Returns:
        The execution status, result, and error information of the command
    """
    result = subprocess.run(
        command,
        shell=True,  # 让命令行通过cmd执行
        capture_output=True,  # 捕获输出
        text=True,  # 输出解码为字符串
    )

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
