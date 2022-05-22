from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import secrets
from binascii import unhexlify
import requests
import json

IP_ADDRESS = "217.28.228.66"

def init_user(pub_key_string, signature, data):
    response = requests.post(f"http://{IP_ADDRESS}:8000/api/init_user", json={
        "public_key": pub_key_string,
        "verification_string": data.hex(),
        "signature": signature.hex()
    })
    if response.status_code == 200:
        return True
    else:
        return False

def add_password(public_key, pub_key_string, signature, data, service, login, password):
    enc_login = public_key.encrypt(
        login.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    ).hex()
    enc_service = public_key.encrypt(
        service.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    ).hex()
    enc_password = public_key.encrypt(
        password.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    ).hex()
    response = requests.post(f"http://{IP_ADDRESS}:8000/api/create_password", json={
        "public_key": pub_key_string,
        "verification_string": data.hex(),
        "signature": signature.hex(),
        "service": enc_service,
        "login": enc_login,
        "password": enc_password

    })

def remove_password(pub_key_string, signature, data, address):
    response = requests.post(f"http://{IP_ADDRESS}:8000/api/delete_password", json={
        "public_key": pub_key_string,
        "verification_string": data.hex(),
        "signature": signature.hex(),
        "address": address
    })

def get_passwords(pub_key_string, private_key, signature, data):
    response = requests.get(f"http://{IP_ADDRESS}:8000/api/get_passwords", json={
        "public_key": pub_key_string,
        "verification_string": data.hex(),
        "signature": signature.hex(),
    })
    res = []
    j = json.loads(response.json())
    for pwd in j["passwords"]:
        pwd["service"] = private_key.decrypt(
            unhexlify(pwd["service"]),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        ).decode("utf-8")
        pwd["login"] = private_key.decrypt(
            unhexlify(pwd["login"]),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        ).decode("utf-8")
        pwd["password"] = private_key.decrypt(
            unhexlify(pwd["password"]),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        ).decode("utf-8")
        res.append(pwd)
    return res

def check_keys():
    # Load private key
    with open("private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )
    # Load public key
    with open("public.pem", "rb") as f:
        pub_key_string = f.read()
        public_key = serialization.load_pem_public_key(
            pub_key_string
        )
        pub_key_string = pub_key_string.hex()
    return private_key, public_key, pub_key_string

def sign_data(private_key):
    data = secrets.token_bytes(128)
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA512()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA512()
    )
    return signature, data

def generate_keys():
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open("private.pem", "wb") as f:
        f.write(private_key_bytes)
    with open("public.pem", "wb") as f:
        f.write(public_key)