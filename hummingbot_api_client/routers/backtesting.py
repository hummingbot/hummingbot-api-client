from typing import Optional, Dict, Any, List
from .base import BaseRouter


class BacktestingRouter(BaseRouter):
    """Backtesting router for running backtesting simulations."""
    
    async def run_backtesting(self, backtesting_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run a backtesting simulation with the provided configuration."""
        return await self._post("/backtesting/run-backtesting", json=backtesting_config)