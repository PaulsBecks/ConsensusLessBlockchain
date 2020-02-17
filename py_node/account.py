import hashlib
from functools import reduce

from .config import SEPERATOR
from cryptography.hazmat.primitives import serialization as crypto_serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.exceptions import InvalidSignature

class Account:
  def __init__(self):
    self.key = rsa.generate_private_key(
      backend=crypto_default_backend(),
      public_exponent=65537,
      key_size=2048
    )  
  
  def sign(self, transaction):
    sig = self.key.sign(
        data=transaction.serialize(with_sig=False).encode('utf-8'),
        padding=padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        algorithm=hashes.SHA256()
    )
    transaction.set_sig(sig.hex())
    return

  def get_public_key(self):
    return self.key.public_key().public_bytes(
      crypto_serialization.Encoding.OpenSSH,
      crypto_serialization.PublicFormat.OpenSSH
    )

  def toJSON(self):
    return json.dumps({public_key: self.get_public_key()})
