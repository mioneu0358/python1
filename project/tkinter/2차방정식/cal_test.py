def solution(a,b,c):
    """
    이차방정식 해 구하기
    판별식 D: b **  2 - (4 * a * c)
    판별식 D > 0: 서로 다른 두개의 실근  =>  ax**2 + bx + c = (dx+e)(fx+g)이며,  a = d*f, c = e*g이며 d*g+e*f = b를 만족하게 된다.
          D = 0: 하나의 해, 즉 중근이 존재  =>  a**2 + bx + c == (dx+e)(dx+e)이며, a = d**2, c = e**2를 만족하게 된다.
          D < 0: 서로 다른 두개의 허근, => 해가 없다로 판별
    """
    D = b ** 2 - (4 * a * c)
    if D > 0:
        divisor_a = [i for i in range(1,a+1) if a % i == 0]
        divisor_c = [i for i in range(1,c+1) if c % i == 0]
        for d in range(len(divisor_a)):
            divisor_a.append(-divisor_a[d])
        for d in range(len(divisor_c)):
            divisor_c.append(-divisor_c[d])

        for d in divisor_a:
            for g in divisor_c:
                f = a // d
                e = c // g
                if d*g + e*f == b:
                    return d,e,f,g
    elif D == 0:
        d = a ** 0.5
        e = c ** 0.5
        return d,e
    else:
        return "해가 없습니다."
if __name__ == "__main__":
    a = int(input("a: "))
    b = int(input("b: "))
    c = int(input("c: "))
    print(solution(a,b,c))

