from pathlib import Path

from cryptography.hazmat.primitives import (
    serialization
)

from cryptography.hazmat.primitives.asymmetric import (
    rsa
)


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)


private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)


public_key = private_key.public_key()


public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


keys_directory = Path("keys")

keys_directory.mkdir(
    exist_ok=True
)


(
    keys_directory / "private_key.pem"
).write_bytes(
    private_pem
)


(
    keys_directory / "public_key.pem"
).write_bytes(
    public_pem
)


print(
    "RSA public and private keys generated successfully."
)