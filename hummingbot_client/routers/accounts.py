from typing import Optional, Dict, Any, List
from .base import BaseRouter


class AccountsRouter(BaseRouter):
    # Portfolio Management
    async def get_portfolio_state(self) -> Dict[str, Any]:
        """Get all accounts portfolio state."""
        return await self._get("/accounts/portfolio/state")
    
    async def get_portfolio_history(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get portfolio history with pagination."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if page:
            params["page"] = page
        if page_size:
            params["page_size"] = page_size
        return await self._get("/accounts/portfolio/history", params=params or None)
    
    async def get_portfolio_distribution(self) -> Dict[str, Any]:
        """Get token distribution across accounts."""
        return await self._get("/accounts/portfolio/distribution")
    
    async def get_portfolio_accounts_distribution(self) -> Dict[str, Any]:
        """Get distribution by accounts."""
        return await self._get("/accounts/portfolio/accounts-distribution")
    
    async def get_account_portfolio_state(self, account_name: str) -> Dict[str, Any]:
        """Get specific account portfolio."""
        return await self._get(f"/accounts/portfolio/state/{account_name}")
    
    async def get_account_portfolio_history(
        self,
        account_name: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get account portfolio history."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if page:
            params["page"] = page
        if page_size:
            params["page_size"] = page_size
        return await self._get(f"/accounts/portfolio/history/{account_name}", params=params or None)
    
    async def get_account_portfolio_distribution(self, account_name: str) -> Dict[str, Any]:
        """Get account token distribution."""
        return await self._get(f"/accounts/portfolio/distribution/{account_name}")
    
    # Account Operations
    async def list_accounts(self) -> List[Dict[str, Any]]:
        """List all accounts."""
        return await self._get("/accounts/")
    
    async def add_account(self, account_name: str) -> Dict[str, Any]:
        """Create new account."""
        return await self._post(f"/accounts/add-account?account_name={account_name}")
    
    async def delete_account(self, account_name: str) -> Dict[str, Any]:
        """Delete account."""
        return await self._post(f"/accounts/delete-account?account_name={account_name}")
    
    async def get_connectors(self) -> List[str]:
        """List available connectors."""
        return await self._get("/accounts/connectors")
    
    async def get_connector_config_map(self, connector_name: str) -> Dict[str, Any]:
        """Get connector config requirements."""
        return await self._get(f"/accounts/connector-config-map/{connector_name}")
    
    # Credentials Management
    async def get_account_credentials(self, account_name: str) -> List[str]:
        """List account credentials."""
        return await self._get(f"/accounts/{account_name}/credentials")
    
    async def add_credential(
        self,
        account_name: str,
        connector_name: str,
        credential_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add/update credentials."""
        return await self._post(
            f"/accounts/add-credential/{account_name}/{connector_name}",
            json=credential_data
        )
    
    async def delete_credential(self, account_name: str, connector_name: str) -> Dict[str, Any]:
        """Delete credentials."""
        return await self._post(f"/accounts/delete-credential/{account_name}/{connector_name}")
    
    # Position Management (Perpetual Contracts)
    async def get_positions(
        self,
        account_name: str,
        connector_name: str
    ) -> List[Dict[str, Any]]:
        """Get real-time positions."""
        return await self._get(f"/accounts/{account_name}/{connector_name}/positions")
    
    async def get_account_positions(self, account_name: str) -> List[Dict[str, Any]]:
        """Get all account positions."""
        return await self._get(f"/accounts/{account_name}/positions")
    
    async def get_position_snapshots(
        self,
        account_name: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get position snapshots."""
        params = {}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        return await self._get(f"/accounts/{account_name}/positions/snapshots", params=params or None)
    
    async def get_funding_payments(
        self,
        account_name: str,
        connector_name: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get funding payment history."""
        params = {}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        return await self._get(
            f"/accounts/{account_name}/{connector_name}/funding-payments",
            params=params or None
        )
    
    async def get_funding_fees(
        self,
        account_name: str,
        connector_name: str,
        trading_pair: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get funding fees summary."""
        params = {}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        return await self._get(
            f"/accounts/{account_name}/{connector_name}/funding-fees/{trading_pair}",
            params=params or None
        )
    
    async def get_account_funding_payments(
        self,
        account_name: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all account funding payments."""
        params = {}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        return await self._get(f"/accounts/{account_name}/funding-payments", params=params or None)