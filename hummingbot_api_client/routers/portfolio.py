from typing import Optional, Dict, Any, List
from .base import BaseRouter


class PortfolioRouter(BaseRouter):
    """Portfolio router for portfolio state and distribution management."""
    
    async def get_state(self, account_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get the current state of all or filtered accounts portfolio."""
        params = {}
        if account_names:
            params["account_names"] = account_names
        return await self._get("/portfolio/state", params=params)
    
    async def get_history(
        self,
        account_names: Optional[List[str]] = None,
        limit: int = 100,
        cursor: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get the historical state of all or filtered accounts portfolio with pagination."""
        params = {"limit": limit}
        if account_names:
            params["account_names"] = account_names
        if cursor:
            params["cursor"] = cursor
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        return await self._get("/portfolio/history", params=params)
    
    async def get_distribution(self, account_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get portfolio distribution by tokens with percentages across all or filtered accounts."""
        params = {}
        if account_names:
            params["account_names"] = account_names
        return await self._get("/portfolio/distribution", params=params)
    
    async def get_accounts_distribution(self, account_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get portfolio distribution by accounts with percentages."""
        params = {}
        if account_names:
            params["account_names"] = account_names
        return await self._get("/portfolio/accounts-distribution", params=params)