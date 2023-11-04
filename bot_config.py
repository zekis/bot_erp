from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

DISPATCHER_CHANNEL_ID = "botmanager"
BOT_ID = "researcher"
BOT_DESCRIPTION = "search google"


APP_ID = os.getenv("MicrosoftAppId")
APP_PASSWORD = os.getenv("MicrosoftAppPassword")

Todo_PollingIntervalSeconds = float(os.getenv("Todo_PollingIntervalSeconds",10.0))
Todo_BotsTaskFolder = os.getenv("Todo_BotsTaskFolder")

DATA_DIR = "data"

#These are set on startup
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#unique to this bot session, set from command line
TENANT_ID = os.getenv("tenant_id")
USER_ID = ""
FRIENDLY_NAME = ""
OFFICE_USER = os.getenv("OFFICE_USER")

RESET_CONFIG = False
VERBOSE = True

HEARTBEAT_NORMAL_SEC = 5.0
HEARTBEAT_SEC = 1.0
HEARTBEAT_RETRY_SEC = 1.0
SERVER_TIMOUT_SEC = 20.0

MAIN_AI = "gpt-3.5-turbo-16k"
TOOL_AI = "gpt-3.5-turbo-16k"

PARAMETER_PUBLISH = {"name": "publish", "description": "set to 'True' to publish as a nicely formatted human readable teams card, 'False' to return the raw data back to AI" }
PROMPT_PUBLISH_TRUE = "Output returned directly to human as a Teams Card. To retrieve the IDs and raw data, set 'publish' key to 'False'"