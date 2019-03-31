import socketio

from conf import streamelements_jwt as jwt_token
from utils.logger import loggyballs as log

sio = socketio.AsyncClient(logger=True)

@sio.on('connect')
async def on_connect():
    await sio.emit('authenticate',{'method':'jwt','token':jwt_token})
    log.debug('connection established')

@sio.on('event')
async def on_event(data):
    print.debug('message received with ', data)

@sio.on('event:test')
async def on_event_test(data):
    print.debug('test message received with ', data)

@sio.on('disconnect')
async def on_disconnect():
    print.debug('disconnected from server')

@sio.on('authenticated')
async def on_authenticated():
    print.debug('authenticated to the server!')

async def listen_streamelements():
    await sio.connect('wss://realtime.streamelements.com', transports=['websocket'])
#   await sio.connect('http://localhost:5000')

# sio.wait()