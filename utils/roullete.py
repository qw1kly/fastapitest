import secrets
import os
import time
import hashlib
from utils.weights import weights

async def do_a_spin(roulette_id):
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

    symbol_weights, symbol_weights_fr, symbol_weights_lst = weights[roulette_id]['symbol_weights'], weights[roulette_id]['symbol_weights_fr'], weights[roulette_id]['symbol_weights_lst']

    weighted_choices = []
    for symbol, weight in symbol_weights.items():
        weighted_choices.extend([symbol] * weight)

    weighted_choices_fr = []
    for symbol, weight in symbol_weights_fr.items():
        weighted_choices_fr.extend([symbol] * weight)


    weighted_choices_lst = []
    for symbol, weight in symbol_weights_lst.items():
        weighted_choices_lst.extend([symbol] * weight)


    results = []
    for i in range(3):
        row = []
        for j in range(3):
            byte_index = (i * 3 + j) % len(final_hash)
            byte_val = final_hash[byte_index]
            if i == 0:
                choice_index = byte_val % len(weighted_choices_fr)
                value = weighted_choices_fr[choice_index]
            elif i == 1:
                choice_index = byte_val % len(weighted_choices)
                value = weighted_choices[choice_index]
            elif i == 2:
                choice_index = byte_val % len(weighted_choices_lst)
                value = weighted_choices_lst[choice_index]
            row.append(value)
        results.append(row)

    return results


async def second_spin(weights_for_model, gift_name):
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
    for symbol, weight in weights_for_model[gift_name].items():
        weighted_choices.extend([symbol] * weight['weight'])
    byte_index = final_hash[0] % len(final_hash)
    byte_val = final_hash[byte_index]
    choice_index = byte_val % len(weighted_choices)
    value = weighted_choices[choice_index]

    return weights_for_model[gift_name][value]['models']



