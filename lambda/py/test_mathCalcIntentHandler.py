from typing import Dict
from unittest import TestCase

from lambda_function import MathCalcIntentHandler, SlotValue


class TestMathCalcIntentHandler(TestCase):
    def test_generate_num_op_lists(self):

        # Definiere Objekte vom Typ SlotValue, um darin beliebig erzeugte Daten zu speichern.
        s1 = self.generate_slot_number(name="numberOne", slot_position=2, number_as_str="One", resolved="1", is_validated=False)
        s2 = self.generate_slot_number(name="numberTwo", slot_position=1, number_as_str="Two", resolved="5", is_validated=False)
        s3 = self.generate_slot_number(name="operatorOne", slot_position=1, number_as_str="One", resolved="OPERATOR_ADD", is_validated=True)

        # Deklariere ein Dictionary faked_amazon_input und speichere darin key=s1.name und value=s1 usw.
        faked_amazon_input: Dict[str, SlotValue] = {s1.name: s1, s2.name: s2, s3.name: s3 }


        # Z1 Erzeuge ein MathCalcIntentHandler() Objekt.
        # Z2 Übergebe faked_amazon_input als Argument an die Methode generate_num_op_lists. Das Ergebnis (Tuple mit 3
        # Listen) in die Variablen unten zuweisen.
        # Z3ff assertEqual-Methoden Testfälle durchführen: Bei den Testdaten von oben muss die Länge von master_list
        # drei, num_4_calc zwei und ops_4_calc 1 aufweisen.
        toll = MathCalcIntentHandler()
        master_list, num_4_calc, ops_4_calc = toll.generate_num_op_lists(faked_amazon_input)
        self.assertEqual(len(master_list), 3)
        self.assertEqual(len(num_4_calc), 2)
        self.assertEqual(len(ops_4_calc), 1)

    def test_generate_num_op_lists_second_test(self):

        s1 = self.generate_slot_number(name="numberOne", slot_position=2, number_as_str="One", resolved="1", is_validated=False)
        s2 = self.generate_slot_number(name="numberTwo", slot_position=1, number_as_str="Two", resolved="5", is_validated=False)
        s3 = self.generate_slot_number(name="numberThree", slot_position=1, number_as_str="Two", resolved="5", is_validated=False)
        s4 = self.generate_slot_number(name="operatorOne", slot_position=1, number_as_str="One", resolved="OPERATOR_ADD", is_validated=True)
        s5 = self.generate_slot_number(name="operatorTwo", slot_position=1, number_as_str="One", resolved="OPERATOR_ADD", is_validated=True)


        faked_amazon_input: Dict[str, SlotValue] = {s1.name: s1,
                                                    s2.name: s2,
                                                    s3.name: s3,
                                                    s4.name: s4,
                                                    s5.name: s5
                                                    }


        toll = MathCalcIntentHandler()
        master_list, num_4_calc, ops_4_calc = toll.generate_num_op_lists(faked_amazon_input)
        self.assertEqual(len(master_list), 3)
        self.assertEqual(len(num_4_calc), 2)
        self.assertEqual(len(ops_4_calc), 1)


    @staticmethod
    def generate_slot_number(name: str, slot_position: int, number_as_str:str, resolved:str, is_validated: bool) -> SlotValue:
        sv = SlotValue()
        sv.name = name
        sv.slot_position = slot_position
        sv.number_as_str = number_as_str
        sv.resolved = resolved
        sv.is_validated = is_validated
        return sv



