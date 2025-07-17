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


async def periodic_portfolio_update_task(hbot_client: HummingbotAPIClient, bot: Bot, chat_id: str, interval: int):
    while True:
        try:
            portfolio_state = await hbot_client.portfolio.get_state()

            master_account = portfolio_state.get('master_account', {})

            lines = ["📊 *Periodic Portfolio Update*"]

            for exchange, assets in master_account.items():
                lines.append(f"\n🔁 Exchange: *{exchange}*")
                for asset in assets:
                    token = asset.get("token")
                    units = asset.get("units", 0)
                    available = asset.get("available_units", 0)
                    value = asset.get("value", 0)
                    price = asset.get("price", 0)

                    lines.append(
                        f"  • Token: `{token}`\n"
                        f"    • Units: `{units:,.4f}`\n"
                        f"    • Available: `{available:,.4f}`\n"
                        f"    • Price: `${price:.2f}`\n"
                        f"    • Value: `${value:,.2f}`"
                    )

            message = "\n".join(lines)
            await bot.send_message(chat_id=chat_id, text=message)
            await asyncio.sleep(interval)
            logging.info("message sent successfully")
        except Exception as e:
            logging.error(e)


async def main():
    # Replace with your bot token from @BotFather
    BOT_TOKEN = 'your-tg-token'

    # Replace with the chat ID you want to send the message to
    CHAT_ID = 'your-chat-id'

    # Create the bot and send the message
    bot = Bot(token=BOT_TOKEN)
    hbot_client = HummingbotAPIClient()
    await hbot_client.init()
    await periodic_portfolio_update_task(hbot_client, bot, CHAT_ID, interval=5)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())