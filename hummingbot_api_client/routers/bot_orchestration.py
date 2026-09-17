from typing import Optional, Dict, Any, List
from .base import BaseRouter


class BotOrchestrationRouter(BaseRouter):
    """Bot Orchestration router for bot lifecycle management and MQTT operations."""

    # Bot Status Operations
    async def get_active_bots_status(self) -> Dict[str, Any]:
        """Get the status of all active bots."""
        return await self._get("/bot-orchestration/status")

    async def get_bot_status(self, bot_name: str) -> Dict[str, Any]:
        """Get the status of a specific bot including performance, logs, and activity."""
        return await self._get(f"/bot-orchestration/{bot_name}/status")

    async def get_bot_history(
            self,
            bot_name: str,
            days: int = 0,
            verbose: bool = False,
            precision: Optional[int] = None,
            timeout: float = 30.0
    ) -> Dict[str, Any]:
        """Get trading history for a bot with optional parameters."""
        params = {
            "days": days,
            "verbose": verbose,
            "timeout": timeout
        }
        if precision is not None:
            params["precision"] = precision
        return await self._get(f"/bot-orchestration/{bot_name}/history", params=params)

    # Bot Control Operations
    async def start_bot(
            self,
            bot_name: str,
            log_level: Optional[str] = None,
            script: Optional[str] = None,
            conf: Optional[str] = None,
            is_quickstart: bool = False,
            async_backend: bool = True
    ) -> Dict[str, Any]:
        """
        Start a bot with the specified configuration.

        Args:
            bot_name: Name of the bot instance to start
            log_level: Logging level ("DEBUG", "INFO", "WARNING", "ERROR")
            script: Script name to run (without .py extension)
            conf: Configuration file name (without .yml extension)
            is_quickstart: Whether to run in quickstart mode
            async_backend: Whether to run in async backend mode
        """
        start_bot_action = {
            "bot_name": bot_name,
            "is_quickstart": is_quickstart,
            "async_backend": async_backend
        }
        if log_level is not None:
            start_bot_action["log_level"] = log_level
        if script is not None:
            start_bot_action["script"] = script
        if conf is not None:
            start_bot_action["conf"] = conf

        return await self._post("/bot-orchestration/start-bot", json=start_bot_action)

    async def stop_bot(
            self,
            bot_name: str,
            skip_order_cancellation: bool = False,
            async_backend: bool = True
    ) -> Dict[str, Any]:
        """
        Stop a bot with the specified configuration.

        Args:
            bot_name: Name of the bot instance to stop
            skip_order_cancellation: Whether to skip cancelling open orders when stopping
            async_backend: Whether to run in async backend mode
        """
        stop_bot_action = {
            "bot_name": bot_name,
            "skip_order_cancellation": skip_order_cancellation,
            "async_backend": async_backend
        }
        return await self._post("/bot-orchestration/stop-bot", json=stop_bot_action)

    async def stop_and_archive_bot(
            self,
            bot_name: str,
            skip_order_cancellation: bool = True,
            archive_locally: bool = True,
            s3_bucket: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Gracefully stop a bot and archive its data in the background.

        Args:
            bot_name: Name of the bot instance to stop and archive
            skip_order_cancellation: Whether to skip cancelling open orders when stopping
            archive_locally: Whether to archive locally (True) or to S3 (False)
            s3_bucket: S3 bucket name for archiving (required if archive_locally=False)
        """
        url = f"/bot-orchestration/stop-and-archive-bot/{bot_name}"
        params = {
            "skip_order_cancellation": str(skip_order_cancellation).lower(),
            "archive_locally": str(archive_locally).lower()
        }
        if s3_bucket:
            params["s3_bucket"] = s3_bucket
        return await self._post(url, params=params)

    # Bot Deployment Operations
    async def deploy_v2_script(
            self,
            instance_name: str,
            credentials_profile: str,
            script: Optional[str] = None,
            script_config: Optional[str] = None,
            image: str = "hummingbot/hummingbot:latest"
    ) -> Dict[str, Any]:
        """
        Creates and autostart a v2 script with a configuration if present.

        Args:
            instance_name: Unique name for the bot instance
            credentials_profile: Name of the credentials profile to use
            script: Script name to run (without .py extension)
            script_config: Script configuration file name (without .yml extension)
            image: Docker image for the Hummingbot instance
        """
        script_deployment = {
            "instance_name": instance_name,
            "credentials_profile": credentials_profile,
            "image": image
        }
        if script is not None:
            script_deployment["script"] = script
        if script_config is not None:
            script_deployment["script_config"] = script_config

        return await self._post("/bot-orchestration/deploy-v2-script", json=script_deployment)

    async def deploy_v2_controllers(
            self,
            instance_name: str,
            credentials_profile: str,
            controllers_config: List[str],
            max_global_drawdown_quote: Optional[float] = None,
            max_controller_drawdown_quote: Optional[float] = None,
            image: str = "hummingbot/hummingbot:latest"
    ) -> Dict[str, Any]:
        """
        Deploy a V2 strategy with controllers.

        Args:
            instance_name: Unique name for the bot instance
            credentials_profile: Name of the credentials profile to use
            controllers_config: List of controller configuration files (without .yml extension)
            max_global_drawdown_quote: Maximum allowed global drawdown in quote asset
            max_controller_drawdown_quote: Maximum allowed per-controller drawdown in quote asset
            image: Docker image for the Hummingbot instance
        """
        controller_deployment = {
            "instance_name": instance_name,
            "credentials_profile": credentials_profile,
            "controllers_config": controllers_config,
            "image": image
        }
        if max_global_drawdown_quote is not None:
            controller_deployment["max_global_drawdown_quote"] = max_global_drawdown_quote
        if max_controller_drawdown_quote is not None:
            controller_deployment["max_controller_drawdown_quote"] = max_controller_drawdown_quote

        return await self._post("/bot-orchestration/deploy-v2-controllers", json=controller_deployment)

    # Controller Performance Operations
    async def get_controller_performance_history(
            self,
            bot_name: Optional[str] = None,
            controller_id: Optional[str] = None,
            limit: Optional[int] = None,
            cursor: Optional[str] = None,
            start_time: Optional[str] = None,
            end_time: Optional[str] = None,
            interval: str = "5m"
    ) -> Dict[str, Any]:
        """
        Get historical controller performance with pagination and interval sampling.

        Args:
            bot_name: Filter by bot name
            controller_id: Filter by controller ID
            limit: Maximum number of results to return
            cursor: Pagination cursor for next page
            start_time: Start time filter (ISO format)
            end_time: End time filter (ISO format)
            interval: Sampling interval (e.g., "5m", "1h", "1d")
        """
        params = {"interval": interval}
        if bot_name is not None:
            params["bot_name"] = bot_name
        if controller_id is not None:
            params["controller_id"] = controller_id
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time

        return await self._get("/bot-orchestration/controller-performance-history", params=params)

    async def get_latest_controller_performance(
            self,
            bot_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get the most recent performance snapshot for each bot/controller.

        Args:
            bot_name: Filter by bot name (optional)
        """
        params = {}
        if bot_name is not None:
            params["bot_name"] = bot_name
        return await self._get("/bot-orchestration/controller-performance-latest", params=params)

    # Bot Runs
    async def get_bot_runs(
            self,
            bot_name: Optional[str] = None,
            account_name: Optional[str] = None,
            strategy_type: Optional[str] = None,
            strategy_name: Optional[str] = None,
            run_status: Optional[str] = None,
            deployment_status: Optional[str] = None,
            limit: int = 100,
            offset: int = 0,
            include_final_status: bool = False
    ) -> Dict[str, Any]:
        """
        Get bot runs with optional filtering.

        Args:
            bot_name: Filter by bot name
            account_name: Filter by account name
            strategy_type: Filter by strategy type (script or controller)
            strategy_name: Filter by strategy name
            run_status: Filter by run status (CREATED, RUNNING, STOPPED, ERROR)
            deployment_status: Filter by deployment status (DEPLOYED, FAILED, ARCHIVED)
            limit: Maximum number of results to return
            offset: Number of results to skip
            include_final_status: Include the final status snapshot in each run. Off by
                default because the blob can be ~89 KB per record (~99% of the payload);
                use get_bot_run() to fetch it for a single run.
        """
        params = {
            "limit": limit,
            "offset": offset,
            "include_final_status": str(include_final_status).lower()
        }
        if bot_name is not None:
            params["bot_name"] = bot_name
        if account_name is not None:
            params["account_name"] = account_name
        if strategy_type is not None:
            params["strategy_type"] = strategy_type
        if strategy_name is not None:
            params["strategy_name"] = strategy_name
        if run_status is not None:
            params["run_status"] = run_status
        if deployment_status is not None:
            params["deployment_status"] = deployment_status

        return await self._get("/bot-orchestration/bot-runs", params=params)

    async def get_bot_run(self, bot_run_id: int) -> Dict[str, Any]:
        """
        Get a single bot run by ID, including its final status snapshot.

        Args:
            bot_run_id: ID of the bot run
        """
        return await self._get(f"/bot-orchestration/bot-runs/{bot_run_id}")

    async def delete_bot_run(self, bot_run_id: int) -> Dict[str, Any]:
        """
        Delete a bot run record by ID.

        Args:
            bot_run_id: ID of the bot run to delete
        """
        return await self._delete(f"/bot-orchestration/bot-runs/{bot_run_id}")

    # Bot Rate Oracle Configuration
    async def get_rate_oracle_sources(self) -> List[str]:
        """
        List the rate oracle sources a bot can be configured with.

        This configures deployed bots, not the API's own pricing.
        """
        return await self._get("/bot-orchestration/rate-oracle/sources")

    async def get_rate_oracle_config(self, account_name: str = "master_account") -> Dict[str, Any]:
        """
        Get the rate oracle configuration that bots deployed with a credentials profile will use.

        Args:
            account_name: Credentials profile whose conf_client.yml to read

        Returns:
            account_name, rate_oracle_source ({name}), global_token
            ({global_token_name, global_token_symbol}) and available_sources
        """
        params = {"account_name": account_name}
        return await self._get("/bot-orchestration/rate-oracle/config", params=params)

    async def update_rate_oracle_config(
            self,
            account_name: str = "master_account",
            rate_oracle_source: Optional[str] = None,
            global_token_name: Optional[str] = None,
            global_token_symbol: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update the bot rate oracle source and/or global token in a credentials profile's conf_client.yml.

        Bots pick the change up on their next deploy (running bots keep their copied config).
        Changing master_account's global token also switches the API's own valuation quote token.
        Fields left as None are not changed.

        Args:
            account_name: Credentials profile whose conf_client.yml to update
            rate_oracle_source: Rate oracle source name (see get_rate_oracle_sources())
            global_token_name: Token to use as global quote (e.g., USDT, USD, BTC); must not be blank
            global_token_symbol: Symbol to display for the global token (e.g., "$")

        Returns:
            success, message and the updated config
        """
        params = {"account_name": account_name}
        update_request = {}
        if rate_oracle_source is not None:
            update_request["rate_oracle_source"] = {"name": rate_oracle_source}
        global_token = {}
        if global_token_name is not None:
            global_token["global_token_name"] = global_token_name
        if global_token_symbol is not None:
            global_token["global_token_symbol"] = global_token_symbol
        if global_token:
            update_request["global_token"] = global_token

        return await self._put("/bot-orchestration/rate-oracle/config", json=update_request, params=params)
