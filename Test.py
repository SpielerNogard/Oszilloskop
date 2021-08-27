import math


wert = 1

for i in range(100):

    wert = math.pow(2,i)
    rounds = math.floor((i-2)/3) + 1
    for k in range(rounds):
        wert = wert + math.pow(10,k) * math.pow(2,i - (2 + 3*k))

    print (wert)
