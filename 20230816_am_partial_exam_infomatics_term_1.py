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


# Programming assignment 3: Three test tubes (6 points)  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 프로그램 과제 3: 세 개의 시험관 (6점)
# 세 개의 시험관이 있으며, 최대 용량은 각각 3, 5, 8 단위입니다. 첫 두 개의 시험관은 비어 있고, 세 번째 시험관은 액체로 가득 차 있습니다.
# 시험관에는 눈금이 없으므로 시험관을 완전히 채우지 않는 액체의 양을 정확히 측정하는 것은 불가능합니다. 소스 시험관에서 목적지 시험관으로 액체를 부을 때 소스가 비거나
# 목적지가 가득 찰 때까지 멈추지 않는 단일 단계의 부음을 통해 4 단위의 액체를 정확하게 측정하는 데 필요한 단계를 찾는 것이 목표입니다. 액체가 흘러내리지 않아야 합니다.
#
# 다음 다이어그램은 6단계에서 4단위의 액체를 정확히 측정하는 방법을 보여줍니다. 이는 이 작업을 수행할 수 있는 최소 단계 수입니다. 그러나 6단계에서 4단위의 액체를 측정할 수 있는 다른 가능성도 있습니다.
# 각 단계에서 각 시험관이 정수 단위의 액체를 포함하고 있음을 보여주기 위해 마킹을 제공했습니다. 각 단계에서 얇은 녹색 화살표는 소스에서 목적지로 향합니다.
#
# 과제 설명
# 이 퍼즐은 𝑛 ∈ ℕ0 개의 시험관으로 일반화할 수 있으며, 0부터 시작하여 왼쪽에서 오른쪽으로 번호를 매깁니다. 시험관의 용량은 튜플 (𝑐0, 𝑐1, ..., 𝑐𝑛−1)로 설명되며,
# 여기서 시험관 𝑖는 최대 𝑐𝑖 ∈ ℕ0 (정수) 단위의 액체를 포함할 수 있습니다 (0 ≤ 𝑖 < 𝑛). 시험관의 상태는 튜플 (𝑣0, 𝑣1, ..., 𝑣𝑛−1)로 설명되며,
# 여기서 시험관 𝑖는 현재 𝑣𝑖 ∈ ℕ (정수; 0 ≤ 𝑣𝑖 < 𝑐𝑖) 단위의 액체를 포함하고 있습니다 (0 ≤ 𝑖 < 𝑛). 따라서 용량은 모든 시험관이 가득 찬 상태로 설명됩니다.
# 서두의 퍼즐에서 세 개의 시험관은 용량 (3, 5, 8)을 가지고 있으며 초기 상태는 (0, 0, 8)입니다.
#
# 해결책이 존재하는 경우 일반화된 퍼즐에 대한 표준 절차가 있습니다. 이 절차는 처리되지 않은 상태를 추적하기 위해 큐 𝑸를 사용하고, 큐 𝑸에 한 번이라도 추가된 모든 상태의 이전 상태를 기억합니다.
# 큐 𝑸는 처음에는 초기 상태만 포함하는 리스트입니다. 딕셔너리 𝑃는 상태를 이전 상태에 매핑하여 이전 상태를 추적하는 데 사용됩니다.
# 초기에는 딕셔너리 𝑃가 초기 상태를 값 None에 매핑하여 초기 상태에 이전 상태가 없음을 나타냅니다.
#
# 절차의 각 단계는 큐 𝑸의 시작 부분에서 상태 𝑝를 처리합니다. 먼저 큐 𝑸의 시작 부분에서 상태 𝑝가 제거됩니다. 그런 다음 상태 𝑝를 따를 수 있는 모든 가능한 상태가 결정됩니다.
# 이러한 후속 상태는 시험관 𝑥(소스)에서 시험관 𝑦(목적지)로 액체를 부어 얻습니다.
# 이는 𝑖) 소스 𝑥와 목적지 𝑦가 다른 시험관인 경우, 𝑖𝑖) 소스 𝑥가 비어 있지 않은 경우, 𝑖𝑖𝑖) 목적지 𝑦가 가득 차 있지 않은 경우에만 가능합니다.
# 아래 그림은 서두의 퍼즐의 초기 상태 (0, 0, 8)가 상태 (0, 5, 3) 및 (3, 0, 5)로 이어질 수 있음을 보여줍니다.
# 왼쪽에서는 얇은 녹색 선이 상태 (0, 0, 8)에서 시험관 2에서 시험관 1로 액체를 부어 상태 (0, 5, 3)로 이어짐을 나타냅니다.
# 오른쪽에서는 얇은 녹색 선이 상태 (0, 0, 8)에서 시험관 2에서 시험관 0으로 액체를 부어 상태 (3, 0, 5)로 이어짐을 나타냅니다. 상태 (0, 0, 8)에서 소스와 목적지의 다른 조합에서는 액체를 부을 수 없습니다.
#
# 마지막으로 상태 𝑝를 따를 수 있는 모든 상태가 증가하는 순서로 처리됩니다: 이 순서는 먼저 위치 0에서 시험관의 액체 양을 비교하고, 위치 𝑥의 시험관이 동일한 액체 양을 포함하고 있는 동안
# 위치 𝑥 + 1에서 시험관의 액체 양을 비교하여 결정됩니다. 이전에 큐 𝑸에 추가된 적이 없는 후속 상태 𝑠에 대해서는 상태 𝑠를 큐의 끝에 추가하고, 상태 𝑠가 상태 𝑝를 따름을 딕셔너리 𝑃에서 상태 𝑠를 𝑝에 매핑하여 기억합니다.
#
# 아래는 서두의 퍼즐에서 시험관에 대한 표준 절차의 진행 상황을 보여줍니다. 초기 상태 (0, 0, 8)는 트리 구조의 맨 위에 있습니다. 화살표는 각 상태를 가능한 모든 후속 상태와 연결합니다.
# 이러한 화살표는 딕셔너리 𝑃에 기록됩니다. 상태가 큐 𝑸에 추가되고 제거되는 순서는 트리 구조의 파란색 상태를 왼쪽에서 오른쪽, 위에서 아래로 읽는 일반적인 읽기 순서에 따라 얻어집니다.
# 더 이상 처리되지 않는 후속 상태는 트리 구조에서 주황색으로 표시됩니다.
#
# 서두의 퍼즐에 대한 시험관에 대한 표준 절차가 거치는 연속적인 단계에 대한 표는 다음을 포함합니다: 𝑖) 큐의 시작 부분에서 처리되는 상태, 𝑖𝑖) 그 후속 상태, 𝑖𝑖𝑖) 큐에서 수행되는 작업.
# 다음 상태는 이전 단계에서 큐에 추가된 경우 더 이상 처리할 필요가 없으므로 주황색으로 표시됩니다. 큐의 시작 부분에서 삭제된 상태는 빨간색으로 교차하여 색칠됩니다. 큐의 끝에 추가된 상태는 초록색으로 색칠됩니다.
#
# 과제:
# 절차가 멈추는 두 가지 경우가 있습니다. 큐 𝑄가 더 이상 어떤 상태도 포함하지 않는 경우, 절차는 다음 단계를 수행할 수 없으며 요청된 액체의 양을 시험관으로 정확하게 측정할 수 없음을 의미합니다.
# 큐 𝑄의 시작 부분에 있는 상태 𝑝가 요청된 양의 액체를 포함하는 시험관을 가지고 있는 경우, 우리는 딕셔너리 𝑃를 사용하여 초기 상태에서 상태 𝑝까지의 경로를 (거꾸로) 재구성할 수 있습니다.
# 이 경로는 가능한 최소한의 부음을 통해 요청된 양의 액체를 측정하는 방법을 설명하며, 따라서 퍼즐에 대한 해결책입니다.
#
# 서두의 퍼즐에서, 위의 그림은 (3,4,1) 상태가 큐의 시작 부분에 나타나는 첫 번째 상태로, 4 단위의 액체를 포함한 시험관이 있음을 보여줍니다.
# 파란색 화살표는 초기 상태 (0,0,8)에서 상태 (3,4,1)로 가는 경로를 나타내며, 이는 표준 절차에 의해 발견된 퍼즐 해결책을 설명합니다:
# (0, 0,8) → (0,5,3) → (3,2,3) → (0,2,6) → (2,0,6) → (2,5,1) → (3,4,1)
# 이것들은 표준 절차를 수행하면서 큐의 시작 부분에 (3,4,1) 상태가 나타날 때의 딕셔너리 𝑃의 내용입니다. 파란색 화살표는 상태 (3,4,1)에서 시작하여 반복적으로 이전 상태를 조회하여
# 초기 상태로 돌아가는 방법을 나타냅니다. 초기 상태는 더 이상 이전 상태가 없습니다 (빨간색 원).
#
# 여러분의 작업:
# 함수 작성: pour 함수는 네 개의 인수를 입력으로 받습니다: 𝑖) 시험관의 상태 𝑝, 𝑖𝑖) 시험관의 용량 𝑐, 𝑖𝑖𝑖) 소스 시험관 번호 𝑥, 𝑖𝑣) 목적지 시험관 번호 𝑦.
# 상태 𝑝에서 소스 𝑥에서 목적지 𝑦로 액체를 붓는 것이 불가능한 경우, None 값을 반환해야 합니다. 그렇지 않은 경우, 소스 𝑥에서 목적지 𝑦로 액체를 부은 후의 시험관 상태를 반환해야 합니다.
# 부음은 소스가 비거나 목적지가 가득 찰 때 중 하나가 먼저 발생할 때까지 멈춥니다.
# 힌트: 액체를 한 시험관에서 다른 시험관으로 붓는 것은 세 가지 조건이 충족될 때만 가능합니다. 이는 표준 절차의 설명에서 설명됩니다.
def pour(state, capacities, x, y):
    # 𝑖) 소스 𝑥와 목적지 𝑦가 다른 시험관인 경우, 𝑖𝑖) 소스 𝑥가 비어 있지 않은 경우, 𝑖𝑖𝑖) 목적지 𝑦가 가득 차 있지 않은 경우에만 가능합니다.
    if x == y or state[x] == 0 or state[y] == capacities[y]:
        return None
    new_state = list(state)
    new_capacities = list(capacities)
    while new_state[y] != new_capacities[y]:
        if not new_state[x]: break
        new_state[y] += 1
        new_state[x] -= 1
    return tuple(new_state)


