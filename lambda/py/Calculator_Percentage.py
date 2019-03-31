import math

"""
PORZENTRECHNUNG
Dieses Programm berechnet Prozentaufgaben und kann ermitteln:
a) Prozentwert
b) Prozentsatz
c) Grundwert
"""


def pc_searched_value_and_values(term: str) -> float:
    """
    This method gets a percentage calculation task as a string within the argument 'term'. At first it checks the
    passed argument whether it contains a string or is empty. Then the string will be split into the required parts
    of the pc task: searched value, value1 and value2.
    Thereafter it returns all 3 parts to the function `pc_prepare_the_calculation`.
    """

    # If the passed argument in 'term' is empty, then raise a ValueError and print out the message.
    if not term:
        raise ValueError("In Ihrer Eingabe ist ein Fehler. Bitte geben sie eine Aufgabe zur Prozentrechnung.")

    # Split the string in 'term' into parts using a blank space or a comma as a delimiter.
    # Assign the result into the list in the variable 'parts'.
    # Afterwards it filters this list from None; it deletes all None values in 'parts'.
    parts = term.split(" ") or term.split(",")
    parts = list(filter(None, parts))

    # If the list in 'parts' contains only 1 element, then convert and return the value as a float.
    # If the casting to float fails, the try loop will catch it.
    if len(parts) == 1:
        result = pc_convert_value_to_float(parts[0])
        return round(result, 2)

    # If the list in 'parts' has not exactly 3 parts, then raise a value error.
    if len(parts) != 3:
        raise ValueError("Ein Fehler ist aufgetreten. Ich benötige eine gesuchte Größe und zwei Werte, um eine "
                         "Prozentaufgabe lösen zu können.")

    # The list in 'parts' contains the full and correct percentage calculation task. From this list assigne the
    # separated values to these variables:
    searched: str = parts[0]
    value1: str = parts[1]
    value2: str = parts[2]

    # Pass the values of the percentage calculation task to the method 'pc_prepare_the_calculation'.
    # Note: When a method returns more than 1 value, then it returns it as a tuple!!!
    return pc_prepare_the_calculation(searched, value1, value2)


def pc_prepare_the_calculation(searched: str, value1: str, value2: str) -> float:
    # Converts the given values 'value1' and 'value2' to floats, calls the pc_calculate_searched_value method and
    # returns the searched value.

    value1 = pc_convert_value_to_float(value1)
    value2 = pc_convert_value_to_float(value2)

    return pc_calculate_searched_value(searched, value1, value2)


def pc_convert_value_to_float(number: str) -> float:
    # Convert the given argument (a string) to float and returns the float value.

    if not number:
        raise ValueError("I need a non empty string")

    else:
        number = float(number)

    return number


def pc_calculate_searched_value(searched, value1, value2) -> float:
    # Calculates the searched value from the percentage calculation problem.

    if searched == "Prozentwert":
        result = (value1 / 100) * value2

    elif searched == "Prozentsatz":
        result = (value1 * 100) / value2

    elif searched == "Grundwert":
        result = (value1 * 100) / value2

    else:
        raise ValueError("Es ist ein Fehler aufgetreten. Ich kann diese Aufgabe nicht ausrechnen. Bitte wiederhole "
                         "Deine Eingabe.")

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


def percentage_calculation_task(term: str) -> str:

    try:
        result = pc_searched_value_and_values(term)
        result_as_string = f"Die Prozentaufgabe lautet: {term} = {str(result)}"
        # Defines a new variable and puts in a formatted text including the result of the whole calculation.
        print(result_as_string)
        return result_as_string  # Makes it easier for testing.
    except ValueError as ex:
        print(f"Fehler: Ich kann '{term}' nicht ausrechnen. Der Grund ist: {ex}")


if __name__ == "__main__":  # pragma no cover
    # Imagine Each line as a new user interaction, that's why we don't do `input`.
    # p = percentage (rate), pv = percentage value (part), b = base
    # Prozentsatz, Prozentwert, Grundwert

    # Berechne den Prozentwert. Wie viel sind 10 % von 100? Der Prozentwert ist: ...
    percentage_calculation_task("Prozentwert 10 100")

    # Berechne den Prozentsatz. Wie viel Prozent sind 115 von 250? Der Prozentsatz ist: ...
    percentage_calculation_task("Prozentsatz 115 250")

    # Was ist der Grundwert, wenn 87% vom Grundwert 34 sind? Der Grund wert ist: ...
    percentage_calculation_task("Grundwert 34 87")

    percentage_calculation_task("r")
    percentage_calculation_task("20")
    percentage_calculation_task("p 30")
    percentage_calculation_task("x 34 87")

    percentage_calculation_task(" ")
    percentage_calculation_task("")
    percentage_calculation_task(None)

