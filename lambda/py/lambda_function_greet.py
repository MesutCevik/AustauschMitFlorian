from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.ui import SimpleCard

from lambda_function import logger


class GreetIntentHandler(AbstractRequestHandler):
    """Handler for Greet Florian or Mesut and everybody else Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("GreetIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # logger.info("In GreetIntent")
        slots = handler_input.request_envelope.request.intent.slots

        name_user = slots["name"].value

        if name_user:
            speech_text = f"Hello {name_user} my friend!"

        else:
            speech_text = "Hello Python World from Classes!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)

        return handler_input.response_builder.response