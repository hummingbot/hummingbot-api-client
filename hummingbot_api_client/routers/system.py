from typing import Any, Dict

from .base import BaseRouter


class SystemRouter(BaseRouter):
    """System router for information about the API server itself."""

    async def get_system_info(self) -> Dict[str, Any]:
        """
        Get the versions this API server runs and how its own container was deployed.

        Read-only. When docker.sock is not mounted or the API cannot identify its own
        container, docker_available is False and container is None, but both versions
        are still reported.

        Returns:
            api_version, hummingbot_version, docker_available, container
            ({id, name, image, image_id, digest, compose_project, compose_working_dir,
            compose_config_files} or None), and pinned / pinned_reason / override_file
            saying whether the image is the published one (pinned is None when the
            container could not be read)
        """
        return await self._get("/system/info")
