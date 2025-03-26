import random

#nahodne pocasi
temperature = [random.randint(-30, 30) for _ in range(7)]


def rendtemp(i):
    temp = ""
    for j in range(7):
        if temperature[j] > -i * 5 + 25:
            temp += "   #"
        else:
            temp += "    "
    return temp


def weather(temperatures):
    result = []
    for i in range(13):
        row = str(-i * 5 + 30).rjust(3) + rendtemp(i)
        result.append(row)

    print("\n".join(result))
    print("     mo  th  we  th  fr  sa  su")

weather(temperature)
