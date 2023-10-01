def solution(n,left,right):
    arr = []
    for x in range(left,right+1):
        i = x // n
        j = x % n
        arr.append(max(i,j) + 1)
    return arr

print(solution(4,7,14))