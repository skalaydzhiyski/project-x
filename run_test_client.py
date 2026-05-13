from fastmcp import Client, FastMCP
import asyncio

client = Client("http://187.124.112.103/mcp", verify=False)


async def main():
    async with client:
        # Basic server interaction
        await client.ping()

        # List available operations
        tools = await client.list_tools()
        print(tools)


if __name__ == "__main__":
    asyncio.run(main())
