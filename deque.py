#deque (double ended queue) =  list와 같이 요소들을 한곳에 담아 두는 배열
#Queue(큐)는 FIFO방식이지만, 덱은 양방향인 큐여서 양쪽에서 요소를 추가 제거 할 수 있다.
#list가 있음에도 deque를 사용하는 이유는 덱의 속도가 훨씬 빠르기 때문이다.


class DQelement:
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right

class Deque:
    def __init__(self):
        self.rear = None
        self.front = None

    def insert_rear(self, data):   #rear로 넣을때
        elem = DQelement(data, None, self.rear)
        if self.rear is None:       #rear가 비어있을때 == front도 비어있을 때
            self.rear = elem        #rear와 front 둘 다 elem를 가르킨다
            self.front = elem
        else:                       #elem이 하나 이상 있을때
            self.rear.left = elem   #기존에 있던 rear의 왼쪽이 새로온 elem을 가르키고
            self.rear = elem        #rear를 새로 들어온 elem으로 바꿔준다

    def insert_front(self, data):  #front로 넣을때는 rear로 넣을때의 반대로 하면 된다
        elem = DQelement(data, self.front, None)
        if self.front is None:
            self.rear = elem
            self.front = elem
        else:
            self.front.right = elem
            self.front = elem

    def delete_rear(self):                   #rear에서 뺄 때
        if self.rear is None:                #원소가 없을 경우엔
            return None
        data = self.rear.data              #rear에서 빼기 때문에 value는 rear의 value가 된다
        if self.rear == self.front:          #원소가 하나 있을 경우
            self.rear = self.front = None    #rear와 front를 None으로 만들어 주면 된다
        else:                                #원소가 두개 이상 있을경우
            self.rear = self.rear.right      #rear를 rear의 right로 바꿔주고
            self.rear.left = None            #바뀐 rear의 left를 None으로 바꿔서 연결을 끊어준다
        return data

    def delete_front(self):                  #front에서 뺄 때는 반대로
        if self.front is None:
            return None
        data = self.front.data
        if self.rear == self.front:
            self.rear = self.front = None
        else:
            self.front = self.front.left
            self.front.right = None
        return data



    def reverse(self):
        curr = self.rear    #rear에서 시작, curr(현재)라는 변수로 rear를 받아주고
        while curr:         #curr이 존재할 때 까지
            curr.left, curr.right = curr.right,curr.left        #현재의 좌우 링크를 바꿔주고
            curr = curr.left                                    #현재를 현재의 왼쪽으로 바꿔준다
        self.rear, self.front = self.front, self.rear           #마지막으로 rear와 front를 바꿔주면 끝

dq = Deque()
for i in range(1, 6):
    dq.insert_rear(i)
    dq.insert_front(-i)

for j in range(10):
    print(dq.delete_front())    
