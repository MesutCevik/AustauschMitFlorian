import math
import re
from enum import Enum
from typing import List


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

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.resolved}"


class Calculator:

    def mul_div_calculator(self, math_term_mul_div: List[SlotValue]) -> List[SlotValue]:
        # This method calculates all multiplication and division tasks in the math term, which is passed by the
        # argument "math_term_mul_div". In "math_term_mul_div" is a list of SlotValue objects. Each object stores one
        # of the requiered numbers or operators within the variable "resolved".
        result_mul_div: int
        op_idx: int = 0
        op_mul_div: int = 0

        print(f"math_term_mul_div: {math_term_mul_div}")

        # STEP 1: Check whether a multiplication or division operator is in the math term.
        for sv_item in math_term_mul_div:
            if sv_item.resolved in ("OPERATOR_MUL", "OPERATOR_DIV"):
                op_mul_div += 1
                print(f"resolved: {sv_item.resolved}")

        # STEP 2: If there is 1 or more mul/div operator in the math term, then continue in this method.
        # Else return the current state of the math term.
        if op_mul_div <= 0:
            return math_term_mul_div

        # STEP 3: Find the first mul/div operator in the list "math_term_mul_div" and save its index in a variable.
        # Then determine the number1 (one index BEFORE the operator) and number2 (one index AFTER the operator).
        # Because the values of "resolved" field is a str, cast them to int!
        for sv_item in math_term_mul_div:
            if sv_item.resolved in ("OPERATOR_MUL", "OPERATOR_DIV"):
                op_idx = math_term_mul_div.index(sv_item)
                num1 = int(math_term_mul_div[op_idx - 1].resolved)
                num2 = int(math_term_mul_div[op_idx + 1].resolved)

                # STEP 4: Calculate the math term as we have number1, operator and number2:
                if math_term_mul_div[op_idx].resolved == "OPERATOR_MUL":
                    result_mul_div = num1 * num2
                elif math_term_mul_div[op_idx].resolved == "OPERATOR_DIV":
                    result_mul_div = int(num1 / num2)

                print(f"The result of mul./div. is: {result_mul_div}")

        # STEP 5: Generate a new SlotValue()-object in order to save the calculated result (number):
        sv_item_new_num = Calculator.helper_generate_slot_value(name=f"number{op_idx - 1}", slot_position=op_idx - 1,
                                                                number_as_str=str(result_mul_div),
                                                                resolved=str(result_mul_div), is_validated=False)
        print(f"sv_item_new_num: {sv_item_new_num}")
        print()

        # STEP 6: Revise the list "math_term_mul_div":
        # 1.) Insert the new object "sv_item_new_num" at position "op_idx - 1", this is the starting index of the
        # calculated math term.
        # 2.) Pop the items, from which we take num1, operator and num2, at index "op_idx", one position after
        # the inserted new slot with the result.
        math_term_mul_div.insert(op_idx - 1, sv_item_new_num)
        del math_term_mul_div[op_idx]
        del math_term_mul_div[op_idx]
        del math_term_mul_div[op_idx]
        print(f"math_term_mul_div AFTER calculation: {math_term_mul_div}")
        print()

        # STEP 7: RECURSION > Start this method again with the updated list "math_term_mul_div" in order solve other
        # mul/div math term.:
        return self.mul_div_calculator(math_term_mul_div)

    def add_sub_calculator(self, math_term_add_sub: List[SlotValue]) -> List[SlotValue]:
        result_add_sub: int
        op_idx: int = 0
        op_add_sub: int = 0

        print(f"math_term_add_sub: {math_term_add_sub}")

        for sv_item in math_term_add_sub:
            if sv_item.resolved in ("OPERATOR_ADD", "OPERATOR_SUB"):
                op_add_sub += 1

        if op_add_sub <= 0:
            return math_term_add_sub

        for sv_item in math_term_add_sub:
            if sv_item.resolved in ("OPERATOR_ADD", "OPERATOR_SUB"):
                op_idx = math_term_add_sub.index(sv_item)
                num1 = int(math_term_add_sub[op_idx - 1].resolved)
                num2 = int(math_term_add_sub[op_idx + 1].resolved)

                if math_term_add_sub[op_idx].resolved == "OPERATOR_ADD":
                    result_add_sub = num1 + num2
                elif math_term_add_sub[op_idx].resolved == "OPERATOR_SUB":
                    result_add_sub = int(num1 - num2)

                print(f"The result of add/sub is: {result_add_sub}")
                break

        sv_item_new_num = Calculator.helper_generate_slot_value(name=f"number{op_idx - 1}", slot_position=op_idx - 1,
                                                                number_as_str=str(result_add_sub),
                                                                resolved=str(result_add_sub), is_validated=False)
        print(f"sv_item_new_num: {sv_item_new_num}")
        print()

        math_term_add_sub.insert(op_idx - 1, sv_item_new_num)
        math_term_add_sub.pop(op_idx)
        math_term_add_sub.pop(op_idx)
        math_term_add_sub.pop(op_idx)
        print(f"math_term_mul_div AFTER calculation: {math_term_add_sub}")
        print(f"The length of 'math_term_mul_div' is: {len(math_term_add_sub)}")
        print()

        return self.add_sub_calculator(math_term_add_sub)

    def math_term_in_brackets_calculator(self, math_term_with_brackets: List[SlotValue]) -> List[SlotValue]:
        m_p_bracket_open = 0
        m_p_bracket_close = 0
        m_t_result: SlotValue

        # Count the number of open and close brackets.
        for sv_item in math_term_with_brackets:
            if sv_item.resolved == "OPERATOR_BRACKET_OPEN":
                m_p_bracket_open += 1
            elif sv_item.resolved == "OPERATOR_BRACKET_CLOSE":
                m_p_bracket_close += 1

        # Check whether there are brackets and whether the amount of open brackets is equal to close brackets.
        if (m_p_bracket_open == m_p_bracket_close) and (m_p_bracket_open > 0):
            op_bracket_open_idx: int
            op_bracket_close_idx: int

            # Loop through the items (SlotValue objects) in math_term_with_brackets. Search for the first close
            # bracket and its counterpart open bracket. Assign and save the slot positions for these brackets in
            # separate VARs. Because the elif-part saves always the index of the last open bracket, we will have both
            # counterpart brackets, when we have found the close bracket.
            for sv_item in math_term_with_brackets:
                if sv_item.resolved == "OPERATOR_BRACKET_CLOSE":
                    op_bracket_close_idx = math_term_with_brackets.index(sv_item)
                    print(f"Index of first close bracket: {op_bracket_close_idx}.")
                    break

                elif sv_item.resolved == "OPERATOR_BRACKET_OPEN":
                    op_bracket_open_idx = math_term_with_brackets.index(sv_item)
                    print(f"Index of last open bracket: {op_bracket_open_idx}.")


            # Extract the math term within the brackets. For this slice the elements (SlotValue objects) in m_p_list_sv
            # after the determined open bracket up to the determined close bracket - without the close bracket.
            # Save all slot_value objects in a VAR as a List[SlotValue].
            math_term_in_brackets: List[SlotValue] = math_term_with_brackets[op_bracket_open_idx + 1:op_bracket_close_idx]
            print(f"Content of 'math_term_in_brackets': {math_term_in_brackets}")

            # To show the math term within brackets, we print the result of extraction:
            to_show = [math_term_in_brackets[x].resolved for x in range(0, len(math_term_in_brackets))]
            print(f"Math term in brackets: {to_show}")

            # Calculate the math term within the brackets:
            for sv_item in math_term_in_brackets:
                # 1st: Try to solve multiplications or divisions problem.
                if sv_item.resolved in ("OPERATOR_MUL", "OPERATOR_DIV"):
                    m_t_result = self.mul_div_calculator(math_term_in_brackets)
                    # math_term_in_brackets = result
                    print(f"Result after mul-div calculation: {m_t_result}")

                # 2nd: Try to solve add-sub tasks:
                elif sv_item.resolved in ("OPERATOR_ADD", "OPERATOR_SUB"):
                    m_t_result = self.add_sub_calculator(math_term_in_brackets)
                    # math_term_in_brackets = result
                    print(f"Result after add-sub calculation: {m_t_result}")

            # Insert the whole elements from "m_t_result" into the origin maths problem list "m_p_list_sv" at the index
            # [op_bracket_close_idx + 1]. "result" contains the slot_value objects with the math term elements.
            # math_term_with_brackets[op_bracket_close_idx + 1] = m_t_result[:]
            # math_term_with_brackets.insert(op_bracket_close_idx + 1, m_t_result)

            for pos, tmp_item in enumerate(m_t_result, start=1):
                math_term_with_brackets.insert(op_bracket_close_idx + pos, tmp_item)

            # Within the origin maths problem delete the math term in brackets and the brackets itself!
            del math_term_with_brackets[op_bracket_open_idx:op_bracket_close_idx + 1]

            print(f"Result of the math term within the brackets: {m_t_result.__str__()}.")
            print(f"Maths problem updatet: {math_term_with_brackets.__str__()}")

            # Recursion: Try it again to solve another existing math term within brackets.
            return self.math_term_in_brackets_calculator(math_term_with_brackets)

        else:
            return math_term_with_brackets

    def trigonometry_and_power_calculator(self, math_term_mul_div: List[SlotValue]) -> List[SlotValue]:
        # Calculates trigonometry and power tasks.

        # for sv_item in math_term_mul_div:
        #     if sv_item.resolved in ("OPERATOR_MUL", "OPERATOR_DIV"):
        #         op_mul_div += 1
        #         print(f"resolved: {sv_item.resolved}")

        for sv_item in math_term_mul_div:
            number = sv_item.resolved

            if "^" in number:  # 4^2 = 4 * 4 = 16
                parts = number.split("^")
                """
                If sep is given, consecutive delimiters are not grouped together and are deemed to delimit empty strings 
                (for example, '1,,2'.split(',') returns ['1', '', '2']). 
                https://docs.python.org/3/library/stdtypes.html#str.split
                """
                parts = list(filter(None, parts))
                if len(parts) != 2:
                    raise ValueError("In der Potenzrechnung stimmt etwas nicht. Bitte wiederholen sie die Aufgabe.")
                base = float(parts[0])
                exponent = float(parts[1])
                number = math.pow(base, exponent)

            elif "cos" in number:  # e.g. cos(25.76)
                cos_num_str = re.findall('[0-9]+', number)  # 25.76
                cos_num_float = float(cos_num_str[0])  # convert to float.
                cos_solution = math.cos(cos_num_float)  # calculate cosinus with math-module.
                number = cos_solution
                number = round(number, 3)

            elif "sin" in number:  # e.g. sin(16.86)
                sin_num_str = re.findall('[0-9]+', number)  # 16.86
                sin_num_float = float(sin_num_str[0])  # convert to float.
                sin_solution = math.cos(sin_num_float)  # calculate cosinus with math-module.
                number = sin_solution
                number = round(number, 3)

            elif "tan" in number:  # e.g. tan(90.54)
                tan_num_str = re.findall('[0-9]+', number)  # 90.54
                tan_num_float = float(tan_num_str[0])  # convert to float.
                tan_solution = math.cos(tan_num_float)  # calculate cosinus with math-module.
                number = tan_solution
                number = round(number, 3)

            elif "sqrt" in number:  # e.g. sqrt(36)
                sqrt_num_str = re.findall('[0-9]+', number)  # 36
                sqrt_num_float = float(sqrt_num_str[0])  # convert to float.
                sqrt_solution = math.sqrt(sqrt_num_float)  # calculate square root with math-module.
                number = sqrt_solution
                number = round(number, 3)

            else:
                number = float(number)

            # Assigns the calculated number back to the SlotValue object.
            sv_item.resolved = str(number)

        return self.mul_div_calculator(math_term_mul_div)

    def master_calculator(self, maths_problem_1_sv: List[SlotValue]) -> List[SlotValue]:

        # (0.) Trigonometrische, Poten- und Wurzelzaufgaben zuerst ausrechnen:
        self.trigonometry_and_power_calculator(maths_problem_1_sv)

        # (1.) Zuerst Klammer-Ausdrücke ausrechnen:
        self.math_term_in_brackets_calculator(maths_problem_1_sv)

        # (2.)Dann Punktrechnung ausrechnen:
        self.mul_div_calculator(maths_problem_1_sv)

        # (3.)Zuletzt Plus-Minus-Rechnung ausrechnen
        self.add_sub_calculator(maths_problem_1_sv)
        m_p_result = maths_problem_1_sv[:]

        # Return das Ergebnis
        return m_p_result

    @staticmethod
    def helper_generate_slot_value(name: str, slot_position: int, number_as_str: str, resolved: str,
                                   is_validated: bool) -> SlotValue:
        sv = SlotValue()
        sv.name = name
        sv.slot_position = slot_position
        sv.number_as_str = number_as_str
        sv.resolved = resolved
        sv.is_validated = is_validated
        return sv

    @staticmethod
    def helper_generate_list_of_slot_values(term: list) -> List[SlotValue]:
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

            # Erzeuge ein slot_value Objekt. Dazu wird innerhalb der Klasse "Calculator" die Methode
            # "helper_generate_slot_value" aufgerufen und die Variablen aus der for-Schleife von oben als Argumente
            # übergeben. Zurück kommt ein Objekt der Klasse "Slot_Value" inkl. ausgefüllter Variablen.
            sv = Calculator.helper_generate_slot_value(name=name, slot_position=index, number_as_str=f"{item}",
                                                       resolved=resolved, is_validated=is_validated)

            # Das erzeugte "Slot_Value"-Objekt "sv" wird in die Liste "slot_values" eingefügt, mit all seinen Variablen
            # und Werten.
            slot_values.append(sv)

        return slot_values

    # @staticmethod
    # def print_maths_problem_as_list(maths_problem: List[SlotValue]) -> List[str]:
    #     # Print maths problem status as list in order to show the status.
    #     maths_problem_4_print = maths_problem
    #     maths_problem_as_list = []
    #
    #     for elem in maths_problem_4_print:
    #         idx_elem = 0
    #         maths_problem_as_list.append(elem.resolved)
    #         idx_elem += 1
    #
    #     return maths_problem_as_list


