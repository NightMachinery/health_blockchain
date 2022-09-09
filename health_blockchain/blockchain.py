from .block_utilities import block_hash, block_sign_verify
from .crypto_utilities import hash_bytes
from .block import Block


class Blockchain:
    #: @todo0 add get_latest_content to get the last dictionary with all the blocks' data
    ##
    def __init__(self, blocks=None):
        if blocks is None:
            blocks = []

        self.blocks = blocks

    def add_block(self, *, block: Block, public_keys=None):
        if public_keys is not None:
            for key_pub in public_keys:
                if not block_sign_verify(key_pub, block):
                    raise Exception("The given block was not signed by all required parties!")

        if len(self.blocks) == 0:
            if block.previous_block_hash is not None:
                raise Exception(
                    "Trying to add a non-root block to an empty blockchain!"
                )
            else:
                self.blocks.append(block)
        else:
            previous_block_hash = block_hash(self.blocks[-1])
            if block.previous_block_hash == previous_block_hash:
                self.blocks.append(block)
            else:
                raise Exception(
                    "The new block's previous_block_hash does not match the last block in this blockchain!"
                )

    def add_blocks(self, blocks):
        for block in blocks:
            self.add_block(block)


def blockchain_hash(blc):
    if len(blc.blocks) > 0:
        return block_hash(blc.blocks[-1])
    else:
        return b"empty blockchain"
