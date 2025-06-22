from typing import Optional, Dict, Any, List
from .base import BaseRouter


class DockerRouter(BaseRouter):
    """Docker router for container and image management operations."""
    
    # Core Operations
    async def check_docker_running(self) -> Dict[str, Any]:
        """Check Docker daemon status."""
        return await self._get("/docker/running")
    
    async def get_active_containers(self) -> List[Dict[str, Any]]:
        """List running containers."""
        return await self._get("/docker/active-containers")
    
    async def get_exited_containers(self) -> List[Dict[str, Any]]:
        """List stopped containers."""
        return await self._get("/docker/exited-containers")
    
    async def clean_exited_containers(self) -> Dict[str, Any]:
        """Clean up stopped containers."""
        return await self._post("/docker/clean-exited-containers")
    
    # Container Management
    async def start_container(self, container_name: str) -> Dict[str, Any]:
        """Start container."""
        return await self._post(f"/docker/start-container/{container_name}")
    
    async def stop_container(self, container_name: str) -> Dict[str, Any]:
        """Stop container."""
        return await self._post(f"/docker/stop-container/{container_name}")
    
    async def remove_container(
        self,
        container_name: str,
        archive_locally: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Remove container with archiving options."""
        json_data = {}
        if archive_locally is not None:
            json_data["archive_locally"] = archive_locally
        return await self._post(
            f"/docker/remove-container/{container_name}",
            json=json_data if json_data else None
        )
    
    # Image Operations
    async def get_available_images(self, image_name: str) -> List[str]:
        """List available images."""
        return await self._get(f"/docker/available-images/{image_name}")
    
    async def pull_image(self, pull_request: Dict[str, Any]) -> Dict[str, Any]:
        """Pull image (background task).
        
        Args:
            pull_request: Request with:
                - image_name: str
                - tag: str (optional)
        """
        return await self._post("/docker/pull-image/", json=pull_request)
    
    async def get_pull_status(self, image_name: str) -> Dict[str, Any]:
        """Check pull status."""
        return await self._get(f"/docker/pull-status/{image_name}")
    
    async def clear_pull_status(self, image_name: str) -> Dict[str, Any]:
        """Clear pull status."""
        return await self._delete(f"/docker/pull-status/{image_name}")
    
    # Convenience methods
    async def pull_hummingbot_image(self, tag: str = "latest") -> Dict[str, Any]:
        """Pull Hummingbot image with specific tag."""
        return await self.pull_image({
            "image_name": "hummingbot/hummingbot",
            "tag": tag
        })