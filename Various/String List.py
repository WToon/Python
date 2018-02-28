word = str(input("give a random string: "))


def palinInvers():
    if word == word[::-1]:
        print("The string is a palindrome")
    else:
        print("The string is not a palindrome")


def palinLists():
    for i in range(len(word)-1):
        if word[i] != word[len(word)-i-1]:
            print("The string is not a palindrome")
            return
    print("The string is a palindrome")

palinInvers()
palinLists()