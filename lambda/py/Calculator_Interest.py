import math

"""
This program is for interest-calculation (Zinsrechnung).
fc is the final capital without compound interest, fcci is the final capital with compound interest.
"""

# TODO: Add Test 3


def ic_searched_and_values(term: str or None) -> float:
    """
    An argument passed to this function will be assigned to the parameter (variable) named term. Thereafter the code
    in the body will be computed with the argument (parameter value).
    This function splits a percentage calculation task (delivered as a string) into the 3 parts and puts them
    into the variables: searched, value1 and value2. Thereafter it returns all 3 parts to the function
    `vat_searched_and_values_str_str_str`.
    """
    if not term:
        raise ValueError("I need a non empty string.")
    """
    This code checks the content of the parameter/variable 'term', whether it has no values. 
    If yes, it raises a ValueError and prints out the given text.
    """

    parts = term.split(" ") or term.split(",")
    parts = list(filter(None, parts))
    """
    This code splits the content of the parameter 'term' in to parts, the splitting delimiter is a blank space. 
    Afterwards it puts the outcome into the variable 'parts'.
    """

    if len(parts) == 1:
        """
        If there is only one piece/part in the string, return it to the caller of this function.
        If the float casting fails, the try loop will catch it.
        """
        result = ic_convert_values_to_float(parts[0])
        return round(result, 2)

    if len(parts) == 2:
        """
        If there are only two elements in the string, raise a value error.
        """
        raise ValueError("Hey I need all information to do a interest-calculation.")

    if len(parts) != 4:  # If there are not exactly 4 parts, raise an value error.
        raise ValueError("Hey I need all information to do a interest-calculation.")

    # Put the splitted values from the list into separate variables.
    searched = parts[0]
    value1 = parts[1]
    value2 = parts[2]
    value3 = parts[3]

    # Return the solution to the caller auf this function.
    return ic_searched_and_values_all_str(searched, value1, value2, value3)


# TODO: Add Test 1
def ic_convert_values_to_float(number: str) -> float:
    # This function gets an argument, converts delivered string values to floats.
    if not number:
        raise ValueError("I need a non empty string")

    else:
        number = float(number)

    return number


# TODO: Add Test 2
def ic_searched_and_values_all_str(searched: str, value1: str, value2: str, value3: str) -> float:
    """
    This function changes the types of value1 and value2 to floats and passes the variables
    searched, value1 and value2 to the function "vat_the_calculation".
    """
    value1 = ic_convert_values_to_float(value1)
    value2 = ic_convert_values_to_float(value2)
    value3 = ic_convert_values_to_float(value3)

    return ic_the_calculation(searched, value1, value2, value3)


# TODO: Add Test 1
def ic_the_calculation(searched: str, value1: float, value2: float, value3: float) -> float:
    # This function calculates the maths problem from the user.
    if searched == "fc":
        start_capital = value1
        interest = 1 + value2 * value3
        result = start_capital + interest

    elif searched == "fcci":
        start_capital = value1
        base = 1 + value2
        exponent = value3
        result = start_capital * base ** exponent

    else:
        raise ValueError("Ohh Jesus, interest calculation is so difficult! I can´t calculate this.")

    d, i = math.modf(result)
    if d == 0:  # If the decimal place is equal to 0, then change the number type to integer.
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
        result = ic_searched_and_values(term)
        result_as_string = f"The interest-calculation task (searched value, start-capital, interest rate, " \
                           f"time period): {term} = {str(result)}"
        print(result_as_string)
        return result_as_string  # make it easier for testing
    except ValueError as ex:
        print(f"Mistake: I'm not able to calc '{term}' Reason: {ex} ")

if __name__ == "__main__":  # pragma: no cover
    # Imagine Each line as a new user interaction, that's why we don't do `input`.
    # p = percentage (rate), pv = percentage value (part), b = base
    interest_calculation_task("fc 1000 0.05 3")
    # What is the (simple) final capital, when 1000 EUR has been invested with an interest rate of 5% over 3 years
    # without compound interest?
    interest_calculation_task("fcci 1000 0.05 12")
    # What is the final capital, when 1000 EUR has been invested with an interest rate of 5% over 3 years
    # with compound interest?

    interest_calculation_task("b 40900 0.34 15")
    interest_calculation_task("r")
    interest_calculation_task(" ")
    interest_calculation_task("")
    interest_calculation_task("20")
    interest_calculation_task("p 30")
    # In the cases above is a calculation not possible, because of the given values.
