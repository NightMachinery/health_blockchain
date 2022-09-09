from .block import Block
from .serialization import block_serialize, block_deserialize

from icecream import ic
from typing import Union, Any, Dict
from cryptography.fernet import Fernet, MultiFernet


def readwrite_key_generate():
    return Fernet(Fernet.generate_key())


def readwrite_key_generate_and_append(fernets):
    return fernets + [readwrite_key_generate()]


class EDWrapper:
    """
    EDWrapper wraps around an object and encrypts/decrypts it.
    """

    def __init__(
        self,
        *,
        obj_decrypted=None,
        obj_encrypted=None,
        readwrite_keys=None
    ):
        if readwrite_key is None:
            raise Exception("No read/write keys provided!")
        else:
            self.fernet = MultiFernet(readwrite_keys)

        if obj_decrypted is None:
            if obj_encrypted is None:
                raise Exception("No obj provided to EDWrapper's constructor!")
            else:
                obj_decrypted_bytes = self.fernet.decrypt(obj_encrypted)
                obj_decrypted = obj_deserialize(obj_decrypted_bytes)
        else:
            obj_decrypted_bytes = obj_serialize(obj_decrypted)

        self.obj_decrypted = obj_decrypted
        self.obj_decrypted_bytes = obj_decrypted_bytes

        if obj_encrypted is None:
            obj_encrypted = self.fernet.encrypt(obj_decrypted_bytes)
        else:
            obj_encrypted = self.fernet.rotate(obj_encrypted)

        self.obj_encrypted = obj_encrypted
