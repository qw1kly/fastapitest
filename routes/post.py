import asyncio

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends, Request

from utils.roulette_manager import spin_exchanger

router = APIRouter()


class SpinRequest(BaseModel):
    roullete_id: int 
    
@router.post("/spin")
async def spin_roullete(roullete_id: SpinRequest, credentinals: Request):
    return await asyncio.create_task(spin_exchanger(id='9090', balance=90008080, roullete_id=roullete_id))



