from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import binascii
from base64 import b64encode
from base64 import b64decode

data = ["0.0085892" , "-0.01978968", "-0.12664734",  "0.2099255", "-0.02405136"]
list2 = []
# list3 = []
   # ct = b64encode(i).decode('utf-8')
    # list2.append(ct)
passwd = b"fdfsdf"
key = b'12345678ABCDEFGT'
# iv =  get_random_bytes(AES.block_size)

cipher = AES.new(key, AES.MODE_CBC)

for i in data:
    list2.append(cipher.encrypt(pad(i.encode('utf-8'), AES.block_size)))

print(list2) 



# iv = b64encode(IV).decode('utf-8')
# iv = b64decode(iv)

# cipher2 = AES.new(key, AES.MODE_CBC, iv)

# for i in list2:
#     # ct = b64decode(i)
#     list3.append(cipher2.decrypt(unpad(i, AES.block_size)))
#     # print(i)

