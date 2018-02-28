import random

if __name__ == "__main__":

    x = str(random.randint(1000, 9999))
    y = 0
    Cont = "Y"
    guesses = 0
    def reset():
        x = str(random.randint(1000,9999))
        guesses = 0
        return x, guesses


    def CowsAndBulls():
        cows = 0
        bulls = 0
        for i in range(0, 4):
            if x[i] == y[i]:
                cows += 1
            else:
                bulls += 1
        return cows, bulls

    while Cont == "Y":
        y = input('Make a guess: ')
        if y == "quit":
            Cont = "N"
        guesses += 1
        cows = CowsAndBulls()[0]
        bulls = CowsAndBulls()[1]
        if cows == 4:
            print("You have guessed correctly! It took u " + str(guesses) + " guesses.")
            Cont = input("Play agian? Y|N")
            if Cont == "Y":
                x = reset()[0]
                guesses = reset()[1]
        else:
            print(str(cows) + " Cows, " + str(bulls) + " Bulls")
