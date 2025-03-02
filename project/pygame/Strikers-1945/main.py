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


class Plane:
    def __init__(self, image_path, x, y, speed, health):
        self.icon = pygame.image.load(image_path)
        self.width = self.icon.get_width()
        self.height = self.icon.get_height()
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health

    def draw(self, screen):
        screen.blit(self.icon, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def shoot(self, target_x=None, target_y=None, speed=5):
        return Bullet(self.x, self.y, self.width, self.height, target_x, target_y, speed)

class Player(Plane):
    def __init__(self):
        super().__init__(f"images/{char_list[selected_char].replace('CHAR_', '')}",
                         screen.get_width()//2,
                         screen.get_height() - 60,
                         speed=5,
                         health=3)

class Enemy(Plane):
    def __init__(self):
        super().__init__("images/enemy_syumi.png",
                         screen.get_width()//2 - 27,
                         0,
                         speed=3,
                         health=100)
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
    def __init__(self, char_x, char_y, char_w, char_h, target_x=None, target_y=None, speed=5):
        self.icon = pygame.image.load("images/bullet.png")
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

def game_execution_page():
    global char
    char = Player()
    boss = Enemy()
    player_bullets = deque()
    enemy_bullets = deque()

    player_last_shot_time = pygame.time.get_ticks()
    enemy_last_shot_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx -= 1
        if keys[pygame.K_RIGHT]: dx += 1
        if keys[pygame.K_UP]: dy -= 1
        if keys[pygame.K_DOWN]: dy += 1
        char.move(dx, dy)

        char.x = max(0, min(screen_width - char.width, char.x))
        char.y = max(0, min(screen_height - char.height, char.y))

        if keys[pygame.K_a]:
            now = pygame.time.get_ticks()
            if now - player_last_shot_time >= 300:
                player_bullets.append(char.shoot())
                player_last_shot_time = now

        now = pygame.time.get_ticks()
        if now - enemy_last_shot_time >= random.randint(300, 500):
            enemy_bullets.append(boss.aim_and_shoot(char.x + char.width // 2, char.y + char.height // 2))
            enemy_last_shot_time = now

        player_bullets = deque([b for b in player_bullets if b.move() or b.y >= 0])
        enemy_bullets = deque([b for b in enemy_bullets if b.move() or b.y <= screen_height])

        # 🔥 충돌 체크 (플레이어 총알 → 적)
        player_bullets = deque([
            bullet for bullet in player_bullets
            if not check_collision(bullet, boss)
        ])

        # 🔥 충돌 체크 (적 총알 → 플레이어)
        enemy_bullets = deque([
            bullet for bullet in enemy_bullets
            if not check_collision(bullet, char)
        ])

        if boss.health <= 0:
            print("적 처치 완료!")
            return

        if char.health <= 0:
            print("플레이어 사망! 게임 오버!")
            return  # 게임 오버 처리 (end_page로 연결 가능)

        screen.fill((100, 100, 100))
        boss.random_move()
        boss.draw(screen)
        char.draw(screen)

        for bullet in player_bullets:
            screen.blit(bullet.icon, (bullet.x, bullet.y))

        for bullet in enemy_bullets:
            screen.blit(bullet.icon, (bullet.x, bullet.y))

        # 체력 표시 (옵션)
        font = pygame.font.SysFont(None, 36)
        hp_text = font.render(f"Player HP: {char.health}", True, (255, 255, 255))
        boss_hp_text = font.render(f"Enemy HP: {boss.health}", True, (255, 0, 0))
        screen.blit(hp_text, (20, 20))
        screen.blit(boss_hp_text, (20, 50))

        pygame.display.flip()
        clock.tick(60)

# 수정된 충돌 함수 (player도 처리)
def check_collision(bullet, target):
    bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
    target_rect = pygame.Rect(target.x, target.y, target.width, target.height)

    if bullet_rect.colliderect(target_rect):
        if isinstance(target, Player):
            print("플레이어 피격!")
            target.health -= 1  # 플레이어는 체력 1씩 감소
        elif isinstance(target, Enemy):
            print("적이 맞았다!")
            target.health -= 10  # 적은 체력 10씩 감소
        return True  # 충돌 발생 (총알 삭제 대상)

    return False  # 충돌 없음




def end_page():
    pass
page_func = [start_page,character_selection_page, game_execution_page, end_page]
# 메인 루프: 현재 페이지에 따라 해당 함수를 호출
while True:
    page_func[current_page]()
    current_page += 1

