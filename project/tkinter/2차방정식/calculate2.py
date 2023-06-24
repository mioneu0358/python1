# A, B, C를 입력받는다.
# A는 x**2의 값, B는 x, C는 상수를 의미
# 해가 2개,1개,없을수 있으므로 그에 해당하는 인수분해 형태를 return 하는 함수
# solution()을 완성하시오.
# A = 0 => 2차방정식이 아니다 => A는 0이 될 수 없습니다 return
#

import math
def divisor(a):
    b = range(1,a)
    c = []
    for i in b:
        if a % i == 0:
            c.append(i)
    c.append(a)
    return c
def solution(A,B,C):
    if not A or A == '0':
        return "A가 잘못 정의되었습니다"

    A = int(A)
    B = int(B) if B else 0
    C = int(C) if C else 0
    # 해가 2개인 경우 ax² + bx + c = (dx + e) (fx + g)
    if B ** 2 - 4 * A * C > 0:
        divisor_A = divisor(A)
        divisor_C = divisor(C)

        divisor_A += list(map(lambda x: -x, divisor_A))
        divisor_C += list(map(lambda x: -x, divisor_C))
        for d in divisor_A:
            for e in divisor_C:
                f = A / d
                g = C / e
                if d * g + e * f == B:
                    if d > 0 or e > 0:
                        op1 = '+' if e > 0 else '-'
                        op2 = '+' if g > 0 else '-'
                        return f"({int(d)}x {op1} {abs(e)})({int(f)}x {op2} {abs(int(g))})"

        # 결과가 정수형태로 나오지 않을경우 근의 공식을 이용해서 결과값 도출
        x1 = (-B + (B**2 - 4*A*C)**0.5) / (2 * A)
        op1 = '+' if x1 > 0 else '-'
        x2 = (-B- (B**2 - 4*A*C)**0.5) / (2 * A)
        op2 = '+' if x2 > 0 else '-'
        return f"(x {op1} {abs(x1):.4f}) (x {op2} {abs(x2):.4f})"

        # 해가 1개인 경우
    elif B ** 2 - 4 * A * C == 0:
        # 해가 1개인 경우 ax² + bx + c = (dx + e)(dx + e) = (dx + e)²
        d = math.sqrt(A)
        e = math.sqrt(C)
        if e == 0:
            return f"{d}x²"
        op = '+' if B > 0 else '-'
        print(f"({int(d)}x {op} {int(e)})²")
        return f"({int(d)}x {op} {int(e)})²"

        # 해가 없는 경우
    elif B ** 2 - 4 * A * C < 0:
        return "해가 없습니다."

# 0 1 2 => A는 0이 될 수 없습니다.
# 6 23 21 => (2x + 3)(3x + 7)
# 1 12 32 => (1x + 4)(1x + 8)
# 1 4 4 =>  (1x + 2)²
# 1 -4 4 =>  (1x - 2)²
# 1 3 7 => 해가 없습니다.
