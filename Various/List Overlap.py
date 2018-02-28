import random

a = []
b = []

for x in range(25):
    a.append(random.randint(0, 100))
    b.append(random.randint(0, 100))
    a.sort()
    b.sort()

print(a, "\n", b)


def getOverlap():
    c = []
    for x in a:
        for y in b:
            if x == y and x not in c:
                c.append(x)
    print(c)


def getOverlap2():
    c = []
    for x in a:
        if x in b and x not in c:
            c.append(x)
    print(c)

getOverlap()
getOverlap2()