#벨먼-포드 알고리즘(BEllman - Ford Algorithm)

#최단거리테이블초기화
#출발노드설정
#모든

#matrix: 가중치 인접행렬
# start: 시작노드
def bellman_ford(matrix,start):
    # 노드의 개수
    v = len(matrix)

    # 1. 최단 거리 테이블 초기화
    distance = [float('inf')] * v

    # 2. 출발 노드 설정
    distance[start] = 0

    # 3. 모든 노드에 대하여 최소 비용 계산
    # (v번, 마지막 음의 사이클 검사까지 포함함)

    for n in range(v):
        for x in range(v):
            for y in range(v):
                cost = matrix[x][y]

                # 최소 비용 갱신
                # 원래라면 distacx[y] != float('inf')를 검사해야 한다.
                # 여기서 검사하지 않은 이유는 어차피 inf + x == inf 이기 때문
                if distance[y] > distance[x] + cost:
                    distance[y] = distance[x] + cost

                    # 4. v번째 에 갱신이 발생했다면 최단 거리를 구할 수 없음
                    if n == v -1:
                        return False, distance
    return True, distance

# inf = float('inf')
# matrix = [
#     [0,7,5,3,inf],
#     [inf,0,inf,inf,inf],
#     [inf,inf,0,3,3],
#     [inf, 3,inf,0,-6],
#     [inf,inf,2,inf,0]
# ]
# success, distance = bellman_ford(matrix,0)
# print('최단 경로의 존재:',success)
# print('마지막 계산된 최단 경로:', distance)


# matrix2 = [
#     [0,3,5,1,inf],
#     [inf,0,6,inf,4],
#     [inf,inf,0,-3,-3],
#     [inf,-2,inf,0,-1],
#     [inf,inf,inf,inf,0]
# ]
# success,distance = bellman_ford(matrix2,0)
# print('최단 경로의 존재:',success)
# print('마지막 계산된 최단 경로:', distance)


# 타임 머신 https://www.acmicpc.net/problem/11657
def bellman(v,matrix,start):
    # 1. 최단 거리 테이블 초기화
    distance = [float('inf')] * (v+1)
    # 2. 출발 노드 설정
    distance[start] = 0

    # 3. 모든 노드에 대하여 최소 비용 계산
    # (v번, 마지막 음의 사이클 검사까지 포함함)

    for n in range(v):
        for x,y, cost in matrix:
            # 최소 비용 갱신
            # 원래라면 distacx[y] != float('inf')를 검사해야 한다.
            # 여기서 검사하지 않은 이유는 어차피 inf + x == inf 이기 때문
            if distance[y] > distance[x] + cost:
                distance[y] = distance[x] + cost
                # 4. v번째 에 갱신이 발생했다면 최단 거리를 구할 수 없음
                if n == v - 1:
                    return [-1]
    return distance[2:]



import sys
input = sys.stdin.readline
# n = 도시 개수, m = 도시간 버스의 노선 개수
# n, m = map(int,input().split())
# matrix = [tuple(map(int,input().split())) for _ in range(m)]
#
#
# result = bellman(m,matrix, 1)
# for i in result:
#     print(i if float('inf') > i else -1)



# 웜홀 https://www.acmicpc.net/problem/1865

TC = int(input())
for _ in range(TC):
    # n = 지점의 수, m = 도로의 개수, w = 웜홀의 개수
    n,m,w = map(int,input().split())
    matrix = [tuple(map(int,input().split())) for _ in range(m)]
    hole = [list(map(int,input().split())) for _ in range(w)]
    print(matrix)
    print(hole)

