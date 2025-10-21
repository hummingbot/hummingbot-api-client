from typing import Optional, Dict, Any, List
from .base import BaseRouter


class GatewayRouter(BaseRouter):
    """Gateway router for managing Gateway container and DEX operations."""

    # ============================================
    # Container Management
    # ============================================

    async def get_status(self) -> Dict[str, Any]:
        """Get Gateway container status."""
        return await self._get("/gateway/status")

    async def start(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start Gateway container.

        Args:
            config: Gateway configuration dict with keys like:
                - image: Docker image name
                - port: Port to expose
                - environment: Environment variables
        """
        return await self._post("/gateway/start", json=config)

    async def stop(self) -> Dict[str, Any]:
        """Stop Gateway container."""
        return await self._post("/gateway/stop")

    async def restart(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Restart Gateway container.

        If config is provided, the container will be removed and recreated with new configuration.
        If no config is provided, the container will be stopped and started with existing configuration.

        Args:
            config: Optional Gateway configuration dict with keys like:
                - image: Docker image name
                - port: Port to expose
                - environment: Environment variables
        """
        return await self._post("/gateway/restart", json=config if config else None)

    async def get_logs(self, tail: int = 100) -> Dict[str, Any]:
        """
        Get Gateway container logs.

        Args:
            tail: Number of log lines to retrieve (default: 100, max: 10000)
        """
        return await self._get("/gateway/logs", params={"tail": tail})

    # ============================================
    # Connectors
    # ============================================

    async def list_connectors(self) -> Dict[str, Any]:
        """
        List all available DEX connectors with their configurations.

        Returns connector details including name, trading types, chain, and networks.
        All fields normalized to snake_case.
        """
        return await self._get("/gateway/connectors")

    async def get_connector_config(self, connector_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific DEX connector.

        Args:
            connector_name: Connector name (e.g., 'meteora', 'raydium')
        """
        return await self._get(f"/gateway/connectors/{connector_name}")

    async def update_connector_config(
        self,
        connector_name: str,
        config_updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update configuration for a DEX connector.

        Args:
            connector_name: Connector name (e.g., 'meteora', 'raydium')
            config_updates: Dict with path-value pairs to update.
                           Keys can be in snake_case (e.g., {"slippage_pct": 0.5})
                           or camelCase (e.g., {"slippagePct": 0.5})
        """
        return await self._post(f"/gateway/connectors/{connector_name}", json=config_updates)

    # ============================================
    # Chains (Networks) and Tokens
    # ============================================

    async def list_chains(self) -> Dict[str, Any]:
        """
        List all available blockchain chains and their networks.

        This also serves as the networks list endpoint.
        """
        return await self._get("/gateway/chains")

    # ============================================
    # Pools
    # ============================================

    async def list_pools(
        self,
        connector_name: str,
        network: str
    ) -> List[Dict[str, Any]]:
        """
        List all liquidity pools for a connector and network.

        Returns normalized data with snake_case fields and trading_pair.

        Args:
            connector_name: DEX connector (e.g., 'meteora', 'raydium')
            network: Network (e.g., 'mainnet-beta')
        """
        return await self._get(
            "/gateway/pools",
            params={"connector_name": connector_name, "network": network}
        )

    async def add_pool(
        self,
        connector_name: str,
        pool_type: str,
        network: str,
        base: str,
        quote: str,
        address: str
    ) -> Dict[str, Any]:
        """
        Add a custom liquidity pool.

        Args:
            connector_name: DEX connector name
            pool_type: Type of pool
            network: Network name
            base: Base token symbol
            quote: Quote token symbol
            address: Pool address
        """
        pool_data = {
            "connector_name": connector_name,
            "type": pool_type,
            "network": network,
            "base": base,
            "quote": quote,
            "address": address
        }
        return await self._post("/gateway/pools", json=pool_data)

    # ============================================
    # Networks (Primary Endpoints)
    # ============================================

    async def list_networks(self) -> Dict[str, Any]:
        """
        List all available networks across all chains.

        Returns a flattened list of network IDs in the format 'chain-network'.
        This is the primary interface for network discovery.
        """
        return await self._get("/gateway/networks")

    async def get_network_config(self, network_id: str) -> Dict[str, Any]:
        """
        Get configuration for a specific network.

        Args:
            network_id: Network ID in format 'chain-network'
                       (e.g., 'solana-mainnet-beta', 'ethereum-mainnet')
        """
        return await self._get(f"/gateway/networks/{network_id}")

    async def update_network_config(
        self,
        network_id: str,
        config_updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update configuration for a specific network.

        Args:
            network_id: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            config_updates: Dict with path-value pairs to update.
                           Keys can be in snake_case (e.g., {"node_url": "https://..."})
                           or camelCase (e.g., {"nodeURL": "https://..."})
        """
        return await self._post(f"/gateway/networks/{network_id}", json=config_updates)

    async def get_network_tokens(
        self,
        network_id: str,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get available tokens for a network.

        Args:
            network_id: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            search: Optional filter to search tokens by symbol or name
        """
        params = {}
        if search:
            params["search"] = search
        return await self._get(f"/gateway/networks/{network_id}/tokens", params=params or None)

    async def add_token(
        self,
        network_id: str,
        address: str,
        symbol: str,
        decimals: int,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a custom token to Gateway's token list for a specific network.

        Args:
            network_id: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta', 'ethereum-mainnet')
            address: Token contract address
            symbol: Token symbol (e.g., 'GOLD', 'USDC')
            decimals: Token decimals (e.g., 6 for USDC, 9 for SOL)
            name: Optional token name (if not provided, symbol will be used)

        Note: After adding a token, restart Gateway for changes to take effect.

        Example:
            await client.gateway.add_token(
                network_id='solana-mainnet-beta',
                address='9QFfgxdSqH5zT7j6rZb1y6SZhw2aFtcQu2r6BuYpump',
                symbol='GOLD',
                decimals=9,
                name='Goldcoin'
            )
        """
        token_data = {
            "address": address,
            "symbol": symbol,
            "decimals": decimals
        }
        if name is not None:
            token_data["name"] = name

        return await self._post(f"/gateway/networks/{network_id}/tokens", json=token_data)

    async def delete_token(
        self,
        network_id: str,
        token_address: str
    ) -> Dict[str, Any]:
        """
        Delete a custom token from Gateway's token list for a specific network.

        Args:
            network_id: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta', 'ethereum-mainnet')
            token_address: Token contract address to delete

        Note: After deleting a token, restart Gateway for changes to take effect.

        Example:
            await client.gateway.delete_token(
                network_id='solana-mainnet-beta',
                token_address='9QFfgxdSqH5zT7j6rZb1y6SZhw2aFtcQu2r6BuYpump'
            )
        """
        return await self._delete(f"/gateway/networks/{network_id}/tokens/{token_address}")