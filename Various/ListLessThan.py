import random

# creating a list containing random integers between 0-100
a = []
for x in range(25):
    a.append(random.randint(0, 100))


def lessthan20():
    for i in a:
        if i < 20:
            print(i)


def lessthan20list():
    b = []
    for i in a:
        if i < 20:
            b.append(i)
    print(b)


def lessthaninput():
    b = []
    try:
        x = int(input("give a random number: "))
    except:
        print("invalid input")
        return
    for i in a:
        if i < x:
            b.append(i)
    print(b)

print(a)
lessthan20()
lessthan20list()
lessthaninput()
