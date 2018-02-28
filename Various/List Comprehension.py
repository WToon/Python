import random

a = []
for x in range(25):
    a.append(random.randint(0, 100))


def evenList():
    b = [number for number in a if number%2 == 0]
    return b


def oddList():
    b = [number for number in a if number%2 != 0]
    return b

print(a)
x = evenList()
y = oddList()
z = evenList()+oddList()
x.sort()
y.sort()
z.sort()
print(x)
print(y)
print(z)

