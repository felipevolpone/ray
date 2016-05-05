
import base64
from Crypto.PublicKey import RSA
from Crypto import Random
from collections import OrderedDict
import json


_COOKIE_NAME = 'RayAuth'
_QUEUE_KEY = 'RayQueue'
_QUEUE_PASS = '123f4qaerf'
__ID_SECURITY_KEY = 'RAY'

__KEY = RSA.generate(2048, Random.new().read).exportKey()


def sign_cookie(user_json):
    key = __get_key()
    user_as_str = json.dumps(OrderedDict(user_json))
    signature = key.sign(user_as_str, '')
    return _COOKIE_NAME, json.dumps({"s": signature[0], "c": user_json})


def cookie_content(cookie_text):
    text = __parse_text(cookie_text)
    if not text:
        return None
    return text['c']


def __parse_text(cookie_text):
    if not cookie_text:
        return False
    value = base64.b64decode(cookie_text)
    text = json.loads(value)
    if not text.keys():
        return None
    return text


def _validate(cookie_text):
    text = __parse_text(cookie_text)
    if not text:
        return False

    signature = (text['s'], )
    content = text['c']
    key = __get_key()
    if not key:
        return False

    content_str = json.dumps(OrderedDict(content))
    return key.verify(content_str, signature)


def __validate_queue(cookie_text):
    passw = base64.b64decode(cookie_text)
    if passw == _QUEUE_PASS:
        return True
    return False


def __get_key():
    global __KEY
    return RSA.importKey(__KEY)
