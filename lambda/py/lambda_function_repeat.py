import json

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Response

from alexa import data
from lambda_function import logger


class RepeatHandler(AbstractRequestHandler):
    """Handler for repeating the response to the user."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        if "recent_response" in attr:
            cached_response_str = json.dumps(attr["recent_response"])
            cached_response = DefaultSerializer().deserialize(
                cached_response_str, Response)
            return cached_response
        else:
            response_builder.speak(data.FALLBACK_ANSWER).ask(data.HELP_MESSAGE)

            return response_builder.response