
#digital signature schemes

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

key = RSA.generate(2048)

msg = b"This is a secret message."
h = SHA256.new(msg)

sig = PKCS1_v1_5.new(key).sign(h)
valid = PKCS1_v1_5.new(key.public_key()).verify(h, sig)

print(h)
print("Signature (hex):", sig)
print("Is signature valid?", valid)
