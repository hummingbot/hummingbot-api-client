from typing import Optional, Dict, Any, List
from .base import BaseRouter


class RateOracleRouter(BaseRouter):
    """Rate Oracle router for managing rate oracle configuration and retrieving rates."""

    async def get_available_sources(self) -> List[str]:
        """Get list of all available rate oracle sources."""
        return await self._get("/rate-oracle/sources")

    async def get_config(self) -> Dict[str, Any]:
        """
        Get current rate oracle configuration.

        Returns:
            Current rate oracle configuration including source, global token, and available sources
        """
        return await self._get("/rate-oracle/config")

    async def update_config(
        self,
        rate_oracle_source: Optional[str] = None,
        global_token_name: Optional[str] = None,
        global_token_symbol: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update rate oracle configuration.

        Args:
            rate_oracle_source: New rate oracle source name (e.g., "binance", "coingecko")
            global_token_name: New global token name (e.g., "USDT")
            global_token_symbol: New global token symbol (e.g., "$")

        Returns:
            Updated configuration with success status
        """
        update = {}
        if rate_oracle_source is not None:
            update["rate_oracle_source"] = {"name": rate_oracle_source}
        if global_token_name is not None or global_token_symbol is not None:
            global_token = {}
            if global_token_name is not None:
                global_token["global_token_name"] = global_token_name
            if global_token_symbol is not None:
                global_token["global_token_symbol"] = global_token_symbol
            update["global_token"] = global_token
        return await self._put("/rate-oracle/config", json=update)

    async def get_rates(self, trading_pairs: List[str]) -> Dict[str, Any]:
        """
        Get rates for specified trading pairs.

        Args:
            trading_pairs: List of trading pairs (e.g., ["BTC-USDT", "ETH-USDT"])

        Returns:
            Rates for the requested trading pairs
        """
        return await self._post("/rate-oracle/rates", json={"trading_pairs": trading_pairs})

    async def get_rate(self, trading_pair: str) -> Dict[str, Any]:
        """
        Get rate for a single trading pair.

        Args:
            trading_pair: Trading pair in format BASE-QUOTE (e.g., "BTC-USDT")

        Returns:
            Rate for the specified trading pair
        """
        return await self._get(f"/rate-oracle/rate/{trading_pair}")

    async def get_rate_async(self, trading_pair: str) -> Dict[str, Any]:
        """
        Get rate for a trading pair using async fetch (direct from exchange).

        This bypasses cached prices and fetches directly from the source.

        Args:
            trading_pair: Trading pair in format BASE-QUOTE (e.g., "BTC-USDT")

        Returns:
            Rate for the specified trading pair
        """
        return await self._get(f"/rate-oracle/rate-async/{trading_pair}")

    async def get_cached_prices(self) -> Dict[str, Any]:
        """
        Get all cached prices from the rate oracle.

        Returns:
            Dictionary with source, quote_token, prices_count, and all cached prices
        """
        return await self._get("/rate-oracle/prices")
