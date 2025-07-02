from typing import Optional, Dict, Any, List, Union
from .base import BaseRouter


class TradingRouter(BaseRouter):
    """Trading router for order management and trade execution."""
    
    # Order Operations
    async def place_order(
        self,
        account_name: str,
        connector_name: str,
        trading_pair: str,
        side: str,
        amount: float,
        order_type: str = "MARKET",
        price: Optional[float] = None,
        position_action: str = "OPEN"
    ) -> Dict[str, Any]:
        """
        Place a buy or sell order.
        
        Args:
            account_name: Account to trade with (e.g., "master_account")
            connector_name: Exchange connector (e.g., "binance", "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            side: "BUY" or "SELL"
            amount: Amount to trade (in base currency)
            order_type: "MARKET", "LIMIT", or "LIMIT_MAKER" (default: "MARKET")
            price: Price for limit orders (required for LIMIT orders)
            position_action: "OPEN" or "CLOSE" for perpetual contracts (default: "OPEN")
            
        Returns:
            Order response with order ID and status
            
        Example:
            # Market buy order
            order = await client.trading.place_order(
                "master_account", "binance_perpetual", "BTC-USDT", "BUY", 0.001
            )
            
            # Limit sell order
            order = await client.trading.place_order(
                "master_account", "binance", "ETH-USDT", "SELL", 0.1, 
                order_type="LIMIT", price=2500.0
            )
        """
        trade_request = {
            "account_name": account_name,
            "connector_name": connector_name,
            "trading_pair": trading_pair,
            "trade_type": side,
            "amount": amount,
            "order_type": order_type,
            "position_action": position_action
        }
        if price is not None:
            trade_request["price"] = price
            
        return await self._post("/trading/orders", json=trade_request)
    
    async def cancel_order(
        self,
        account_name: str,
        connector_name: str,
        client_order_id: str,
    ) -> Dict[str, Any]:
        """
        Cancel a specific order.
        
        Args:
            account_name: Account name
            connector_name: Connector name
            client_order_id: Order ID to cancel
            trading_pair: Trading pair for the order
            
        Returns:
            Cancellation confirmation
            
        Example:
            result = await client.trading.cancel_order(
                "master_account", "binance", "order_123", "BTC-USDT"
            )
        """
        return await self._post(
            f"/trading/{account_name}/{connector_name}/orders/{client_order_id}/cancel",
        )
    
    # Data Retrieval with Clean Parameters
    async def get_positions(
        self,
        account_names: Optional[List[str]] = None,
        connector_names: Optional[List[str]] = None,
        limit: int = 50,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get current trading positions.
        
        Args:
            account_names: List of accounts to filter by (default: all accounts)
            connector_names: List of connectors to filter by (default: all connectors)
            limit: Maximum number of positions to return (default: 50)
            cursor: Pagination cursor for next page
            
        Returns:
            Paginated positions data
            
        Example:
            # Get all positions
            positions = await client.trading.get_positions()
            
            # Get positions for specific account and connector
            positions = await client.trading.get_positions(
                account_names=["master_account"],
                connector_names=["binance_perpetual"]
            )
        """
        filter_request = {"limit": limit}
        if account_names is not None:
            filter_request["account_names"] = account_names
        if connector_names is not None:
            filter_request["connector_names"] = connector_names
        if cursor is not None:
            filter_request["cursor"] = cursor
            
        return await self._post("/trading/positions", json=filter_request)
    
    async def get_active_orders(
        self,
        account_names: Optional[List[str]] = None,
        connector_names: Optional[List[str]] = None,
        trading_pairs: Optional[List[str]] = None,
        limit: int = 50,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get active (pending/partially filled) orders.
        
        Args:
            account_names: List of accounts to filter by (default: all accounts)
            connector_names: List of connectors to filter by (default: all connectors)
            trading_pairs: List of trading pairs to filter by (default: all pairs)
            limit: Maximum number of orders to return (default: 50)
            cursor: Pagination cursor for next page
            
        Returns:
            Paginated active orders data
            
        Example:
            # Get all active orders
            orders = await client.trading.get_active_orders()
            
            # Get active BTC orders for specific account
            orders = await client.trading.get_active_orders(
                account_names=["master_account"],
                trading_pairs=["BTC-USDT"]
            )
        """
        filter_request = {"limit": limit}
        if account_names is not None:
            filter_request["account_names"] = account_names
        if connector_names is not None:
            filter_request["connector_names"] = connector_names
        if trading_pairs is not None:
            filter_request["trading_pairs"] = trading_pairs
        if cursor is not None:
            filter_request["cursor"] = cursor
            
        return await self._post("/trading/orders/active", json=filter_request)
    
    async def search_orders(
        self,
        account_names: Optional[List[str]] = None,
        connector_names: Optional[List[str]] = None,
        trading_pairs: Optional[List[str]] = None,
        status: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 50,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search historical orders with filters.
        
        Args:
            account_names: List of accounts to filter by (default: all accounts)
            connector_names: List of connectors to filter by (default: all connectors)
            trading_pairs: List of trading pairs to filter by (default: all pairs)
            status: Order status filter (e.g., "FILLED", "CANCELLED")
            start_time: Start timestamp (Unix timestamp in seconds)
            end_time: End timestamp (Unix timestamp in seconds)
            limit: Maximum number of orders to return (default: 50)
            cursor: Pagination cursor for next page
            
        Returns:
            Paginated historical orders data
            
        Example:
            # Get all filled orders for last 24 hours
            import time
            yesterday = int(time.time()) - 86400
            orders = await client.trading.search_orders(
                status="FILLED",
                start_time=yesterday
            )
            
            # Get BTC orders for specific account
            orders = await client.trading.search_orders(
                account_names=["master_account"],
                trading_pairs=["BTC-USDT"]
            )
        """
        filter_request = {"limit": limit}
        if account_names is not None:
            filter_request["account_names"] = account_names
        if connector_names is not None:
            filter_request["connector_names"] = connector_names
        if trading_pairs is not None:
            filter_request["trading_pairs"] = trading_pairs
        if status is not None:
            filter_request["status"] = status
        if start_time is not None:
            filter_request["start_time"] = start_time
        if end_time is not None:
            filter_request["end_time"] = end_time
        if cursor is not None:
            filter_request["cursor"] = cursor
            
        return await self._post("/trading/orders/search", json=filter_request)
    
    async def get_trades(
        self,
        account_names: Optional[List[str]] = None,
        connector_names: Optional[List[str]] = None,
        trading_pairs: Optional[List[str]] = None,
        trade_types: Optional[List[str]] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 50,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get trade execution history.
        
        Args:
            account_names: List of accounts to filter by (default: all accounts)
            connector_names: List of connectors to filter by (default: all connectors)
            trading_pairs: List of trading pairs to filter by (default: all pairs)
            trade_types: List of trade types to filter by ("BUY", "SELL")
            start_time: Start timestamp (Unix timestamp in seconds)
            end_time: End timestamp (Unix timestamp in seconds)
            limit: Maximum number of trades to return (default: 50)
            cursor: Pagination cursor for next page
            
        Returns:
            Paginated trade execution data
            
        Example:
            # Get all recent trades
            trades = await client.trading.get_trades()
            
            # Get BTC buy trades for last week
            import time
            week_ago = int(time.time()) - (7 * 24 * 60 * 60)
            trades = await client.trading.get_trades(
                trading_pairs=["BTC-USDT"],
                trade_types=["BUY"],
                start_time=week_ago
            )
        """
        filter_request = {"limit": limit}
        if account_names is not None:
            filter_request["account_names"] = account_names
        if connector_names is not None:
            filter_request["connector_names"] = connector_names
        if trading_pairs is not None:
            filter_request["trading_pairs"] = trading_pairs
        if trade_types is not None:
            filter_request["trade_types"] = trade_types
        if start_time is not None:
            filter_request["start_time"] = start_time
        if end_time is not None:
            filter_request["end_time"] = end_time
        if cursor is not None:
            filter_request["cursor"] = cursor
            
        return await self._post("/trading/trades", json=filter_request)
    
    async def get_funding_payments(
        self,
        account_names: Optional[List[str]] = None,
        connector_names: Optional[List[str]] = None,
        trading_pair: Optional[str] = None,
        limit: int = 50,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get funding payment history for perpetual contracts.
        
        Args:
            account_names: List of accounts to filter by (default: all accounts)
            connector_names: List of perpetual connectors to filter by (default: all perpetual connectors)
            trading_pair: Trading pair to filter by (default: all pairs)
            limit: Maximum number of payments to return (default: 50)
            cursor: Pagination cursor for next page
            
        Returns:
            Paginated funding payments data
            
        Example:
            # Get all funding payments
            payments = await client.trading.get_funding_payments()
            
            # Get BTC funding payments for specific account
            payments = await client.trading.get_funding_payments(
                account_names=["master_account"],
                trading_pair="BTC-USDT"
            )
        """
        filter_request = {"limit": limit}
        if account_names is not None:
            filter_request["account_names"] = account_names
        if connector_names is not None:
            filter_request["connector_names"] = connector_names
        if trading_pair is not None:
            filter_request["trading_pair"] = trading_pair
        if cursor is not None:
            filter_request["cursor"] = cursor
            
        return await self._post("/trading/funding-payments", json=filter_request)
    
    # Convenience methods for common operations
    async def get_recent_trades(
        self,
        trading_pair: str,
        account_name: Optional[str] = None,
        connector_name: Optional[str] = None,
        hours: int = 24
    ) -> Dict[str, Any]:
        """
        Get recent trades for a specific trading pair.
        
        Args:
            trading_pair: Trading pair to get trades for (e.g., "BTC-USDT")
            account_name: Specific account name (optional)
            connector_name: Specific connector name (optional)
            hours: Number of hours to look back (default: 24)
            
        Returns:
            Recent trades data
            
        Example:
            # Get BTC trades from last 24 hours
            trades = await client.trading.get_recent_trades("BTC-USDT")
            
            # Get ETH trades from last 4 hours on specific exchange
            trades = await client.trading.get_recent_trades(
                "ETH-USDT", connector_name="binance", hours=4
            )
        """
        import time
        
        start_time = int(time.time()) - (hours * 60 * 60)
        
        account_names = [account_name] if account_name else None
        connector_names = [connector_name] if connector_name else None
        
        return await self.get_trades(
            account_names=account_names,
            connector_names=connector_names,
            trading_pairs=[trading_pair],
            start_time=start_time
        )
    
    async def get_open_positions(
        self,
        account_name: Optional[str] = None,
        connector_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get all open positions (shortcut for positions with non-zero amounts).
        
        Args:
            account_name: Specific account name (optional)
            connector_name: Specific connector name (optional)
            
        Returns:
            Open positions data
            
        Example:
            # Get all open positions
            positions = await client.trading.get_open_positions()
            
            # Get open positions for specific account
            positions = await client.trading.get_open_positions("master_account")
        """
        account_names = [account_name] if account_name else None
        connector_names = [connector_name] if connector_name else None
        
        return await self.get_positions(
            account_names=account_names,
            connector_names=connector_names
        )
    
    # Perpetual Trading Features
    async def get_position_mode(
        self,
        account_name: str,
        connector_name: str
    ) -> Dict[str, Any]:
        """
        Get position mode for a perpetual connector.
        
        Args:
            account_name: Account name
            connector_name: Perpetual connector name (e.g., "binance_perpetual")
            
        Returns:
            Current position mode information
            
        Example:
            mode = await client.trading.get_position_mode("master_account", "binance_perpetual")
        """
        return await self._get(f"/trading/{account_name}/{connector_name}/position-mode")
    
    async def set_position_mode(
        self,
        account_name: str,
        connector_name: str,
        position_mode: str
    ) -> Dict[str, Any]:
        """
        Set position mode for a perpetual connector.
        
        Args:
            account_name: Account name
            connector_name: Perpetual connector name (e.g., "binance_perpetual")
            position_mode: "HEDGE" or "ONEWAY"
            
        Returns:
            Operation result
            
        Example:
            result = await client.trading.set_position_mode(
                "master_account", "binance_perpetual", "HEDGE"
            )
        """
        return await self._post(
            f"/trading/{account_name}/{connector_name}/position-mode",
            json={"position_mode": position_mode}
        )
    
    async def set_leverage(
        self,
        account_name: str,
        connector_name: str,
        trading_pair: str,
        leverage: int
    ) -> Dict[str, Any]:
        """
        Set leverage for a trading pair on a perpetual connector.
        
        Args:
            account_name: Account name
            connector_name: Perpetual connector name (e.g., "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            leverage: Leverage value (e.g., 10 for 10x leverage)
            
        Returns:
            Operation result
            
        Example:
            result = await client.trading.set_leverage(
                "master_account", "binance_perpetual", "BTC-USDT", 10
            )
        """
        return await self._post(
            f"/trading/{account_name}/{connector_name}/leverage",
            json={"trading_pair": trading_pair, "leverage": leverage}
        )