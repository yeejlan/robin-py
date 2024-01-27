import socketio
import redis
import os
import sys
from dotenv import load_dotenv

def terminate(msg):
    print(msg)
    sys.exit(1)

load_dotenv()

redis_manager = os.getenv('REDIS_MANAGER')
if not redis_manager:
    terminate('REDIS_MANAGER not found')

redis_channel = os.getenv('REDIS_CHANNEL')
if not redis_channel:
    terminate('REDIS_CHANNEL not found')

#create manager
external_sio = socketio.RedisManager(url=redis_manager, channel=redis_channel, write_only=True)

sid = 'zOpqM7vtdBuGFBY3AAAD'
# emit an event
external_sio.emit('external_sio_via_sid', data='1124423377', room=sid)

