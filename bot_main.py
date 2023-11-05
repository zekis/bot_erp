# Copyright (c) Tierney Morris
# This bot starts, registers itself with the server, and then waits for a message from a user.
# when bot rescieves message, it will start an instance of itself and parse the message on to the bot.
# the bot will send and recieve messages from the user until the task is complete and then shutdown

import bot_config
import sys
import traceback
import uuid
import bot_logging
import os

from datetime import datetime
from http import HTTPStatus

from typing import Dict


import asyncio
import threading

# from aiohttp import web
# from botbuilder.core.integration import aiohttp_error_middleware

from bot_manager import (
    process_server_message,
    register_self,
    clear_heartbeats,
    heartbeat,
)


async def main_loop():
    # logger.info("Start message processing")
    clear_heartbeats()
    # register_self()

    while True:
        await process_server_message()
        await asyncio.sleep(0.5)


async def heartbeat_loop():
    # logger.info("Start message processing")
    # register_self()

    while True:
        heartbeat()
        await asyncio.sleep(30.0)


async def main():
    script_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_path)

    logger = bot_logging.logging.getLogger("Bot_ERP")
    logger.addHandler(bot_logging.file_handler)
    logger.info(f"Init Bot")

    tasks = []
    tasks.append(asyncio.create_task(main_loop()))
    tasks.append(asyncio.create_task(heartbeat_loop()))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
