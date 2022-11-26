# #프로그래머스 행렬의 곱셈
# def solution(arr1,arr2):
#     # arr1 = A로 arr2 = B로 설명
#     # 0으로 채워진 행렬을 먼저 생성
#     # 행렬 곱의 결과는 b행렬의 행의 길이와 A행령의 열의 길이에 달려있다
#
#     answer = [[0 for _ in range(len(arr2[0]))] for _ in range(len(arr1))]
#
#     for i in range(len(arr1)):
#         for j in range(len(arr2[0])):
#             for k in range(len(arr1[0])):
#                 answer[i][j] += (arr1[i][k] * arr2[k][j])
#     return answer
#
# arr1 =[[2, 3, 2], [4, 2, 4], [3, 1, 4]]
#
# arr2 =	[[5, 4, 3], [2, 4, 1], [3, 1, 1]]
# print(solution(arr1,arr2))


# #Heap(힙)

class Heap:
    def __init__(self,_list):
        self.heap = [0]+_list

    #최소 self.heap

    def insert(self, n):              # self.heap에 값을 넣는 함수
        self.heap.append(n)          # self.heap의 맨 마지막에 값을 삽입한다.
        curr_pos = len(self.heap)-1  # 현재 위치 기억(마지막자리에 넣었기 떄문에 길이 -1)
        while curr_pos != 0:    # 현재 위치가 루트가 아닐 때 까지
            parent_pos = curr_pos // 2 # 부모의 위치는 자신의 위치 // 2
            if self.heap[parent_pos] > self.heap[curr_pos]:
                self.heap[parent_pos],self.heap[curr_pos] = self.heap[curr_pos],self.heap[parent_pos]
            else:
                break
            curr_pos = parent_pos   # 값이 교환되었으므로 자식을 가리키는 index도 변경시켜준다.


    def smallest(self,):
        if len(self.heap) == 1:
            return None
        value = self.heap[1]         # 반환할 최소값을 기억해둔다.
        last = self.heap.pop()
        if len(self.heap) == 1:
            return value
        self.heap[1] = last

        p = 1                   #현재 위치(부모의 위치)
        while p * 2 <= len(self.heap) -1 :        # p의 자식이 존재할 때 까지
            c0 = p * 2                  # 왼쪽 자식의 위치
            c1 = p * 2 + 1             # 오른쪽 자식의 위치
            minc = 0                   # 최소값을 가질 자식의 위치
            if c1 <= len(self.heap) -1:     #오른쪽 자식이 존재할 때
                minc = c0 if self.heap[c0] < self.heap[c1] else c1    #자식 둘을 비교해서 최소값을 받는다.
            else:
                minc = c0
            if self.heap[p] > self.heap[minc]:
                self.heap[p],self.heap[minc] = self.heap[minc],self.heap[p]
            else:
                break

            p = minc                   # 값을 교환했으면 위치도 따라서 바꾸어 준다.

        return value
#
#
#
#
# #더 맵게
#
# insert(12)
# insert(10)
# insert(9)
# insert(3)
# insert(2)
# insert(1)
# print(self.heap)
#
# for i in range(6):
#     print(smallest())





#최소 s

# def insert(s,n):              # s에 값을 넣는 함수
#     s.append(n)          # s의 맨 마지막에 값을 삽입한다.
#     curr_pos = len(s)-1  # 현재 위치 기억(마지막자리에 넣었기 떄문에 길이 -1)
#     while curr_pos != 0:    # 현재 위치가 루트가 아닐 때 까지
#         parent_pos = curr_pos // 2 # 부모의 위치는 자신의 위치 // 2
#         if s[parent_pos] > s[curr_pos]:
#             s[parent_pos],s[curr_pos] = s[curr_pos],s[parent_pos]
#         else:
#             break
#         curr_pos = parent_pos   # 값이 교환되었으므로 자식을 가리키는 index도 변경시켜준다.
#
# def smallest(s):
#     if len(s) == 1:
#         return None
#     value = s[1]         # 반환할 최소값을 기억해둔다.
#     last = s.pop()
#     if len(s) == 1:
#         return value
#     s[1] = last
#
#     p = 1                   #현재 위치(부모의 위치)
#     while p * 2 <= len(s) -1 :        # p의 자식이 존재할 때 까지
#         c0 = p * 2                  # 왼쪽 자식의 위치
#         c1 = p * 2 + 1             # 오른쪽 자식의 위치
#         minc = 0                   # 최소값을 가질 자식의 위치
#         if c1 <= len(s) -1:     #오른쪽 자식이 존재할 때
#             minc = c0 if s[c0] < s[c1] else c1    #자식 둘을 비교해서 최소값을 받는다.
#         else:
#             minc = c0
#         if s[p] > s[minc]:
#             s[p],s[minc] = s[minc],s[p]
#         else:
#             break
#
#         p = minc                   # 값을 교환했으면 위치도 따라서 바꾸어 준다.
#
#     return value

def serch(s,k):
    for i in s:
        if k > i:
            return False
    return True

def solution(scoville,k):
    count = 0
    s  = Heap(scoville)
    print(s.heap)

    while min(s.heap[1:]) < k and s.heap != [0]:
        l1 = s.smallest()
        l2 = s.smallest()

        mix_s = l1 + l2 * 2
        print(l1,l2,s.heap,mix_s)
        s.insert(mix_s)
        count += 1


    return count

s = [1, 2, 3, 9, 10, 12]
k = 7
print(solution(s,k))