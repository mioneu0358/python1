#__init__ self = 생성될 인스턴스


#인스턴스화


#인스턴스 객체(instance Object)
# 인스턴스객체가 수행하는 단 하나의 연산은 참조연산이다.

#메서드 - 객체에 속한 함수. 객체의 올바른 메서드 이름은 해당 클래스에따라 다르다.
#클래스의 모든 함수 객체속성들을상응하는 인스턴스의메서드들을 정의한다.
# class myclass:
#     def f(self):
#         return "hello"
# x = myclass()
# print(type(x.f))        #method
# print(type(myclass.f))  #function


#
# class AAA:
#     share = 10
#     def __init__(self,value):
#         self.unique = value
#
# a = AAA(1)
# b = AAA(2)
# print(a == b)                   # False  서로 다른 인스턴스객체이기 떄문에 같지 않다.
# print(a.unique == b.unique)     # False  //
# print(a.share == b.share)       # True   share는 인스턴스객체가 아닌 클래스 객체이므로 공유된다.
# AAA.share = 0
# print(a.share == b.share)       # True    a와b가 share를 가지는 것이 아니라 AAA의 share를 참조한다.
# a.share = 5
# print(a.share == b.share)       # False   a.share=5 는 a에 share라는 새로운 객채를 생성하여 5를 대입한것이므로 기존의 AAA의 share를 참조하던것이 가려진다.


# class Person:
#     cnt = 0
#
#     def __init__(self,name:str,num:str,address:str):
#         self.name = name
#         self.num = num
#         self.address = address
#         Person.cnt += 1
#
#
#     def get_name(self):
#         return self.name
#     def chage_name(self,name:str):
#         self.name = name
#     def get_age(self):
#         return 2022 - (1900+int(self.num[:2]))
#     def get_s(self):
#         s = self.num.split('-')[1][0]
#         if s in ['1','3']:
#             return "male"
#         else:
#             return "female"
#     def get_address(self):
#         return self.address
#     def change_address(self,address:str):
#         self.address = address
#     def get_cnt(self):
#         return self.cnt
#
#
# man1 = Person("박찬빈","941227-1","부천시")
#
# print(man1.get_cnt())


# 다중 상속

# class 파생클래스식별자(기반클래스1,기반클래스2,...):
#     def 기반클래스의 기능(self):
#         pass
# 상속받은 기능을 찾기 위해서 dfs방식으로 탐지를 해나간다.
# # 다이아몬드상속
#    class A
#    /      \
#



# class Reverse:
#     def __init__(self,data):
#         self.data = data
#         self.index = len(data)
#     def __iter__(self):
#         return self
#     def __next__(self):
#         if self.index == 0:
#             raise StopIteration
#         self.index = self.index -1
#         return self.data[self.index]
# rev = Reverse("HELLO")
# for char in rev:
#     print(char)
# # for문은 객채의 iterater객채를 호출한다.

# 제너레이터(generagter) =
# def generate_test():
#     yield 1
#     yield 2
#     yield 3
# it = generate_test()
# print(next(it))
# print(next(it))
# print(next(it))
# print(next(it))

#
# def reverse(data):
#     for i in range(len(data)-1,-1,-1):
#         yield data[i]
#
# for char in reverse("HELLO"):
#     print(char)


# 세 종류의 값을 저장하는 클래스

# class value3:
#     def __init__(self,v1,v2,v3):
#         self.v1 = v1
#         self.v2 = v2
#         self.v3 = v3
#         self.index = -1
#
#     def __iter__(self):
#         return self
#     def __next__(self):
#         self.index += 1
#         if self.index > 2 :
#             raise StopIteration
#         if self.index == 0:
#             return self.v1
#         elif self.index == 1:
#             return self.v2
#         else:
#             return self.v3


# Generater.ver
#
# class value3:
#     def __init__(self, v1, v2, v3):
#         self.v1 = v1
#         self.v2 = v2
#         self.v3 = v3
#
#     def __iter__(self):
#         def gen_iter():
#             yield self.v1
#             yield self.v2
#             yield self.v3
#         return gen_iter()
#
#
# value3 = value3("문자열",1000,("튜플",1))
#
#
# # 1.for문은 내부적으로 in 우측에 있는 객체에 대한 iter 메소드를 실행한다.
# # 2. iterator 객체에서 next 메서드 호출
# # 3. 2번을 StopIteration 예외 발생 까지 반복
# for i in value3:
#     print(i)



# 연산자 재정의 (Operator overiding)
# class Person:
#     def __init__(self,name):
#         self.name = name
# 
#     def print_name(self):
#         print(self.name)
# 
#     def __add__(self, other):
#         new = Marriage(self,other)
#         return new
# 
# 
# 
# class Marriage:
#     def __init__(self,x,y):
#         self.x = x
#         self.y = y
# 
# 
#     def print_familly(self):
#         print("[가족구성]")
#         self.x.print_name()
#         self.y.print_name()
# 
# 
# a = Person("철수")
# b = Person("영희")
# # a + b == a.__add__(b)
# m = a+b
# 
# m.print_familly()
