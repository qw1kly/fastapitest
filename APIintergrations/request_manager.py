# request_manager.py
import asyncio
from APIintergrations.main import main
from APIintergrations.endpoints import Getter
from utils.gifts_collections import collection_roulette, collection_saper

class TokenUpdater:
    def __init__(self):
        self.token = None
        self.getter = Getter()
        self._lock = asyncio.Lock()

    async def update_token(self):
        async with self._lock:
            self.token = await main()


class PriceGetter(TokenUpdater):

    def __init__(self):
        super().__init__()
        self.names_1 = collection_roulette[1]
        self.names_2 = collection_roulette[2]
        self.names_3 = collection_roulette[3]
        self.names_4 = collection_roulette[4]
        self.names_5 = collection_roulette[5]
        self.names_6 = collection_roulette[6]
        self.names_7 = collection_roulette[7]
        self.names_8 = collection_roulette[8]
        self.names_9 = collection_roulette[9]

        self.names_saper_1 = collection_saper[1]
        self.names_saper_2 = collection_saper[2]
    async def price_getter(self):
        manager = self.getter

        if not self.token:
            await self.update_token()

        try:
            objects = await manager.minimalGifts(self.token)
        except Exception:
            await self.update_token()
            objects = await manager.minimalGifts(self.token)

        objects[''] = '0'
        price_1 = [objects.get(name, '0') for name in self.names_1]
        price_2 = [objects.get(name, '0') for name in self.names_2]
        price_3 = [objects.get(name, '0') for name in self.names_3]
        price_4 = [objects.get(name, '0') for name in self.names_4]
        price_5 = [objects.get(name, '0') for name in self.names_5]
        price_6 = [objects.get(name, '0') for name in self.names_6]
        price_7 = [objects.get(name, '0') for name in self.names_7]
        price_8 = [objects.get(name, '0') for name in self.names_8]
        price_9 = [objects.get(name, '0') for name in self.names_9]

        price_saper_1 = [objects.get(name, '0') for name in self.names_saper_1]
        price_saper_2 = [objects.get(name, '0') for name in self.names_saper_2]


        return {
            "roulette" : {
                1: {"price": price_1, "names": self.names_1, "price_per_spin": 0.1},
                2: {"price": price_2, "names": self.names_2, "price_per_spin": 0.5},
                3: {"price": price_3, "names": self.names_3, "price_per_spin": 1},
                4: {"price": price_4, "names": self.names_4, "price_per_spin": 2},
                5: {"price": price_5, "names": self.names_5, "price_per_spin": 5},
                6: {"price": price_6, "names": self.names_6, "price_per_spin": 10},
                7: {"price": price_7, "names": self.names_7, "price_per_spin": 25},
                8: {"price": price_8, "names": self.names_8, "price_per_spin": 50},
                9: {"price": price_9, "names": self.names_9, "price_per_spin": 0.2}
            },
            "saper" : {
                1: {"price": price_saper_1, "names": self.names_saper_1, "price_per_spin": 1},
                2: {"price": price_saper_2, "names": self.names_saper_2, "price_per_spin": 2}
            }
        }

    async def id_getter(self, name, model=None):
        if not self.token:
            await self.update_token()
        manager = self.getter
        creditinals = await manager.search(self.token, name, model)
        for i in range(len(creditinals)):
            result = creditinals[i]
            if result['status'] == "listed":
                return creditinals[i]['id'], name, creditinals[i]['price'], creditinals[i]['photo_url'], creditinals[i]['tg_id']

    async def current_item_getter(self, name, nft_id):
        if not self.token:
            await self.update_token()
        manager = self.getter
        creditinals = await manager.search(self.token, name)
        for i in range(len(creditinals)):
            if creditinals[i]["id"] == nft_id:
                return creditinals[i]['price']
        return creditinals[0]['price']

    async def buy_gift_to_withdraw(self, nft_id, price):
        if not self.token:
            await self.update_token()
        manager = self.getter
        creditinals = await manager.buy_gift(self.token, nft_id, price)
        if creditinals['message'] == 200:
            return True
        return False

    async def transfer_gift_to_winner(self, nft_id, user_id):
        if not self.token:
            await self.update_token()
        manager = self.getter
        creditinals = await manager.transfer(self.token, nft_id, user_id)
        if creditinals['message'] == 200:
            return True
        return False

    async def sale_gift(self, nft_id, price):
        if not self.token:
            await self.update_token()
        manager = self.getter
        asyncio.create_task(manager.sale_gift_endp(self.token, nft_id=nft_id, price=price))


    # from CRUD.pydantic_model import Gift
    # async def quick_change_buy(self, gift: Gift):
    #     if not self.token:
    #         await self.update_token()
    #     manager = self.getter
    #     quick_buy =

price_getter_instance = PriceGetter()
amount = []

async def main_price():
    while True:
        try:
            global amount
            amount = await price_getter_instance.price_getter()
            await asyncio.sleep(60)
        except Exception as e:
            await asyncio.sleep(10)
