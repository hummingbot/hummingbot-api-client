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
