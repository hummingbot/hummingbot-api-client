from typing import Optional, Dict, Any, List
from .base import BaseRouter


class ScriptsRouter(BaseRouter):
    """Scripts router for custom script management."""
    
    # Script Management
    async def list_scripts(self) -> List[str]:
        """List all scripts."""
        return await self._get("/scripts/")
    
    async def get_script(self, script_name: str) -> str:
        """Get script content."""
        return await self._get(f"/scripts/{script_name}")
    
    async def create_or_update_script(
        self,
        script_name: str,
        script_content: str
    ) -> Dict[str, Any]:
        """Create/update script."""
        return await self._post(
            f"/scripts/{script_name}",
            json={"script_content": script_content}
        )
    
    async def delete_script(self, script_name: str) -> Dict[str, Any]:
        """Delete script."""
        return await self._delete(f"/scripts/{script_name}")
    
    async def get_script_config_template(self, script_name: str) -> Dict[str, Any]:
        """Get script config template."""
        return await self._get(f"/scripts/{script_name}/config/template")
    
    # Configuration Management
    async def list_script_configs(self) -> List[str]:
        """List all script configs."""
        return await self._get("/scripts/configs/")
    
    async def get_script_config(self, config_name: str) -> Dict[str, Any]:
        """Get script config."""
        return await self._get(f"/scripts/configs/{config_name}")
    
    async def create_or_update_script_config(
        self,
        config_name: str,
        config_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create/update script config."""
        return await self._post(f"/scripts/configs/{config_name}", json=config_data)
    
    async def delete_script_config(self, config_name: str) -> Dict[str, Any]:
        """Delete script config."""
        return await self._delete(f"/scripts/configs/{config_name}")
    
    # Convenience methods
    async def upload_script(self, script_name: str, script_content: str) -> Dict[str, Any]:
        """Upload a new script."""
        return await self.create_or_update_script(script_name, script_content)
    
    async def download_script(self, script_name: str) -> str:
        """Download script content."""
        return await self.get_script(script_name)