from typing import Optional
import aiohttp
from .routers import (
    AccountsRouter,
    MarketsRouter,
    TradingRouter,
    DockerRouter,
    BotOrchestrationRouter,
    ControllersRouter,
    ScriptsRouter,
    DatabasesRouter,
    BacktestingRouter,
    PerformanceRouter
)


class HummingbotClient:
    def __init__(
        self, 
        base_url: str,
        username: str = "admin",
        password: str = "admin",
        timeout: Optional[aiohttp.ClientTimeout] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.auth = aiohttp.BasicAuth(username, password)
        self.timeout = timeout or aiohttp.ClientTimeout(total=30)
        self._session: Optional[aiohttp.ClientSession] = None
        self._accounts: Optional[AccountsRouter] = None
        self._markets: Optional[MarketsRouter] = None
        self._trading: Optional[TradingRouter] = None
        self._docker: Optional[DockerRouter] = None
        self._bot_orchestration: Optional[BotOrchestrationRouter] = None
        self._controllers: Optional[ControllersRouter] = None
        self._scripts: Optional[ScriptsRouter] = None
        self._databases: Optional[DatabasesRouter] = None
        self._backtesting: Optional[BacktestingRouter] = None
        self._performance: Optional[PerformanceRouter] = None
    
    async def init(self) -> None:
        """Initialize the client session and routers."""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                auth=self.auth,
                timeout=self.timeout
            )
            self._accounts = AccountsRouter(self._session, self.base_url)
            self._markets = MarketsRouter(self._session, self.base_url)
            self._trading = TradingRouter(self._session, self.base_url)
            self._docker = DockerRouter(self._session, self.base_url)
            self._bot_orchestration = BotOrchestrationRouter(self._session, self.base_url)
            self._controllers = ControllersRouter(self._session, self.base_url)
            self._scripts = ScriptsRouter(self._session, self.base_url)
            self._databases = DatabasesRouter(self._session, self.base_url)
            self._backtesting = BacktestingRouter(self._session, self.base_url)
            self._performance = PerformanceRouter(self._session, self.base_url)
    
    async def close(self) -> None:
        """Close the client session."""
        if self._session:
            await self._session.close()
            self._session = None
            self._accounts = None
            self._markets = None
            self._trading = None
            self._docker = None
            self._bot_orchestration = None
            self._controllers = None
            self._scripts = None
            self._databases = None
            self._backtesting = None
            self._performance = None
    
    @property
    def accounts(self) -> AccountsRouter:
        """Access the accounts router."""
        if self._accounts is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._accounts
    
    @property
    def markets(self) -> MarketsRouter:
        """Access the markets router."""
        if self._markets is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._markets
    
    @property
    def trading(self) -> TradingRouter:
        """Access the trading router."""
        if self._trading is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._trading
    
    @property
    def docker(self) -> DockerRouter:
        """Access the docker router."""
        if self._docker is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._docker
    
    @property
    def bot_orchestration(self) -> BotOrchestrationRouter:
        """Access the bot orchestration router."""
        if self._bot_orchestration is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._bot_orchestration
    
    @property
    def controllers(self) -> ControllersRouter:
        """Access the controllers router."""
        if self._controllers is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._controllers
    
    @property
    def scripts(self) -> ScriptsRouter:
        """Access the scripts router."""
        if self._scripts is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._scripts
    
    @property
    def databases(self) -> DatabasesRouter:
        """Access the databases router."""
        if self._databases is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._databases
    
    @property
    def backtesting(self) -> BacktestingRouter:
        """Access the backtesting router."""
        if self._backtesting is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._backtesting
    
    @property
    def performance(self) -> PerformanceRouter:
        """Access the performance router."""
        if self._performance is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._performance
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.init()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()