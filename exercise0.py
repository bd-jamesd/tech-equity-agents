import asyncio
from mcp import Client
from helpers import get_data  # noqa: F401  (imported to confirm helpers.py loads cleanly)

TOKEN = "YOUR_API_TOKEN"
MCP_URL = f"https://mcp.brightdata.com/mcp?token={TOKEN}"

async def main():
    async with Client(MCP_URL) as client:
        result = await client.list_tools()
        print(f"Connected! {len(result.tools)} tools available:")
        for t in result.tools[:10]:
            print(f"  - {t.name}: {t.description[:70]}")

asyncio.run(main())