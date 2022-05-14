#그래프와 인접행렬
# 0-------1
# | \     |
# |   \   |
# |     \ |
# 2-------3


# matrix = [
#     [1,1,1,1],
#     [1,1,0,1],
#     [1,0,1,1],
#     [1,1,1,1]
# ]
# visit = [False] * len(matrix)
# # DFS(깊이 우선 탐색)
# # vertex: 현재 정점, matrix: 인접행렬, visit: 방문한 정점 표시
#
# def dfs(vertex,matrix,visit):
#     #현재 정점을 방문했다고 표시함
#     visit[vertex] = True
#     print("정점", vertex ,'방문')
#     #현재 정점에서 갈 수 있는 가능한 정점을 탐색함
#     # 방문한 적 없고 간선이 연결된 경우
#     for i in range(len(matrix)):
#         if visit[i] == False and matrix[vertex][i] == 1:
#             dfs(i,matrix, visit)    #재귀 호출이 발생
#
# dfs(0,matrix,visit)



# #BFS(너비 우선 탐색)
# def bfs(vertex, matrix):
#     visit = [False] * len(matrix)
#     #리스트로 큐 구현
#     Que = []
#     #큐에 첫번째 정점 삽입
#     Que.append(vertex)
#     visit[vertex] = True
#     while Que:  #큐가 비어있지 않을떄 까지 탐색
#         curr =  Que.pop(0)  # 큐에서 정점 하나를뺀다
#         print("정점",curr, "방문")
#         for i in range(len(matrix)):
#             if visit[i] is  False and matrix[curr][i]== 1:
#                 Que.append(i)
#                 visit[i] = True
# bfs(0,matrix)


#프로그래머스
# def dfs(curr,idx,numbers,target):
#     #현재 인덱스와 numbers의 길이가 같을떄
#     if idx == len(numbers):
#         if curr == target:
#             return 1
#         else:
#             return 0
#
#     count = dfs(curr - numbers[idx], idx+1, numbers, target)
#     count += dfs(curr + numbers[idx], idx+1, numbers, target)
#
# def solution(numbers,target):
#     return dfs(0,0,numbers,target)
# print(solution([1,1,1,1,1],3))

#43162번 네트워크
#
# def dfs(vertex,computers):
#     global visit
#     #현재 정점을 방문했다고 표시함
#     visit[vertex] = True
#     #현재 정점에서 갈 수 있는 가능한 정점을 탐색함
#     # 방문한 적 없고 간선이 연결된 경우
#     for i in range(len(computers)):
#         if visit[i] == False and computers[vertex][i] == 1:
#             dfs(i,computers)    #재귀 호출이 발생

# def solution(n, computers):
#     global visit
#     visit = [False] * len(computers)
#     network = 0
#     for i in range(len(visit)):
#         if visit[i] == False:
#             dfs(i, computers)
#             network += 1
#     return network
#
# n=3
# computers = [[1, 1, 0],
#              [1, 1, 0],
#              [0, 0, 1]]
#
# print(solution(n,computers))