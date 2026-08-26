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
        return await self._get("/docker/available-images/", params={"image_name": image_name})
    
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
    #
    # There is no per-container status route. Read a container's state from
    # get_active_containers() / get_exited_containers(), both of which take a
    # name_filter.
    async def start_container(self, container_name: str) -> Dict[str, Any]:
        """Start a stopped container."""
        return await self._post(f"/docker/start-container/{container_name}")

    async def stop_container(self, container_name: str) -> Dict[str, Any]:
        """Stop a running container."""
        return await self._post(f"/docker/stop-container/{container_name}")

    async def remove_container(
        self,
        container_name: str,
        archive_locally: bool = True,
        s3_bucket: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Remove a Hummingbot container, archiving its bot data first.

        The route only accepts containers named `hummingbot-*`: removal is bound up
        with archiving the instance's data, which only those have.
        """
        params: Dict[str, Any] = {"archive_locally": archive_locally}
        if s3_bucket:
            params["s3_bucket"] = s3_bucket
        return await self._post(f"/docker/remove-container/{container_name}", params=params)

    # Image Management
    async def pull_image(self, image_name: str, tag: str = "latest") -> Dict[str, Any]:
        """Pull a Docker image from registry."""
        # The route takes one `image_name` carrying the tag, not a name/tag pair.
        return await self._post("/docker/pull-image/", json={"image_name": f"{image_name}:{tag}"})
    
    async def get_pull_status(self) -> Dict[str, Any]:
        """Get the status of image pull operations."""
        return await self._get("/docker/pull-status/")
