"""Synchronous wrapper for HummingbotAPIClient."""
import asyncio
from functools import wraps
from typing import Any, Callable, TypeVar, Optional, TYPE_CHECKING

from .client import HummingbotAPIClient

if TYPE_CHECKING:
    from .routers.accounts import AccountsRouter
    from .routers.archived_bots import ArchivedBotsRouter
    from .routers.backtesting import BacktestingRouter
    from .routers.bot_orchestration import BotOrchestrationRouter
    from .routers.connectors import ConnectorsRouter
    from .routers.controllers import ControllersRouter
    from .routers.docker import DockerRouter
    from .routers.market_data import MarketDataRouter
    from .routers.portfolio import PortfolioRouter
    from .routers.scripts import ScriptsRouter
    from .routers.trading import TradingRouter

T = TypeVar('T')


def sync_wrapper(async_func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to convert async methods to sync."""
    @wraps(async_func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(async_func(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


class SyncHummingbotAPIClient:
    """Synchronous wrapper for HummingbotAPIClient.
    
    This provides a synchronous interface to the async HummingbotAPIClient
    without modifying the original implementation.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        username: str = "admin",
        password: str = "admin",
        timeout: Optional[float] = None
    ):
        """Initialize the sync client with connection parameters.
        
        Args:
            base_url: The base URL of the Hummingbot API
            username: The username for authentication
            password: The password for authentication
            timeout: Optional timeout in seconds (defaults to 300 seconds)
        """
        self._base_url = base_url
        self._username = username
        self._password = password
        self._timeout = timeout
        self._async_client: Optional[HummingbotAPIClient] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._created_loop: bool = False

        # Type hints for dynamically created attributes
        if TYPE_CHECKING:
            self.accounts: AccountsRouter
            self.archived_bots: ArchivedBotsRouter
            self.backtesting: BacktestingRouter
            self.bot_orchestration: BotOrchestrationRouter
            self.connectors: ConnectorsRouter
            self.controllers: ControllersRouter
            self.docker: DockerRouter
            self.market_data: MarketDataRouter
            self.portfolio: PortfolioRouter
            self.scripts: ScriptsRouter
            self.trading: TradingRouter

    def __enter__(self) -> 'SyncHummingbotAPIClient':
        """Enter context manager and initialize the async client."""
        # Check if there's already a running event loop
        try:
            self._loop = asyncio.get_running_loop()
            self._created_loop = False
        except RuntimeError:
            # No running loop, create a new one
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._created_loop = True

        # Create and initialize the async client
        import aiohttp
        timeout_obj = aiohttp.ClientTimeout(total=self._timeout) if self._timeout else None
        self._async_client = HummingbotAPIClient(
            self._base_url,
            self._username,
            self._password,
            timeout=timeout_obj
        )

        # Initialize based on whether we created the loop
        if self._created_loop:
            self._loop.run_until_complete(self._async_client.init())
        else:
            # For existing loop, schedule coroutine as a task
            import concurrent.futures
            future = concurrent.futures.Future()

            async def init_wrapper():
                try:
                    await self._async_client.init()
                    future.set_result(None)
                except Exception as e:
                    future.set_exception(e)

            asyncio.run_coroutine_threadsafe(init_wrapper(), self._loop)
            future.result()  # Wait for completion

        # Dynamically create sync wrappers for all routers
        self._wrap_routers()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and cleanup resources."""
        if self._async_client:
            if self._created_loop:
                self._loop.run_until_complete(self._async_client.close())
            else:
                # For existing loop, use run_coroutine_threadsafe
                import concurrent.futures
                future = concurrent.futures.Future()

                async def close_wrapper():
                    try:
                        await self._async_client.close()
                        future.set_result(None)
                    except Exception as e:
                        future.set_exception(e)

                asyncio.run_coroutine_threadsafe(close_wrapper(), self._loop)
                future.result()  # Wait for completion

        if self._created_loop and self._loop:
            self._loop.close()

    def _wrap_routers(self):
        """Dynamically wrap all router methods to be synchronous."""
        # List of router attributes on the async client
        router_attrs = [
            'accounts', 'archived_bots', 'backtesting', 'bot_orchestration',
            'connectors', 'controllers', 'docker', 'market_data',
            'portfolio', 'scripts', 'trading'
        ]

        for router_name in router_attrs:
            if hasattr(self._async_client, router_name):
                async_router = getattr(self._async_client, router_name)
                sync_router = SyncRouterWrapper(async_router, self._loop, self._created_loop)
                setattr(self, router_name, sync_router)


class SyncRouterWrapper:
    """Wrapper that converts async router methods to sync."""

    def __init__(self, async_router: Any, loop: asyncio.AbstractEventLoop, created_loop: bool):
        self._async_router = async_router
        self._loop = loop
        self._created_loop = created_loop

    def __getattr__(self, name: str) -> Any:
        """Dynamically wrap async methods to be synchronous."""
        attr = getattr(self._async_router, name)

        if asyncio.iscoroutinefunction(attr):
            def sync_method(*args, **kwargs):
                if self._created_loop:
                    # We created the loop, so we can use run_until_complete
                    return self._loop.run_until_complete(attr(*args, **kwargs))
                else:
                    # Using existing loop, must use run_coroutine_threadsafe
                    import concurrent.futures
                    future = concurrent.futures.Future()

                    async def wrapper():
                        try:
                            result = await attr(*args, **kwargs)
                            future.set_result(result)
                        except Exception as e:
                            future.set_exception(e)

                    asyncio.run_coroutine_threadsafe(wrapper(), self._loop)
                    return future.result()
            return sync_method
        
        return attr
