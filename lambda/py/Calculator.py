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

    def mul_div_calculator(self, m_p_list_sv: List[SlotValue]) -> List[SlotValue]:
        # Loop through the slot value items in m_p_list_sv. Search for the first operater and check, whether the
        # operator is a subtraction or division one. Assign and save the slot positions for this operator in a VAR.
        for sv_item in m_p_list_sv:
            if sv_item.resolved == "OPERATOR_SUB":
                slot_pos_operator = sv_item.slot_position
                num1_index = slot_pos_operator - 1

                # Prepare the numbers for calculation:
                num1 = m_p_list_sv[slot_pos_operator - 1].resolved
                num2 = m_p_list_sv[slot_pos_operator + 1].resolved

                # Calculate the math term in the list:
                result_mul_div = num1 * num2
                print(f"Result of multiplication: {result_mul_div}")
                print()


            elif sv_item.resolved == "OPERATOR_BRACKET_OPEN":
                slot_pos_bracket_open = sv_item.slot_position
                print(f"Slot position of open bracket: {slot_pos_bracket_open}.")

        if '*' in m_p_list_sv.__str__():
            opindex = m_p_list_sv.index('*')
            num1index = opindex - 1

            # Prepare the numbers for calculation:
            # num1 = mylist[opindex - 1]
            # num2 = mylist[opindex + 1]

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

    def math_term_in_brackets_calculator(self, m_p_list_sv: List[SlotValue]) -> List[SlotValue]:
        m_p_bracket_open = 0
        m_p_bracket_close = 0

        # Count the number of open brackets and close brackets.
        for sv_item in m_p_list_sv:
            if sv_item.resolved == "OPERATOR_BRACKET_OPEN":
                m_p_bracket_open += 1
            elif sv_item.resolved == "OPERATOR_BRACKET_CLOSE":
                m_p_bracket_close += 1
            else:
                continue

        # Check whether there are brackets and whether the amount of open brackets is equal to close brackets.
        if m_p_bracket_open == m_p_bracket_close > 0:
            slot_pos_bracket_open = None
            slot_pos_bracket_close = None
            result: List[SlotValue]= []

            # Loop through the slot value items in m_p_list_sv. Search for the first close bracket and its counterpart
            # open bracket. Assign and save the slot positions for these brackets in separate VARs.
            for sv_item in m_p_list_sv:
                if sv_item.resolved == "OPERATOR_BRACKET_CLOSE":
                    slot_pos_bracket_close = sv_item.slot_position
                    print(f"Slot position of first close bracket: {slot_pos_bracket_close}.")

                elif sv_item.resolved == "OPERATOR_BRACKET_OPEN":
                    slot_pos_bracket_open = sv_item.slot_position
                    print(f"Slot position of open bracket: {slot_pos_bracket_open}.")

            # Extract the math term within the brackets. For this slice the elements (SlotValue objects) in m_p_list_sv
            # after the determined open bracket until the determined close bracket.
            math_term_in_brackets = m_p_list_sv[slot_pos_bracket_open + 1: slot_pos_bracket_close]
            zum_ausdrucken = [math_term_in_brackets[x].resolved for x in range(0, len(math_term_in_brackets))]
            print(f"Math term in brackets: {zum_ausdrucken}")

            # Calculate the math term within the brackets:
            for sv_item in math_term_in_brackets:
                # 1st: Try to solve multiplications or divisions problem
                if sv_item.resolved == "OPERATOR_MUL" or "OPERATOR_DIV":
                    result = self.mul_div_calculator(math_term_in_brackets)
                    # math_term_in_brackets = result
                    print(f"Result after mul-div calculation: {result}")

                # 2nd: Try to solve add-sub tasks:
                elif sv_item.resolved == "OPERATOR_ADD" or "OPERATOR_SUB":
                    result = self.add_sub_calculator(math_term_in_brackets)
                    # math_term_in_brackets = result
                    print(f"Result after add-sub calculation: {result}")
                else:
                    pass

            # Within the origin maths problem delete the math term in brackets and the brackets itself!
            del m_p_list_sv[slot_pos_bracket_open: slot_pos_bracket_close + 1]

            # Insert the whole elements from result into the origin maths problem list "m_p_list_sv" at the index
            # [slot_pos_bracket_open].
            m_p_list_sv[slot_pos_bracket_open:slot_pos_bracket_open] = result[:]

            print(f"Result of the math term within the brackets: {result}.")
            print(f"Maths problem updatet: {m_p_list_sv}")

            # Recursion: Try it again to solve an existing math termin within brackets.
            self.math_term_in_brackets_calculator(m_p_list_sv)

        else:
            return m_p_list_sv

    def master_calculator(self, m_p_list_sv: List[SlotValue]) -> List[SlotValue]:
        mt_no_brackets = []
        mt_no_mul_div = []
        mt_no_add_div = []

        # Zuerst Klammer-Ausdrücke ausrechnen:
        self.math_term_in_brackets_calculator(m_p_list_sv)

        # Dann Punktrechnung ausrechnen:
        self.mul_div_calculator(m_p_list_sv)

        # Zuletzt Plus-Minus-Rechnung ausrechnen
        self.add_sub_calculator(m_p_list_sv)
        result = m_p_list_sv[0]

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

            # Erzeuge ein Standard-Objekt der Klasse "Calculator" und rufe die "Methode helper_ge..." auf. Dabei
            # übergebe als Argumente die Variablen von oben aus der for-Schleife. Weise das Objekt in die VAR sv zu.
            sv = Calculator.helper_generate_slot_value(name=name, slot_position=index, number_as_str=f"{item}", resolved=resolved, is_validated=is_validated)

            # Füge die Values der VAR "sv" in das Objekt "slot_values" hinzu.
            slot_values.append(sv)

        return slot_values

    # >>>>> IN ARBEIT <<<<<
    def __str__(self) -> str:
        result = m_p_list_sv[]
        return super().__str__()


if __name__ == '__main__':
    math_task_1 = [2, '*', 5, '+', '(', 7, '*', 4, ')', '-', 90, '/', 10]
    math_task_2 = [4, '*', 20, '+', '(', 12, '/', 4, '+', 17, ')', '-', 81, '/', 9]
    math_task_1_sv = Calculator.helper_generate_list_of_slotvalues(math_task_1)
    math_task_2_sv = Calculator.helper_generate_list_of_slotvalues(math_task_2)
    idx_elem = 0
    list_elem = []
    for elem in math_task_1_sv:
        list_elem.append(math_task_1_sv[idx_elem].resolved)
        idx_elem += 1
    print(math_task_1_sv[0].resolved)
    print(math_task_2_sv)

    c = Calculator()  # Generate an standard object from the class "Calculator" and assign it to VAR 'c'.

    print(f"The math task as a list: {math_task_1}")
    print(f"The math task as a list of SlotValue objects: {math_task_1_sv}")

    result_math_task_1 = c.master_calculator(math_task_1_sv)
    print(f"Traraaaa. The result is: {result_math_task_1}")

    print(f"The math task as a list: {math_task_2}")
    result_math_task_2 = c.master_calculator(math_task_2_sv)
    print(f"The result is: {result_math_task_2}")