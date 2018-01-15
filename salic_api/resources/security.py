from hashlib import md5

from Crypto import Random
from Crypto.Cipher import AES

from ..app import app

API_KEY_BYTES = app.config['URL_KEY'].encode('ascii')


def encrypt(text):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(API_KEY_BYTES, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(b''.join(text))
    return msg.encode('hex')


def decrypt(cypher_text):
    try:
        enc_msg = cypher_text.decode('hex')
        iv = enc_msg[:AES.block_size]
        cipher = AES.new(API_KEY_BYTES, AES.MODE_CFB, iv)
        dec_msg = cipher.decrypt(enc_msg)
    except Exception:
        return 'invalid'

    return dec_msg[AES.block_size:]


def md5hash(text):
    m = md5.new()
    m.update(text)
    return m.hexdigest()
