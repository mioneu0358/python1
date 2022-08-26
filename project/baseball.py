'''BASEBALL GAME RULE'''

""" 
Rule1: 무작위 정수 3개를 정답으로 선언한다.(단, 중복은 없도록)
Rule2: 매 턴 마다 정수 3개를 입력하고 비교한다.
Rule3: 입력한 수가 존재하며, 자리도 같다면 STRIKE
       존재는 하지만 자리가 다르면 BALL
Rule4: 총 10회 안에 문제를 맞혀야 하며, 턴이 0이 되면 종료
"""


import random

cnt = 10
answer = []
while len(answer) <= 2 :
    num = random.randint(0,9)
    if num not in answer:
        answer.append(num)

ball = 0
strike = 0
while True:
    result = list(map(int,input("숫자 3개를 입력하시오: ").split()))
    print()
    cnt -= 1
    print("남은 기회 %d" % cnt)
    if cnt == 0:
        print("You lose")
        print("정답 : ",answer)
        exit()
    for i in range(len(result)):
        if result[i] in answer:
            ball += 1
            if result[i] == answer[i]:
                ball -= 1
                strike += 1
    if answer == result:
        print("Correct!")
        exit()
    print("Ball: %d, Strike: %d" % (ball,strike))
    ball = 0
    strike = 0

