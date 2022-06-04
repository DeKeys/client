from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from gui.constants import private_key

import secrets


def generate_verification():
    """generate signature and data func"""
    data = secrets.token_bytes(128)
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA512()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA512()
    )
    return data.hex(), signature.hex()

