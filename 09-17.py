# from collections import  deque
# queue = deque(['a','b','c'])
# queue.appendleft('d')
# queue.appendleft('e')
# print(queue)
# print(queue.pop())
# print(queue.pop())
# print(queue)
#
# squares= list(map(lambda x: x**2,range(10)))
# #1에서 10까지 제곱.
# vec = [-4,-2,0,2,4]
# #[x*2 for x in vec] 리스트 2배
# #요놈
#
# fruits = ['apple','banana','coconut']
# [f.strip() for f in fruits] #알파벳 순으로 배열
#
# vecvecvec = [[1,2,3],[4,5,6],[7,8,9]]
# #[num for elem in vecvecvec for num in elem]# 리스트 분해
#
# matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
# transposed = [[row[i], for ]]
# transposed = []
# for i in range(4):
#     transposed_row = []
#     for row in matrix:
#         transposed_row.append(row[i])\
#     transposed.append((transposed_row))
#
# list(zip(*matrix  ))
#
#
#
# import sys
# b = int(sys.stdin.readline())
#
#
#
# stick = [[int(sys.stdin.readline()) for _ in range(b)]]
# answer = 1
#
#
# for i in stick:
#     a = stick.pop()
#     stickr = stick
#     stickr.reverse()
#     if a < i:
#         answer += 1
#     continue
#
#
# print(answer)
#
# import sys
# n = int(sys.stdin.readline())
#
# stack = [int(sys.stdin.readline()) for _ in range(n)]
#
# count = 0
# max_stick = 0
#
# while stack:
#     stick = stack.pop()
#     if stick > max_stick:
#         max_stick = stick
#         count += 1
# print(count)


import sys
from collections import  deque
n = int(sys.stdin.readline())

queue = deque(num for num in range(1, n+1))

t =1

while len(queue) != 1:
    k = t**3 % len(queue)
    for i in range(k):
        x = queue.popleft()
        queue.append(x)

    queue.pop()
    t+= 1

print(queue[0])


