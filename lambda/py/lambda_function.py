# -*- coding: utf-8 -*-

# IMPORTANT: Please note that this template uses Display Directives,
# Display Interface for your skill should be enabled through the Amazon
# developer console
# See this screen shot - https://alexa.design/enabledisplay

import logging
from enum import Enum
from typing import List, Dict, Union, Tuple

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.response_helper import (
    get_plain_text_content)

from ask_sdk_model.interfaces.display import (
    ImageInstance, Image, RenderTemplateDirective, BackButtonBehavior, BodyTemplate2, BodyTemplate1)
from ask_sdk_model import ui, Response, Slot, IntentRequest
from ask_sdk_model.slu.entityresolution import StatusCode

from alexa import data, util

# Skill Builder object
from lambda_function_greet import GreetIntentHandler
from lambda_function_quiz import QuizHandler
from lambda_function_quiz_answer import QuizAnswerHandler
from lambda_function_quiz_answer_element import QuizAnswerElementSelectedHandler
from lambda_function_repeat import RepeatHandler

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SlotType(Enum):
    operator = 1
    number = 2


class SlotValue:
    name: str
    type: SlotType
    synonym: str
    resolved: str
    is_validated: bool
    number_as_str: str
    slot_position: int


# TODO: Vielleicht hier eine eigene Klasse zurückgeben, mit den feldern: master_list, result as int,
#  result as text_speechtext? CalcResult

class CalcResult:
    mst_list = List[SlotValue]
    result_as_int = int
    result_as_speechtext = str

# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In LaunchRequestHandler")
        handler_input.response_builder.speak(data.WELCOME_MESSAGE).ask(data.HELP_MESSAGE)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In SessionEndedRequestHandler")
        print("Session ended with reason: {}".format(handler_input.request_envelope))
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


