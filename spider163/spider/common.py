#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/16.
# email to LipsonChan@yahoo.com
#
import json
import os

from spider163.spider import public as uapi
from spider163.utils import encrypt
from spider163.utils import tools

csrf_dict = {'csrf_token': 'csrf'}


def create_params_by_dict(obj):
    try:
        return create_params_text(json.dumps(obj))
    except:
        raise


def create_params_text(text):
    # text = '{"ids":[' + str(song_id) + '], br:"320000",csrf_token:"csrf"}'
    nonce = '0CoJUm6Qyw8W8jud'
    nonce2 = 16 * 'F'
    encText = encrypt.aes(
        encrypt.aes(text, nonce).decode("utf-8"), nonce2
    )
    return encText


def rsa_encrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(tools.hex(text), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def create_secretKey(size):
    return (
               ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size)))
           )[0:16]


modulus = uapi.comment_module
pubKey = uapi.pubKey
secKey = uapi.secKey
encSecKey = rsa_encrypt(secKey, pubKey, modulus)
