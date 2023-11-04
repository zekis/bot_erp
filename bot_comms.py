import traceback
import pika
import json
import time 
import bot_logging
import bot_config

comms_logger = bot_logging.logging.getLogger('BotComms')
comms_logger.addHandler(bot_logging.file_handler)
"This module handles sending and recieving between server and bots"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
message_channel = connection.channel()

def encode_command(bot_id, command: str, data: str) -> str:
    "encode a <prompt> into a dict and return a string to send via rabbitmq to a bot"
    
    response = {
        "bot_id": bot_id,
        "command": command,
        "data": data
    }
    comms_logger.debug(f"ENCODING: {response}")

    return json.dumps(response)

def encode_response(bot_id, user_id, prompt: str) -> str:
    "encode a <prompt> into a dict and return a string to send via rabbitmq to a bot"
    
    response = {
        "bot_id": bot_id,
        "user_id": user_id,
        "prompt": prompt
    }
    comms_logger.debug(f"ENCODING: {response}")

    return json.dumps(response)

def encode_instance_message(user_id, prompt: str) -> str:
    "encode a <prompt> into a dict and return a string to send via rabbitmq to a bot"
    
    response = {
        "user_id": user_id,
        "prompt": prompt
    }
    comms_logger.debug(f"ENCODING: {response}")

    return json.dumps(response)

def encode_instance_credentials(user_id, credentials: list) -> str:
    "encode a <prompt> into a dict and return a string to send via rabbitmq to a bot"
    
    response = {
        "user_id": user_id,
        "credentials": credentials
    }
    comms_logger.debug(f"ENCODING: {response}")

    return json.dumps(response)


def decode_response(response: dict) -> str:
    "decode a dict <response> into a message and return the prompt as string"
    
    try:
        response = response.decode("utf-8")

        comms_logger.debug(f"DECODING: {response}")

        response_dict = json.loads(response)

        #prompt = response_dict.get('prompt')
        
        return response_dict
    except Exception as e:
        traceback.print_exc()
        return "prompt", f"error: {e}", None


def from_dispatcher() -> str:
    'consume and decode a message from <channel_id> directed as a specific user'

    channel_id = bot_config.BOT_ID    

    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # message_channel = connection.channel()
    
    message_channel.queue_declare(queue=channel_id)

    method, properties, body = message_channel.basic_get(queue=channel_id, auto_ack=True)

    # message_channel.close()

    if body:
        response = decode_response(body)
        return response
    else:
        return None

def send_to_dispatcher(command: str, data: str):
    "encode and send a message directly to a bot using <channel_id>"

    channel_id = bot_config.DISPATCHER_CHANNEL_ID
    bot_id = bot_config.BOT_ID


    comms_logger.debug(f"CHANNEL: {channel_id} - {bot_id} - {command}")

    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # message_channel = connection.channel()

    message_channel.queue_declare(queue=channel_id)

    message = encode_command(bot_id, command, data)

    message_channel.basic_publish(exchange='',routing_key=channel_id,body=message)

def send_to_user(user_id: str, prompt: str):
    "encode and send a message directly to a bot using <channel_id>"

    channel_id = bot_config.DISPATCHER_CHANNEL_ID
    bot_id = bot_config.BOT_ID


    comms_logger.info(f"CHANNEL: {channel_id} - {user_id} - {prompt}")

    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # message_channel = connection.channel()

    message_channel.queue_declare(queue=channel_id)

    message = encode_response(bot_id, user_id, prompt)

    message_channel.basic_publish(exchange='',routing_key=channel_id,body=message)

def send_to_instance(user_id: str, prompt: str):
    "encode and send a message directly to a bot using <channel_id>"
    bot_instance_channel = bot_config.BOT_ID + user_id
    

    comms_logger.info(f"CHANNEL: {bot_instance_channel} - {user_id} - {prompt}")

    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # message_channel = connection.channel()

    message_channel.queue_declare(queue=bot_instance_channel)

    message = encode_instance_message(user_id, prompt)

    message_channel.basic_publish(exchange='',routing_key=bot_instance_channel,body=message)



def send_credentials_to_instance(user_id: str, credentials: list):
    "encode and send a message directly to a bot using <channel_id>"
    bot_instance_channel = bot_config.BOT_ID + user_id

    comms_logger.info(f"CHANNEL: {bot_instance_channel} - {user_id} - {credentials}")

    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # message_channel = connection.channel()

    message_channel.queue_declare(queue=bot_instance_channel)

    message = encode_instance_credentials(user_id, credentials)

    message_channel.basic_publish(exchange='',routing_key=bot_instance_channel,body=message)


def clear_queue(channel_id: str):
    "clear message queue (do this on start)"
    comms_logger.info("Clearing message queue")

    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # message_channel = connection.channel()

    message_channel.queue_delete(channel_id)

    message_channel.queue_declare(channel_id)
