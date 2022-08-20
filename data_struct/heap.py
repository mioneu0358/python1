class Heap:
    def __init__(self,_list):
        self.heap = [0]+_list

    #최소 self.heap

    def insert(self, n):              # self.heap에 값을 넣는 함수
        self.heap.append(n)          # self.heap의 맨 마지막에 값을 삽입한다.
        curr_pos = len(self.heap)-1  # 현재 위치 기억(마지막자리에 넣었기 떄문에 길이 -1)
        while curr_pos != 0:    # 현재 위치가 루트가 아닐 때 까지
            parent_pos = curr_pos // 2 # 부모의 위치는 자신의 위치 // 2
            if self.heap[parent_pos] > self.heap[curr_pos]:
                self.heap[parent_pos],self.heap[curr_pos] = self.heap[curr_pos],self.heap[parent_pos]
            else:
                break
            curr_pos = parent_pos   # 값이 교환되었으므로 자식을 가리키는 index도 변경시켜준다.


    def smallest(self,):
        if len(self.heap) == 1:
            return None
        value = self.heap[1]         # 반환할 최소값을 기억해둔다.
        last = self.heap.pop()
        if len(self.heap) == 1:
            return value
        self.heap[1] = last

        p = 1                   #현재 위치(부모의 위치)
        while p * 2 <= len(self.heap) -1 :        # p의 자식이 존재할 때 까지
            c0 = p * 2                  # 왼쪽 자식의 위치
            c1 = p * 2 + 1             # 오른쪽 자식의 위치
            minc = 0                   # 최소값을 가질 자식의 위치
            if c1 <= len(self.heap) -1:     #오른쪽 자식이 존재할 때
                minc = c0 if self.heap[c0] < self.heap[c1] else c1    #자식 둘을 비교해서 최소값을 받는다.
            else:
                minc = c0
            if self.heap[p] > self.heap[minc]:
                self.heap[p],self.heap[minc] = self.heap[minc],self.heap[p]
            else:
                break

            p = minc                   # 값을 교환했으면 위치도 따라서 바꾸어 준다.

        return value
