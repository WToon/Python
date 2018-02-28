
def isOfTypeInt(s):
    try:
        int(s)
        return True
    except:
        return

def calc(dateofbirth):
    if isOfTypeInt(dateofbirth):
        print("you will be 100 years old in " + str(int(dateofbirth)+100))

dateofbirth = input("state the year of birth: ")
copyamount = input("How many times do u want this msg printed? ")

if isOfTypeInt(copyamount) and isOfTypeInt(dateofbirth):
    for i in range(0, int(copyamount)):
        calc(dateofbirth)
        i += 1
else:
    print("Input of invalid type")


