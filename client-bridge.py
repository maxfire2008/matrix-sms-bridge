import smsframework.providers.log
import logging
import smsframework
from importlib import util
import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText)
import flask

mx_pw = input("MATRIX PASSWORD:")

async def matrix_send():
    pass

async def matrix_listener():
    async_client = AsyncClient(
        "https://matrix.maxstuff.net", "developer_testing"
    )
    response = await async_client.login(mx_pw)

    with open("next_batch", "r") as next_batch_token:
        async_client.next_batch = next_batch_token.read()

    print(response)
    while (True):
        sync_response = await async_client.sync(30000)
        joins = sync_response.rooms.join
        for room_id in joins:
            for event in joins[room_id].timeline.events:
                if hasattr(event, 'body'):
                    print(event)
                    
        with open("next_batch", "w+") as next_batch_token:
            next_batch_token.write(sync_response.next_batch)


def sms_send(message):
    print(message)

async def sms_listener():
    pass

logging.basicConfig(level=logging.DEBUG)

loop = asyncio.get_event_loop()
loop.create_task(matrix_listener())
loop.create_task(sms_listener())
loop.run_forever()
