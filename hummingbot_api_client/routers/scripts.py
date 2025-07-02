from typing import Optional, Dict, Any, List
from .base import BaseRouter


class ScriptsRouter(BaseRouter):
    """Scripts router for script and script configuration management."""
    
    # Script Operations
    async def list_scripts(self) -> List[str]:
        """List all available scripts."""
        return await self._get("/scripts/")
    
    async def get_script(self, script_name: str) -> Dict[str, str]:
        """Get script content by name."""
        return await self._get(f"/scripts/{script_name}")
    
    async def create_or_update_script(self, script_name: str, script_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update a script."""
        return await self._post(f"/scripts/{script_name}", json=script_data)
    
    async def delete_script(self, script_name: str) -> Dict[str, Any]:
        """Delete a script."""
        return await self._delete(f"/scripts/{script_name}")
    
    async def get_script_config_template(self, script_name: str) -> Dict[str, Any]:
        """Get script configuration template with default values."""
        return await self._get(f"/scripts/{script_name}/config/template")
    
    # Script Configuration Operations
    async def list_script_configs(self) -> List[Dict]:
        """List all script configurations with metadata."""
        return await self._get("/scripts/configs/")
    
    async def get_script_config(self, config_name: str) -> Dict[str, Any]:
        """Get script configuration by config name."""
        return await self._get(f"/scripts/configs/{config_name}")
    
    async def create_or_update_script_config(self, config_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update script configuration."""
        return await self._post(f"/scripts/configs/{config_name}", json=config)
    
    async def delete_script_config(self, config_name: str) -> Dict[str, Any]:
        """Delete script configuration."""
        return await self._delete(f"/scripts/configs/{config_name}")