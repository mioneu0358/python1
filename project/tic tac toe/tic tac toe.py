from function import disp_board
from function import victory
from function import Draw
from function import log_in
import random

#로그인

count = 1
while True:
    id = input("ID: ")
    pw = input("PW: ")
    if count == 3:
        print("3회 이상 로그인 되었습니다. 종료합니다.")
        exit()
    if log_in(id, pw):
        print("로그인 되었습니다.")
        break
    print("아이디와 비밀번호를 확인해주세요")
    count += 1


# 게임 실행 부분
player = input("'O' 나 'X'를 선택하시오: ")
if player == 'O':
	computer = 'X'
else:
	computer = 'O'
#보드판 초기화
board = ['*'] * 9
#보드판 출력
disp_board(board)
turn = 0

#게임 실행
while True:
    # Player turn
    while True:
        pos = int(input("좌표를 입력하시오(1~9): "))
        if board[pos-1] == "*":
            board[pos-1] = player
            break
        print("해당 자리가 입력되어있습니다.")
    disp_board(board)
    if victory(board,player) == 1:
        print("Player Win!")
        break
    turn +=1

    #무승부
    if Draw(turn):
        print("----Draw----")
        if input("Restart?(Y/N): ") == "Y":
            turn = 0
            board = ['*'] * 9
            continue
        else:
            break

    #computer turn
    while True:
        pos = int(random.random()* 10) % 9 #0~8
        if board[pos] == '*':
            board[pos] = computer
            break

    disp_board(board)
    if victory(board, computer) == 1:
        print("Computer win!")
        break
    turn += 1







