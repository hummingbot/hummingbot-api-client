from typing import Optional, Dict, Any, List
from .base import BaseRouter


class TradingRouter(BaseRouter):
    """Trading router for order management and trade execution."""
    
    # Order Operations
    async def place_order(self, trade_request: Dict[str, Any]) -> Dict[str, Any]:
        """Place buy/sell order.
        
        Args:
            trade_request: Order request with:
                - account_name: str
                - connector_name: str
                - trading_pair: str
                - trade_type: "BUY" | "SELL"
                - amount: float
                - order_type: "MARKET" | "LIMIT" (optional)
                - price: float (optional for limit orders)
                - position_action: "OPEN" | "CLOSE" (optional for perpetuals)
        """
        return await self._post("/trading/orders", json=trade_request)
    
    async def cancel_order(
        self,
        account_name: str,
        connector_name: str,
        client_order_id: str,
        trading_pair: str
    ) -> Dict[str, Any]:
        """Cancel specific order."""
        return await self._post(
            f"/trading/{account_name}/{connector_name}/orders/{client_order_id}/cancel",
            json={"trading_pair": trading_pair}
        )
    
    # Data Retrieval (POST with filter requests)
    async def get_positions(self, filter_request: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get current positions with filtering and pagination.
        
        Args:
            filter_request: Filter with account_names, connector_names, trading_pairs, limit, cursor, etc.
        """
        if filter_request is None:
            filter_request = {}
        return await self._post("/trading/positions", json=filter_request)
    
    async def get_active_orders(self, filter_request: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get active (in-flight) orders with filtering and pagination.
        
        Args:
            filter_request: Filter with account_names, connector_names, trading_pairs, limit, cursor, etc.
        """
        if filter_request is None:
            filter_request = {}
        return await self._post("/trading/orders/active", json=filter_request)
    
    async def search_orders(self, filter_request: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get historical order data with filtering and pagination.
        
        Args:
            filter_request: Filter with account_names, connector_names, trading_pairs, limit, cursor, start_time, end_time, etc.
        """
        if filter_request is None:
            filter_request = {}
        return await self._post("/trading/orders/search", json=filter_request)
    
    async def get_trades(self, filter_request: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get trade history with filtering and pagination.
        
        Args:
            filter_request: Filter with account_names, connector_names, trading_pairs, limit, cursor, start_time, end_time, etc.
        """
        if filter_request is None:
            filter_request = {}
        return await self._post("/trading/trades", json=filter_request)
    
    # Perpetual Trading Features
    async def get_position_mode(
        self,
        account_name: str,
        connector_name: str
    ) -> Dict[str, Any]:
        """Get position mode for a perpetual connector."""
        return await self._get(f"/trading/{account_name}/{connector_name}/position-mode")
    
    async def set_position_mode(
        self,
        account_name: str,
        connector_name: str,
        position_mode: str
    ) -> Dict[str, Any]:
        """Set position mode for a perpetual connector.
        
        Args:
            position_mode: "HEDGE" or "ONEWAY"
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
        """Set leverage for a trading pair on a perpetual connector."""
        return await self._post(
            f"/trading/{account_name}/{connector_name}/leverage",
            json={"trading_pair": trading_pair, "leverage": leverage}
        )