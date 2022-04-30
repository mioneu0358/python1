import random   #random 사용 암시
#중복체크 /
make_board = []     #틱택톡 보드판 만들기
def tic():
    for i in range(9):
        make_board.append('*')

def board():
    print(make_board[0] +" | "+ make_board[1] +" | "+ make_board[2])
    print("---------")
    print(make_board[3] +" | "+ make_board[4] +" | "+ make_board[5])
    print("---------")
    print(make_board[6] +" | "+ make_board[7] +" | "+ make_board[8])

# --> 보드판 만들기
def check_win(who_turn):    #게임 승리 조건

    check = False # True  win, False

    if make_board[0] == who_turn and make_board[1] == who_turn and make_board[2] == who_turn:   #맨위 가로연결
        check = True
    elif make_board[3] == who_turn and make_board[4] == who_turn and make_board[5] == who_turn: #중간 가로연결
        check = True
    elif make_board[6] == who_turn and make_board[7] == who_turn and make_board[8] == who_turn: #맨밑 가로연결
        check = True
    elif make_board[0] == who_turn and make_board[3] == who_turn and make_board[6] == who_turn: #맨왼 세로연결
        check = True
    elif make_board[1] == who_turn and make_board[4] == who_turn and make_board[7] == who_turn: #중간 세로연결
        check = True
    elif make_board[2] == who_turn and make_board[5] == who_turn and make_board[8] == who_turn: #맨왼 세로연결
        check = True
    elif make_board[0] == who_turn and make_board[4] == who_turn and make_board[8] == who_turn: # \ 연결
        check = True
    elif make_board[2] == who_turn and make_board[4] == who_turn and make_board[6] == who_turn: # / 연결
        check = True
    return check

tic()               #게임시작
board()             #보드판 열림
turn = 0            #자기 턴
while True:
    # my turn
    if turn == 0:   #자기 턴일 때
        while True:
            choose = int(input('Enter the your location : ')) #위치 정해서 표시
            if make_board[choose] == '*':        #안 고른 위치이면
                make_board[choose] = 'O'         #0입력  ==> 이것은 별 표 있는 것만 고른다는 것을 의미 중복시 계속 반복해
                break

        board()                                 #입력 성공한다면 보드 등장
        check = check_win('O')                  #O이 보드판안에 조건 충족
        if check:                               #만약 이기는 조건을 충족한다면
            print("your win")
            break
        turn = 1 #턴 바뀜

    else:        #컴퓨터 차례
        print('computer Turn')
        while True:
            computer = random.randrange(0, 9) #컴퓨터는 랜덤으로 값을 넣는다.
            if make_board[computer] == '*':   #컴퓨터는 중복되지 않는 값 중에서 골라서
                make_board[computer] = 'X'    #X를 표시한다.
                break

        turn = 0     #사용자 차례로 바뀜
        board()      #틱택 보드 다시
