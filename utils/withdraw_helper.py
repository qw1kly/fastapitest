import asyncio
from APIintergrations.request_manager import price_getter_instance
from CRUD.pydantic_model import Gift

async def make_rq(gift: Gift):

    transfer_ = await price_getter_instance.transfer_gift_to_winner(gift.nft_id, gift.owner_id)

    return {"message": "ok!"}