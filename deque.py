class DQelement:
    def __init__(self,value,left,right):
        left = None
        right = None
        self.value = value

class Deque:
    def __init__(self):
        self.rear = None
        self.front = None


    def insert_rear(self,value):
        elem = DQelement(self,None,None)
        if self.rear is None:
            self.rear = elem
            self.front = elem
        else:
            self.rear = elem
            self.rear.left = elem


    def insert_front(self,value):
        elem = DQelement(self,None, None)
        if self.rear is None:
            self.rear = elem
            self.front = elem
        else:
            self.front = elem
            self.rear.right = elem


    def delete_rear(self):
        if self.rear is None:
            return None
        value = self.rear.value
        if self.rear == self.front:
            self.rear = self.front = None
        else:
            self.rear = self.rear.right
            self.rear.right = None
        return value


    def delete_front(self):
        if self.rear is None:
            return None
        value = self.front.value
        if self.rear == self.front:
            self.rear = self.front = None
        else:
            self.front = self.front.left
            self.front.left = None
        return value

        pass

    def reverse(self0):
        pass

dq = Deque()
for i in range(1,6):
    dq.insert_rear(i)
    dq.insert_front(-i)

for j in range(10):
    print(dq.delete_front())
    
https://allendowney.github.io/DSIRP/deque.html
