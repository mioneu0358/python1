import pygame, random
from datetime import datetime
from datetime import timedelta
from perceptron import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20


RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)


pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



def draw_background(screen):
    background = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, WHITE, background)


def draw_block(screen, color, position):
    block = pygame.Rect(
        (position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE),
        (BLOCK_SIZE, BLOCK_SIZE)
    )
    pygame.draw.rect(screen, color, block)


def draw_lines(screen, color):
    for i in range(int(SCREEN_WIDTH / 20)):
        pygame.draw.line(screen, color, (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, SCREEN_HEIGHT), 1)
        pygame.draw.line(screen, color, (0, i * BLOCK_SIZE), (SCREEN_WIDTH, i * BLOCK_SIZE), 1)



class Offset:
    NONE = [0, 0]
    RIGHT = [1, 0]
    LEFT = [-1, 0]
    UP = [0, -1]
    DOWN = [0, 1]



class Snake:
    def __init__(self, color, position, offset):
        self.color = color
        self.offset = offset
        self.positions = [
            position,
            [position[0], position[1] + 1],
            [position[0], position[1] + 2],
            [position[0], position[1] + 3]
        ]
        # TODO: Snake 에 지능을 주자
        self.neural_network = NeuralNetwork(6, 30, 3)

    def draw(self):
        for position in self.positions:
            draw_block(screen, self.color, position)

    def move(self):
        now_position = [self.positions[0][0], self.positions[0][1]]
        self.positions[0][0] += self.offset[0]
        self.positions[0][1] += self.offset[1]
        last_position = now_position
        for i in range(1, len(self.positions)):
            now_position = [self.positions[i][0], self.positions[i][1]]
            self.positions[i] = last_position
            last_position = now_position

    def growth(self):
        end_tail = self.positions[-1]
        front_tail = self.positions[-2]

        Xdiff = end_tail[0] - front_tail[0]
        Ydiff = end_tail[1] - front_tail[1]
        self.positions.append([end_tail[0] + Xdiff, end_tail[1] + Ydiff])

    # TODO: 현재 방향을 기준으로 전방, 좌측, 우측 Offset을 리턴하는 함수
    def getDriection(self):
        # 리턴 값은 [Front, Left, Right]
        if self.offset == Offset.UP:
            return [Offset.UP, Offset.LEFT, Offset.RIGHT]
        elif self.offset == Offset.DOWN:
            return [Offset.DOWN, Offset.RIGHT, Offset.LEFT]
        elif self.offset == Offset.LEFT:
            return [Offset.LEFT, Offset.DOWN, Offset.UP]
        else:
            return [Offset.RIGHT, Offset.UP, Offset.DOWN]

    # TODO: 현재 방향을 기준으로 장애물을 감지하고 센서값을 리턴하는 함수
    def obstacleSensor(self):
        ob_sensor = [1.0, 1.0, 1.0]      # 전방, 좌측, 우측의 감지 결과
        direction = self.getDriection()  # 현재 방향을 기준으로 [앞, 왼, 오]

        head = list(self.positions[0])   # 현재 뱀 머리의 위치
        for i in range(3):
            for j in range(1, 6):
                if not (20 > head[0] + direction[i][0] * j >= 0
                        and 20 > head[1] + direction[i][1] * j >= 0):
                    ob_sensor[i] -= 0.2
                elif True:  # 뱀꼬리를 감지하는 경우
                    pass
        return ob_sensor

    # TODO: 현재 방향을 기준으로 사과가 놓인 방향을 감지하고 리턴하는 함수
    def appleSensor(self, applePos):
        direction = self.getDriection()
        # 뱀이 향하고 있는 방향을 기준으로 사과의 위치를 감지한다.
        # [FORWARD, LEFT, RIGHT] 중 하나만 1.0 나머지 0.0

        fbeam = list(self.positions[0])
        while 0 <= fbeam[0] < 20 and 0 <= fbeam[1] < 20:
            # fbeam을 direction front만큼 증가시키고 사과의 위치와 일치하는지 감지
            # 한번 증가후 lbeam과 rbeam도 while문을 통해 좌우로 감지
            # 사과를 발견하거나 모두 탐색할때까지 반복
            fbeam[0] += direction[0][0]
            fbeam[1] += direction[0][1]
            if fbeam == applePos:
                return [1.0, 0.0, 0.0]

            lbeam = list(fbeam)
            while 0 <= lbeam[0] < 20 and 0 <= lbeam[1] < 20:
                if lbeam == applePos:
                    return [0.0, 1.0, 0.0]
                lbeam[0] += direction[1][0]
                lbeam[1] += direction[1][1]
            rbeam = list(fbeam)
            while 0 <= rbeam[0] < 20 and 0 <= rbeam[1] < 20:
                if rbeam == applePos:
                    return [0.0, 0.0, 1.0]
                rbeam[0] += direction[2][0]
                rbeam[1] += direction[2][1]
            pass
        return [0.0, 0.0, 0.0]

    # TODO: 신경망의 결과값을 보고 다음 이동 Offset 을 정해주는 함수
    def setOffset(self, output):
        direction = self.getDriection()
        self.offset = direction[np.argmax(output)]

class Apple:

    def __init__(self, color, position):
        self.color = color
        self.position = position

    def draw(self):
        draw_block(screen, self.color, self.position)

    pass



