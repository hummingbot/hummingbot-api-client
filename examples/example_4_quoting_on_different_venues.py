from telegram import Bot
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


async def quoting_on_multiple_exchanges(hbot_client: HummingbotAPIClient, bot: Bot, chat_id: str, interval: int):
    while True:
        try:
            connectors_to_quote = ["binance", "okx", "bybit", "mexc"]
            trading_pair = "WLD-USDT"
            quote_volume = 200000.0
            tasks = [hbot_client.market_data.get_price_for_quote_volume(
                connector=connector, trading_pair=trading_pair, quote_volume=quote_volume, is_buy=True) for connector in connectors_to_quote]
            prices = await asyncio.gather(*tasks)
            message = f"📈 *Quoting on Multiple Exchanges*\n\n"
            for connector, price in zip(connectors_to_quote, prices):
                if price is not None:
                    message += f"🔗 Connector: *{connector}*\n"
                    message += f"💰 Quote Volume: `${quote_volume}`\n"
                    message += f"💵 Price: `${price['result_price']:.4f}`\n\n"
                else:
                    message += f"🔗 Connector: *{connector}* - No price data available\n\n"

            await bot.send_message(chat_id=chat_id, text=message)
            logging.info("message sent successfully")
        except Exception as e:
            logging.error(e)
        finally:
            await asyncio.sleep(interval)


async def main():
    # Replace with your bot token from @BotFather
    BOT_TOKEN = 'your-telegram-token'

    # Replace with the chat ID you want to send the message to
    CHAT_ID = 'your-chat-id'

    # Create the bot and send the message
    bot = Bot(token=BOT_TOKEN)
    hbot_client = HummingbotAPIClient()
    await hbot_client.init()
    await quoting_on_multiple_exchanges(hbot_client, bot, CHAT_ID, interval=5)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())