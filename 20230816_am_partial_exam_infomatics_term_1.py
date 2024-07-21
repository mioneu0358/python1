# # Programming assignment 1: Letters and numbers (4 points) ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# #
# # ONE + TWO - THREE - FOUR + FIVE = 1
# # 위 방정식은 각 단어를 해당하는 숫자나 그 단어의 글자 수로 대체해도 성립합니다. 어떤 방식으로 해도 결과는 1입니다. 또 다른 예는 다음과 같습니다:
# # ONE + TWO - THREE - FOUR + FIVE - SIX + SEVEN + EIGHT + NINE - TEN + ELEVEN + TWELVE - THIRTEEN - FOURTEEN = 5
# # 입력
# # 영어 숫자 이름(대문자)으로 구성된 식으로, 각 이름은 더하기 기호(+) 또는 빼기 기호(-)로 구분됩니다. 더하기와 빼기 기호 전후에는 공백이 있을 수 있습니다.
# # 출력
# # 각 이름을 그 이름의 글자 수로 대체한 후 식을 평가한 결과를 출력합니다.
# #
# # 팁
# # 이 결과를 계산하는 또 다른 방법은 더해야 하는 이름의 각 글자를 +1로, 빼야 하는 이름의 각 글자를 -1로 세는 것입니다.
# #
# # 예제
# # 입력:
# # ONE + TWO - THREE - FOUR + FIVE
# # 출력:
# # 1
# #
# # 입력:
# # ONE+TWO-THREE-FOUR+FIVE-SIX+SEVEN+EIGHT+NINE-TEN+ELEVEN+TWELVE-THIRTEEN-FOURTEEN
# # 출력:
# # 5

#
# exp = input().replace(' ','')
# sign = 1
# result = 0
# for i in exp:
#     if i == '+':
#         sign = 1
#     elif i == '-':
#         sign = -1
#     else:
#         result += sign
# print(result)

# Programming assignment 2: Fifty fifty (5 points)----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 많은 비정상적이고 모순된 문법 규칙들로 인해, 영어는 많은 복잡한 요소를 가지고 있습니다. 그러나 동일한 현상이 많은 영어 사전에 있는 단어들에게도 적용됩니다.
# 단어 "cabbageheaded"는 알파벳의 첫 절반(a–m)으로만 구성된 가장 긴 단어입니다. 단어 "nontortuous"는 알파벳의 두 번째 절반(n–z)으로만 구성된 가장 긴 단어입니다.

# 우리는 또한 알파벳의 첫 절반과 두 번째 절반의 문자들이 교대로 나오는 단어들을 찾을 수 있습니다. 첫 절반의 알파벳 문자로 시작하는 가장 긴 교대 단어들은 12글자입니다.
# 예로는 "comparatives"와 "itinerariums"가 있습니다. 두 번째 절반의 알파벳 문자로 시작하는 가장 긴 교대 단어들은 13글자입니다.
# 예로는 "paranephritis"와 "phraseography"가 있습니다.

# 과제
# 단어는 오직 대문자와 소문자로만 구성됩니다. 당신의 과제는 다음과 같습니다:
alphabet = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def position(c):
    return alphabet.find(c.upper())
# first_position 함수: 단어(str)를 입력으로 받아야 합니다. 이 함수는 단어에서 알파벳 순서상 첫 번째 문자의 위치(int; A=1, B=2, C=3, …, Z=26)를 반환해야 합니다.
def first_position(string):
    arr = []
    for i in string:
        arr.append(position(i))
    return min(arr)
# last_position 함수: 단어(str)를 입력으로 받아야 합니다. 이 함수는 단어에서 알파벳 순서상 마지막 문자의 위치(int; A=1, B=2, C=3, …, Z=26)를 반환해야 합니다.
def last_position(string):
    arr = []
    for i in string:
        arr.append(position(i))
    return max(arr)
# isfirst 함수: 단어(str)를 입력으로 받아야 합니다. 이 함수는 단어가 알파벳의 첫 절반(a–m)으로만 구성되어 있는지를 나타내는 부울 값(bool)을 반환해야 합니다.
def isfirst(string):
    for c in string:
        idx = position(c)
        if idx >= 14: return False
    return True
# issecond 함수: 단어(str)를 입력으로 받아야 합니다. 이 함수는 단어가 알파벳의 두 번째 절반(n–z)으로만 구성되어 있는지를 나타내는 부울 값(bool)을 반환해야 합니다.
def issecond(string):
    for c in string:
        idx = position(c)
        if idx < 14: return False
    return True
# isalternate 함수: 단어(str)를 입력으로 받아야 합니다. 이 함수는 단어가 알파벳의 첫 절반(a–m)과 두 번째 절반(n–z)의 문자들이 교대로 나오는지를 나타내는 부울 값(bool)을 반환해야 합니다.
# 이 함수들 중 어떤 것도 대문자와 소문자를 구분해서는 안 됩니다.
def isalternate(string):
    for i in range(len(string)-1):
        a = isfirst(string[i])
        b = issecond((string[i+1]))
        if a != b: return False
    return True
