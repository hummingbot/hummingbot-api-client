from typing import Optional, Dict, Any, List
from .base import BaseRouter


class DockerRouter(BaseRouter):
    """Docker router for container and image management operations."""
    
    # Core Operations
    async def check_docker_running(self) -> Dict[str, Any]:
        """Check Docker daemon status."""
        return await self._get("/docker/running")
    
    async def get_available_images(self, image_name: str) -> Dict[str, Any]:
        """Get available Docker images matching the specified name."""
        return await self._get(f"/docker/available-images/{image_name}")
    
    async def get_active_containers(self, name_filter: Optional[str] = None) -> Dict[str, Any]:
        """Get all currently active (running) Docker containers."""
        params = {"name_filter": name_filter} if name_filter else None
        return await self._get("/docker/active-containers", params=params)
    
    async def get_all_containers(self) -> Dict[str, Any]:
        """Get all Docker containers (running and stopped)."""
        return await self._get("/docker/all-containers")
    
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
    
    async def get_container_logs(self, container_name: str, tail: int = 100) -> Dict[str, Any]:
        """Get logs from a container."""
        params = {"tail": tail}
        return await self._get(f"/docker/logs/{container_name}", params=params)
    
    # Image Management
    async def pull_image(self, image_name: str, tag: str = "latest") -> Dict[str, Any]:
        """Pull a Docker image from registry."""
        return await self._post("/docker/images/pull", json={"name": image_name, "tag": tag})
    
    # Bot Archiving
    async def list_archived_bots(self) -> Dict[str, Any]:
        """List all archived bot instances."""
        return await self._get("/docker/archived-bots")
    
    async def restore_archived_bot(self, bot_name: str) -> Dict[str, Any]:
        """Restore an archived bot instance."""
        return await self._post(f"/docker/archived-bots/{bot_name}/restore")