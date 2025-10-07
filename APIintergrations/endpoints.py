from sys import path_hooks

import requests
import asyncio
from urllib.parse import unquote, quote_plus
import re
import aiohttp

class MainAPI:
    url = 'https://portals-market.com/api/'
    HEADERS = {
            "Authorization": "",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
            "Origin": "https://portals-market.com",
            "Referer": "https://portals-market.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
        }

    def cap(self, text) -> str:
        words = re.findall(r"\w+(?:'\w+)?", text)
        for word in words:
            if len(word) > 0:
                cap = word[0].upper() + word[1:]
                text = text.replace(word, cap, 1)
        return text

    def listToURL(self, gifts: list) -> str:
        return '%2C'.join(quote_plus(self.cap(gift)) for gift in gifts)

class Getter(MainAPI):

    async def minimalGifts(self, authData):
        URL = self.url + "collections/floors"


        self.HEADERS["Authorization"] = authData
        async with aiohttp.ClientSession() as session:
            async with session.get(URL, headers=self.HEADERS) as response:
                response_data = await response.json()

        return response_data['floorPrices'] if response_data['floorPrices'] else None

    async def search(self, authData, name, model):
        if model:
            URL = self.url + "nfts/" + "search?" + f"offset={0}" + f"&limit={20}" + f"&sort_by=price+asc" + f"&filter_by_collections={quote_plus(self.cap(name))}" + f"&filter_by_models={self.listToURL(model)}"
        else:
            URL = self.url + "nfts/" + "search?" + f"offset={0}" + f"&limit={20}" + f"&sort_by=price+asc" + f"&filter_by_collections={quote_plus(self.cap(name))}"
        self.HEADERS["Authorization"] = authData
        async with aiohttp.ClientSession() as session:
            async with session.get(URL, headers=self.HEADERS) as response:
                response_data = await response.json()
        return response_data['results']


    async def transfer(self, authData, nft_id, recipient_id):
        URL = self.url+"nfts/transfer-gifts"

        self.HEADERS["Authorization"] = authData

        PAYLOAD = {
            "nft_ids": [nft_id],
            "recipient": recipient_id,
            "anonymous": False
        }
        async with aiohttp.ClientSession() as session:

            async with session.post(URL, headers=self.HEADERS, json=PAYLOAD) as response:
                response_data = await response.json()

        return {"message": 200}

    async def buy_gift(self, auth_data, nft_id, price):
        URL = self.url + "nfts"

        self.HEADERS = {
            "Authorization": auth_data,
            "Content-Type": "application/json"
        }

        nfts = [{"id": nft_id, "price": str(price)}]
        PAYLOAD = {"nft_details": nfts}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(URL, headers=self.HEADERS, json=PAYLOAD) as response:
                    response_data = await response.json()
                    print(response_data, PAYLOAD)
                    if (response_data.get('purchase_results', [{}])[0].get('status') == 'failed' and
                            response_data.get('purchase_results', [{}])[0].get('reason') != "NFT_NOT_LISTED"):

                        new_price = response_data['purchase_results'][0]['nft']['price']
                        nfts = [{"id": nft_id, "price": str(new_price)}]
                        payload = {"nft_details": nfts}

                        # Повторный запрос с новой ценой
                        async with session.post(URL, headers=self.HEADERS, json=PAYLOAD) as retry_response:
                            retry_data = await retry_response.json()

                            if retry_data.get('purchase_results', [{}])[0].get('status') == 'success':
                                return {"message": 200}
                            else:
                                return {"message": 500}

                    # Если первый запрос успешен
                    elif response_data.get('purchase_results', [{}])[0].get('status') == 'success':
                        return {"message": 200}
                    else:
                        return {"message": 500}

            except Exception as e:
                print(f"Error during NFT purchase: {e}")
                return {"message": 500}

    async def sale_gift_endp(self, authData, nft_id, price):
        URL = self.url + "nfts/bulk-list"

        self.HEADERS["Authorization"] = authData
        nfts = [{"nft_id": nft_id, "price": str(price)}]

        PAYLOAD = {
            "nft_prices": nfts
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(URL, headers=self.HEADERS, json=PAYLOAD) as response:
                response_data = await response.json()
