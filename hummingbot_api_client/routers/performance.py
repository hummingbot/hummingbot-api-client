from typing import Dict, Any
from .base import BaseRouter


class PerformanceRouter(BaseRouter):
    """Performance router for performance analysis."""
    
    async def calculate_performance_results(
        self,
        executor_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate performance results from executor data.
        
        Args:
            executor_data: Executor data for performance calculation
        """
        return await self._post("/performance/results", json=executor_data)
    
    # Convenience methods for different types of performance analysis
    async def analyze_trading_performance(
        self,
        trades: list,
        initial_capital: float,
        start_time: int,
        end_time: int
    ) -> Dict[str, Any]:
        """Analyze trading performance from trade data.
        
        Args:
            trades: List of trade records
            initial_capital: Starting capital amount
            start_time: Analysis start timestamp
            end_time: Analysis end timestamp
        """
        executor_data = {
            "trades": trades,
            "initial_capital": initial_capital,
            "start_time": start_time,
            "end_time": end_time
        }
        return await self.calculate_performance_results(executor_data)
    
    async def analyze_bot_performance(
        self,
        bot_name: str,
        executor_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze performance for a specific bot.
        
        Args:
            bot_name: Name of the bot
            executor_data: Bot's executor data
        """
        enhanced_data = {
            "bot_name": bot_name,
            **executor_data
        }
        return await self.calculate_performance_results(enhanced_data)