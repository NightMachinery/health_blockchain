from . import block_utilities
from .crypto_utilities import hash_bytes
from .block import Block


class Blockchain:
    def __init__(self, blocks=None, public_keys=None):
        self.blocks = []
        if blocks is not None:
            self.add_blocks(blocks, public_keys=public_keys)


    def add_block(self, block: Block, *, public_keys=None):
        if not block_utilities.block_sign_verify_all(
            public_keys=public_keys, block=block
        ):
            raise Exception("The given block was not signed by all required parties!")

        if len(self.blocks) == 0:
            if False and block.previous_block_hash is not None:
                #: I have disabled this error, as it gives more flexibility to the users.

                raise Exception(
                    "Trying to add a non-root block to an empty blockchain!"
                )
            else:
                self.blocks.append(block)
        else:
            previous_block_hash = block_utilities.block_hash(self.blocks[-1])
            if block.previous_block_hash == previous_block_hash:
                self.blocks.append(block)
            else:
                raise Exception(
                    "The new block's previous_block_hash does not match the last block in this blockchain!"
                )

    def add_blocks(self, blocks, **kwargs):
        for block in blocks:
            self.add_block(block=block, **kwargs)

    def get_latest_content(self):
        if len(self.blocks) >= 1:
            res = self.blocks[0].content_dictionary.copy()

            for block in self.blocks[1:]:
                res.update(**block.content_dictionary)

            return res
        else:
            return None

    def __str__(self):
        return f"Blockchain:\n\tblocks={str(self.blocks)}\n\tcontent={self.get_latest_content()}\n"


def blockchain_hash(blc):
    if len(blc.blocks) > 0:
        return block_hash(blc.blocks[-1])
    else:
        return b"empty blockchain"
