import time

#선형 탐색 liner search

def liner_search(_list,data):
    for i, n in enumerate(_list):
        if n == data:
            return i
    return None


# 이진 탐색(binary search)
# 알고리즘
# 1. 리시트는 정렬이 되어 있어야 한다.
# 2. 리스트의 시작과 끝을 left, right로 지정하고 middle은 (left + right) // 2로 지정한다.
# 3. middle번째의 값이 찾고자 하는 값이랑 같으면 해당 위치를 반환한다.
# 4. 값이 다른경우
#    4-1. middle 보다 찾는 값이 크다면 -> left = middle + 1
#    4-2. middle 보다 찾는 값이 작다면 -> right = middle - 1
#    4-3. 위를 수행 후 3번 부터 다시 실행
# 5. left > right 가 되는 경우  값을 찾지 못한것으로 보고 None을 리턴

def binary_search(_list,data):
    left = 0
    right = len(_list) -1

    while left <= right:
        middle = (left + right) // 2
        if _list[middle] == data:
            return middle
        elif _list[middle] < data:
            left = middle + 1
        else:
            right = middle -1
    return None

a = list(range(100000000))
key = 7500000
start = time.time()
print("찾은 위치:",liner_search(a,key))
print("수행 시간:", time.time() - start)
start = time.time()
print("찾은 위치:",binary_search(a,key))
print("수행 시간:", time.time() - start)