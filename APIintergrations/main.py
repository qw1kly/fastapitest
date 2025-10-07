import asyncio
import aiohttp
from urllib.parse import unquote
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName, InputUser
from APIintergrations.config.config import keys

# Глобальный клиент (инициализируется один раз)
_client = None


def get_client():
    global _client
    if _client is None:
        _client = Client('main', api_id=28311789, api_hash="c655b9344e4e2f567bc2d4aae75ff1c5")
    return _client


async def get_auth_token():
    client = get_client()
    if not client.is_connected:
        await client.start()

    try:
        bot_entity = await client.get_users('portals')
        bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.raw.access_hash)
        peer = await client.resolve_peer('portals')
        bot_app = InputBotAppShortName(bot_id=bot, short_name='market')

        web_view = await client.invoke(
            RequestAppWebView(
                peer=peer,
                app=bot_app,
                platform="desktop",
            )
        )

        init_data = unquote(web_view.url.split('tgWebAppData=', 1)[1].split('&tgWebAppVersion', 1)[0])
        token = f'tma {init_data}'
        return token
    finally:
        # Не останавливаем клиент, чтобы переиспользовать
        pass


async def main():
    return await get_auth_token()


# Функция для корректного закрытия
async def close_client():
    global _client
    if _client and _client.is_connected:
        await _client.stop()

        _client = None
