import os

import pygame
import sys

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("mySTRIKERS 1945")
clock = pygame.time.Clock()


# 현재 페이지 상태
current_page = 0

# 선택된 케릭터
selected_char = 0

# 시작 페이지 함수
def start_page():
    global current_page
    blink = True
    last_blink_time = pygame.time.get_ticks()  # 마지막 깜빡임 시간 기록
    blink_interval = 500  # 깜빡임 간격 (밀리초 단위, 500ms = 0.5초)
    while True:
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time > blink_interval:
            blink = not blink
            last_blink_time = current_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 예: 스페이스바를 누르면 캐릭터 선택 페이지로 전환
            if event.type == pygame.KEYDOWN:
                return

        screen.fill((0, 0, 0))  # 배경 검정색
        background = pygame.image.load("images/background1.png")
        screen.blit(background, (0, 0))
        if blink:
            font = pygame.font.SysFont(None, 48)
            text = font.render("Press any key to start", True, (255, 255, 255))
            screen.blit(text, (screen.get_width() // 2 - 180, screen.get_height() // 3 * 2))
        pygame.display.flip()
        clock.tick(60)

select_sec = 60
char_list = list(filter(lambda x: x.startswith("Char"), os.listdir("images")))
print(char_list)
# 캐릭터 선택 페이지 함수
def character_selection_page():
    global current_page
    global selected_char
    global select_sec
    blink = True
    last_blink_time = pygame.time.get_ticks()  # 마지막 깜빡임 시간 기록
    blink_interval = 1000  # 깜빡임 간격 (밀리초 단위, 500ms = 0.5초)
    while True:
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time > blink_interval:
            select_sec -= 1
            blink = not blink
            last_blink_time = current_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 예: 스페이스바를 누르면 게임 실행 페이지로 전환
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_LEFT:
                    selected_char -= 1
                    if selected_char < 0:
                        selected_char = 3
                elif event.key == pygame.K_RIGHT:
                    selected_char += 1
                    if selected_char > 3:
                        selected_char = 0


        screen.fill((50, 50, 50))  # 배경 회색
        font = pygame.font.SysFont(None, 48)
        text = font.render("Press SPACE to Select", True, (255, 255, 255))
        screen.blit(pygame.image.load(f"images/{char_list[selected_char]}"),(0,0))
        if blink:
            text_sec = font.render(f"{select_sec}", True, (255, 255, 255))
            screen.blit(text_sec, (800,600))
        screen.blit(text, (50, 600))
        pygame.display.flip()
        clock.tick(60)


# 게임 실행 페이지 함수
def game_execution_page():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((100, 100, 100))  # 배경 진회색
        font = pygame.font.SysFont(None, 48)
        text = font.render("게임 실행 중...", True, (255, 255, 255))
        screen.blit(text, (150, 220))
        pygame.display.flip()
        clock.tick(60)


def end_page():
    pass
page_func = [start_page,character_selection_page, game_execution_page, end_page]
# 메인 루프: 현재 페이지에 따라 해당 함수를 호출
while True:
    page_func[current_page]()
    current_page += 1

