from typing import Optional, Dict, Any, List
from .base import BaseRouter


class DockerRouter(BaseRouter):
    """Docker router for container and image management operations."""
    
    # Core Operations
    async def is_running(self) -> bool:
        """Check Docker daemon status."""
        return await self._get("/docker/running")
    
    async def get_available_images(self, image_name: Optional[str]) -> Dict[str, Any]:
        """Get available Docker images matching the specified name."""
        return await self._get(f"/docker/available-images", params={"image_name": image_name})
    
    async def get_active_containers(self, name_filter: Optional[str] = None) -> Dict[str, Any]:
        """Get all currently active (running) Docker containers."""
        params = {"name_filter": name_filter} if name_filter else None
        return await self._get("/docker/active-containers", params=params)
    
    async def get_exited_containers(self, name_filter: Optional[str] = None) -> Dict[str, Any]:
        """Get all stopped/exited Docker containers."""
        params = {"name_filter": name_filter} if name_filter else None
        return await self._get("/docker/exited-containers", params=params)
    
    async def clean_exited_containers(self) -> Dict[str, Any]:
        """Clean up (remove) all exited containers."""
        return await self._post("/docker/clean-exited-containers")
    
    # Container Management
    async def get_container_status(self, container_name: str) -> Dict[str, Any]:
        """Get detailed status information for a specific container."""
        return await self._get(f"/docker/container/{container_name}/status")
    
    async def start_container(self, container_name: str) -> Dict[str, Any]:
        """Start a stopped container."""
        return await self._post(f"/docker/container/{container_name}/start")
    
    async def stop_container(self, container_name: str) -> Dict[str, Any]:
        """Stop a running container."""
        return await self._post(f"/docker/container/{container_name}/stop")
    
    async def remove_container(self, container_name: str, force: bool = False) -> Dict[str, Any]:
        """Remove a container."""
        params = {"force": force} if force else None
        return await self._delete(f"/docker/container/{container_name}", params=params)

    # Image Management
    async def pull_image(self, image_name: str, tag: str = "latest") -> Dict[str, Any]:
        """Pull a Docker image from registry."""
        return await self._post("/docker/pull-image/", json={"name": image_name, "tag": tag})
    
    async def get_pull_status(self) -> Dict[str, Any]:
        """Get the status of image pull operations."""
        return await self._get("/docker/pull-status/")
