import asyncio

from fastapi import APIRouter, HTTPException, Depends, Request

from utils.roulette_manager import spin_exchanger

router = APIRouter()


@router.post("/spin")
async def spin_roullete(id, credentinals: Request):
    return await asyncio.create_task(spin_exchanger(id='9090', balance=90008080, roullete_id=id))
