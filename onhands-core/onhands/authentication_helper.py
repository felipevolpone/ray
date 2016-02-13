
import base64
from functools import wraps
from Crypto.PublicKey import RSA
from Crypto import Random
from collections import OrderedDict
import json


__COOKIE_NAME = 'OnHandsAuth'
_QUEUE_KEY = 'OnHandsQueue'
_QUEUE_PASS = '123f4qaerf'
__ID_SECURITY_KEY = 'ONHANDS'

__KEY = RSA.generate(2048, Random.new().read).exportKey()


def sign_cookie(user_json):
    key = __get_key()
    user_as_str = json.dumps(OrderedDict(user_json))
    signature = key.sign(user_as_str, '')
    return __COOKIE_NAME, json.dumps({"s": signature[0], "c": user_json})


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
