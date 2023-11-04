import sys
import os
import traceback
import bot_config
from datetime import datetime, timedelta

# import pytz
from typing import Any, Dict, Optional, Type

sys.path.append("/root/projects")
import common.bot_logging
from common.bot_comms import (
    publish_event_card,
    publish_list,
    send_to_another_bot,
    send_to_user,
    send_to_me,
    publish_error,
)
from common.bot_utils import tool_description, tool_error

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from langchain.utilities import GoogleSearchAPIWrapper

# tool_logger = common.bot_logging.logging.getLogger('ToolLogger')
# tool_logger.addHandler(common.bot_logging.file_handler)


class GoogleSearch(BaseTool):
    parameters = []
    optional_parameters = []
    name = "GOOGLE_SEARCH"
    summary = """useful when you need to answer questions about current events"""
    parameters.append({"name": "query", "description": "google search query"})
    description = tool_description(name, summary, parameters, optional_parameters)
    return_direct = False

    def _run(
        self,
        query: str,
        publish: str = "True",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            ai_summary = ""
            human_summary = []
            os.environ["GOOGLE_API_KEY"] = bot_config.GOOGLE_API_KEY
            os.environ["GOOGLE_CSE_ID"] = bot_config.GOOGLE_CSE_ID

            search = GoogleSearchAPIWrapper()
            response = search.run(query)
            # send_to_user(response)
            return response
        except Exception as e:
            # traceback.print_exc()
            tb = traceback.format_exc()
            publish_error(e, tb)
            return tool_error(e, tb, self.description)

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("GET_CALENDAR_EVENTS does not support async")
