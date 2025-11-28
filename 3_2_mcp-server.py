import json

from mcp.server.fastmcp import FastMCP

mcp = FastMCP()


@mcp.tool()
async def calculator(expression: str) -> str:
    """A calculator for evaluating the provided Python mathematical expression

    Args:
        expression: A mathematical expression compatible with Python's eval() function
    Returns:
        The result of evaluating the expression
    """
    try:
        result = eval(expression)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps(
            {"result": f"Error in evaluating mathematical expression: {str(e)}"}
        )


def main():
    # Initialize and run the server
    mcp.run(transport="stdio")
    # mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
