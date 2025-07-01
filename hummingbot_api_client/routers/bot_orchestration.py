from typing import Optional, Dict, Any, List
from .base import BaseRouter


class BotOrchestrationRouter(BaseRouter):
    """Bot orchestration router for bot lifecycle management and monitoring."""
    
    # Bot Management
    async def get_bots_status(self) -> List[Dict[str, Any]]:
        """Get all active bots status."""
        return await self._get("/bot-orchestration/status")
    
    async def get_bot_status(self, bot_name: str) -> Dict[str, Any]:
        """Get specific bot status."""
        return await self._get(f"/bot-orchestration/{bot_name}/status")
    
    async def get_bot_history(
        self,
        bot_name: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get bot trading history."""
        params = {}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if page:
            params["page"] = page
        if page_size:
            params["page_size"] = page_size
        return await self._get(f"/bot-orchestration/{bot_name}/history", params=params or None)
    
    async def start_bot(self, start_request: Dict[str, Any]) -> Dict[str, Any]:
        """Start bot with config.
        
        Args:
            start_request: Request with:
                - bot_name: str
                - log_level: str (optional) - DEBUG, INFO, WARNING, ERROR
                - script: str (optional)
                - conf: str (optional)
                - async_backend: bool (optional)
        """
        return await self._post("/bot-orchestration/start-bot", json=start_request)
    
    async def stop_bot(self, bot_name: str) -> Dict[str, Any]:
        """Stop bot."""
        return await self._post("/bot-orchestration/stop-bot", json={"bot_name": bot_name})
    
    async def stop_and_archive_bot(self, bot_name: str) -> Dict[str, Any]:
        """Stop and archive bot."""
        return await self._post(f"/bot-orchestration/stop-and-archive-bot/{bot_name}")
    
    # Instance Creation
    async def create_hummingbot_instance(
        self,
        instance_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create new Hummingbot instance.
        
        Args:
            instance_request: Request with instance configuration
        """
        return await self._post(
            "/bot-orchestration/create-hummingbot-instance",
            json=instance_request
        )
    
    async def deploy_v2_controllers(
        self,
        deployment_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deploy V2 strategy with controllers.
        
        Args:
            deployment_request: Request with deployment configuration
        """
        return await self._post(
            "/bot-orchestration/deploy-v2-controllers",
            json=deployment_request
        )
    
    # MQTT Integration
    async def get_mqtt_status(self) -> Dict[str, Any]:
        """Get MQTT connection status."""
        return await self._get("/bot-orchestration/mqtt")
    
    # Convenience methods
    async def start_simple_bot(
        self,
        bot_name: str,
        script: Optional[str] = None,
        conf: Optional[str] = None,
        log_level: str = "INFO"
    ) -> Dict[str, Any]:
        """Start a bot with simple configuration."""
        request = {
            "bot_name": bot_name,
            "log_level": log_level
        }
        if script:
            request["script"] = script
        if conf:
            request["conf"] = conf
        return await self.start_bot(request)