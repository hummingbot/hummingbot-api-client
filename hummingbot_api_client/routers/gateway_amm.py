from typing import Optional, Dict, Any, List
from decimal import Decimal
from .base import BaseRouter


class GatewayAMMRouter(BaseRouter):
    """Gateway AMM router for DEX AMM liquidity operations via Hummingbot Gateway.

    Supports AMM connectors (Meteora DAMM v2, Raydium CPMM, Uniswap/Pancakeswap V2). Unlike CLMM,
    Meteora DAMM v2 positions are NFTs, so these routes are position-addressed: remove requires
    position_address (meteora), add takes it optionally (omit = new position), position-info returns
    a positions[] breakdown, and positions-owned lists all of a wallet's positions. Fungible-LP AMMs
    ignore position_address and reject positions-owned.
    """

    async def get_pool_info(
        self,
        connector: str,
        network: str,
        pool_address: str,
    ) -> Dict[str, Any]:
        """
        Get AMM pool information (reserves, price, base fee) by pool address.

        Example:
            info = await client.gateway_amm.get_pool_info(
                connector='meteora', network='solana-mainnet-beta',
                pool_address='Bv65dPQKpUo7vRELhEGBkkm5wq9J3MvKGyUj8WxYtunM')
        """
        return await self._get("/gateway/amm/pool-info", params={
            "connector": connector, "network": network, "pool_address": pool_address,
        })

    async def get_position_info(
        self,
        connector: str,
        network: str,
        pool_address: str,
        wallet_address: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get a wallet's aggregate liquidity in an AMM pool plus a per-position breakdown (DAMM v2).

        The top-level amounts are the aggregate across the wallet's positions in the pool; the
        `positions` array (Meteora only) breaks that out per NFT. Read it to get the position
        addresses to pass to add_liquidity / remove_liquidity.
        """
        params = {"connector": connector, "network": network, "pool_address": pool_address}
        if wallet_address:
            params["wallet_address"] = wallet_address
        return await self._get("/gateway/amm/position-info", params=params)

    async def get_positions_owned(
        self,
        connector: str,
        network: str,
        wallet_address: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        List all of a wallet's AMM positions across pools (Meteora DAMM v2 only).

        Fungible-LP AMMs (raydium, uniswap, pancakeswap) have no enumerable positions and are
        rejected — use get_position_info with a specific pool address instead.
        """
        request_data = {"connector": connector, "network": network}
        if wallet_address:
            request_data["wallet_address"] = wallet_address
        return await self._post("/gateway/amm/positions-owned", json=request_data)

    async def get_swap_quote(
        self,
        connector: str,
        network: str,
        pool_address: str,
        base_token: str,
        side: str,
        amount: Decimal,
        slippage_pct: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        """Quote a swap against a specific AMM pool (pool-scoped, not router)."""
        request_data = {
            "connector": connector,
            "network": network,
            "pool_address": pool_address,
            "base_token": base_token,
            "side": side,
            "amount": str(amount),
        }
        if slippage_pct is not None:
            request_data["slippage_pct"] = str(slippage_pct)
        return await self._post("/gateway/amm/quote-swap", json=request_data)

    async def execute_swap(
        self,
        connector: str,
        network: str,
        pool_address: str,
        base_token: str,
        side: str,
        amount: Decimal,
        slippage_pct: Optional[Decimal] = None,
        wallet_address: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute a swap against a specific AMM pool."""
        request_data = {
            "connector": connector,
            "network": network,
            "pool_address": pool_address,
            "base_token": base_token,
            "side": side,
            "amount": str(amount),
        }
        if slippage_pct is not None:
            request_data["slippage_pct"] = str(slippage_pct)
        if wallet_address:
            request_data["wallet_address"] = wallet_address
        return await self._post("/gateway/amm/execute-swap", json=request_data)

    async def get_liquidity_quote(
        self,
        connector: str,
        network: str,
        pool_address: str,
        base_token_amount: Decimal,
        quote_token_amount: Decimal,
        slippage_pct: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        """Quote a two-sided liquidity deposit."""
        request_data = {
            "connector": connector,
            "network": network,
            "pool_address": pool_address,
            "base_token_amount": str(base_token_amount),
            "quote_token_amount": str(quote_token_amount),
        }
        if slippage_pct is not None:
            request_data["slippage_pct"] = str(slippage_pct)
        return await self._post("/gateway/amm/quote-liquidity", json=request_data)

    async def add_liquidity(
        self,
        connector: str,
        network: str,
        pool_address: str,
        base_token_amount: Decimal,
        quote_token_amount: Decimal,
        slippage_pct: Optional[Decimal] = None,
        wallet_address: Optional[str] = None,
        position_address: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add two-sided liquidity to an AMM pool.

        Meteora DAMM v2: pass position_address to add to that NFT position; omit it to open a NEW
        position. Fungible-LP AMMs ignore position_address.
        """
        request_data = {
            "connector": connector,
            "network": network,
            "pool_address": pool_address,
            "base_token_amount": str(base_token_amount),
            "quote_token_amount": str(quote_token_amount),
        }
        if slippage_pct is not None:
            request_data["slippage_pct"] = str(slippage_pct)
        if wallet_address:
            request_data["wallet_address"] = wallet_address
        if position_address:
            request_data["position_address"] = position_address
        return await self._post("/gateway/amm/add-liquidity", json=request_data)

    async def remove_liquidity(
        self,
        connector: str,
        network: str,
        pool_address: str,
        percentage_to_remove: Decimal,
        position_address: Optional[str] = None,
        slippage_pct: Optional[Decimal] = None,
        wallet_address: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Remove liquidity from an AMM pool.

        Meteora DAMM v2 requires position_address (positions are NFTs); "remove 100%" then truly
        exits that named position. Fungible-LP AMMs ignore it.
        """
        request_data = {
            "connector": connector,
            "network": network,
            "pool_address": pool_address,
            "percentage_to_remove": str(percentage_to_remove),
        }
        if position_address:
            request_data["position_address"] = position_address
        if slippage_pct is not None:
            request_data["slippage_pct"] = str(slippage_pct)
        if wallet_address:
            request_data["wallet_address"] = wallet_address
        return await self._post("/gateway/amm/remove-liquidity", json=request_data)

    async def create_pool(
        self,
        connector: str,
        network: str,
        base_token: str,
        quote_token: str,
        base_token_amount: Decimal,
        quote_token_amount: Optional[Decimal] = None,
        initial_price: Optional[Decimal] = None,
        slippage_pct: Optional[Decimal] = None,
        wallet_address: Optional[str] = None,
        extra_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create and seed a new AMM pool.

        Seed price priority: initial_price -> quote_token_amount ratio -> live market price
        (anti-snipe). Only base_token_amount is required. slippage_pct bounds the seeding
        deposit on EVM connectors; omit to use the connector's configured slippage.
        Connector-specific params ride extra_params under Gateway's own names:
        configAddress (meteora, required there), ammConfigIndex (raydium).
        Unknown keys are rejected by the API with a 400.
        """
        request_data = {
            "connector": connector,
            "network": network,
            "base_token": base_token,
            "quote_token": quote_token,
            "base_token_amount": str(base_token_amount),
        }
        if quote_token_amount is not None:
            request_data["quote_token_amount"] = str(quote_token_amount)
        if initial_price is not None:
            request_data["initial_price"] = str(initial_price)
        if slippage_pct is not None:
            request_data["slippage_pct"] = str(slippage_pct)
        if wallet_address:
            request_data["wallet_address"] = wallet_address
        if extra_params:
            request_data["extra_params"] = extra_params
        return await self._post("/gateway/amm/create-pool", json=request_data)
