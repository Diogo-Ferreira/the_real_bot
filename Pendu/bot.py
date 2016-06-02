"""Pendu bot by Debrot Aurélie & Ferreira Venancio Diogo"""
import asyncio
import json
import signal
import websockets
import aiohttp
from PenduController import PenduController
from secrets import TOKEN

DEBUG = True

RUNNING = True

# Dict of users with the channel, PenduController and user name as key
users = {}


async def processMessage(message):
    """Consume the message by interpeting them with the penducontroller class"""

    print("IN : " + str(message))

    # message to dict
    message = json.loads(message)

    # is the message interesting for us ?
    if "user" in message and "type" in message and message["type"] == "message":
        # new user ?
        if message["user"] not in users:
            users[message["user"]] = PenduController()

        # Pendu logic
        out = users[message["user"]].interpret_user_input(message["text"].lower())

        await api_call(
            method="chat.postMessage",
            user=message["user"],
            text=out,
            channel=message["channel"],
            type="message",
            attachments=[
                {
                    "fallback":"test",
                    "image_url": users[message["user"]].get_current_image()
                }
            ]
        )


async def api_call(method, **kwargs):
    # JSON encode any sub-structure...
    for k, w in kwargs.items():
        # keep str as is.
        if not isinstance(w, (bytes, str)):
            kwargs[k] = json.dumps(w)

    with aiohttp.ClientSession() as session:
        form = aiohttp.FormData(kwargs or {})
        form.add_field('token', TOKEN)
        async with session.post('https://slack.com/api/{0}'.format(method),
                                data=form) as response:
            assert 200 == response.status, ('{0} with {1} failed.'
                                            .format(method, data))
            return await response.json()


async def bot():
    """Create a bot that joins Slack."""
    rtm = await api_call("rtm.start")
    async with websockets.connect(rtm["url"]) as ws:
        while RUNNING:
            message = await ws.recv()
            asyncio.ensure_future(processMessage(message))


def stop():
    """Gracefully stop the bot."""
    global RUNNING
    RUNNING = False
    print("Stopping... closing connections.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(DEBUG)
    loop.add_signal_handler(signal.SIGINT, stop)
    loop.run_until_complete(bot())
    loop.close()
