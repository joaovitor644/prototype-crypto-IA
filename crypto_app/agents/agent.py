import logging
import json
from typing import Iterable
from abc import ABC, abstractmethod
from openai import OpenAI
from openai.types.responses import ResponseInputParam, ToolParam
from openai.types import ResponsesModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Agent(ABC):
    def __init__(
        self,
        openai_api_key: str,
        model: ResponsesModel,
        tools: Iterable[ToolParam],
        system_prompt: str,
    ):
        self._openai_api_key = openai_api_key
        self._model = model
        self._system_prompt = system_prompt
        self._tools = tools
        self._client = OpenAI(api_key=self._openai_api_key)

    @abstractmethod
    def _call_function(self, function_name: str, params): ...

    def ask(self, prompt: str):
        input: ResponseInputParam = [
            {
                "type": "message",
                "role": "system",
                "content": self._system_prompt,
            },
            {
                "type": "message",
                "role": "user",
                "content": prompt,
            },
        ]

        has_function_call = True
        while has_function_call:
            logger.info("calling-openai-api reponse-create")
            response = self._client.responses.create(
                model=self._model,
                tools=self._tools,
                input=input,
            )

            has_function_call = False
            for output in response.output:
                if output.type == "function_call":
                    logger.info("reponse-create found-function-call=%s", output.name)
                    has_function_call = True

                    params = json.loads(output.arguments)
                    result = self._call_function(output.name, params)

                    input.append(output)
                    input.append(
                        {
                            "type": "function_call_output",
                            "call_id": output.call_id,
                            "output": json.dumps(result),
                        }
                    )
                elif output.type == "web_search_call":
                    input.append(output)
                elif output.type == "message":
                    input.append(output)

        return input, response
