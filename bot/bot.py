import sys
import traceback
import argparse
from datetime import datetime


import asyncio
import threading


import bot_config
from bot_main import aiBot
#from bot_comms import publish, publish_action, publish_actions

sys.path.append("/root/projects")
import common.bot_logging
#logger = common.bot_logging.logging.getLogger('BotInstance') 



async def heartbeat_scheduler(bot):
    #publish("Let me check to see if I have any scheduled tasks due today.")
    while True:
        
        bot.heartbeat()
        await asyncio.sleep(bot_config.HEARTBEAT_SEC)


async def ai_response(bot):
    
    #publish(f"Hi {ai_config.FRIENDLY_NAME}, How can I help you today?")
    #publish_action("Get Started", "List available tools", "BOT_RESTART")
    #buttons = [("Check my tasks", "Show me a list of my task folders"),("Check the weather", "Check the weather for my saved location"),("Check emails", "Did I get any emails today?"), ("Book a meeting", "Book a meeting for tomorrow morning"), ("Draft an email", "Draft an email"), ("Research AI news", "Research AI news"), ("Restart BOT", "bot_restart")]
    #publish_actions("How can I help you today?", buttons)
    while True:
        #model_selector()
        bot.process_messages()
        await asyncio.sleep(0.5)
        #await asyncio.Event().wait()
    
async def main():
    #Create master bot
    bot = aiBot()
    
    
    common.bot_logging.bot_logger.info(f"Init Bot Instance")

    
    ai_tasks = []
    ai_tasks.append(asyncio.create_task(ai_response(bot)))
    ai_tasks.append(asyncio.create_task(heartbeat_scheduler(bot)))
    await asyncio.gather(*ai_tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Language Chain Bot")
    parser.add_argument("user_id", type=str, help="User ID")
    parser.add_argument("bot_id", type=str, help="Bot ID")
    
    args = parser.parse_args()

    print("starting bot...")
    print("user_id: " + args.user_id)
    print("bot_id: " + args.bot_id)

    bot_config.USER_ID = args.user_id
    bot_config.BOT_ID = args.bot_id

    #bot_config.RESET_CONFIG = args.reset_config
    common.bot_logging.init()
    #logger.addHandler(common.bot_logging.file_handler)

    asyncio.run(main())