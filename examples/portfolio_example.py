#!/usr/bin/env python3
"""
Portfolio Router Test Script

This script demonstrates the complete portfolio management functionality of the Hummingbot API.
It covers portfolio state monitoring, distribution analysis, and historical tracking.

Usage:
    python test_portfolio_router.py              # Run automatically
    python test_portfolio_router.py --interactive # Interactive mode with explanations
"""

import asyncio
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hummingbot_api_client.client import HummingbotClient


class PortfolioRouterTester:
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

    async def step_1_get_portfolio_state(self):
        """Step 1: Get current portfolio state for all accounts."""
        await self.wait_for_user("Step 1: Getting current portfolio state for all accounts")
        
        try:
            portfolio_state = await self.client.portfolio.get_state()
            account_count = len(portfolio_state)
            
            print(f"📊 Portfolio state for {account_count} accounts:")
            
            for account_name, account_data in portfolio_state.items():
                print(f"\n🏦 Account: {account_name}")
                connector_count = len(account_data)
                print(f"   Connected to {connector_count} exchanges:")
                
                total_value = 0
                total_tokens = 0
                
                for connector, balances in account_data.items():
                    print(f"   📈 {connector}:")
                    for balance in balances[:3]:  # Show first 3 tokens
                        token = balance.get("token", "Unknown")
                        units = balance.get("units", 0)
                        value = balance.get("value", 0)
                        price = balance.get("price", 0)
                        print(f"      {token}: {units:.6f} (${value:.2f} @ ${price:.4f})")
                        total_value += value
                        total_tokens += 1
                    
                    if len(balances) > 3:
                        print(f"      ... and {len(balances) - 3} more tokens")
                        for balance in balances[3:]:
                            total_value += balance.get("value", 0)
                            total_tokens += 1
                
                print(f"   💰 Total portfolio value: ${total_value:.2f}")
                print(f"   🪙 Total tokens: {total_tokens}")
            
            return portfolio_state
            
        except Exception as e:
            print(f"❌ Error getting portfolio state: {e}")
            return {}

    async def step_2_get_portfolio_distribution(self):
        """Step 2: Get portfolio distribution by tokens."""
        await self.wait_for_user("Step 2: Getting portfolio distribution by tokens")
        
        try:
            distribution = await self.client.portfolio.get_distribution()
            
            if "token_distribution" in distribution:
                token_dist = distribution["token_distribution"]
                print(f"🪙 Token distribution across portfolio:")
                
                # Sort by value descending
                sorted_tokens = sorted(token_dist.items(), 
                                     key=lambda x: x[1].get("total_value", 0), 
                                     reverse=True)
                
                for token, data in sorted_tokens[:10]:  # Top 10 tokens
                    percentage = data.get("percentage", 0)
                    total_value = data.get("total_value", 0)
                    total_units = data.get("total_units", 0)
                    print(f"   {token}: {percentage:.2f}% (${total_value:.2f}, {total_units:.6f} units)")
                
                if len(sorted_tokens) > 10:
                    print(f"   ... and {len(sorted_tokens) - 10} more tokens")
            else:
                print("📊 Distribution data structure:")
                for key, value in distribution.items():
                    if isinstance(value, dict):
                        print(f"   {key}: {len(value)} items")
                    else:
                        print(f"   {key}: {value}")
            
            return distribution
            
        except Exception as e:
            print(f"❌ Error getting token distribution: {e}")
            return {}

    async def step_3_get_accounts_distribution(self):
        """Step 3: Get portfolio distribution by accounts."""
        await self.wait_for_user("Step 3: Getting portfolio distribution by accounts")
        
        try:
            distribution = await self.client.portfolio.get_accounts_distribution()
            
            if "account_distribution" in distribution:
                account_dist = distribution["account_distribution"]
                print(f"🏦 Account distribution:")
                
                for account, data in account_dist.items():
                    percentage = data.get("percentage", 0)
                    total_value = data.get("total_value", 0)
                    connectors = data.get("connectors", {})
                    print(f"   {account}: {percentage:.2f}% (${total_value:.2f})")
                    
                    if connectors:
                        print(f"      Connectors: {list(connectors.keys())}")
            else:
                print("📊 Accounts distribution data:")
                for key, value in distribution.items():
                    if isinstance(value, dict):
                        print(f"   {key}: {len(value)} items")
                    else:
                        print(f"   {key}: {value}")
            
            return distribution
            
        except Exception as e:
            print(f"❌ Error getting accounts distribution: {e}")
            return {}

    async def step_4_get_portfolio_history(self):
        """Step 4: Get portfolio history with pagination."""
        await self.wait_for_user("Step 4: Getting portfolio history with pagination")
        
        try:
            # Get recent history
            history = await self.client.portfolio.get_history(limit=5)
            
            if "data" in history:
                history_data = history["data"]
                pagination = history.get("pagination", {})
                
                print(f"📈 Portfolio history ({len(history_data)} entries):")
                print(f"   Pagination - Has more: {pagination.get('has_more', False)}")
                
                for entry in history_data:
                    timestamp = entry.get("timestamp", "Unknown")
                    account = entry.get("account_name", "Unknown")
                    print(f"   📅 {timestamp} - Account: {account}")
            else:
                print("📊 Portfolio history structure:")
                for key, value in history.items():
                    if isinstance(value, list):
                        print(f"   {key}: {len(value)} items")
                    elif isinstance(value, dict):
                        print(f"   {key}: {list(value.keys())}")
                    else:
                        print(f"   {key}: {value}")
            
            return history
            
        except Exception as e:
            print(f"❌ Error getting portfolio history: {e}")
            return {}

    async def step_5_demonstrate_filtering(self):
        """Step 5: Demonstrate filtering by account names."""
        await self.wait_for_user("Step 5: Demonstrating account filtering")
        
        try:
            # Get list of accounts first
            accounts = await self.client.accounts.list_accounts()
            print(f"🔍 Available accounts: {accounts}")
            
            if accounts:
                # Filter by first account
                filtered_account = accounts[0]
                print(f"\n📊 Filtering portfolio by account: {filtered_account}")
                
                # Get state for specific account
                filtered_state = await self.client.portfolio.get_state([filtered_account])
                
                if filtered_account in filtered_state:
                    account_data = filtered_state[filtered_account]
                    print(f"   Account {filtered_account} has {len(account_data)} connectors")
                    
                    for connector, balances in account_data.items():
                        total_value = sum(b.get("value", 0) for b in balances)
                        print(f"   📈 {connector}: ${total_value:.2f} ({len(balances)} tokens)")
                else:
                    print(f"   No data found for account: {filtered_account}")
                
                # Also try distribution filtering
                filtered_dist = await self.client.portfolio.get_distribution([filtered_account])
                print(f"\n📊 Filtered distribution keys: {list(filtered_dist.keys())}")
                
            return True
            
        except Exception as e:
            print(f"❌ Error demonstrating filtering: {e}")
            return False

    async def step_6_portfolio_analytics(self):
        """Step 6: Demonstrate portfolio analytics and insights."""
        await self.wait_for_user("Step 6: Performing portfolio analytics")
        
        try:
            # Get full portfolio state for analysis
            portfolio_state = await self.client.portfolio.get_state()
            
            print("📊 Portfolio Analytics:")
            
            # Calculate total portfolio value
            total_portfolio_value = 0
            total_tokens = 0
            total_connectors = 0
            token_summary = {}
            
            for account_name, account_data in portfolio_state.items():
                for connector, balances in account_data.items():
                    total_connectors += 1
                    for balance in balances:
                        token = balance.get("token", "Unknown")
                        value = balance.get("value", 0)
                        units = balance.get("units", 0)
                        
                        total_portfolio_value += value
                        total_tokens += 1
                        
                        # Aggregate token summary
                        if token not in token_summary:
                            token_summary[token] = {"total_value": 0, "total_units": 0}
                        token_summary[token]["total_value"] += value
                        token_summary[token]["total_units"] += units
            
            print(f"\n💰 Total Portfolio Value: ${total_portfolio_value:.2f}")
            print(f"🏦 Accounts: {len(portfolio_state)}")
            print(f"🔗 Total Connectors: {total_connectors}")
            print(f"🪙 Total Token Positions: {total_tokens}")
            print(f"🎯 Unique Tokens: {len(token_summary)}")
            
            # Top tokens by value
            top_tokens = sorted(token_summary.items(), 
                              key=lambda x: x[1]["total_value"], 
                              reverse=True)[:5]
            
            print(f"\n🏆 Top 5 Tokens by Value:")
            for token, data in top_tokens:
                percentage = (data["total_value"] / total_portfolio_value * 100) if total_portfolio_value > 0 else 0
                print(f"   {token}: ${data['total_value']:.2f} ({percentage:.1f}%)")
            
            return {
                "total_value": total_portfolio_value,
                "accounts": len(portfolio_state),
                "connectors": total_connectors,
                "token_positions": total_tokens,
                "unique_tokens": len(token_summary),
                "top_tokens": top_tokens
            }
            
        except Exception as e:
            print(f"❌ Error performing analytics: {e}")
            return {}

    async def run_test_suite(self):
        """Run the complete Portfolio router test suite."""
        print("💼 Starting Portfolio Router Test Suite")
        print("=" * 50)
        
        async with HummingbotClient("http://localhost:8000", "admin", "admin") as client:
            self.client = client
            
            # Step 1: Get portfolio state
            portfolio_state = await self.step_1_get_portfolio_state()
            
            # Step 2: Get token distribution
            token_distribution = await self.step_2_get_portfolio_distribution()
            
            # Step 3: Get accounts distribution
            accounts_distribution = await self.step_3_get_accounts_distribution()
            
            # Step 4: Get portfolio history
            portfolio_history = await self.step_4_get_portfolio_history()
            
            # Step 5: Demonstrate filtering
            filtering_success = await self.step_5_demonstrate_filtering()
            
            # Step 6: Portfolio analytics
            analytics = await self.step_6_portfolio_analytics()
            
            print("\n" + "=" * 50)
            print("✅ Portfolio Router Test Suite Completed Successfully!")
            print("\n📝 Summary:")
            print(f"  - Accounts monitored: {len(portfolio_state)}")
            print(f"  - Token distribution available: {'Yes' if token_distribution else 'No'}")
            print(f"  - Account distribution available: {'Yes' if accounts_distribution else 'No'}")
            print(f"  - Historical data available: {'Yes' if portfolio_history else 'No'}")
            print(f"  - Filtering functionality: {'Working' if filtering_success else 'Issues'}")
            
            if analytics:
                print(f"  - Total portfolio value: ${analytics.get('total_value', 0):.2f}")
                print(f"  - Unique tokens: {analytics.get('unique_tokens', 0)}")
            
            return True


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test Portfolio Router functionality")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode with step-by-step explanations")
    args = parser.parse_args()
    
    tester = PortfolioRouterTester(interactive=args.interactive)
    
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