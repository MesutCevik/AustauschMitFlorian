math_task = [2, '*', 5, '+', '(', 7, '*', 4, ')', '-', 90, '/', 10]


def mul_div_calculator(mylist: list) -> list:
    result_mul_div = []

    if '*' in mylist:
        # ex. [4, '*', 6]
        opindex = mylist.index('*')
        num1index = opindex - 1

        num1 = mylist[opindex - 1]
        num2 = mylist[opindex + 1]

        result_mul_div = num1 * num2
        print(f"Result of multiplication: {result_mul_div}")
        print()

        mylist.insert((opindex + 2), result_mul_div)
        mylist.pop(num1index)
        mylist.pop(num1index)
        mylist.pop(num1index)
        print(f"Status after multiplication: {mylist}")
        print()

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

    else:
        return mylist

    # ***** My awesome recursion: *****
    mul_div_calculator(mylist)


def add_sub_calculator(mylist: list) -> list:
    if '+' in mylist:
        opindex = mylist.index('+')
        num1index = opindex - 1
        print(opindex)

        num1 = mylist[opindex - 1]
        num2 = mylist[opindex + 1]

        result = num1 + num2

        mylist.insert((opindex + 2), result)
        print(f"Status 1: {mylist}")
        print()

        mylist.pop(num1index)
        mylist.pop(num1index)
        mylist.pop(num1index)

        print(opindex)
        print(f"Status 2: {mylist}")

    elif '-' in mylist:
        opindex = mylist.index('-')
        num1index = opindex - 1
        print(opindex)

        num1 = mylist[opindex - 1]
        num2 = mylist[opindex + 1]

        result = int(num1 - num2)

        mylist.insert((opindex + 2), result)
        print(f"Status 3: {mylist}")
        print()

        mylist.pop(num1index)
        mylist.pop(num1index)
        mylist.pop(num1index)

        print(opindex)
        print(f"Status 4: {mylist}")


    else:
        return mylist

    # ***** My awesome recursion: *****
    add_sub_calculator(mylist)


def bracket_term_calculator(math_task: list) -> list:
    # math_task_new = []
    if '(' and ')' in math_task:
        bracket_open = math_task.index('(')
        print(f"Index of bracket open: {bracket_open}.")
        bracket_close = math_task.index(')')
        print(f"Index of bracket close: {bracket_close}.")
        print()

        mt_in_brackets: list = math_task[bracket_open + 1: bracket_close]
        print(f"Math task in brackets: {mt_in_brackets}.")

        # Calculate the math task within the brackets:
        result1 = mul_div_calculator(mt_in_brackets)
        print(f"Was kommt nach mul-div raus? {result1}")

        result2 = add_sub_calculator(result1)
        print(f"Was kommt nach add-sub raus? {result2}")

        # Within the origin math task delete the math term in brackets and the brackets itself!
        del math_task[bracket_open: bracket_close + 1]
        math_task_new = math_task
        print(math_task_new)
        print()

        # Insert the result of the math term within brackets in to the new math task.
        math_task_new.insert(bracket_open, result2)
        print(f"Das Ergebnis des Klammerausdrucks ist: {mt_in_brackets}. "
              f"Hier die überarbeitete Mathe-Aufgabe: {math_task_new}")

        bracket_term_calculator(math_task_new)

    else:
        return math_task_new


def master_calculator(math_task) -> list:
    # Zuerst Klammer-Ausdrücke ausrechnen:
    mt_no_brackets = bracket_term_calculator(math_task)

    # Dann Punktrechnung ausrechnen:
    mt_no_mul_div = mul_div_calculator(mt_no_brackets)

    # Zuletzt Plus-Minus-Rechnung ausrechnen
    result = add_sub_calculator(mt_no_mul_div)

    # Return das Ergebnis
    return result


if __name__ == '__main__':
    print(f"The math task in a list: {math_task}")
    print()

    result = master_calculator(math_task)
    print(result)
