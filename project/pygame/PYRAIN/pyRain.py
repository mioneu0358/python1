import pygame
import keyword
import random
import os

class Word:
    def __init__(self, data,string,x,y,speed):
        self.data = data
        self.string = string
        self.x = x
        self.y = y
        self.speed = speed


def get_word_list():
    words_list = []
    if os.path.exists("words.text"):
        with open("words.text", "r") as file:
            words_list = list(map(lambda x : x.strip(), file.readlines()))
            return words_list
    else:
        with open("words.text", "w") as file:
            for word in keyword.kwlist:
                file.write(word+'\n')


pygame.init()

# 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
font = pygame.font.Font(None,50)


background = pygame.image.load("background.png")
heart = pygame.image.load("heart.png")
pygame.display.set_caption("타자연습 산성비")



# 타이머에 사용할 분,초,밀리초
on_board = []

game_font = pygame.font.SysFont('arial', 30, True, False)
def runGame():
    word_list = get_word_list()
    heart_cnt = 3
    input_word = ""
    FPS = 60  # FPS(Frame per Seconds)
    screen_size = (600, 800)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    run_status = True
    minutes = 0
    seconds = 0
    hour = 0


    while run_status:
        screen.blit(background, (0, 0))
        # 시간 설정
        seconds += 1
        timer = game_font.render("Timer: " + str(hour) + ":" + str(minutes) + ":" + str(seconds), True,
                                 BLACK)

        # 이벤트 처리
        for event in pygame.event.get():
            # 종료 창 버튼
            if event.type == pygame.QUIT:
                run_status = False
                pygame.quit()
            # 키 입력 이벤트
            elif event.type == pygame.KEYDOWN:
                # 엔터키 입력시
                if event.key == pygame.K_RETURN:
                    for i in range(len(on_board)):
                        if input_word == on_board[i].string:
                            del on_board[i]
                            print(1)
                            break
                    input_word = ""
                # 단어 입력
                else:
                    input_word += event.unicode
                    pygame.display.update()

    # 단어 만들기
        if not on_board:
            while len(on_board) < 15:
                idx = random.randint(0,len(word_list)-1)
                x = random.randint(0,500)
                speed=random.randint(0,30)/10
                word = Word(font.render(word_list[idx],True,(BLACK)),word_list[idx],x,50,speed)
                on_board.append(word)
    # 속도 조절
        idx = 0
        while idx < len(on_board):
            on_board[idx].y += on_board[idx].speed
            if on_board[idx].y > 600:
                heart_cnt -= 1
                if not heart_cnt:
                    print("끝")
                    pygame.quit()
                del on_board[idx]
                continue
            screen.blit(on_board[idx].data,(on_board[idx].x,on_board[idx].y))
            idx += 1

        # 생명 보이기
        for i in range(heart_cnt):
            screen.blit(heart,(440+i*52,0))


        # 정답 칸
        targetRect = pygame.draw.rect(screen, WHITE, [200, 700, 200, 40])
        block = font.render(input_word, True, (255, 255, 161))
        rect = block.get_rect()
        rect.topleft = targetRect.topleft  # 왼쪽정렬


        # 타이머 효과
        screen.blit(timer, (0, 0))
        if seconds >= 60:
            minutes += 1
            seconds = 0
            if minutes >= 60:
                hour += 1
                minutes = 0


        pygame.display.update()
        clock.tick(10)



runGame()



