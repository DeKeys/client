from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes
import secrets
from binascii import unhexlify
import requests
import json


IP_ADDRESS = "http://217.28.228.66:8000/api/{}"


def init_user(pub_key_string, signature, data):
    """initialisation of user in server

    @param pub_key_string: public key
    @param signature: signature for authentic user in server
    @param data: verification string
    """

    response = requests.post(IP_ADDRESS.format("init_user"), json={
        "public_key": pub_key_string,
        "verification_string": data.hex(),
        "signature": signature.hex()
    })
    if response.status_code == 200:
        return True
    else:
        return False


def add_password(public_key, pub_key_string, signature, data, service, login, password):
    """Encrypts and send to server new password

    @param pub_key_string: public key
    @param signature: signature for authentic user in server
    @param data: verification string
    @param public_key: public key
    @param service: key's service
    @param login: key's login
    @param password: key's password
    """

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
    response = requests.post(IP_ADDRESS.format("create_password"), json={
        "public_key": pub_key_string,
        "verification_string": data.hex(),
        "signature": signature.hex(),
        "service": enc_service,
        "login": enc_login,
        "password": enc_password

    })


def delete_password(pub_key_string, signature, verification_string, address):
    """Send to server key address to delete them

    @param pub_key_string: public key
    @param signature: signature for authentic user in server
    @param verification_string: verification string
    @param address: key's adress
    """

    response = requests.post(IP_ADDRESS.format("delete_password"), json={
        "public_key": pub_key_string,
        "verification_string": verification_string.hex(),
        "signature": signature.hex(),
        "address": address
    })


def get_passwords(pub_key_string, private_key, signature, data):
    """Get all keys from server and decrypt them

    @param pub_key_string: public key
    @param signature: signature for authentic user in server
    @param data: verification string
    @param private_key: private key
    """

    response = requests.get(IP_ADDRESS.format("get_passwords"), json={
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
    """Check public and private keys"""

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
    """Make signature and data from private key

    @param private_key: private key
    """

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
    """Generate private and public keys"""

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
        
def edit_password(public_key, pub_key_string, signature, address, service, login, password, data):
    """Edit password

    @param pub_key_string: public key
    @param signature: signature for authentic user in server
    @param data: verification string
    @param public_key: public key
    @param service: key's service
    @param login: key's login
    @param password: key's password
    @param address: key's address
    """

    enc_login = public_key.encrypt(
        login.encode("utf-8"),
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
    enc_service = public_key.encrypt(
        service.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    ).hex()
    response = requests.post(f"http://{IP_ADDRESS}:8000/api/edit_password", json={
        "public_key": pub_key_string,
        "verification_string": data.hex(),
        "signature": signature.hex(),
        "address": address,
        "service": enc_service,
        "login": enc_login,
        "password": enc_password
    })
