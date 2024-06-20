# Programming assignment 1: The Feynman ciphers (4 points)------------------------------------------------------------------------------------------------------------------------------------

s = int(input())    # 입력받은 문자열을 끊어 읽을 수
t = int(input())    # 입력받은 문자열의 수

sentence = ''
for _ in range(t):
    sentence += input()

sentence = sentence[::-1]

for i in range(s):
    for j in range(i,len(sentence),s):
        print(sentence[j],end = '')

# THEREISNOAUTHORITYWHODECIDESWHATISAGOODIDEA

# Programming assignment 2: Platypus (5 points)------------------------------------------------------------------------------------------------------------------------------------
