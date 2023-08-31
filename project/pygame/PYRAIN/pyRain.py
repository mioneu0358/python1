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
game_font = pygame.font.SysFont('arial', 30, True, False)


background = pygame.image.load("background.png")
heart = pygame.image.load("heart.png")
pygame.display.set_caption("타자연습 산성비")




# 타이머에 사용할 분,초,밀리초
on_board = []


def runGame():
    word_list = get_word_list()
    heart_cnt = 3
    input_word = ""

    FPS = 30  # FPS(Frame per Seconds)
    screen_size = (600, 800)
    screen = pygame.display.set_mode(screen_size)

    clock = pygame.time.Clock()
    level = 1
    run_status = True
    minutes = 0
    seconds = 0
    hour = 0

    def PAUSE():
        pause = True
        pause_font = pygame.font.SysFont('arial',100, True, False)
        pause_Title = pause_font.render("PAUSE", True, RED)
        pause_Rect = text_Title.get_rect()
        pause_Rect.centerx = round(screen_size[0] / 2) - 150
        pause_Rect.y = round(screen_size[1] / 2) - 200
        screen.blit(pause_Title,pause_Rect)
        while pause:
            for evt in pygame.event.get():
                if evt.type == pygame.KEYDOWN:
                    pause = False
            pygame.display.update()


    while run_status:
        print(f"input_word: {input_word}")

        screen.blit(background, (0, 0))
        text_Rect_bg = pygame.Rect(210,700,180,50)
        pygame.draw.rect(screen,WHITE,text_Rect_bg)
        # 입력창에 글 쓰기
        text_Title = game_font.render(input_word, True, BLACK)
        text_Rect = text_Title.get_rect()
        text_Rect.centerx = round(screen_size[0] / 2)
        text_Rect.y = 700
        print(text_Rect.x, text_Rect.y, text_Rect.width, text_Rect.height)

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
                # Backspace처리
                elif event.key == pygame.K_BACKSPACE:
                    input_word = input_word[:-1]
                elif event.key == pygame.K_ESCAPE:
                    PAUSE()
                # 타이핑 처리
                else:
                    input_word += event.unicode
        screen.blit(text_Title,text_Rect)
    # 단어 만들기
        if not on_board:
            while len(on_board) < 15:
                idx = random.randint(0,len(word_list)-1)
                x = random.randint(0,500)
                speed = random.randint(0,40) / 10
                word = Word(game_font.render(word_list[idx],True,(BLACK)),word_list[idx],x,50,speed)
                on_board.append(word)
    # 속도 조절
        idx = 0
        while idx < len(on_board):
            on_board[idx].y += on_board[idx].speed
            # 단어 충돌처리
            if on_board[idx].y > 650:
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

        # 타이머 효과
        screen.blit(timer, (0, 0))
        if seconds >= 60:
            minutes += 1
            seconds = 0
            if minutes >= 60:
                hour += 1
                minutes = 0


        pygame.display.update()
        # 게임 속도
        clock.tick(20 + (level * 5))



runGame()



