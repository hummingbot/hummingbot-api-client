from typing import Optional, Dict, Any, List
from .base import BaseRouter


class BacktestingRouter(BaseRouter):
    """Backtesting router for running backtesting simulations."""
    
    async def run_backtesting(
        self,
        start_time: int,
        end_time: int,
        backtesting_resolution: str = "1m",
        trade_cost: float = 0.0006,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Run a backtesting simulation with the provided configuration.
        
        Args:
            start_time: Start timestamp for backtesting
            end_time: End timestamp for backtesting
            backtesting_resolution: Time resolution for backtesting (default: "1m")
            trade_cost: Trading cost/fee (default: 0.0006)
            config: Additional configuration options
        """
        payload = {
            "start_time": start_time,
            "end_time": end_time,
            "backtesting_resolution": backtesting_resolution,
            "trade_cost": trade_cost,
            "config": config or {}
        }
        return await self._post("/backtesting/run-backtesting", json=payload)