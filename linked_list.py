# 리스트를 흉내낸 자료형 MyList를 구현하라
# Python의 자료형 List: 연결 리스트 <-> 순차 리스트
# self.head -> [1]-> [2]-> [3] -> [4]->  [5]-> None
class Element:
    def __init__(self,data):
        self.data = data
        self.next = None

class MyList:
    def __init__(self,*args):
        self.head = None
        self.tail = None
        self.length = 0
        for i in args:
            self.append(i)
    def __repr__(self):
        result = "<"
        curr = self.head
        for i in range(self.length):
            result += str(curr.data)
            if i != self.length-1:
                result += ', '
            curr = curr.next
        return result + '>'

    def append(self, data):
        # 새로운 노드 생성
        elem = Element(data)
        # 리스트가 비어있는 경우
        if self.head is None:
            self.head = elem
            self.tail = elem
        # 리스트가 비어있지 않은 경우
        else:
            self.tail.next = elem
            self.tail = elem
        # 연결 후 길이를 늘려준다
        self.length += 1

    def pop(self,idx = -1):
        if idx < 0:
            idx += self.length
        # print(f"idx: {idx}")
        if idx >= self.length or idx < 0:
            raise IndexError("index out of range")

        if self.head is None:
            return None
        if self.length == 1:
            ret_value = self.head.data
            self.head = self.tail = None
            self.length -= 1
            return ret_value
        else:
            if idx == 0:
                ret_value = self.head.data
                self.head.next = self.head.next.next
                self.length -= 1
                return ret_value
            elif idx == self.length - 1:
                ret_value = self.tail.data
                curr = self.head
                for i in range(idx - 1):
                    curr = curr.next
                curr.next = None
                self.tail = curr
                self.length -= 1
                return ret_value
            else:
                curr = self.head
                for i in range(idx - 1):
                    curr = curr.next
                ret_value = curr.next.data
                curr.next = curr.next.next
                self.length -= 1
                return ret_valuef



    def __getitem__(self, item):
        # print(arr[0])  => arr의 0번째 원소값을 리턴
        # item자리에 인덱스번호가 들어온다.
        pass

    def __setitem__(self, key, value):
        # arr[0] = 'a' => arr의 0번째 원소값을 'a'로 변경
        # key자리에 index번호가, value에는 변경할 원소값이 들어온다.
        pass

    def __add__(self, other):
        # arr + arr2 => <'a', 3, 4, 5, 6, 7>
        pass

    # iterator 정의 generator


arr = MyList(1,2,3,4)
# arr.check()
print(arr)  # <1, 2, 3, 4>

arr.append(5)
print(arr)  # <1, 2, 3, 4, 5>
#
print(arr.pop())    # 5
print(arr)          # <1, 2, 3, 4>
print(arr.pop(1))   # 2
print(arr)          # <1, 3, 4>
print(arr.pop())    # 4
print(arr)          # <1, 3>
print(arr.pop())    # 3
print(arr)          # <1>
print(arr.pop())    # 1
print(arr)          # <>


#
# print(arr[0])       # 1
# arr[0] = 'a'
# print(arr)          # <'a', 3, 4>
#
# arr2 = MyList(5,6,7)
# print(arr2)         # <5, 6, 7>
# print(arr + arr2)   # <'a', 3, 4, 5, 6, 7>
#
# for i in arr:
#     print(i, end=' ')   # a 3 4
