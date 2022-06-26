from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import binascii
from base64 import b64encode
from base64 import b64decode

data = []
passwd = b"fdfsdf"
key = b'12345678ABCDEFGT'
# iv =  get_random_bytes(AES.block_size)
cipher = AES.new(key, AES.MODE_CBC)
for i in data:
    list2.append(cipher.encrypt(pad(i.encode('utf-8'), AES.block_size)))

print(list2) 

