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
    
    async def get_orders(
        self,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all orders with filters."""
        params = {}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if page:
            params["page"] = page
        if page_size:
            params["page_size"] = page_size
        return await self._get("/trading/orders", params=params or None)
    
    async def get_active_orders(self) -> List[Dict[str, Any]]:
        """Get all active orders."""
        return await self._get("/trading/orders/active")
    
    async def get_orders_summary(self) -> Dict[str, Any]:
        """Get order statistics."""
        return await self._get("/trading/orders/summary")
    
    async def cancel_order(
        self,
        account_name: str,
        connector_name: str,
        client_order_id: str
    ) -> Dict[str, Any]:
        """Cancel specific order."""
        return await self._post(
            f"/trading/{account_name}/{connector_name}/orders/{client_order_id}/cancel"
        )
    
    # Account-Specific Trading
    async def get_account_orders(
        self,
        account_name: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get account orders."""
        params = {}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if page:
            params["page"] = page
        if page_size:
            params["page_size"] = page_size
        return await self._get(f"/trading/{account_name}/orders", params=params or None)
    
    async def get_account_active_orders(self, account_name: str) -> List[Dict[str, Any]]:
        """Get account active orders."""
        return await self._get(f"/trading/{account_name}/orders/active")
    
    async def get_account_orders_summary(self, account_name: str) -> Dict[str, Any]:
        """Get account order summary."""
        return await self._get(f"/trading/{account_name}/orders/summary")
    
    async def get_account_trades(
        self,
        account_name: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get account trades."""
        params = {}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if page:
            params["page"] = page
        if page_size:
            params["page_size"] = page_size
        return await self._get(f"/trading/{account_name}/trades", params=params or None)
    
    async def get_connector_active_orders(
        self,
        account_name: str,
        connector_name: str
    ) -> List[Dict[str, Any]]:
        """Get connector active orders."""
        return await self._get(f"/trading/{account_name}/{connector_name}/orders/active")
    
    # Perpetual Trading Features
    async def get_position_mode(
        self,
        account_name: str,
        connector_name: str
    ) -> Dict[str, Any]:
        """Get position mode."""
        return await self._get(f"/trading/{account_name}/{connector_name}/position-mode")
    
    async def set_position_mode(
        self,
        account_name: str,
        connector_name: str,
        position_mode: str
    ) -> Dict[str, Any]:
        """Set position mode."""
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
        """Set leverage."""
        return await self._post(
            f"/trading/{account_name}/{connector_name}/leverage",
            json={"trading_pair": trading_pair, "leverage": leverage}
        )
    
    async def get_supported_order_types(
        self,
        account_name: str,
        connector_name: str
    ) -> List[str]:
        """Get supported order types."""
        return await self._get(f"/trading/{account_name}/{connector_name}/order-types")
    
    # Trade History
    async def get_all_trades(
        self,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all trades."""
        params = {}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if page:
            params["page"] = page
        if page_size:
            params["page_size"] = page_size
        return await self._get("/trading/trades", params=params or None)