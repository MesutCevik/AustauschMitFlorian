# -*- coding: utf-8 -*-

# IMPORTANT: Please note that this template uses Display Directives,
# Display Interface for your skill should be enabled through the Amazon
# developer console
# See this screen shot - https://alexa.design/enabledisplay

import json
import logging
from typing import List, Dict, Any, Union

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.response_helper import (
    get_plain_text_content, get_rich_text_content)

from ask_sdk_model.interfaces.display import (
    ImageInstance, Image, RenderTemplateDirective, ListTemplate1,
    BackButtonBehavior, ListItem, BodyTemplate2, BodyTemplate1, BodyTemplate6, TextContent)
from ask_sdk_model import ui, Response, Slot, IntentRequest
from ask_sdk_model.slu.entityresolution import Resolutions, Resolution, StatusCode
from ask_sdk_model.ui import SimpleCard

from alexa import data, util


# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# TODO
# 1. Hessen als neuer amerikanischen Bundestadt hinzufügen und in prod testen >> DONE
# 2. füge einen mesut und flori intent hinzu, der auf hallo flori und hallo mesut reagiert mit hallo flori bzw. mesut


# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        handler_input.response_builder.speak(data.WELCOME_MESSAGE).ask(
            data.HELP_MESSAGE)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        print("Session ended with reason: {}".format(
            handler_input.request_envelope))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        handler_input.attributes_manager.session_attributes = {}
        # Resetting session

        handler_input.response_builder.speak(
            data.HELP_MESSAGE).ask(data.HELP_MESSAGE)
        return handler_input.response_builder.response


