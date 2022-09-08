from .block import Block
import pickle

def block_deserialize(block_bytes: bytes) -> Block:
    return pickle.loads(block_bytes)


def block_serialize(block: Block) -> bytes:
    return pickle.dumps(block,
                        protocol=5,)
