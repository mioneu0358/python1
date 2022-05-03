import random
game_board = ['*'] * 9
#보드 출력
def print_board(game_board):
    for i in range(3):
        print(game_board[i*3]+ ' | ' + game_board[i*3 +1]+ ' | ' + game_board[i*3 +2])

#우승 기준
def win(OX):
  if game_board[0:3].count(OX) ==3 or game_board[3:6].count(OX) ==3 or game_board[6:9].count(OX) ==3  :
      return 1
  elif game_board[0:9:3].count(OX) == 3 or  game_board[1:9:3].count(OX) == 3 or  game_board[2:9:3].count(OX) == 3 :
      return 1
  elif game_board[0] == OX and game_board[4] == OX and game_board[8] == OX:
      return 1
  elif game_board[2] == OX and game_board[4] == OX and game_board[6] == OX:
      return 1
  else:
      return 0

#게임 실행

turn = 0
player = input("'O' 나 'X'를 선택하시오: ")
computer = 'X' if player == 'O' else 'O'
while True:
    #player 턴
    if turn % 2 == 0:
        while True:
            num = int(input("좌표를 입력하시오: "))-1
            if game_board[num] != '*':
                print("이미 있는 자리입니다. 다시 입력하시오")
                continue
            game_board[num] = player
            print_board(game_board)
            turn += 1
            break
        if win(player):
            print("player Win!")
            break
    #computer 턴
    elif turn % 2 == 1:
        while True:
            com_num = random.randrange(0,9)
            if game_board[com_num] != '*':
                continue
            game_board[com_num] = computer
            print_board(game_board)
            turn += 1
            break
        if win(computer):
            print("computer Win!")
            break
    if turn == 9:
        print("무승부")
        print()
        print()
        print("Restart!")
        game_board = ['*'] * 9
        turn = 0




