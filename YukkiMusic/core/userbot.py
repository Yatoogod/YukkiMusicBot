#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import sys
from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []


class Userbot:
    def __init__(self):
        self.clients = []

        # Initialize clients dynamically based on available strings
        for session_string in [
            config.STRING1,
            config.STRING2,
            config.STRING3,
            config.STRING4,
            config.STRING5,
        ]:
            if session_string:
                self.clients.append(
                    Client(
                        session_string=session_string,
                        api_id=config.API_ID,
                        api_hash=config.API_HASH,
                        no_updates=True,
                    )
                )

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistant Clients")
        for index, client in enumerate(self.clients, start=1):
            try:
                await client.start()
                assistants.append(index)
                await self.join_support_chats(client)
                await self.log_start(client, index)
                get_me = await client.get_me()
                client.username = get_me.username
                client.id = get_me.id
                assistantids.append(get_me.id)
                client.name = (
                    f"{get_me.first_name} {get_me.last_name}"
                    if get_me.last_name
                    else get_me.first_name
                )
                LOGGER(__name__).info(f"Assistant {index} Started as {client.name}")
            except Exception as e:
                LOGGER(__name__).error(
                    f"Failed to start Assistant {index}: {str(e)}"
                )
                sys.exit()

    async def join_support_chats(self, client):
        try:
            await client.join_chat("TeamYM")
            await client.join_chat("TheYukki")
            await client.join_chat("YukkiSupport")
        except Exception as e:
            LOGGER(__name__).warning(f"Failed to join support chats: {str(e)}")

    async def log_start(self, client, index):
        try:
            await client.send_message(config.LOG_GROUP_ID, f"Assistant {index} Started")
        except Exception as e:
            LOGGER(__name__).error(
                f"Assistant {index} failed to access the log Group. Make sure it is added and promoted in the group. Error: {str(e)}"
            )
            sys.exit()
