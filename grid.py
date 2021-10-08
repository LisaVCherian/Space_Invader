def sort_string(string):
    return "".join(sorted(string))


for _ in range(int(input())):
    n = int(input())
    string = []
    for i in range(n):
        s = input()
        string.append(sort_string(s))
    value = True
    for j in range(n):
        for i in range(n - 1):
            if string[i][j] > string[i + 1][j]:
                value = False
                break
        if not value:
            break

    if value:
        print('YES')
    else:
        print('NO')
