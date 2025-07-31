# hummingbot-api-client

An async Python client for the Hummingbot API with modular router support.

## Installation

```bash
pip install hummingbot-api-client
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

#### 🐳 Docker Router (`client.docker`)
Container and image management for Hummingbot Docker instances.

**Key features:**
- Check Docker daemon status
- List/start/stop/remove containers
- Pull Docker images with progress monitoring
- Clean up exited containers
- Filter containers by name

**Common methods:**
- `is_running()` - Check if Docker is running
- `get_active_containers()` - List all running containers
- `start_container(name)` - Start a stopped container
- `stop_container(name)` - Stop a running container
- `pull_image(name, tag)` - Pull a Docker image

#### 👤 Accounts Router (`client.accounts`)
Manage trading accounts and exchange credentials.

**Key features:**
- Create and delete trading accounts
- Add/update/delete exchange credentials
- List configured connectors per account
- Secure credential storage

**Common methods:**
- `list_accounts()` - Get all account names
- `add_account(name)` - Create new account
- `add_credential(account, connector, credentials)` - Add exchange credentials
- `list_account_credentials(account)` - List connectors with credentials

#### 💰 Trading Router (`client.trading`)
Execute trades and manage orders across exchanges.

**Key features:**
- Place market and limit orders
- Cancel active orders
- Monitor open positions
- Track trade history with pagination
- Access funding payments (perpetuals)
- Configure leverage and position modes

**Common methods:**
- `place_order(account, connector, pair, type, amount, ...)` - Place an order
- `cancel_order(account, connector, order_id)` - Cancel an order
- `get_active_orders()` - List all active orders
- `get_positions()` - Get current positions
- `get_trades()` - Get trade history
- `set_leverage(account, connector, pair, leverage)` - Set leverage

#### 💼 Portfolio Router (`client.portfolio`)
Monitor and analyze portfolio performance.

**Key features:**
- Real-time portfolio state across all accounts
- Token distribution analysis
- Account balance tracking
- Historical portfolio data
- Value calculations in USD

**Common methods:**
- `get_state()` - Get current portfolio state
- `get_total_value()` - Calculate total portfolio value
- `get_distribution()` - Get token distribution percentages
- `get_token_holdings(token)` - Find specific token holdings
- `get_portfolio_summary()` - Get comprehensive summary

#### 🔌 Connectors Router (`client.connectors`)
Access exchange connector information.

**Key features:**
- List available exchange connectors
- Get configuration requirements
- Access trading rules (min/max amounts, tick sizes)
- Supported order types per exchange

**Common methods:**
- `list_connectors()` - List all available connectors
- `get_config_map(connector)` - Get required configuration fields
- `get_trading_rules(connector, pairs)` - Get trading rules
- `get_supported_order_types(connector)` - Get supported order types

### Bot Management Routers

#### 🤖 Bot Orchestration Router (`client.bot_orchestration`)
Manage bot lifecycle and deployment.

**Key features:**
- Start/stop/restart bots
- Deploy V2 scripts and controllers
- Monitor bot status via MQTT
- Get bot performance metrics
- Archive bot data
- Track bot runs with filtering

**Common methods:**
- `start_bot(name, script, config)` - Start a bot
- `stop_bot(name)` - Stop a bot
- `get_bot_status(name)` - Get bot status
- `deploy_v2_script(name, profile, script, config)` - Deploy a script bot
- `deploy_v2_controllers(name, profile, controllers)` - Deploy controller bot
- `get_bot_runs()` - Get bot run history

#### 📋 Controllers Router (`client.controllers`)
Manage V2 strategy controllers.

**Key features:**
- List available controller types
- Create/update/delete controllers
- Manage controller configurations
- Get controller templates
- Bot-specific controller configs

**Common methods:**
- `list_controllers()` - List all controllers by type
- `get_controller(type, name)` - Get controller content
- `create_or_update_controller(type, name, data)` - Create/update controller
- `list_controller_configs()` - List all configurations
- `get_bot_controller_configs(bot)` - Get bot's controller configs

#### 📜 Scripts Router (`client.scripts`)
Manage traditional Hummingbot scripts.

**Key features:**
- List available scripts
- Create/update/delete scripts
- Manage script configurations
- Get configuration templates

**Common methods:**
- `list_scripts()` - List all scripts
- `get_script(name)` - Get script content
- `create_or_update_script(name, data)` - Create/update script
- `list_script_configs()` - List all script configurations
- `get_script_config_template(name)` - Get config template

#### 📊 Backtesting Router (`client.backtesting`)
Run strategy backtests.

**Key features:**
- Run backtesting simulations
- Configure time periods and resolution
- Set trading costs
- Custom configuration options

**Common methods:**
- `run_backtesting(start_time, end_time, resolution, trade_cost, config)` - Run backtest

#### 🗄️ Archived Bots Router (`client.archived_bots`)
Analyze historical bot data.

**Key features:**
- List database files
- Get performance analysis
- Access trade/order history
- View executor and position data
- Analyze controller configurations

**Common methods:**
- `list_databases()` - List all database files
- `get_database_performance(db)` - Get performance metrics
- `get_database_trades(db, limit, offset)` - Get trade history
- `get_database_orders(db, limit, offset, status)` - Get order history
- `get_database_positions(db)` - Get position data

#### 📈 Market Data Router (`client.market_data`)
Access real-time and historical market data.

**Key features:**
- Real-time price feeds
- Historical candle data (OHLCV)
- Order book snapshots
- Funding rates (perpetuals)
- Volume/price analysis
- VWAP calculations

**Common methods:**
- `get_candles(connector, pair, interval, max_records)` - Get real-time candles
- `get_historical_candles(connector, pair, interval, start, end)` - Get historical data
- `get_prices(connector, pairs)` - Get current prices
- `get_order_book(connector, pair, depth)` - Get order book
- `get_funding_info(connector, pair)` - Get funding rates
- `get_vwap_for_volume(connector, pair, volume, is_buy)` - Calculate VWAP

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
