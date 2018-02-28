Cont = "Y"

def promptNumber():
    try:
        check = int(input("Give a testnumber: "))
        loop = False
        return check, loop
    except:
        print("Invalid input")


def checkPrime(number):
    divisors = []
    for i in range(1, number):
        if number%i == 0:
            divisors.append(i)
    if len(divisors) == 1:
        return True
    else:
        return False

while Cont == "Y":
    loop = True
    while loop == True:
        res = promptNumber()
        check = res[0]
        loop = res[1]
    if checkPrime(check):
        print("The given number is prime")
    else:
        print("The given number is nonprime")
    Cont = input("Test another number? Y|N: ")
