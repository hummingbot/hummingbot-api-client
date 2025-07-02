from typing import Optional, Dict, Any, List
from .base import BaseRouter


class ControllersRouter(BaseRouter):
    """Controllers router for controller and configuration management."""
    
    # Controller Operations
    async def list_controllers(self) -> Dict[str, List[str]]:
        """List all controllers organized by type."""
        return await self._get("/controllers/")
    
    async def get_controller(self, controller_type: str, controller_name: str) -> Dict[str, str]:
        """Get controller content by type and name."""
        return await self._get(f"/controllers/{controller_type}/{controller_name}")
    
    async def create_or_update_controller(
        self, 
        controller_type: str, 
        controller_name: str, 
        controller_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create or update a controller."""
        return await self._post(f"/controllers/{controller_type}/{controller_name}", json=controller_data)
    
    async def delete_controller(self, controller_type: str, controller_name: str) -> Dict[str, Any]:
        """Delete a controller."""
        return await self._delete(f"/controllers/{controller_type}/{controller_name}")
    
    async def get_controller_config_template(self, controller_type: str, controller_name: str) -> Dict[str, Any]:
        """Get controller configuration template with default values."""
        return await self._get(f"/controllers/{controller_type}/{controller_name}/config/template")
    
    # Controller Configuration Operations
    async def list_controller_configs(self) -> List[Dict]:
        """List all controller configurations with metadata."""
        return await self._get("/controllers/configs/")
    
    async def get_controller_config(self, config_name: str) -> Dict[str, Any]:
        """Get controller configuration by config name."""
        return await self._get(f"/controllers/configs/{config_name}")
    
    async def create_or_update_controller_config(self, config_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update controller configuration."""
        return await self._post(f"/controllers/configs/{config_name}", json=config)
    
    async def delete_controller_config(self, config_name: str) -> Dict[str, Any]:
        """Delete controller configuration."""
        return await self._delete(f"/controllers/configs/{config_name}")
    
    # Bot-specific Controller Config Operations
    async def get_bot_controller_configs(self, bot_name: str) -> List[Dict]:
        """Get all controller configurations for a specific bot."""
        return await self._get(f"/controllers/bots/{bot_name}/configs")
    
    async def update_bot_controller_config(
        self, 
        bot_name: str, 
        controller_name: str, 
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update controller configuration for a specific bot."""
        return await self._post(f"/controllers/bots/{bot_name}/{controller_name}/config", json=config)