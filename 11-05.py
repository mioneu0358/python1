# # BFS(너비우선탐색) 시작경로에 대해 항상 최적해를 갖는다.
# from collections import deque
#
# # def BFS(matrix,start_node):
# #     visit = [False] * len(matrix)
# #     queue = deque()
# #
# #     # 큐에 탐색 시작 노드를 넣는다.
# #     queue.append(start_node)
# #     visit[start_node] = True
# #     print('방문 %d 노드'%start_node)
# #
# #     # 큐가 빌 때까지 수행
# #     while queue:
# #         node = queue.popleft()
# #
# #         # 현 위치에서 방문 가능한 모든 노드들을 큐에 넣는다.
# #         for next_node in range(len(matrix)):
# #             if matrix[node][next_node] == 1:
# #                 if not visit[next_node]:
# #                     queue.append(next_node)
# #                     visit[next_node] = True
# #                     print('방문 %d 노드'%next_node)
#
# # matrix = [[0,1,0,1,0],
# #           [1,0,1,0,0,],
# #           [0,1,0,1,1],
# #           [1,0,1,0,0],
# #           [0,0,1,0,0]]
# #
# # BFS(matrix,0)
# # 0 =벽 , 1 = 길
#
#
#
# # def BFS(matrix,start_node):
# #     visit = [False] * len(matrix)
# #     queue = deque()
# #
# #     # 큐에 탐색 시작 노드를 넣는다.
# #     queue.append(start_node)
# #     visit[start_node] = True
# #     print('방문 %d 노드'%start_node)
# #
# #     # 큐가 빌 때까지 수행
# #     while queue:
# #         node = queue.popleft()
# #
# #         # 현 위치에서 방문 가능한 모든 노드들을 큐에 넣는다.
# #         for next_node in range(len(matrix)):
# #             if matrix[node][next_node] == 1:
# #                 if not visit[next_node]:
# #                     queue.append(next_node)
# #                     visit[next_node] = True
# #                     print('방문 %d 노드'%next_node)
#
# from collections import deque
# # 이동 가능한 좌표인지 검증
# def movable(x,y,maps):
#     w = len(maps)
#     h = len(maps[0])
#     if 0 <= x < w and y < h and maps[x][y] == 1:
#         return True
#     return False
# def BFS(maps):
#     # 방문을 표시할 이중 리스트
#     visit = [[False] * len(m) for m in maps]
#     queue = deque()
#     # 목표
#     tx,ty = len(maps) - 1, len(maps[0]) - 1
#
#     #시작 좌표 및 경로의 길이의 초기값 enque
#     queue.append((0,0,1))   #x,y,d
#     while queue:
#         # 좌표와 경로의 길이를 deque
#         x,y,d = queue.popleft()
#         # 꺼낸 좌표와 목표가 같을 경우 길이 반환
#         if (x,y) == (tx,ty):
#             return d
#         # 현재 좌표에서 갈 수 있는 경로에 큐를 enque
#         offset = [[1,0],[-1,0],[0,1],[0,-1]]
#         for ox, oy in offset:
#             nx, ny = x + ox, y + oy
#             if movable(nx,ny,maps) and not visit[nx][ny]:
#                 queue.append((nx,ny,d+1))
#                 visit[nx][ny] = True
#     return -1
#
#
#
#
# def solution(maps):
#     return BFS(maps)
#
# map = [[1,0,1,1,1],
#        [1,0,1,0,1],
#        [1,0,1,1,1],
#        [1,1,1,0,1],
#        [0,0,0,0,1]]
#
# print(solution(map))

# 어떤 점이 테두리 위에 존재하는가
# 유효한 테두리 좌표인지 검사하는 함수
def is_boundary(point,rects):
    # 1. point가 어떤 rect의 범위에 속해야 하고,
    x,y = point
    stat = False
    for rect in rects:
        x1,y1,x2,y2 = rect
        if x1 <= x <= x2 and y1 <= y <= y2: # 해당 좌표가 어느 사각형이던 테두리나 내부에 존재한다면
            stat = True
            break
    if not stat:
        return False
    # 2, point는 어떤 rect의 테두리 내부에 있을경우 안댐
    for rect in rects:
        x1,y1,x2,y2 = rect
        if x1 < x < x2 and y1 < y < y2:
            return False
    return True

def solution(rectangle, characterX, characterY, itemX, itemY):
    answer = 0


    x1,y1,x2,y2 = rects
    print(x1,y1,x2,y2)
    return answer




rectangle,characterX,characterY,itemX,itemY=[[1,1,7,4],[3,2,5,5],[4,3,6,9],[2,6,8,8]],1,3,7,8
# print(solution(rectangle,characterX,characterY,itemX,itemY))