# MESUTS HANDLER: Greet Intent
class GreetIntentHandler(AbstractRequestHandler):
    """Handler for Greet Florian or Mesut and everybody else Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GreetIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GreetIntent")
        slots = handler_input.request_envelope.request.intent.slots

        name_user = slots["name"].value

        if name_user:
            speech_text = f"Hello {name_user} my friend!"

        else:
            speech_text = "Hello Python World from Classes!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)

        return handler_input.response_builder.response


# MESUTS HANDLER: Math Calc Intent
class MathCalcIntentHandler(AbstractRequestHandler):
    """Handler for Math Calc Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("MathCalcIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info(">>> MathCalcIntent: In MathCalcIntent")

        # Alle User-Eingaben in Slots in eine Variable "slots" reinpacken.
        slots = handler_input.request_envelope.request.intent.slots

        response_builder = handler_input.response_builder

        try:
            # Hole alle slot Werte aus "slots" mit der Methode get_slot_values() und speichere sie in "all_slots".
            # "get_slot_values() nimmt als Argument den gesamten Inhalt der slots ("slots") und liefert ein dictionary
            # "slot_values" mit den slot Werten in normalisierter Form, damit diese besser verarbeiten werden können.
            all_slots = get_slot_values(slots)
            logger.info(f">>> MathCalcIntent: Inhalt von all_slots: {all_slots}")

            # Definiere jeweils zwei Listen, um alle Nummern und alle Operatoren darin zu sammeln.
            all_number_slots = []
            all_numbers = []
            all_op_slots = []
            all_ops = []

            # Iteriere durch alle Key-Value-Paare im dictionary "all_slots"!
            # In Python Dictionary, items() method is used to return the list with all dictionary keys with values.
            numiter = 0
            opiter = 0
            for name, slot in all_slots.items():
                # slot.synonym und slot.resolved. für dich wichtig ist aber nur slot.resolved
                # if name hat prefix number, dann ist es ne Nummer. Füge es in die Liste all_number_slots hinzu!
                # if name hat prefix operator, dann ist es nen Operator. Füge es in die Liste all_op_slots hinzu!
                logger.info(f">>> MathCalcIntent: Slot: {name} - {slot}")
                if name.startswith("number"):
                    all_number_slots.append(slot)
                    logger.info(f">>> MathCalcIntent: all_number_slots: {all_number_slots}")

                    all_numbers.append(int(all_number_slots[numiter]['resolved']))
                    logger.info(f">>> MathCalcIntent: all_numbers: {all_numbers}")

                    numiter += 1

                elif name.startswith("operator"):
                    all_op_slots.append(slot)
                    logger.info(f">>> MathCalcIntent: all_op_slots: {all_op_slots}")

                    all_ops.append(all_op_slots[opiter]['resolved'])
                    logger.info(f">>> MathCalcIntent: all_ops: {all_ops}")

                    opiter += 1

                else:
                    # Irgendwas ist doof, ich kann nur number und operator, ich ignoriere einfach mal den Wert
                    speech_text = "Irgendwas ist doof, ich kann nur number und operator, ich ignoriere einfach mal den " \
                                  "Wert. Oh my God, something went wrong. Please try again."
                    continue

            result = 0

            if len(all_numbers) == 0:  # User typed no number.
                logger.info(">>> MathCalcIntent: need at least one number")
            elif len(all_numbers) == 1:  # User typed only one number.
                logger.info(f">>> MathCalcIntent: Yeah, you entered {all_numbers[0]}")
            else:
                logger.info(f">>> MathCalcIntent: Numbers OK!")
                # User typed two or more numbers, everything is OK. Carry on!
                # Check, if the amount of numbers is one more than the amount of the operators.
                if len(all_numbers) == (len(all_ops) + 1):
                    logger.info(f">>> MathCalcIntent: In 1st If-Condition. Numbers {len(all_numbers)} and Operators "
                                f"{len(all_ops)} are OK! Next step: calculate!")
                    # Alles in Ordnung, jetzt rechnen!

                    # While-Schleife, bis keine Zahlen und Operatoren mehr da sind!
                    while len(all_numbers) > 1:
                        num1 = all_numbers[0]
                        op = all_ops[0]
                        num2 = all_numbers[1]
                        logger.info(f">>> MathCalcIntent: In while-loop. Variables has the values: num1 = {num1}, "
                                    f"num2 = {num2}, op = {op}")

                        if op == "OPERATOR_ADD":
                            result = num1 + num2
                            speech_text = f"The sum of {num1} and {num2} is {result}. " \
                                f"Please add the next math question:"

                        elif op == "OPERATOR_SUB":
                            result = num1 - num2
                            speech_text = f"The substraction of {num2} from {num1} is {result}. " \
                                f"Please add the next math question:"

                        elif op == "OPERATOR_DIV":
                            result = int(num1 / num2)
                            speech_text = f"The division result of {num1} divided by {num2} is {result}. " \
                                f"Please add the next math question:"

                        elif op == "OPERATOR_MUL":
                            result = int(num1 * num2)
                            speech_text = f"The multiplication of {num1} and {num2} is {result}. " \
                                f"Please add the next math question:"

                        else:
                            speech_text = f"Sorry..."

                        # Entferne nach dem Rechnen die benutzten Nummern und den benutzen Operator aus den Listen!
                        all_numbers.pop(0)  # Lösche das erste Element in der Liste "all_number_slots"!
                        all_numbers.pop(0)  # Lösche das erste Element, das von der 2. Stelle gerückt ist, in "all_number_slots"!
                        all_ops.pop(0)  # Lösche den ersten Operator in der Liste "all_op_slots"!
                        all_numbers.insert(0, result)  # Weise das Rechenergebnis (neue Nummer) an die erste Stelle in der Liste "all_number_slots" zu!
                        logger.info(f">>> MathCalcIntent: all_numbers: {all_numbers}")
                        logger.info(f">>> MathCalcIntent: all_ops: {all_ops}")

                        logger.info(">>> MathCalcIntent: YEAH! First loop is done. Carry on!")
                else:
                    speech_text = "Oh my God, something went wrong. Please try again."
                    response_builder.speak(speech_text)
                    return response_builder.response

            logger.info(f">>> MathCalcIntent: all slots {all_slots}")
            logger.info(f">>> MathCalcIntent: Result = {result}")

            response_builder.speak(speech_text)
            response_builder.ask(speech_text)

        except ValueError:
            speech_text = "Sorry, I can't calculate this. Try saying two numbers like add 5 to 17."
            response_builder.speak(speech_text)
            return response_builder.response
        except TypeError as e:
            speech_text = f"Sorry, I can't calculate this. Try saying more than one number, at least two. {e}"
            response_builder.speak(speech_text)
            return response_builder.response
        except Exception as e:
            logger.info(f"MathCalcIntent exception {e}")
            speech_text = f"Sorry, there was an exception 'e'. Try it again and tell me a math task with two numbers. {e}"
            response_builder.speak(speech_text)
            return response_builder.response

        response_builder.set_card(ui.StandardCard(title="Math Quiz", text=speech_text))

        if util.supports_display(handler_input):
            response_builder.add_directive(
                RenderTemplateDirective(
                    BodyTemplate1(title="Math Answer",
                                  text_content=get_plain_text_content(primary_text=speech_text,  tertiary_text="toll"))
                )
            )

            return response_builder.response


def get_resolved_value(request: IntentRequest, slot_name: str) -> Union[str, None]:
    """Resolve the slot name from the request using resolutions."""

    try:
        return request.intent.slots[slot_name].resolutions.resolutions_per_authority[0].values[0].value.name
    except (AttributeError, ValueError, KeyError, IndexError, TypeError) as e:
        logger.info("Couldn't resolve {} for request: {}".format(slot_name, request))
        logger.info(str(e))
        return None


def get_slot_values(filled_slots: Dict[str, Slot]) -> Dict[str, Any]:
    """Return slot values with additional info."""
    slot_values = {}
    logger.info("Filled slots: {}".format(filled_slots))

    for key, slot_item in filled_slots.items():
        name = slot_item.name  # Z.B. "operatorOne"
        try:
            logger.info("Filled : {} - {}".format(name, slot_item.resolutions.resolutions_per_authority[0]))
            status_code = slot_item.resolutions.resolutions_per_authority[0].status.code

            if status_code == StatusCode.ER_SUCCESS_MATCH:
                slot_values[name] = {
                    "synonym": slot_item.value,
                    "resolved": slot_item.resolutions.resolutions_per_authority[0].values[0].value.name,
                    "is_validated": True,
                }
            elif status_code == StatusCode.ER_SUCCESS_NO_MATCH:
                slot_values[name] = {
                    "synonym": slot_item.value,
                    "resolved": slot_item.value,
                    "is_validated": False,
                }
            else:
                pass
        except (AttributeError, ValueError, KeyError, IndexError, TypeError) as e:
            logger.info("Couldn't resolve status_code for slot item: {}".format(slot_item))
            logger.info(e)
            slot_values[name] = {
                "synonym": slot_item.value,
                "resolved": slot_item.value,
                "is_validated": False,
            }
    logger.info("Filled slot values: {}".format(slot_values))

    return slot_values

class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop and Pause intents."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("AMAZON.PauseIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")
        handler_input.response_builder.speak(
            data.EXIT_SKILL_MESSAGE).set_should_end_session(True)
        return handler_input.response_builder.response


class QuizHandler(AbstractRequestHandler):
    """Handler for starting a quiz.

    The ``handle`` method will initiate a quiz state and build a
    question randomly from the states data, using the util methods.
    If the skill can use cards, then the question choices are added to
    the card and shown in the Response. If the skill uses display,
    then the question is displayed using RenderTemplates.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("QuizIntent")(handler_input) or
                is_intent_name("AMAZON.StartOverIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
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
                        ht=1024, wd=600, label=item["abbreviation"]))])
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


class DefinitionHandler(AbstractRequestHandler):
    """Handler for providing states info to the users.

    This handler is triggered when the QUIZ is not started and the
    user asks for a specific state, capital, statehood order, statehood
    year or abbreviation. Similar to the quiz handler, the information
    is added to the Card or the RenderTemplate after checking if that
    is supported.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AnswerIntent")(handler_input) and
                attr.get("state") != "QUIZ")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In DefinitionHandler")
        response_builder = handler_input.response_builder
        item, is_resolved = util.get_item(
            slots=handler_input.request_envelope.request.intent.slots,
            states_list=data.STATES_LIST)

        if is_resolved:
            if data.USE_CARDS_FLAG:
                response_builder.set_card(
                    ui.StandardCard(
                        title=util.get_card_title(item),
                        text=util.get_card_description(item),
                        image=ui.Image(
                            small_image_url=util.get_small_image(item),
                            large_image_url=util.get_large_image(item)
                        )))

            if util.supports_display(handler_input):
                img = Image(
                    sources=[ImageInstance(url=util.get_large_image(item))])
                title = util.get_card_title(item)
                primary_text = get_plain_text_content(
                    primary_text=util.get_card_description(item))

                response_builder.add_directive(
                    RenderTemplateDirective(
                        BodyTemplate2(
                            back_button=BackButtonBehavior.VISIBLE,
                            image=img, title=title,
                            text_content=primary_text)))

            response_builder.speak(
                util.get_speech_description(item)).ask(data.REPROMPT_SPEECH)

        else:
            response_builder.speak(
                util.get_bad_answer(item)).ask(util.get_bad_answer(item))

        return response_builder.response


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


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent.

     2018-May-01: AMAZON.FallackIntent is only currently available in
     en-US locale. This handler will not be triggered except in that
     locale, so it can be safely deployed for any locale."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        handler_input.response_builder.speak(
            data.FALLBACK_ANSWER).ask(data.HELP_MESSAGE)

        return handler_input.response_builder.response


# Interceptor classes
class CacheResponseForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the response sent to the user in session.

    The interceptor is used to cache the handler response that is
    being sent to the user. This can be used to repeat the response
    back to the user, in case a RepeatIntent is being used and the
    skill developer wants to repeat the same information back to
    the user.
    """
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["recent_response"] = response


# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.

    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


# Request and Response Loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Envelope: {}".format(
            handler_input.request_envelope))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Response: {}".format(response))


# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(QuizHandler())
sb.add_request_handler(DefinitionHandler())
sb.add_request_handler(QuizAnswerHandler())
sb.add_request_handler(QuizAnswerElementSelectedHandler())
sb.add_request_handler(RepeatHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(GreetIntentHandler())
sb.add_request_handler(MathCalcIntentHandler())


# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Add response interceptor to the skill.
sb.add_global_response_interceptor(CacheResponseForRepeatInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()
