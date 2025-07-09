from typing import Optional, Dict, Any, List, Union
from .base import BaseRouter


class MarketDataRouter(BaseRouter):
    """Market Data router for real-time and historical market data."""
    
    # Candles Operations
    async def get_candles(
        self,
        connector: str,
        trading_pair: str,
        interval: str = "1m",
        max_records: int = 100
    ) -> Dict[str, Any]:
        """
        Get real-time candles data for a specific trading pair.
        
        Args:
            connector: Exchange connector name (e.g., "binance", "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            interval: Candle interval (e.g., "1m", "5m", "1h", "1d")
            max_records: Maximum number of candles to return
            
        Returns:
            Real-time candles data
        """
        candles_config = {
            "connector": connector,
            "trading_pair": trading_pair,
            "interval": interval,
            "max_records": max_records
        }
        return await self._post("/market-data/candles", json=candles_config)
    
    async def get_historical_candles(
        self,
        connector: str,
        trading_pair: str,
        interval: str = "1m",
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get historical candles data for a specific trading pair.
        
        Args:
            connector: Exchange connector name (e.g., "binance", "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            interval: Candle interval (e.g., "1m", "5m", "1h", "1d")
            start_time: Start timestamp (Unix timestamp in seconds)
            end_time: End timestamp (Unix timestamp in seconds)
            
        Returns:
            Historical candles data
            
        Note:
            For large date ranges (>1 month of minute data), consider using 
            get_candles_last_days() or higher intervals (5m, 1h) to avoid timeouts.
        """
        config = {
            "connector_name": connector,
            "trading_pair": trading_pair,
            "interval": interval
        }
        if start_time is not None:
            config["start_time"] = int(start_time)
        if end_time is not None:
            config["end_time"] = int(end_time)

        return await self._post("/market-data/historical-candles", json=config)
    
    async def get_candles_last_days(
        self,
        connector: str,
        trading_pair: str,
        days: int,
        interval: str = "1h"
    ) -> Dict[str, Any]:
        """
        Get candles for the last N days.
        
        Args:
            connector: Exchange connector name (e.g., "binance", "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            days: Number of days to look back (e.g., 1, 7, 30)
            interval: Candle interval (e.g., "1m", "5m", "1h", "1d")
            
        Returns:
            Historical candles data for the last N days
            
        Example:
            # Get last 7 days of hourly candles
            candles = await client.market_data.get_candles_last_days(
                "binance_perpetual", "BTC-USDT", 7, "1h"
            )
            
            # Get last 24 hours of 5-minute candles
            candles = await client.market_data.get_candles_last_days(
                "binance_perpetual", "BTC-USDT", 1, "5m"
            )
        """
        import time
        
        end_time = int(time.time())
        start_time = end_time - (days * 24 * 60 * 60)  # days * seconds_per_day
        
        return await self.get_historical_candles(
            connector=connector,
            trading_pair=trading_pair,
            interval=interval,
            start_time=start_time,
            end_time=end_time
        )
    
    async def get_available_candle_connectors(self) -> List[str]:
        """
        Get list of available connectors that support candle data feeds.
        
        Returns:
            List of connector names that can be used for fetching candle data
        """
        return await self._get("/market-data/available-candle-connectors")
    
    async def get_active_feeds(self) -> Dict[str, Any]:
        """Get information about currently active market data feeds."""
        return await self._get("/market-data/active-feeds")
    
    async def get_market_data_settings(self) -> Dict[str, Any]:
        """Get current market data settings for debugging."""
        return await self._get("/market-data/settings")
    
    # Enhanced Market Data Operations
    async def get_prices(
        self, 
        connector: str, 
        trading_pairs: Union[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Get current prices for specified trading pairs from a connector.
        
        Args:
            connector: Exchange connector name (e.g., "binance", "binance_perpetual")
            trading_pairs: Single trading pair or list of trading pairs (e.g., "BTC-USDT" or ["BTC-USDT", "ETH-USDT"])
            
        Returns:
            Current prices for the specified trading pairs
            
        Example:
            prices = await client.market_data.get_prices("binance_perpetual", "BTC-USDT")
            prices = await client.market_data.get_prices("binance", ["BTC-USDT", "ETH-USDT"])
        """
        if isinstance(trading_pairs, str):
            trading_pairs = [trading_pairs]
            
        price_request = {
            "connector_name": connector,
            "trading_pairs": trading_pairs
        }
        return await self._post("/market-data/prices", json=price_request)
    
    async def get_funding_info(self, connector: str, trading_pair: str) -> Dict[str, Any]:
        """
        Get funding information for a perpetual trading pair.
        
        Args:
            connector: Perpetual exchange connector name (e.g., "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            
        Returns:
            Funding information including rates, timestamps, and prices
            
        Example:
            funding = await client.market_data.get_funding_info("binance_perpetual", "BTC-USDT")
        """
        funding_request = {
            "connector_name": connector,
            "trading_pair": trading_pair
        }
        return await self._post("/market-data/funding-info", json=funding_request)
    
    async def get_order_book(
        self, 
        connector: str, 
        trading_pair: str, 
        depth: int = 10
    ) -> Dict[str, Any]:
        """
        Get order book snapshot with specified depth.
        
        Args:
            connector: Exchange connector name (e.g., "binance", "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            depth: Number of price levels to return (1-100)
            
        Returns:
            Order book snapshot with bids and asks
            
        Example:
            order_book = await client.market_data.get_order_book("binance", "BTC-USDT", depth=20)
        """
        order_book_request = {
            "connector_name": connector,
            "trading_pair": trading_pair,
            "depth": depth
        }
        return await self._post("/market-data/order-book", json=order_book_request)
    
    # Order Book Query Operations
    async def get_price_for_volume(
        self, 
        connector: str, 
        trading_pair: str, 
        volume: float, 
        is_buy: bool
    ) -> Dict[str, Any]:
        """
        Get the price required to fill a specific volume on the order book.
        
        Args:
            connector: Exchange connector name (e.g., "binance", "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            volume: Volume to fill (in base asset)
            is_buy: True for buy side, False for sell side
            
        Returns:
            Price information for the specified volume
            
        Example:
            # Get price to buy 1 BTC
            result = await client.market_data.get_price_for_volume("binance", "BTC-USDT", 1.0, True)
        """
        request = {
            "connector_name": connector,
            "trading_pair": trading_pair,
            "volume": volume,
            "is_buy": is_buy
        }
        return await self._post("/market-data/order-book/price-for-volume", json=request)
    
    async def get_volume_for_price(
        self, 
        connector: str, 
        trading_pair: str, 
        price: float, 
        is_buy: bool
    ) -> Dict[str, Any]:
        """
        Get the volume available at a specific price level on the order book.
        
        Args:
            connector: Exchange connector name (e.g., "binance", "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            price: Price level to query
            is_buy: True for buy side, False for sell side
            
        Returns:
            Volume information at the specified price
            
        Example:
            # Get available volume at $50000 on buy side
            result = await client.market_data.get_volume_for_price("binance", "BTC-USDT", 50000.0, True)
        """
        request = {
            "connector_name": connector,
            "trading_pair": trading_pair,
            "price": price,
            "is_buy": is_buy
        }
        return await self._post("/market-data/order-book/volume-for-price", json=request)
    
    async def get_price_for_quote_volume(
        self, 
        connector: str, 
        trading_pair: str, 
        quote_volume: float, 
        is_buy: bool
    ) -> Dict[str, Any]:
        """
        Get the price required to fill a specific quote volume on the order book.
        
        Args:
            connector: Exchange connector name (e.g., "binance", "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            quote_volume: Quote volume to fill (in quote asset, e.g., USDT)
            is_buy: True for buy side, False for sell side
            
        Returns:
            Price information for the specified quote volume
            
        Example:
            # Get price to spend $10000 buying BTC
            result = await client.market_data.get_price_for_quote_volume("binance", "BTC-USDT", 10000.0, True)
        """
        request = {
            "connector_name": connector,
            "trading_pair": trading_pair,
            "quote_volume": quote_volume,
            "is_buy": is_buy
        }
        return await self._post("/market-data/order-book/price-for-quote-volume", json=request)
    
    async def get_quote_volume_for_price(
        self, 
        connector: str, 
        trading_pair: str, 
        price: float, 
        is_buy: bool
    ) -> Dict[str, Any]:
        """
        Get the quote volume available at a specific price level on the order book.
        
        Args:
            connector: Exchange connector name (e.g., "binance", "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            price: Price level to query
            is_buy: True for buy side, False for sell side
            
        Returns:
            Quote volume information at the specified price
            
        Example:
            # Get available quote volume (USDT) at $50000 on buy side
            result = await client.market_data.get_quote_volume_for_price("binance", "BTC-USDT", 50000.0, True)
        """
        request = {
            "connector_name": connector,
            "trading_pair": trading_pair,
            "price": price,
            "is_buy": is_buy
        }
        return await self._post("/market-data/order-book/quote-volume-for-price", json=request)
    
    async def get_vwap_for_volume(
        self, 
        connector: str, 
        trading_pair: str, 
        volume: float, 
        is_buy: bool
    ) -> Dict[str, Any]:
        """
        Get the VWAP (Volume Weighted Average Price) for a specific volume on the order book.
        
        Args:
            connector: Exchange connector name (e.g., "binance", "binance_perpetual")
            trading_pair: Trading pair (e.g., "BTC-USDT")
            volume: Volume to calculate VWAP for (in base asset)
            is_buy: True for buy side, False for sell side
            
        Returns:
            VWAP information for the specified volume
            
        Example:
            # Get VWAP for buying 1 BTC
            result = await client.market_data.get_vwap_for_volume("binance", "BTC-USDT", 1.0, True)
        """
        request = {
            "connector_name": connector,
            "trading_pair": trading_pair,
            "volume": volume,
            "is_buy": is_buy
        }
        return await self._post("/market-data/order-book/vwap-for-volume", json=request)