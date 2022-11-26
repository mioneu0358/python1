# #함수(Function)
# # 함수란 무엇인가?
# # 프로그래밍에서 함수란 특별한 목적의 작업을 수행하기 위해 독립적으로 설계된 프로그램 코드를 의미
# # 프로그래밍할 때 반복되는 작업을 함수로 만들어서 분리해두면 여러번 재사용이 가능하며 프로그램 유지보수가 쉬워지고가독성이 증가한다.
#
#
# def check_grade(score:int):
#     grade = ''
#     if  100 >= score and score >= 90:
#         grade = "A"
#     elif score >= 80:
#         grade = "B"
#     elif score >= 70:
#         grade = "C"
#     elif score >= 60:
#         grade = "D"
#     else:
#         garde = "F"
#     return grade
#
#
# def sep_ODD(_list:list):
#     ODD_list = []
#     for i in _list:
#         if i % 2 != 0:
#             ODD_list.append(i)
#     return ODD_list
#
#
# def game369(num):
#     s_num = str(num)
#     # cnt = s_num.count("3") + s_num.count("6") + s_num.count("9")
#     # if cnt == 0:
#     #     print(num)
#     # else:
#     #     print("짝" * cnt)
#
# for i in range(20,40):
#     game369(i)
#
#
# cba

# def get_average(*args):
#     total = sum(args)
#     n = len(args)
#     return total / n
#
# print(get_average(1,2,3,4,5,6,7,8,9,10))

# 재귀 함수(Recursive funcion) 함수가 함수 내부에서 자기 자신을 호출하는것
# 피보나치 수열 (1,1,2,3,5...) An = A(n-1) + A(n-2)
#
# count = 0
# def fibonacci(n):
#     global count
#     count += 1
#     if n < 2:
#         return 1
#     return fibonacci(n-1) + fibonacci(n-2)

# print(fibonacci(20))
# print("총 호출 횟수:", count)

# 고차 함수
# 파이썬의 함수는 객체.
# 파이썬의 함수는 매개변수로 넘겨줄 수 있고, 함수 내에서 반환할 수 있다.
# 파이썬의 객체는 일급 객체, 그러므로 함수는 '일급 함수'라고 한다.
# def multiplier(n):
#     def multi(x):
#         return x * n
#     return multi

# multi2 = multiplier(2)
# multi3 = multiplier(3)
# print(multi2(5))
# print(multi3(5))

# 콜백 함수
# 함수의 입력으로 들어가는 함수 객체를 콜백 함수라고 한다.
# def callback():
#     print("작업이 끝났습니다.")
#
# def print_n(n, cb):
#     for i in range(1, n + 1):
#         print(i)
#     cb()
#
# print_n(100, callback)

# 합성 함수
# f(x), g(x)의 합성 함수는 f(g(x))
# f(x) = x * x
# g(x) = x + 1
# f(g(x)) = (x + 1) * (x + 1)
# def f(func):
#     def result(x):
#         return func(x) * func(x)
#     return result
#
# def g(x):
#     return x + 1
#
# h = f(g)
# print(h(3))

# 가비지 컬렉션 (garbage collection)
# 더 이상 참조되지 않는 객체(변수)를 파이썬의 가비지 컬렉터가 확인 후 메모리에서 삭제한다.

# 클로저 (closure)
# 함수가 종료되었음에도 불구하고, 함수의 지역 변수를 참조하는
# 다른 객체가 존재하는 경우 그 지역 변수는 메모리에서 사라지지 않는다.
# 이를 클로저라고 한다.
# count = 0
# def func():
#     global count
#     count += 1
#     print(count, "번 호출되었습니다.")
# func()
# func()
# func()
#
# def factory():
#     count = {'c' : 0}
#
#     def func():
#         count['c'] += 1
#         print(count['c'], "번 호출되었습니다.")
#     return func
#
# f = factory()
# h = factory()
# f()
# f()
# f()
# h()
# h()
# h()

# 메모이제이션 (Memoization)
# 이전에 도출한 결과를 기억하고 다음에 똑같은 입력이 들어오면
# 새로 계산하는 것이 아닌 기억된 값을 돌려주는 기법
# cache = {}
# def fib(n):
#     if n < 2:
#         return 1
#     if n not in cache.keys():
#         cache[n] = fib(n - 1) + fib(n - 2)
#     return cache[n]
# print(fib(100))

# 문제) 일반 재귀함수를 메모이제이션 함수로 만들어서 반환하는
# 팩토리 함수를 작성해보세요.
# def to_memoization(func):
#     cache = {}
#     def result(n):
#         if n not in cache.keys():
#             cache[n] = func(n)
#         return cache[n]
#     return result