if __name__ == '__main__':
    # The 1st maths problem as a list:
    # maths_problem_1 = [2, '*', 5, '+', '(', 7, '*', 4, ')', '-', 90, '/', 10]
    # maths_problem_1 = ['(', 8, '/', '(', 8, '/', 2, ')', ')', '*', 3, '+', '(', 8, '/', 2, ')']
    # maths_problem_1 = ['(', 8, '/', '(', 8, '/', 2, ')', ')', '*', 3, '+', '(', 51, '*', '(', 8, '/', 2, ')', '-',
    # 73, ')']
    maths_problem_1 = ['(', '(', 8, '/', '(', 8, '/', 2, ')', ')', '*', 30, ')', '-', 24, '*', 3, '+', '(', 51, '*',
                       '(', 8, '/', 2, ')', '-', 73, ')']

    # Calls the method "helper_generate..." from the class "Calculator" in order to generate a list of SlotValue
    # objects, which contains the maths problems numbers and operators:
    maths_problem_1_sv = Calculator.helper_generate_list_of_slot_values(maths_problem_1)

    print(f"The maths problem as a list in 'maths_problem_1': {maths_problem_1}")
    print(f"The maths problem as a list of SlotValue objects in 'maths_problem_1_sv': {maths_problem_1_sv}")
    print(f"The first SlotValue object in 'maths_problem_1_sv': {maths_problem_1_sv[0]}")
    print()

    # Generates a standard object from the class "Calculator" and assigns it to VAR 'c'.
    c = Calculator()

    result_maths_problem_1_sv = c.master_calculator(maths_problem_1_sv)
    result = int(result_maths_problem_1_sv[0].resolved)
    print(f"THE RESULT IS: {result}")

    # The 2nd maths problem:
    # maths_problem_2 = [4, '*', 20, '+', '(', 12, '/', 4, '+', 17, ')', '-', 81, '/', 9]
    # maths_problem_2_sv = Calculator.helper_generate_list_of_slot_values(maths_problem_2)

    # print(f"The maths problem as a list: {maths_problem_2}")
    # result_math_task_2 = c.master_calculator(maths_problem_2_sv)
    # print(f"The result is: {result_math_task_2}")

    # Prints the maths problem as a list:
    # idx_elem = 0
    # list_elem = []
    # for elem in maths_problem_1_sv:
    #     list_elem.append(maths_problem_1_sv[idx_elem].resolved)
    #     idx_elem += 1
    # print(list_elem)
