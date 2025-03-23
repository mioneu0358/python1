import os
from collections import deque
import random
import pygame
import sys

# -------------- 버튼 및 조이스틱 설정 ------------------
import spidev
import time
import RPi.GPIO as GPIO

swt_channel = 0
vrx_channel = 1
vry_channel = 2

delay = 0.1

spi = spidev.SpiDev()
spi.open(0, 0)  # bus=0, device=0
spi.max_speed_hz = 1000000  # SPI 속도 설정

button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)	# 풀업저항 할당

# ------------------------------------------------------


# Pygame 초기화
pygame.init()
screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("MY STRIKERS 1945")
clock = pygame.time.Clock()


# 현재 페이지 상태
current_page = 0

# 선택된 케릭터

# 시작 페이지 함수
def start_page():
    global current_page, font
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
        background = pygame.image.load("images/loading_page.png")
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


class Plane:
    def __init__(self, plane_image_path, x, y, speed, health, bullet_img):
        self.icon = pygame.image.load(plane_image_path).convert_alpha()   # 이미지 투명 처리
        self.icon.set_colorkey((255,255,255))
        self.width = self.icon.get_width()
        self.height = self.icon.get_height()
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.bullet_img =bullet_img
    def draw(self, screen):
        screen.blit(self.icon, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
    def shoot(self, target_x=None, target_y=None, speed=5):
        return Bullet(self.x, self.y, self.width, self.height, target_x, target_y, speed, image=self.bullet_img)



class Player(Plane):
    def __init__(self):
        super().__init__(f"images/{char_list[selected_char].replace('CHAR_', '')}",
                         screen.get_width()//2,
                         screen.get_height() - 60,
                         speed=5,
                         health=3,
                         bullet_img="images/player_bullet.png")

class Boss(Plane):
    def __init__(self):
        super().__init__("images/boss_syumi.png",
                         screen.get_width()//2 - 27,
                         0,
                         speed=3,
                         health=100,
                         bullet_img="images/enemy_bullet.png")
        self.movement = deque()

    def random_move(self):
        if self.movement:
            self.x += self.movement.popleft()
            if self.x < 0 or self.x + self.width > screen_width:
                self.movement.clear()
        else:
            direction = self.speed if random.randint(0, 1) else -self.speed
            self.movement.extend([direction] * random.randint(30, 40))

    def aim_and_shoot(self, player_x, player_y):
        return self.shoot(player_x, player_y, speed=5)  # 일정한 속도로 고정

class Bullet:
    def __init__(self, char_x, char_y, char_w, char_h, target_x=None, target_y=None, speed=5, image=''):
        self.icon = pygame.image.load(image).convert_alpha()
        self.icon.set_colorkey((255,255,255))
        self.width = self.icon.get_width()
        self.height = self.icon.get_height()
        self.x = char_x + (char_w // 2)
        self.y = char_y
        self.speed = speed

        if target_x is not None and target_y is not None:
            # 방향 벡터 계산
            dx = target_x - self.x
            dy = target_y - self.y
            length = (dx**2 + dy**2)**0.5
            self.mx = dx / length * speed
            self.my = dy / length * speed
        else:
            self.mx = 0
            self.my = -speed  # 기본 위로 발사

    def move(self):
        self.x += self.mx
        self.y += self.my

class Enemy(Plane):
    def __init__(self):
        super().__init__(f"images/enemy_a6m_zero.png",
                         random.randint(0, screen_width-50),
                         50,
                         speed=3,
                         health=1,
                         bullet_img="images/enemy_bullet.png")  # 한 방 맞으면 사망
        self.last_shot_time = pygame.time.get_ticks()  # 마지막 발사 시간 기록

    def move(self):
        self.y += self.speed  # 아래로 직선 이동

    def shoot(self):
        return Bullet(self.x, self.y, self.width, self.height, target_x=player.x + player.width // 2, target_y=player.y,
                      speed=3, image="images/enemy_bullet.png")


# 배경 스크롤을 위한 변수 추가
background = pygame.image.load("images/background1.png")
bg_y1 = 0
bg_y2 = -screen_height  # 두 번째 배경을 첫 번째 배경 위에 배치
def check_collision(bullet, target):
    bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
    target_rect = pygame.Rect(target.x, target.y, target.width, target.height)

    if bullet_rect.colliderect(target_rect):
        if isinstance(target, Player):
            print("플레이어 피격!")
            target.health -= 1  # 플레이어는 체력 1씩 감소
        elif isinstance(target, Boss):
            print("적이 맞았다!")
            target.health -= 10  # 적은 체력 10씩 감소
        return True  # 충돌 발생 (총알 삭제 대상)
    return False  # 충돌 없음

def update_background():
    global bg_y1, bg_y2
    bg_speed = 2  # 배경이 내려가는 속도

    # 배경 위치 이동
    bg_y1 += bg_speed
    bg_y2 += bg_speed

    # 배경이 완전히 화면 아래로 내려가면 다시 위로 보냄
    if bg_y1 >= screen_height:
        bg_y1 = -screen_height
    if bg_y2 >= screen_height:
        bg_y2 = -screen_height

def draw_background():
    screen.blit(background, (0, bg_y1))
    screen.blit(background, (0, bg_y2))

def get_movement(channel):
    val = spi.xfer2([1,(8+channel)<<4,0])
    # print(f"val:{val}")
    data = ((val[1] & 3) << 8) + val[2]
    return data



# 게임 실행 페이지에서 enemy의 추가 및 삭제 로직 수정
def game_execution_page():
    global player, font
    player = Player()
    boss = Boss()
    enemies = deque()  # 적들을 저장하는 리스트

    player_bullets = deque()
    enemy_bullets = deque()

    player_last_shot_time = pygame.time.get_ticks()
    enemy_last_shot_time = pygame.time.get_ticks()

    while True:
        update_background()
        # 적 스폰: 적이 6마리 이하일 때 랜덤하게 생성
        while len(enemies) < random.randint(1, 3):
            enemies.append(Enemy())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        dx, dy = 0, 0
        # if keys[pygame.K_LEFT]: dx -= 1
        # if keys[pygame.K_RIGHT]: dx += 1
        # if keys[pygame.K_UP]: dy -= 1
        # if keys[pygame.K_DOWN]: dy += 1
        # player.move(dx, dy)
        # JoyStick/test.py의 내용 연결하기
        
        vrx_pos = get_movement(vrx_channel)
        # 100이하면 왼쪽, 900이상이면 오른쪽 
        vry_pos = get_movement(vry_channel)
        # 100이하면 위, 900이상이면 아래   
        swt_val = get_movement(swt_channel)
        # 일단 패스 나중에 궁극기 같은거로 판단
        if vrx_pos <= 200:
            dx -= 1
        elif vrx_pos >= 800:
            d += 1
            
        if vry_pos <= 200:
            dy -= 1
        elif vry_pos >= 800:
            dy += 1
        player.move(dx,dy)
    
        player.x = max(0, min(screen_width - player.width, player.x))
        player.y = max(0, min(screen_height - player.height, player.y))


        # 플레이어 총알 발사
        if GPIO.input(button_pin) == GPIO.LOW:
            now = pygame.time.get_ticks()
            if now - player_last_shot_time >= 300:
                player_bullets.append(player.shoot())
                player_last_shot_time = now

        now = pygame.time.get_ticks()

        # 보스 총알 발사
        if now - enemy_last_shot_time >= random.randint(300, 500):
            enemy_bullets.append(boss.aim_and_shoot(player.x + player.width // 2, player.y + player.height // 2))
            enemy_last_shot_time = now

        # 적 총알 발사 보스 보다 느리게
        for enemy in enemies:
            if now - enemy.last_shot_time >= random.randint(1500, 3000):  # 보스보다 느리게 발사
                enemy_bullets.append(enemy.shoot())
                enemy.last_shot_time = now

        # 적 이동 및 화면 밖 제거
        enemies = deque([e for e in enemies if e.move() or e.y < screen_height])

        # 총알 이동
        player_bullets = deque([b for b in player_bullets if b.move() or b.y >= 0])
        enemy_bullets = deque([b for b in enemy_bullets if b.move() or b.y <= screen_height])

        # 충돌 체크 (플레이어 총알 → 적)
        player_bullets = deque([
            bullet for bullet in player_bullets
            if not check_collision(bullet, boss)
        ])

        # 충돌 체크 (플레이어 총알 → 일반 적)
        new_enemies = deque()
        for enemy in enemies:
            hit = False
            for bullet in list(player_bullets):
                if check_collision(bullet, enemy):
                    hit = True
                    player_bullets.remove(bullet)
                    break
            if not hit:
                new_enemies.append(enemy)
        enemies = new_enemies

        # 충돌 체크 (적 총알 → 플레이어)
        enemy_bullets = deque([
            bullet for bullet in enemy_bullets
            if not check_collision(bullet, player)
        ])

        if boss.health <= 0:
            print("적 처치 완료!")
            while True:
                victory = font.render(f"ViCTORY\nContinue?(Y/N)", True, (255, 255, 255))
                screen.blit(victory, (50,300))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            current_page = -1
                            return
                        elif event.key == pygame.K_n:
                            exit()


        if player.health <= 0:
            print("플레이어 사망! 게임 오버!")
            while True:
                fail = font.render(f"Fail\nContinue?(Y/N)", True, (255, 255, 255))
                screen.blit(fail, (0,0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            current_page = -1
                            return
                        elif event.key == pygame.K_n:
                            exit()

        draw_background()
        boss.random_move()
        boss.draw(screen)
        player.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        for bullet in player_bullets:
            screen.blit(bullet.icon, (bullet.x, bullet.y))

        for bullet in enemy_bullets:
            screen.blit(bullet.icon, (bullet.x, bullet.y))

        font = pygame.font.SysFont(None, 36)
        hp_text = font.render(f"Player HP: {player.health}", True, (255, 255, 255))
        boss_hp_text = font.render(f"Boss HP: {boss.health}", True, (255, 0, 0))
        screen.blit(hp_text, (20, 20))
        screen.blit(boss_hp_text, (20, 50))

        pygame.display.flip()
        clock.tick(60)

# 수정된 충돌 함수 (player도 처리)





def end_page():
    return


page_func = [start_page,character_selection_page, game_execution_page]
# 메인 루프: 현재 페이지에 따라 해당 함수를 호출
while True:
    page_func[current_page % 3]()
    current_page += 1
