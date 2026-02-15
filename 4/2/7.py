def chunked(lst, n):
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])
    return result



s = input().split()
n = int(input())
print(chunked(s, n))