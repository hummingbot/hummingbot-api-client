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
    # API Keys
    # ============================================

    async def get_api_keys(self) -> Dict[str, Any]:
        """
        Get all configured API keys from Gateway.

        Returns a dict mapping provider name to API key value.

        Example:
            api_keys = await client.gateway.get_api_keys()
            # Returns: {"helius": "abc123", "infura": "xyz789", "coingecko": "...", "etherscan": ""}
        """
        return await self._get("/gateway/apiKeys")

    async def update_api_keys(self, api_keys: Dict[str, str]) -> Dict[str, Any]:
        """
        Update API keys in Gateway configuration.

        Args:
            api_keys: Dict mapping provider name to API key value
                     (e.g., {"helius": "abc123", "infura": "xyz789"})

        Note: After updating API keys, restart Gateway for changes to take effect.

        Example:
            await client.gateway.update_api_keys({
                "helius": "new-helius-key",
                "infura": "new-infura-key"
            })
        """
        return await self._post("/gateway/apiKeys", json={"api_keys": api_keys})

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

    async def delete_pool(
        self,
        connector: str,
        network: str,
        pool_type: str,
        address: str
    ) -> Dict[str, Any]:
        """
        Delete a liquidity pool from Gateway's pool list.

        Args:
            connector: DEX connector (e.g., 'meteora', 'raydium', 'uniswap')
            network: Network name (e.g., 'mainnet-beta', 'mainnet')
            pool_type: Pool type (e.g., 'CLMM', 'AMM')
            address: Pool contract address to remove

        Example:
            await client.gateway.delete_pool(
                connector='meteora',
                network='mainnet-beta',
                pool_type='CLMM',
                address='2sf5NYcY4zUPXUSmG6f66mskb24t5F8S11pC1Nz5nQT3'
            )
        """
        params = {
            "connector_name": connector,
            "network": network,
            "pool_type": pool_type.lower()  # Gateway expects lowercase (amm, clmm)
        }
        return await self._delete(f"/gateway/pools/{address}", params=params)

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

    async def save_network_token(
        self,
        network_id: str,
        token_address: str
    ) -> Dict[str, Any]:
        """
        Save a token by address - auto-fetches token info from GeckoTerminal.

        This is the simplest way to add a token. Just provide the address and
        the API will fetch symbol, name, and decimals automatically.

        Args:
            network_id: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            token_address: Token contract address

        Example:
            await client.gateway.save_network_token(
                network_id='solana-mainnet-beta',
                token_address='9QFfgxdSqH5zT7j6rZb1y6SZhw2aFtcQu2r6BuYpump'
            )
        """
        return await self._post(f"/gateway/networks/{network_id}/tokens/save/{token_address}")

    # ============================================
    # Network Pools (Primary Pool Endpoints)
    # ============================================

    async def get_network_pools(
        self,
        network_id: str,
        connector: Optional[str] = None,
        pool_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get pools for a specific network.

        Args:
            network_id: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            connector: Optional filter by connector (e.g., 'raydium', 'meteora', 'uniswap')
            pool_type: Optional filter by type ('amm' or 'clmm')
            search: Optional search by trading pair or address

        Example:
            await client.gateway.get_network_pools(
                network_id='solana-mainnet-beta',
                connector='raydium',
                pool_type='clmm'
            )
        """
        params = {}
        if connector:
            params["connector"] = connector
        if pool_type:
            params["pool_type"] = pool_type.lower()
        if search:
            params["search"] = search
        return await self._get(f"/gateway/networks/{network_id}/pools", params=params or None)

    async def add_network_pool(
        self,
        network_id: str,
        connector_name: str,
        pool_type: str,
        address: str,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        base_address: Optional[str] = None,
        quote_address: Optional[str] = None,
        fee_pct: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Add a pool to a specific network.

        Args:
            network_id: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            connector_name: DEX connector name (e.g., 'raydium', 'meteora')
            pool_type: Pool type ('amm' or 'clmm')
            address: Pool contract address
            base: Optional base token symbol
            quote: Optional quote token symbol
            base_address: Optional base token address
            quote_address: Optional quote token address
            fee_pct: Optional fee percentage

        Example:
            await client.gateway.add_network_pool(
                network_id='solana-mainnet-beta',
                connector_name='raydium',
                pool_type='clmm',
                address='58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2'
            )
        """
        pool_data = {
            "connector_name": connector_name,
            "type": pool_type.lower(),
            "address": address
        }
        if base:
            pool_data["base"] = base
        if quote:
            pool_data["quote"] = quote
        if base_address:
            pool_data["base_address"] = base_address
        if quote_address:
            pool_data["quote_address"] = quote_address
        if fee_pct is not None:
            pool_data["fee_pct"] = fee_pct

        return await self._post(f"/gateway/networks/{network_id}/pools", json=pool_data)

    async def delete_network_pool(
        self,
        network_id: str,
        address: str,
        pool_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Delete a pool from a specific network.

        Args:
            network_id: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            address: Pool contract address to remove
            pool_type: Optional pool type ('amm' or 'clmm')

        Example:
            await client.gateway.delete_network_pool(
                network_id='solana-mainnet-beta',
                address='58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2'
            )
        """
        params = {}
        if pool_type:
            params["pool_type"] = pool_type.lower()
        return await self._delete(f"/gateway/networks/{network_id}/pools/{address}", params=params or None)

    async def save_network_pool(
        self,
        network_id: str,
        pool_address: str
    ) -> Dict[str, Any]:
        """
        Save a pool by address - auto-fetches pool info from the blockchain.

        This is the simplest way to add a pool. Just provide the address and
        the API will fetch connector, type, tokens, and fees automatically.

        Args:
            network_id: Network ID in format 'chain-network' (e.g., 'solana-mainnet-beta')
            pool_address: Pool contract address

        Example:
            await client.gateway.save_network_pool(
                network_id='solana-mainnet-beta',
                pool_address='58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2'
            )
        """
        return await self._post(f"/gateway/networks/{network_id}/pools/save/{pool_address}")

    # ============================================
    # Wallets
    # ============================================

    async def create_wallet(
        self,
        chain: str,
        set_default: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new wallet in Gateway.

        Args:
            chain: Blockchain chain (e.g., 'solana', 'ethereum')
            set_default: Whether to set this wallet as the default (default: False)

        Returns:
            Dict with address and chain of the created wallet.

        Example:
            await client.gateway.create_wallet(
                chain='solana',
                set_default=True
            )
        """
        wallet_data = {
            "chain": chain,
            "set_default": set_default
        }
        return await self._post("/gateway/wallets/create", json=wallet_data)

    async def show_private_key(
        self,
        chain: str,
        address: str,
        passphrase: str
    ) -> Dict[str, Any]:
        """
        Show private key for a wallet.

        WARNING: This endpoint exposes sensitive information. Use with caution.

        Args:
            chain: Blockchain chain (e.g., 'solana', 'ethereum')
            address: Wallet address
            passphrase: Gateway passphrase for decryption

        Returns:
            Dict with privateKey field.

        Example:
            await client.gateway.show_private_key(
                chain='solana',
                address='<wallet-address>',
                passphrase='<gateway-passphrase>'
            )
        """
        request_data = {
            "chain": chain,
            "address": address,
            "passphrase": passphrase
        }
        return await self._post("/gateway/wallets/show-private-key", json=request_data)

    async def send_transaction(
        self,
        chain: str,
        network: str,
        address: str,
        to_address: str,
        amount: str
    ) -> Dict[str, Any]:
        """
        Send a native token transaction.

        Args:
            chain: Blockchain chain (e.g., 'solana', 'ethereum')
            network: Network name (e.g., 'mainnet-beta', 'mainnet')
            address: Sender wallet address
            to_address: Recipient wallet address
            amount: Amount to send as string (e.g., '0.001')

        Returns:
            Dict with transaction signature/hash.

        Example:
            await client.gateway.send_transaction(
                chain='solana',
                network='mainnet-beta',
                address='<sender-address>',
                to_address='<recipient-address>',
                amount='0.001'
            )
        """
        transaction_data = {
            "chain": chain,
            "network": network,
            "address": address,
            "to_address": to_address,
            "amount": amount
        }
        return await self._post("/gateway/wallets/send", json=transaction_data)