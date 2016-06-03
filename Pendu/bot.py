"""Pendu bot by Debrot Aurélie & Ferreira Venancio Diogo"""
import asyncio
import json
import signal
import websockets
import aiohttp
from PenduController import *
from secrets import *

class bot:
    """
    Communication slack pour le bot pendu
    """
    async def processMessage(self,message):
        """
        Traite le message reçu de l'utilisateur
        :param message: message utilisateur
        """

        print("IN : " + str(message))

        # message to dict
        message = json.loads(message)

        # message intéréssant pour nous ?
        if "user" in message and "type" in message and message["type"] == "message":
            # new user ?
            if message["user"] not in self.users:
                self.users[message["user"]] = PenduController()

            # Pendu logic
            out = self.users[message["user"]].interpret_user_input(message["text"].lower())

            await self.api_call(
                method="chat.postMessage",
                user=message["user"],
                text=out,
                channel=message["channel"],
                type="message",
                attachments=[
                    {
                        "fallback":"image pendu",
                        "image_url": self.users[message["user"]].get_current_image()
                    }
                ]
            )


    async def api_call(self,method, **kwargs):
        """
        Communication avec slack via websockets
        :param method:
        :param kwargs:
        :return:
        """
        # JSON encode any sub-structure...
        for k, w in kwargs.items():
            # keep str as is.
            if not isinstance(w, (bytes, str)):
                kwargs[k] = json.dumps(w)

        with aiohttp.ClientSession() as session:
            form = aiohttp.FormData(kwargs or {})
            form.add_field('token', self.TOKEN)
            async with session.post('https://slack.com/api/{0}'.format(method),
                                    data=form) as response:
                assert 200 == response.status, ('{0} with {1} failed.'
                                                .format(method, self.data))
                return await response.json()


    async def start(self):
        """
        init de la communication avec slack
        :return:
        """
        rtm = await self.api_call("rtm.start")
        async with websockets.connect(rtm["url"]) as ws:
            while self.RUNNING:
                message = await ws.recv()
                asyncio.ensure_future(self.processMessage(message))

    def stop(self):
        """
        Arrête la communication
        """
        self.RUNNING = False
        print("Stopping... closing connections.")

    def __init__(self,TOKEN):
        self.TOKEN = TOKEN
        self.DEBUG = True
        self.RUNNING = True
        self.users = {}
        loop = asyncio.get_event_loop()
        loop.set_debug(self.DEBUG)
        loop.add_signal_handler(signal.SIGINT, self.stop)
        loop.run_until_complete(self.start())
        loop.close()

if __name__ == "__main__":
    bot(TOKEN)
