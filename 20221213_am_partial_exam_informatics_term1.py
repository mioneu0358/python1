# # Programming assignment 1: Fortuitous numbers (4 points)

# s = input().strip().replace('-',' ').replace(',',' ')
# result = 1
# for i in s.split():
#     print(i,len(i))
#     result *= len(i)
# print(result)



# Programming assignment 2: Luciferase (5 points)

# 생물학에서 서열 모티프(sequence motif)는 많은 다른 단백질에 널리 퍼져 있는 펩타이드(단백질의 일부)를 말합니다. 이 반복적인 특성은 보통 모티프를 포함하는
# 거대 분자의 생물학적 기능과 관련이 있습니다. 모티프를 찾는 일은 작은 변이가 발생하기 때문에 복잡할 수 있으며, 반복이 반드시 동일하지는 않습니다.
# 모티프의 모든 가능한 변형을 나타내기 위해, 단백질 데이터베이스 PROSITE는 대시(-)로 구분된 하나 이상의 단위로 구성된 패턴을 사용합니다.
# 예를 들어, [AC]-x-V-x-{ED}. 각 단위는 모티프의 특정 위치에 어떤 문자가 올 수 있는지를 설명합니다. 단위에 대한 네 가지 다른 표기법이 있습니다:
#
# 대문자 (예: V)는 해당 위치에 이 문자만 올 수 있음을 나타냅니다.
# 소문자 x는 해당 위치에 어떤 문자든 올 수 있음을 나타냅니다.
# 대괄호 안에 하나 이상의 대문자 (예: [AC])는 해당 위치에 이 문자들 중 하나가 와야 함을 나타냅니다.
# 중괄호 안에 하나 이상의 대문자 (예: {ED})는 해당 위치에 이 문자들이 오면 안 됨을 나타냅니다.
# 같은 대문자가 대괄호나 중괄호 사이에 여러 번 올 수 있지만, 이는 패턴을 변경하지 않습니다. 각 단위는 모티프의 단일 위치에 해당하므로, 패턴과 일치하는 모티프의 길이는 항상 패턴의 단위 수와 같습니다.
#
# 예를 들어, 다섯 개의 단위로 이루어진 패턴 [DJINN]-x-V-x-{SATAN}는 첫 번째 문자가 D, I, J, 또는 N이고, 두 번째와 네 번째 문자는 어떤 문자든 될 수 있으며, 세 번째 문자는 V이고, 다섯 번째 문자는 A, N, S, 또는 T가 아닌 다섯 글자 모티프와 일치합니다.
# 예를 들어, 이 패턴은 모티프 DEVIL과 일치합니다.
#

# 당신의 과제:
# 함수 unit을 작성하세요. 이 함수는 문자열 u(str)를 입력으로 받습니다.
# 문자열 u가 단일 단위로 된 패턴을 설명하지 않으면(위의 PROSITE에서 사용된 네 가지 표기법 참조),
# "invalid pattern" 메시지와 함께 AssertionError를 발생시켜야 합니다.
# 그렇지 않으면 함수는 해당 단위 u와 일치하는 모든 대문자 알파벳을 알파벳 순서대로 나열한 문자열(str)을 반환해야 합니다. 중복된 문자는 없어야 합니다.
def unit(U: str):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if U[0] == '[' and U[-1] == ']':
        # print(3,U)
        result = ""
        for i in U[1:-1]:
            if i not in result:
                result += i
        return result
    elif U[0] == '{' and U[-1] == '}':
        # print(4,U)
        result = ""
        for a in alphabet:
            if a not in U:
                result += a
        return result
    elif len(U) == 1 and U.isupper():
        # print(1,U)
        return U
    elif len(U) == 1 and  U.islower():
        # print(2,U)
        return alphabet

    else:
        raise AssertionError('Invalid pattern')

# 함수 expand를 작성하세요. 이 함수는 패턴 p(str)를 입력으로 받습니다. 함수는 패턴 p의 각 단위에 대해 해당 단위와 일치하는
# 모든 대문자 알파벳을 알파벳 순서대로 나열한 문자열(str)을 포함하는 리스트(list)를 반환해야 합니다. 중복된 문자는 없어야 합니다.
def expand(p: str):
    parts = p.split('-')
    result = []
    for part in parts:
        result.append(unit(part))
    return result


# 함수 ismotif을 작성하세요. 이 함수는 두 개의 인수를 입력으로 받습니다: ① 패턴 p(str) ② 문자열 m(str). 함수는 문자열 m이 패턴 p와 일치하는지를 나타내는 부울 값(bool)을 반환해야 합니다.
# 패턴 매칭은 문자열 m의 대문자와 소문자를 구분하지 않아야 합니다. 또한 문자열의 길이가 패턴의 단위 수와 다르면, 그 문자열은 패턴과 일치하지 않습니다.
def ismotif(p: str, m: str):
    if len(m) != len(p.split('-')): return False

    answer = expand(p)
    for i in range(len(m)):
        if m[i] not in answer[i]:
            return False
    return True


# 함수 motifs를 작성하세요. 이 함수는 두 개의 인수를 입력으로 받습니다: ① 패턴 p(str) ② 문자열 s(str).
# 함수는 문자열 s에서 패턴 p와 일치하는 모든 모티프를 포함하는 집합(set)을 반환해야 합니다.
# 집합 내에서 각 모티프는 두 요소로 구성된 튜플(tuple)로 표현됩니다:
# ① 문자열 s에서 모티프의 첫 번째 문자의 위치(int) ② 모티프의 문자를 포함하는 문자열(str).
# 패턴 매칭은 주어진 문자열 s의 대문자와 소문자를 구분하지 않아야 합니다. 문자열의 문자의 위치는 왼쪽에서 오른쪽으로 0부터 번호가 매겨집니다.
def motifs(p: str, s: str):
    l = len(p.split('-'))
    result = set()
    for i in range(0,len(s)-l):
        print(s[i:i+l])
        if ismotif(p,s[i:i+l].upper()):
            result.add((i,s[i:i+l]))

    return result


