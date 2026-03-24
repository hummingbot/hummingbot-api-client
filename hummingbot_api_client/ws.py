import asyncio
import base64
import logging
from typing import Optional, Dict, Any, AsyncIterator, Callable, Awaitable

import aiohttp

logger = logging.getLogger(__name__)


class MarketDataWebSocket:
    """WebSocket client for streaming market data (order book, trades, candles).

    Usage::

        async with client.ws.market_data() as ws:
            await ws.subscribe_candles("binance_perpetual", "BTC-USDT", interval="1m")
            await ws.subscribe_order_book("binance_perpetual", "BTC-USDT", depth=10)
            await ws.subscribe_trades("binance_perpetual", "BTC-USDT")

            async for msg in ws:
                print(msg["type"], msg.get("subscription_id"))

                if msg["type"] == "candles":
                    print(f"  {len(msg['data'])} candle records")
                elif msg["type"] == "order_book":
                    print(f"  bids: {len(msg['data']['bids'])}")
    """

    def __init__(self, ws: aiohttp.ClientWebSocketResponse):
        self._ws = ws
        self._connection_id: Optional[str] = None

    @property
    def connection_id(self) -> Optional[str]:
        return self._connection_id

    @property
    def closed(self) -> bool:
        return self._ws.closed

    async def _send(self, msg: dict) -> None:
        await self._ws.send_json(msg)

    async def _receive(self) -> Dict[str, Any]:
        ws_msg = await self._ws.receive()
        if ws_msg.type == aiohttp.WSMsgType.TEXT:
            return ws_msg.json()
        elif ws_msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING):
            raise ConnectionError("WebSocket connection closed")
        elif ws_msg.type == aiohttp.WSMsgType.ERROR:
            raise ConnectionError(f"WebSocket error: {self._ws.exception()}")
        else:
            raise ConnectionError(f"Unexpected WebSocket message type: {ws_msg.type}")

    async def subscribe_candles(
        self,
        connector: str,
        trading_pair: str,
        interval: str = "1m",
        max_records: int = 100,
        update_interval: float = 1.0,
    ) -> str:
        """Subscribe to candle data.

        Args:
            connector: Exchange connector name (e.g. "binance_perpetual")
            trading_pair: Trading pair (e.g. "BTC-USDT")
            interval: Candle interval (e.g. "1m", "5m", "1h")
            max_records: Maximum number of candle records to receive
            update_interval: How often the server pushes updates (seconds)

        Returns:
            Subscription ID
        """
        msg = {
            "action": "subscribe",
            "type": "candles",
            "connector": connector,
            "trading_pair": trading_pair,
            "interval": interval,
            "max_records": max_records,
            "update_interval": update_interval,
        }
        await self._send(msg)
        resp = await self._receive()
        if resp.get("type") == "error":
            raise RuntimeError(f"Subscribe failed: {resp.get('message')}")
        return resp.get("subscription_id", "")

    async def subscribe_order_book(
        self,
        connector: str,
        trading_pair: str,
        depth: int = 10,
        update_interval: float = 1.0,
    ) -> str:
        """Subscribe to order book snapshots.

        Args:
            connector: Exchange connector name
            trading_pair: Trading pair
            depth: Number of price levels per side
            update_interval: How often the server pushes updates (seconds)

        Returns:
            Subscription ID
        """
        msg = {
            "action": "subscribe",
            "type": "order_book",
            "connector": connector,
            "trading_pair": trading_pair,
            "depth": depth,
            "update_interval": update_interval,
        }
        await self._send(msg)
        resp = await self._receive()
        if resp.get("type") == "error":
            raise RuntimeError(f"Subscribe failed: {resp.get('message')}")
        return resp.get("subscription_id", "")

    async def subscribe_trades(
        self,
        connector: str,
        trading_pair: str,
        update_interval: float = 1.0,
    ) -> str:
        """Subscribe to trade events.

        Args:
            connector: Exchange connector name
            trading_pair: Trading pair
            update_interval: How often the server pushes batched trades (seconds)

        Returns:
            Subscription ID
        """
        msg = {
            "action": "subscribe",
            "type": "trades",
            "connector": connector,
            "trading_pair": trading_pair,
            "update_interval": update_interval,
        }
        await self._send(msg)
        resp = await self._receive()
        if resp.get("type") == "error":
            raise RuntimeError(f"Subscribe failed: {resp.get('message')}")
        return resp.get("subscription_id", "")

    async def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from a subscription.

        Args:
            subscription_id: The subscription ID returned from subscribe_*
        """
        await self._send({
            "action": "unsubscribe",
            "subscription_id": subscription_id,
        })
        resp = await self._receive()
        if resp.get("type") == "error":
            raise RuntimeError(f"Unsubscribe failed: {resp.get('message')}")

    async def receive(self) -> Dict[str, Any]:
        """Receive the next message from the WebSocket.

        Returns a dict with at least a "type" field. Common types:
        - "candles": full candle history (on new candle)
        - "candle_update": live update to the current candle
        - "order_book": order book snapshot with bids/asks
        - "trades": batch of recent trades
        - "heartbeat": server keepalive
        - "error": error message
        """
        return await self._receive()

    def __aiter__(self) -> "MarketDataWebSocket":
        return self

    async def __anext__(self) -> Dict[str, Any]:
        try:
            return await self._receive()
        except ConnectionError:
            raise StopAsyncIteration

    async def close(self) -> None:
        """Close the WebSocket connection."""
        if not self._ws.closed:
            await self._ws.close()


class WebSocketRouter:
    """Manages WebSocket connections to the Hummingbot API."""

    def __init__(self, session: aiohttp.ClientSession, base_url: str, username: str, password: str):
        self._session = session
        self._base_url = base_url.rstrip("/")
        self._username = username
        self._password = password

    def _ws_url(self, path: str) -> str:
        base = self._base_url.replace("http://", "ws://").replace("https://", "wss://")
        return f"{base}/{path.lstrip('/')}"

    def _auth_token(self) -> str:
        return base64.b64encode(f"{self._username}:{self._password}".encode()).decode()

    def market_data(self) -> "_MarketDataWSContext":
        """Open a WebSocket connection for streaming market data.

        Usage::

            async with client.ws.market_data() as ws:
                await ws.subscribe_order_book("binance", "BTC-USDT")
                async for msg in ws:
                    print(msg)
        """
        return _MarketDataWSContext(self)

    async def _connect_market_data(self) -> MarketDataWebSocket:
        url = self._ws_url(f"/ws/market-data?token={self._auth_token()}")
        ws = await self._session.ws_connect(url)
        md_ws = MarketDataWebSocket(ws)
        # Wait for the "connected" message
        msg = await md_ws.receive()
        if msg.get("type") == "error":
            await ws.close()
            raise RuntimeError(f"WebSocket auth failed: {msg.get('message')}")
        md_ws._connection_id = msg.get("connection_id")
        return md_ws


class _MarketDataWSContext:
    """Async context manager for MarketDataWebSocket."""

    def __init__(self, router: WebSocketRouter):
        self._router = router
        self._ws: Optional[MarketDataWebSocket] = None

    async def __aenter__(self) -> MarketDataWebSocket:
        self._ws = await self._router._connect_market_data()
        return self._ws

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._ws:
            await self._ws.close()
