#저번 시간에 스택 하고 큐 배움
# stack
#FILO/LIFO
# Queue

# 내가 쓴 코드
# progresses = [95, 90, 99, 99, 80, 99]
#
def solution(progresses, speeds):
    terms= []
    for i in range(len(progresses)):
        cnt = 0
        while progresses[i] < 100:
            progresses[i] += 1 * speeds[i]
            cnt += 1
        terms.append(cnt)
    terms.reverse()

    top = terms.pop()
    cnt = [1]
    while terms:
        elem = terms.pop()
        if elem <= top:
            cnt[-1] += 1
        else:
            top = elem
            cnt.append(1)

    answer = cnt
    return answer


# print(a)
#
# answer = []
# for i in range(len(a) - 1):
#     cnt = 0
#     if a[i] < a[i + 1]:
#         cnt += 1
#         answer.append(cnt)
#     else:
#         d_day =  i
#         for j in range(i+1, len(a)):
#             if a[d_day] < a[j]:
#                 cnt += 1
#             else:
#                 continue
#         answer.append(cnt)
# print(answer)

#민기썜 풀이
# def ceil(num): #실수를 정수로 변환
#     if num > int(num):      #소수점 밑으로 수가 있는지 판별후
#         return int(num)+1   #있다면 올림
#     return int(num)         #없으면 수 그대로 출력
#
# #
# def solution(progresses, speeds):
#     answer = []
#
#     terms = [ceil((100-a)/b) for a,b in zip(progresses,speeds)]  #기능이 완료되기까지 걸리는 기간
#     #100(완성) - 93(현재 진척도) = 7(남은 진척도) / speeds = terms
#     terms.reverse()
#     #기능 배포 개수 계산산
#     #조건1. 기능은 무조건 앞에 있는 기능이 먼저 배포 되어야한다.
#
#     top = terms.pop()
#     cnt = [1]
#     while terms:
#         elem = terms.pop()
#         if elem <= top:
#             cnt[-1] += 1
#         else:
#             top = elem
#             cnt.append(1)
#
#     answer = cnt
#     return answer
#


#리스트를 이용해서 Stack 구조를 구현해보기

#push, pop, peek


#
# def push(value):
#     stack_list.append(value)
#
# def pop():
#     del stack_list[len(stack_list)-1]
#
# def peek():
#     return stack_list[-1]
#
# stack_list = [1,2,3,4,5]
#
# push(13)
# print(stack_list)
# pop()
# print(stack_list)
# peek()
# print(stack_list)