import socketio
import redis.asyncio as redis
import os
import sys
from dotenv import load_dotenv
from hashlib import sha256
import base58
from datetime import datetime

def terminate(msg):
    print(msg)
    sys.exit(1)

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

load_dotenv()
app_debug = False
app_debug_str = os.getenv('APP_DEBUG', 'false')
if app_debug_str == 'True' or app_debug_str == 'true':
    app_debug = True

app_key = os.getenv('APP_KEY')
if not app_key :
    terminate('APP_KEY not found')

redis_manager = os.getenv('REDIS_MANAGER')
if not redis_manager:
    terminate('REDIS_MANAGER not found')

redis_channel = os.getenv('REDIS_CHANNEL')
if not redis_channel:
    terminate('REDIS_CHANNEL not found')

redis_prefix = os.getenv('REDIS_PREFIX')
if not redis_prefix:
    terminate('REDIS_PREFIX not found')    

#redis pool
redis_pool = redis.ConnectionPool.from_url(redis_manager)

#create manager
mgr = socketio.AsyncRedisManager(url=redis_manager, channel=redis_channel, write_only=False)

# create a Socket.IO server
sio = socketio.AsyncServer(client_manager=mgr, async_mode="asgi", cors_allowed_origins="*", 
    logger=app_debug, engineio_logger=app_debug)

# wrap with ASGI application
app = socketio.ASGIApp(sio)

@sio.on('ping')
async def ping_event(sid, data):
    await sio.emit('pong', '', room=sid)

@sio.on('*')
async def any_event(event, sid, data):
    await sio.emit(sid, data, room=sid)

@sio.event
async def connect(sid, environ, auth):
    if app_debug:
        print('connected ', sid)
        print('auth ', auth)
    if not ('token' in auth):
        return False
    token = auth['token']
    if not isinstance(token, str):
        return False
    user = decodeToken(token, app_key)
    if not user:
        return False
    if app_debug:
        print('auth ', user)

    try:
        client = redis.Redis.from_pool(redis_pool)
        await client.set(f'{redis_prefix}_{user["uid"]}_{user["cid"]}', sid, ex=3600)
        await client.aclose()
    except redis.RedisError:
        print('Save auth info error:', user)

@sio.event
async def disconnect(sid):
    if app_debug:    
        print('disconnected ', sid)
