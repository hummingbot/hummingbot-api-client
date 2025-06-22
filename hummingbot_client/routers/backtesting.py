from typing import Optional, Dict, Any
from .base import BaseRouter


class BacktestingRouter(BaseRouter):
    """Backtesting router for strategy backtesting functionality."""
    
    async def run_backtesting(
        self,
        config: Dict[str, Any],
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        backtesting_resolution: Optional[str] = None,
        trade_cost: Optional[float] = None
    ) -> Dict[str, Any]:
        """Run backtesting simulation.
        
        Args:
            config: Backtesting configuration object (required)
            start_time: Start timestamp (optional)
            end_time: End timestamp (optional)
            backtesting_resolution: Resolution for backtesting (optional)
            trade_cost: Trade cost percentage (optional)
        """
        request = {
            "config": config
        }
        if start_time:
            request["start_time"] = start_time
        if end_time:
            request["end_time"] = end_time
        if backtesting_resolution:
            request["backtesting_resolution"] = backtesting_resolution
        if trade_cost:
            request["trade_cost"] = trade_cost
        
        return await self._post("/backtesting/run-backtesting", json=request)
    
    # Convenience methods for common backtesting scenarios
    async def run_strategy_backtest(
        self,
        strategy_config: Dict[str, Any],
        start_date: str,
        end_date: str,
        resolution: str = "1m",
        trade_cost: float = 0.1
    ) -> Dict[str, Any]:
        """Run a strategy backtest with date strings.
        
        Args:
            strategy_config: Strategy configuration
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            resolution: Backtesting resolution (default: 1m)
            trade_cost: Trade cost percentage (default: 0.1%)
        """
        import datetime
        
        # Convert date strings to timestamps
        start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        start_timestamp = int(start_dt.timestamp() * 1000)
        end_timestamp = int(end_dt.timestamp() * 1000)
        
        return await self.run_backtesting(
            config=strategy_config,
            start_time=start_timestamp,
            end_time=end_timestamp,
            backtesting_resolution=resolution,
            trade_cost=trade_cost
        )