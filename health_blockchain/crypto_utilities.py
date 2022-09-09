from typing import List
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def hash_bytes(bs: List[bytes], /) -> bytes:
    digest = hashes.Hash(hashes.BLAKE2b(64))

    for b in bs:
        digest.update(b)

    return digest.finalize()


def sign_keys_generate():
    private_key = Ed25519PrivateKey.generate()
    return (private_key, private_key.public_key())


def sign_bytes(key_prv, b: bytes, /) -> bytes:
    return key_prv.sign(b)


def verify_sign(key_pub, sign: bytes, b: bytes, /) -> bool:
    try:
        key_pub.verify(sign, b)
        return True
    except:
        return False