# 함수 작성: next_states 함수는 시험관의 상태 𝑝와 시험관의 용량 𝑐을 입력으로 받습니다.
# 이 함수는 한 시험관에서 다른 시험관으로 액체를 부은 후 따라올 수 있는 모든 상태를 포함하는 집합을 반환해야 합니다.
def next_states(state, capacities):
    result = set()
    for x in range(len(state)):
        for y in range(len(state)):
            po = pour(state,capacities,x,y)
            if po:
                result.add(po)
    return result



def step(Queue, Predecessors, capacities):
    # 함수 작성: step 함수는 세 개의 인수를 입력으로 받습니다: 𝑖) 큐 𝑄(리스트), 𝑖𝑖) 선행자를 포함하는 딕셔너리 𝑃(dict), 𝑖𝑖𝑖) 시험관의 용량 𝑐. 큐 𝑄와 딕셔너리 𝑃의 내용은
    # 시험관 퍼즐을 해결하기 위해 표준 절차를 적용하는 동안의 한 시점을 나타냅니다. 함수는 큐 𝑄가 비어 있지 않다고 가정할 수 있으며 이를 명시적으로 확인할 필요는 없습니다.
    # 이 함수는 표준 절차의 단일 단계를 수행해야 하며, 큐 𝑄의 시작 부분에서 상태 𝑝를 삭제하고, 절차에 따라 상태 𝑝를 따를 수 있는 모든 상태를 처리해야 합니다.
    # 단계를 수행할 때 큐 𝑄와 딕셔너리 𝑃는 필요에 따라 업데이트되어야 합니다. 이 함수는 명시적으로 값을 반환해서는 안 됩니다 (읽기: 함수는 None 값을 반환해야 합니다).
    # 힌트: 큐 𝑄와 딕셔너리 𝑃 모두 이미 방문한 상태에 대한 정보를 포함하고 있습니다.
    curr_state = Queue.pop(0)
    next_p = next_states(curr_state,capacities)
    for np in next_p:
        if np not in Predecessors:
            Queue.append(np)
            Predecessors[np] = curr_state



