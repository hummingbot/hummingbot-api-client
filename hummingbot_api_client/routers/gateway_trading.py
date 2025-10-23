from typing import Optional, Dict, Any
from decimal import Decimal
from .base import BaseRouter


class GatewayTradingRouter(BaseRouter):
    """Gateway Trading router for DEX trading operations via Hummingbot Gateway."""

    # ============================================
    # Swap Operations (Router: Jupiter, 0x)
    # ============================================

    async def get_swap_quote(
        self,
        connector: str,
        network: str,
        trading_pair: str,
        side: str,
        amount: Decimal,
        slippage_pct: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        """
        Get a price quote for a swap via router (Jupiter, 0x).

        Args:
            connector: DEX connector name (e.g., 'jupiter', '0x')
            network: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            trading_pair: Trading pair in format 'BASE-QUOTE' (e.g., 'SOL-USDC')
            side: Trade side - 'BUY' or 'SELL'
            amount: Amount to trade
            slippage_pct: Optional slippage percentage (default: 1.0)

        Returns:
            Quote with price, expected output amount, and gas estimate

        Example:
            quote = await client.gateway_trading.get_swap_quote(
                connector='jupiter',
                network='solana-mainnet-beta',
                trading_pair='SOL-USDC',
                side='BUY',
                amount=Decimal('1'),
                slippage_pct=Decimal('1.0')
            )
        """
        request_data = {
            "connector": connector,
            "network": network,
            "trading_pair": trading_pair,
            "side": side,
            "amount": str(amount),
            "slippage_pct": str(slippage_pct) if slippage_pct else "1.0"
        }
        return await self._post("/gateway/swap/quote", json=request_data)

    async def execute_swap(
        self,
        connector: str,
        network: str,
        trading_pair: str,
        side: str,
        amount: Decimal,
        slippage_pct: Optional[Decimal] = None,
        wallet_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a swap transaction via router (Jupiter, 0x).

        Args:
            connector: DEX connector name (e.g., 'jupiter', '0x')
            network: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            trading_pair: Trading pair in format 'BASE-QUOTE' (e.g., 'SOL-USDC')
            side: Trade side - 'BUY' or 'SELL'
            amount: Amount to trade
            slippage_pct: Optional slippage percentage (default: 1.0)
            wallet_address: Optional wallet address (uses default if not provided)

        Returns:
            Transaction hash and swap details

        Example:
            result = await client.gateway_trading.execute_swap(
                connector='jupiter',
                network='solana-mainnet-beta',
                trading_pair='SOL-USDC',
                side='BUY',
                amount=Decimal('1'),
                slippage_pct=Decimal('1.0')
            )
            print(f"Transaction hash: {result['transaction_hash']}")
        """
        request_data = {
            "connector": connector,
            "network": network,
            "trading_pair": trading_pair,
            "side": side,
            "amount": str(amount),
            "slippage_pct": str(slippage_pct) if slippage_pct else "1.0"
        }
        if wallet_address:
            request_data["wallet_address"] = wallet_address

        return await self._post("/gateway/swap/execute", json=request_data)

    # ============================================
    # Query Endpoints for Swaps and Positions
    # ============================================

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
            swap = await client.gateway_trading.get_swap_status(
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
            results = await client.gateway_trading.search_swaps(
                network='solana-mainnet-beta',
                connector='jupiter',
                status='CONFIRMED',
                limit=10
            )
            for swap in results['data']:
                print(f"Swap: {swap['trading_pair']} - {swap['status']}")
        """
        request_data = {}
        if network is not None:
            request_data["network"] = network
        if connector is not None:
            request_data["connector"] = connector
        if wallet_address is not None:
            request_data["wallet_address"] = wallet_address
        if trading_pair is not None:
            request_data["trading_pair"] = trading_pair
        if status is not None:
            request_data["status"] = status
        if start_time is not None:
            request_data["start_time"] = start_time
        if end_time is not None:
            request_data["end_time"] = end_time
        request_data["limit"] = limit
        request_data["offset"] = offset

        return await self._post("/gateway/swaps/search", json=request_data)

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
            summary = await client.gateway_trading.get_swaps_summary(
                network='solana-mainnet-beta',
                wallet_address='ABC...'
            )
            print(f"Total volume: {summary['total_volume']}")
            print(f"Success rate: {summary['success_rate']}")
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
