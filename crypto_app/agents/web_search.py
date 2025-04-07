import logging
from openai.types.responses import WebSearchToolParam
from openai.types import ResponsesModel

from crypto_app.agents.agent import Agent
from crypto_app.agents.prompts import WS_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEB_SEARCH: list[WebSearchToolParam] = [
    {
        "type": "web_search_preview",
        "search_context_size": "medium",
    }
]


class WebSearchAgent(Agent):
    def __init__(
        self, openai_api_key: str, model: ResponsesModel = "gpt-4o-mini"
    ):
        super().__init__(
            openai_api_key, model=model, tools=WEB_SEARCH, system_prompt=WS_PROMPT
        )

    def _call_function(self, function_name, params):
        logger.error("function-call impossible")
        raise Exception("This class does not have functions")
