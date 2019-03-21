from enum import Enum
from typing import List, Dict, Union, Tuple, Optional, Any

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
        for sv_item in m_p_list_sv:
            # Loop through the slot value-items in the list "m_p_list_sv". Search for the first operator and check,
            # whether the operator is a multiplication or division one. Assign and save the items index for this
            # operator in a VAR. Then continue.
            if sv_item.resolved == "OPERATOR_MUL":
                op_idx = m_p_list_sv.index(sv_item)

                # Prepare the numbers for calculation:
                # num1: Take the value of field "resolved" from the sv_item one BEFORE the sv_item with the operator.
                # num2: Take the value of field "resolved" from the sv_item one AFTER the sv_item with the operator.
                # Because the values of "resolved" field are str, cast them to int!
                num1 = int(m_p_list_sv[op_idx - 1].resolved)
                num2 = int(m_p_list_sv[op_idx + 1].resolved)

                # Calculate the math term in the list:
                result_mul_div: int = num1 * num2
                print(f"Result of multiplication: {result_mul_div}")

                # Generate a new SlotValue()-object "slot_value" for the calculated result (number):
                sv_item_new_num = self.helper_generate_slot_value(name=f"number{op_idx - 1}", slot_position=op_idx - 1, number_as_str=str(result_mul_div), resolved=str(result_mul_div), is_validated=False)

                # Revise the list m_p_list_sv: insert the new SlotValue()-object "sv_item_new_num" at position
                # "op_idx - 1". This is the starting index of the calculated math term.
                # Then pop all items (objects), which we used in the calculation above.
                m_p_list_sv.insert(op_idx - 1, sv_item_new_num)
                m_p_list_sv.pop(op_idx)
                m_p_list_sv.pop(op_idx)
                m_p_list_sv.pop(op_idx)
                print(f"Status after multiplication: {self.print_maths_problem_as_list(m_p_list_sv)}")
                print()

                # My awesome recursion:
                self.mul_div_calculator(m_p_list_sv)

            elif sv_item.resolved == "OPERATOR_DIV":
                op_idx = m_p_list_sv.index(sv_item)

                # Prepare the numbers for calculation:
                # num1: Take the value of field "resolved" from the sv_item one BEFORE the sv_item with the operator.
                # num2: Take the value of field "resolved" from the sv_item one AFTER the sv_item with the operator.
                # Because the values of "resolved" field are str, cast them to int!
                num1 = int(m_p_list_sv[op_idx - 1].resolved)
                num2 = int(m_p_list_sv[op_idx + 1].resolved)

                # Calculate the math term in the list. Because a devisions result is a float, cast it to int:
                result_mul_div = int(num1 / num2)
                print(f"Result of division: {result_mul_div}")

                # Generate a new SlotValue()-object "slot_value" for the calculated result (number):
                sv_item_new_num = self.helper_generate_slot_value(name=f"number{op_idx - 1}", slot_position=op_idx - 1, number_as_str=str(result_mul_div), resolved=str(result_mul_div), is_validated=False)

                # Revise the list m_p_list_sv: insert the new SlotValue()-object "sv_item_new_num" at position
                # "op_idx - 1". This is the starting index of the calculated math term.
                # Then pop all items (objects), which we used in the calculation above.
                m_p_list_sv.insert(op_idx - 1, sv_item_new_num)
                m_p_list_sv.pop(op_idx)
                m_p_list_sv.pop(op_idx)
                m_p_list_sv.pop(op_idx)
                print(f"Status after multiplication: {self.print_maths_problem_as_list(m_p_list_sv)}")
                print()

                # My awesome recursion:
                self.mul_div_calculator(m_p_list_sv)

            else:
                # If there is no mul-div term to solve, this method returns the last status of m_p_list_sv.
                return m_p_list_sv

    def add_sub_calculator(self, m_p_list_sv: List[SlotValue]) -> List[SlotValue]:
        for sv_item in m_p_list_sv:
            if sv_item.resolved == "OPERATOR_ADD":
                op_idx = m_p_list_sv.index(sv_item)

                num1 = int(m_p_list_sv[op_idx - 1].resolved)
                num2 = int(m_p_list_sv[op_idx + 1].resolved)

                result_add_sub = num1 + num2
                print(f"Result of addition: {result_add_sub}")

                # Generate a new SlotValue()-object "slot_value" for the calculated result (number):
                sv_item_new_num = self.helper_generate_slot_value(name=f"number{op_idx - 1}", slot_position=op_idx - 1, number_as_str=str(result_add_sub), resolved=str(result_add_sub), is_validated=False)

                m_p_list_sv.insert((op_idx - 1), sv_item_new_num)
                m_p_list_sv.pop(op_idx)
                m_p_list_sv.pop(op_idx)
                m_p_list_sv.pop(op_idx)
                print(f"Status after addition: {self.print_maths_problem_as_list(m_p_list_sv)}")
                print()

                self.add_sub_calculator(m_p_list_sv)

            elif sv_item.resolved == "OPERATOR_SUB":
                op_idx = m_p_list_sv.index(sv_item)

                num1 = int(m_p_list_sv[op_idx - 1].resolved)
                num2 = int(m_p_list_sv[op_idx + 1].resolved)

                result_add_sub = num1 - num2
                print(f"Result of subtraction: {result_add_sub}")

                # Generate a new SlotValue()-object "slot_value" for the calculated result (number):
                sv_item_new_num = self.helper_generate_slot_value(name=f"number{op_idx - 1}", slot_position=op_idx - 1, number_as_str=str(result_add_sub), resolved=str(result_add_sub), is_validated=False)

                m_p_list_sv.insert((op_idx - 1), sv_item_new_num)
                m_p_list_sv.pop(op_idx)
                m_p_list_sv.pop(op_idx)
                m_p_list_sv.pop(op_idx)
                print(f"Status after addition: {self.print_maths_problem_as_list(m_p_list_sv)}")
                print()

                self.add_sub_calculator(m_p_list_sv)

            else:
                return m_p_list_sv

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
                    Idx_slot_pos_bracket_close = sv_item.slot_position
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

    def print_maths_problem_as_list(self, maths_problem: List[SlotValue]) -> List[str]:
        # Print maths problem status as list in order to show the status.
        maths_problem_4_print = maths_problem
        idx_elem = 0
        maths_problem_as_list = []
        for elem in maths_problem_4_print:
            maths_problem_as_list.append(elem.resolved)
            idx_elem += 1

        return maths_problem_as_list


