def oddEven():
    try:
        num = int(input("give any number: "))
        if num % 4 ==0:
            print("The given number is a multiple of 4")
        elif num % 2 != 0:
            print("The given number is odd")
        else:
            print("The given number is even")
    except:
        print("Input invalid")

def dividable():
    try:
        num1 = int(input("give a number: "))
        num2 = int(input("give a second number: "))
        if num1%num2 == 0:
            print("The numbers are divisable")
        else:
            print("The numbers are not divisable")
    except:
        print("Input invalid")

oddEven()
print(">-----------------------------------------<")
dividable()

