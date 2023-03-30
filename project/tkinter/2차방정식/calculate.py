import math

def solution(A, B, C):
    # a가 0 인 경우
    if A == 0:
        return "A는 0이 될 수 없습니다."

    # 해가 2개인 경우
    if B ** 2 - 4 * A * C > 0:
        for a in range(max(A, 1), min(A, 1) - 1, -1):
            if a == 0: continue
            if A % a == 0:
                c = A // a
                for b in range(max(C, 1), min(C, 1) - 1, -1):
                    if b == 0: continue
                    if C % b == 0:
                        d = C // b
                        if a * d + b * c == B :
                            op1 = '-' if b < 0 else '+'
                            op2 = '-' if d < 0 else '+'
                            return f"({a}x {op1} {abs(b)})({c}x {op2} {abs(d)})"

    # 해가 1개인 경우
    elif B ** 2 - 4 * A * C == 0:
        # x1 = (-B + math.sqrt(B ** 2 - 4 * A * C)) / (2 * A)
        # op1 = '-' if x1 > 0 else '+'
        # if round(x1) == 0:
        #     return f"x²"
        # return f"(x {op1} {abs(round(x1))})² "
        a = math.sqrt(A)
        b = math.sqrt(C)
        if b == 0:
            return f"{a}x²"
        op = '+' if B > 0 else '-'
        return f"({int(a)}x {op} {int(b)})²"


    # 해가 없는 경우
    elif B ** 2 - 4 * A * C < 0:
        return "해가 없습니다."