# MESUTS HANDLER: Math Calc Intent
class MathCalcIntentHandler(AbstractRequestHandler):
    result = 0

    """Handler for Math Calc Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("MathCalcIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info(">>> MathCalcIntent: In MathCalcIntent")

        # Alle User-Eingaben in Slots in eine Variable "slots" reinpacken.
        slots = handler_input.request_envelope.request.intent.slots
        logger.info(f">>> MathCalcIntent: slots in Rohform: {slots}")

        speech_text = None
        response_builder = handler_input.response_builder

        master_list = None

        try:
            # 1.) Hole alle slot Werte aus "slots" mit der Methode get_slot_values() und speichere sie in "all_slots".
            # "get_slot_values() nimmt als Argument den gesamten Inhalt der slots ("slots") und liefert ein dictionary
            # "slot_values" mit den slot Werten in normalisierter Form, damit diese besser verarbeiten werden können.
            all_slots: Dict[str, SlotValue] = get_slot_values(slots)
            logger.info(f">>> MathCalcIntent: Inhalt von all_slots: {all_slots}")

            # 2.) Trenne alle Nummern und Operatoren und packe sie in separate Listen in der Reihenfolge ihrer Eingaben.
            num_4_calc, ops_4_calc = self.generate_num_op_lists(all_slots)

            # 3.) Prüfe die Anzahl der Nummern und Operatoren, ob daraus ein logischer Mathematik-Ausdruck gebildet
            # werden kann, also ob die Mathe-Aufgabe stimmt.
            result, speech_text = self.check_amount_nums_and_ops(num_4_calc, ops_4_calc)
            if result and not speech_text:
                # 4.) Erzeuge eine master_list aus den Listen num_4_calc und ops_4_calc!
                master_list = self.generate_master_list(num_4_calc, ops_4_calc)
            else:
                return speech_text

            math_task_result = self.calculate_the_math_task(master_list)
            speech_text = f"The result for your math task is: {math_task_result}."

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
            speech_text = f"Sorry, there was an exception 'e'. Try it again and tell me a math task with " \
                f"two numbers. {e}"
            response_builder.speak(speech_text)
            return response_builder.response

        # Return the result of the math task with the text in speech_text:
        response_builder.speak(speech_text)
        response_builder.ask(speech_text)

        # Erzeuge Card zur Anzeige auf Display von entsprechenden Amazon-Geräten:
        response_builder.set_card(ui.StandardCard(title="Math Quiz", text=speech_text))

        if util.supports_display(handler_input):
            response_builder.add_directive(
                RenderTemplateDirective(
                    BodyTemplate1(title="Math Answer",
                                  text_content=get_plain_text_content(primary_text=speech_text, tertiary_text="toll"))
                )
            )

        return response_builder.response

    def check_amount_nums_and_ops(self, numbers_4_calc, operators_4_calc) -> Tuple[bool, str]:
        # Prüft, ob Anzahl der Zahlen und Operatoren logisch ist für eine Mathe-Aufgabe.
        # Liefert einen Tuple mit bool (True, logisch OR False, nicht logisch) und str (speech_text) zurück.

        if len(numbers_4_calc) == 0:
            # User typed no number.
            logger.info(">>> MathCalcIntent: need at least one number")
            speech_text = "You haven't typed any number. Please type your math task."
            return False, speech_text

        if len(numbers_4_calc) == 1:
            # User typed only one number.
            logger.info(f">>> MathCalcIntent: Yeah, you entered {numbers_4_calc['numberOne']['resolved']}")
            return True, ""

        logger.info(f">>> MathCalcIntent: Numbers OK!")
        # User typed two or more numbers, everything is OK. Carry on!

        if len(numbers_4_calc) == (len(operators_4_calc) + 1):
        # Check, if the amount of numbers is one more than the amount of the operators.
            logger.info(f">>> MathCalcIntent: The amount of Numbers {len(numbers_4_calc)} and Operators "
                        f"{len(operators_4_calc)} is OK! Next step: calculate the math task!")
            # Wenn Anzahl Nummern u. Operatoren OK, dann True u. leeren String zurückgeben.
            return True, ""
        else:
            speech_text = "Oh my God, something went wrong. Please try again."
            return False, speech_text

    def generate_num_op_lists(self, all_slots: Dict[str, SlotValue]) -> Tuple[List[SlotValue], List[SlotValue]]:
        # Eine finale Liste mit SlotValue-Objekten erstellen, in der alle Zahlen (Operanden) und Operatoren
        # in der Reihenfolge ihrer Eingabe gespeichert sind.

        for name, slot in all_slots.items():
            # Iteriere durch alle Key-Value-Paare in all_slots. Unterscheide die Elemente nach dem Namen in Nummern und
            # Operatoren, speichere dafür im Value (Objekt 'slot') den SlotTyp (siehe oben!) und die Nummer, welcher
            # aus dem Namen getrennt wurde.
            if name.startswith("number"):
                # Wenn der Name des Elements aus all_slots mit "number" beginnt, dann tue dies:
                # Setze zuerst die VAR type im slot Objekt auf den Typ 'SlotType.number'!
                # Speichere in VAR number des slot Objekts den Slice des Namens, der nach 'number' kommt, z.B. 'One'!
                slot.type = SlotType.number
                slot.number = name.split("number", 1)  # "number" = Separator, 1 = maximal einmal separieren.
            elif name.startswith("operator"):
                # Das ganze von oben hier abarbeiten, wenn Name des Elements aus all_slots mit "operator" beginnt:
                slot.type = SlotType.operator
                slot.number = name.split("operator", 1)

            logger.info(f">>> MathCalcIntent: Slot: {name} - {slot} {slot.number}")

        possible_num_values = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']

        for name, slot_value in all_slots.items():
            # Iteriere durch alle Key-Value-Paare in all_slots. Nehme aus dem Value slot_value den Wert der VAR
            # number_as_str. Ermittle dann mit diesem Wert den dazugehörigen Index in der Liste possible_num_values.
            # Erhöhe den Index um 1 und weise das Ergebnis der VAR position_in_list zu.
            # Zum Schluss füge position_in_list in die VAR number_as_int in slot_value.
            logger.info(f">>> MathCalcIntent: num_slot = {name} {slot_value}")
            position_in_list = possible_num_values.index(slot_value.number_as_str) + 1
            slot_value.slot_position = position_in_list

        # Erzeuge und befülle die Listen num_4_calc und ops_4_calc!
        # Z1 Stark verkürzte Schreibeweise (list comprehension) für:
        # for-loop: Iteriere durch die Elemente (Key-Value-Paare) von all_slots.
        # Die if-condition: Enthält VAR 'type' in 'slot_value' den Wert 'SlotType.number'? Wenn für ein Element
        # die if-Bedingung gilt, dann weise alle Werte des betrachteten slots (ein dictionary) mit dem Namen 'name' in
        # die Liste 'num_4_calc'.
        # !!! The method values() returns a list of all the values available in a given dictionary.!!!
        # Z2 Dasselbe wie oben für die Operatoren.
        num_4_calc: List[SlotValue] = {name: slot_value for name, slot_value in all_slots.items() if
                                       slot_value.type == SlotType.number}.values()
        ops_4_calc: List[SlotValue] = {name: slot_value for name, slot_value in all_slots.items() if
                                       slot_value.type == SlotType.operator}.values()

        # Z1 Sortiere die Liste num_4_calc mit der lambda function.
        # Z2 Sortiere die Liste ops_4_calc mit der lambda function.
        num_4_calc.sort(key=lambda x: x.number_as_int)
        ops_4_calc.sort(key=lambda x: x.number_as_int)

        return num_4_calc, ops_4_calc

    def generate_master_list(self, num_4_calc, ops_4_calc) -> List[SlotValue]:
        # Erzeugt eine Liste mit allen Nummern- und Operatoren in der Reihenfolge aus der Mathe-Aufgabe.
        # Die Elemente dieser Liste sind vom Typ SlotValue.
        master_list: [SlotValue] = []

        # Iteriert durch alle alle Zahlen in num_4_calc und Operatoren in ops_4_calc der Reihe nach durch:
        # 1.) Nimmt zuerst die erste Zahl in num_4_calc und fügt sie in master_list hinten an. Dann löscht es diese Zahl
        # in der urprünglichen Liste.
        # 2.) Nimmt dann den ersten Operator in ops_4_calc und fügt sie in master_list hinten an. Dann löscht es
        # den Operator in der urprünglichen Liste.
        # 3.) Nimmt als drittes wieder die erste Zahl (die Zahlen sind vorgerückt, weil in 1.) eine Zahl gelöscht
        # wurde) und fügt sie in master_list hinten an. Dann löscht es die Zahl in der urprünglichen Liste.
        while len(num_4_calc) > 0 and len(ops_4_calc) > 0:
            master_list.append(num_4_calc.pop(0))
            master_list.append(ops_4_calc.pop(0))
            master_list.append(num_4_calc.pop(0))

        return master_list

    def calculate_the_math_task(self, master_list) -> CalcResult:
    # Berechnet anhand der master_list die ganze Mathe-Aufgabe. Gibt einen Tuple zurück mit master_list, calc_result
    # und speech_text zurück.
        mst_list = master_list

        result = 0

        while len(mst_list) > 1:
            op = mst_list[1]  # Das 2. Element ist immer ein Operator.
            num1 = mst_list[0]  # Das 1. Element ist immer eine Zahl.
            num2 = mst_list[2]  # Das 3. Element ist immer eine Zahl.
            # for op in operators:
                # num1 = numbers[0]
                # num2 = numbers[1]
            logger.info(f">>> MathCalcIntent: Calculation with: num1 = {num1}, "
                        f"num2 = {num2}, op = {op}")

            if op == "OPERATOR_ADD":
                result = num1 + num2

            elif op == "OPERATOR_SUB":
                result = num1 - num2

            elif op == "OPERATOR_DIV":
                result = int(num1 / num2)

            elif op == "OPERATOR_MUL":
                result = int(num1 * num2)

            else:
                speech_text = f"Sorry, I can´t calculate your math task!"

            # Entferne nach dem Rechnen die benutzten Nummern und den benutzen Operator aus den Listen!
            mst_list.pop(0)  # Lösche das erste Element in der Liste "mst_list", welches eine Zahl ist!
            mst_list.pop(0)  # Lösche das erste Element, das von der 2. Stelle gerückt ist und ein Operator ist!
            mst_list.pop(0)  # Lösche das erste Element, das von der 3. Stelle gerückt ist und eine Zahl ist!
            mst_list.insert(0, result)  # Füge das errechnete Ergebnis an die 1. Stelle in der Liste 'mst_list'!

            logger.info(">>> MathCalcIntent: YEAH! First loop is done. Carry on!")
            logger.info(f">>> MathCalcIntent: Status der Liste mit allen ops und nums 'mst_list': {mst_list}")

            # TODO: Vielleicht hier eine eigene Klasse zurückgeben, mit den feldern: master_list, result as int,
            #  result as text_speechtext?

        # Wenn alles gut gegangen ist mit der Berechnung:
        speech_text = f"The result of the math task is: {mst_list}. Please add the next math question:"

        # Erzeuge ein Objekt der Klasse CalcResult() und weise es calc_result zu!
        calc_result = CalcResult()

        # Befülle die Variablen des Objekts calc_result:
        calc_result.mst_list = master_list
        calc_result.result_as_int = mst_list
        calc_result.result_as_speechtext = speech_text

        return calc_result

def get_resolved_value(request: IntentRequest, slot_name: str) -> Union[str, None]:
    """ Resolve the slot name from the request using resolutions."""

    try:
        return request.intent.slots[slot_name].resolutions.resolutions_per_authority[0].values[0].value.name
    except (AttributeError, ValueError, KeyError, IndexError, TypeError) as e:
        logger.info("Couldn't resolve {} for request: {}".format(slot_name, request))
        logger.info(str(e))
        return None


def get_slot_values(filled_slots: Dict[str, Slot]) -> Dict[str, SlotValue]:
    """Return slot values with additional info."""
    slot_values = {}
    logger.info(f"Filled slots: {filled_slots}")

    # Iteriert durch alle Elemente des Dictionaries filled_slots und speichert verschiedene Werte daraus
    # im Objekt slot_value in dessen Variablen ab: slot_value.synonym, ..name, .. resolved, ..is_validated.
    for key, slot_item in filled_slots.items():
        name = slot_item.name  # Z.B. "operatorOne"
        try:
            logger.info(f"Filled : {name} - {slot_item.resolutions.resolutions_per_authority[0]}")
            status_code = slot_item.resolutions.resolutions_per_authority[0].status.code

            slot_value = SlotValue()  # Erzeuge ein SlotValue()-Objekt und weise es der VAR slot_value zu.
            slot_value.synonym = slot_item.value  # Speichere slot_item.value im Objekt slot_value unter synonym ab.
            slot_value.name = name  # Speichere name (siehe oben!) im Objekt slot_value unter name ab.

            # Wenn VAR status_code (siehe oben!) den Wert 'ER_SUCCESS_MATCH' hat wie das Objekt StatusCode, dann
            # speichere im Objekt slot_value in die VAR resolved und VAR is_validated folgende Daten ab:
            if status_code == StatusCode.ER_SUCCESS_MATCH:
                slot_value.resolved = slot_item.resolutions.resolutions_per_authority[0].values[0].value.name,
                slot_value.is_validated = True

            elif status_code == StatusCode.ER_SUCCESS_NO_MATCH:
                slot_value.resolved = slot_item.value,
                slot_value.is_validated = False

            # Speichere jetzt alle slot_value Objekte in der Liste slot_values unter dem jeweiligen Namen des Slots ab:
            slot_values[name] = slot_value

        except (AttributeError, ValueError, KeyError, IndexError, TypeError) as e:
            logger.info(f"Couldn't resolve status_code for slot item: {slot_item}")
            logger.info(e)
    logger.info(f"Filled slot values: {slot_values}")

    return slot_values


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop and Pause intents."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("AMAZON.PauseIntent")(handler_input))

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In ExitIntentHandler")
        handler_input.response_builder.speak(
            data.EXIT_SKILL_MESSAGE).set_should_end_session(True)
        return handler_input.response_builder.response


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
