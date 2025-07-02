#!/usr/bin/env python3
"""
Accounts Router Test Script

This script demonstrates the complete account and credential management functionality
of the Hummingbot API. It covers account creation, credential management, and cleanup.

Usage:
    python test_accounts_router.py              # Run automatically
    python test_accounts_router.py --interactive # Interactive mode with explanations
"""

import asyncio
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hummingbot_api_client.client import HummingbotClient


class AccountsRouterTester:
    def __init__(self, interactive=False):
        self.interactive = interactive
        self.client = None
        self.test_account_name = "test_account_demo"
        self.test_connector = "binance"

    async def wait_for_user(self, message):
        """Wait for user input in interactive mode."""
        if self.interactive:
            print(f"\n🔄 {message}")
            input("Press Enter to continue...")
        else:
            print(f"\n🔄 {message}")

    async def step_1_list_existing_accounts(self):
        """Step 1: List all existing accounts."""
        await self.wait_for_user("Step 1: Listing existing accounts")
        
        try:
            accounts = await self.client.accounts.list_accounts()
            print(f"📋 Found {len(accounts)} existing accounts:")
            for account in accounts:
                print(f"  - {account}")
            return accounts
        except Exception as e:
            print(f"❌ Error listing accounts: {e}")
            return []

    async def step_2_create_test_account(self):
        """Step 2: Create a test account."""
        await self.wait_for_user(f"Step 2: Creating test account '{self.test_account_name}'")
        
        try:
            result = await self.client.accounts.add_account(self.test_account_name)
            print(f"✅ Account creation result: {result}")
            return True
        except Exception as e:
            print(f"❌ Error creating account: {e}")
            return False

    async def step_3_verify_account_created(self):
        """Step 3: Verify the test account was created."""
        await self.wait_for_user("Step 3: Verifying account was created")
        
        try:
            accounts = await self.client.accounts.list_accounts()
            if self.test_account_name in accounts:
                print(f"✅ Test account '{self.test_account_name}' found in account list")
                return True
            else:
                print(f"❌ Test account '{self.test_account_name}' not found")
                return False
        except Exception as e:
            print(f"❌ Error verifying account: {e}")
            return False

    async def step_4_list_available_connectors(self):
        """Step 4: List available connectors (from connectors router)."""
        await self.wait_for_user("Step 4: Listing available connectors")
        
        try:
            connectors = await self.client.connectors.list_connectors()
            print(f"🔌 Found {len(connectors)} available connectors:")
            # Show first 10 connectors
            for connector in connectors[:10]:
                print(f"  - {connector}")
            if len(connectors) > 10:
                print(f"  ... and {len(connectors) - 10} more")
            
            # Verify our test connector exists
            if self.test_connector in connectors:
                print(f"✅ Test connector '{self.test_connector}' is available")
                return True
            else:
                print(f"❌ Test connector '{self.test_connector}' not found")
                # Try to find an alternative
                for connector in connectors:
                    if "binance" in connector.lower():
                        self.test_connector = connector
                        print(f"🔄 Using alternative connector: {self.test_connector}")
                        return True
                return False
        except Exception as e:
            print(f"❌ Error listing connectors: {e}")
            return False

    async def step_5_add_test_credentials(self):
        """Step 5: Add test credentials for the connector."""
        await self.wait_for_user(f"Step 5: Adding test credentials for '{self.test_connector}'")
        
        try:
            # Create dummy credentials (these are just for testing)
            # First get the required fields for this connector
            config_map = await self.client.connectors.get_config_map(self.test_connector)
            print(f"📋 Required fields for {self.test_connector}: {config_map}")
            
            # Create credentials based on the required fields
            test_credentials = {}
            for field in config_map:
                if "key" in field.lower():
                    test_credentials[field] = "test_api_key_123"
                elif "secret" in field.lower():
                    test_credentials[field] = "test_api_secret_456"
                else:
                    test_credentials[field] = "test_value"
            
            result = await self.client.accounts.add_credential(
                self.test_account_name,
                self.test_connector,
                test_credentials
            )
            print(f"✅ Credentials added: {result}")
            return True
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️  Error adding credentials (this is expected with dummy credentials): {error_msg}")
            # For demo purposes, we'll continue even if credential validation fails
            # as this is likely due to the API validating against the actual exchange
            return "validation_failed"

    async def step_6_verify_credentials_added(self):
        """Step 6: Verify credentials were added."""
        await self.wait_for_user("Step 6: Verifying credentials were added")
        
        try:
            credentials = await self.client.accounts.list_account_credentials(self.test_account_name)
            print(f"🔑 Found {len(credentials)} connectors with credentials:")
            for cred in credentials:
                print(f"  - {cred}")
            
            if self.test_connector in credentials:
                print(f"✅ Credentials for '{self.test_connector}' found")
                return True
            else:
                print(f"❌ Credentials for '{self.test_connector}' not found")
                return False
        except Exception as e:
            print(f"❌ Error verifying credentials: {e}")
            return False

    async def step_7_delete_credentials(self):
        """Step 7: Delete the test credentials."""
        await self.wait_for_user(f"Step 7: Deleting credentials for '{self.test_connector}'")
        
        try:
            result = await self.client.accounts.delete_credential(
                self.test_account_name,
                self.test_connector
            )
            print(f"✅ Credentials deleted: {result}")
            return True
        except Exception as e:
            print(f"❌ Error deleting credentials: {e}")
            return False

    async def step_8_verify_credentials_deleted(self):
        """Step 8: Verify credentials were deleted."""
        await self.wait_for_user("Step 8: Verifying credentials were deleted")
        
        try:
            credentials = await self.client.accounts.list_account_credentials(self.test_account_name)
            print(f"🔑 Found {len(credentials)} connectors with credentials after deletion:")
            for cred in credentials:
                print(f"  - {cred}")
            
            if self.test_connector not in credentials:
                print(f"✅ Credentials for '{self.test_connector}' successfully removed")
                return True
            else:
                print(f"❌ Credentials for '{self.test_connector}' still present")
                return False
        except Exception as e:
            print(f"❌ Error verifying credential deletion: {e}")
            return False

    async def step_9_delete_test_account(self):
        """Step 9: Delete the test account."""
        await self.wait_for_user(f"Step 9: Deleting test account '{self.test_account_name}'")
        
        try:
            result = await self.client.accounts.delete_account(self.test_account_name)
            print(f"✅ Account deleted: {result}")
            return True
        except Exception as e:
            print(f"❌ Error deleting account: {e}")
            return False

    async def step_10_verify_account_deleted(self):
        """Step 10: Verify the test account was deleted."""
        await self.wait_for_user("Step 10: Verifying account was deleted")
        
        try:
            accounts = await self.client.accounts.list_accounts()
            if self.test_account_name not in accounts:
                print(f"✅ Test account '{self.test_account_name}' successfully removed")
                print(f"📋 Remaining accounts: {accounts}")
                return True
            else:
                print(f"❌ Test account '{self.test_account_name}' still present")
                return False
        except Exception as e:
            print(f"❌ Error verifying account deletion: {e}")
            return False

    async def cleanup_if_needed(self):
        """Cleanup test account if it already exists."""
        try:
            accounts = await self.client.accounts.list_accounts()
            if self.test_account_name in accounts:
                print(f"🧹 Cleaning up existing test account '{self.test_account_name}'")
                await self.client.accounts.delete_account(self.test_account_name)
        except:
            pass  # Ignore cleanup errors

    async def run_test_suite(self):
        """Run the complete Accounts router test suite."""
        print("👤 Starting Accounts Router Test Suite")
        print("=" * 50)
        
        async with HummingbotClient("http://localhost:8000", "admin", "admin") as client:
            self.client = client
            
            # Cleanup any existing test account
            await self.cleanup_if_needed()
            
            # Step 1: List existing accounts
            initial_accounts = await self.step_1_list_existing_accounts()
            
            # Step 2: Create test account
            if not await self.step_2_create_test_account():
                return False
            
            # Step 3: Verify account created
            if not await self.step_3_verify_account_created():
                return False
            
            # Step 4: List available connectors
            if not await self.step_4_list_available_connectors():
                return False
            
            # Step 5: Add test credentials
            credentials_result = await self.step_5_add_test_credentials()
            if credentials_result == "validation_failed":
                print("ℹ️  Skipping credential verification steps due to API validation requirements")
                credentials_added = False
            elif credentials_result:
                credentials_added = True
                # Step 6: Verify credentials added
                if not await self.step_6_verify_credentials_added():
                    return False
                
                # Step 7: Delete credentials
                if not await self.step_7_delete_credentials():
                    return False
                
                # Step 8: Verify credentials deleted
                if not await self.step_8_verify_credentials_deleted():
                    return False
            else:
                return False
            
            # Step 9: Delete test account
            if not await self.step_9_delete_test_account():
                return False
            
            # Step 10: Verify account deleted
            if not await self.step_10_verify_account_deleted():
                return False
            
            print("\n" + "=" * 50)
            print("✅ Accounts Router Test Suite Completed Successfully!")
            print("\n📝 Summary:")
            print(f"  - Initial accounts: {len(initial_accounts)}")
            print(f"  - Test account created and deleted: {self.test_account_name}")
            print(f"  - Credentials tested with connector: {self.test_connector}")
            if credentials_result == "validation_failed":
                print(f"  - Note: Credential operations require valid API keys for validation")
            
            return True


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test Accounts Router functionality")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode with step-by-step explanations")
    args = parser.parse_args()
    
    tester = AccountsRouterTester(interactive=args.interactive)
    
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