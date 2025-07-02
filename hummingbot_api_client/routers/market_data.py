from typing import Optional, Dict, Any, List
from .base import BaseRouter


class MarketDataRouter(BaseRouter):
    """Market Data router for real-time and historical market data."""
    
    # Candles Operations
    async def get_candles(self, candles_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get real-time candles data for a specific trading pair."""
        return await self._post("/market-data/candles", json=candles_config)
    
    async def get_historical_candles(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get historical candles data for a specific trading pair."""
        return await self._post("/market-data/historical-candles", json=config)
    
    async def get_active_feeds(self) -> Dict[str, Any]:
        """Get information about currently active market data feeds."""
        return await self._get("/market-data/active-feeds")
    
    async def get_market_data_settings(self) -> Dict[str, Any]:
        """Get current market data settings for debugging."""
        return await self._get("/market-data/settings")
    
    # Enhanced Market Data Operations
    async def get_prices(self, price_request: Dict[str, Any]) -> Dict[str, Any]:
        """Get current prices for specified trading pairs from a connector."""
        return await self._post("/market-data/prices", json=price_request)
    
    async def get_funding_info(self, funding_request: Dict[str, Any]) -> Dict[str, Any]:
        """Get funding information for a perpetual trading pair."""
        return await self._post("/market-data/funding-info", json=funding_request)
    
    async def get_order_book(self, order_book_request: Dict[str, Any]) -> Dict[str, Any]:
        """Get order book snapshot with specified depth."""
        return await self._post("/market-data/order-book", json=order_book_request)
    
    # Order Book Query Operations
    async def get_price_for_volume(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get the price required to fill a specific volume on the order book."""
        return await self._post("/market-data/order-book/price-for-volume", json=request)
    
    async def get_volume_for_price(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get the volume available at a specific price level on the order book."""
        return await self._post("/market-data/order-book/volume-for-price", json=request)
    
    async def get_price_for_quote_volume(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get the price required to fill a specific quote volume on the order book."""
        return await self._post("/market-data/order-book/price-for-quote-volume", json=request)
    
    async def get_quote_volume_for_price(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get the quote volume available at a specific price level on the order book."""
        return await self._post("/market-data/order-book/quote-volume-for-price", json=request)
    
    async def get_vwap_for_volume(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get the VWAP (Volume Weighted Average Price) for a specific volume on the order book."""
        return await self._post("/market-data/order-book/vwap-for-volume", json=request)