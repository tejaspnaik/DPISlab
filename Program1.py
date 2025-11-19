#DES
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

key = b'8bytekey'
cipher = DES.new(key, DES.MODE_ECB)
#u can replace DES.block_size with 8 cause size is 8bytes
ct = cipher.encrypt(pad(b"hellosymmetricDES", DES.block_size))
pt = unpad(cipher.decrypt(ct), DES.block_size)

print("encrypted text:",ct)
print("plaintext:",pt)

#AES
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)

ct, tag = cipher.encrypt_and_digest(b"secret msg")

print("Ciphertext:", ct)

pt = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce).decrypt_and_verify(ct, tag)
print("Plaintext:", pt.decode())




