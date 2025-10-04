import secrets
import os
import time
import hashlib
import asyncio

async def generate_cell(weights):
    entropy_sources = [
        secrets.token_bytes(32),
        os.urandom(16),
        str(time.time_ns()).encode(),
        str(secrets.randbelow(1000000000)).encode(),
        str(os.getpid()).encode(),
        secrets.token_bytes(8)
    ]

    secrets.SystemRandom().shuffle(entropy_sources)
    combined_entropy = b''.join(entropy_sources)
    hash_result = hashlib.sha3_512(combined_entropy).digest()
    salt = secrets.token_bytes(8)
    final_hash = hashlib.sha3_256(hash_result + salt).digest()


    weighted_choices = []
    for symbol, weight in weights.items():
        weighted_choices.extend([symbol] * weight)


    byte_index = final_hash[0] % len(final_hash)
    byte_val = final_hash[byte_index]
    choice_index = byte_val % len(weighted_choices)
    value = weighted_choices[choice_index]


    return value

async def gift_picker(map_id):
    from APIintergrations.request_manager import amount
    from utils.weights import weights_for_saper

    objects = sorted(list(zip(list(map(float, amount['saper'][map_id]['price'])), amount['saper'][map_id]['names'])), key=lambda x: x[0])

    for i in range(1, 6):
        weights_for_saper[map_id][i]["gift_price"] = objects[i-1][0]
        weights_for_saper[map_id][i]['gift_name'] = objects[i-1][1]

    entropy_sources = [
        secrets.token_bytes(32),
        os.urandom(16),
        str(time.time_ns()).encode(),
        str(secrets.randbelow(1000000000)).encode(),
        str(os.getpid()).encode(),
        secrets.token_bytes(8)
    ]

    secrets.SystemRandom().shuffle(entropy_sources)
    combined_entropy = b''.join(entropy_sources)
    hash_result = hashlib.sha3_512(combined_entropy).digest()
    salt = secrets.token_bytes(8)
    final_hash = hashlib.sha3_256(hash_result + salt).digest()

    weighted_choices = []
    for symbol, weight in weights_for_saper[map_id].items():
        weighted_choices.extend([symbol] * weight['weight'])

    byte_index = final_hash[0] % len(final_hash)
    byte_val = final_hash[byte_index]
    choice_index = byte_val % len(weighted_choices)
    value = weighted_choices[choice_index]

    return value