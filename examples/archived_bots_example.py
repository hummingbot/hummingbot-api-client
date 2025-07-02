#!/usr/bin/env python3
"""
Archived Bots Router Interactive Example

This script demonstrates the archived bots functionality of the Hummingbot API.
It shows you the actual code before executing each operation to help you learn how to use the client.

Usage:
    python archived_bots_example.py              # Run automatically
    python archived_bots_example.py --interactive # Interactive mode with step-by-step explanations
"""

import asyncio
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hummingbot_api_client.client import HummingbotAPIClient


class ArchivedBotsRouterDemo:
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

    async def overview_archived_bots_functionalities(self):
        """Present all Archived Bots router functionalities."""
        print("🗃️ Archived Bots Router - Available Functionalities")
        print("=" * 70)
        
        functionalities = [
            ("📊 List Databases", "list_databases()", "Get all available database files"),
            ("🏥 Database Status", "get_database_status(db_path)", "Check database health"),
            ("📋 Database Summary", "get_database_summary(db_path)", "Get basic statistics"),
            ("📈 Performance Data", "get_database_performance(db_path)", "Get performance analysis"),
            ("💼 Trade History", "get_database_trades(db_path, params)", "Get trade records"),
            ("📋 Order History", "get_database_orders(db_path, params)", "Get order records"),
            ("🤖 Executors", "get_database_executors(db_path)", "Get executor information"),
        ]
        
        print("Available Archived Bots Router Methods:")
        print()
        # Calculate the maximum width for proper alignment
        max_icon_width = max(len(icon) for icon, _, _ in functionalities)
        max_method_width = max(len(method) for _, method, _ in functionalities)
        
        for icon, method, description in functionalities:
            print(f"  {icon:<{max_icon_width + 2}} {method:<{max_method_width + 2}} - {description}")
        
        await self.wait_for_user("Ready to explore archived bot data?")

    async def demo_list_databases(self):
        """Demonstrate listing available databases."""
        self.print_code_block(
            "List Available Database Files",
            """
# Get all available database files
databases = await client.archived_bots.list_databases()

print(f"Found {len(databases)} database files:")
for db in databases:
    print(f"  - {db}")

# Databases contain historical trading data from your bots
# Each bot run creates its own database file
            """,
            "Shows all archived bot databases available for analysis"
        )
        
        await self.wait_for_user("About to list available database files")
        
        try:
            databases = await self.client.archived_bots.list_databases()
            print(f"📊 Found {len(databases)} database files:")
            for db in databases[:10]:  # Show first 10
                print(f"  - {db}")
            if len(databases) > 10:
                print(f"  ... and {len(databases) - 10} more databases")
            
            return databases
        except Exception as e:
            print(f"❌ Error listing databases: {e}")
            return []

    async def demo_analyze_database(self, databases):
        """Demonstrate analyzing a database."""
        if not databases:
            print("⚠️  No databases available for analysis")
            return None
        
        db_path = databases[0]
        
        self.print_code_block(
            "Analyze Database Health and Summary",
            f"""
# Get database status and health check
db_path = "{db_path}"
status = await client.archived_bots.get_database_status(db_path)
print(f"Database healthy: {{status.get('healthy')}}")

# Get basic database summary
summary = await client.archived_bots.get_database_summary(db_path)
print(f"Total Orders: {{summary.get('total_orders', 0)}}")
print(f"Total Trades: {{summary.get('total_trades', 0)}}")
print(f"Total Executors: {{summary.get('total_executors', 0)}}")
print(f"Trading Pairs: {{summary.get('trading_pairs', [])}}")
print(f"Exchanges: {{summary.get('exchanges', [])}}")

# This gives you a quick overview of the bot's activity
            """,
            "Provides health check and basic statistics for a bot database"
        )
        
        await self.wait_for_user(f"About to analyze database '{db_path}'")
        
        try:
            # Get database status
            print(f"📋 Getting status for: {db_path}")
            status = await self.client.archived_bots.get_database_status(db_path)
            print(f"  Status: {'Healthy' if status.get('healthy') else 'Issues detected'}")
            
            # Get database summary
            print(f"📊 Getting summary for: {db_path}")
            summary = await self.client.archived_bots.get_database_summary(db_path)
            print(f"  Total Orders: {summary.get('total_orders', 0)}")
            print(f"  Total Trades: {summary.get('total_trades', 0)}")
            print(f"  Total Executors: {summary.get('total_executors', 0)}")
            print(f"  Trading Pairs: {summary.get('trading_pairs', [])}")
            print(f"  Exchanges: {summary.get('exchanges', [])}")
            
            return db_path
        except Exception as e:
            print(f"❌ Error analyzing database: {e}")
            return None

    async def demo_get_performance_data(self, db_path):
        """Demonstrate getting performance analysis."""
        if not db_path:
            print("⚠️  No database available for performance analysis")
            return
        
        self.print_code_block(
            "Get Performance Analysis",
            f"""
# Get detailed performance analysis
db_path = "{db_path}"
performance = await client.archived_bots.get_database_performance(db_path)

if "error" not in performance:
    summary = performance.get("summary", {{}})
    print("Performance Summary:")
    print(f"  Total Trades: {{summary.get('total_trades', 0)}}")
    print(f"  Final Net PnL: {{summary.get('final_net_pnl_quote', 0):.4f}}")
    print(f"  Final Realized PnL: {{summary.get('final_realized_pnl_quote', 0):.4f}}")
    print(f"  Final Unrealized PnL: {{summary.get('final_unrealized_pnl_quote', 0):.4f}}")
    print(f"  Total Fees: {{summary.get('total_fees_quote', 0):.4f}}")
    print(f"  Final Net Position: {{summary.get('final_net_position', 0):.6f}}")
    
    # Performance data contains detailed trade-by-trade analysis
    perf_data = performance.get("performance_data", [])
    print(f"  Performance Records: {{len(perf_data)}}")
else:
    print(f"Performance data not available: {{performance['error']}}")
            """,
            "Provides detailed profit/loss analysis for the bot's trading session"
        )
        
        await self.wait_for_user(f"About to get performance data for '{db_path}'")
        
        try:
            performance = await self.client.archived_bots.get_database_performance(db_path)
            
            if "error" in performance:
                print(f"⚠️  {performance['error']}")
                return
            
            summary = performance.get("summary", {})
            print(f"📈 Performance Summary:")
            print(f"  Total Trades: {summary.get('total_trades', 0)}")
            print(f"  Final Net PnL: {summary.get('final_net_pnl_quote', 0):.4f}")
            print(f"  Final Realized PnL: {summary.get('final_realized_pnl_quote', 0):.4f}")
            print(f"  Final Unrealized PnL: {summary.get('final_unrealized_pnl_quote', 0):.4f}")
            print(f"  Total Fees: {summary.get('total_fees_quote', 0):.4f}")
            print(f"  Final Net Position: {summary.get('final_net_position', 0):.6f}")
            
            perf_data = performance.get("performance_data", [])
            print(f"  Performance Records: {len(perf_data)}")
            
        except Exception as e:
            print(f"❌ Error getting performance data: {e}")

    async def demo_get_trades_and_orders(self, db_path):
        """Demonstrate getting trade and order history."""
        if not db_path:
            print("⚠️  No database available for trade/order history")
            return
        
        self.print_code_block(
            "Get Trade and Order History",
            f"""
# Get trade history with pagination
db_path = "{db_path}"
trades = await client.archived_bots.get_database_trades(db_path, limit=5)

trade_list = trades.get("trades", [])
pagination = trades.get("pagination", {{}})

print(f"Recent Trades: {{len(trade_list)}} (Total: {{pagination.get('total', 0)}})")
for trade in trade_list:
    symbol = trade.get('symbol', 'Unknown')
    trade_type = trade.get('trade_type', 'Unknown')
    amount = trade.get('amount', 0)
    price = trade.get('price', 0)
    print(f"  - {{symbol}} {{trade_type}} {{amount}} @ {{price}}")

# Get order history
orders = await client.archived_bots.get_database_orders(db_path, limit=5)
order_list = orders.get("orders", [])

print(f"Recent Orders: {{len(order_list)}}")
for order in order_list:
    symbol = order.get('symbol', 'Unknown')
    trade_type = order.get('trade_type', 'Unknown')
    status = order.get('last_status', 'Unknown')
    print(f"  - {{symbol}} {{trade_type}} [{{status}}]")

# You can also filter by status, symbol, or use pagination
filtered_orders = await client.archived_bots.get_database_orders(
    db_path, limit=10, status="FILLED"
)
            """,
            "Shows detailed trade and order records from the bot's database"
        )
        
        await self.wait_for_user(f"About to get trades and orders for '{db_path}'")
        
        try:
            # Get recent trades
            print(f"📊 Getting recent trades...")
            trades = await self.client.archived_bots.get_database_trades(db_path, limit=5)
            trade_list = trades.get("trades", [])
            pagination = trades.get("pagination", {})
            
            print(f"  Recent Trades: {len(trade_list)} (Total: {pagination.get('total', 0)})")
            for trade in trade_list:
                symbol = trade.get('symbol', 'Unknown')
                trade_type = trade.get('trade_type', 'Unknown')
                amount = trade.get('amount', 0)
                price = trade.get('price', 0)
                print(f"    - {symbol} {trade_type} {amount} @ {price}")
            
            # Get recent orders
            print(f"📋 Getting recent orders...")
            orders = await self.client.archived_bots.get_database_orders(db_path, limit=5)
            order_list = orders.get("orders", [])
            pagination = orders.get("pagination", {})
            
            print(f"  Recent Orders: {len(order_list)} (Total: {pagination.get('total', 0)})")
            for order in order_list:
                symbol = order.get('symbol', 'Unknown')
                trade_type = order.get('trade_type', 'Unknown')
                amount = order.get('amount', 0)
                price = order.get('price', 0)
                status = order.get('last_status', 'Unknown')
                print(f"    - {symbol} {trade_type} {amount} @ {price} [{status}]")
            
        except Exception as e:
            print(f"❌ Error getting trades/orders: {e}")

    async def demo_get_executors(self, db_path):
        """Demonstrate getting executor data."""
        if not db_path:
            print("⚠️  No database available for executor data")
            return
        
        self.print_code_block(
            "Get Executor Information",
            f"""
# Get executor data from the database
db_path = "{db_path}"
executors = await client.archived_bots.get_database_executors(db_path)

executor_list = executors.get("executors", [])
total = executors.get("total", 0)

print(f"Found {{total}} executors:")
for i, executor in enumerate(executor_list):
    print(f"  {{i+1}}. Executor ID: {{executor.get('id', 'Unknown')}}")
    print(f"     Type: {{executor.get('type', 'Unknown')}}")
    print(f"     Status: {{executor.get('status', 'Unknown')}}")

# Executors are the trading strategies that were running
# Each executor represents a different strategy or market maker
            """,
            "Shows the trading strategies (executors) that were active in this bot session"
        )
        
        await self.wait_for_user(f"About to get executor data for '{db_path}'")
        
        try:
            executors = await self.client.archived_bots.get_database_executors(db_path)
            executor_list = executors.get("executors", [])
            total = executors.get("total", 0)
            
            print(f"🤖 Found {total} executors:")
            for i, executor in enumerate(executor_list[:3]):  # Show first 3
                print(f"  {i+1}. Executor ID: {executor.get('id', 'Unknown')}")
                print(f"     Type: {executor.get('type', 'Unknown')}")
                print(f"     Status: {executor.get('status', 'Unknown')}")
                
            if len(executor_list) > 3:
                print(f"     ... and {len(executor_list) - 3} more executors")
            
        except Exception as e:
            print(f"❌ Error getting executors: {e}")

    async def demo_filtering_capabilities(self, db_path):
        """Demonstrate filtering capabilities."""
        if not db_path:
            print("⚠️  No database available for filtering demonstration")
            return
        
        self.print_code_block(
            "Filtering and Pagination Examples",
            f"""
# Filter orders by status
db_path = "{db_path}"
filled_orders = await client.archived_bots.get_database_orders(
    db_path, limit=3, status="FILLED"
)
filled_list = filled_orders.get("orders", [])
print(f"Filled orders: {{len(filled_list)}}")

# Get trades with pagination
trades_page1 = await client.archived_bots.get_database_trades(
    db_path, limit=2, offset=0
)
trades_page2 = await client.archived_bots.get_database_trades(
    db_path, limit=2, offset=2
)

page1_list = trades_page1.get("trades", [])
page2_list = trades_page2.get("trades", [])
print(f"Page 1: {{len(page1_list)}} trades")
print(f"Page 2: {{len(page2_list)}} trades")

# You can also filter by:
# - symbol: specific trading pairs
# - time ranges: start_time, end_time
# - order types: LIMIT, MARKET, etc.
            """,
            "Shows how to filter and paginate through large datasets"
        )
        
        await self.wait_for_user("About to demonstrate filtering capabilities")
        
        try:
            print(f"🔍 Filtering capabilities:")
            
            # Filter orders by status
            print(f"  📋 Getting filled orders only...")
            filled_orders = await self.client.archived_bots.get_database_orders(
                db_path, limit=3, status="FILLED"
            )
            filled_list = filled_orders.get("orders", [])
            print(f"     Found {len(filled_list)} filled orders")
            
            # Paginated trades
            print(f"  📊 Getting trades with pagination...")
            trades_page1 = await self.client.archived_bots.get_database_trades(
                db_path, limit=2, offset=0
            )
            trades_page2 = await self.client.archived_bots.get_database_trades(
                db_path, limit=2, offset=2
            )
            
            page1_list = trades_page1.get("trades", [])
            page2_list = trades_page2.get("trades", [])
            print(f"     Page 1: {len(page1_list)} trades")
            print(f"     Page 2: {len(page2_list)} trades")
            
        except Exception as e:
            print(f"❌ Error demonstrating filtering: {e}")

    async def run_interactive_demo(self):
        """Run the complete Archived Bots router interactive demo."""
        print("🗃️ Archived Bots Router Interactive Demo")
        print("=" * 70)
        print("This demo will show you how to analyze historical bot trading data.")
        print("Perfect for learning performance analysis with the Hummingbot API!")
        print("=" * 70)
        
        async with HummingbotAPIClient("http://localhost:8000", "admin", "admin") as client:
            self.client = client
            
            # Overview of functionalities
            await self.overview_archived_bots_functionalities()
            
            # Step 1: List databases
            databases = await self.demo_list_databases()
            
            # Step 2: Analyze a database
            selected_db = await self.demo_analyze_database(databases)
            
            # Step 3: Get performance data
            await self.demo_get_performance_data(selected_db)
            
            # Step 4: Get trades and orders
            await self.demo_get_trades_and_orders(selected_db)
            
            # Step 5: Get executors
            await self.demo_get_executors(selected_db)
            
            # Step 6: Demonstrate filtering
            await self.demo_filtering_capabilities(selected_db)
            
            print("\n" + "=" * 70)
            print("✅ Archived Bots Router Demo Completed!")
            print("\n📝 Summary:")
            print(f"  - Total databases found: {len(databases)}")
            if selected_db:
                print(f"  - Analyzed database: {selected_db}")
                print(f"  - Demonstrated: status, summary, performance, trades, orders, executors")
            print(f"  - All archived bots functionality tested")
            
            print("\n🎓 You now know how to analyze historical bot performance!")
            print("💡 Try implementing these in your own scripts using the code examples shown.")
            
            return True


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Archived Bots Router Interactive Demo")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode with step-by-step explanations")
    args = parser.parse_args()
    
    demo = ArchivedBotsRouterDemo(interactive=args.interactive)
    
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