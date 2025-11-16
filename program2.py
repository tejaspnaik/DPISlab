AES
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)

nonce = cipher.nonce
ct, tag = cipher.encrypt_and_digest(b"This is a secret message.")

pt = AES.new(key, AES.MODE_EAX, nonce=nonce).decrypt_and_verify(ct, tag)
print(pt.decode())


Key exchange algos

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util import number

# RSA
key = RSA.generate(2048)
cipher = PKCS1_OAEP.new(key.public_key())
ct = cipher.encrypt(b"this is a secret message")
pt = PKCS1_OAEP.new(key).decrypt(ct)

#print(key.public_key().export_key()) use if needed to show public key

print("Decrypted message:", pt.decode())

# Diffie-Hellman
p = number.getPrime(128)
g = 2
priv = number.getRandomRange(2, p-2)
pub = pow(g, priv, p)

print("Diffie-Hellman public key:", pub)