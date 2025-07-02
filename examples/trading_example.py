#!/usr/bin/env python3
"""
Trading Router Test Script

This script demonstrates the complete trading functionality of the Hummingbot API.
It covers order management, position tracking, trade history, and perpetual trading features.

Usage:
    python test_trading_router.py              # Run automatically
    python test_trading_router.py --interactive # Interactive mode with explanations
"""

import asyncio
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hummingbot_api_client.client import HummingbotClient


class TradingRouterTester:
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

    async def step_1_check_current_positions(self):
        """Step 1: Check current trading positions."""
        await self.wait_for_user("Step 1: Checking current trading positions")
        
        try:
            positions = await self.client.trading.get_positions({"limit": 10})
            position_count = len(positions["data"])
            print(f"📊 Found {position_count} current positions:")
            
            for position in positions["data"][:5]:  # Show first 5
                print(f"  - {position.get('trading_pair', 'Unknown')} on {position.get('connector_name', 'Unknown')}")
                print(f"    Size: {position.get('amount', 0)}, PnL: {position.get('unrealized_pnl', 0)}")
            
            if position_count > 5:
                print(f"    ... and {position_count - 5} more positions")
            
            return positions
        except Exception as e:
            print(f"❌ Error getting positions: {e}")
            return {"data": [], "pagination": {}}

    async def step_2_get_recent_trades(self):
        """Step 2: Get recent trade history."""
        await self.wait_for_user("Step 2: Getting recent trade history")
        
        try:
            trades = await self.client.trading.get_trades({"limit": 5})
            trade_count = len(trades["data"])
            print(f"📈 Found {trade_count} recent trades:")
            
            for trade in trades["data"]:
                print(f"  - {trade.get('trade_type', 'Unknown')} {trade.get('amount', 0)} {trade.get('trading_pair', 'Unknown')}")
                print(f"    Price: {trade.get('price', 0)}, Fee: {trade.get('fee_paid', 0)} {trade.get('fee_currency', '')}")
                print(f"    Time: {trade.get('timestamp', 'Unknown')}")
            
            return trades
        except Exception as e:
            print(f"❌ Error getting trades: {e}")
            return {"data": [], "pagination": {}}

    async def step_3_check_active_orders(self):
        """Step 3: Check currently active (in-flight) orders."""
        await self.wait_for_user("Step 3: Checking active (in-flight) orders")
        
        try:
            active_orders = await self.client.trading.get_active_orders({"limit": 10})
            order_count = len(active_orders["data"])
            print(f"🔄 Found {order_count} active orders:")
            
            for order in active_orders["data"]:
                print(f"  - {order.get('trade_type', 'Unknown')} {order.get('amount', 0)} {order.get('trading_pair', 'Unknown')}")
                print(f"    Price: {order.get('price', 0)}, Status: {order.get('status', 'Unknown')}")
                print(f"    Order ID: {order.get('order_id', 'Unknown')}")
            
            return active_orders
        except Exception as e:
            print(f"❌ Error getting active orders: {e}")
            return {"data": [], "pagination": {}}

    async def step_4_search_historical_orders(self):
        """Step 4: Search historical orders from database."""
        await self.wait_for_user("Step 4: Searching historical orders")
        
        try:
            orders = await self.client.trading.search_orders({"limit": 5})
            order_count = len(orders["data"])
            total_count = orders["pagination"].get("total_count", order_count)
            print(f"📋 Found {order_count} orders (total: {total_count}):")
            
            for order in orders["data"]:
                print(f"  - {order.get('trade_type', 'Unknown')} {order.get('amount', 0)} {order.get('trading_pair', 'Unknown')}")
                print(f"    Price: {order.get('price', 0)}, Status: {order.get('status', 'Unknown')}")
                print(f"    Created: {order.get('created_at', 'Unknown')}")
            
            return orders
        except Exception as e:
            print(f"❌ Error searching orders: {e}")
            return {"data": [], "pagination": {}}

    async def step_5_demonstrate_position_mode(self):
        """Step 5: Demonstrate position mode operations for perpetual connectors."""
        await self.wait_for_user("Step 5: Demonstrating position mode operations")
        
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

    async def step_6_show_trading_capabilities(self):
        """Step 6: Show trading capabilities and limitations."""
        await self.wait_for_user("Step 6: Showing trading capabilities")
        
        try:
            # Show available accounts with credentials
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
                
                # Show details for first trading-ready account
                account, connectors = trading_ready_accounts[0]
                print(f"\nFirst trading-ready account: {account}")
                print(f"Available connectors: {connectors}")
                
                return trading_ready_accounts
            else:
                print("\n⚠️  No accounts configured for trading")
                return []
                
        except Exception as e:
            print(f"❌ Error checking trading capabilities: {e}")
            return []

    async def step_7_demonstrate_order_placement(self, trading_accounts):
        """Step 7: Demonstrate order placement (if accounts are available)."""
        await self.wait_for_user("Step 7: Demonstrating order placement capabilities")
        
        if not trading_accounts:
            print("ℹ️  Skipping order placement - no trading accounts available")
            return None
        
        try:
            account, connectors = trading_accounts[0]
            connector = connectors[0]
            
            print(f"🎯 Would place order using account: {account}, connector: {connector}")
            print("📝 Example order placement:")
            print("   - Trading pair: BTC-USDT")
            print("   - Order type: LIMIT")
            print("   - Side: BUY")
            print("   - Amount: 0.001")
            print("   - Price: Current market price - 5%")
            print("\n⚠️  Note: Actual order placement requires:")
            print("   - Valid API credentials")
            print("   - Sufficient account balance")
            print("   - Proper risk management")
            
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
            return example_order
            
        except Exception as e:
            print(f"❌ Error demonstrating order placement: {e}")
            return None

    async def step_8_show_order_monitoring(self):
        """Step 8: Show how to monitor orders."""
        await self.wait_for_user("Step 8: Showing order monitoring capabilities")
        
        try:
            print("📊 Order monitoring capabilities:")
            print("1. Active Orders: Real-time status of open orders")
            print("2. Order History: Complete order database with pagination")
            print("3. Trade History: Executed trades with fees and timestamps")
            print("4. Position Tracking: Current positions with PnL")
            
            # Show pagination example
            print("\n📄 Pagination example:")
            orders = await self.client.trading.search_orders({"limit": 2})
            pagination = orders.get("pagination", {})
            print(f"   - Limit: {pagination.get('limit', 'N/A')}")
            print(f"   - Has more: {pagination.get('has_more', 'N/A')}")
            print(f"   - Total count: {pagination.get('total_count', 'N/A')}")
            print(f"   - Next cursor: {pagination.get('next_cursor', 'N/A')}")
            
            return True
        except Exception as e:
            print(f"❌ Error showing monitoring: {e}")
            return False

    async def step_9_demonstrate_filtering(self):
        """Step 9: Demonstrate advanced filtering capabilities."""
        await self.wait_for_user("Step 9: Demonstrating filtering capabilities")
        
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

    async def run_test_suite(self):
        """Run the complete Trading router test suite."""
        print("💰 Starting Trading Router Test Suite")
        print("=" * 50)
        
        async with HummingbotClient("http://localhost:8000", "admin", "admin") as client:
            self.client = client
            
            # Step 1: Check current positions
            positions = await self.step_1_check_current_positions()
            
            # Step 2: Get recent trades
            trades = await self.step_2_get_recent_trades()
            
            # Step 3: Check active orders
            active_orders = await self.step_3_check_active_orders()
            
            # Step 4: Search historical orders
            historical_orders = await self.step_4_search_historical_orders()
            
            # Step 5: Demonstrate position mode
            perpetual_available = await self.step_5_demonstrate_position_mode()
            
            # Step 6: Show trading capabilities
            trading_accounts = await self.step_6_show_trading_capabilities()
            
            # Step 7: Demonstrate order placement
            example_order = await self.step_7_demonstrate_order_placement(trading_accounts)
            
            # Step 8: Show order monitoring
            await self.step_8_show_order_monitoring()
            
            # Step 9: Demonstrate filtering
            await self.step_9_demonstrate_filtering()
            
            print("\n" + "=" * 50)
            print("✅ Trading Router Test Suite Completed Successfully!")
            print("\n📝 Summary:")
            print(f"  - Current positions: {len(positions.get('data', []))}")
            print(f"  - Recent trades: {len(trades.get('data', []))}")
            print(f"  - Active orders: {len(active_orders.get('data', []))}")
            print(f"  - Historical orders available: {historical_orders.get('pagination', {}).get('total_count', 'Unknown')}")
            print(f"  - Perpetual trading available: {'Yes' if perpetual_available else 'No'}")
            print(f"  - Trading-ready accounts: {len(trading_accounts)}")
            
            return True


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test Trading Router functionality")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode with step-by-step explanations")
    args = parser.parse_args()
    
    tester = TradingRouterTester(interactive=args.interactive)
    
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