
#deque (double ended queue) =  list와 같이 요소들을 한곳에 담아 두는 배열
#Queue(큐)는 FIFO방식이지만, 덱은 양방향인 큐여서 양쪽에서 요소를 추가 제거 할 수 있다.
#list가 있음에도 deque를 사용하는 이유는 덱의 속도가 훨씬 빠르기 때문이다.


# Deque(Double-ended queue) 덱
class DequeElement:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

class Deque:
    def __init__(self):
        self.rear = None
        self.front = None

    def insert_rear(self, value):
        elem = DequeElement(value, None, self.rear)
        if self.rear is None:
            self.rear = elem
            self.front = elem
        else:
            self.rear.left = elem
            self.rear = elem

    def insert_front(self, value):
        elem = DequeElement(value, self.front, None)
        if self.rear is None:
            self.rear = elem
            self.front = elem
        else:
            self.front.right = elem
            self.front = elem

    def delete_rear(self):
        if self.rear is None:   # 원소가 없는 경우
            return None
        value = self.rear.value
        if self.rear == self.front:  # 원소가 하나인 경우
            self.rear = self.front = None
        else:   # 원소가 두개 이상인 경우
            self.rear = self.rear.right
            self.rear.left = None
        return value

    def delete_front(self):
        if self.rear is None:   # 원소가 없는 경우
            return None
        value = self.front.value
        if self.rear == self.front:  # 원소가 하나인 경우
            self.rear = self.front = None
        else:   # 원소가 두개 이상인 경우
            self.front = self.front.left
            self.front.right = None
        return value

    def reverse(self):
        curr = self.rear
        while curr is not None:
            curr.left, curr.right = curr.right, curr.left
            curr = curr.left
        self.rear, self.front = self.front, self.rear


d = Deque()

for i in range(1, 6):
    d.insert_rear(i)
    d.insert_front(-i)
d.reverse()
for i in range(10):
    print(d.delete_rear())
