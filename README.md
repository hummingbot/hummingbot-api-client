# hummingbot-client

An async Python client for the Hummingbot API with modular router support.

## Installation

```bash
# Using uv
uv venv && source .venv/bin/activate
uv pip install aiohttp

# Or install the package
pip install .
```

## Usage

```python
import asyncio
from hummingbot_client import HummingbotClient

async def main():
    client = HummingbotClient(
        base_url="http://localhost:8080",
        username="admin",
        password="admin"
    )
    
    await client.init()
    
    # Access different API routers
    account_state = await client.accounts.get_state()
    candles = await client.markets.get_candles("BTC-USDT", interval="1h", limit=10)
    
    await client.close()

# Or use as context manager
async def example():
    async with HummingbotClient(base_url="http://localhost:8080") as client:
        markets = await client.markets.list_markets()
        print(markets)

asyncio.run(main())
```

## Building

```bash
uv pip install build
python -m build
```