class Game:
    def __init__(self, snake, apple):
        self.snake = snake
        self.apple = apple
        # TODO: 게임 점수와 타이머
        self.score = 0
        self.timer = 50

    def draw(self):
        draw_background(screen)
        self.apple.draw()
        self.snake.draw()
        pygame.display.update()

    def isCrashed(self):
        snake_head = self.snake.positions[0]

        if snake_head in self.snake.positions[1:]:
            return True

        if snake_head[0] > 19 or snake_head[1] > 19 or snake_head[0] < 0 or snake_head[1] < 0:
            return True
        return False

    def start(self):
        last_movement = datetime.now()
        move_flag = True
        # TODO: 마지막에 발생한 input 값
        last_input = []
        # TODO: 마지막에 발생한 output 값
        last_output = []
        # TODO: 사과를 먹은 경우에 대한 성공 리스트
        eat_list = []
        # TODO: 매턴 생존한 경우에 대한 성공 리스트
        live_list = []
        # TODO: 게임 속도 조절
        time_speed = 1
        # TODO: 학습횟수 및 최고점수
        train_cnt = 0
        max_score = 0
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN and move_flag:
                    move_flag = False
                    if event.key == pygame.K_RIGHT and self.snake.offset != Offset.LEFT:
                        self.snake.offset = Offset.RIGHT
                    elif event.key == pygame.K_LEFT and self.snake.offset != Offset.RIGHT:
                        self.snake.offset = Offset.LEFT
                    elif event.key == pygame.K_DOWN and self.snake.offset != Offset.UP:
                        self.snake.offset = Offset.DOWN
                    elif event.key == pygame.K_UP and self.snake.offset != Offset.DOWN:
                        self.snake.offset = Offset.UP
                    # TODO: 게임 속도 조절
                    elif event.key == pygame.K_w:
                        time_speed = time_speed - 1 if not time_speed == 1 else 1
                    elif event.key == pygame.K_s:
                        time_speed = time_speed + 1 if not time_speed == 300 else 30

            if timedelta(milliseconds=time_speed) <= datetime.now() - last_movement:
                # TODO: 타이머 감소
                self.timer -= 1

                # TODO: 생존한 경우 생존 리스트에 마지막 input과 output 세트를 삽입
                if len(last_input) != 0 and len(last_output) != 0:
                    output = [0.0, 0.0, 0.0]
                    output[np.argmax(last_output)] = 1.0
                    live_list.insert(0, [last_input, output])

                # TODO: 신경망의 input 값 생성
                input1 = self.snake.obstacleSensor()
                input2 = self.snake.appleSensor(self.apple.position)
                last_input = input1 + input2
                # TODO: input 값을 통해 신경망에 질의
                last_output = self.snake.neural_network.query(last_input)

                # TODO: output 값을 보고 다음 이동방향 결정
                self.snake.setOffset(last_output)

                move_flag = True
                self.snake.move()
                last_movement = datetime.now()
            if self.apple.position == self.snake.positions[0]:
                # TODO: 점수 증가, 타이머 증가
                self.score += 1
                self.timer += 50

                # TODO: 사과를 먹은 경우 마지막 input 과 output 을 eat_list 에 삽입
                output = [0.0, 0.0, 0.0]
                output[np.argmax(last_output)] = 1.0
                eat_list.insert(0, [last_input, output])

                while self.apple.position in self.snake.positions:
                    self.apple.position = [random.randint(0, 19), random.randint(0, 19)]
                self.snake.growth()
            if self.isCrashed() or self.timer == 0:
                # TODO: 점수가 0점이면 마지막 input 에 대해 랜덤 output 학습
                if self.score == 0:
                    for i in range(10):
                        output = [0.0, 0.0, 0.0]
                        output[random.randint(0, 2)] = 1.0
                        self.snake.neural_network.train(last_input, output, 0.1)
                # TODO: 0점이 아니고 충돌로 죽었다면 live_list 학습
                elif self.isCrashed():
                    for io in live_list:
                        self.snake.neural_network.train(io[0], io[1], 0.01)

                # TODO: eat_list에 값이 하나라도 존재하면 학습
                for io in eat_list:
                    self.snake.neural_network.train(io[0], io[1], 0.02)

                # TODO: 리스트들 비우기
                last_input = []
                last_output = []
                live_list = []

                # TODO: 학습 횟수 증가하고 최대 점수 출력
                train_cnt += 1
                if max_score < self.score:
                    print("{}회 학습중 최고 점수 {}".format(train_cnt, self.score))
                    max_score = self.score

                # TODO: 죽었을때 init 함수 호출
                head = [9, 9]
                self.snake.offset = Offset.UP
                self.snake.positions = [
                    head,
                    [head[0], head[1] + 1],
                    [head[0], head[1] + 2],
                    [head[0], head[1] + 3]
                ]
                self.apple.position = [random.randint(0, 19), random.randint(0, 19)]
                while self.apple.position in self.snake.positions:
                    self.apple.position = [random.randint(0, 19), random.randint(0, 19)]
                self.__init__(self.snake, self.apple)

            self.draw()

game = Game(Snake(GREEN, [9,9], Offset.UP), Apple(RED, [5,5]))
game.start()
