from hashlib import md5
import codecs

from Crypto import Random
from Crypto.Cipher import AES
from flask import current_app as app


def url_key():
    return app.config['URL_KEY'].rjust(16).encode('ascii')


def encrypt(text):
    # FIXME: check the correct algorithm
    text = text.encode('utf8')
    iv = Random.new().read(AES.block_size)
    iv = b'0' * 16
    cipher = AES.new(url_key(), AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(text)
    return codecs.encode(msg, 'hex').decode('ascii')


def decrypt(cypher_text):
    try:
        enc_msg = cypher_text.decode('hex')
        iv = enc_msg[:AES.block_size]
        cipher = AES.new(url_key(), AES.MODE_CFB, iv)
        dec_msg = cipher.decrypt(enc_msg)
    except Exception:
        return 'invalid'

    return dec_msg[AES.block_size:]


def md5hash(text):
    m = md5.new()
    m.update(text)
    return m.hexdigest()
