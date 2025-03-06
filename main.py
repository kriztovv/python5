

temperature = [5, 22, -3, 9, 0, 6, 7]
temp = None
def rendTemp(i):
    for j in range(7):
        if(j in temperature[] > i * 5 + 30 - 5):
            temp =+ "#"
        else:
            temp =+ " "
    return(temp)
    temp = None

def weather(temperatures):
    for i in range(13):
        print(str(-i * 5 + 30).rjust(3) + rendTemp(i))
    print("     mo  th  we  th  fr  sa  su")
weather(temperature[])