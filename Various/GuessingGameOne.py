import random

Cont = "Y"
Start = True


def reset():
    x = random.randint(0, 100)
    guesses = 0
    return x, guesses

while Cont == "Y":
    if Start == True:
        guesses = 0
        x = random.randint(0, 100)
        Start = False
    y = "empty"
    while type(y) != int:
        try:
            y = int(input("Make a guess: "))
        except:
            print("give a valid input" )
    guesses += 1
    if x == y:
        print("You guessed right!")
        print("It took u " + str(guesses)+ " guesses")
        print(">-------<")
        x = reset()[0]
        guesses = reset()[1]
        Cont = input("Continue playing? Y|N: ")
    elif x >= y:
        print("You guessed too low")
    else:
        print("You guessed too high")


