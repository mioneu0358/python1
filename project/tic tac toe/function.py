def log_in(id,pw):
	f = open("log_in.txt","r",encoding= "utf-8")
	lines = f.readlines()
	user_id = ''
	user_pw = ''
	for line in lines:

		if line[:3] == "ID:":
			user_id = line[4:].replace('\n','')
		elif line[:3] == "PW:":
			user_pw = line[4:].replace('\n','')

		if user_id == id and user_pw == pw:
			return 1
	return 0


def disp_board(board):
	for i in range(3):
		print("-------------")
		print("| %c | %c | %c |" %(board[i*3],board[i*3+1],board[i*3+2]))
	print("-------------")


def victory(board,user):
	#조건을 충족할경우 1리턴 아닐경우 0리턴
	for i in range(3):
		if board[i * 3] == user and board[i * 3 + 1 ] == user and board[i * 3 +2] == user:
			return 1
		elif board[i+ 0] == user and board[i+ 3] == user and board[i+ 6] == user:
			return 1
	if board[0] == user and board[4] == user and board[8] == user:
		return 1
	elif  board[2] == user and board[4] == user and board[6] == user:
		return 1
	return 0

def Draw(turn):
	return turn == 9
