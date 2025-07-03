# hummingbot-api-client

An async Python client for the Hummingbot API with modular router support.

## Installation

```bash
# Using uv (recommended)
uv venv && source .venv/bin/activate
uv pip install aiohttp

# Or using pip
pip install aiohttp

# Install the package
pip install -e .
```

## Quick Start

```python
import asyncio
from hummingbot_api_client import HummingbotAPIClient


async def main():
  # Using context manager (recommended)
  async with HummingbotAPIClient("http://localhost:8000", "admin", "admin") as client:
    # Get portfolio state
    portfolio = await client.portfolio.get_state()
    print(f"Portfolio value: ${sum(b['value'] for a in portfolio.values() for c in a.values() for b in c):.2f}")

    # List available connectors
    connectors = await client.connectors.list_connectors()
    print(f"Available connectors: {len(connectors)}")

    # Check Docker status
    docker_status = await client.docker.is_running()
    print(f"Docker running: {docker_status['is_docker_running']}")


asyncio.run(main())
```

## Prerequisites

Before using the client, ensure:

1. The Hummingbot API is running on `http://localhost:8000` (default)
2. Authentication credentials are configured (default: `admin:admin`)
3. Docker is running (for Docker-related operations)
4. Required dependencies are installed

## API Client Features

The client provides access to all Hummingbot API functionality through specialized routers:

### Core Routers

- **🐳 Docker** (`client.docker`): Container and image management
  - List/start/stop containers
  - Pull images with progress monitoring
  - Clean up exited containers

- **👤 Accounts** (`client.accounts`): Account and credential management
  - Create/delete accounts
  - Manage exchange credentials
  - List configured connectors per account

- **💰 Trading** (`client.trading`): Order and position management
  - Place/cancel orders
  - Monitor positions and PnL
  - Access trade history with pagination
  - Configure perpetual trading modes

- **💼 Portfolio** (`client.portfolio`): Portfolio monitoring and analysis
  - Real-time portfolio state
  - Token and account distribution
  - Historical portfolio tracking

- **🔌 Connectors** (`client.connectors`): Exchange connector information
  - List available connectors
  - Get configuration requirements
  - Access trading rules and order types

### Bot Management Routers

- **🤖 Bot Orchestration** (`client.bot_orchestration`): Bot lifecycle management
  - Start/stop bots
  - Deploy strategies
  - Monitor bot status via MQTT

- **📋 Controllers** (`client.controllers`): Advanced strategy controllers
- **📜 Scripts** (`client.scripts`): Traditional Hummingbot scripts
- **📊 Backtesting** (`client.backtesting`): Strategy backtesting
- **🗄️ Archived Bots** (`client.archived_bots`): Analysis of stopped bots
- **📈 Markets** (`client.markets`): Market data and candles

## Examples

### Jupyter Notebooks

The library includes comprehensive Jupyter notebooks demonstrating usage for each router. These provide interactive, step-by-step tutorials with explanations:

**Note:** Jupyter notebooks are not included in the repository by default. To run the example notebooks, install Jupyter:

```bash
pip install jupyter notebook
# or
pip install jupyterlab
```

Example notebooks cover:
- Basic usage demonstrating all features
- Router-specific examples (docker, accounts, trading, portfolio, connectors)
- Advanced patterns and error handling
- Real-time monitoring and bot management

Each notebook provides interactive demonstrations of the complete functionality with real API calls and detailed explanations.

## Advanced Usage

### Error Handling

```python
async with HummingbotClient("http://localhost:8000", "admin", "admin") as client:
    try:
        orders = await client.trading.search_orders({"limit": 10})
        print(f"Found {len(orders['data'])} orders")
    except aiohttp.ClientResponseError as e:
        print(f"API error: {e.status} - {e.message}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

### Pagination

```python
async def get_all_orders(client):
    """Fetch all orders using pagination."""
    all_orders = []
    cursor = None
    
    while True:
        filter_request = {"limit": 100}
        if cursor:
            filter_request["cursor"] = cursor
            
        response = await client.trading.search_orders(filter_request)
        all_orders.extend(response["data"])
        
        pagination = response["pagination"]
        if not pagination["has_more"]:
            break
            
        cursor = pagination["next_cursor"]
    
    return all_orders
```

### Custom Timeout

```python
import aiohttp

# Create client with custom timeout
timeout = aiohttp.ClientTimeout(total=60)  # 60 seconds
client = HummingbotClient(
    "http://localhost:8000",
    "admin",
    "admin",
    timeout=timeout
)
```

## Building

```bash
# Install build dependencies
uv pip install build

# Build the package
python -m build

# Install in development mode
pip install -e .
```

## License

Apache License 2.0
