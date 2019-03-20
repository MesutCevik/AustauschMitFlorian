from enum import Enum
from typing import List, Dict, Union, Tuple, Optional

import logging


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


class Calculator:
    def mul_div_calculator(self, mylist: List[str]) -> List[str]:
        if '*' in mylist:
            opindex = mylist.index('*')
            num1index = opindex - 1

            # Prepare the numbers for calculation:
            num1 = mylist[opindex - 1]
            num2 = mylist[opindex + 1]

            # Calculate the math task in the list:
            result_mul_div = num1 * num2
            print(f"Result of multiplication: {result_mul_div}")
            print()

            # Revise the list:
            mylist.insert((opindex + 2), result_mul_div)
            mylist.pop(num1index)
            mylist.pop(num1index)
            mylist.pop(num1index)
            print(f"Status after multiplication: {mylist}")
            print()

            # My awesome recursion:
            self.mul_div_calculator(mylist)

        elif '/' in mylist:
            opindex = mylist.index('/')
            num1index = opindex - 1

            num1 = mylist[opindex - 1]
            num2 = mylist[opindex + 1]

            result_mul_div = int(num1 / num2)
            print(f"Result of division: {result_mul_div}")
            print()

            mylist.insert((opindex + 2), result_mul_div)
            mylist.pop(num1index)
            mylist.pop(num1index)
            mylist.pop(num1index)
            print(f"Status after division: {mylist}")
            print()

            self.mul_div_calculator(mylist)

        else:
            # pass
            return mylist

    def add_sub_calculator(self, mylist: List[str]) -> List[str]:
        if '+' in mylist:
            opindex = mylist.index('+')
            num1index = opindex - 1

            num1 = mylist[opindex - 1]
            num2 = mylist[opindex + 1]

            result_add_sub = num1 + num2
            print(f"Result of addition: {mylist}")
            print()

            mylist.insert((opindex + 2), result_add_sub)
            mylist.pop(num1index)
            mylist.pop(num1index)
            mylist.pop(num1index)
            print(f"Status after addition: {mylist}")
            print()

            self.add_sub_calculator(mylist)

        elif '-' in mylist:
            opindex = mylist.index('-')
            num1index = opindex - 1

            num1 = mylist[opindex - 1]
            num2 = mylist[opindex + 1]

            result_add_sub = int(num1 - num2)
            print(f"Result of subraction: {mylist}")
            print()

            mylist.insert((opindex + 2), result_add_sub)
            mylist.pop(num1index)
            mylist.pop(num1index)
            mylist.pop(num1index)
            print(f"Status after subtraction: {mylist}")
            print()

        else:
            return mylist

    def bracket_term_calculator(self, math_task: List[str]) -> List[str]:
        mt_in_brackets_2 = []
        mt_in_brackets_3 = []

        if '(' and ')' in math_task:
            bracket_open = math_task.index('(')
            print(f"Index of bracket open: {bracket_open}.")
            bracket_close = math_task.index(')')
            print(f"Index of bracket close: {bracket_close}.")
            print()

            mt_in_brackets: list = math_task[bracket_open + 1: bracket_close]
            print(f"Math task in brackets: {mt_in_brackets}.")

            # Calculate the math task within the brackets:
            # 1st: Try to solve mul-div tasks
            result = self.mul_div_calculator(mt_in_brackets)
            mt_in_brackets_2.append(result)
            print(type(mt_in_brackets_2))
            print(f"Was kommt nach mul-div raus? {mt_in_brackets_2}")

            # 2nd: Try to solve add-sub tasks:
            mt_in_brackets_3.append(self.add_sub_calculator(mt_in_brackets))
            print(f"Was kommt nach add-sub raus? {mt_in_brackets_3}")

            # Within the origin math task delete the math term in brackets and the brackets itself!
            del math_task[bracket_open: bracket_close + 1]

            # Insert at the index of the bracket open the result of the the bracket term.
            # result_bracket_term = mt_in_brackets_3[:]
            math_task[bracket_open:bracket_open] = mt_in_brackets[:]

            print(f"Das Ergebnis des Klammerausdrucks ist: {mt_in_brackets}.")
            print(f"Hier die überarbeitete Mathe-Aufgabe: {math_task}")

            self.bracket_term_calculator(math_task)

        else:
            return math_task

    def master_calculator(self, math_task: List[str]) -> str:
        mt_no_brackets = []
        mt_no_mul_div = []
        mt_no_add_div = []

        # Zuerst Klammer-Ausdrücke ausrechnen:
        self.bracket_term_calculator(math_task)

        # Dann Punktrechnung ausrechnen:
        self.mul_div_calculator(math_task)

        # Zuletzt Plus-Minus-Rechnung ausrechnen
        self.add_sub_calculator(math_task)
        result = math_task[0]

        # Return das Ergebnis
        return result

    @staticmethod
    def helper_generate_slot_value(name: str, slot_position: int, number_as_str:str, resolved:str, is_validated: bool) -> SlotValue:
        sv = SlotValue()
        sv.name = name
        sv.slot_position = slot_position
        sv.number_as_str = number_as_str
        sv.resolved = resolved
        sv.is_validated = is_validated
        return sv

    @staticmethod
    def helper_generate_list_of_slotvalues(term: list) -> List[SlotValue]:
        slot_values: List[SlotValue] = []
        num_op = 0
        num_num = 0
        num_bracket = 0
        for index, item in enumerate(term):
            is_validated = True
            if item == "+":
                resolved = "OPERATOR_ADD"
                num_op += 1
                name = f"operator{num_op}"
            elif item == "-":
                resolved = "OPERATOR_SUB"
                num_op += 1
                name = f"operator{num_op}"
            elif item == "*":
                resolved = "OPERATOR_MUL"
                num_op += 1
                name = f"operator{num_op}"
            elif item == "/":
                resolved = "OPERATOR_DIV"
                num_op += 1
                name = f"operator{num_op}"
            elif item == "(":
                resolved = "OPERATOR_BRACKET_OPEN"
                num_bracket += 1
                name = f"num_bracket{num_bracket}"
            elif item == ")":
                resolved = "OPERATOR_BRACKET_CLOSE"
                num_bracket += 1
                name = f"num_bracket{num_bracket}"
            else:
                resolved = f"{item}"
                is_validated = False
                num_num += 1
                name = f"number{num_num}"

            sv = Calculator.helper_generate_slot_value(name=name, slot_position=index, number_as_str=f"{item}", resolved=resolved, is_validated=is_validated)
            slot_values.append(sv)

        return slot_values
        

if __name__ == '__main__':
    math_task_1 = [2, '*', 5, '+', '(', 7, '*', 4, ')', '-', 90, '/', 10]
    math_task_2 = [4, '*', 20, '+', '(', 12, '/', 4, '+', 17, ')', '-', 81, '/', 9]
    math_task_1_sv = Calculator.helper_generate_list_of_slotvalues(math_task_1)
    math_task_2_sv = Calculator.helper_generate_list_of_slotvalues(math_task_2)
    print(math_task_1_sv)
    print(math_task_2_sv)


    # print(f"The math task as a list: {math_task_1}")
    # result_math_task_1 = master_calculator(math_task_1)
    # print(f"Traraaaa. The result is: {result_math_task_1}")
    c = Calculator()
    print(f"The math task as a list: {math_task_2}")
    result_math_task_2 = c.master_calculator(math_task_2)
    print(f"The result is: {result_math_task_2}")