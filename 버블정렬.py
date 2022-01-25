#python
#가장 작은 숫자를 차례대로 탐색
# 가장 왼쪽자리 부터 스왑
#가장 작은 숫자를 선택하는 방식으로 정렬


# def selction_sort(a):
#     for i in range(len(a)-1):        #스왑 해주다 보면 마지막은 해줄 필요가 없어지기 때문에
#         min_index = i                               # 최소값이 위치할 자리
#         for j in range(i+1,len(a)):  #i위치에 있는 것을 제외한 나머지 내에서 최소값을 찾아야하기 때문에
#             if a[j] < a[min_index]:          #현재 위치(j)에 있는 수가 최소값이 있어야할 위치의 수보다 작으면
#                 a[j],a[min_index] = a[min_index],a[j]   # 두 위치의 수를 스왑 해준다
#             print(a)

# selction_sort([3,4,5,1,2])

#버블정렬
#붙어있는 두 수를 비교하여 큰수는 오른쪽으로 작은수는 왼쪽으로 스왑
# def bubble_sort(a):
#     length = len(a) - 1   #스왑해주다 보면 마지막은 해줄 필요가 없어지기 때문에
#     for i in range(length):                     #마지막을 제외한 범위 선택
#         for j in range(length - i):             #앞뒤 숫자를 순차적으로 비교해서 큰수는 뒤로만 가기 때문에 가장 큰수가 가장 오른쪽으로 가기 때문에
#                                                 #length - i를 해줘서 오른쪽으로 밀어 넣은 수의 갯수 만큼 시도를 뺴준다
#             if a[j] > a[j + 1]:                       #붙어 있는 두 수를 비교해서 앞에수가 큰 수면 자리를 바꿔준다
#                 a[j], a[j + 1] = a[j + 1], a[j]     # 두 위치의 수를 스왑
#                 print(a)
# a = [3,4,5,1,2]
# bubble_sort(a)
#삽입정렬 insert_sort
#정렬범위를 1칸씩 확장해 가면서 새롭게 정렬범위에 들어온 값을 기존 값들과 비교하여 알맞은 자리에 꼽아주는 알고리즘

# a = [2, 1, 5, 4, 3]

# for i in range(1,len(a)):           #j의 범위
#     for j in range(i, 0, -1):
#         if a[j-1]> a[j]:
#             a[j-1],a[j] = a[j],a[j-1]
#             print(a)

# for i in range(1, len(a)):
#     j = i
#     while j > 0 and a[j - 1] > a[j]:
#         a[j - 1], a[j] = a[j], a[j - 1]
#         j -= 1
#         print(a)
#


