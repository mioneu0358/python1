import os
from collections import deque
import random
import pygame
import sys

# Pygame 초기화
pygame.init()
screen_width =1080
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("MY STRIKERS 1945")
clock = pygame.time.Clock()


# 현재 페이지 상태
current_page = 0

# 선택된 케릭터

# 시작 페이지 함수
def start_page():
    global current_page
    blink = True
    last_blink_time = pygame.time.get_ticks()  # 마지막 깜빡임 시간 기록
    blink_interval = 500  # 깜빡임 간격 (밀리초 단위, 500ms = 0.5초)
    while True:
        player_current_time = pygame.time.get_ticks()
        if player_current_time - last_blink_time > blink_interval:
            blink = not blink
            last_blink_time = player_current_time
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


char_list = list(filter(lambda x: x.startswith("CHAR"), os.listdir("images")))
selected_char = 0
# 캐릭터 선택 페이지 함수
def character_selection_page():
    print("비행기 선택")
    select_sec = 60

    global current_page
    global selected_char
    blink = True
    last_blink_time = pygame.time.get_ticks()  # 마지막 깜빡임 시간 기록
    blink_interval = 500  # 깜빡임 간격 (밀리초 단위, 500ms = 0.5초)
    while True:
        player_current_time = pygame.time.get_ticks()
        if player_current_time - last_blink_time > blink_interval:
            select_sec -= 0.5
            blink = not blink
            last_blink_time = player_current_time
            if select_sec == 0:
                return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 예: 스페이스바를 누르면 게임 실행 페이지로 전환
            if event.type == pygame.KEYDOWN:
                print(event.key)
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
            text_sec = font.render(f"{int(select_sec)}", True, (255, 255, 255))
            screen.blit(text_sec, (800,600))
        screen.blit(text, (50, 600))
        pygame.display.flip()
        clock.tick(60)

class Bullet:
    def __init__(self,char_x,char_y,char_w, char_h,mx,my):
        self.icon = pygame.image.load("images/bullet.png")
        self.width = self.icon.get_width()
        self.height = self.icon.get_height()
        self.x = char_x+(char_w // 2)
        self.y = char_y
        self.speed = 5
        self.mx = mx
        self.my = my

    def move(self):
        self.x += self.mx * self.speed
        self.y += self.my * self.speed



class Charcter:
    def __init__(self):
        self.selected_char = selected_char
        self.health = 3
        self.icon = pygame.image.load(f"images/{char_list[selected_char].replace('CHAR_','')}")   # 55 x 40
        self.width = self.icon.get_width()
        self.height = self.icon.get_height()
        self.x = screen.get_width()//2-self.width
        self.y = screen.get_height()-self.height
        self.speed = 5

    def shoot(self):
        bullet = Bullet(self.x,self.y,self.width,self.height,0,-1)
        return bullet

    def ult(self):
        pass


class Enemy:
    def __init__(self):
        self.selected_char = selected_char
        self.health = 100
        self.icon = pygame.image.load(f"images/enemy_syumi.png")   # 55 x 40
        self.width = self.icon.get_width()
        self.height = self.icon.get_height()
        self.x = (screen.get_width()//2)-(self.width//2)
        self.y = 0
        self.speed = 3
        self.dir_ = -1
        self.movement = deque()

    def shoot(self):
        bullet = Bullet(self.x,self.y+self.height,self.width,self.height,0,1)
        return bullet

    def random_move(self):
        if self.movement:
            self.x += self.movement.popleft()
            if self.x < 0:
                self.x = 0
                self.movement.clear()
            elif self.x + self.width > screen_width:
                self.x = screen_width - self.width
                self.movement.clear()

        else:
            random_move = self.speed if random.randint(0,1)  else -self.speed
            for _ in range(random.randint(30,40)):
                self.movement.append(random_move)


    def ult(self):
        pass


# 게임 실행 페이지 함수
def game_execution_page():
    char = Charcter()
    boss = Enemy()
    player_bullet_info = deque()  # 총알 정보를 저장하는 큐
    enemy_bullet_info = deque()
    # 마지막 총알 발사 시간 초기화
    player_last_shot_time = pygame.time.get_ticks()
    player_fire_rate = 300  # 발사 간격을 300ms (0.3초)로 설정
    enemy_last_shot_time = pygame.time.get_ticks()
    enemy_fire_rate = random.randint(200,400)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # x, y 축 이동 (대각선 이동을 고려하여 속도 분배)
        if keys[pygame.K_LEFT]:
            char.x -= char.speed
        if keys[pygame.K_RIGHT]:
            char.x += char.speed
        if keys[pygame.K_UP]:
            char.y -= char.speed
        if keys[pygame.K_DOWN]:
            char.y += char.speed

        # 캐릭터 화면 밖으로 나가는 작업 방지
        if char.x < 0: char.x = 0
        elif char.x + char.width > screen_width: char.x = screen_width-char.width
        if char.y < 0: char.y = 0
        elif char.y + char.height > screen_height: char.y = screen_height - char.height

        # 'a' 키를 눌렀을 때 총알 발사, 발사 간격을 체크
        if keys[pygame.K_a]:
            player_current_time = pygame.time.get_ticks()  # 현재 시간
            if player_current_time - player_last_shot_time >= player_fire_rate:  # 발사 간격 체크
                bullet = char.shoot()
                player_bullet_info.append(bullet)  # 총알을 큐에 추가
                player_last_shot_time = player_current_time  # 마지막 발사 시간을 현재 시간으로 갱신

        # 총알 이동 (y축으로 이동)
        for _ in range(len(player_bullet_info)):
            bullet = player_bullet_info.popleft()  # 큐에서 하나씩 가져옴
            bullet.move()                          # 총알을 위로 이동
            if bullet.y >= 0:                      # 화면 밖으로 나가지 않도록
                player_bullet_info.append(bullet)  # 총알이 화면에 남아 있으면 큐에 다시 추가


        enemy_current_time = pygame.time.get_ticks()  # 현재 시간
        if enemy_current_time - enemy_last_shot_time >= enemy_fire_rate:  # 발사 간격 체크
            bullet = boss.shoot()
            enemy_bullet_info.append(bullet)  # 총알을 큐에 추가
            enemy_last_shot_time = enemy_current_time  # 마지막 발사 시간을 현재 시간으로 갱신

        for _ in range(len(enemy_bullet_info)):
            bullet = enemy_bullet_info.popleft()  # 큐에서 하나씩 가져옴
            bullet.move()  # 총알을 아래로
            if bullet.y <= screen_height:  # 화면 밖으로 나가지 않도록
                player_bullet_info.append(bullet)  # 총알이 화면에 남아 있으면 큐에 다시 추가



        # 화면을 채우기 전에 배경을 그리기
        screen.fill((100, 100, 100))  # 배경 진회색

        # 캐릭터와 총알을 화면에 그리기
        boss.random_move()
        screen.blit(boss.icon, (boss.x,boss.y))
        screen.blit(char.icon, (char.x, char.y))
        for bullet in player_bullet_info:
            screen.blit(bullet.icon, (bullet.x, bullet.y))

        pygame.display.flip()
        clock.tick(60)

def end_page():
    pass
page_func = [start_page,character_selection_page, game_execution_page, end_page]
# 메인 루프: 현재 페이지에 따라 해당 함수를 호출
while True:
    page_func[current_page]()
    current_page += 1

