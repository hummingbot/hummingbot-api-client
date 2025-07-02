#!/usr/bin/env python3
"""
Docker Router Interactive Example

This script demonstrates the complete Docker management functionality of the Hummingbot API.
It shows you the actual code before executing each operation to help you learn how to use the client.

Usage:
    python docker_example.py              # Run automatically
    python docker_example.py --interactive # Interactive mode with step-by-step explanations
"""

import asyncio
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hummingbot_api_client.client import HummingbotAPIClient


class DockerRouterDemo:
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

    async def overview_docker_functionalities(self):
        """Present all Docker router functionalities."""
        print("🐳 Docker Router - Available Functionalities")
        print("=" * 70)
        
        functionalities = [
            ("✅ Check Docker Status", "check_docker_running()", "Verify if Docker daemon is running"),
            ("📦 List Images", "get_available_images(image_name)", "Find available Docker images"),
            ("🏃 Active Containers", "get_active_containers()", "List currently running containers"),
            ("💤 Exited Containers", "get_exited_containers()", "List stopped/exited containers"),
            ("🧹 Clean Containers", "clean_exited_containers()", "Remove all exited containers"),
            ("📥 Pull Images", "pull_image(name, tag)", "Download Docker images from registry"),
            ("📊 Pull Status", "get_pull_status()", "Check image pull operation status"),
            ("▶️ Start Container", "start_container(name)", "Start a stopped container"),
            ("⏸️ Stop Container", "stop_container(name)", "Stop a running container"),
            ("🗑️ Remove Container", "remove_container(name, force)", "Delete a container"),
            ("📋 Container Status", "get_container_status(name)", "Get detailed container info"),
            ("📄 Container Logs", "get_container_logs(name, tail)", "View container logs"),
        ]
        
        print("Available Docker Router Methods:")
        print()
        # Calculate the maximum width for proper alignment
        max_icon_width = max(len(icon) for icon, _, _ in functionalities)
        max_method_width = max(len(method) for _, method, _ in functionalities)
        
        for icon, method, description in functionalities:
            print(f"  {icon:<{max_icon_width + 2}} {method:<{max_method_width + 2}} - {description}")
        
        await self.wait_for_user("Ready to explore Docker operations?")

    async def demo_check_docker_status(self):
        """Demonstrate checking Docker daemon status."""
        self.print_code_block(
            "Check Docker Daemon Status",
            """
# Check if Docker daemon is running
status = await client.docker.check_docker_running()
print(f"Docker running: {status.get('is_docker_running')}")
            """,
            "This is essential before performing any Docker operations"
        )
        
        await self.wait_for_user("About to check Docker status")
        
        try:
            status = await self.client.docker.is_running()
            if status.get("is_docker_running"):
                print("✅ Docker daemon is running")
                return True
            else:
                print("❌ Docker daemon is not running")
                return False
        except Exception as e:
            print(f"❌ Error checking Docker status: {e}")
            return False

    async def demo_list_available_images(self):
        """Demonstrate listing available images."""
        self.print_code_block(
            "List Available Images",
            """
# Get all images matching a specific name pattern
images = await client.docker.get_available_images("hummingbot")
print(f"Found {len(images)} images:")
for image in images:
    print(f"  - {image}")
            """,
            "Useful for finding what Hummingbot images are available locally"
        )
        
        await self.wait_for_user("About to list available Hummingbot images")
        
        try:
            images = await self.client.docker.get_available_images("hummingbot")
            print(f"📦 Found {len(images)} Hummingbot-related images:")
            for image in images:
                print(f"  - {image}")
            return images
        except Exception as e:
            print(f"❌ Error listing images: {e}")
            return []

    async def demo_get_active_containers(self):
        """Demonstrate getting active containers."""
        self.print_code_block(
            "Get Active Containers",
            """
# Get all currently running containers
containers = await client.docker.get_active_containers()
print(f"Active containers: {len(containers)}")
for container in containers:
    print(f"  - {container['name']} ({container['id'][:12]}) - {container['status']}")

# You can also filter by name
filtered = await client.docker.get_active_containers(name_filter="hummingbot")
            """,
            "Shows all running containers, useful for monitoring your bots"
        )
        
        await self.wait_for_user("About to get active containers")
        
        try:
            containers = await self.client.docker.get_active_containers()
            print(f"🏃 Found {len(containers)} active containers:")
            for container in containers:
                print(f"  - {container['name']} ({container['id'][:12]}) - {container['status']}")
            return containers
        except Exception as e:
            print(f"❌ Error getting active containers: {e}")
            return []

    async def demo_get_exited_containers(self):
        """Demonstrate getting exited containers."""
        self.print_code_block(
            "Get Exited Containers",
            """
# Get all stopped/exited containers
exited_containers = await client.docker.get_exited_containers()
print(f"Exited containers: {len(exited_containers)}")
for container in exited_containers:
    print(f"  - {container['name']} ({container['id'][:12]}) - {container['status']}")

# You can also filter by name
filtered = await client.docker.get_exited_containers(name_filter="bot")
            """,
            "Helps identify containers that have stopped and may need cleanup"
        )
        
        await self.wait_for_user("About to get exited containers")
        
        try:
            containers = await self.client.docker.get_exited_containers()
            print(f"💤 Found {len(containers)} exited containers:")
            for container in containers:
                print(f"  - {container['name']} ({container['id'][:12]}) - {container['status']}")
            return containers
        except Exception as e:
            print(f"❌ Error getting exited containers: {e}")
            return []

    async def demo_clean_exited_containers(self):
        """Demonstrate cleaning exited containers."""
        self.print_code_block(
            "Clean Exited Containers",
            """
# Remove all exited containers to free up space
result = await client.docker.clean_exited_containers()
print(f"Cleanup result: {result}")

# This is equivalent to: docker container prune -f
            """,
            "Removes all stopped containers to free up disk space"
        )
        
        await self.wait_for_user("About to clean exited containers")
        
        try:
            result = await self.client.docker.clean_exited_containers()
            print(f"🧹 Cleanup result: {result}")
            return True
        except Exception as e:
            print(f"❌ Error cleaning containers: {e}")
            return False

    async def demo_pull_image(self):
        """Demonstrate pulling a Docker image."""
        self.print_code_block(
            "Pull Docker Image",
            """
# Pull a Docker image from Docker Hub
pull_result = await client.docker.pull_image("hummingbot/hummingbot", "latest")
print(f"Pull initiated: {pull_result}")

# Check the status of the pull operation
await asyncio.sleep(2)  # Wait a moment
status = await client.docker.get_pull_status()
print(f"Pull status: {status}")

# This is equivalent to: docker pull hummingbot/hummingbot:latest
            """,
            "Downloads the latest Hummingbot image from Docker Hub"
        )
        
        await self.wait_for_user("About to pull hummingbot/hummingbot:latest image")
        
        try:
            # Attempt to pull the latest hummingbot image
            print("🔄 Initiating pull for hummingbot/hummingbot:latest...")
            pull_result = await self.client.docker.pull_image("hummingbot/hummingbot", "latest")
            print(f"📥 Pull operation initiated: {pull_result}")
            
            # Wait a moment and check status
            await asyncio.sleep(2)
            status = await self.client.docker.get_pull_status()
            print(f"📊 Pull status: {status}")
            
            return True
        except Exception as e:
            print(f"❌ Error with pull operation: {e}")
            print("ℹ️  This might happen if the API endpoint is not fully configured")
            return False

    async def demo_container_management_info(self, containers):
        """Show container management capabilities without executing."""
        self.print_code_block(
            "Container Management Operations",
            """
# Start a stopped container
result = await client.docker.start_container("my-bot-container")
print(f"Start result: {result}")

# Stop a running container
result = await client.docker.stop_container("my-bot-container") 
print(f"Stop result: {result}")

# Remove a container (add force=True to remove running containers)
result = await client.docker.remove_container("my-bot-container", force=False)
print(f"Remove result: {result}")

# Get detailed container status
status = await client.docker.get_container_status("my-bot-container")
print(f"Container status: {status}")

# Get container logs (last 50 lines)
logs = await client.docker.get_container_logs("my-bot-container", tail=50)
print(f"Container logs: {logs}")
            """,
            "Additional container operations available (not executed in this demo for safety)"
        )
        
        print("\n🛡️  SAFETY NOTE: These operations are not executed in this demo because they can")
        print("   affect running containers. Use them carefully in production!")
        
        if containers:
            example_container = containers[0]
            container_name = example_container.get('name', 'unknown')
            print(f"\n📋 Example container available: {container_name}")
            print(f"   Status: {example_container.get('status', 'unknown')}")
            print(f"   ID: {example_container.get('id', 'unknown')[:12]}")
        
        await self.wait_for_user("Container management info shown")

    async def run_interactive_demo(self):
        """Run the complete Docker router interactive demo."""
        print("🐳 Docker Router Interactive Demo")
        print("=" * 70)
        print("This demo will show you the actual code before executing each operation.")
        print("Perfect for learning how to use the Hummingbot Docker API!")
        print("=" * 70)
        
        async with HummingbotAPIClient("http://localhost:8000", "admin", "admin") as client:
            self.client = client
            
            # Overview of functionalities
            await self.overview_docker_functionalities()
            
            # Step 1: Check Docker status
            docker_running = await self.demo_check_docker_status()
            if not docker_running:
                print("❌ Cannot continue Docker demo without Docker running")
                return False
            
            # Step 2: List available images
            images = await self.demo_list_available_images()
            
            # Step 3: Get active containers
            active_containers = await self.demo_get_active_containers()
            
            # Step 4: Get exited containers
            exited_containers = await self.demo_get_exited_containers()
            
            # Step 5: Clean exited containers
            await self.demo_clean_exited_containers()
            
            # Step 6: Pull image
            await self.demo_pull_image()
            
            # Step 7: Show container management (without executing)
            all_containers = active_containers + exited_containers
            await self.demo_container_management_info(all_containers)
            
            print("\n" + "=" * 70)
            print("✅ Docker Router Demo Completed!")
            print("\n📝 Summary:")
            print(f"  - Available images: {len(images)}")
            print(f"  - Active containers: {len(active_containers)}")
            print(f"  - Exited containers: {len(exited_containers)}")
            print("\n🎓 You now know how to use all Docker Router operations!")
            print("💡 Try implementing these in your own scripts using the code examples shown.")
            
            return True


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Docker Router Interactive Demo")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode with step-by-step explanations")
    args = parser.parse_args()
    
    demo = DockerRouterDemo(interactive=args.interactive)
    
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