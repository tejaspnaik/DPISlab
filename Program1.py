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


