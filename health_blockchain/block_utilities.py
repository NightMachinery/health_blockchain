from .block import Block


def block_hash(block: Block) -> bytes:
    block_without_sig = block_update(block, signatures=[])
    block_bytes = block_serialize(block_without_sig)

    digest = hashes.Hash(hashes.BLAKE2b(64))
    digest.update(block_bytes)
    return digest.finalize()


def block_sign(block: Block):
    #: @todo0
    block_bytes = block_serialize(block)

    pass
