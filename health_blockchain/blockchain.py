from .block_utilities import block_hash
from .block import Block


class Blockchain:
    def __init__(self, blocks=None):
        if blocks is None:
            blocks = []

        self.blocks = blocks

    def add_block(self, block: Block):
        #: @todo0 verify the block's signatures
        ##
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
