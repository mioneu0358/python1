# 틱택토 프로젝트
# 3X3 보드판에서 O나 X를 선택 후, 빙고가 되도록 보드판을 선택하는 게임
# 로그인, O나 X를 선택하는 기능, O나 X를 보드판에 입력하는 기능, 우승 확인,
# 보드판을 확인하는 기능, 컴퓨터가 랜덤한 위치에 O나 X를 입력하는 기능,

from functions import *


# 게임 실행 순서
# ------- 1. 로그인 -------
cnt = 0
while True:
    input_id = input("아이디를 입력하세요: ")
    input_pw = input("비밀번호를 입력하세요: ")
    if log_in(input_id,input_pw):
        print(f"{input_id}님 로그인 되었습니다.")
        break
    else:
        print("아이디나 비밀번호를 확인해주세요")
    cnt += 1
    if cnt == 3:
        print("로그인 횟수가 3회를 초과했습니다. 종료합니다.")
        exit()
# ------- 1. 로그인 -------

# ----- 2.plyaer와 compter에 문양 넣어주기 -----
player = ''     # player의 문양
computer = ''   # computer의 문양
while True:
    player = input("O나 X를 선택해주세요: ")
    if player in ['O','X']:
        if player == 'O':
            computer = 'X'
        else:
            computer = 'O'
        break
    else:
        print("다시 입력해주세요.")
# ---
# -- plyaer와 compter에 문양 넣어주기 -----


board = ['*'] * 9

display_board(board)


# 게임 실행
while True:
# 3-1 이미 입력된 자리일 경우 다시 입력받는다.input_pos()를
# 사용해서 위치 가져오기
    pos = input_pos(board)
    board[pos] = player

    display_board(board)
# TODO:4.victory(board, player)를 사용해서 우승조건 판별
# 4-1 우승 조건: 한 줄 빙고
    if victory(board,player):
        print("Player Win!")
        exit()
    if DRAW(board):
        print("무승부")
        exit()
# 5. 컴퓨터가 랜덤한 자리에 문양 입력
# 5-1 이미 입력된 자리일 경우 다시 자리를 구한다.
# import random 후에 random.randint()사용
    pos = random_pos(board)
    board[pos] = computer
    display_board(board)

# 6. victory(board, computer)를 사용해서 우승조건 판별
# 6-1 우승 조건: 한 줄 빙고
    if victory(board, computer):
        print("Computer Win!")
        exit()





# 3~6은 우승 조건이 나오기 전까지 or 무승부 조건이 되기 전까지 반복
