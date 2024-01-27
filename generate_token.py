import socketio
import redis.asyncio as redis
import os
import sys
from dotenv import load_dotenv
import random, string
from datetime import datetime
from hashlib import sha256
import base58

def random_word(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def terminate(msg):
    print(msg)
    sys.exit(1)

load_dotenv()

app_key = os.getenv('APP_KEY')
if not app_key :
    terminate('APP_KEY not found')


def genToken(userid, clientid):
    r = random_word(10)
    t = datetime.now().timestamp()
    u = userid
    c = clientid
    s1 = f'r={r};t={t};uid={u};cid={c}'
    s2 = sha256(f'{s1};k={app_key}'.encode()).digest()
    s1_encoded_bin = base58.b58encode(s1)
    s1_encoded_str = s1_encoded_bin.decode()
    s2_encoded_bin = base58.b58encode(s2)
    s2_encoded_str = s2_encoded_bin.decode()
    token = f'{s1_encoded_str}-{s2_encoded_str}'
    return token

def decodeToken(token, app_key):
    if not token:
        return None
    tlist = token.split('-', 2)
    if len(tlist) != 2:
        return None
    s1,s2 = tlist
    s1 = base58.b58decode(s1).decode()
    s2 = base58.b58decode(s2)
    signature = sha256(f'{s1};k={app_key}'.encode()).digest()
    if signature != s2:
        return None
    dlist = [x.split('=') for x in s1.split(';')]
    user = dict(dlist)
    t = user['t']
    if abs(datetime.now().timestamp()-float(t))>86400:
        return None
    return user

t = genToken('6648', 'bevy')
print(t)
res = decodeToken(t, app_key)
print(res);