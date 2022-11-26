# #정렬 알고리즘
#
# #선택정렬(selection_sort)
## 알고리즘 = 입력받은 리스트 A의 첫번째 원소 i의 위치에 최소값을 찾아 넣는다.
##          j = i+1부터 리스트의 마지막원소까지 탐지해가며 최소값을 찾고
##           구한 최소값이 i번째 값보다 작다면 교환한다.
# def selection_sort(arr):
#     for i in range(len(arr)):
#         least = i
#         for j in range(i+1,len(arr)):
#             if arr[least] > arr[j]:
#                 least = j
#         arr[least],arr[i] = arr[i],arr[least]
#     return arr
#
# arr = [6,4,3,5,1,2]
# print(selection_sort(arr))

# #버블정렬(bubble_sort)
# #알고리즘 = 입력받은 리스트A의 마지막 원소 i = len(A) -1 부터 정렬한다.
# #         j = 0 부터 i 까지 1씩 늘려가며 A[j] > A[j+1]인 경우 A[j] 와 A[j+1]을 교환한다.
# def bubble_sort(arr):
#     for i in range(len(arr)-1,0,-1):
#         for j in range(0,i):
#             if arr[j] > arr[j+1]:
#                 arr[j],arr[j+1] = arr[j+1],arr[j]
#
# arr = [6,4,3,5,1,2]
# bubble_sort(arr)
# print(arr)

# #삽입정렬(insertion_sort)
# #알고리즘 = 입력받은 리스트A의 두번째 원소 i=1부터 정렬을 시작한다.
# #          임시 저장소 k에 A[i]의 값을 저장한다.
# #          j = 1부터 출발하여 A[j-1]이 k보다 크고 j는 0보다 클때까지 j를 1씩 감소시키며 원소들을 오른쪽으로 한칸씩 이동시킨다.
# #          A[j-1]이 k보다 크면 이동을 멈추고, 이동으로 생긴 빈자리인 a[j]에 k를 삽입한다.
# #          현재 위치 i가 리스트의 마지막 원소에 도달할 때 까지 1씩 증가시키며 위를 반복한다.
# def insertion_sort(arr):
#     for i in range(1,len(arr)):
#         k = arr[i]
#         j = i
#         while arr[j-1] > k and j >0:
#             arr[j] = arr[j-1]
#             j -=1
#         arr[j] = k
# arr = [6,4,3,5,1,2]
# insertion_sort(arr)
# print(arr)


#퀵정렬(Quick_sort)
#알고리즘 =  1.입력받은 리스트의 양끝을 가리키는 Left와  Right를 만들어준다.
#          2.left와 right사이의 중앙값p(pivot)을 설정한다.
#          3. left를 오른쪽으로 움직이며 p보다 큰 값의 위치를 찾는다.
#          4. right를 왼쪽으로 움직이며 p보다 작은 값의 위치를 찾는다.
#          5. left와 right의 값을교환한다.
#          6. left<right일때까지 3_5를 반복한다.
#          7. p왼쪽의 길이가 2 이상이면 그 부분을 대상으로 퀵정렬을 한다.
#          8. p오른쪽의 길이가 2 이상이면 그 부분을 대상으로 퀵 정렬을 한다.



# def Quick_sort(arr,left,right):
#     if right - left < 1:    #원소의 개수가 1개보다 작으면 리턴
#         return
#
#     p = (left+right) // 2   #피버값 생성
#     i = left                #left
#     j = right               #right
#     while i < j:            #i가 j보다 작을때까지 == 서로 만나거나 교차하기 전까지 반복
#         while arr[i] < arr[p] : #피벗보다 큰arr[i]찾기
#             i += 1
#         while arr[j] > arr[p]:  #피벗보다 큰 arr[j]찾기
#             j -= 1
#         arr[i],arr[j] = arr[j],arr[i] #두 값을 교환함
#
#         Quick_sort(arr,left,i-1)      #남은 부분에 대한 퀵정렬
#         Quick_sort(arr,j+1,right)     #남은 부분에 대한 퀵정렬
#
#
# arr = [3,9,2,8,5,1,6,4,7]
# Quick_sort(arr,0,len(arr)-1)
# print(arr)


#합병정렬(merge sort) - 외부정렬에서 사용
#두개의 정렬된 파일을 하나의 큰 정렬된 파일로 합친다.

def Merge_sort(arr):
    if len(arr) < 2:
        return arr
    mid = len(arr)//2
    left_arr = Merge_sort(arr[:mid])
    right_arr = Merge_sort(arr[mid:])
    # print(left_arr,right_arr)
    Merge_arr = []
    l =0
    r =0
    while l < len(left_arr) and r < len(right_arr):
        #둘중 작은 값을 찾아 넣는다.
        if left_arr[l] < right_arr[r]:
            Merge_arr.append(left_arr[l])
            l += 1
        else:
            Merge_arr.append(right_arr[r])
            r+= 1
    Merge_arr += left_arr[l:]
    Merge_arr += right_arr[r:]

    # 왼쪽 오른쪽에서 작은 값을 찾으며 합침
    # 값이 남은 리스트를 그대로 뒤에 붙여줌
    return Merge_arr

# def Merge_sort(arr):
#     if len(arr) < 2:
#         return arr
#     mid = len(arr)//2
#     left_arr = Merge_sort(arr[:mid])
#     right_arr = Merge_sort(arr[mid:])
#     # print(left_arr,right_arr)
#     Merge_arr = []
#     while left_arr and right_arr:
#         #둘중 작은 값을 찾아 넣는다.
#         if left_arr[0] < right_arr[0]:
#             Merge_arr.append(left_arr.pop(0))
#         else:
#             Merge_arr.append(left_arr.pop(0))
#
#     while left_arr:
#         Merge_arr.append(left_arr.pop(0))
#     while right_arr:
#         Merge_arr.append(right_arr.pop(0))
#     return Merge_arr
arr = [3,9,2,8,5,1,6,4,7,10]
arr = Merge_sort(arr)
print(arr)