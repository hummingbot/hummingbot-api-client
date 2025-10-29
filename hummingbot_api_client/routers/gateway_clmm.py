from typing import Optional, Dict, Any, List
from decimal import Decimal
from .base import BaseRouter


class GatewayCLMMRouter(BaseRouter):
    """Gateway CLMM router for DEX CLMM liquidity operations via Hummingbot Gateway.
    Supports CLMM connectors (Meteora, Raydium, Uniswap V3) for concentrated liquidity positions.
    """

    async def get_pool_info(
        self,
        connector: str,
        network: str,
        pool_address: str
    ) -> Dict[str, Any]:
        """
        Get detailed information about a CLMM pool by pool address.

        Args:
            connector: CLMM connector (e.g., 'meteora', 'raydium')
            network: Network ID in 'chain-network' format (e.g., 'solana-mainnet-beta')
            pool_address: Pool contract address

        Returns:
            Pool information including liquidity, price, bins (for Meteora), etc.
            All field names are returned in snake_case format.

        Example:
            pool_info = await client.gateway_clmm.get_pool_info(
                connector='meteora',
                network='solana-mainnet-beta',
                pool_address='2sf5NYcY4zUPXUSmG6f66mskb24t5F8S11pC1Nz5nQT3'
            )
        """
        params = {
            "connector": connector,
            "network": network,
            "pool_address": pool_address
        }
        return await self._get("/gateway/clmm/pool-info", params=params)

    async def get_pools(
        self,
        connector: str,
        page: int = 0,
        limit: int = 50,
        search_term: Optional[str] = None,
        sort_key: Optional[str] = "volume",
        order_by: Optional[str] = "desc",
        include_unknown: bool = True
    ) -> Dict[str, Any]:
        """
        Get list of available CLMM pools for a connector.

        Currently supports: meteora

        Args:
            connector: CLMM connector (e.g., 'meteora')
            page: Page number (default: 0)
            limit: Results per page (default: 50, max: 100)
            search_term: Search term to filter pools (optional)
            sort_key: Sort by field (volume, tvl, feetvlratio, etc.)
            order_by: Sort order (asc, desc)
            include_unknown: Include pools with unverified tokens

        Returns:
            List of available pools with trading pairs, addresses, liquidity, volume, APR, etc.

        Example:
            pools = await client.gateway_clmm.get_pools(
                connector='meteora',
                search_term='SOL',
                limit=20
            )
            for pool in pools['pools']:
                print(f"{pool['trading_pair']}: TVL ${pool['liquidity']}")
        """
        params = {
            "connector": connector,
            "page": page,
            "limit": min(limit, 100),  # Cap at 100
            "include_unknown": str(include_unknown).lower()  # Convert boolean to lowercase string
        }
        if search_term:
            params["search_term"] = search_term
        if sort_key:
            params["sort_key"] = sort_key
        if order_by:
            params["order_by"] = order_by

        return await self._get("/gateway/clmm/pools", params=params)

    async def open_position(
        self,
        connector: str,
        network: str,
        pool_address: str,
        lower_price: Decimal,
        upper_price: Decimal,
        base_token_amount: Optional[Decimal] = None,
        quote_token_amount: Optional[Decimal] = None,
        slippage_pct: Optional[Decimal] = None,
        wallet_address: Optional[str] = None,
        extra_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Open a NEW CLMM position with initial liquidity.

        Args:
            connector: CLMM connector (e.g., 'meteora')
            network: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            pool_address: Pool contract address
            lower_price: Lower price bound
            upper_price: Upper price bound
            base_token_amount: Amount of base token to provide (optional)
            quote_token_amount: Amount of quote token to provide (optional)
            slippage_pct: Slippage percentage tolerance (default: 1.0)
            wallet_address: Wallet address (uses default if not provided)
            extra_params: Additional connector-specific parameters (e.g., {"strategyType": 0} for Meteora)

        Returns:
            Transaction hash and position address

        Example:
            result = await client.gateway_clmm.open_position(
                connector='meteora',
                network='solana-mainnet-beta',
                pool_address='2sf5NYcY4zUPXUSmG6f66mskb24t5F8S11pC1Nz5nQT3',
                lower_price=Decimal('150'),
                upper_price=Decimal('250'),
                base_token_amount=Decimal('0.01'),
                quote_token_amount=Decimal('2'),
                slippage_pct=Decimal('1'),
                extra_params={"strategyType": 0}
            )
        """
        request_data = {
            "connector": connector,
            "network": network,
            "pool_address": pool_address,
            "lower_price": str(lower_price),
            "upper_price": str(upper_price),
            "slippage_pct": str(slippage_pct) if slippage_pct else "1.0"
        }
        if base_token_amount is not None:
            request_data["base_token_amount"] = str(base_token_amount)
        if quote_token_amount is not None:
            request_data["quote_token_amount"] = str(quote_token_amount)
        if wallet_address:
            request_data["wallet_address"] = wallet_address
        if extra_params:
            request_data["extra_params"] = extra_params

        return await self._post("/gateway/clmm/open", json=request_data)

    async def close_position(
        self,
        connector: str,
        network: str,
        position_address: str,
        wallet_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        CLOSE a position completely (removes all liquidity).

        Args:
            connector: CLMM connector (e.g., 'meteora')
            network: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            position_address: Position NFT address
            wallet_address: Wallet address (uses default if not provided)

        Returns:
            Transaction hash

        Example:
            result = await client.gateway_clmm.close_position(
                connector='meteora',
                network='solana-mainnet-beta',
                position_address='...'
            )
        """
        request_data = {
            "connector": connector,
            "network": network,
            "position_address": position_address
        }
        if wallet_address:
            request_data["wallet_address"] = wallet_address

        return await self._post("/gateway/clmm/close", json=request_data)

    async def collect_fees(
        self,
        connector: str,
        network: str,
        position_address: str,
        wallet_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Collect accumulated fees from a liquidity position.

        Args:
            connector: CLMM connector (e.g., 'meteora')
            network: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            position_address: Position NFT address
            wallet_address: Wallet address (uses default if not provided)

        Returns:
            Transaction hash and collected fee amounts

        Example:
            result = await client.gateway_clmm.collect_fees(
                connector='meteora',
                network='solana-mainnet-beta',
                position_address='...'
            )
            print(f"Collected: {result['base_fee_collected']} base, {result['quote_fee_collected']} quote")
        """
        request_data = {
            "connector": connector,
            "network": network,
            "position_address": position_address
        }
        if wallet_address:
            request_data["wallet_address"] = wallet_address

        return await self._post("/gateway/clmm/collect-fees", json=request_data)

    async def get_positions_owned(
        self,
        connector: str,
        network: str,
        pool_address: str,
        wallet_address: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all liquidity positions owned by a wallet for a specific pool.

        Args:
            connector: CLMM connector (e.g., 'meteora')
            network: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            pool_address: Pool contract address
            wallet_address: Wallet address (uses default if not provided)

        Returns:
            List of position information for the specified pool

        Example:
            positions = await client.gateway_clmm.get_positions_owned(
                connector='meteora',
                network='solana-mainnet-beta',
                pool_address='2sf5NYcY4zUPXUSmG6f66mskb24t5F8S11pC1Nz5nQT3'
            )
            for pos in positions:
                print(f"Position: {pos['position_address']} - In Range: {pos['in_range']}")
        """
        request_data = {
            "connector": connector,
            "network": network,
            "pool_address": pool_address
        }
        if wallet_address:
            request_data["wallet_address"] = wallet_address

        return await self._post("/gateway/clmm/positions_owned", json=request_data)

    async def get_position_events(
        self,
        position_address: str,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get event history for a position.

        Args:
            position_address: Position NFT address
            event_type: Filter by event type (OPEN, ADD_LIQUIDITY, REMOVE_LIQUIDITY, COLLECT_FEES, CLOSE)
            limit: Max events to return

        Returns:
            List of position events

        Example:
            events = await client.gateway_clmm.get_position_events(
                position_address='...',
                event_type='COLLECT_FEES',
                limit=10
            )
            for event in events['data']:
                print(f"Event: {event['event_type']} - {event['transaction_hash']}")
        """
        params = {"limit": limit}
        if event_type:
            params["event_type"] = event_type

        return await self._get(f"/gateway/clmm/positions/{position_address}/events", params=params)

    async def search_positions(
        self,
        network: Optional[str] = None,
        connector: Optional[str] = None,
        wallet_address: Optional[str] = None,
        trading_pair: Optional[str] = None,
        status: Optional[str] = None,
        position_addresses: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0,
        refresh: bool = False
    ) -> Dict[str, Any]:
        """
        Search positions with filters.

        Args:
            network: Filter by network (e.g., 'solana-mainnet-beta')
            connector: Filter by connector (e.g., 'meteora')
            wallet_address: Filter by wallet address
            trading_pair: Filter by trading pair (e.g., 'SOL-USDC')
            status: Filter by status (OPEN, CLOSED)
            position_addresses: Filter by specific position addresses (list)
            limit: Max results (default 50, max 1000)
            offset: Pagination offset
            refresh: If True, refresh position data from Gateway before returning

        Returns:
            Paginated list of positions

        Example:
            results = await client.gateway_clmm.search_positions(
                network='solana-mainnet-beta',
                connector='meteora',
                status='OPEN',
                limit=10,
                refresh=True
            )
            for position in results['data']:
                print(f"Position: {position['position_address']} - {position['in_range']}")
        """
        request_data = {
            "limit": limit,
            "offset": offset,
            "refresh": refresh
        }
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
        if position_addresses is not None:
            request_data["position_addresses"] = position_addresses

        return await self._post("/gateway/clmm/positions/search", json=request_data)
