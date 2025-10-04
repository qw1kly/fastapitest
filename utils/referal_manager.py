import asyncio

from CRUD.create import register_referal_db
from CRUD.model import Referals
from CRUD.pydantic_model import Referal, User_Creds
from CRUD.read import user_getter, referal_getter


async def referal_state(creds: Referal):
    refers = str(creds.referal_id)
    new_usr = str(creds.child_id)
    if refers == new_usr:
        return False
    user_exist = await asyncio.create_task(user_getter(User_Creds(id=new_usr, balance=0)))
    if user_exist[-1]:
        return False
    referal_exists = await asyncio.create_task(referal_getter(Referal(referal_id=refers, child_id=new_usr)))
    if referal_exists:
        return False
    await register_referal_db(creds)