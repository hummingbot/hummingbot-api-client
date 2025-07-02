from typing import Optional
import aiohttp
from .routers import (
    AccountsRouter,
    ArchivedBotsRouter,
    BacktestingRouter,
    BotOrchestrationRouter,
    ConnectorsRouter,
    ControllersRouter,
    DockerRouter,
    MarketDataRouter,
    PortfolioRouter,
    ScriptsRouter,
    TradingRouter
)


class HummingbotAPIClient:
    def __init__(
        self, 
        base_url: str = "http://localhost:8000",
        username: str = "admin",
        password: str = "admin",
        timeout: Optional[aiohttp.ClientTimeout] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.auth = aiohttp.BasicAuth(username, password)
        # Increase default timeout for operations like historical candles
        self.timeout = timeout or aiohttp.ClientTimeout(total=300)  # 5 minutes
        self._session: Optional[aiohttp.ClientSession] = None
        self._accounts: Optional[AccountsRouter] = None
        self._archived_bots: Optional[ArchivedBotsRouter] = None
        self._backtesting: Optional[BacktestingRouter] = None
        self._bot_orchestration: Optional[BotOrchestrationRouter] = None
        self._connectors: Optional[ConnectorsRouter] = None
        self._controllers: Optional[ControllersRouter] = None
        self._docker: Optional[DockerRouter] = None
        self._market_data: Optional[MarketDataRouter] = None
        self._portfolio: Optional[PortfolioRouter] = None
        self._scripts: Optional[ScriptsRouter] = None
        self._trading: Optional[TradingRouter] = None
    
    async def init(self) -> None:
        """Initialize the client session and routers."""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                auth=self.auth,
                timeout=self.timeout
            )
            self._accounts = AccountsRouter(self._session, self.base_url)
            self._archived_bots = ArchivedBotsRouter(self._session, self.base_url)
            self._backtesting = BacktestingRouter(self._session, self.base_url)
            self._bot_orchestration = BotOrchestrationRouter(self._session, self.base_url)
            self._connectors = ConnectorsRouter(self._session, self.base_url)
            self._controllers = ControllersRouter(self._session, self.base_url)
            self._docker = DockerRouter(self._session, self.base_url)
            self._market_data = MarketDataRouter(self._session, self.base_url)
            self._portfolio = PortfolioRouter(self._session, self.base_url)
            self._scripts = ScriptsRouter(self._session, self.base_url)
            self._trading = TradingRouter(self._session, self.base_url)
    
    async def close(self) -> None:
        """Close the client session."""
        if self._session:
            await self._session.close()
            self._session = None
            self._accounts = None
            self._archived_bots = None
            self._backtesting = None
            self._bot_orchestration = None
            self._connectors = None
            self._controllers = None
            self._docker = None
            self._market_data = None
            self._portfolio = None
            self._scripts = None
            self._trading = None
    
    @property
    def accounts(self) -> AccountsRouter:
        """Access the accounts router."""
        if self._accounts is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._accounts
    
    @property
    def archived_bots(self) -> ArchivedBotsRouter:
        """Access the archived bots router."""
        if self._archived_bots is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._archived_bots
    
    @property
    def backtesting(self) -> BacktestingRouter:
        """Access the backtesting router."""
        if self._backtesting is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._backtesting
    
    @property
    def bot_orchestration(self) -> BotOrchestrationRouter:
        """Access the bot orchestration router."""
        if self._bot_orchestration is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._bot_orchestration
    
    @property
    def connectors(self) -> ConnectorsRouter:
        """Access the connectors router."""
        if self._connectors is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._connectors
    
    @property
    def controllers(self) -> ControllersRouter:
        """Access the controllers router."""
        if self._controllers is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._controllers
    
    @property
    def docker(self) -> DockerRouter:
        """Access the docker router."""
        if self._docker is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._docker
    
    @property
    def market_data(self) -> MarketDataRouter:
        """Access the market data router."""
        if self._market_data is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._market_data
    
    @property
    def portfolio(self) -> PortfolioRouter:
        """Access the portfolio router."""
        if self._portfolio is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._portfolio
    
    @property
    def scripts(self) -> ScriptsRouter:
        """Access the scripts router."""
        if self._scripts is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._scripts
    
    @property
    def trading(self) -> TradingRouter:
        """Access the trading router."""
        if self._trading is None:
            raise RuntimeError("Client not initialized. Call await client.init() first.")
        return self._trading
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.init()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()