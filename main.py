# # #클레스
# # class FourCal:
# #     # pass    #추가 내용이 없어도 상속받은 기능은 그대로 사용가능
# #     #생성자(멤버 메소드)
# #     def __init__(self):
# #         #멤버 변수(속성)
# #         self.result = 0
# #
# #         #멤버 메소드
# #     def add(self, num):
# #         self.result += num
# #         return self.result
# #
# #     def sub(self, num):
# #         self.result -= num
# #         return self.result
# #
# #     def mul(self,num):
# #         self.result *= num
# #         return self.result
# #
# #     def div(self,num):
# #         self.result /= num
# #         return self.result
# #
# # cal1  = FourCal()
# #
# #
# # # # 상속 (Inheritance)
# # #
# # class MoreFourCal(FourCal):
# #     def pow(self, num):
# #         self.result = self.result ** num
# #         return self.result
# #
# #     #add 오버라이딩(overriding)
# #     def add(self, num):
# #         super().add(num)    #super class = 부모 클래스 s
# #         return self.result
#
# #     #연산자 오버라이딩
# #     def __add__(self, other):
# #         new_cal = MoreFourCal()
# #         new_c
# #         self.result + other.result
# #
# #
# # mcal1 = MoreFourCal()
# # mcal2 = MoreFourCal()
# # mcal1.add(5)
# # mcal2.add(7)
# #
# # list
#
# class Student:
#     def __init__(self):
#         self.result = 0
#
#     def sum(self, val1, val2, val3):
#         self.value = val1 + val2 + val3
#         return self.value
#
#     def avg(self,val1, val2, val3):
#         self.value = (val1+ val2+ val3)/ 3
#         return self.value
#
# std = Student()
# std.sum(10,20,30)
# print(std.value)
# std.avg(10,20,30)
# print(std.value)


# def solution(s):
#     x = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9}
#     a,b = x.keys(),x.values()
#     for i in a:
#         if i in s:
#             s.replace(i,b[])
#     answer = s
#     return answer



