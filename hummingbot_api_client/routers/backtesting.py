from typing import Optional, Dict, Any, Union, List
from .base import BaseRouter


class BacktestingRouter(BaseRouter):
    """Backtesting router for running backtesting simulations."""

    async def run(
        self,
        start_time: int,
        end_time: int,
        backtesting_resolution: str = "1m",
        trade_cost: float = 0.0006,
        config: Optional[Union[Dict[str, Any], str]] = None
    ) -> Dict[str, Any]:
        """Run a backtesting simulation synchronously (no storage).

        Args:
            start_time: Start timestamp for backtesting
            end_time: End timestamp for backtesting
            backtesting_resolution: Time resolution for backtesting (default: "1m")
            trade_cost: Trading cost/fee (default: 0.0006)
            config: Controller config dict or YAML file path string
        """
        payload = {
            "start_time": start_time,
            "end_time": end_time,
            "backtesting_resolution": backtesting_resolution,
            "trade_cost": trade_cost,
            "config": config or {}
        }
        return await self._post("/backtesting/run", json=payload)

    async def submit_task(
        self,
        start_time: int,
        end_time: int,
        backtesting_resolution: str = "1m",
        trade_cost: float = 0.0006,
        config: Optional[Union[Dict[str, Any], str]] = None
    ) -> Dict[str, Any]:
        """Submit a backtesting task to run in the background.

        Args:
            start_time: Start timestamp for backtesting
            end_time: End timestamp for backtesting
            backtesting_resolution: Time resolution for backtesting (default: "1m")
            trade_cost: Trading cost/fee (default: 0.0006)
            config: Controller config dict or YAML file path string

        Returns:
            Dict with task_id and status.
        """
        payload = {
            "start_time": start_time,
            "end_time": end_time,
            "backtesting_resolution": backtesting_resolution,
            "trade_cost": trade_cost,
            "config": config or {}
        }
        return await self._post("/backtesting/tasks", json=payload)

    async def list_tasks(self) -> List[Dict[str, Any]]:
        """List all backtesting tasks (summaries without results)."""
        return await self._get("/backtesting/tasks")

    async def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get a backtesting task by ID, including results if completed.

        Args:
            task_id: The task identifier.
        """
        return await self._get(f"/backtesting/tasks/{task_id}")

    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Cancel or delete a backtesting task.

        Args:
            task_id: The task identifier.
        """
        return await self._delete(f"/backtesting/tasks/{task_id}")
