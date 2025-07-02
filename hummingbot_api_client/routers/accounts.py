from typing import Optional, Dict, Any, List
from .base import BaseRouter


class AccountsRouter(BaseRouter):
    """Accounts router for account and credential management operations."""
    
    # Account Operations
    async def list_accounts(self) -> List[str]:
        """List all account names."""
        return await self._get("/accounts/")
    
    async def add_account(self, account_name: str) -> Dict[str, Any]:
        """Create new account."""
        return await self._post("/accounts/add-account", params={"account_name": account_name})
    
    async def delete_account(self, account_name: str) -> Dict[str, Any]:
        """Delete account."""
        return await self._post("/accounts/delete-account", params={"account_name": account_name})
    
    # Credentials Management
    async def list_account_credentials(self, account_name: str) -> List[str]:
        """List connector names that have credentials configured for an account."""
        return await self._get(f"/accounts/{account_name}/credentials")
    
    async def add_credential(
        self,
        account_name: str,
        connector_name: str,
        credentials: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add or update connector credentials for an account."""
        return await self._post(
            f"/accounts/add-credential/{account_name}/{connector_name}",
            json=credentials
        )
    
    async def delete_credential(self, account_name: str, connector_name: str) -> Dict[str, Any]:
        """Delete connector credentials for an account."""
        return await self._post(f"/accounts/delete-credential/{account_name}/{connector_name}")