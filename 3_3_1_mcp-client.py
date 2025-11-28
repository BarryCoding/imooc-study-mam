import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    # 1.初始化stdio的服务器连接参数
    server_params = StdioServerParameters(
        command="uv",
        args=[
            "--directory",
            "/Users/aiman/AI/Imooc_MCP_A2A/my-code/study-code",
            "run",
            "3_2_mcp-server.py",
        ],
        env=None,
    )

    # 2.创建标准输入输出客户端
    async with stdio_client(server_params) as transport:
        # 3.获取写入和写出流
        read_stream, write_stream = transport

        # 4.创建客户端会话上下文
        async with ClientSession(read_stream, write_stream) as session:
            # 5.初始化mcp服务器连接
            await session.initialize()

            # 6.获取工具列表信息
            list_tools_response = await session.list_tools()
            tools = list_tools_response.tools
            print("Available tools:", [tool.name for tool in tools])

            # 7.调用指定的工具
            call_tool_response = await session.call_tool(
                "calculator", {"expression": "564*34+12.4/455**2"}
            )
            print("Tool result:", call_tool_response)


if __name__ == "__main__":
    asyncio.run(main())
