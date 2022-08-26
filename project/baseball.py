import random

cnt = 10  #시도횟수
answer = [] #정답을 받아줄 변수
while len(answer) <= 2 :    #중복되지 않은 3개의 수를 랜덤으로 넣어준다.
    num = random.randint(0,9)
    if num not in answer:
        answer.append(num)  
        
print(answer)

ball = 0    #ball count
strike = 0  #strike cout
while True:
    result = list(map(int,input("숫자 3개를 입력하시오: ").split()))   #수 3개를 입력받는 리스트
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

