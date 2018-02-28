import getpass

Continue = "Y"
while Continue == "Y":
    playerA = input("playerA : R|P|S?: ")
    playerB = input("playerB : R|P|S?: ")
    if playerA == playerB:
        print("Draw!")
    elif playerA == "R":
        if playerB == "P":
            print("PlayerB wins!")
        else:
            print("PlayerA wins!")
    elif playerA == "P":
        if playerB == "R":
            print("playerA wins!")
        else:
            print("playerB wins!")
    elif playerA == "S":
        if playerB == "R":
            print("playerB wins!")
        else:
            print("playerA wins!")
    else:
        print("Invalid input")
    Continue = input("Continue playing? Y/N: ")