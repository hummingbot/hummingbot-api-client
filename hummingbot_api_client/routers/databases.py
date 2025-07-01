from typing import Optional, Dict, Any, List
from .base import BaseRouter


class DatabasesRouter(BaseRouter):
    """Databases router for data management and checkpoints."""
    
    # Database Operations
    async def list_databases(self) -> List[str]:
        """List all database files."""
        return await self._get("/databases/")
    
    async def read_databases(
        self,
        read_request: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Read data from multiple databases.
        
        Args:
            read_request: Request with database query parameters
        """
        return await self._post("/databases/read", json=read_request)
    
    async def create_checkpoint(
        self,
        checkpoint_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create data checkpoint.
        
        Args:
            checkpoint_request: Request with checkpoint parameters
        """
        return await self._post("/databases/checkpoint", json=checkpoint_request)
    
    async def list_checkpoints(self) -> List[str]:
        """List checkpoint files."""
        return await self._get("/databases/checkpoints")
    
    async def load_checkpoint(
        self,
        checkpoint_request: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Load checkpoint data.
        
        Args:
            checkpoint_request: Request with checkpoint parameters
        """
        return await self._post("/databases/checkpoints/load", json=checkpoint_request)
    
    # Convenience methods
    async def read_trades(
        self,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        connector_name: Optional[str] = None,
        trading_pair: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Read trade data with filters."""
        request = {
            "table": "trades"
        }
        filters = {}
        if start_time:
            filters["timestamp"] = {">=": start_time}
        if end_time:
            if "timestamp" in filters:
                filters["timestamp"]["<="] = end_time
            else:
                filters["timestamp"] = {"<=": end_time}
        if connector_name:
            filters["connector_name"] = connector_name
        if trading_pair:
            filters["trading_pair"] = trading_pair
        
        if filters:
            request["filters"] = filters
        
        return await self.read_databases(request)
    
    async def read_orders(
        self,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Read order data with filters."""
        request = {
            "table": "orders"
        }
        filters = {}
        if start_time:
            filters["creation_timestamp"] = {">=": start_time}
        if end_time:
            if "creation_timestamp" in filters:
                filters["creation_timestamp"]["<="] = end_time
            else:
                filters["creation_timestamp"] = {"<=": end_time}
        if status:
            filters["status"] = status
        
        if filters:
            request["filters"] = filters
        
        return await self.read_databases(request)