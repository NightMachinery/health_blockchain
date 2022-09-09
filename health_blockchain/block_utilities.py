from .block import Block
from typing import List
from .crypto_utilities import hash_bytes


def block_hash(block: Block) -> bytes:
    block_without_sig = block_update(block, signatures=[])
    block_bytes = block_serialize(block_without_sig)
    return hash_bytes([block_bytes])


def block_sign(key_prv, block: Block) -> Block:
    block_without_sig = block_update(block, signatures=[])
    block_bytes = block_serialize(block_without_sig)

    signatures = block.signatures + [sign_bytes(key_prv, block_bytes)]
    return block_update(
        block,
        signatures=signatures,)


def block_sign_verify(key_pub, block: Block):
    block_without_sig = block_update(block, signatures=[])
    block_bytes = block_serialize(block_without_sig)

    for sign in block.signatures:
        if sign_verify(key_pub, sign, block_bytes):
            return True

    return False
