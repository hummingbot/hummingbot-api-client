from typing import Optional, Dict, Any, List
from .base import BaseRouter


class ControllersRouter(BaseRouter):
    """Controllers router for strategy controller management."""
    
    # Controller Management
    async def list_controllers(self) -> Dict[str, List[str]]:
        """List all controllers by type."""
        return await self._get("/controllers/")
    
    async def get_controller(
        self,
        controller_type: str,
        controller_name: str
    ) -> str:
        """Get controller content."""
        return await self._get(f"/controllers/{controller_type}/{controller_name}")
    
    async def create_or_update_controller(
        self,
        controller_type: str,
        controller_name: str,
        controller_content: str
    ) -> Dict[str, Any]:
        """Create/update controller."""
        return await self._post(
            f"/controllers/{controller_type}/{controller_name}",
            json={"controller_content": controller_content}
        )
    
    async def delete_controller(
        self,
        controller_type: str,
        controller_name: str
    ) -> Dict[str, Any]:
        """Delete controller."""
        return await self._delete(f"/controllers/{controller_type}/{controller_name}")
    
    async def get_controller_config_template(
        self,
        controller_type: str,
        controller_name: str
    ) -> Dict[str, Any]:
        """Get config template."""
        return await self._get(f"/controllers/{controller_type}/{controller_name}/config/template")
    
    # Configuration Management
    async def list_controller_configs(self) -> List[str]:
        """List all controller configs."""
        return await self._get("/controllers/configs/")
    
    async def get_controller_config(self, config_name: str) -> Dict[str, Any]:
        """Get controller config."""
        return await self._get(f"/controllers/configs/{config_name}")
    
    async def create_or_update_controller_config(
        self,
        config_name: str,
        config_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create/update controller config."""
        return await self._post(f"/controllers/configs/{config_name}", json=config_data)
    
    async def delete_controller_config(self, config_name: str) -> Dict[str, Any]:
        """Delete controller config."""
        return await self._delete(f"/controllers/configs/{config_name}")
    
    # Bot-Specific Operations
    async def get_bot_controller_configs(self, bot_name: str) -> Dict[str, Any]:
        """Get bot controller configs."""
        return await self._get(f"/controllers/bots/{bot_name}/configs")
    
    async def update_bot_controller_config(
        self,
        bot_name: str,
        controller_name: str,
        config_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update bot controller config."""
        return await self._post(
            f"/controllers/bots/{bot_name}/{controller_name}/config",
            json=config_data
        )
    
    # Convenience methods for common controller types
    async def list_directional_trading_controllers(self) -> List[str]:
        """List directional trading controllers."""
        controllers = await self.list_controllers()
        return controllers.get("directional_trading", [])
    
    async def list_market_making_controllers(self) -> List[str]:
        """List market making controllers."""
        controllers = await self.list_controllers()
        return controllers.get("market_making", [])
    
    async def create_directional_trading_controller(
        self,
        controller_name: str,
        controller_content: str
    ) -> Dict[str, Any]:
        """Create directional trading controller."""
        return await self.create_or_update_controller(
            "directional_trading",
            controller_name,
            controller_content
        )
    
    async def create_market_making_controller(
        self,
        controller_name: str,
        controller_content: str
    ) -> Dict[str, Any]:
        """Create market making controller."""
        return await self.create_or_update_controller(
            "market_making",
            controller_name,
            controller_content
        )