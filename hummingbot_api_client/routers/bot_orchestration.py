from typing import Optional, Dict, Any, List
from .base import BaseRouter


class BotOrchestrationRouter(BaseRouter):
    """Bot Orchestration router for bot lifecycle management and MQTT operations."""
    
    # Bot Status Operations
    async def get_active_bots_status(self) -> Dict[str, Any]:
        """Get the status of all active bots."""
        return await self._get("/bot-orchestration/status")
    
    async def get_mqtt_status(self) -> Dict[str, Any]:
        """Get MQTT connection status and discovered bots."""
        return await self._get("/bot-orchestration/mqtt")
    
    async def get_bot_status(self, bot_name: str) -> Dict[str, Any]:
        """Get the status of a specific bot."""
        return await self._get(f"/bot-orchestration/{bot_name}/status")
    
    async def get_bot_history(
        self,
        bot_name: str,
        days: int = 0,
        verbose: bool = False,
        precision: Optional[int] = None,
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """Get trading history for a bot with optional parameters."""
        params = {
            "days": days,
            "verbose": verbose,
            "timeout": timeout
        }
        if precision is not None:
            params["precision"] = precision
        return await self._get(f"/bot-orchestration/{bot_name}/history", params=params)
    
    # Bot Control Operations
    async def start_bot(self, start_bot_action: Dict[str, Any]) -> Dict[str, Any]:
        """Start a bot with the specified configuration."""
        return await self._post("/bot-orchestration/start-bot", json=start_bot_action)
    
    async def stop_bot(self, stop_bot_action: Dict[str, Any]) -> Dict[str, Any]:
        """Stop a bot with the specified configuration."""
        return await self._post("/bot-orchestration/stop-bot", json=stop_bot_action)
    
    async def stop_and_archive_bot(
        self,
        bot_name: str,
        skip_order_cancellation: bool = True,
        archive_locally: bool = True,
        s3_bucket: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gracefully stop a bot and archive its data in the background."""
        params = {
            "skip_order_cancellation": skip_order_cancellation,
            "archive_locally": archive_locally
        }
        if s3_bucket:
            params["s3_bucket"] = s3_bucket
        return await self._post(f"/bot-orchestration/stop-and-archive-bot/{bot_name}", params=params)
    
    # Bot Deployment Operations
    async def deploy_v2_script(self, script_deployment: Dict[str, Any]) -> Dict[str, Any]:
        """Creates and autostart a v2 script with a configuration if present."""
        return await self._post("/bot-orchestration/deploy-v2-script", json=script_deployment)
    
    async def deploy_v2_controllers(self, controller_deployment: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy a V2 strategy with controllers by generating the script config and creating the instance."""
        return await self._post("/bot-orchestration/deploy-v2-controllers", json=controller_deployment)