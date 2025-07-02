from typing import Optional, Dict, Any, List
from .base import BaseRouter


class BotOrchestrationRouter(BaseRouter):
    """Bot Orchestration router for bot lifecycle management and MQTT operations."""
    
    # Bot Status Operations
    async def get_active_bots_status(self) -> Dict[str, Any]:
        """Get the status of all active bots."""
        return await self._get("/bot-orchestration/status")
    
    async def get_mqtt_status(self) -> Dict[str, Any]:
        """Get MQTT connection status and discovered bots."""
        return await self._get("/bot-orchestration/mqtt")
    
    async def get_bot_status(self, bot_name: str) -> Dict[str, Any]:
        """Get the status of a specific bot."""
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
        async_backend: bool = False
    ) -> Dict[str, Any]:
        """
        Start a bot with the specified configuration.
        
        Args:
            bot_name: Name of the bot instance to start
            log_level: Logging level ("DEBUG", "INFO", "WARNING", "ERROR")
            script: Script name to run (without .py extension)
            conf: Configuration file name (without .yml extension)
            async_backend: Whether to run in async backend mode
            
        Returns:
            Dictionary with status and response from bot start operation
            
        Example:
            # Start a bot with default settings
            result = await client.bot_orchestration.start_bot("my_trading_bot")
            
            # Start a bot with specific script and config
            result = await client.bot_orchestration.start_bot(
                "my_bot", 
                log_level="INFO", 
                script="directional_strategy_v3", 
                conf="my_strategy_config"
            )
        """
        start_bot_action = {
            "bot_name": bot_name,
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
        async_backend: bool = False
    ) -> Dict[str, Any]:
        """
        Stop a bot with the specified configuration.
        
        Args:
            bot_name: Name of the bot instance to stop
            skip_order_cancellation: Whether to skip cancelling open orders when stopping
            async_backend: Whether to run in async backend mode
            
        Returns:
            Dictionary with status and response from bot stop operation
            
        Example:
            # Stop a bot and cancel open orders
            result = await client.bot_orchestration.stop_bot("my_trading_bot")
            
            # Stop a bot without cancelling orders
            result = await client.bot_orchestration.stop_bot(
                "my_bot", 
                skip_order_cancellation=True
            )
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
        
        This initiates a background task that will:
        1. Stop the bot trading process via MQTT
        2. Wait 15 seconds for graceful shutdown
        3. Monitor and stop the Docker container
        4. Archive the bot data (locally or to S3)
        5. Remove the container
        
        Returns immediately with a success message while the process continues in the background.
        
        Args:
            bot_name: Name of the bot instance to stop and archive
            skip_order_cancellation: Whether to skip cancelling open orders when stopping
            archive_locally: Whether to archive locally (True) or to S3 (False)
            s3_bucket: S3 bucket name for archiving (required if archive_locally=False)
            
        Returns:
            Dictionary with status and details about the background operation
            
        Example:
            # Stop and archive locally
            result = await client.bot_orchestration.stop_and_archive_bot("my_bot")
            
            # Stop and archive to S3
            result = await client.bot_orchestration.stop_and_archive_bot(
                "my_bot", 
                archive_locally=False, 
                s3_bucket="my-bot-archives"
            )
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
            
        Returns:
            Dictionary with creation response and instance details
            
        Example:
            # Deploy a simple script bot
            result = await client.bot_orchestration.deploy_v2_script(
                "my_trading_bot",
                "binance_credentials",
                script="directional_strategy_v3",
                script_config="my_strategy_config"
            )
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
        Deploy a V2 strategy with controllers by generating the script config and creating the instance.
        This endpoint simplifies the deployment process for V2 controller strategies.
        
        Args:
            instance_name: Unique name for the bot instance
            credentials_profile: Name of the credentials profile to use
            controllers_config: List of controller configuration files (without .yml extension)
            max_global_drawdown_quote: Maximum allowed global drawdown in quote asset (usually USDT)
            max_controller_drawdown_quote: Maximum allowed per-controller drawdown in quote asset
            image: Docker image for the Hummingbot instance
            
        Returns:
            Dictionary with deployment response and generated configuration details
            
        Example:
            # Deploy a controller-based strategy
            result = await client.bot_orchestration.deploy_v2_controllers(
                "my_controller_bot",
                "binance_credentials",
                ["market_maker_v1", "arbitrage_v2"],
                max_global_drawdown_quote=1000.0
            )
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
    
    # Convenience methods for common operations
    async def restart_bot(
        self,
        bot_name: str,
        skip_order_cancellation: bool = False
    ) -> Dict[str, Any]:
        """
        Restart a bot by stopping and then starting it again.
        
        Args:
            bot_name: Name of the bot instance to restart
            skip_order_cancellation: Whether to skip cancelling open orders when stopping
            
        Returns:
            Dictionary with restart operation results
            
        Example:
            result = await client.bot_orchestration.restart_bot("my_trading_bot")
        """
        # First stop the bot
        stop_result = await self.stop_bot(bot_name, skip_order_cancellation)
        
        if not stop_result.get("status") == "success":
            return {
                "status": "error",
                "message": "Failed to stop bot",
                "stop_result": stop_result
            }
        
        # Then start the bot
        start_result = await self.start_bot(bot_name)
        
        return {
            "status": "success" if start_result.get("status") == "success" else "error",
            "message": "Bot restarted successfully" if start_result.get("status") == "success" else "Failed to start bot after stopping",
            "stop_result": stop_result,
            "start_result": start_result
        }
    
    async def get_bot_performance(
        self,
        bot_name: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Get bot performance metrics for a specific time period.
        
        Args:
            bot_name: Name of the bot to get performance for
            days: Number of days to analyze (default: 7)
            
        Returns:
            Dictionary with performance metrics and trading history
            
        Example:
            # Get last 7 days performance
            performance = await client.bot_orchestration.get_bot_performance("my_bot")
            
            # Get last 30 days performance
            performance = await client.bot_orchestration.get_bot_performance("my_bot", 30)
        """
        # Get bot status for current metrics
        status = await self.get_bot_status(bot_name)
        
        # Get historical performance
        history = await self.get_bot_history(bot_name, days=days, verbose=True)
        
        return {
            "bot_name": bot_name,
            "period_days": days,
            "current_status": status,
            "trading_history": history,
            "timestamp": status.get("data", {}).get("timestamp") if status.get("status") == "success" else None
        }
    
    async def list_all_bots(self) -> Dict[str, Any]:
        """
        Get a comprehensive list of all bots including active, discovered, and MQTT status.
        
        Returns:
            Dictionary with all bot information
            
        Example:
            all_bots = await client.bot_orchestration.list_all_bots()
        """
        # Get active bots status
        active_status = await self.get_active_bots_status()
        
        # Get MQTT status and discovered bots
        mqtt_status = await self.get_mqtt_status()
        
        return {
            "active_bots": active_status,
            "mqtt_status": mqtt_status,
            "summary": {
                "total_active_bots": len(mqtt_status.get("data", {}).get("active_bots", [])) if mqtt_status.get("status") == "success" else 0,
                "total_discovered_bots": len(mqtt_status.get("data", {}).get("discovered_bots", [])) if mqtt_status.get("status") == "success" else 0,
                "mqtt_connected": mqtt_status.get("data", {}).get("mqtt_connected", False) if mqtt_status.get("status") == "success" else False
            }
        }