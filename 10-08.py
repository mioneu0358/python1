# 십진수 소수 -> 이진수 소수
# 정수부는 십진수를 이진수로 바꾸는 형태 그대로 사용
# 실수부는 2로 곱한뒤 나온 정수부를 이어 붙힌다.


# 이진수 소수 -> 십진수 소수
# a  = '011'
#
# def make_decimal(a):
#     answer = 0
#     for i in range(len(a)):
#         answer += int(a[i]) / (2 **(i+1))
#     return answer
# print(make_decimal(a))


# def make_binary_decimal(decimal):
#     divisior = 10 ** len(str(decimal))
#     binary = ""
#
#
#     while decimal > 0 and len(binary) < 23:
#         decimal *= 2
#         binary += str(decimal // divisior)
#         decimal %= divisior
#     return binary
# print(make_binary_decimal(int(input())))


# 컴퓨터의 실수 표현
# 1. 고정 소수점(fixed point)
# 2. 지수 표기법
# 부호 S, 지수E, 가수M, 실수 V
# V = -1**S * M * 2**E


print(0.1 +0.2 == 0.3)