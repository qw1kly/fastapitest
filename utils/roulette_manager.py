import asyncio
from APIintergrations.main import main
from CRUD.create import add_item, add_gift_to_basket
from CRUD.pydantic_model import User_Creds, Gift
from CRUD.update import update_balance
from utils.roullete import do_a_spin, second_spin
from utils.gifts_collections import collection_roulette, models_roulette
import time
import random
from fastapi import HTTPException

async def spin_exchanger(id, balance, roullete_id):
    from APIintergrations.request_manager import amount, price_getter_instance
    if roullete_id not in amount['roulette']:
        raise HTTPException(404)
    price = amount['roulette'][roullete_id]['price_per_spin']
    if balance < price:
        raise HTTPException(500)
    matrix_gpsh = await asyncio.create_task(do_a_spin(roulette_id=roullete_id))
    flag = False
    await asyncio.create_task(update_balance(User_Creds(id=id, balance=balance), price=price))
    if matrix_gpsh[1][0] == matrix_gpsh[1][1] and matrix_gpsh[1][1] == matrix_gpsh[1][2]:
        flag = True
        if roullete_id == 1 and matrix_gpsh[1][0] in [4, 5, 6]:
            return [matrix_gpsh, roullete_id]
        gift = collection_roulette[roullete_id][matrix_gpsh[1][0]-1]
        current_models = await second_spin(models_roulette, gift)
        gift_id, gift_name, gift_price, image_url, tg_id = await asyncio.create_task(price_getter_instance.id_getter(gift, current_models))
        asyncio.create_task(add_gift_to_basket(Gift(owner_id=id, nft_id=gift_id, gift_name=gift_name, image_url=image_url, gift_price=gift_price, timestamp=int(time.time()), tg_id=tg_id)))
        asyncio.create_task(price_getter_instance.buy_gift_to_withdraw(nft_id=gift_id, price=gift_price))
    casino = random.randint(1, 6)
    if casino == 1 and not(flag):
        if roullete_id == 1:
            which_gift = random.randint(1, 3)
            matrix_gpsh[1] = [which_gift, which_gift, matrix_gpsh[1][2]]
            casino_full = random.randint(1, 2)
            if casino_full == 1:
                matrix_gpsh[2] = [matrix_gpsh[2][0], matrix_gpsh[2][1], which_gift]
            if matrix_gpsh[1][0] == matrix_gpsh[1][1] and matrix_gpsh[1][1] == matrix_gpsh[1][2]:
                indexes = [1, 2, 3]
                indexes.remove(which_gift)
                matrix_gpsh[1] = [which_gift, which_gift, indexes[random.randint(0, 2)]]
        else:
            which_gift = random.randint(1, 6)
            matrix_gpsh[1] = [which_gift, which_gift, matrix_gpsh[1][2]]
            casino_full = random.randint(1, 2)
            if casino_full == 1:
                matrix_gpsh[2] = [matrix_gpsh[2][0], matrix_gpsh[2][1], which_gift]
            if matrix_gpsh[1][0] == matrix_gpsh[1][1] and matrix_gpsh[1][1] == matrix_gpsh[1][2]:
                indexes = [1, 2, 3, 4, 5, 6]
                indexes.remove(which_gift)
                matrix_gpsh[1] = [which_gift, which_gift, indexes[random.randint(0, 4)]]
    return [matrix_gpsh, roullete_id]