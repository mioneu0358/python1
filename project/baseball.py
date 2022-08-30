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

print(answer)
Ball = 0
Strike = 0
while True:
    #TODO: 1. 정수 3개를 입력받는다(띄어쓰기로 구분)
    #      2. 입력받은 정수와 정답을 비교한다.
    #         2-1. 입력받은 정수가 존재하면 Ball을 증가시킨다.
    #         2-2. 자리도 같을 경우 Strike를 증가시키고 Ball을 줄여준다.
    #         2-3. 비교가 끝나면 Ball과 Strike를 출력한다. (단, Ball과 Strike가 0이면 Foul출력)
    #      3. 입력받은 정수와 정답이 같을 경우 이겼다는 문장을 출력 후, 게임 종료
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
            Ball += 1
            if result[i] == answer[i]:
                Ball -= 1
                Strike += 1
    if answer == result:
        print("Correct!")
        exit()
    if Ball == Strike == 0:
        print("Foul!")
    else:
       print("Ball: %d, Strike: %d" % (Ball,Strike))
    Ball = 0
    Strike = 0

