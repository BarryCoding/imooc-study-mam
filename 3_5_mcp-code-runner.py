import os
import subprocess
import uuid

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Code Runner MCP", port=9888)
BASE_DIR = "/Users/aiman/AI/Imooc_MCP_A2A/my-code/study-code"
UV_CMD = "uv"


@mcp.tool()
async def run_code(language: str, code: str, timeout: int = 10) -> str:
    """Run code in a subprocess with a timeout.

    Args:
        language: The language of the code to run. (python, javascript, etc.)
        code: The code to run.
        timeout: The timeout in seconds. (default: 10)

    Returns:
        The output of the code. (stdout and stderr)
    """

    # 1. check language
    language = (language or "").strip().lower()
    if language not in ["python", "javascript"]:
        return "Unsupported language. Only Python and JavaScript are supported."

    # 2. generate a temporary file
    suffix = "py" if language == "python" else "js"
    file_name = f"temp_{uuid.uuid4().hex}.{suffix}"
    tmp_path = os.path.join(BASE_DIR, file_name)

    # 3. create the base directory if it doesn't exist
    os.makedirs(BASE_DIR, exist_ok=True)

    try:
        # 4. write the code to the temporary file
        with open(tmp_path, "w", encoding="utf-8") as file:
            file.write(code)

        # 5. run the code with the appropriate command
        if language == "python":
            cmd = [UV_CMD, "--directory", BASE_DIR, "run", file_name]
        elif language == "javascript":
            cmd = ["bun", tmp_path]

        # 6. run the command with a subprocess
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=BASE_DIR,
        )

        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()

        if proc.returncode != 0:
            return f"Error running code: {stderr}"

        return stdout
    except subprocess.TimeoutExpired:
        return f"Timeout running code: {timeout} seconds"
    except FileNotFoundError as e:
        return f"File not found: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

    finally:
        # 7. remove the temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def main() -> None:
    """Main function to run the MCP server."""
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
