import math

"""
ZINSRECHNUNG
Dieses Programm berechnet Zinsaufgaben und kann ermitteln:
a) Verzinsung einer Investition
b) Endkapital bei Zinseszins einer Investition
"""


def ic_searched_value_and_values(term: str or None) -> float:
    """
    This method gets an interest calculation task as a string within the argument 'term'. At first it checks the
    passed argument whether it contains a string or is empty. Then the string will be split into the required parts
    of the ic task: gesuchter_wert, anfangskapital, zinssatz and anzahl_jahre.
    Thereafter it returns all 4 parts to the function `ic_prepare_the_calculation`.
    """

    # If the passed argument in 'term' is empty, then raise a ValueError and print out the message.
    if not term:
        raise ValueError("In Ihrer Eingabe ist ein Fehler. Bitte geben sie eine Aufgabe zur Zinsrechnung.")

    # Splits the string in 'term' into parts using a blank space or a comma as a delimiter.
    # Assigns the result into the list in the variable 'parts'.
    parts = term.split(" ") or term.split(",")
    parts = list(filter(None, parts))

    # If the list in 'parts' contains only 1 element, then convert and return the value as a float.
    # If the casting to float fails, the try-except loop will catch it.
    if len(parts) == 1:
        result = ic_convert_value_to_float(parts[0])
        return round(result, 2)

    # If the list in 'parts' has only 2 parts, then raise a value error.
    if len(parts) == 2:
        raise ValueError("Ein Fehler ist aufgetreten. Bitte geben Sie alle benötigten Angaben, damit rechnen kann.")

    # If the list in 'parts' has not exactly 4 parts, then raise a value error.
    if len(parts) != 4:  # If there are not exactly 4 parts, raise an value error.
        raise ValueError("Ein Fehler ist aufgetreten. Bitte geben Sie alle benötigten Angaben, damit rechnen kann.")

    # Put the splitted values from the list into separate variables.
    gesuchter_wert: str = parts[0]
    anfangskapital: str = parts[1]
    zinssatz: str = parts[2]
    anzahl_jahre: str = parts[3]

    # Pass the values of the interest calculation task to the method 'ic_prepare_the_calculation'.
    # Note: When a method returns more than 1 value, then it returns it as a tuple!!!
    return ic_prepare_the_calculation(gesuchter_wert, anfangskapital, zinssatz, anzahl_jahre)


def ic_prepare_the_calculation(gesuchter_wert: str, anfangskapital: str, zinssatz: str, anzahl_jahre: str) -> float:
    # Converts the given values 'anfangskapital', 'zinssatz' and 'anzahl_jahre' to floats, calls the method
    # ic_calculate_searched_value method and returns the searched value.

    anfangskapital = ic_convert_value_to_float(anfangskapital)
    zinssatz = ic_convert_value_to_float(zinssatz)
    anzahl_jahre = ic_convert_value_to_float(anzahl_jahre)

    return ic_calculate_searched_value(gesuchter_wert, anfangskapital, zinssatz, anzahl_jahre)


def ic_convert_value_to_float(number: str) -> float:
    # Converts the passed argument (a string, which stands for a number) to a float.
    if not number:
        raise ValueError("I need a non empty string")

    else:
        number = float(number)

    return number


def ic_calculate_searched_value(gesuchter_wert: str, anfangskapital: float, zinssatz: float, anzahl_jahre: float) \
        -> float:
    # Calculates the searched value from the interest calculations problem.
    if gesuchter_wert == "Zinserträge":
        basis = 1 + zinssatz
        exponent = anzahl_jahre
        endkapital = anfangskapital * basis ** exponent
        result = endkapital - anfangskapital

    elif gesuchter_wert == "Endkapital":
        basis = 1 + zinssatz
        exponent = anzahl_jahre
        result = anfangskapital * basis ** exponent

    else:
        raise ValueError("Bei der Berechnung ist ein Fehler aufgetreten. Bitte prüfen sie ihre Eingabe und geben sie"
                         "Zinsrechnungsaufgabe erneut ein.")

    # Do not return the decimal place of result, if it is 0. Then return an integer.
    # R1: Split the float number in 'result' into the fractional and integer parts.
    # R2: If the decimal place is 0, then convert the float number to integer.
    # R4: Else round the result to two decimal places if necessary.
    d, i = math.modf(result)
    if d == 0:
        result = int(result)
    else:
        result = round(result, 2)

    return result


def interest_calculation_task(term: str) -> str:
    """
    to increase tests coverage from 82% to 100%, than remove this comment :-)
    hint: the newly added return str helps
    """

    try:
        result = ic_searched_value_and_values(term)
        result_as_string = f"Die Zinsrechnungsaufgabe (gesucht ist das Endkapital, gegeben ist Anfangskapital, " \
            f"Zinssatz und Jahre): {term} = {str(result)}"
        print(result_as_string)
        return result_as_string  # make it easier for testing
    except ValueError as ex:
        print(f"Fehler: Ich kann diese Aufgabe nicht rechnen: '{term}'. Grund: {ex} ")


if __name__ == "__main__":  # pragma: no cover
    # Imagine Each line as a new user interaction, that's why we don't do `input`.
    """
    Kn 	: Endkapital (inkl. Zinsen nach n Jahren)
    K0 	: Anfangskapital
    p 	: Zinssatz (in Prozent pro Jahr)
    n 	: Jahre (Anzahl)
    Formel für Endkapital nach n-Jahren: Kn = K0 ((p/100) + 1) hoch n
    Formel für Zinserträge nach n-Jahren: Zn = Kn - K0 (Zinzen inkl. Zinseszinsen)
    """

    interest_calculation_task("Zinserträge 1000 0.07 5")
    # What is the (simple) final capital, when 1000 EUR has been invested with an interest rate of 5% over 3 years
    # without compound interest?
    interest_calculation_task("Endkapital 1000 0.07 5")
    # Wie hoch ist das Endkapital, wenn 1000 EUR bei 7% Zinsen 5 Jahre angelegt werden? (mit Zinseszinsen)

    interest_calculation_task("b 40900 0.34 15")
    interest_calculation_task("r")
    interest_calculation_task(" ")
    interest_calculation_task("")
    interest_calculation_task("20")
    interest_calculation_task("p 30")
    # In the cases above is a calculation not possible, because of the given values.
