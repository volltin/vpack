from vpack import breakpt

for i in range(10):
    print(i)
    breakpt.at(8) # break at i = 7
    breakpt.at(5) # break at i = 4

for i in range(6):
    print(i)
    if i == 2: breakpt.disable() # disable breakpt
    if i == 4: breakpt.enable() # enable breakpt
    breakpt.always() # break at i = 0, 1, 4, 5
