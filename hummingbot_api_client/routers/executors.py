from typing import Optional, Dict, Any, List
from .base import BaseRouter


class ExecutorsRouter(BaseRouter):
    """Executors router for managing trading executors and position holds."""

    # Executor CRUD Operations
    async def create_executor(
        self,
        executor_config: Dict[str, Any],
        account_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new executor with the given configuration.

        Args:
            executor_config: Executor configuration dictionary
            account_name: Account to run the executor on (optional)

        Returns:
            Created executor information

        Example:
            executor = await client.executors.create_executor(
                {"type": "dca", "trading_pair": "BTC-USDT", ...},
                account_name="master_account"
            )
        """
        params = {}
        if account_name is not None:
            params["account_name"] = account_name
        body = {"executor_config": executor_config}
        return await self._post("/executors/", json=body, params=params if params else None)

    async def search_executors(
        self,
        executor_ids: Optional[List[str]] = None,
        controller_id: Optional[str] = None,
        executor_types: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
        is_active: Optional[bool] = None,
        is_archived: Optional[bool] = None,
        trading_pair: Optional[str] = None,
        connector_name: Optional[str] = None,
        account_name: Optional[str] = None,
        side: Optional[str] = None,
        start_time_from: Optional[int] = None,
        start_time_to: Optional[int] = None,
        end_time_from: Optional[int] = None,
        end_time_to: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Search for executors with various filters.

        Args:
            executor_ids: List of executor IDs to filter by
            controller_id: Controller ID to filter by
            executor_types: List of executor types to filter by
            statuses: List of statuses to filter by
            is_active: Filter by active status
            is_archived: Filter by archived status
            trading_pair: Trading pair to filter by
            connector_name: Connector name to filter by
            account_name: Account name to filter by
            side: Trade side to filter by ("buy" or "sell")
            start_time_from: Filter executors started after this timestamp
            start_time_to: Filter executors started before this timestamp
            end_time_from: Filter executors ended after this timestamp
            end_time_to: Filter executors ended before this timestamp

        Returns:
            List of matching executors

        Example:
            # Get all active executors
            executors = await client.executors.search_executors(is_active=True)

            # Get executors for a specific trading pair
            executors = await client.executors.search_executors(
                trading_pair="BTC-USDT",
                connector_name="binance_perpetual"
            )
        """
        filters = {}
        if executor_ids is not None:
            filters["executor_ids"] = executor_ids
        if controller_id is not None:
            filters["controller_id"] = controller_id
        if executor_types is not None:
            filters["executor_types"] = executor_types
        if statuses is not None:
            filters["statuses"] = statuses
        if is_active is not None:
            filters["is_active"] = is_active
        if is_archived is not None:
            filters["is_archived"] = is_archived
        if trading_pair is not None:
            filters["trading_pair"] = trading_pair
        if connector_name is not None:
            filters["connector_name"] = connector_name
        if account_name is not None:
            filters["account_name"] = account_name
        if side is not None:
            filters["side"] = side
        if start_time_from is not None:
            filters["start_time_from"] = start_time_from
        if start_time_to is not None:
            filters["start_time_to"] = start_time_to
        if end_time_from is not None:
            filters["end_time_from"] = end_time_from
        if end_time_to is not None:
            filters["end_time_to"] = end_time_to

        return await self._post("/executors/search", json=filters)

    async def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all executors.

        Returns:
            Summary statistics for executors

        Example:
            summary = await client.executors.get_summary()
        """
        return await self._get("/executors/summary")

    async def get_executor(self, executor_id: str) -> Dict[str, Any]:
        """
        Get a specific executor by ID.

        Args:
            executor_id: The executor ID to retrieve

        Returns:
            Executor details

        Example:
            executor = await client.executors.get_executor("exec_123")
        """
        return await self._get(f"/executors/{executor_id}")

    async def stop_executor(
        self,
        executor_id: str,
        keep_position: bool = False
    ) -> Dict[str, Any]:
        """
        Stop a running executor.

        Args:
            executor_id: The executor ID to stop
            keep_position: If True, keep the position open after stopping

        Returns:
            Stop operation result

        Example:
            # Stop and close position
            result = await client.executors.stop_executor("exec_123")

            # Stop but keep position open
            result = await client.executors.stop_executor("exec_123", keep_position=True)
        """
        params = {"keep_position": str(keep_position).lower()}
        return await self._post(f"/executors/{executor_id}/stop", json={}, params=params)

    async def delete_executor(self, executor_id: str) -> Dict[str, Any]:
        """
        Delete an executor.

        Args:
            executor_id: The executor ID to delete

        Returns:
            Delete operation result

        Example:
            result = await client.executors.delete_executor("exec_123")
        """
        return await self._delete(f"/executors/{executor_id}")

    # Position Hold Management
    async def get_positions_summary(self) -> Dict[str, Any]:
        """
        Get summary of all positions held by executors.

        Returns:
            Summary of held positions

        Example:
            summary = await client.executors.get_positions_summary()
        """
        return await self._get("/executors/positions/summary")

    async def get_position_held(
        self,
        connector_name: str,
        trading_pair: str,
        account_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get the position held for a specific connector and trading pair.

        Args:
            connector_name: Exchange connector name
            trading_pair: Trading pair (e.g., "BTC-USDT")
            account_name: Account name (optional)

        Returns:
            Position held information

        Example:
            position = await client.executors.get_position_held(
                "binance_perpetual", "BTC-USDT", "master_account"
            )
        """
        params = {}
        if account_name is not None:
            params["account_name"] = account_name
        return await self._get(
            f"/executors/positions/{connector_name}/{trading_pair}",
            params=params if params else None
        )

    async def clear_position_held(
        self,
        connector_name: str,
        trading_pair: str,
        account_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Clear the position held for a specific connector and trading pair.

        Args:
            connector_name: Exchange connector name
            trading_pair: Trading pair (e.g., "BTC-USDT")
            account_name: Account name (optional)

        Returns:
            Clear operation result

        Example:
            result = await client.executors.clear_position_held(
                "binance_perpetual", "BTC-USDT", "master_account"
            )
        """
        params = {}
        if account_name is not None:
            params["account_name"] = account_name
        return await self._delete(
            f"/executors/positions/{connector_name}/{trading_pair}",
            params=params if params else None
        )

    # Executor Types/Schema
    async def get_available_executor_types(self) -> List[str]:
        """
        Get list of available executor types.

        Returns:
            List of executor type names

        Example:
            types = await client.executors.get_available_executor_types()
            # Returns: ["dca", "grid", "twap", ...]
        """
        return await self._get("/executors/types/available")

    async def get_executor_config_schema(self, executor_type: str) -> Dict[str, Any]:
        """
        Get the configuration schema for a specific executor type.

        Args:
            executor_type: The executor type to get schema for

        Returns:
            JSON schema for the executor configuration

        Example:
            schema = await client.executors.get_executor_config_schema("dca")
        """
        return await self._get(f"/executors/types/{executor_type}/config")
