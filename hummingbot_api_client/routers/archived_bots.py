from typing import Optional, Dict, Any, List
from .base import BaseRouter


class ArchivedBotsRouter(BaseRouter):
    """Archived Bots router for database and bot history management."""
    
    async def list_databases(self) -> List[str]:
        """List all available database files in the system."""
        return await self._get("/archived-bots/")
    
    async def get_database_status(self, db_path: str) -> Dict[str, Any]:
        """Get status information for a specific database."""
        return await self._get(f"/archived-bots/{db_path}/status")
    
    async def get_database_summary(self, db_path: str) -> Dict[str, Any]:
        """Get a summary of database contents including basic statistics."""
        return await self._get(f"/archived-bots/{db_path}/summary")
    
    async def get_database_performance(self, db_path: str) -> Dict[str, Any]:
        """Get trade-based performance analysis for a bot database."""
        return await self._get(f"/archived-bots/{db_path}/performance")
    
    async def get_database_trades(
        self, 
        db_path: str, 
        limit: int = 100, 
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get trade history from a database."""
        params = {"limit": limit, "offset": offset}
        return await self._get(f"/archived-bots/{db_path}/trades", params=params)
    
    async def get_database_orders(
        self, 
        db_path: str, 
        limit: int = 100, 
        offset: int = 0,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get order history from a database."""
        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        return await self._get(f"/archived-bots/{db_path}/orders", params=params)
    
    async def get_database_executors(self, db_path: str) -> Dict[str, Any]:
        """Get executor data from a database."""
        return await self._get(f"/archived-bots/{db_path}/executors")