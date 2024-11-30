class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None


class MinHeap:
    def __init__(self):
        self.root = None    # 최상위 노드
        self.last = None    # 가장 마지막에 추가된 노드

    def get_insert_position(self):
        # 연결할부모노드, 부모노드와 연결할 링크(왼쪽 or 오른쪽) 가져오기
        from collections import deque
        Que = deque()
        Que.append(self.root)
        while Que:
            curr = Que.popleft()
            if curr.left is None:
                return curr, 'L'
            elif curr.right is None:
                return curr,'R'
            else:
                Que.append(curr.left)
                Que.append(curr.right)

    def heapify_up(self, curr):
        # 현재 바라보고 있는 노드의 데이터와 부모노드의 데이터를 비교하여 교환하는 작업
        while curr.parent:
            parent = curr.parent
            if curr.data < parent.data:
                curr.data, parent.data = parent.data, curr.data
                curr = parent
            else:
                break

    def push(self, data):
        # 가장 뒤쪽에 노드를 추가한다.
        # 추가한 노드의 값과, 그 부모 노드의 값을 서로 비교하여
        # 노드의 값이 더 작다면 부모노드의 값과 교환하는 과정을 반복한다.
        node = Node(data)
        if self.root is None:
            self.root = node
            self.last = node
        else:
            insert_pos, LR = self.get_insert_position()
            if LR == 'L':
                insert_pos.left = node
            else:
                insert_pos.right = node
            node.parent = insert_pos
            self.heapify_up(node)
            self.last = node

    def get_last(self):
        from collections import deque
        Que = deque()
        Que.append(self.root)
        prev_last = None
        while Que:
            prev_last = Que.popleft()
            if prev_last.left:
                Que.append(prev_last.left)
            if prev_last.right:
                Que.append(prev_last.right)
        return prev_last

    def heapify_down(self, node):
        while node:
            smallest = node
            if node.left and node.left.data < smallest.data:
                smallest = node.left
            if node.right and node.right.data < smallest.data:
                smallest = node.right

            if smallest != node:
                node.data, smallest.data = smallest.data, node.data
                node = smallest
            else:
                break
    def pop(self):
        if self.root is None:
            return None

        ret_data = self.root.data  # 최소값 저장
        if self.root == self.last:
            # 루트 노드가 유일한 노드인 경우
            self.root = self.last = None
        # 여러개 있는 경우, 마지막(가장 아래단계+가장 우측)노드의 데이터를 루트에 복사해 넣는다. + 마지막 노드와 그 부모의 링크를 해제
        # 루트에서 부터 아래로 내려오면서 데이터의 위치를 변환한다(heapify_down)
        # heapify_down: 현재 노드를 기준으로 왼쪽자식과 오른쪽자식을 비교, 더 작은 노드를 기억
        # 기억한 노드와 현재 노드 비교, 현재 노드의 값이 더 큰 경우 서로 교환
        # 이 과정을 반복
        else:
            # 마지막 노드와 루트 노드 교체
            self.root.data = self.last.data

            # 마지막 노드 제거
            if self.last.parent.right == self.last:
                self.last.parent.right = None
            else:
                self.last.parent.left = None

            # 새로운 마지막 노드 찾기
            self.last = self.get_last()
            # 힙 속성 복구
            self.heapify_down(self.root)

        return ret_data
data = [75, 100, 99, 40, 6, 3, 67, 80, 26, 59,
        44, 51, 62, 94, 93, 21, 46, 61, 14, 25]

minHeap = MinHeap()
for d in data:
    minHeap.push(d)

for _ in range(len(data)):
    print(minHeap.pop(), end= ' ')
# [3, 6, 14, 21, 25, 26, 40, 44, 46, 51, 59, 61, 62, 67, 75, 80, 93, 94, 99, 100]
