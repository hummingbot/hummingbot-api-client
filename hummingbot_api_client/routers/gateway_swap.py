from typing import Optional, Dict, Any
from decimal import Decimal
from .base import BaseRouter


class GatewaySwapRouter(BaseRouter):
    """Gateway Swap router for DEX swap operations via Hummingbot Gateway.
    Supports Router connectors (Jupiter, 0x) for token swaps.
    """

    async def get_swap_quote(
        self,
        connector: str,
        network: str,
        trading_pair: str,
        side: str,
        amount: Decimal,
        slippage_pct: Optional[Decimal] = None,
        extra_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get a price quote for a swap via router (Jupiter, 0x).

        Args:
            connector: DEX connector name (e.g., 'jupiter', '0x')
            network: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            trading_pair: Trading pair in format 'BASE-QUOTE' (e.g., 'SOL-USDC')
            side: Trade side - 'BUY' or 'SELL'
            amount: Amount to trade
            slippage_pct: Optional slippage percentage. Omit to use the
                connector's configured slippage; 0 is a real value.
            extra_params: Optional connector-specific params under Gateway's own
                key names. Supported: approximateIfNoExactOut (bool) for the
                jupiter/dflow/okx/titan routers.

        Returns:
            Quote with price, expected output amount, and gas estimate

        Example:
            quote = await client.gateway_swap.get_swap_quote(
                connector='jupiter',
                network='solana-mainnet-beta',
                trading_pair='SOL-USDC',
                side='BUY',
                amount=Decimal('1')
            )
        """
        request_data = {
            "connector": connector,
            "network": network,
            "trading_pair": trading_pair,
            "side": side,
            "amount": str(amount)
        }
        if slippage_pct is not None:
            request_data["slippage_pct"] = str(slippage_pct)
        if extra_params is not None:
            request_data["extra_params"] = extra_params
        return await self._post("/gateway/swap/quote", json=request_data)

    async def execute_swap(
        self,
        connector: str,
        network: str,
        trading_pair: str,
        side: str,
        amount: Decimal,
        slippage_pct: Optional[Decimal] = None,
        wallet_address: Optional[str] = None,
        extra_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a swap transaction via router (Jupiter, 0x).

        Args:
            connector: DEX connector name (e.g., 'jupiter', '0x')
            network: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            trading_pair: Trading pair in format 'BASE-QUOTE' (e.g., 'SOL-USDC')
            side: Trade side - 'BUY' or 'SELL'
            amount: Amount to trade
            slippage_pct: Optional slippage percentage. Omit to use the
                connector's configured slippage; 0 is a real value.
            wallet_address: Optional wallet address (uses default if not provided)
            extra_params: Optional connector-specific params under Gateway's own
                key names. Supported: approximateIfNoExactOut (bool) for the
                jupiter/dflow/okx/titan routers.

        Returns:
            Transaction hash and swap details

        Example:
            result = await client.gateway_swap.execute_swap(
                connector='jupiter',
                network='solana-mainnet-beta',
                trading_pair='SOL-USDC',
                side='BUY',
                amount=Decimal('1')
            )
            print(f"Transaction hash: {result['transaction_hash']}")
        """
        request_data = {
            "connector": connector,
            "network": network,
            "trading_pair": trading_pair,
            "side": side,
            "amount": str(amount)
        }
        if slippage_pct is not None:
            request_data["slippage_pct"] = str(slippage_pct)
        if wallet_address:
            request_data["wallet_address"] = wallet_address
        if extra_params is not None:
            request_data["extra_params"] = extra_params

        return await self._post("/gateway/swap/execute", json=request_data)

    async def get_swap_status(
        self,
        transaction_hash: str
    ) -> Dict[str, Any]:
        """
        Get status of a specific swap by transaction hash.

        Args:
            transaction_hash: Transaction hash of the swap

        Returns:
            Swap details including current status

        Example:
            swap = await client.gateway_swap.get_swap_status(
                transaction_hash='5X...'
            )
            print(f"Status: {swap['status']}")
        """
        return await self._get(f"/gateway/swaps/{transaction_hash}/status")

    async def search_swaps(
        self,
        network: Optional[str] = None,
        connector: Optional[str] = None,
        wallet_address: Optional[str] = None,
        trading_pair: Optional[str] = None,
        status: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search swap history with filters.

        Args:
            network: Filter by network (e.g., 'solana-mainnet-beta')
            connector: Filter by connector (e.g., 'jupiter')
            wallet_address: Filter by wallet address
            trading_pair: Filter by trading pair (e.g., 'SOL-USDC')
            status: Filter by status (SUBMITTED, CONFIRMED, FAILED)
            start_time: Start timestamp (unix seconds)
            end_time: End timestamp (unix seconds)
            limit: Max results (default 50, max 1000)
            offset: Pagination offset

        Returns:
            Paginated list of swaps with pagination metadata

        Example:
            results = await client.gateway_swap.search_swaps(
                network='solana-mainnet-beta',
                connector='jupiter',
                status='CONFIRMED',
                limit=10
            )
            for swap in results['data']:
                print(f"Swap: {swap['trading_pair']} - {swap['status']}")
        """
        # hapi declares these as query parameters on a POST — a JSON body is
        # silently ignored, so the filters must ride the query string.
        params = {}
        if network is not None:
            params["network"] = network
        if connector is not None:
            params["connector"] = connector
        if wallet_address is not None:
            params["wallet_address"] = wallet_address
        if trading_pair is not None:
            params["trading_pair"] = trading_pair
        if status is not None:
            params["status"] = status
        if start_time is not None:
            params["start_time"] = str(start_time)
        if end_time is not None:
            params["end_time"] = str(end_time)
        params["limit"] = str(limit)
        params["offset"] = str(offset)

        return await self._post("/gateway/swaps/search", params=params)

    async def get_swaps_summary(
        self,
        network: Optional[str] = None,
        wallet_address: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get swap summary statistics.

        Args:
            network: Filter by network
            wallet_address: Filter by wallet address
            start_time: Start timestamp (unix seconds)
            end_time: End timestamp (unix seconds)

        Returns:
            Summary statistics including volume, fees, success rate

        Example:
            summary = await client.gateway_swap.get_swaps_summary(
                network='solana-mainnet-beta',
                wallet_address='ABC...'
            )
            for token, volume in summary['volume_by_quote_token'].items():
                print(f"Volume ({token}): {volume}")
        """
        params = {}
        if network is not None:
            params["network"] = network
        if wallet_address is not None:
            params["wallet_address"] = wallet_address
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time

        return await self._get("/gateway/swaps/summary", params=params)
