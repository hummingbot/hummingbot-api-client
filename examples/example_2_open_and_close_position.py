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


async def open_and_close_a_position(hbot_client: HummingbotAPIClient, interval: int):
    # 1: Set position mode HEDGE
    await hbot_client.trading.set_position_mode(account_name="master_account", connector_name="binance_perpetual",
                                                position_mode="HEDGE")
    await asyncio.sleep(0.5)

    # 2: Set leverage to 75x
    await hbot_client.trading.set_leverage(account_name="master_account", connector_name="binance_perpetual",
                                           trading_pair="ERA-USDT", leverage=75)
    await asyncio.sleep(0.5)


    # 3: Convert 100 USDT to ERA
    price = await hbot_client.market_data.get_prices(connector_name="binance_perpetual", trading_pairs="ERA-USDT")
    amount_in_era = 100 / price["prices"]["ERA-USDT"]

    # 4: Open a long position on ERA-USDT on Binance perpetual with 100 USDT
    await hbot_client.trading.place_order(
        account_name="master_account",
        connector_name="binance_perpetual",
        trading_pair="ERA-USDT",
        order_type="MARKET",
        side="BUY",
        amount=amount_in_era,
        position_action="OPEN",
    )
    await asyncio.sleep(interval)
    # 5: Open a short position on ERA-USDT on Binance perpetual with 100 USDT
    await hbot_client.trading.place_order(
        account_name="master_account",
        connector_name="binance_perpetual",
        trading_pair="ERA-USDT",
        order_type="MARKET",
        side="SELL",
        amount=amount_in_era,
        position_action="OPEN",
    )
    await asyncio.sleep(interval)
    # 7: Print the current positions
    positions = await hbot_client.trading.get_positions()
    logging.info(f"Current positions: {positions}")
    # 8: Close the long position
    await hbot_client.trading.place_order(
        account_name="master_account",
        connector_name="binance_perpetual",
        trading_pair="ERA-USDT",
        order_type="MARKET",
        side="SELL",
        amount=amount_in_era,
        position_action="CLOSE",
    )
    await asyncio.sleep(interval)
    # 9: Close the short position
    await hbot_client.trading.place_order(
        account_name="master_account",
        connector_name="binance_perpetual",
        trading_pair="ERA-USDT",
        order_type="MARKET",
        side="BUY",
        amount=amount_in_era,
        position_action="CLOSE",
    )




async def main():
    hbot_client = HummingbotAPIClient()
    await hbot_client.init()
    await open_and_close_a_position(hbot_client, interval=10)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())