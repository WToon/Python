sentence = input("Give a sentence: ")

def reverseWords(sentence):
    print(' '.join(sentence.split()[::-1]))

reverseWords(sentence)