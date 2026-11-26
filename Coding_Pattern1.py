1.a = [1, 2, 2, 3, 3, 3]

for i in range(len(a)):
    count = 0

    for j in range(len(a)):
        if a[i] == a[j]:
            count = count + 1

    print(a[i], "=", count)

2.a = [1, 2, 3, 2, 4, 3]

for i in range(len(a)):
    for j in range(i + 1, len(a)):
        if a[i] == a[j]:
            print(a[i])
            break

3.a = [1, 2, 2, 3, 4, 4]

for i in range(len(a)):
    count = 0

    for j in range(len(a)):
        if a[i] == a[j]:
            count = count + 1

    if count == 1:
        print(a[i])

4.a = [1, 2, 2, 3, 4, 4]

b = []

for i in range(len(a)):
    if a[i] not in b:
        b.append(a[i])

print(b)

5.a = [1, 2, 3, 1]

found = False

for i in range(len(a)):
    for j in range(i + 1, len(a)):
        if a[i] == a[j]:
            found = True

if found:
    print("True")
else:
    print("False")

6.a = [1, 2, 3, 1]
k = 3

found = False

for i in range(len(a)):
    for j in range(i + 1, len(a)):
        if a[i] == a[j] and j - i <= k:
            found = True

if found:
    print("True")
else:
    print("False")

7.a = [10, 5, 3, 4, 3, 5, 6]

for i in range(len(a)):
    for j in range(i + 1, len(a)):
        if a[i] == a[j]:
            print(a[i])
            exit()

8.a = [4, 5, 1, 2, 1, 4, 5]

for i in range(len(a)):
    count = 0

    for j in range(len(a)):
        if a[i] == a[j]:
            count = count + 1

    if count == 1:
        print(a[i])
        break

9.a = [2, 2, 1, 2, 3, 2, 2]

for i in range(len(a)):
    count = 0

    for j in range(len(a)):
        if a[i] == a[j]:
            count = count + 1

    if count > len(a) // 2:
        print(a[i])
        break

10.a = [4, 3, 2, 7, 8, 2, 3, 1]

b = []

for i in range(len(a)):
    count = 0

    for j in range(len(a)):
        if a[i] == a[j]:
            count = count + 1

    if count > 1 and a[i] not in b:
        b.append(a[i])

print(b)