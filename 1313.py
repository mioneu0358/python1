# # # def solution(p):
# # #     answer = ""
# # #     #1단계- p가 빈문자열이면 빈 문자열반환 or 올바른 괄호 문자열이면 p반환
# # #     if len(p) == 0 or right(p):
# # #         return p
# # #     #2단계 -
# # #     return recursion(p)
# # #
# # #
# # #
# # #
# # #
# # #
# # # def recursion(p):
# # #     p = list(p)
# # #     u = ''
# # #     while p:
# # #         u+=p.pop(0)
# # #         if u.count("(") == u.count(")"):
# # #             break
# # #     v = ''.join(p)
# # #     if right(u):
# # #         u += solution(v)
# # #     else:
# # #         temp = '('+ solution(v) + ')'
# # #         for i in u[1:-1]:
# # #             if i =='(':
# # #                 temp += ')'
# # #             else:
# # #                 temp += '('
# # #     return temp
# # #
# # #
# # # def right(s):
# # #     stack = []
# # #     for i in s:
# # #         if len(stack) == 0 :
# # #             stack.append(i)
# # #         else:
# # #             if i == ")":
# # #                 if stack[-1] == "(":
# # #                     stack.pop(-1)
# # #             else:
# # #                 stack.append(i)
# # #     return len(stack) == 0
# # # p = "()))((()"
# # # print(solution(p))
# #
# #
# # # 균형잡힌 괄호 문자열인지 판별하는 함수
# # def balance(s):
# #     if s == "":
# #         return False
# #     return s.count("(") == s.count(")")
# #
# #
# # def correct(s):
# #     stack = [""]  # 빈 문자열을 넣어 out of index방지
# #     for ch in s:
# #         if ch == '(':
# #             stack.append(ch)
# #         elif ch == ')' and stack[-1] == '(':
# #             stack.pop(-1)
# #         else:  # 스택의 Top에 매칭되는 괄호가 없으면 올바르지 않음
# #             return False
# #     return len(stack) == 1  # 스택이 비어있어야 올바르다.
# #
# #
# # def solution(p):
# #     # 1. 입력이 빈 문자열인 경우와 올바른 경우 그대로 반환
# #     if p == "" or correct(p):
# #         return p
# #     # 2. 문자열 p를 균형잡힌 괄호 문자열 u,v로 분리
# #     i = 0
# #     while not balance(p[:i]):
# #         i += 2
# #     u = p[:i]
# #     v = p[i:]
# #
# #     # 3. 문자열 u가 올바른 괄호 문자열인 경우 v에 대해 1단계부터 다시 수행
# #     if correct(u):
# #         return u + solution(v)
# #
# #     # 4.4. 문자열 u가 "올바른 괄호 문자열"이 아니라면 아래 과정을 수행합니다.
# #     else:
# #         # 4-1. 빈 문자열에 첫 번째 문자로 '('를 붙입니다.
# #         # 4-2. 문자열 v에 대해 1단계부터 재귀적으로 수행한 결과 문자열을 이어 붙입니다.
# #         # 4-3. ')'를 다시 붙입니다.
# #         answer = "(" + solution(v) + ")"
# #         # 4-4. u의 첫 번째와 마지막 문자를 제거하고, 나머지 문자열의 괄호 방향을 뒤집어서 뒤에 붙입니다.
# #         for ch in u[1:-1]:
# #             if ch == '(':
# #                 answer += ')'
# #             else:
# #                 answer += "("
# #     return answer
# #
# # p = "()))((()"
# # print(solution(p))
# #
# #
# def Turn_matrix(query, matrix):
#     x1,y1,x2,y2 = query
#     new_matrix = matrix
#
#     min = len(matrix)
#     nums = []
#     for x in range(x1-1,x2):
#         for y in range(y1-1,y2):
#             if x not in [x1-1,x2-1] and y not in [y1-1,y2-1]:
#                 continue
#             if x == x-1:
#                 if y == y-1
#
#
#             if matrix[x][y] < min:
#                 min = matrix[x][y]
#
#
#
#     print(nums)
#
#
#     return min
#
#
#
# def solution(rows, columns, queries):
#     answer = []
#     matrix = []
#     num =1
#     for i in range(rows):
#         row = []
#         for j in range(columns):
#             row.append(num)
#             num += 1
#         matrix.append(row)
#     print(matrix)
#     for query in queries:
#         answer.append(Turn_matrix(query, matrix))
#     return answer
# rows = 6
# columns = 6
# queries = [[2,2,5,4],[3,3,6,6],[5,1,6,3]]
# print(solution(rows, columns,queries))
#

def rotate(matrix,x1,y1,x2,y2):
    min_v = 100*100
    last = matrix[x1][y1]

    #x1,y1에서 x2,y1까지의 값을 움직임
    for xn in range(x1,x2):
        matrix[xn][y1] = matrix[xn+1][y1]
        min_v = min(min_v, matrix[xn+1][y1])
    #x2,y1 에서 x2,y2까지의 값을 움직임
    for yn in range(y1,y2):
        matrix[x2][yn] = matrix[x2][yn+1]
        min_v = min(min_v,matrix[x2][yn+1])
    #x2,y2에서 x1,y2까지의 값을 움직임
    for xn in range(x2-1,x1-1,-1):
        matrix[xn+1][y2] = matrix[xn][y2]
        min_v = min(min_v,matrix[xn][y2])
    #x1,y2에서 x1,y1까지의 값을 움직임
    for yn in range(y2-1,y1,-1):
        matrix[x1][yn+1] = matrix[x1][yn]
        min_v = min(min_v,matrix[x1][yn])
    matrix[x1][y1+1] = last
    min_v = min(min_v,last)
    return min_v



def solution(rows, columns, queries):
    # row x colums 행렬 생성(좌표가 1부터 시작하므로 각 영역 +1씩 해줌)
    matrix = [[0] * (columns+1) for _ in range(rows+1)]
    #값을 순서대로 채워줌
    for x in range(1,rows+1):
        for y in range(1, columns + 1):
            matrix[x][y] = columns * (x-1) + y
    print(matrix)
    #주어진 queris 영역을 시계 방향으로 회전시키면서 최소값 리스트를 만듦
    answer = []
    for query in queries:
        x1,y1,x2,y2 = query
        answer.append(rotate(matrix,x1,y1,x2,y2))



    return answer

r = 6
c= 6
queries = [[2,2,5,4],[3,3,6,6],[5,1,6,3]]
print(solution(r,c,queries))