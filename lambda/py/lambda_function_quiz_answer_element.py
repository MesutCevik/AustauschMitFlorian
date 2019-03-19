from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type

from lambda_function import logger
from lambda_function_quiz_answer import QuizAnswerHandler


class QuizAnswerElementSelectedHandler(AbstractRequestHandler):
    """Handler for ElementSelected Request.

    This handler handles the logic of Display.ElementSelected request
    if the users selects the answer choice on a multimodal device,
    rather than answering through voice. This calls the QuizAnswerHandler
    handle function directly, since the underlying logic of checking the
    answer and responding is the same."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return (attr.get("state") == "QUIZ" and
                is_request_type("Display.ElementSelected")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In QuizAnswerElementSelectedHandler")
        return QuizAnswerHandler().handle(handler_input)