if __name__ == '__main__':
    maths_problem_1 = [2, '*', 5, '+', '(', 7, '*', 4, ')', '-', 90, '/', 10]
    maths_problem_2 = [4, '*', 20, '+', '(', 12, '/', 4, '+', 17, ')', '-', 81, '/', 9]
    maths_problem_1_sv = Calculator.helper_generate_list_of_slotvalues(maths_problem_1)
    maths_problem_2_sv = Calculator.helper_generate_list_of_slotvalues(maths_problem_2)
    idx_elem = 0
    list_elem = []
    for elem in maths_problem_1_sv:
        list_elem.append(maths_problem_1_sv[idx_elem].resolved)
        idx_elem += 1
    print(maths_problem_1_sv[0].resolved)
    print(maths_problem_2_sv)

    c = Calculator()  # Generate an standard object from the class "Calculator" and assign it to VAR 'c'.

    print(f"The math task as a list: {maths_problem_1}")
    print(f"The math task as a list of SlotValue objects: {maths_problem_1_sv}")

    result_math_task_1 = c.master_calculator(maths_problem_1_sv)
    print(f"Traraaaa. The result is: {result_math_task_1}")

    print(f"The math task as a list: {maths_problem_2}")
    result_math_task_2 = c.master_calculator(maths_problem_2_sv)
    print(f"The result is: {result_math_task_2}")
