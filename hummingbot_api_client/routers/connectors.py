from typing import Optional, Dict, Any, List
from .base import BaseRouter


class ConnectorsRouter(BaseRouter):
    """Connectors router for connector information and trading rules."""
    
    async def list_connectors(self) -> List[str]:
        """Get a list of all available connectors."""
        return await self._get("/connectors/")
    
    async def get_config_map(self, connector_name: str) -> List[str]:
        """Get configuration fields required for a specific connector."""
        return await self._get(f"/connectors/{connector_name}/config-map")
    
    async def get_trading_rules(
        self, 
        connector_name: str, 
        trading_pairs: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get trading rules for a connector, optionally filtered by trading pairs."""
        params = {"trading_pairs": trading_pairs} if trading_pairs else None
        return await self._get(f"/connectors/{connector_name}/trading-rules", params=params)
    
    async def get_supported_order_types(self, connector_name: str) -> Dict[str, Any]:
        """Get order types supported by a specific connector."""
        return await self._get(f"/connectors/{connector_name}/order-types")