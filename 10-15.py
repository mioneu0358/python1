
# 탐색 알고리즘
#1. 순차 탐색(Sequential searching)

def  Sequential_searching(data_list, targetData):
    for index,data in enumerate(data_list):
        if data == targetData:
            return index
    return None


# 2. 이진 탐색(Binary searching) - 정렬된 상태에서만 사용되어야한다.

def Binary_search(data_list, targetData):
    left = 0
    right = len(data_list) -1
    while left <= right:
        middle = (left + right) // 2
        if data_list[middle] == targetData:
            return middle
        elif data_list[middle] > targetData:
            right = middle - 1
        else:
            left = middle + 1
    return None

# 이진탐색 재귀함수로 풀기
def recursion_b(data_list, targetData,left,right):
    if left > right :
        return None
    middle =(left + right) // 2
    if data_list[middle] == targetData:
        return middle
    elif data_list[middle] > targetData:
        return recursion_b(data_list,targetData, left,middle -1)
    else:
        return recursion_b(data_list,targetData,middle +1, right)

# arr  = [1,3,4,6,7,8,10,13,14,18,19,21,24,37,40,45,71]
# print(recursion_b(arr,7,0,len(arr)-1))

def solution(n, times):
    times.sort()
    minutes = 0
    l = 1                       #최소 시간
    r = times[-1] * n      #최대 시간
    arrivals = 0
    middle = (l + r) // 2
    #n을 처리하는 최소 시간
    for t in times:
        arrivals += (middle // t)





print(list(range(1,61)))
