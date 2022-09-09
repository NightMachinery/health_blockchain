from .block import Block, block_update
from typing import List
from .crypto_utilities import hash_bytes, sign_bytes, sign_verify
from . import serialization
from icecream import ic


def block_hash(block: Block) -> bytes:
    block_bytes = block_serialize_for_sig(block)

    return hash_bytes([block_bytes])


def block_sign(key_prv, block: Block) -> Block:
    block_bytes = block_serialize_for_sig(block)

    signatures = block.signatures + [sign_bytes(key_prv, block_bytes)]
    return block_update(
        block,
        signatures=signatures,
    )


def block_serialize_for_sig(block: Block) -> Block:
    block_without_sig = block_update(block, signatures=[])
    block_bytes = serialization.block_serialize(block_without_sig)
    return block_bytes


def block_sign_verify(key_pub, block: Block):
    block_bytes = block_serialize_for_sig(block)

    for sign in block.signatures:
        if sign_verify(key_pub, sign, block_bytes):
            return True

    return False


def block_sign_verify_all(*, public_keys, block: Block):
    if public_keys is not None:
        for key_pub in public_keys:
            if not block_sign_verify(key_pub, block):
                return False

    return True


def block_new_from(previous_block: Block, content: dict):
    content_new = dict(**previous_block.content_dictionary)
    content_new.update(**content)
    new_block = Block(content_new, block_hash(previous_block), [])
    return new_block
