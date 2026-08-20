import asyncio, re
from mcp import Client
from helpers import get_data

TOKEN = "YOUR_API_TOKEN"
MCP_URL = f"https://mcp.brightdata.com/mcp?token={TOKEN}"

async def main():
    async with Client(MCP_URL) as client:
        search_result = await client.call_tool(
            "search_engine",
            {"query": "electric vehicle battery recycling", "engine": "google"}
        )
        data = get_data(search_result)

        if not isinstance(data, dict):
            print("Unexpected response, got:", data)
            return

        urls = [item["link"] for item in data.get("organic", [])[:3]]
        print("Found URLs:", urls)

        keyword = "lithium"
        report = {}
        for url in urls:
            page = await client.call_tool("scrape_as_markdown", {"url": url})
            text = get_data(page)
            if not isinstance(text, str):
                text = ""
            count = len(re.findall(keyword, text, re.IGNORECASE))
            report[url] = count

        print("--- KEYWORD FREQUENCY REPORT ---")
        for url, count in report.items():
            print(f"{count:3d} mentions of '{keyword}' — {url}")

asyncio.run(main())
