def calculate(exp):
    # 연산자 표기 변환
    operators = '+-*/'
    exp = exp.replace('x', '*').replace('÷', '/').split()
    # 연속된 연산자 처리
    for i in range(len(exp)-1):
        if exp[i] in operators and exp[i+1] in operators:
            return "잘못된 계산식입니다."

    # 우선순위 정의
    op_priority = {'+': 0, '-': 0, '*': 1, '/': 1}
    op_stack = []
    postfix = []


    # 중위 → 후위 변환
    for e in exp:
        if e.isdigit():
            postfix.append(e)
        elif e in operators:
            while op_stack and op_priority[op_stack[-1]] >= op_priority[e]:
                postfix.append(op_stack.pop())
            op_stack.append(e)

    while op_stack:
        postfix.append(op_stack.pop())

    print("후위표기식:", postfix)

    # 후위 계산
    try:
        nums = []
        for e in postfix:
            if e.isdigit():
                nums.append(float(e))
            else:
                b = nums.pop()
                a = nums.pop()
                if e == '+':
                    nums.append(a + b)
                elif e == '-':
                    nums.append(a - b)
                elif e == '*':
                    nums.append(a * b)
                elif e == '/':
                    nums.append(a / b)
    except ZeroDivisionError:
        return "계산중 0으로 나누는 과정이 발생하였습니다."
    result = nums[0]
    return int(result) if result % 1 == 0 else result
