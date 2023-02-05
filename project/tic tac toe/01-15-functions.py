def log_in(input_id,input_pw):
    # log_in.txt파일을 불러와서 입력받은 input_id와 input_pw가 일치하는지
    # 확인후에 일치할 경우 True, 아니면 False를 리턴하시오
    real_id = ""
    real_pw = ""
    file = open('log_in.txt','r',encoding='utf8')
    lines = file.readlines()
    for line in lines:
        key,value = line.split()
        if '\n' in value:
            value = value.replace('\n','')
        if key[:-1] == 'ID':
            real_id = value
        else:
            real_pw = value
            if real_id == input_id and real_pw == input_pw:
                return True
    return False


def display_board(board):
    for i in range(3):
        print("-------------")
        print(f"| {board[i*3]} | {board[i*3+1]} | {board[i*3+2]} |")
    print("-------------")


def input_pos(board):
    while True:
        pos = int(input("1부터 9 사이의 값을 입력하시오: "))
        if 1 <= pos <= 9:
            if board[pos-1] == '*':
                return pos -1
            else:
                print("이미 있는 자리입니다. 다시 입력해주세요")
        else:
            print("범위를 벗어났습니다. 다시 입력해주세요")
        # pos은 보드판의 범위 안에 있어야 하고,
        # 보 드판의 pos번째 값이 * 이어야한다.
        # 위의 조건에 만족하지 않으면 다시 입력받는다.

def victory(board,user):
    for i in range(3):
        if board[i*3] == board[i*3+1] == board[i*3+2] == user:
            return True
        elif board[i] == board[3+i] == board[6+i] == user:
            return True
    if board[0] == board[4] == board[8] == user:
        return True
    elif board[2] == board[4] == board[6] == user:
        return True
    return False
    # 가로, 세로 , 대각선 중에서 해당 유저의 문양이
    # 한줄이 되는 경우 True를 아니면 False를 return 한다.

def random_pos(board):
    import random
    while True:
        pos = random.randint(0,8)
        if board[pos] == '*':
            return pos


def DRAW(board):
    if '*' not in board:
        return True
    return False
