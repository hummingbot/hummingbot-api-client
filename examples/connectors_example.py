#!/usr/bin/env python3
"""
Connectors Router Test Script

This script demonstrates the complete connector discovery and configuration functionality
of the Hummingbot API. It covers connector listing, configuration requirements, and trading rules.

Usage:
    python test_connectors_router.py              # Run automatically
    python test_connectors_router.py --interactive # Interactive mode with explanations
"""

import asyncio
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hummingbot_api_client.client import HummingbotClient


class ConnectorsRouterTester:
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

    async def step_1_list_all_connectors(self):
        """Step 1: List all available connectors."""
        await self.wait_for_user("Step 1: Listing all available connectors")
        
        try:
            connectors = await self.client.connectors.list_connectors()
            print(f"🔌 Found {len(connectors)} available connectors:")
            
            # Show first 15 connectors as examples
            for connector in connectors[:15]:
                print(f"  - {connector}")
            
            if len(connectors) > 15:
                print(f"  ... and {len(connectors) - 15} more connectors")
            
            return connectors
            
        except Exception as e:
            print(f"❌ Error listing connectors: {e}")
            return []

    async def step_2_categorize_connectors(self, connectors):
        """Step 2: Categorize connectors by type."""
        await self.wait_for_user("Step 2: Categorizing connectors by type")
        
        try:
            categories = {
                "perpetual": [],
                "spot": [],
                "testnet": [],
                "dex": [],
                "other": []
            }
            
            for connector in connectors:
                connector_lower = connector.lower()
                if "perpetual" in connector_lower:
                    categories["perpetual"].append(connector)
                elif "testnet" in connector_lower:
                    categories["testnet"].append(connector)
                elif any(dex in connector_lower for dex in ["dexalot", "dydx", "vertex", "xrpl", "injective"]):
                    categories["dex"].append(connector)
                else:
                    # Check if it's a known CEX
                    cex_names = ["binance", "coinbase", "kraken", "kucoin", "okx", "gate", "bybit", "bitget", "mexc"]
                    if any(cex in connector_lower for cex in cex_names):
                        categories["spot"].append(connector)
                    else:
                        categories["other"].append(connector)
            
            print("📊 Connector categories:")
            for category, conn_list in categories.items():
                print(f"  🏷️  {category.capitalize()}: {len(conn_list)} connectors")
                if conn_list:
                    # Show first 3 examples
                    examples = conn_list[:3]
                    print(f"      Examples: {', '.join(examples)}")
                    if len(conn_list) > 3:
                        print(f"      ... and {len(conn_list) - 3} more")
            
            return categories
            
        except Exception as e:
            print(f"❌ Error categorizing connectors: {e}")
            return {}

    async def step_3_get_configuration_requirements(self, connectors):
        """Step 3: Get configuration requirements for sample connectors."""
        await self.wait_for_user("Step 3: Getting configuration requirements for sample connectors")
        
        try:
            # Test configuration for a few popular connectors
            test_connectors = []
            for connector in connectors:
                if connector.lower() in ["binance", "coinbase_advanced_trade", "kucoin", "binance_perpetual"]:
                    test_connectors.append(connector)
                if len(test_connectors) >= 4:
                    break
            
            print(f"🔧 Configuration requirements for sample connectors:")
            
            config_data = {}
            for connector in test_connectors:
                try:
                    config_fields = await self.client.connectors.get_config_map(connector)
                    config_data[connector] = config_fields
                    print(f"\n  📋 {connector}:")
                    print(f"      Required fields: {len(config_fields)}")
                    for field in config_fields:
                        print(f"        - {field}")
                except Exception as e:
                    print(f"  ❌ {connector}: Error getting config - {e}")
            
            return config_data
            
        except Exception as e:
            print(f"❌ Error getting configuration requirements: {e}")
            return {}

    async def step_4_get_trading_rules(self, connectors):
        """Step 4: Get trading rules for specific connectors."""
        await self.wait_for_user("Step 4: Getting trading rules for specific connectors")
        
        try:
            # Test trading rules for a couple of connectors
            test_connectors = ["binance", "binance_perpetual"]
            trading_rules_data = {}
            
            for connector in test_connectors:
                if connector in connectors:
                    try:
                        print(f"\n🔍 Getting trading rules for {connector}:")
                        
                        # Get all trading rules
                        all_rules = await self.client.connectors.get_trading_rules(connector)
                        
                        if isinstance(all_rules, dict):
                            pair_count = len(all_rules)
                            print(f"  📊 Found trading rules for {pair_count} pairs")
                            
                            # Show rules for a few popular pairs
                            sample_pairs = ["BTC-USDT", "ETH-USDT", "SOL-USDT"]
                            for pair in sample_pairs:
                                if pair in all_rules:
                                    rules = all_rules[pair]
                                    print(f"    📈 {pair}:")
                                    print(f"      Min order size: {rules.get('min_order_size', 'N/A')}")
                                    print(f"      Max order size: {rules.get('max_order_size', 'N/A')}")
                                    print(f"      Order size increment: {rules.get('min_base_amount_increment', 'N/A')}")
                                    print(f"      Min notional: {rules.get('min_notional_size', 'N/A')}")
                                    break
                            
                            # Test with specific trading pairs
                            specific_rules = await self.client.connectors.get_trading_rules(
                                connector, ["BTC-USDT", "ETH-USDT"]
                            )
                            if specific_rules:
                                print(f"  🎯 Filtered rules for specific pairs: {len(specific_rules)} pairs")
                        
                        trading_rules_data[connector] = all_rules
                        
                    except Exception as e:
                        print(f"  ❌ Error getting trading rules for {connector}: {e}")
            
            return trading_rules_data
            
        except Exception as e:
            print(f"❌ Error getting trading rules: {e}")
            return {}

    async def step_5_get_order_types(self, connectors):
        """Step 5: Check supported order types."""
        await self.wait_for_user("Step 5: Checking supported order types")
        
        try:
            # Test order types for several connectors
            test_connectors = ["binance", "binance_perpetual", "coinbase_advanced_trade", "kucoin"]
            order_types_data = {}
            
            print("🔧 Supported order types by connector:")
            
            for connector in test_connectors:
                if connector in connectors:
                    try:
                        order_types = await self.client.connectors.get_order_types(connector)
                        order_types_data[connector] = order_types
                        print(f"  📋 {connector}: {', '.join(order_types)}")
                    except Exception as e:
                        print(f"  ❌ {connector}: Error - {e}")
            
            return order_types_data
            
        except Exception as e:
            print(f"❌ Error getting order types: {e}")
            return {}

    async def step_6_connector_capabilities_analysis(self, connectors, categories, config_data, trading_rules, order_types):
        """Step 6: Analyze connector capabilities."""
        await self.wait_for_user("Step 6: Analyzing connector capabilities")
        
        try:
            print("📊 Connector Capabilities Analysis:")
            
            # Analysis by category
            print(f"\n🏷️  Categories breakdown:")
            for category, conn_list in categories.items():
                if conn_list:
                    print(f"  {category.capitalize()}: {len(conn_list)} connectors")
            
            # Configuration complexity analysis
            print(f"\n🔧 Configuration complexity:")
            if config_data:
                for connector, fields in config_data.items():
                    complexity = "Simple" if len(fields) <= 2 else "Moderate" if len(fields) <= 4 else "Complex"
                    print(f"  {connector}: {len(fields)} fields ({complexity})")
            
            # Order type support analysis
            print(f"\n📋 Order type support:")
            if order_types:
                all_order_types = set()
                for connector, types in order_types.items():
                    all_order_types.update(types)
                    print(f"  {connector}: {len(types)} types supported")
                
                print(f"\n  All supported order types: {', '.join(sorted(all_order_types))}")
            
            # Trading pairs availability
            print(f"\n📈 Trading pairs availability:")
            if trading_rules:
                for connector, rules in trading_rules.items():
                    if isinstance(rules, dict):
                        print(f"  {connector}: {len(rules)} trading pairs available")
            
            return True
            
        except Exception as e:
            print(f"❌ Error in capabilities analysis: {e}")
            return False

    async def step_7_connector_account_relationship(self):
        """Step 7: Show relationship between connectors and accounts."""
        await self.wait_for_user("Step 7: Showing connector-account relationships")
        
        try:
            # Get accounts and their configured connectors
            accounts = await self.client.accounts.list_accounts()
            print(f"🔗 Connector-Account relationships:")
            
            total_configured = 0
            account_connector_map = {}
            
            for account in accounts:
                try:
                    credentials = await self.client.accounts.list_account_credentials(account)
                    account_connector_map[account] = credentials
                    total_configured += len(credentials)
                    
                    if credentials:
                        print(f"  🏦 {account}: {len(credentials)} connectors configured")
                        for connector in credentials[:3]:  # Show first 3
                            print(f"      - {connector}")
                        if len(credentials) > 3:
                            print(f"      ... and {len(credentials) - 3} more")
                    else:
                        print(f"  🏦 {account}: No connectors configured")
                        
                except Exception as e:
                    print(f"  ❌ Error checking {account}: {e}")
            
            print(f"\n📊 Summary:")
            print(f"  - Total accounts: {len(accounts)}")
            print(f"  - Total configured connectors: {total_configured}")
            
            # Show usage pattern
            if account_connector_map:
                configured_accounts = sum(1 for creds in account_connector_map.values() if creds)
                print(f"  - Accounts with connectors: {configured_accounts}/{len(accounts)}")
            
            return account_connector_map
            
        except Exception as e:
            print(f"❌ Error analyzing connector-account relationships: {e}")
            return {}

    async def run_test_suite(self):
        """Run the complete Connectors router test suite."""
        print("🔌 Starting Connectors Router Test Suite")
        print("=" * 50)
        
        async with HummingbotClient("http://localhost:8000", "admin", "admin") as client:
            self.client = client
            
            # Step 1: List all connectors
            connectors = await self.step_1_list_all_connectors()
            if not connectors:
                print("❌ No connectors found, cannot continue")
                return False
            
            # Step 2: Categorize connectors
            categories = await self.step_2_categorize_connectors(connectors)
            
            # Step 3: Get configuration requirements
            config_data = await self.step_3_get_configuration_requirements(connectors)
            
            # Step 4: Get trading rules
            trading_rules = await self.step_4_get_trading_rules(connectors)
            
            # Step 5: Get order types
            order_types = await self.step_5_get_order_types(connectors)
            
            # Step 6: Capabilities analysis
            analysis_success = await self.step_6_connector_capabilities_analysis(
                connectors, categories, config_data, trading_rules, order_types
            )
            
            # Step 7: Connector-account relationships
            account_relationships = await self.step_7_connector_account_relationship()
            
            print("\n" + "=" * 50)
            print("✅ Connectors Router Test Suite Completed Successfully!")
            print("\n📝 Summary:")
            print(f"  - Total connectors available: {len(connectors)}")
            print(f"  - Connector categories identified: {len(categories)}")
            print(f"  - Configuration examples analyzed: {len(config_data)}")
            print(f"  - Trading rules retrieved: {len(trading_rules)}")
            print(f"  - Order types analyzed: {len(order_types)}")
            print(f"  - Account relationships mapped: {'Yes' if account_relationships else 'No'}")
            
            return True


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test Connectors Router functionality")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode with step-by-step explanations")
    args = parser.parse_args()
    
    tester = ConnectorsRouterTester(interactive=args.interactive)
    
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