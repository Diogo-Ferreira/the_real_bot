"""Pendu bot by Debrot Aurélie & Ferreira Venancio Diogo"""
import asyncio
import json
import signal

import aiohttp
import websockets

from PenduController import PenduController
from secrets import TOKEN

DEBUG = True

RUNNING = True

#Dict of users with the channel, PenduController and user name as key
users = {}

#Messages to pass to the producer, TODO: use asyncio queue
toSendQueue = []

async def producer():

    #Are they any messages to process ?
    if len(toSendQueue) > 0:
        msg = toSendQueue.pop()
        out = {"user": msg["user"],"text":msg["text"],"channel":msg["channel"],"mrkdwn": False,"type":"message","attachments": [{
                   "fallback": "image of pendu",
                   "image_url": "http://diogoferreira.ch/pendu/1.png"
               }]}
        #print("OUT : " + str(out))
        return json.dumps(out)
    else:
        #If not, send a ping, to keep the connection alive
        await asyncio.sleep(10)
        return json.dumps({"type": "ping"})


async def consumer(message):
    """Consume the message by interpeting them with the penducontroller class"""

    print("IN : " + str(message))

    #message to dict
    message = json.loads(message)

    #is the message interesting for us ?
    if "user" in message and "type" in message and message["type"] == "message":
        #new user ?
        if message["user"] not in users:
            users[message["user"]] = {"channel" : message["channel"],"controller" : PenduController()}

        #Pendu logic, should it be here ? Maybe check if it's not better in the producer
        out = users[message["user"]]["controller"].interpret_user_input(message["text"].lower())

        #Pass it to the producer
        toSendQueue.insert(0, {
                               "user" : message["user"],
                               "text" : str(out),
                               "channel" : users[message["user"]]["channel"]
                           })

async def bot(token):
    """Create a bot that joins Slack."""
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as client:
        async with client.post("https://slack.com/api/rtm.start",
                               data={"token": TOKEN}) as response:
            assert 200 == response.status, "Error connecting to RTM."
            rtm = await response.json()

    async with websockets.connect(rtm["url"]) as ws:
        while RUNNING:
            listener_task = asyncio.ensure_future(ws.recv())
            producer_task = asyncio.ensure_future(producer())

            done, pending = await asyncio.wait(
                [listener_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

            if listener_task in done:
                message = listener_task.result()
                await consumer(message)

            if producer_task in done:
                message = producer_task.result()
                print(message)
                await ws.send(message)


def stop():
    """Gracefully stop the bot."""
    global RUNNING
    RUNNING = False
    print("Stopping... closing connections.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(DEBUG)
    loop.add_signal_handler(signal.SIGINT, stop)
    loop.run_until_complete(bot(TOKEN))
    loop.close()