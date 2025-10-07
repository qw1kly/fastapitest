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
    try:
        return "tma user=%7B%22id%22%3A7102670717%2C%22first_name%22%3A%22.%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22aze_official_01%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2F9xdU5r1S-B6ZuyON8OMPHr_TaTAYPF8zYBA4RKM0k3M4B_8JoC9MDJQ1PJsDTnYM.svg%22%7D&chat_instance=267653665114097988&chat_type=sender&auth_date=1759857755&signature=zeh9l35pYBn4TN17gJxJ995Qs3F7hICrwJElYkp2D_c95ZqlX31OA0jrrr-5pkuIEHbFNFDA81QDi48TGz0pCg&hash=9a587de458efbd50102e029526cfb909505bc51e96034a4a260b91647371b677"
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


