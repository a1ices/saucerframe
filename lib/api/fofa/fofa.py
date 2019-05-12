#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

import sys
import json
import base64
from lib.utils.config import ConfigFileParser
from lib.core.common import colorprint
from lib.core.data import paths,conf
try:
    import requests
except:
    colorprint.red("[-] Can't import requests")
    colorprint.cyan("[*] Try pip install requests")
    sys.exit()

# verify email and key
def check(email, key): 
    if email and key:
        auth_url = "https://fofa.so/api/v1/info/my?email={0}&key={1}".format(email, key)
        try:
            response = requests.get(auth_url)
            if response.code == 200:
                return True
        except Exception as e:
            return False
    return False



def handle_fofa(query, limit, offset=0):
    try:
        msg = '[+] Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        colorprint.green(msg)
        email = ConfigFileParser().fofa_email()
        key = ConfigFileParser().fofa_key()
        if check(email, key):
            pass
        else:
            raise SystemExit  # will go to except block
    except:
        msg = '[*] Automatic authorization failed.'
        colorprint.cyan(msg)
        msg = '[*] Please input your FoFa Email and API Key below.'
        colorprint.cyan(msg)
        email = input("[*] Fofa Email: ").strip()
        key = input('[*] Fofa API Key: ').strip()
        if not check(email, key):
            msg = '[-] Fofa API authorization failed, Please re-run it and enter a valid key.'
            colorprint.red(msg)
            sys.exit()

    query = base64.b64encode(query)

    request = "https://fofa.so/api/v1/search/all?email={0}&key={1}&qbase64={2}".format(email, key, query)
    try:
        response = requests.get(request)
        resp = response.readlines()[0]
        resp = json.loads(resp)
        if resp["error"] is None:
            for item in resp.get('results'):
                conf.target.append(item[0])
            if resp.get('size') >= 100:
                colorprint.cyan("{0} items found! just 100 returned....".format(resp.get('size')))
    except Exception as e:
        colorprint.red(e)
        sys.exit()
