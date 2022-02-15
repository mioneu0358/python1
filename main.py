# Stack 스택
# 1. 쌓이는 형태의 자료구조(Data structure)
# 2. list로 구현이 되어있다.
# 3. 맨 마지막에 넣은게 먼저 나오고, 처음 넣은게 마지막에 나온다(lifo)


class StackElement():
    #생성자 생성
    def __init__(self,data,next):
        #요소의 값
        self.data = data
        # 다음 요소의 위치
        self.next = next

class Stack:
    def __init__(self):
        self.top = None

    def push(self,data):
         #스텍이 비어있는 경우
         if self.top is None:
             elem = StackElement(data, None)
             self.top = elem
         #스텍이 있는 경우
         else:
            elem = StackElement(data, self.top)
            self.top = elem

    def pop(self):
        if self.top is None:
            return None
        else:
            temp = self.top
            self.top = temp.next
            return temp.data

    def peek(self):
        if self.top is None:
            return None
        else:
            return self.top.data




#프로그래머스 스택관련문제 


# prices = [1, 2, 3, 2, 3]
# answer = [0]
# t_a = []
# for p in list(reversed(prices))[1:]:
#     time = 0
#     while t_a and t_a[-1][0] >= p:
#         #스텍이 비어있지 않고, top의 가격이 현재가 보다 크거나 같으면
#         time += t_a.pop()[1]
#         #스텍에서 시간을 꺼내서
#     t_a.append([p, time +1])
#     # 더해준다
#     answer.append(time +1)
# answer = reversed(answer)
# print(list(answer))



# def solution(prices):
#     # 마지막 price는 항상 0초 이므로 0을 미리 넣음.
#     answer = [0]
#
#     # 가격-시간 스택 선언
#     t_a = []
#
#     # prices의 마지막을 제외한 부분을 역순회함.
#     for p in list(reversed(prices))[1:]:
#
#         # 스택이 비어있지 않고 스택의 TOP의 가격이 현재 가격보다 크거나 같으면
#         # 스택에서 시간을 빼서 더해줌
#         time = 0
#         while t_a and t_a[-1][0] >= p:
#             time += t_a.pop()[1]
#
#         # 스택의 TOP에 현재 가격-시간을 넣어줌
#         t_a.append([p, time + 1])
#         answer.append(time + 1)
#
#     answer.reverse()
#     return answer



