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

redis_prefix = os.getenv('REDIS_PREFIX')
if not redis_prefix:
    terminate('REDIS_PREFIX not found')    

#create manager
external_sio = socketio.RedisManager(url=redis_manager, channel=redis_channel, write_only=True)


#redis pool
redis_pool = redis.ConnectionPool.from_url(redis_manager)

client = redis.Redis.from_pool(redis_pool)

uid = 6648
cid = 'bevy'
sid =  client.get(f'{redis_prefix}_{uid}_{cid}')
if not sid:
    terminate(f'Error: uid={uid}, cid={cid}, sid not found')

sid = sid.decode()
print(f'uid={uid}, cid={cid}, sid={sid}')

# emit an event
external_sio.emit('external_sio_via_uid_cid', data=f'uid={uid}, cid={cid}, sid={sid}', room=sid)