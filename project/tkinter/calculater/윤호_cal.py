def calculate(exp):
    # 중위표기법으로 적힌 exp를 후위표기법으로 변환 후, 연산한 결과값을 반환
    # 중위 -> 후위 규칙
    # 1. 숫자는 그대로 출력
    # 2. 연산자의 경우 이미 stack에 연산자가 있다면, stack의 마지막 연산자가 현재 보고 있는 연산자보다
    #    우선순위가 높다면 출력한다.
    # 3. 연산자를 stack에 추가

    op_priority = {'+':0,'-':0,'*':1,'/':1}
    op_stack = []
    postfix = []
    operators = '+-*/'
    for e in exp.split():
        if e.isdigit():
            postfix.append(e)
        else:
            if op_stack and op_priority[op_stack[-1]] > op_priority[e]:
                postfix.append(op_stack.pop())
            op_stack.append(e)
    postfix += op_stack[::-1]
    print(postfix)  # 123*+

    nums = []
    # 후위 표기법 계산 방식
    # 1. 숫자는 스텍에 추가
    # 2. 연산자면 스텍의 최근 두 숫자를 뽑아 연산 후 다시 스텍에 추가

    for e in postfix:
        if e.isdigit():
            nums.append(float(e))
        else:
            b = nums.pop()
            a = nums.pop()
            if e == '+':
                c = a + b
            elif e == '-':
                c = a - b
            elif e == '*':
                c = a * b
            else:
                c = a / b
            nums.append(c)
    result = nums[0]
    if result % 1 == 0:
        return int(result)
    else:
        return result

exp = "5 / 2"
result = calculate(exp)
print(result)   # 7
