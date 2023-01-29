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
            if board[pos] == '*':
                return pos -1
        else:
            print("다시 입력해주세요")
        # pos은 보드판의 범위 안에 있어야 하고,
        # 보 드판의 pos번째 값이 * 이어야한다.
        # 위의 조건에 만족하지 않으면 다시 입력받는다.


def victory(board,user):
    # 가로, 세로 , 대각선 중에서 해당 유저의 문양이
    # 한줄이 되는 경우 True를 아니면 False를 return 한다.
    return
