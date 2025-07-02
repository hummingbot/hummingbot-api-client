#!/usr/bin/env python3
"""
Archived Bots Router Test Script

This script demonstrates the archived bots functionality of the Hummingbot API.
It covers database listing, analysis, and historical data extraction.

Usage:
    python archived_bots_example.py              # Run automatically
    python archived_bots_example.py --interactive # Interactive mode with explanations
"""

import asyncio
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hummingbot_api_client.client import HummingbotClient


class ArchivedBotsRouterTester:
    def __init__(self, interactive=False):
        self.interactive = interactive
        self.client = None

    async def wait_for_user(self, message):
        """Wait for user input in interactive mode."""
        if self.interactive:
            print(f"\n🔄 {message}")
            input("Press Enter to continue...")
        else:
            print(f"\n🔄 {message}")

    async def step_1_list_databases(self):
        """Step 1: List all available database files."""
        await self.wait_for_user("Step 1: Listing available database files")
        
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

    async def step_2_analyze_database(self, databases):
        """Step 2: Analyze the first available database."""
        if not databases:
            print("⚠️  No databases available for analysis")
            return None
        
        db_path = databases[0]
        await self.wait_for_user(f"Step 2: Analyzing database '{db_path}'")
        
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

    async def step_3_get_performance_data(self, db_path):
        """Step 3: Get performance analysis for the database."""
        if not db_path:
            print("⚠️  No database available for performance analysis")
            return
        
        await self.wait_for_user(f"Step 3: Getting performance data for '{db_path}'")
        
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

    async def step_4_get_trades_and_orders(self, db_path):
        """Step 4: Get trade and order history from the database."""
        if not db_path:
            print("⚠️  No database available for trade/order history")
            return
        
        await self.wait_for_user(f"Step 4: Getting trades and orders for '{db_path}'")
        
        try:
            # Get recent trades
            print(f"📊 Getting recent trades...")
            trades = await self.client.archived_bots.get_database_trades(db_path, limit=5)
            trade_list = trades.get("trades", [])
            pagination = trades.get("pagination", {})
            
            print(f"  Recent Trades: {len(trade_list)} (Total: {pagination.get('total', 0)})")
            for trade in trade_list:
                print(f"    - {trade.get('symbol', 'Unknown')} {trade.get('trade_type', 'Unknown')} "
                      f"{trade.get('amount', 0)} @ {trade.get('price', 0)}")
            
            # Get recent orders
            print(f"📋 Getting recent orders...")
            orders = await self.client.archived_bots.get_database_orders(db_path, limit=5)
            order_list = orders.get("orders", [])
            pagination = orders.get("pagination", {})
            
            print(f"  Recent Orders: {len(order_list)} (Total: {pagination.get('total', 0)})")
            for order in order_list:
                print(f"    - {order.get('symbol', 'Unknown')} {order.get('trade_type', 'Unknown')} "
                      f"{order.get('amount', 0)} @ {order.get('price', 0)} [{order.get('last_status', 'Unknown')}]")
            
        except Exception as e:
            print(f"❌ Error getting trades/orders: {e}")

    async def step_5_get_executors(self, db_path):
        """Step 5: Get executor data from the database."""
        if not db_path:
            print("⚠️  No database available for executor data")
            return
        
        await self.wait_for_user(f"Step 5: Getting executor data for '{db_path}'")
        
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

    async def step_6_demonstrate_filtering(self, db_path):
        """Step 6: Demonstrate filtering capabilities."""
        if not db_path:
            print("⚠️  No database available for filtering demonstration")
            return
        
        await self.wait_for_user(f"Step 6: Demonstrating filtering capabilities")
        
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

    async def run_test_suite(self):
        """Run the complete Archived Bots router test suite."""
        print("🗃️  Starting Archived Bots Router Test Suite")
        print("=" * 50)
        
        async with HummingbotClient("http://localhost:8000", "admin", "admin") as client:
            self.client = client
            
            # Step 1: List databases
            databases = await self.step_1_list_databases()
            
            # Step 2: Analyze a database
            selected_db = await self.step_2_analyze_database(databases)
            
            # Step 3: Get performance data
            await self.step_3_get_performance_data(selected_db)
            
            # Step 4: Get trades and orders
            await self.step_4_get_trades_and_orders(selected_db)
            
            # Step 5: Get executors
            await self.step_5_get_executors(selected_db)
            
            # Step 6: Demonstrate filtering
            await self.step_6_demonstrate_filtering(selected_db)
            
            print("\n" + "=" * 50)
            print("✅ Archived Bots Router Test Suite Completed Successfully!")
            print("\n📝 Summary:")
            print(f"  - Total databases found: {len(databases)}")
            if selected_db:
                print(f"  - Analyzed database: {selected_db}")
                print(f"  - Demonstrated: status, summary, performance, trades, orders, executors")
            print(f"  - All archived bots functionality tested")
            
            return True


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test Archived Bots Router functionality")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode with step-by-step explanations")
    args = parser.parse_args()
    
    tester = ArchivedBotsRouterTester(interactive=args.interactive)
    
    try:
        success = await tester.run_test_suite()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())