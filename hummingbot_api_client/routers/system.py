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
            api_version, hummingbot_version, market_data (the MARKET_DATA_* tunables as
            this API process resolved them -- reported, never writable, since the API
            cannot rewrite its own .env), docker_available, container
            ({id, name, image, image_id, digest, compose_project, compose_working_dir,
            compose_config_files} or None), and pinned / pinned_reason / override_file
            saying whether the image is the published one (pinned is None when the
            container could not be read)
        """
        return await self._get("/system/info")

    async def get_upgrade_preflight(self) -> Dict[str, Any]:
        """
        Ask whether this API server can replace its own container with the published image.

        Read-only and never fails on a daemon problem: an unreachable Docker daemon, a
        container the API cannot place, missing compose labels and a registry that cannot
        be read all come back as can_upgrade False with a blocked_reason, because the
        caller of a destructive action needs the reason more than it needs an error.

        Returns:
            image_ref, current_digest, available_digest, up_to_date, the pinning verdict
            (pinned / pinned_reason / override_file), compose ({project, working_dir,
            config_files} or None), running_executors, running_bots, and can_upgrade with
            its blocked_reason -- None only when the upgrade may actually be started.
        """
        return await self._get("/system/upgrade/preflight")

    async def start_upgrade(self, acknowledge_executor_loss: bool = False) -> Dict[str, Any]:
        """
        Pull the published image and hand the container recreate to a helper container.

        The server re-runs its own preflight, so an upgrade that has become unsafe since
        you last looked is refused rather than started on a stale reading.

        Args:
            acknowledge_executor_loss: Consent to every RUNNING executor being closed as
                SYSTEM_CLEANUP and not restored. Required when the server has any running
                executor; it defaults to False, so an unwitting caller is refused.

        Returns:
            run_id and the initial phase. The API is replaced part-way through the run, so
            read the outcome back from get_upgrade_status() once it answers again.

        Raises:
            aiohttp.ClientResponseError: 409 when the upgrade is refused, with the reason
                as its message. Nothing was pulled and nothing on the server was changed.
        """
        return await self._post(
            "/system/upgrade",
            json={"acknowledge_executor_loss": acknowledge_executor_loss},
        )

    async def get_upgrade_status(self) -> Dict[str, Any]:
        """
        Get the current or last self-upgrade of this API server.

        Phases: idle, pulling, recreating (the API is about to be replaced, so the next
        answer comes from the new container), done, failed. After a recreate the record
        is the one the new API collected from the helper container on boot.

        Returns:
            run_id, phase, detail, previous_digest, new_digest, exit_code and log_tail.
        """
        return await self._get("/system/upgrade/status")
