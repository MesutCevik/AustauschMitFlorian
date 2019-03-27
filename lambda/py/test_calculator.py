from typing import List
from unittest import TestCase

from Calculator import Calculator, SlotValue


class TestCalculator(TestCase):

    def test_helper_generate_list_of_slot_values_long_term(self):
        # Tests the generating of a list of slot values from a maths problem as a list.

        # Maths problem as a Python list:
        maths_problem_1 = [2, '*', 5, '+', '(', 7, '*', 4, ')', '-', 90, '/', 10]

        # Maths problem as a list of SlotValue objects:
        maths_problem_1_sv = Calculator.helper_generate_list_of_slot_values(maths_problem_1)

        self.assertEqual(str(maths_problem_1[0]), maths_problem_1_sv[0].resolved)
        print(str(maths_problem_1[0]))  # In the Python list the number at index 0 is 2.
        print(maths_problem_1_sv[0].resolved)  # In the list of SlotValues at index 0 must be 2.

        self.assertEqual("OPERATOR_MUL", maths_problem_1_sv[1].resolved)
        print("OPERATOR_MUL", maths_problem_1_sv[1].resolved)

        self.assertEqual(str(maths_problem_1[2]), maths_problem_1_sv[2].resolved)
        print(str(maths_problem_1[2]), maths_problem_1_sv[2].resolved)

        self.assertEqual("OPERATOR_BRACKET_OPEN", maths_problem_1_sv[4].resolved)
        print("OPERATOR_BRACKET_OPEN", maths_problem_1_sv[4].resolved)

        self.assertEqual("OPERATOR_BRACKET_CLOSE", maths_problem_1_sv[8].resolved)
        print("OPERATOR_BRACKET_CLOSE", maths_problem_1_sv[8].resolved)

        self.assertEqual("OPERATOR_ADD", maths_problem_1_sv[3].resolved)
        self.assertEqual(str(maths_problem_1[5]), maths_problem_1_sv[5].resolved)
        self.assertEqual("OPERATOR_MUL", maths_problem_1_sv[6].resolved)
        self.assertEqual("OPERATOR_DIV", maths_problem_1_sv[11].resolved)

    def test_helper_generate_slot_value(self):
        sv = Calculator.helper_generate_slot_value(name='4', slot_position=0, number_as_str=f"{4}",
                                                   resolved='4', is_validated=False)
        sv1 = Calculator.helper_generate_slot_value(name='*', slot_position=1, number_as_str=f"{'*'}",
                                                    resolved="OPERATOR_MUL", is_validated=True)
        sv2 = Calculator.helper_generate_slot_value(name='(', slot_position=3, number_as_str=f"{'('}",
                                                    resolved="OPERATOR_BRACKET_OPEN", is_validated=True)

        self.assertEqual(('4', 0, '4', '4', False), (sv.name, sv.slot_position, sv.number_as_str, sv.resolved,
                                                     sv.is_validated))
        print(('4', 0, '4', '4', False), (sv.name, sv.slot_position, sv.number_as_str, sv.resolved, sv.is_validated))

        self.assertEqual(('*', 1, '*', 'OPERATOR_MUL', True), (sv1.name, sv1.slot_position, sv1.number_as_str,
                                                               sv1.resolved, sv1.is_validated))
        print(('*', 1, '*', 'OPERATOR_MUL', True), (sv1.name, sv1.slot_position, sv1.number_as_str, sv1.resolved,
                                                    sv1.is_validated))

        self.assertEqual(('(', 3, '(', 'OPERATOR_BRACKET_OPEN', True), (sv2.name, sv2.slot_position, sv2.number_as_str,
                                                                        sv2.resolved, sv2.is_validated))
        print(('(', 3, '(', 'OPERATOR_BRACKET_OPEN', True), (sv2.name, sv2.slot_position, sv2.number_as_str,
                                                             sv2.resolved, sv2.is_validated))

    def test_helper_generate_list_of_slot_values(self):
        maths_problem_1 = [2, '*', 5, '+', 80, '/', 10]

        maths_problem_1_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(maths_problem_1)

        self.assertEqual("OPERATOR_ADD", maths_problem_1_sv[3].resolved)
        self.assertEqual("OPERATOR_DIV", maths_problem_1_sv[5].resolved)
        self.assertEqual(str(maths_problem_1[6]), maths_problem_1_sv[6].resolved)

        print(f"Values of field 'resolved' in list maths_problem_1_sv: {maths_problem_1_sv}")

    def test_master_calculator_small_term(self):
        maths_problem_1 = [2, '*', 5, '+', '3']

        math_task_1_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(maths_problem_1)

        print(f"The maths_problem_1 - Python list:                  {maths_problem_1}")
        print(f"The maths_problem_1_sv - list of SlotValue objects: {maths_problem_1}")
        print()
        self.assertEqual(str(maths_problem_1[0]), math_task_1_sv[0].resolved)
        self.assertEqual("OPERATOR_MUL", math_task_1_sv[1].resolved)
        self.assertEqual(str(maths_problem_1[2]), math_task_1_sv[2].resolved)
        self.assertEqual("OPERATOR_ADD", math_task_1_sv[3].resolved)

        c = Calculator()
        result: List[SlotValue] = c.master_calculator(math_task_1_sv)
        self.assertEqual("13", result[0].resolved)
        print("13", result[0].resolved)

    def test_mul_div_calculator(self):
        maths_problem_1 = [28]
        maths_problem_2 = [2, '*', 5]
        maths_problem_3 = [2, '*', 5, '+', 80, '/', 10]

        c = Calculator()

        maths_problem_1_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(maths_problem_1)
        result: List[SlotValue] = c.mul_div_calculator(maths_problem_1_sv)
        self.assertEqual("28", result[0].resolved)
        print("28", result[0].resolved)

        maths_problem_2_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(maths_problem_2)
        result2: List[SlotValue] = c.mul_div_calculator(maths_problem_2_sv)
        self.assertEqual("10", result2[0].resolved)

        maths_problem_3_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(maths_problem_3)
        result3: List[SlotValue] = c.mul_div_calculator(maths_problem_3_sv)
        print(f"result3: {result3}")
        self.assertEqual("[10, OPERATOR_ADD, 8]", str(result3))
        self.assertEqual("10", result3[0].resolved)
        self.assertEqual("OPERATOR_ADD", result3[1].resolved)
        self.assertEqual("8", result3[2].resolved)

    def test_add_sub_calculator(self):
        maths_problem_1 = [5498]
        maths_problem_2 = [789, '-', 89]
        maths_problem_3 = [1789, '+', 60, '-', 1204, '/', 14]

        c = Calculator()

        maths_problem_1_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(maths_problem_1)
        result: List[SlotValue] = c.add_sub_calculator(maths_problem_1_sv)
        self.assertEqual("5498", result[0].resolved)

        maths_problem_2_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(maths_problem_2)
        result2: List[SlotValue] = c.add_sub_calculator(maths_problem_2_sv)
        self.assertEqual("700", result2[0].resolved)

        maths_problem_3_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(maths_problem_3)
        result3: List[SlotValue] = c.add_sub_calculator(maths_problem_3_sv)
        print(f"result3: {result3}")
        self.assertEqual("[645, OPERATOR_DIV, 14]", str(result3))
        self.assertEqual("645", result3[0].resolved)
        self.assertEqual("OPERATOR_DIV", result3[1].resolved)
        self.assertEqual("14", result3[2].resolved)

    def test_master_calculator_long_term(self):
        maths_problem_1 = ['(', '(', 8, '/', 2, ')', '*', 3, ')', '+', 1]
        # maths_problem_1 = ['(', 8, '/', '(', 8, '/', 2, ')', ')', '*', 3, '+', '(', 8, '/', 2, ')']

        maths_problem_1_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(maths_problem_1)

        c = Calculator()
        maths_problem_1_sv: List[SlotValue] = c.master_calculator(maths_problem_1_sv)
        # maths_problem_1_sv[0].resolved
        print(maths_problem_1_sv)
        self.assertEqual("13", str(maths_problem_1_sv[0]))


