import logging

from hummingbot_api_client import HummingbotAPIClient

# Configure logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)

def create_grid_strategy_config(
    id: str,
    trading_pair: str,
    start_price: float,
    end_price: float,
    limit_price: float,
    side: int,  # 1 = long, -1 = short
) -> dict:
    return {
        "id": id,
        "controller_name": "grid_strike",
        "controller_type": "generic",
        "total_amount_quote": "1000",
        "manual_kill_switch": False,
        "candles_config": [],
        "initial_positions": [],
        "leverage": 50,
        "position_mode": "HEDGE",
        "connector_name": "binance_perpetual",
        "trading_pair": trading_pair,
        "side": side,
        "start_price": f"{start_price:.6f}",
        "end_price": f"{end_price:.6f}",
        "limit_price": f"{limit_price:.6f}",
        "min_spread_between_orders": "0.001",
        "min_order_amount_quote": "5",
        "max_open_orders": 3,
        "max_orders_per_batch": 1,
        "order_frequency": 3,
        "activation_bounds": 0.002,
        "keep_position": False,
        "triple_barrier_config": {
            "open_order_type": 3,
            "stop_loss": None,
            "stop_loss_order_type": 1,
            "take_profit": "0.0008",
            "take_profit_order_type": 3,
            "time_limit": None,
            "time_limit_order_type": 1,
            "trailing_stop": None,
        },
    }

def generate_aggressive_and_conservative_configs(candles, trading_pair, aggressive_side, conservative_side):
    def create_grid_strategy_config(
        id: str,
        trading_pair: str,
        start_price: float,
        end_price: float,
        limit_price: float,
        side: int,
    ) -> dict:
        return {
            "id": id,
            "controller_name": "grid_strike",
            "controller_type": "generic",
            "total_amount_quote": "1000",
            "manual_kill_switch": False,
            "candles_config": [],
            "initial_positions": [],
            "leverage": 50,
            "position_mode": "HEDGE",
            "connector_name": "binance_perpetual",
            "trading_pair": trading_pair,
            "side": side,
            "start_price": f"{start_price:.6f}",
            "end_price": f"{end_price:.6f}",
            "limit_price": f"{limit_price:.6f}",
            "min_spread_between_orders": "0.001",
            "min_order_amount_quote": "5",
            "max_open_orders": 3,
            "max_orders_per_batch": 1,
            "order_frequency": 3,
            "activation_bounds": 0.002,
            "keep_position": False,
            "triple_barrier_config": {
                "open_order_type": 3,
                "stop_loss": None,
                "stop_loss_order_type": 1,
                "take_profit": "0.0008",
                "take_profit_order_type": 3,
                "time_limit": None,
                "time_limit_order_type": 1,
                "trailing_stop": None,
            },
        }

    # Extract values from candles
    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    closes = [c["close"] for c in candles]

    # Aggressive (last 20 closes)
    aggressive_low = min(closes[-20:])
    aggressive_high = max(closes[-20:])
    aggressive_start = aggressive_low
    aggressive_end = aggressive_high
    aggressive_limit = (
        aggressive_start - 0.01 if aggressive_side == 1 else aggressive_end + 0.01
    )

    # Conservative (all lows/highs)
    conservative_low = min(lows)
    conservative_high = max(highs)
    conservative_start = conservative_low
    conservative_end = conservative_high
    conservative_limit = (
        conservative_start - 0.01 if conservative_side == 1 else conservative_end + 0.01
    )

    # Create both configs
    aggressive_config = create_grid_strategy_config(
        id="aggressive_grid",
        trading_pair=trading_pair,
        start_price=aggressive_start,
        end_price=aggressive_end,
        limit_price=aggressive_limit,
        side=aggressive_side,
    )

    conservative_config = create_grid_strategy_config(
        id="conservative_grid",
        trading_pair=trading_pair,
        start_price=conservative_start,
        end_price=conservative_end,
        limit_price=conservative_limit,
        side=conservative_side,
    )

    return aggressive_config, conservative_config

async def create_grid_configs_and_deploy_bot(hbot_client: HummingbotAPIClient, trading_pair: str, interval: int):
    candles = await hbot_client.market_data.get_candles(
        connector_name="binance_perpetual",
        trading_pair=trading_pair,
        interval="1m",
        max_records=60,
    )
    aggressive_config, conservative_config = generate_aggressive_and_conservative_configs(
        candles=candles,
        trading_pair=trading_pair,
        aggressive_side=1,  # Long
        conservative_side=2  # Short
    )
    await hbot_client.controllers.create_or_update_controller_config(
        config_name=aggressive_config["id"],
        config=aggressive_config
    )
    await hbot_client.controllers.create_or_update_controller_config(
        config_name=conservative_config["id"],
        config=conservative_config
    )
    available_configs = await hbot_client.controllers.list_controller_configs()
    logging.info(f"Available configs: {available_configs}")

    await hbot_client.bot_orchestration.deploy_v2_controllers(
        instance_name="double_grid_bot",
        credentials_profile="master_account",
        controllers_config=[
            aggressive_config["id"],
            conservative_config["id"]
        ],
    )
    while True:
        try:

            status = await hbot_client.bot_orchestration.get_active_bots_status()
            logging.info(f"Bot status: {status}")
            if status["status"] == "RUNNING":
                logging.info("Bot deployed and running successfully.")
                break
        except Exception as e:
            logging.error(f"Error checking bot status: {e}")
        await asyncio.sleep(interval)

async def main():
    hbot_client = HummingbotAPIClient()
    await hbot_client.init()
    trading_pair = "ERA-USDT"
    await create_grid_configs_and_deploy_bot(hbot_client, trading_pair, interval=5)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())