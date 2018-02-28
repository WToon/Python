import random

a = []
b = []
for x in range(25):
    a.append(random.randint(0, 100))
    b.append(random.randint(0, 100))

c = []
c = [number for number in a if number in b]

a.sort()
b.sort()
c.sort()
print(a)
print(b)
print(c)