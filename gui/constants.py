from cryptography.hazmat.primitives import serialization


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

