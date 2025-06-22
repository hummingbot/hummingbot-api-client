from typing import Optional, Dict, Any, List
from .base import BaseRouter


class MarketsRouter(BaseRouter):
    """Market data router for real-time and historical market data."""
    
    async def get_candles(
        self,
        candle_requests: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Get real-time candles.
        
        Args:
            candle_requests: List of candle request objects with:
                - connector_name: str
                - trading_pair: str
                - interval: str (1s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
                - max_records: int (optional)
        """
        return await self._post("/market-data/candles", json=candle_requests)
    
    async def get_historical_candles(
        self,
        candle_requests: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Get historical candles.
        
        Args:
            candle_requests: List of candle request objects with:
                - connector_name: str
                - trading_pair: str
                - interval: str
                - start_time: int (timestamp)
                - end_time: int (timestamp, optional)
        """
        return await self._post("/market-data/historical-candles", json=candle_requests)
    
    async def get_active_feeds(self) -> List[Dict[str, Any]]:
        """Get active market data feeds."""
        return await self._get("/market-data/active-feeds")
    
    async def get_market_data_settings(self) -> Dict[str, Any]:
        """Get market data settings."""
        return await self._get("/market-data/settings")
    
    async def get_trading_rules(self, connector: str) -> Dict[str, Any]:
        """Get all trading rules for a connector."""
        return await self._get(f"/market-data/trading-rules/{connector}")
    
    async def get_trading_pair_rules(
        self,
        connector: str,
        trading_pair: str
    ) -> Dict[str, Any]:
        """Get trading rules for a specific trading pair."""
        return await self._get(f"/market-data/trading-rules/{connector}/{trading_pair}")
    
    async def get_supported_order_types(self, connector: str) -> List[str]:
        """Get supported order types for a connector."""
        return await self._get(f"/market-data/supported-order-types/{connector}")
    
    # Convenience methods for single candle requests
    async def get_single_candle(
        self,
        connector_name: str,
        trading_pair: str,
        interval: str = "1m",
        max_records: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get candles for a single trading pair."""
        request = {
            "connector_name": connector_name,
            "trading_pair": trading_pair,
            "interval": interval
        }
        if max_records:
            request["max_records"] = max_records
        
        return await self.get_candles([request])
    
    async def get_single_historical_candle(
        self,
        connector_name: str,
        trading_pair: str,
        interval: str,
        start_time: int,
        end_time: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get historical candles for a single trading pair."""
        request = {
            "connector_name": connector_name,
            "trading_pair": trading_pair,
            "interval": interval,
            "start_time": start_time
        }
        if end_time:
            request["end_time"] = end_time
        
        return await self.get_historical_candles([request])