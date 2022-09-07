from .block import Block
from .serialization import block_serialize, block_deserialize

from icecream import ic
from typing import Union, Any, Dict
from cryptography.fernet import Fernet, MultiFernet

class BlockWrapper:
    """
    BlockWrapper wraps around a Block and handles its cryptographical concerns.
    """

    def __init__(*, block_decrypted: Block=None, block_encrypted=None, signature_pub_key=None, readwrite_keys=None):
        if readwrite_key is None:
            raise Exception("No read/write keys provided!")
        else:
            self.ferret = MultiFernet(readwrite_keys)

        if block_decrypted is None:
            if block_encrypted is None:
                raise Exception("No block provided to BlockWrapper's constructor!")
            else:
                block_decrypted_bytes = self.ferret.decrypt(block_encrypted)
                block_decrypted = block_deserialize(block_decrypted_bytes)
        else:
            block_decrypted_bytes = block_serialize(block_decrypted)

        self.block_decrypted = block_decrypted
        self.block_decrypted_bytes = block_decrypted_bytes

        if block_encrypted is None:
            block_encrypted = self.ferret.encrypt(block_decrypted_bytes)
        else:
            block_encrypted = self.ferret.rotate(block_encrypted)

        self.block_encrypted = block_encrypted
