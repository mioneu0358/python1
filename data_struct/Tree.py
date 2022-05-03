class TreeNode:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

class BinaryTree:
    def __init__(self):
        self.root = None
        
    def insert(self, value):
        node = TreeNode(value, None, None)
        # 트리가 비어있는 경우
        if self.root is None:
            self.root = node
            return
        # 트리가 비어있지 않은 경우
        curr = self.root
        while True:
            if value >= curr.value:
                if curr.right is None:
                    curr.right = node
                    return
                curr = curr.right
            else:
                if curr.left is None:
                    curr.left = node
                    return
                curr = curr.left

    def find(self, value):
        # 찾으면 True 아니면 False
        curr = self.root
        while curr:
            if curr.value == value:
                return True
            elif curr.value < value:
                curr = curr.right
            else:
                curr = curr.left
        return False

    def delete(self, value):
        parent = None       # 현재 노드의 부모
        curr = self.root    # 현재 노드
        while curr:
            if curr.value == value:
                # 삭제 하려는 노드의 자식 노드가 없는 경우
                if curr.right is None and curr.left is None:
                    if parent.left == curr:
                        parent.left = None
                    else:
                        parent.right = None
                # 삭제 하려는 노드의 자식 노드가 하나인 경우
                elif curr.right is None and curr.left is not None:
                    if parent.left == curr:
                        parent.left = curr.left
                    else:
                        parent.right = curr.left
                elif curr.right is not None and curr.left is None:
                    if parent.left == curr:
                        parent.left = curr.right
                    else:
                        parent.right = curr.right
                # 삭제 하려는 노드의 자식 노드가 두개인 경우(왼쪽 서브트리의 제일 오른쪽 값을 삭제할 노드의 위치로 복사)
                else:
                    # 후속자를 찾는 과정
                    ret_value = curr.value  # 리턴할 삭제값 저장
                    succ_p = None       # 후속자의 부모
                    succ = curr.left    # 후속자를 삭제할 값의 왼쪽 서브트리에서 찾는다
                    while succ.right is not None:
                        succ_p = succ
                        succ = succ.right
                    curr.value = succ.value     # 삭제 노드의 위치에 후속자의 값 복사
                    succ_p.right = succ.left    # 후속자와 후속자 부모의 연결을 끊고 왼쪽 자식을 연결해줌(None일 수 있음)
                    return ret_value
                return curr.value
            elif curr.value < value:
                parent = curr
                curr = curr.right
            else:
                parent = curr
                curr = curr.left
        return None
        