if __name__ == "__main__":
    # print(unit('V'))      #  'V'
    # print(unit('x'))       #  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # print(unit('[DJINN]')) #  'DIJN'
    # print(unit('{SATAN}')) #  'BCDEFGHIJKLMOPQRUVWXYZ'
    # print(unit('abc'))     #   Traceback(most recent call last): AssertionError: invalid pattern

    # print(expand('[DJINN]-x-V-x-{SATAN}')) # ['DIJN', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'V', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'BCDEFGHIJKLMOPQRUVWXYZ']
    # print(ismotif('[DJINN]-x-V-x-{SATAN}', 'DEVIL')) #  True
    # print(ismotif('[DJINN]-x-V-x-{SATAN}', 'dive'))  # False
    # print(ismotif('[DJINN]-x-V-x-{SATAN}', 'SATAN')) # False

    # print(motifs('[DJINN]-x-V-x-{SATAN}', 'GNFLEKVRMYPKLVDEVILFLHQDFPSDHMYAKVSATPVPKTPPVPWLLGTSNKSAKLAI')) #    {(14, 'DEVIL')}
    # print(motifs('[DIL]-x-{AEIOU}-[AEIOU]-x-x-[ORS]', 'fanhymkkcllnpwsdetailslmmipiedqcwwffvluciferrhaqcnhgqdyytspmhinfernodkwcfiyveagp'))
    # {(15, 'details'), (37, 'lucifer'), (61, 'inferno')}


# Programming assignment 3: A box code (6 points)

def read_box_code(param:tuple):
    # 입력: 문자열 튜플, 각 문자열은 0부터 9까지의 숫자가 각각 어떻게 표현될 수 있는지를 문서화합니다.
    # 출력: 숫자 (str)를 해당 숫자의 모든 형태 (str)가 포함된 알파벳 순서의 집합(set)으로 매핑하는 딕셔너리(dict)입니다. 이 딕셔너리는 상자 코드(box code)의 표현이라고 합니다.
    result = {}
    for p in param:
        key,val = p.split()
        if key in result:
            result[key].add(val)
        else:
            result[key] = {val}
    return result
def letter2code(l:str,B:dict):
    # 입력: 문자 l (str)과 상자 코드 B (딕셔너리).
    # 출력: 상자 코드 B에 따라 문자 l을 인코딩한 결과 (str)를 반환합니다. 각 숫자는 가능한 모든 형태 중 하나로 무작위로 선택되어야 합니다.
    pass
def code2letter():
    #     입력: 인코딩된 문자 l (str)과 인코딩에 사용된 상자 코드 B (딕셔너리).
    # 출력: 숫자가 가능한 모든 형태 중 하나로 표현되며, 형태의 세그먼트는 임의의 순서로 나열될 수 있습니다. 원래의 문자 (str; 대문자)를 반환합니다.
    pass
# def encode(message, box_code):
#     #     입력: 메시지 (str)와 상자 코드 B (딕셔너리 표현).
#     # 출력: 메시지의 각 숫자를 가능한 모든 형태 중 하나로 인코딩한 결과 (str)를 반환합니다. 메시지에 포함된 문자만 인코딩해야 합니다.
#     pass
import random
def encode(message, box_code):
    pass

def decode():
    #     입력: 인코딩된 메시지 (str)와 해당 인코딩에 사용된 상자 코드 B (딕셔너리).
    # 출력: 숫자가 가능한 모든 형태 중 하나로 표현되며, 형태의 세그먼트는 임의의 순서로 나열될 수 있습니다. 원래의 메시지 문자열 (str; 대문자)을 반환합니다.
    pass

code = ('0 hde', '1 b', '1 d', '2 fcah', '3 gfac', '4 bgf', '5 eah', '6 ghfc', '6 chgb', '7 afh', '7 ab', '8 fhcaeg', '9 eafh', '9 ebfa')

box_code = read_box_code(code)
# print(box_code)
# # {'0': {'hde'}, '1': {'d', 'b'}, '2': {'fcah'}, '3': {'gfac'}, '4': {'bgf'},
# # '5': {'eah'}, '6': {'ghfc', 'chgb'}, '7': {'ab', 'afh'}, '8': {'fhcaeg'}, '9': {'ebfa', 'eafh'}}
# print(box_code['1'])


print(encode('And now for something completely different!', box_code))
# 'b b-bgf fbg d-bfg b-hae afhc-fagc bhgc b-eha b-hfceag d-feha d-hae b-agfc hae afh
#  c-edh ghecfa fahe d-fgb ab gcaf b-aeh d-gfca d-gcbh d-chfa eah cahf-hed eah d-acfh
#  hfac-hea fbg fbea ghcb chgb eha b-cahfeg hae b-bgf hcfa-hed'



# # 1줄로 만들기, 반전, 5개씩 끊어읽기
#
# s = int(input())
# t = int(input())
# string = ""
# for _ in range(t):
#     string += input().strip()
# string = string[::-1]
# print(string)
# for i in range(s):
#     for j in range(i,len(string),s):
#         print(string[j],end = '')
