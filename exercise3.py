import asyncio
from mcp import Client
from helpers import get_data

TOKEN = "YOUR_API_TOKEN"
MCP_URL = f"https://mcp.brightdata.com/mcp?token={TOKEN}&pro=1"

WATCHLIST = [
    {"url": "https://www.amazon.com/dp/B0BDHWDR12", "target_price": 300},
    {"url": "https://www.amazon.com/dp/B09B8V1LZ3", "target_price": 40},
]

def unwrap_product(data):
    """web_data_amazon_product returns a JSON array with one product
    object inside, even for a single URL. Unwrap it to a plain dict."""
    if isinstance(data, list) and len(data) > 0:
        return data[0]
    if isinstance(data, dict):
        return data
    return None

async def check_product(client, url, target_price):
    try:
        result = await asyncio.wait_for(
            client.call_tool("web_data_amazon_product", {"url": url}),
            timeout=90,
        )
    except asyncio.TimeoutError:
        print(f"\n{'-'*60}\n{url}\n  TIMED OUT waiting for data — skipping.")
        return

    raw = get_data(result)
    product = unwrap_product(raw)

    if product is None:
        print(f"\n{'-'*60}\n{url}\n  Could not parse product data. Got: {raw!r:.200}")
        return

    title = product.get("title", "Unknown product")
    price = product.get("final_price") or product.get("price")
    rating = product.get("rating")
    reviews = product.get("reviews_count")
    availability = product.get("availability")

    print(f"\n{'-'*60}")
    print(f"{title[:80]}{'...' if len(title) > 80 else ''}")
    print(f"  Price:        ${price}" if price is not None else "  Price:        N/A")
    print(f"  Target:       ${target_price}")
    print(f"  Rating:       {rating} ({reviews:,} reviews)" if rating else "  Rating:       N/A")
    print(f"  Availability: {availability}")

    if price is not None and float(price) <= target_price:
        print(f"  🚨 ALERT: Price dropped below target! Buy now.")
    else:
        print(f"  No action — price still above target.")

async def main():
    async with Client(MCP_URL) as client:
        for item in WATCHLIST:
            await check_product(client, item["url"], item["target_price"])
        print(f"\n{'-'*60}")

asyncio.run(main())
