import random

temperature = [random.randint(-30, 30) for _ in range(7)]


def rendtemp(i):
    temp = ""  # Initialize temp as an empty string for this row
    for j in range(7):
        if temperature[j] > -i * 5 + 25:
            temp += "   #"
        else:
            temp += "    "
    return temp  # Return the final string for this row


def weather(temperatures):
    result = []  # Collect all rows to print at once
    for i in range(13):
        row = str(-i * 5 + 30).rjust(3) + rendtemp(i)
        result.append(row)  # Add the row to the result list

    # Print the entire result
    print("\n".join(result))
    print("     mo  th  we  th  fr  sa  su")


weather(temperature)