if __name__ == "__main__":
    # print(position('G'))
    # 7
    # print(position('v'))
    # 22
    #
    # print(first_position('FIDDLEDEEDEE'))
    # 4
    # print(first_position('soupspoons'))
    # 14
    # print(first_position('CoMpArAtIvEs'))
    # 1
    # print(first_position('pArAnEpHrItIs'))
    # 1
    #
    # print(last_position('FIDDLEDEEDEE'))
    # 12
    # print(last_position('soupspoons'))
    # 21
    # print(last_position('CoMpArAtIvEs'))
    # 22
    # print(last_position('pArAnEpHrItIs'))
    # 20
    #
    # print(isfirst('FIDDLEDEEDEE'))
    # True
    # print(isfirst('soupspoons'))
    # False
    # print(isfirst('CoMpArAtIvEs'))
    # False
    # print(isfirst('pArAnEpHrItIs'))
    # False

    # print(issecond('FIDDLEDEEDEE'))
    # False
    # print(issecond('soupspoons'))
    # True
    # print(issecond('CoMpArAtIvEs'))
    # False
    # print(issecond('pArAnEpHrItIs'))
    # False

    print(isalternate('FIDDLEDEEDEE'))
    False
    print(isalternate('soupspoons'))
    False
    print(isalternate('CoMpArAtIvEs'))
    True
    print(isalternate('pArAnEpHrItIs'))
    True



# 다음 정보를 포함하는 일곱 줄이 있으며, 이는 엘리베이터의 궤적을 시뮬레이션하는 데 사용됩니다:
#
# 시뮬레이션할 단계 수 (steps); 엘리베이터가 방문하는 각 층은 시뮬레이션의 단일 단계에 포함됩니다.
# 시뮬레이션이 시작되는 층의 번호 (start_floor); 로비는 번호 0으로 지정됩니다.
# 최고층에 지정된 번호 (top_floor).
# 엘리베이터가 시뮬레이션 시작 시 올라가는지 내려가는지를 나타내는 문자; 캐럿(caret; ^)은 엘리베이터가 처음에 올라가는 것을 나타내고,
# 문자 v는 엘리베이터가 처음에 내려가는 것을 나타냅니다.
# 시뮬레이션 시작 시의 24시간제 시간 (start_hour); 예를 들어, 시뮬레이션이 23:14에 시작되면 23.
# 시뮬레이션 시작 시의 24시간제 분 (start_minute); 예를 들어, 시뮬레이션이 23:14에 시작되면 14.
# 시뮬레이션의 출력 세부 수준을 나타내는 텍스트; 텍스트 verbose는 시뮬레이션의 각 단계 동안 출력이 생성되어야 함을 나타내고,
# 텍스트 quiet는 엘리베이터가 start_floor를 방문할 때만 출력이 생성되어야 함을 나타냅니다.

# 출력
# 엘리베이터는 start_floor에서 시작하여 주어진 방향으로 이동합니다. 도착 일정에 포함되어야 하는 각 층에 대해, 현재 시간,
# 엘리베이터가 방문한 층 번호, 엘리베이터가 현재 층을 떠나는 방향(^는 계속 올라가는 경우, v는 계속 내려가는 경우)을 포함하는 줄이 출력되어야 합니다.
# 마지막 입력 줄이 텍스트 verbose를 포함하면, 시뮬레이션 동안 엘리베이터가 방문한 모든 층이 도착 일정에 포함되어야 합니다.
# 마지막 입력 줄이 텍스트 quiet를 포함하면, 시뮬레이션 시작 시 엘리베이터가 방문한 층만 도착 일정에 포함되어야 합니다.
#
steps = int(input())
floor = int(input())
top_floor = int(input())
up_down = input()
hour = int(input())
minute = int(input())
text = input()


_next = 1
if up_down == 'v': _next = -1
for _ in range(steps):
    if _next < 0: up_down = 'v'
    else:         up_down = '^'
    if text == 'quiet' :
        pass
    else:
        print(f"{hour:02d}:{minute:02d} {floor} [{up_down}]")
    minute += 1
    if minute >= 60:
        minute = 0
        hour += 1
        if hour == 24:
            hour = 0
    floor += _next
    if floor in [top_floor, 0]: _next *= -1



#
#
# # 입력
# # steps = 30
# # floor = 6
# # top_floor = 8
# # up_down = '^'
# # hour = 23
# # minute = 50
# # text = verbose
#
# # 출력
# # 23:50 6 [^]
# # 23:51 7 [^]
# # 23:52 8 [v]
# # 23:53 7 [v]
# # 23:54 6 [v]
# # 23:55 5 [v]
# # 23:56 4 [v]
# # 23:57 3 [v]
# # 23:58 2 [v]
# # 23:59 1 [v]
# # 00:00 0 [^]
# # 00:01 1 [^]
# # 00:02 2 [^]
# # 00:03 3 [^]
# # 00:04 4 [^]
# # 00:05 5 [^]
# # 00:06 6 [^]
# # 00:07 7 [^]
# # 00:08 8 [v]
# # 00:09 7 [v]
# # 00:10 6 [v]
# # 00:11 5 [v]
# # 00:12 4 [v]
# # 00:13 3 [v]
# # 00:14 2 [v]
# # 00:15 1 [v]
# # 00:16 0 [^]
# # 00:17 1 [^]
# # 00:18 2 [^]
# # 00:19 3 [^]





