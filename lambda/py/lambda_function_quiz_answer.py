from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.response_helper import get_plain_text_content, get_rich_text_content
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import ui
from ask_sdk_model.interfaces.display import Image, ImageInstance, ListItem, RenderTemplateDirective, ListTemplate1, \
    BackButtonBehavior, BodyTemplate1

from alexa import util, data
from lambda_function import logger


class QuizAnswerHandler(AbstractRequestHandler):
    """Handler for answering the quiz.

    The ``handle`` method will check if the answer specified is correct,
    by checking if it matches with the corresponding session attribute
    value. According to the type of answer, alexa responds to the user
    with either the next question or the final score.

    Similar to the quiz handler, the question choices are
    added to the Card or the RenderTemplate after checking if that
    is supported.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AnswerIntent")(handler_input) and
                attr.get("state") == "QUIZ")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In QuizAnswerHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder

        item = attr["quiz_item"]
        item_attr = attr["quiz_attr"]
        is_ans_correct = util.compare_token_or_slots(
            handler_input=handler_input,
            value=item[item_attr])

        if is_ans_correct:
            speech = util.get_speechcon(correct_answer=True)
            attr["quiz_score"] += 1
            handler_input.attributes_manager.session_attributes = attr
        else:
            speech = util.get_speechcon(correct_answer=False)

        speech += util.get_answer(item_attr, item)

        if attr['counter'] < data.MAX_QUESTIONS:
            # Ask another question
            speech += util.get_current_score(
                attr["quiz_score"], attr["counter"])
            question = util.ask_question(handler_input)
            speech += question
            reprompt = question

            # Update item and item_attr for next question
            item = attr["quiz_item"]
            item_attr = attr["quiz_attr"]

            if data.USE_CARDS_FLAG:
                response_builder.set_card(
                    ui.StandardCard(
                        title="Question #{}".format(str(attr["counter"])),
                        text=question,
                        image=ui.Image(
                            small_image_url=util.get_small_image(item),
                            large_image_url=util.get_large_image(item)
                        )))

            if util.supports_display(handler_input):
                title = "Question #{}".format(str(attr["counter"]))
                background_img = Image(
                    sources=[ImageInstance(
                        util.get_image(
                            ht=1024, wd=600,
                            label=attr["quiz_item"]["abbreviation"]))])
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
            return response_builder.speak(speech).ask(reprompt).response
        else:
            # Finished all questions.
            speech += util.get_final_score(attr["quiz_score"], attr["counter"])
            speech += data.EXIT_SKILL_MESSAGE

            response_builder.set_should_end_session(True)

            if data.USE_CARDS_FLAG:
                response_builder.set_card(
                    ui.StandardCard(
                        title="Final Score".format(str(attr["counter"])),
                        text=(util.get_final_score(
                            attr["quiz_score"], attr["counter"]) +
                              data.EXIT_SKILL_MESSAGE)
                    ))

            if util.supports_display(handler_input):
                title = "Thank you for playing"
                primary_text = get_rich_text_content(
                    primary_text=util.get_final_score(
                        attr["quiz_score"], attr["counter"]))

                response_builder.add_directive(
                    RenderTemplateDirective(
                        BodyTemplate1(
                            back_button=BackButtonBehavior.HIDDEN,
                            title=title,
                            text_content=primary_text
                        )))

            return response_builder.speak(speech).response