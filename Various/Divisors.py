def getDivisors():
    try:
        num = int(input("give a number: "))
    except:
        print("Invalid input")

    a = range(1, num+1)
    b = []
    for i in a:
        if num%i == 0:
            b.append(i)
    print(b)

def bit():
    a = 0
    for x in range(0, 32):
        a += 2**x

    print(a)

getDivisors()
bit()
