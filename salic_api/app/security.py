import codecs
from hashlib import md5

from Crypto import Random
from Crypto.Cipher import AES
from flask import current_app as app


def url_key():
    return app.config['URL_KEY'].rjust(16).encode('ascii')


SECRET_KEY = ('1234' * 4).encode('ascii')
TESTING_IV = b'0123456789abcdef'
STATIC_IV = None


def encrypt(text):
    """
    Uses AES to encrypt text with a global secret key.

    It saves the initialization vector with the resulting message.
    """

    if STATIC_IV is None:
        iv = Random.new().read(AES.block_size)
    else:
        iv = STATIC_IV

    cipher = AES.new(SECRET_KEY, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(text.encode('utf8'))
    return codecs.encode(msg, 'hex').decode('ascii')


def decrypt(text):
    """
    Uses AES to decrypt text with a global secret key.

    It extracts the initialization vector from the input message.
    """

    msg = codecs.decode(text.encode('ascii'), 'hex')
    iv = msg[:AES.block_size]

    if len(iv) != AES.block_size:
        return 'invalid'

    cipher = AES.new(SECRET_KEY, AES.MODE_CFB, iv)
    decoded = cipher.decrypt(msg[AES.block_size:])
    return decoded.decode('utf8')


def md5hash(text):
    m = md5.new()
    m.update(text)
    return m.hexdigest()
