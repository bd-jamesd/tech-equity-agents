import asyncio
from mcp import Client
from helpers import get_data

TOKEN = "YOUR_API_TOKEN"
MCP_URL = f"https://mcp.brightdata.com/mcp?token={TOKEN}"

async def main():
    async with Client(MCP_URL) as client:
        search_result = await client.call_tool(
            "search_engine",
            {"query": "best noise cancelling headphones 2026", "engine": "google"}
        )
        print("--- SEARCH RESULTS ---")
        print(get_data(search_result))

        scrape_result = await client.call_tool(
            "scrape_as_markdown",
            {"url": "https://en.wikipedia.org/wiki/Noise-cancelling_headphones"}
        )
        print("--- SCRAPED PAGE ---")
        content = get_data(scrape_result)
        print(content[:500] if isinstance(content, str) else content)

asyncio.run(main())