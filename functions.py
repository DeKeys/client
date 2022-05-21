from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import secrets
from binascii import hexlify, unhexlify
import requests
import json
import  subprocess

def picture():
    print(""""╔═══╗╔═══╗╔╗╔═╗╔═══╗╔╗──╔╗╔═══╗
╚╗╔╗║║╔══╝║║║╔╝║╔══╝║╚╗╔╝║║╔═╗║
─║║║║║╚══╗║╚╝╝─║╚══╗╚╗╚╝╔╝║╚══╗
─║║║║║╔══╝║╔╗║─║╔══╝─╚╗╔╝─╚══╗║
╔╝╚╝║║╚══╗║║║╚╗║╚══╗──║║──║╚═╝║
╚═══╝╚═══╝╚╝╚═╝╚═══╝──╚╝──╚═══╝""")

def menu():
    print(''.join(40 * ["[]"]))
    print(f""" DeKeys Menu:\n1 - Show all paswords\n2 - Add Password\n3 - Remove Password\n4 - Leave""")
    choice = input("Enter an option: ")
    if choice in ["1", "2", "3", "4"]:
        print(''.join(40 * ["[]"]))
    else:
        menu()
    return choice

def init_user(pub_key_string, signature, data):
    response = requests.post(f"http://217.28.228.66:8000/api/init_user", json={
        "public_key": pub_key_string,
        "verification_string": data.hex(),
        "signature": signature.hex()
    })
    if response.status_code == 200:
        return True
    else:
        return False

def add_password(public_key, pub_key_string, signature, data):
    service = input("Enter service\n")
    login = input("\nEnter login\n")
    password = input("\nEnter password\n")
    check_flag = (input("\nDo you approve the addition?\nY/N\n")).upper()
    if check_flag == "N":
        print(''.join(40 * ["[]"]))
        return
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
    response = requests.post(f"http://217.28.228.66:8000/api/create_password", json={
        "public_key": pub_key_string,
        "verification_string": data.hex(),
        "signature": signature.hex(),
        "service": enc_service,
        "login": enc_login,
        "password": enc_password

    })
    print("Your password has been successfully added")

def remove_password(pub_key_string, signature, data):
    response = requests.post(f"http://217.28.228.66:8000/api/delete_password", json={
        "public_key": pub_key_string,
        "verification_string": data.hex(),
        "signature": signature.hex(),
        "address": "QmYP8txbVsU2AHXXyjkAPcW3Rufpr3n9PWBUWWQ3KG3cZu"
    })
    print("Your password has been removed")

def get_passwords(pub_key_string, private_key, signature, data):
    response = requests.get(f"http://217.28.228.66:8000/api/get_passwords", json={
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
    count = 0
    print("")
    for i in res:
        count += 1
        print(f"id: {count}")
        print(f"Service: {i['service']}")
        print(f"Login: {i['login']}")
        print(f"Password: {i['password']}\n")

def check_keys():
    print(''.join(40 * ["[]"]))
    key_flag = (input("Do you have a private and public key?\nY/N\n")).upper()
    if key_flag == "N":
        subprocess.Popen(['python3', 'gen_rsa.py'])
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