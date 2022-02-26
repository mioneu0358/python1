
import pygame
from datetime import timedelta
from datetime import datetime
import random

#스크린과 한 픽셀의 크기 정의

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20     #화면 크기의 픽셀을 정의

#뱀 게임에서 사용할 색상을 정의
#rgb의 단위가 255인 이유 = 1byte가 표현할수 있는 최대 수가 255이기때문
RED = (255,0,0)         #사과에 사용할 색상
GREEN = (0,255,0)       #뱀에 사용할 색상
WHITE = (255,255,255)   #배경에 사용할 색상
GRAY = (127,127,127)

#초기화
pygame.init()

#screen생성
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#배경 그리는 함수정의
def draw_background(screen):
    #좌표상의 직사각형 공간을 정의후  draw.rect를 통해 그린다.
    background = pygame.Rect((0,0),(SCREEN_WIDTH,SCREEN_HEIGHT))  #ball을  ballrect에 넣을때처럼 배경도 넣어줘야한다
    pygame.draw.rect(screen,WHITE,background)

#블록(픽셀)을 그리는 함수 정의
def draw_block(screen,color,position):
    block = pygame.Rect(
        (position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE),
        (BLOCK_SIZE,BLOCK_SIZE)
    )
    pygame.draw.rect(screen,color, block)

# 뱀이 움직이는 방향에 대한 오프셋
class Offset:
    NONE = [0,0]
    RIGHT = [1,0]
    LEFT = [-1,0]
    UP = [0,-1]
    DOWN = [0,1]

    #뱀의 위치와 방향 색을 정의하는 클래스
class Snake:
    #생성시 뱀의 색상과 위치, 초기에 움직일 방향을 입력
    def __init__(self,color,position, offset):
        self.color = color
        self.offset = offset
        #머리~꼬리의 위치들
        self.positions = [
            position,
            [position[0], position[1] + 1],
            [position[0], position[1] + 2],
            [position[0], position[1] + 3]
       ]
    #뱀을 그리는 함수
    def draw(self):
        for position in self.positions:
            draw_block(screen, self.color, position)

    #뱀을 움직이는 함수 - 꼬리가 머리를 따라가는 함수
    def move(self):
        #현재 위치를 기억
        now_pos  = [self.positions[0][0],self.positions[0][1]]
        #머리를 오프셋 만큼 이동
        self.positions[0][0] += self.offset[0]
        self.positions[0][1] += self.offset[1]
        #마지막 위치를 기억
        last_pos = now_pos
        for i in range(1, len(self.positions)):
            now_pos = self.positions[i][0],self.positions[i][1]   # now_pos는 i번쨰 position의 위치를 바인딩
            self.positions[i] = last_pos                        #움직일 i번째 position은 last_pos으로 이동
            last_pos = now_pos                                  #다시 last_pos는 now_pos를 바인딩
    #뱀의 꼬리 길이를 한칸 늘리는 함수
    def grow(self):
        self.positions.append([self.positions[-1][0],self.positions[-1][1]])    #늘어날 자리는 뱀의 꼬리 위치 - 뱀이 이동하면서

#뱀의 먹이(점수)인 사과의 색과 위치를 정의하는 클래스
class Apple:
    # 생성시 사과의 위치와 색상을 입력한다
    def __init__(self,color, position):
        self.color = color
        self.position = position

    def draw(self):
        draw_block(screen, self.color, self.position)
    #사과를 랜덤한 위치로 이동하시키는 함수

    def random_move(self):
        self.position = [random.randint(0,19),random.randint(0,19)]

#게임을 정의하는 클래스
class  Game:
    # 생성시 뱀과사과의 인스턴스를 생성한다
    def __init__(self):
        self.snake = Snake(GREEN,[9,9],Offset.NONE)
        self.apple = Apple(RED,[3,3])
    #배경과 생성된 인스턴스를 그리는 함수    배경보다 뱀을 먼저 그리면 배경이 뱀을 가려버림
    def draw(self):
         draw_background(screen)
         self.snake.draw()
         self.apple.draw()
         pygame.display.update()        #그려진 재용이 반영되도록 업데이트한다 (필수)

    #게임을 진행하는 함수
    def Start(self):
        last_movement = datetime.now()  #시간이 흐름을 표현하기 위해 만든 변수 (뱀의 움직임을 표현할때 사용)
        keydown_flag = False #키가 눌린상태인지 확인하는 플래그

        while True:
            events = pygame.event.get() #게임의 이벤트 현상을 받는다
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

                elif event.type == pygame.KEYDOWN and not keydown_flag:
                    if event.key == pygame.K_RIGHT and self.snake.offset != Offset.LEFT:
                        self.snake.offset = Offset.RIGHT
                        keydown_flag = True
                    elif event.key == pygame.K_LEFT and self.snake.offset != Offset.RIGHT:
                        self.snake.offset = Offset.LEFT
                        keydown_flag = True
                    elif event.key == pygame.K_DOWN and self.snake.offset != Offset.UP:
                        self.snake.offset = Offset.DOWN
                        keydown_flag = True
                    elif event.key == pygame.K_UP and self.snake.offset != Offset.DOWN:
                        self.snake.offset = Offset.UP
                        keydown_flag = True


                if self.snake.positions[0] in self.apple.position:
                    self.apple.random_move()
                    self.snake.grow()

                # TODO: 뱀이 꼬리나 벽에 충돌했을때 처리
                if self.snake.positions[0] == self.snake.positions[-1]:
                    exit()



            if timedelta(milliseconds=300) <= datetime.now() - last_movement:       #timedelta <= 시간의 간격(현재시각 - 지난시각)
                self.snake.move()
                last_movement = datetime.now()
                keydown_flag = False

            self.draw() #게임의 모든 인스턴스를 그린다

game = Game()
game.Start()
