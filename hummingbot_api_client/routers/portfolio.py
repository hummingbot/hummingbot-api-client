from typing import Optional, Dict, Any, List, Union
from .base import BaseRouter


class PortfolioRouter(BaseRouter):
    """Portfolio router for portfolio state and distribution management."""
    
    async def get_state(
        self,
        account_names: Optional[List[str]] = None,
        connector_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get the current portfolio state across accounts and connectors.
        
        Args:
            account_names: List of accounts to filter by (default: all accounts)
            connector_names: List of connectors to filter by (default: all connectors)
            
        Returns:
            Portfolio state with account balances and token information
            
        Example:
            # Get all portfolio state
            state = await client.portfolio.get_state()
            
            # Get state for specific account
            state = await client.portfolio.get_state(["master_account"])
            
            # Get state for specific account and connector
            state = await client.portfolio.get_state(
                ["master_account"], 
                ["binance", "binance_perpetual"]
            )
        """
        filter_request = {}
        if account_names is not None:
            filter_request["account_names"] = account_names
        if connector_names is not None:
            filter_request["connector_names"] = connector_names
            
        return await self._post("/portfolio/state", json=filter_request)
    
    async def get_history(
        self,
        account_names: Optional[List[str]] = None,
        connector_names: Optional[List[str]] = None,
        limit: int = 100,
        cursor: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get historical portfolio states with filtering and pagination.
        
        Args:
            account_names: List of accounts to filter by (default: all accounts)
            connector_names: List of connectors to filter by (default: all connectors)
            limit: Maximum number of history entries to return (default: 100)
            cursor: Pagination cursor for next page
            start_time: Start timestamp (Unix timestamp in seconds)
            end_time: End timestamp (Unix timestamp in seconds)
            
        Returns:
            Paginated historical portfolio data
            
        Example:
            # Get recent portfolio history
            history = await client.portfolio.get_history()
            
            # Get history for last 7 days
            import time
            week_ago = int(time.time()) - (7 * 24 * 60 * 60)
            history = await client.portfolio.get_history(
                start_time=week_ago,
                limit=50
            )
        """
        filter_request = {"limit": limit}
        if account_names is not None:
            filter_request["account_names"] = account_names
        if connector_names is not None:
            filter_request["connector_names"] = connector_names
        if cursor is not None:
            filter_request["cursor"] = cursor
        if start_time is not None:
            filter_request["start_time"] = start_time
        if end_time is not None:
            filter_request["end_time"] = end_time
            
        return await self._post("/portfolio/history", json=filter_request)
    
    async def get_distribution(
        self,
        account_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get portfolio distribution by tokens with percentages.
        
        Args:
            account_names: List of accounts to analyze (default: all accounts)
            
        Returns:
            Token distribution data with percentages and values
            
        Example:
            # Get distribution across all accounts
            distribution = await client.portfolio.get_distribution()
            
            # Get distribution for specific accounts
            distribution = await client.portfolio.get_distribution(
                ["master_account", "trading_account"]
            )
        """
        filter_request = {}
        if account_names is not None:
            filter_request["account_names"] = account_names
            
        return await self._post("/portfolio/distribution", json=filter_request)
    
    async def get_accounts_distribution(
        self,
        account_names: Optional[List[str]] = None,
        connector_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get portfolio distribution by accounts with percentages.
        
        Args:
            account_names: List of accounts to analyze (default: all accounts)
            connector_names: List of connectors to filter by (default: all connectors)
            
        Returns:
            Account distribution data with percentages and connector breakdown
            
        Example:
            # Get distribution across all accounts
            distribution = await client.portfolio.get_accounts_distribution()
            
            # Get distribution for specific accounts and connectors
            distribution = await client.portfolio.get_accounts_distribution(
                ["master_account"],
                ["binance", "binance_perpetual"]
            )
        """
        filter_request = {}
        if account_names is not None:
            filter_request["account_names"] = account_names
        if connector_names is not None:
            filter_request["connector_names"] = connector_names
            
        return await self._post("/portfolio/accounts-distribution", json=filter_request)
    
    # Convenience methods for common operations
    async def get_total_value(
        self,
        account_name: Optional[str] = None,
        connector_name: Optional[str] = None
    ) -> float:
        """
        Get total portfolio value.
        
        Args:
            account_name: Specific account name (optional)
            connector_name: Specific connector name (optional)
            
        Returns:
            Total portfolio value in USD
            
        Example:
            # Get total portfolio value
            total = await client.portfolio.get_total_value()
            
            # Get value for specific account
            total = await client.portfolio.get_total_value("master_account")
        """
        account_names = [account_name] if account_name else None
        connector_names = [connector_name] if connector_name else None
        
        state = await self.get_state(account_names, connector_names)
        
        total_value = 0.0
        for account_data in state.values():
            for connector_balances in account_data.values():
                for balance in connector_balances:
                    total_value += balance.get("value", 0)
        
        return total_value
    
    async def get_token_holdings(
        self,
        token: str,
        account_name: Optional[str] = None,
        connector_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get holdings for a specific token across the portfolio.
        
        Args:
            token: Token symbol to search for (e.g., "BTC", "ETH")
            account_name: Specific account name (optional)
            connector_name: Specific connector name (optional)
            
        Returns:
            Token holdings data with total amounts and values
            
        Example:
            # Get all BTC holdings
            btc_holdings = await client.portfolio.get_token_holdings("BTC")
            
            # Get USDT holdings for specific account
            usdt_holdings = await client.portfolio.get_token_holdings(
                "USDT", "master_account"
            )
        """
        account_names = [account_name] if account_name else None
        connector_names = [connector_name] if connector_name else None
        
        state = await self.get_state(account_names, connector_names)
        
        holdings = {
            "token": token,
            "total_units": 0.0,
            "total_value": 0.0,
            "average_price": 0.0,
            "locations": []
        }
        
        for account_name, account_data in state.items():
            for connector_name, connector_balances in account_data.items():
                for balance in connector_balances:
                    if balance.get("token", "").upper() == token.upper():
                        units = balance.get("units", 0)
                        value = balance.get("value", 0)
                        price = balance.get("price", 0)
                        
                        holdings["total_units"] += units
                        holdings["total_value"] += value
                        
                        holdings["locations"].append({
                            "account": account_name,
                            "connector": connector_name,
                            "units": units,
                            "value": value,
                            "price": price
                        })
        
        # Calculate average price
        if holdings["total_units"] > 0:
            holdings["average_price"] = holdings["total_value"] / holdings["total_units"]
        
        return holdings
    
    async def get_portfolio_summary(
        self,
        account_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a comprehensive portfolio summary.
        
        Args:
            account_name: Specific account name (optional, default: all accounts)
            
        Returns:
            Portfolio summary with key metrics and top holdings
            
        Example:
            # Get full portfolio summary
            summary = await client.portfolio.get_portfolio_summary()
            
            # Get summary for specific account
            summary = await client.portfolio.get_portfolio_summary("master_account")
        """
        account_names = [account_name] if account_name else None
        
        # Get portfolio state and distribution
        state = await self.get_state(account_names)
        distribution = await self.get_distribution(account_names)
        
        # Calculate summary metrics
        total_value = await self.get_total_value(account_name)
        
        # Count accounts and connectors
        account_count = len(state)
        connector_count = sum(len(account_data) for account_data in state.values())
        
        # Get token count and top tokens
        tokens = distribution.get("tokens", {})
        token_count = len(tokens)
        
        # Sort tokens by value and get top 5
        sorted_tokens = sorted(
            tokens.items(),
            key=lambda x: x[1].get("value", 0),
            reverse=True
        )
        top_tokens = sorted_tokens[:5]
        
        return {
            "total_value": total_value,
            "account_count": account_count,
            "connector_count": connector_count,
            "token_count": token_count,
            "top_tokens": [
                {
                    "token": token,
                    "value": data.get("value", 0),
                    "percentage": data.get("percentage", 0)
                }
                for token, data in top_tokens
            ],
            "accounts": list(state.keys()) if account_name is None else [account_name]
        }