from fastapi import HTTPException
import asyncio

from CRUD.create import create_new_map
from CRUD.delete import delete_saper_game
from CRUD.update import update_balance, update_cells
from CRUD.read import user_getter, get_open_games, get_time_gifts
from CRUD.pydantic_model import User_Creds
from utils.saper import generate_cell


async def saper_game_starter(id, balance, map_id):
    if (await get_open_games(id=id)):
        raise HTTPException(500)
    from APIintergrations.request_manager import amount, price_getter_instance
    price_list = amount['saper']
    if map_id not in price_list:
        raise HTTPException(404)
    price_per_game = price_list[map_id]['price_per_spin']
    if price_per_game > balance:
        raise HTTPException(500)
    await asyncio.create_task(update_balance(User_Creds(id=id, balance=balance), price=price_per_game))
    await create_new_map(user_id=id, map_id=map_id)

    return {"message": 200}

async def open_current_cell(id):
    data = await get_open_games(id=id)
    if not(data):
        raise HTTPException(500)
    green, red, gift = data
    green_weight = 75 - (75 - green * 5)
    red_weight = 20 + ((15 - green) * 5)
    gift_weight = 5 + ((15 - green) - ((5 - gift) * 5)) if 5 + ((15 - green) - ((5 - gift) * 5)) >=0 else 0
    weights_for_cell = {
        -1: red_weight,
        0: green_weight,
        1: gift_weight
    }
    result = await generate_cell(weights_for_cell)

    opened_cell = None

    if result == -1:
        opened_cell = await delete_saper_game(id)
        from CRUD.delete import delete_all_time_gifts
        await delete_all_time_gifts(user_id=id)
    elif result == 0:
        opened_cell = await update_cells(id, is_green=True)
    if result == 1:
        opened_cell = await update_cells(id, is_gift=True)

    return opened_cell