def path(state, Predecessors):
    # 함수 작성: path 함수는 시험관의 상태 𝑝와 선행자가 포함된 딕셔너리 𝑃(dict)를 입력으로 받습니다.
    # 딕셔너리 𝑃는 시험관 퍼즐을 해결하기 위해 표준 절차를 적용하는 동안의 한 시점에서 선행자를 설명하며,
    # 그 순간에 상태 𝑝는 이전에 큐에 추가되었습니다. 이 함수는 초기 상태에서 상태 𝑝까지의 경로를 설명하는 상태 목록을 반환해야 합니다. 함수는 딕셔너리 𝑃를 수정해서는 안 됩니다.
    curr = state
    path_list = []
    while curr:
        path_list.append(curr)
        curr = Predecessors[curr]
    return list(reversed(path_list))

def solution(state, capacities, taget):
    # 함수 작성: solution 함수는 시험관 퍼즐의 일반화된 버전을 설명하는 세 개의 인수를 입력으로 받습니다:
    # 𝑖) 시험관의 초기 상태 𝑝, 𝑖𝑖) 시험관의 용량 𝑐, 𝑖𝑖𝑖) 요청된 액체의 양 𝑣∈ℕ0 (정수).
    # 퍼즐에 해결책이 없는 경우 None 값을 반환해야 합니다. 그렇지 않으면, 표준 절차에서 얻은 해결책을 연속적인 상태의 최단 경로 목록으로 반환해야 합니다.
    # 위의 모든 함수는 유효한 인수만 전달된다고 가정할 수 있으며 이를 명시적으로 확인할 필요는 없습니다.
    Queue = [state]
    Predecessors = {state: None}

    while Queue:
        curr_state = Queue[0]
        if taget in curr_state:
            return path(curr_state, Predecessors)
        step(Queue, Predecessors, capacities)

    return None

