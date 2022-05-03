# 큐(Queue)
# 1. 데이터를 줄을 세우는것 => 선입선출 ,후입후출
# 2. list에 구현되어있음

# a = []
# a.append(1)
# a.append(2)
# a.append(3)

# print(a.pop(0))
# print(a.pop(0))
# print(a.pop(0))

class QueueElement():
        #생성자 생성
        def __init__(self,value,next):
            #요소의 값
            self.value = value
            # 다음 요소의 위치
            self.next = next

class Queue:
    def __init__(self):
        self.Rear = None
        self.Front = None

    def enqueue(self, value):
         #큐가 비어있는 경우
         if self.Rear is None:
             elem = QueueElement(value, None)
             self.Rear = elem
             self.Front = elem
         #큐가 있는 경우
         else:
            elem = QueueElement(value, None)
            self.Rear.next = elem
            self.Rear = elem

    def dequeue(self):
        #큐가 비어 있는 경우
        if self.Front is None:
            return None
        # 큐가 있는 경우
        else:
            value =self.Front.value
            self.Front = self.Front.next
            return value

    def reverse(self):
        prev =None
        curr = self.front
        while curr:
            next = curr.next
            curr.next = prev
            prev = curr
            curr = next
        self.Rear, self.Front = self.Front, self.Rear


que = Queue()
for i in range(10):
    que.enqueue((i))
que.reverse()
for i in range(10):
    print(que.dequeue())

