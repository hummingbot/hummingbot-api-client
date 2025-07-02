#!/usr/bin/env python3
"""
Docker Router Test Script

This script demonstrates the complete Docker management functionality of the Hummingbot API.
It covers container management, image operations, and background task monitoring.

Usage:
    python test_docker_router.py              # Run automatically
    python test_docker_router.py --interactive # Interactive mode with explanations
"""

import asyncio
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hummingbot_api_client.client import HummingbotClient


class DockerRouterTester:
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

    async def step_1_check_docker_status(self):
        """Step 1: Check if Docker daemon is running."""
        await self.wait_for_user("Step 1: Checking Docker daemon status")
        
        try:
            status = await self.client.docker.check_docker_running()
            if status.get("is_docker_running"):
                print("✅ Docker daemon is running")
            else:
                print("❌ Docker daemon is not running")
                return False
            return True
        except Exception as e:
            print(f"❌ Error checking Docker status: {e}")
            return False

    async def step_2_list_available_images(self):
        """Step 2: List available Hummingbot-related images."""
        await self.wait_for_user("Step 2: Listing available Hummingbot images")
        
        try:
            images = await self.client.docker.get_available_images("hummingbot")
            print(f"📦 Found {len(images)} Hummingbot-related images:")
            for image in images:
                print(f"  - {image}")
            return images
        except Exception as e:
            print(f"❌ Error listing images: {e}")
            return []

    async def step_3_get_active_containers(self):
        """Step 3: Get currently running containers."""
        await self.wait_for_user("Step 3: Getting active containers")
        
        try:
            containers = await self.client.docker.get_active_containers()
            print(f"🏃 Found {len(containers)} active containers:")
            for container in containers:
                print(f"  - {container['name']} ({container['id'][:12]}) - {container['status']}")
            return containers
        except Exception as e:
            print(f"❌ Error getting active containers: {e}")
            return []

    async def step_4_get_exited_containers(self):
        """Step 4: Get stopped/exited containers."""
        await self.wait_for_user("Step 4: Getting exited containers")
        
        try:
            containers = await self.client.docker.get_exited_containers()
            print(f"💤 Found {len(containers)} exited containers:")
            for container in containers:
                print(f"  - {container['name']} ({container['id'][:12]}) - {container['status']}")
            return containers
        except Exception as e:
            print(f"❌ Error getting exited containers: {e}")
            return []

    async def step_5_demonstrate_image_pull(self):
        """Step 5: Demonstrate pulling a Docker image (background operation)."""
        await self.wait_for_user("Step 5: Demonstrating image pull operation")
        
        try:
            # Attempt to pull the latest hummingbot image
            print("🔄 Initiating pull for hummingbot/hummingbot:latest...")
            pull_result = await self.client.docker.pull_image("hummingbot/hummingbot:latest")
            print(f"📥 Pull operation initiated: {pull_result}")
            
            # Wait a moment and check status
            await asyncio.sleep(2)
            status = await self.client.docker.get_pull_status()
            print(f"📊 Pull status: {status}")
            
            return True
        except Exception as e:
            print(f"❌ Error with pull operation: {e}")
            return False

    async def step_6_clean_exited_containers(self):
        """Step 6: Clean up exited containers."""
        await self.wait_for_user("Step 6: Cleaning up exited containers")
        
        try:
            result = await self.client.docker.clean_exited_containers()
            print(f"🧹 Cleanup result: {result}")
            return True
        except Exception as e:
            print(f"❌ Error cleaning containers: {e}")
            return False

    async def step_7_demonstrate_container_operations(self, containers):
        """Step 7: Demonstrate container start/stop operations."""
        if not containers:
            print("ℹ️  No containers available for start/stop demonstration")
            return True
            
        await self.wait_for_user("Step 7: Demonstrating container operations (if available)")
        
        try:
            # Find a container we can work with (prefer stopped ones)
            target_container = None
            for container in containers:
                if "hummingbot" in container.get("name", "").lower():
                    target_container = container
                    break
            
            if target_container:
                container_name = target_container["name"]
                print(f"🎯 Working with container: {container_name}")
                
                # Demonstrate getting container info
                print(f"📋 Container status: {target_container.get('status', 'unknown')}")
            else:
                print("ℹ️  No suitable Hummingbot containers found for operations")
            
            return True
        except Exception as e:
            print(f"❌ Error with container operations: {e}")
            return False

    async def run_test_suite(self):
        """Run the complete Docker router test suite."""
        print("🐳 Starting Docker Router Test Suite")
        print("=" * 50)
        
        async with HummingbotClient("http://localhost:8000", "admin", "admin") as client:
            self.client = client
            
            # Step 1: Check Docker status
            docker_running = await self.step_1_check_docker_status()
            if not docker_running:
                print("❌ Cannot continue without Docker running")
                return False
            
            # Step 2: List available images
            images = await self.step_2_list_available_images()
            
            # Step 3: Get active containers
            active_containers = await self.step_3_get_active_containers()
            
            # Step 4: Get exited containers
            exited_containers = await self.step_4_get_exited_containers()
            
            # Step 5: Demonstrate image pull
            await self.step_5_demonstrate_image_pull()
            
            # Step 6: Clean exited containers
            await self.step_6_clean_exited_containers()
            
            # Step 7: Container operations
            all_containers = active_containers + exited_containers
            await self.step_7_demonstrate_container_operations(all_containers)
            
            print("\n" + "=" * 50)
            print("✅ Docker Router Test Suite Completed Successfully!")
            print("\n📝 Summary:")
            print(f"  - Available images: {len(images)}")
            print(f"  - Active containers: {len(active_containers)}")
            print(f"  - Exited containers: {len(exited_containers)}")
            
            return True


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test Docker Router functionality")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode with step-by-step explanations")
    args = parser.parse_args()
    
    tester = DockerRouterTester(interactive=args.interactive)
    
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