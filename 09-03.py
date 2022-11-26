#연산자 오버로딩(Operator overloading)
#메서드 오버로딩 = 클래스에 정의된 메서드들을 매개변수 목록에 따라 다르게 호출하는 방식
#== 매개변수를 다르게 넘겨주는 방식으로 메서드에 다형성(polymorphism)을 부여하는 것


#산술 연산자 오버로딩(Arithmetic operator overloading)
# +(__add__), -(__sub__),*(__mul__), /(__truediv__), **(__pow__),//(__floordiv__), %(__mod__)

# class ArithmeticAddlist(list):
#     def __init__(self,data = ()):
#         super().__init__(data)
#
#     # + 연산자에 대한 오버로딩
#     #self가 왼쪽 피연산자, other가 오른쪽 피연산자
#     def __add__(self, other):
#         #두 리스트의 길이가 다르면 예외 발생
#         if len(self) != len(other):
#             raise Exception("리스트의 길이가 다릅니다.")
#         # 결과값을 저장할 새 인스턴스를 생성한다.
#         result = ArithmeticAddlist()
#
#         #각 원소들을 더하여 결과값에 저장한다.
#         for item1,item2 in zip(self,other):
#             result.append(item1 + item2)
#         return result
#
#
# alist1 = ArithmeticAddlist([1,2,3])
# alist2 = ArithmeticAddlist([4,5,6])
# alist3 = alist1 + alist2
# print(alist3)
#
# # 비교연산자 오버라이딩(Comparison operator overloading)
# #==(__eq__), !=(__ne__), >(__gt__), < (__lt__),
#
#
# class Point2D:
#     def __init__(self,x,y):
#         self.x = x
#         self.y = y
#
#     # 두 피연산자를 비교하여 x,y좌표가 모두 같으면 True 아니면 False
#     def __eq__(self, other):
#         return self.x == other.x and self.y == other.y
#
#     def __ne__(self, other):
#         # not equal은 equal의 부정값이다.
#         return not self.__eq__(other)
#
# p1 = Point2D(1,2)
# p2 = Point2D(1,2)
# p3 = Point2D(2,3)
# print(p1 == p2)
# print(p1 == p3)
# print(p1 != p3)


#
# class ThreeItem:
#     def __init__(self,item1,item2,item3):
#         self.item1 = item1
#         self.item2 = item2
#         self.item3 = item3
#
#     def __getitem__(self, item):
#         if item == 0:
#             return self.item1
#         elif item == 1:
#             return self.item2
#         elif item == 2:
#             return self.item3
#         else:
#             raise IndexError("0~2까지의 값만 참조할 수 있습니다.")
#
# t = ThreeItem("하나", "둘","셋")
# print(t[0])
# print(t[1])
# print(t[2])
# print(t[3])




#TODO: 연결 리스트(Linked List)구현하기
#순차 자료구조(Sequential data type)
# 순차 자료구조는 데이터를 컴퓨터의 메모리상에 물리적으로 연속적으로 저장하고 접근하는 자료구조를 뜻한다.
# 보통 C언어와같은 로우레벨언어는 순차자료구조  배열(Array)이라는 자료구조를 사용한다.

#연결 자료구조(Linked data type)
# 연결 자료구조는 메모리에 저자오딘 물리적인 위치와 관계없이 연결이라는 논리적인 순서로 데이터를 접근한다. 물론 실제 데이터는 메모리에 위치해있지만,
# 그 데이터들이 메모리상에서 연속적으로 존재하지않는다. 대신 원소에는 데이터뿐만 아니라 다음 원소의 위치를 저장하는 링크도
# 있다. 이 연결 자료구조의 대표적인 예가 연결리스트이다. 연결리스트는 노드라고 하는 데이터를 저장하는 객체들의

#TODO:노드 클래스 구현하기
# 노드는 데이터를 저장하는 data와 다음 연결(노드)을 저장하는 link 속성을 가지고 있다. 이 조건을 만족하는 클래스 Node를 작성하라

class Node:
    def __init__(self,data,link = None):
        self.data = data
        self.link = link
# b = Node(2)
# a = Node(1,b)
# print(a.data)
# print(a.link.data)
# print(a.link.link)

class Mylist:
    def __init__(self,*args):
        self.head = None
        self.tail = None
        self.length = 0
        for i in args:
            self.append(i)

    def append(self,data):
        node = Node(data)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.link = node
            self.tail = node
        self.length += 1

    # def __iter__(self):
    #     node = self.head
    #     while node:
    #         yield node.data
    #         node = node.link

    def __iter__(self):
        # 이터레이터를 반환하는 제너레이터 함수 구현
        def gen():
            # 첫번째 노드를 현재 노드로 초기화
            curr = self.head
            #노드가 None이 아닐때 까지 반복
            while curr is not None:
                #노드의 데이터를 next 호출시 넘김
                yield curr.data
                # 다음 노드로 넘어감
                curr = curr.link
        #함수를 호출하여 이터레이터 반환
        return gen()

    def __len__(self):
        return self.length

    # def __str__(self):
    #     ret_str = ""
    #     curr = self.head
    #     while curr:
    #         ret_str += str(curr.data) + ', '
    #         curr = curr.link
    #     return "<" + ret_str[:-2] + ">"

    def __str__(self):
        s = "<"
        for idx,data in enumerate(self):
            s += str(data)
            if idx < len(self)-1:
                s += ", "
            else:
                s += ">"
        return s

    def __getitem__(self, item):
        if type(item) is not int:
            raise TypeError("인덱스는 반드시 정수여야 합니다.")

        if item < 0:
            item  = len(self) + item
        if item >= len(self) or item < 0:
            raise IndexError("인덱스 범위를 벗어났습니다.")

        for idx, data in enumerate(self):
            if idx == item:
                return data

    def __setitem__(self, key, value):
        if type(key) is not int:
            raise TypeError("인덱스는 반드시 정수여야 합니다.")
        if key < 0:
            key = len(self) + key
        if key >= len(self) or key < 0:
            raise IndexError("인덱스 범위를 벗어났습니다.")

        curr = self.head
        for i in range(key):
            curr = curr.link
        curr.data = value


mylist = Mylist(1,2,3,4)
mylist[2] = 5
print(mylist)



