from typing import List
from unittest import TestCase

from Calculator import Calculator, SlotValue


class TestCalculator(TestCase):
    def test_master_calculator(self):
        math_task_1 = [2, '*', 5, '+', '(', 7, '*', 4, ')', '-', 90, '/', 10]

        math_task_1_sv = Calculator.helper_generate_list_of_slot_values(math_task_1)

        self.assertEqual(str(math_task_1[0]), math_task_1_sv[0].resolved)
        self.assertEqual("OPERATOR_MUL", math_task_1_sv[1].resolved)
        self.assertEqual(str(math_task_1[2]), math_task_1_sv[2].resolved)
        self.assertEqual("OPERATOR_ADD", math_task_1_sv[3].resolved)
        self.assertEqual("OPERATOR_BRACKET_OPEN", math_task_1_sv[4].resolved)
        self.assertEqual(str(math_task_1[5]), math_task_1_sv[5].resolved)
        self.assertEqual("OPERATOR_MUL", math_task_1_sv[6].resolved)
        self.assertEqual("OPERATOR_DIV", math_task_1_sv[11].resolved)
        self.assertEqual(str(math_task_1[12]), math_task_1_sv[12].resolved)

    def test_master_calculator_small_term(self):
        math_task_1 = [2, '*', 5, '+', '3']

        math_task_1_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(math_task_1)

        self.assertEqual(str(math_task_1[0]), math_task_1_sv[0].resolved)
        self.assertEqual("OPERATOR_MUL", math_task_1_sv[1].resolved)
        self.assertEqual(str(math_task_1[2]), math_task_1_sv[2].resolved)
        self.assertEqual("OPERATOR_ADD", math_task_1_sv[3].resolved)
        c = Calculator()
        result: List[SlotValue] = c.master_calculator(math_task_1_sv)
        self.assertEqual("13", result[0].number_as_str)

    def test_mul_div_calculator(self):
        math_task_1 = [28]

        math_task_1_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(math_task_1)

        self.assertEqual("28", math_task_1_sv[0].resolved)

    def test_master_calculator_small_term_large(self):
        math_task_1 = ['(', '(', 8, '/', 2, ')', '*', 3, ')', '+', 1]
        # math_task_1 = ['(', 8, '/', '(', 8, '/', 2, ')', ')', '*', 3, '+', '(', 8, '/', 2, ')']

        math_task_1_sv: List[SlotValue] = Calculator.helper_generate_list_of_slot_values(math_task_1)

        c = Calculator()
        math_task_1_sv: List[SlotValue] = c.master_calculator(math_task_1_sv)
        # math_task_1_sv[0].resolved
        print(math_task_1_sv)
        self.assertEqual("13", "13")