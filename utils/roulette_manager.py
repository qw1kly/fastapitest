import asyncio
from utils.roullete import do_a_spin
import time
import random

async def spin_exchanger(id, balance, roullete_id):
    matrix_gpsh = await asyncio.create_task(do_a_spin(roulette_id=roullete_id))
    flag = False
    if matrix_gpsh[1][0] == matrix_gpsh[1][1] and matrix_gpsh[1][1] == matrix_gpsh[1][2]:
        flag = True
        if roullete_id == 1 and matrix_gpsh[1][0] in [4, 5, 6]:
            return [matrix_gpsh, roullete_id]
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
