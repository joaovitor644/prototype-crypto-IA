import logging
from typing import Any
from collections.abc import Callable
from openai.types.responses import FunctionToolParam, Response
from openai.types import ResponsesModel
from pydantic import BaseModel, Field
 
from crypto_app.agents.agent import Agent
from crypto_app.agents.coin_market_cap import CoinMarketAgent
from crypto_app.agents.web_search import WebSearchAgent
from crypto_app.agents.prompts import O_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoinMarketCapAgentParams(BaseModel):
    query: str = Field(
        description="""Prompt de consulta para o agente LLm que tem acesso a API do CoinMarketCap""",
    )

    model_config = {
        "extra": "forbid",
    }

class WebSeatchAgentParams(BaseModel):
    query: str = Field(
        description="""Prompt de consulta para o agente LLm que pode fazer pesquisas web sobre criptomoedas""",
    )

    model_config = {
        "extra": "forbid",
    }


FUNCTIONS: list[FunctionToolParam] = [
    {
        "type": "function",
        "name": "coin_market_cap_agent",
        "strict": True,
        "parameters": CoinMarketCapAgentParams.model_json_schema(),
        "description": """Retorna informações sobre criptomeodas coletadas pelo agente LLM a partir da API do CoinMArketCap como cotações e listagens""",
    },
    {
        "type": "function",
        "name": "web_search_agent",
        "strict": True,
        "parameters": WebSeatchAgentParams.model_json_schema(),
        "description": """Retorna informações sobre cripotmoedas coletadas pelo agente LLM a partir de suas pesquisas web realizadas""",
    },
]


class Orchestrator(Agent):
    def __init__(self, openai_api_key: str, coimarketcap_api_key: str, model: ResponsesModel = "gpt-4o-mini"):
        super().__init__(openai_api_key, model, FUNCTIONS, O_PROMPT)
        self._coin_market_cap = CoinMarketAgent(openai_api_key, coimarketcap_api_key, model)
        self._web_search = WebSearchAgent(openai_api_key, model)

    def _coin_market_cap_agent(self, query: str):
        _, r = self._coin_market_cap.ask(query)
        return r

    def _web_search_agent(self, query: str):
        _, r = self._coin_market_cap.ask(query)
        return r

    def _call_function(self, function_name, params):
        functions: dict[str, Callable[[Any], Response]] = {
            "coin_market_cap_agent": self._coin_market_cap_agent,
            "web_search_agent": self._web_search_agent,
        }
        if function_name not in functions:
            logger.error("function-not-found=%s", function_name)
            raise Exception(f"Function '{function_name}' does not exist")
        if "query" not in params:
            logger.error("params-query-error")
            raise Exception("Params are missing the query")

        query = params["query"]
        response = functions[function_name](query)
        return response.output_text
    