if __name__ == "__main__":
    # print(pour((0, 2, 6), (3, 5, 8), 2, 0))
    # (3, 2, 3)
    # print(pour((0, 2, 6), (3, 5, 8), 2, 1))
    # (0, 5, 3)
    # print(pour((3, 2, 3), (3, 5, 8), 1, 0))
    # print(pour((3, 2, 3), (3, 5, 8), 2, 2))
    #
    # print(next_states((0, 0, 8), (3, 5, 8)))
    # {(0, 5, 3), (3, 0, 5)}
    # print(next_states((0, 5, 3), (3, 5, 8)))
    # {(3, 2, 3), (0, 0, 8), (3, 5, 0)}
    # print(next_states((3, 0, 5), (3, 5, 8)))
    # {(0, 3, 5), (0, 0, 8), (3, 5, 0)}
    # print()
    #
    # queue = [(0, 0, 8)]
    # predecessor = {(0, 0, 8): None}
    #
    # print("step(queue, predecessor, (3, 5, 8))")
    # step(queue, predecessor, (3, 5, 8))
    # print(queue)
    # [(0, 5, 3), (3, 0, 5)]
    # print(predecessor)
    # {(0, 0, 8): None, (0, 5, 3): (0, 0, 8), (3, 0, 5): (0, 0, 8)}
    # print()
    #
    # print("step(queue, predecessor, (3, 5, 8))")
    # step(queue, predecessor, (3, 5, 8))
    # print(queue)
    # [(3, 0, 5), (3, 2, 3), (3, 5, 0)]
    # print(predecessor)
    # {(0, 0, 8): None, (0, 5, 3): (0, 0, 8), (3, 0, 5): (0, 0, 8), (3, 2, 3): (0, 5, 3), (3, 5, 0): (0, 5, 3)}
    # print()
    #
    # print("path((3, 5, 0), predecessor)")
    # print(path((3, 5, 0), predecessor))
    # [(0, 0, 8), (0, 5, 3), (3, 5, 0)]
    # print()

    print("solution((0, 0, 8), (3, 5, 8), 4))")
    print(solution((0, 0, 8), (3, 5, 8), 4))
    [(0, 0, 8), (0, 5, 3), (3, 2, 3), (0, 2, 6), (2, 0, 6), (2, 5, 1), (3, 4, 1)]
    print()

    print("solution((0, 5, 0, 17), (3, 5, 11, 17), 7)")
    print(solution((0, 5, 0, 17), (3, 5, 11, 17), 7))
    [(0, 5, 0, 17), (0, 0, 5, 17), (0, 5, 5, 12), (0, 0, 10, 12), (0, 5, 10, 7)]
    print()

    print("solution((0, 0, 0, 0, 13), (5, 7, 7, 11, 13), 12)")
    print(solution((0, 0, 0, 0, 13), (5, 7, 7, 11, 13), 12))
    [(0, 0, 0, 0, 13), (0, 0, 0, 11, 2), (5, 0, 0, 6, 2), (0, 0, 0, 6, 7), (5, 0, 0, 1, 7), (0, 0, 0, 1, 12)]



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





