import asyncio

from fastapi import APIRouter, HTTPException, Depends, Request

from CRUD.delete import sell_gift, sell_all_gifts, last_spin
from CRUD.pydantic_model import User_Creds, Referal, RoulleteId, Gift, Webhook, Map, Invoice, StarsWebhook
from CRUD.read import user_getter, gifts_getter, get_open_games
from CRUD.update import delete_all_sessions_data, deposit_with_ton
from TonAPI.main import hash_identifier

from authentication.telegram_hash_parser import verify_telegram_hash
from starsPayment.authentication import equal
from starsPayment.link_generator import stars_payment
from starsPayment.stars_conventer import stars_to_ton_conventer
from starsPayment.tonRate_getter import tonRateHandler
from utils.referal_manager import referal_state
from utils.roulette_manager import spin_exchanger
from utils.saper_manager import saper_game_starter, open_current_cell

router = APIRouter()

@router.post("/auth")
async def get_users(credentinals: Request) -> tuple:
    boolie = await asyncio.create_task(verify_telegram_hash(credentinals.headers['x-telegram-init-data']))
    if boolie[0]:
        return boolie, (await asyncio.create_task(user_getter(User_Creds(id=boolie[0], balance=0))))[0], await gifts_getter(id=boolie[0])
    raise HTTPException(401)

@router.post("/referal")
async def referal_register(id_manager: Referal = Depends(referal_state)) -> dict:

    return {200: "ok"}


@router.post("/spin")
async def spin_roullete(id: RoulleteId, credentinals: Request):
    boolie = await asyncio.create_task(verify_telegram_hash(credentinals.headers['x-telegram-init-data']))
    if boolie[0]:
        balance = (await asyncio.create_task(user_getter(User_Creds(id=boolie[0], balance=0))))[0]
        return await asyncio.create_task(spin_exchanger(id=boolie[0], balance=balance, roullete_id=id.roullete_id))
    raise HTTPException(401)


@router.post("/second-spin")
async def second_roulette_spin(credentinals: Request):
    boolie = await asyncio.create_task(verify_telegram_hash(credentinals.headers['x-telegram-init-data']))
    if boolie[0]:
        return await last_spin(user_id=boolie[0])
    raise HTTPException(401)


@router.post("/sellgift")
async def current_gift(gift: Gift, credentinals: Request) -> dict:
    boolie = await asyncio.create_task(verify_telegram_hash(credentinals.headers['x-telegram-init-data']))
    if boolie[0] != gift.owner_id:
        raise HTTPException(401)
    if boolie[0]:
        return await sell_gift(gift=gift)
    raise HTTPException(401)


@router.post("/sellall")
async def all_gift(user: User_Creds, credentinals: Request):
    boolie = await asyncio.create_task(verify_telegram_hash(credentinals.headers['x-telegram-init-data']))
    if boolie[0] and boolie[0] == user.id:
        return await sell_all_gifts(user)
    raise HTTPException(401)


@router.post("/withdraw-gift")
async def withdraw_gift(gift: Gift, credentinals: Request):
    boolie = await asyncio.create_task(verify_telegram_hash(credentinals.headers['x-telegram-init-data']))
    if boolie[0] != gift.owner_id:
        raise HTTPException(401)
    if boolie[0]:
        return await sell_gift(gift, is_it_withdraw=True)
    raise HTTPException(401)


@router.post("/start-game")
async def start_game_saper(map_id: Map, credentinals: Request):
    boolie = await asyncio.create_task(verify_telegram_hash(credentinals.headers['x-telegram-init-data']))
    if boolie[0]:
        return await saper_game_starter(id=boolie[0], balance=(await user_getter(User_Creds(id=boolie[0], balance=0)))[0], map_id=map_id.map_id)
    raise HTTPException(401)


@router.post("/open-cell")
async def open_cell(credentinals: Request):
    boolie = await asyncio.create_task(verify_telegram_hash(credentinals.headers['x-telegram-init-data']))
    if boolie[0]:
        return await open_current_cell(id=boolie[0])
    raise HTTPException(401)

@router.post("/take-gifts")
async def take_gifts(credentinals: Request):
    boolie = await asyncio.create_task(verify_telegram_hash(credentinals.headers['x-telegram-init-data']))
    if boolie[0]:
        return await delete_all_sessions_data(user_id=boolie[0])
    raise HTTPException(401)


@router.post("/payment-stars")
async def deposit_with_stars(amount: Invoice):
    return {"message":stars_payment(amount)}


@router.post("/paymentwebhooker-89120aszopasdi1239asmcxdas09123lloalsdmcxzqwerty")
async def deposit(webhook: Webhook = Depends(hash_identifier)):
    return {"message": webhook}


@router.post("/paymentwebhooker-78546aszopasdi1239asmcxdas09123lloalsdmcxzqwerty")
async def stars_webhook(webhook: StarsWebhook = Depends(equal)):
    tonrate = await tonRateHandler()

    if type(tonrate['message']) == str:
        raise HTTPException(404)

    tonrate = tonrate['message']
    final_amount = await stars_to_ton_conventer(stars_amount=webhook.stars_amount, tonRate=tonrate)

    asyncio.create_task(deposit_with_ton(webhook.user_id, final_amount))