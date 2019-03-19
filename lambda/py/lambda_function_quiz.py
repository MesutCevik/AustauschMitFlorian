from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.response_helper import get_plain_text_content
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Response, ui
from ask_sdk_model.interfaces.display import Image, ImageInstance, ListItem, RenderTemplateDirective, ListTemplate1, \
    BackButtonBehavior

from alexa import util, data
from lambda_function import logger


class QuizHandler(AbstractRequestHandler):
    """Handler for starting a quiz.

    The ``handle`` method will initiate a quiz state and build a
    question randomly from the states data, using the util methods.
    If the skill can use cards, then the question choices are added to
    the card and shown in the Response. If the skill uses display,
    then the question is displayed using RenderTemplates.
    """

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return (is_intent_name("QuizIntent")(handler_input) or
                is_intent_name("AMAZON.StartOverIntent")(handler_input))

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In QuizHandler")
        attr = handler_input.attributes_manager.session_attributes
        attr["state"] = "QUIZ"
        attr["counter"] = 0
        attr["quiz_score"] = 0

        question = util.ask_question(handler_input)
        response_builder = handler_input.response_builder
        response_builder.speak(data.START_QUIZ_MESSAGE + question)
        response_builder.ask(question)

        if data.USE_CARDS_FLAG:
            item = attr["quiz_item"]
            response_builder.set_card(
                ui.StandardCard(
                    title="Question #1",
                    text=data.START_QUIZ_MESSAGE + question,
                    image=ui.Image(
                        small_image_url=util.get_small_image(item),
                        large_image_url=util.get_large_image(item)
                    )))

        if util.supports_display(handler_input):
            item = attr["quiz_item"]
            item_attr = attr["quiz_attr"]
            title = "Question #{}".format(str(attr["counter"]))
            background_img = Image(
                sources=[ImageInstance(
                    url=util.get_image(
                        ht=1024, wd=600, label=attr["abbreviation"]))])
            item_list = []
            for ans in util.get_multiple_choice_answers(
                    item, item_attr, data.STATES_LIST):
                item_list.append(ListItem(
                    token=ans,
                    text_content=get_plain_text_content(primary_text=ans)))

            response_builder.add_directive(
                RenderTemplateDirective(
                    ListTemplate1(
                        token="Question",
                        back_button=BackButtonBehavior.HIDDEN,
                        background_image=background_img,
                        title=title,
                        list_items=item_list)))

        return response_builder.response