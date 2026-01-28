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
        body = {"executor_config": executor_config}
        if account_name is not None:
            body["account_name"] = account_name
        return await self._post("/executors/", json=body)

    async def search_executors(
        self,
        account_names: Optional[List[str]] = None,
        connector_names: Optional[List[str]] = None,
        trading_pairs: Optional[List[str]] = None,
        executor_types: Optional[List[str]] = None,
        status: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Search for executors with various filters.

        Args:
            account_names: List of account names to filter by
            connector_names: List of connector names to filter by
            trading_pairs: List of trading pairs to filter by
            executor_types: List of executor types to filter by
            status: Status to filter by
            cursor: Pagination cursor for fetching next page
            limit: Maximum number of results to return (default 50)

        Returns:
            Dict containing matching executors and pagination info

        Example:
            # Get all executors for specific accounts
            executors = await client.executors.search_executors(
                account_names=["master_account"]
            )

            # Get executors for specific trading pairs
            executors = await client.executors.search_executors(
                trading_pairs=["BTC-USDT", "ETH-USDT"],
                connector_names=["binance_perpetual"]
            )
        """
        filters = {"limit": limit}
        if account_names is not None:
            filters["account_names"] = account_names
        if connector_names is not None:
            filters["connector_names"] = connector_names
        if trading_pairs is not None:
            filters["trading_pairs"] = trading_pairs
        if executor_types is not None:
            filters["executor_types"] = executor_types
        if status is not None:
            filters["status"] = status
        if cursor is not None:
            filters["cursor"] = cursor

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
        body = {"keep_position": keep_position}
        return await self._post(f"/executors/{executor_id}/stop", json=body)

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
    async def get_available_executor_types(self) -> Dict[str, Any]:
        """
        Get list of available executor types.

        Returns:
            Dict containing executor type information

        Example:
            types = await client.executors.get_available_executor_types()
            # Returns: {"executor_types": [...]}
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
