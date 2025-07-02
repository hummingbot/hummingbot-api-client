#!/usr/bin/env python3
"""
Trading Router Interactive Example

This script demonstrates the complete trading functionality of the Hummingbot API.
It shows you the actual code before executing each operation to help you learn how to use the client.

Usage:
    python trading_example.py              # Run automatically
    python trading_example.py --interactive # Interactive mode with step-by-step explanations
"""

import asyncio
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hummingbot_api_client.client import HummingbotAPIClient


class TradingRouterDemo:
    def __init__(self, interactive=False):
        self.interactive = interactive
        self.client = None

    def print_code_block(self, title: str, code: str, description: str = None):
        """Print a formatted code block with title and description."""
        print(f"\n{'='*70}")
        print(f"📝 {title}")
        if description:
            print(f"💡 {description}")
        print(f"{'='*70}")
        print("```python")
        print(code.strip())
        print("```")
        print(f"{'='*70}")

    async def wait_for_user(self, message: str):
        """Wait for user input in interactive mode."""
        if self.interactive:
            print(f"\n🔄 {message}")
            input("Press Enter to continue...")
        else:
            print(f"\n🔄 {message}")

    async def overview_trading_functionalities(self):
        """Present all Trading router functionalities."""
        print("💰 Trading Router - Available Functionalities")
        print("=" * 70)
        
        functionalities = [
            ("📊 Current Positions", "get_positions(params)", "Get current trading positions"),
            ("📈 Trade History", "get_trades(params)", "Get executed trade history"),
            ("🔄 Active Orders", "get_active_orders(params)", "Get currently active orders"),
            ("🔍 Search Orders", "search_orders(params)", "Search historical orders"),
            ("⚙️ Position Mode", "get_position_mode(account, connector)", "Get perpetual position mode"),
            ("🎯 Order Placement", "place_order(order_data)", "Place new trading orders"),
            ("❌ Cancel Orders", "cancel_order(order_id)", "Cancel existing orders"),
        ]
        
        print("Available Trading Router Methods:")
        print()
        # Calculate the maximum width for proper alignment
        max_icon_width = max(len(icon) for icon, _, _ in functionalities)
        max_method_width = max(len(method) for _, method, _ in functionalities)
        
        for icon, method, description in functionalities:
            print(f"  {icon:<{max_icon_width + 2}} {method:<{max_method_width + 2}} - {description}")
        
        await self.wait_for_user("Ready to explore trading operations?")

    async def demo_get_positions(self):
        """Demonstrate getting current positions."""
        self.print_code_block(
            "Get Current Trading Positions",
            """
# Get current trading positions with pagination
positions = await client.trading.get_positions({"limit": 10})

print(f"Current positions: {len(positions['data'])}")
for position in positions["data"]:
    trading_pair = position.get('trading_pair', 'Unknown')
    connector = position.get('connector_name', 'Unknown')
    amount = position.get('amount', 0)
    unrealized_pnl = position.get('unrealized_pnl', 0)
    
    print(f"  {trading_pair} on {connector}")
    print(f"    Size: {amount}, PnL: {unrealized_pnl}")

# You can also filter by account or trading pair
filtered_positions = await client.trading.get_positions({
    "account_names": ["main_account"],
    "trading_pairs": ["BTC-USDT"],
    "limit": 5
})
            """,
            "Shows your current open positions across all exchanges"
        )
        
        await self.wait_for_user("About to get current trading positions")
        
        try:
            positions = await self.client.trading.get_positions({"limit": 10})
            position_count = len(positions["data"])
            print(f"📊 Found {position_count} current positions:")
            
            for position in positions["data"][:5]:  # Show first 5
                trading_pair = position.get('trading_pair', 'Unknown')
                connector = position.get('connector_name', 'Unknown')
                amount = position.get('amount', 0)
                unrealized_pnl = position.get('unrealized_pnl', 0)
                print(f"  - {trading_pair} on {connector}")
                print(f"    Size: {amount}, PnL: {unrealized_pnl}")
            
            if position_count > 5:
                print(f"    ... and {position_count - 5} more positions")
            
            return positions
        except Exception as e:
            print(f"❌ Error getting positions: {e}")
            return {"data": [], "pagination": {}}

    async def demo_get_trades(self):
        """Demonstrate getting trade history."""
        self.print_code_block(
            "Get Trade History",
            """
# Get recent trade history
trades = await client.trading.get_trades({"limit": 5})

print(f"Recent trades: {len(trades['data'])}")
for trade in trades["data"]:
    trade_type = trade.get('trade_type', 'Unknown')
    amount = trade.get('amount', 0)
    trading_pair = trade.get('trading_pair', 'Unknown')
    price = trade.get('price', 0)
    fee_paid = trade.get('fee_paid', 0)
    fee_currency = trade.get('fee_currency', '')
    timestamp = trade.get('timestamp', 'Unknown')
    
    print(f"  {trade_type} {amount} {trading_pair}")
    print(f"    Price: {price}, Fee: {fee_paid} {fee_currency}")
    print(f"    Time: {timestamp}")

# Filter trades by account, pair, or date range
filtered_trades = await client.trading.get_trades({
    "account_names": ["main_account"],
    "trading_pairs": ["BTC-USDT", "ETH-USDT"],
    "limit": 10
})
            """,
            "Shows your executed trades with prices, fees, and timestamps"
        )
        
        await self.wait_for_user("About to get recent trade history")
        
        try:
            trades = await self.client.trading.get_trades({"limit": 5})
            trade_count = len(trades["data"])
            print(f"📈 Found {trade_count} recent trades:")
            
            for trade in trades["data"]:
                trade_type = trade.get('trade_type', 'Unknown')
                amount = trade.get('amount', 0)
                trading_pair = trade.get('trading_pair', 'Unknown')
                price = trade.get('price', 0)
                fee_paid = trade.get('fee_paid', 0)
                fee_currency = trade.get('fee_currency', '')
                timestamp = trade.get('timestamp', 'Unknown')
                
                print(f"  - {trade_type} {amount} {trading_pair}")
                print(f"    Price: {price}, Fee: {fee_paid} {fee_currency}")
                print(f"    Time: {timestamp}")
            
            return trades
        except Exception as e:
            print(f"❌ Error getting trades: {e}")
            return {"data": [], "pagination": {}}

    async def demo_get_active_orders(self):
        """Demonstrate getting active orders."""
        self.print_code_block(
            "Get Active Orders",
            """
# Get currently active (in-flight) orders
active_orders = await client.trading.get_active_orders({"limit": 10})

print(f"Active orders: {len(active_orders['data'])}")
for order in active_orders["data"]:
    trade_type = order.get('trade_type', 'Unknown')
    amount = order.get('amount', 0)
    trading_pair = order.get('trading_pair', 'Unknown')
    price = order.get('price', 0)
    status = order.get('status', 'Unknown')
    order_id = order.get('order_id', 'Unknown')
    
    print(f"  {trade_type} {amount} {trading_pair}")
    print(f"    Price: {price}, Status: {status}")
    print(f"    Order ID: {order_id}")

# Filter by account or trading pair
filtered_orders = await client.trading.get_active_orders({
    "account_names": ["main_account"],
    "trading_pairs": ["BTC-USDT"]
})
            """,
            "Shows orders that are currently pending or partially filled"
        )
        
        await self.wait_for_user("About to get active orders")
        
        try:
            active_orders = await self.client.trading.get_active_orders({"limit": 10})
            order_count = len(active_orders["data"])
            print(f"🔄 Found {order_count} active orders:")
            
            for order in active_orders["data"]:
                trade_type = order.get('trade_type', 'Unknown')
                amount = order.get('amount', 0)
                trading_pair = order.get('trading_pair', 'Unknown')
                price = order.get('price', 0)
                status = order.get('status', 'Unknown')
                order_id = order.get('order_id', 'Unknown')
                
                print(f"  - {trade_type} {amount} {trading_pair}")
                print(f"    Price: {price}, Status: {status}")
                print(f"    Order ID: {order_id}")
            
            return active_orders
        except Exception as e:
            print(f"❌ Error getting active orders: {e}")
            return {"data": [], "pagination": {}}

    async def demo_search_orders(self):
        """Demonstrate searching historical orders."""
        self.print_code_block(
            "Search Historical Orders",
            """
# Search historical orders from database
orders = await client.trading.search_orders({"limit": 5})

order_count = len(orders["data"])
total_count = orders["pagination"].get("total_count", order_count)
print(f"Found {order_count} orders (total: {total_count})")

for order in orders["data"]:
    trade_type = order.get('trade_type', 'Unknown')
    amount = order.get('amount', 0)
    trading_pair = order.get('trading_pair', 'Unknown')
    price = order.get('price', 0)
    status = order.get('status', 'Unknown')
    created_at = order.get('created_at', 'Unknown')
    
    print(f"  {trade_type} {amount} {trading_pair}")
    print(f"    Price: {price}, Status: {status}")
    print(f"    Created: {created_at}")

# Advanced filtering examples
filtered_orders = await client.trading.search_orders({
    "account_names": ["main_account"],
    "trading_pairs": ["BTC-USDT", "ETH-USDT"],
    "status": "FILLED",
    "limit": 10
})
            """,
            "Searches through your complete order history with powerful filters"
        )
        
        await self.wait_for_user("About to search historical orders")
        
        try:
            orders = await self.client.trading.search_orders({"limit": 5})
            order_count = len(orders["data"])
            total_count = orders["pagination"].get("total_count", order_count)
            print(f"📋 Found {order_count} orders (total: {total_count}):")
            
            for order in orders["data"]:
                trade_type = order.get('trade_type', 'Unknown')
                amount = order.get('amount', 0)
                trading_pair = order.get('trading_pair', 'Unknown')
                price = order.get('price', 0)
                status = order.get('status', 'Unknown')
                created_at = order.get('created_at', 'Unknown')
                
                print(f"  - {trade_type} {amount} {trading_pair}")
                print(f"    Price: {price}, Status: {status}")
                print(f"    Created: {created_at}")
            
            return orders
        except Exception as e:
            print(f"❌ Error searching orders: {e}")
            return {"data": [], "pagination": {}}

    async def demo_position_mode(self):
        """Demonstrate position mode operations."""
        self.print_code_block(
            "Get Position Mode (Perpetual Trading)",
            """
# Get position mode for perpetual connectors
accounts = await client.accounts.list_accounts()

for account in accounts:
    # Check if this account has perpetual connectors
    credentials = await client.accounts.list_account_credentials(account)
    
    for connector in credentials:
        if "perpetual" in connector.lower():
            print(f"Found perpetual connector: {connector} in account {account}")
            
            # Get position mode
            mode = await client.trading.get_position_mode(account, connector)
            print(f"Current position mode: {mode}")
            
            # Position modes are typically:
            # - HEDGE: Separate long/short positions
            # - ONEWAY: Net positions only
            break

# Note: Changing position mode typically requires no open positions
# set_result = await client.trading.set_position_mode(account, connector, "HEDGE")
            """,
            "Manages position modes for perpetual/futures trading"
        )
        
        await self.wait_for_user("About to check position mode operations")
        
        try:
            # Try to find an account with perpetual connectors
            accounts = await self.client.accounts.list_accounts()
            perpetual_found = False
            
            for account in accounts:
                try:
                    # Check if this account has perpetual connectors
                    credentials = await self.client.accounts.list_account_credentials(account)
                    for connector in credentials:
                        if "perpetual" in connector.lower():
                            print(f"🔄 Found perpetual connector: {connector} in account {account}")
                            
                            # Try to get position mode
                            try:
                                mode = await self.client.trading.get_position_mode(account, connector)
                                print(f"📊 Current position mode: {mode}")
                                perpetual_found = True
                                break
                            except Exception as e:
                                print(f"⚠️  Could not get position mode for {connector}: {e}")
                        
                except Exception:
                    continue
                
                if perpetual_found:
                    break
            
            if not perpetual_found:
                print("ℹ️  No perpetual connectors with credentials found")
            
            return perpetual_found
        except Exception as e:
            print(f"❌ Error with position mode operations: {e}")
            return False

    async def demo_order_placement_info(self):
        """Show order placement capabilities without executing."""
        self.print_code_block(
            "Order Placement Example",
            """
# Example order placement (NOT executed in this demo)
order_data = {
    "account_name": "main_account",
    "connector_name": "binance",
    "trading_pair": "BTC-USDT",
    "trade_type": "BUY",
    "order_type": "LIMIT",
    "amount": 0.001,
    "price": 50000.0
}

# Place a limit buy order
result = await client.trading.place_order(order_data)
print(f"Order placed: {result}")

# Place a market order (no price needed)
market_order = {
    "account_name": "main_account",
    "connector_name": "binance",
    "trading_pair": "ETH-USDT",
    "trade_type": "SELL",
    "order_type": "MARKET",
    "amount": 0.1
}

result = await client.trading.place_order(market_order)
print(f"Market order placed: {result}")

# Cancel an order
cancel_result = await client.trading.cancel_order("order_id_here")
print(f"Order cancelled: {cancel_result}")
            """,
            "Shows how to place and manage orders (not executed for safety)"
        )
        
        await self.wait_for_user("About to show order placement capabilities")
        
        try:
            # Check which accounts are ready for trading
            accounts = await self.client.accounts.list_accounts()
            trading_ready_accounts = []
            
            print("🔍 Checking accounts for trading readiness:")
            for account in accounts:
                try:
                    credentials = await self.client.accounts.list_account_credentials(account)
                    if credentials:
                        print(f"  ✅ {account}: {len(credentials)} connectors configured")
                        trading_ready_accounts.append((account, credentials))
                    else:
                        print(f"  ⚠️  {account}: No connectors configured")
                except Exception:
                    print(f"  ❌ {account}: Error checking credentials")
            
            if trading_ready_accounts:
                print(f"\n📊 {len(trading_ready_accounts)} accounts ready for trading")
                
                # Show example for first trading-ready account
                account, connectors = trading_ready_accounts[0]
                connector = connectors[0]
                
                print(f"\n🎯 Example order for account: {account}, connector: {connector}")
                print(f"📝 Order structure:")
                print(f"   - Trading pair: BTC-USDT")
                print(f"   - Order type: LIMIT")
                print(f"   - Side: BUY")
                print(f"   - Amount: 0.001")
                print(f"   - Price: Current market price - 5%")
                
                print(f"\n⚠️  Note: Actual order placement requires:")
                print(f"   - Valid API credentials")
                print(f"   - Sufficient account balance")
                print(f"   - Proper risk management")
                
                # Show the structure of what a real order would look like
                example_order = {
                    "account_name": account,
                    "connector_name": connector,
                    "trading_pair": "BTC-USDT",
                    "trade_type": "BUY",
                    "order_type": "LIMIT",
                    "amount": 0.001,
                    "price": 50000.0  # Example price
                }
                
                print(f"\n📋 Example order structure: {example_order}")
                return trading_ready_accounts
            else:
                print("\n⚠️  No accounts configured for trading")
                return []
                
        except Exception as e:
            print(f"❌ Error checking trading capabilities: {e}")
            return []

    async def demo_filtering_capabilities(self):
        """Demonstrate advanced filtering capabilities."""
        self.print_code_block(
            "Advanced Filtering Examples",
            """
# Example filters for different trading queries

# Filter by account
account_trades = await client.trading.get_trades({
    "account_names": ["main_account"],
    "limit": 10
})

# Filter by trading pairs
pair_trades = await client.trading.get_trades({
    "trading_pairs": ["BTC-USDT", "ETH-USDT"],
    "limit": 10
})

# Filter orders by status
filled_orders = await client.trading.search_orders({
    "status": "FILLED",
    "limit": 10
})

# Combine multiple filters
filtered_data = await client.trading.search_orders({
    "account_names": ["main_account"],
    "trading_pairs": ["BTC-USDT"],
    "status": "FILLED",
    "limit": 5,
    "offset": 0  # For pagination
})

# Use pagination to get more data
next_page = await client.trading.search_orders({
    "account_names": ["main_account"],
    "limit": 5,
    "offset": 5
})

print(f"First page: {len(filtered_data['data'])} orders")
print(f"Next page: {len(next_page['data'])} orders")
            """,
            "Shows powerful filtering options for analyzing your trading data"
        )
        
        await self.wait_for_user("About to demonstrate filtering capabilities")
        
        try:
            print("🔍 Advanced filtering capabilities:")
            
            # Demonstrate different filter types
            filters_examples = [
                {
                    "name": "By account",
                    "filter": {"account_names": ["master_account"], "limit": 3}
                },
                {
                    "name": "By trading pair",
                    "filter": {"trading_pairs": ["BTC-USDT", "ETH-USDT"], "limit": 3}
                },
                {
                    "name": "Recent orders only", 
                    "filter": {"limit": 5}
                }
            ]
            
            for example in filters_examples:
                print(f"\n📋 {example['name']}:")
                try:
                    result = await self.client.trading.search_orders(example["filter"])
                    count = len(result.get("data", []))
                    total = result.get("pagination", {}).get("total_count", count)
                    print(f"   Found {count} orders (total matching: {total})")
                except Exception as e:
                    print(f"   Error: {e}")
            
            return True
        except Exception as e:
            print(f"❌ Error demonstrating filtering: {e}")
            return False

    async def run_interactive_demo(self):
        """Run the complete Trading router interactive demo."""
        print("💰 Trading Router Interactive Demo")
        print("=" * 70)
        print("This demo will show you how to monitor and manage your trading activity.")
        print("Perfect for learning trading operations with the Hummingbot API!")
        print("=" * 70)
        
        async with HummingbotAPIClient("http://localhost:8000", "admin", "admin") as client:
            self.client = client
            
            # Overview of functionalities
            await self.overview_trading_functionalities()
            
            # Step 1: Check current positions
            positions = await self.demo_get_positions()
            
            # Step 2: Get recent trades
            trades = await self.demo_get_trades()
            
            # Step 3: Check active orders
            active_orders = await self.demo_get_active_orders()
            
            # Step 4: Search historical orders
            historical_orders = await self.demo_search_orders()
            
            # Step 5: Demonstrate position mode
            perpetual_available = await self.demo_position_mode()
            
            # Step 6: Show order placement capabilities
            trading_accounts = await self.demo_order_placement_info()
            
            # Step 7: Demonstrate filtering
            await self.demo_filtering_capabilities()
            
            print("\n" + "=" * 70)
            print("✅ Trading Router Demo Completed!")
            print("\n📝 Summary:")
            print(f"  - Current positions: {len(positions.get('data', []))}")
            print(f"  - Recent trades: {len(trades.get('data', []))}")
            print(f"  - Active orders: {len(active_orders.get('data', []))}")
            print(f"  - Historical orders available: {historical_orders.get('pagination', {}).get('total_count', 'Unknown')}")
            print(f"  - Perpetual trading available: {'Yes' if perpetual_available else 'No'}")
            print(f"  - Trading-ready accounts: {len(trading_accounts)}")
            
            print("\n🎓 You now know how to monitor and manage trading operations!")
            print("💡 Try implementing these in your own scripts using the code examples shown.")
            
            return True


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Trading Router Interactive Demo")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode with step-by-step explanations")
    args = parser.parse_args()
    
    demo = TradingRouterDemo(interactive=args.interactive)
    
    try:
        success = await demo.run_interactive_demo()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())