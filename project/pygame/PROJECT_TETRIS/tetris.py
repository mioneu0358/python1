import time
import pygame
import sys
import random
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
move_interval = 0.05
spint_interval = 0.3
# ================================================SETTING===============================================================
SCREEN_WIDTH = BLOCK_SIZE * BOARD_WIDTH
SCREEN_HEIGHT =  BLOCK_SIZE * BOARD_HEIGHT
BG_COLOR = (0,0,0)
GRID_COLOR = (70,70,70)
color = {'PUPPLE' : (163,73,164), 'BLUE' : (0,0,255), 'RED':(255,0,0), 'WHITE':(200,200,200), 'CYAN':(0,230,230)}
# ================================================TEtroMinO============================================================
class Tetromino:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
    def draw(self, surface):
        for row_idx, row in enumerate(self.shape):
            for cal_idx, cell in enumerate(row):
                if cell:
                    px = (self.x+cal_idx) * BLOCK_SIZE
                    py = (self.y+row_idx) * BLOCK_SIZE
                    rect = pygame.Rect(px, py, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(surface, self.color, rect)
                    pygame.draw.rect(surface, GRID_COLOR, rect,1)
    def rotate(self,key):
        if key == 'right':
            self.shape = [list(row) for row in zip(*self.shape[::-1])]
        else:
            pass

class Board:
    def __init__(self,width, height):
        self.board = [[0]*width for _ in range(height)]
    def __repr__(self):
        board_string = ''
        for bo in self.board:
            for b in bo:
                board_string += f"| {b} "
            board_string += "|\n"
        # return board_string + '\n'
        return str(self.board)
    def if_valid(self, piece, dx = 0, dy = 0): # 충돌 판정
        """
        :param piece:
        :param dx:
        :param dy:
        :return:
        """
        old_shape = piece.shape
        for r, row in enumerate(old_shape):
            for c, cell in enumerate(row):
                if cell:
                    nx = piece.x + c + dx
                    ny = piece.y + r + dy
                    if nx < 0 or nx >= BOARD_WIDTH:
                        return False
                    if ny >= BOARD_HEIGHT:
                        return False
                    if self.board[ny][nx] == 1:
                        return False
        return True

    def lock_piece(self,piece): # 땅에 고정
        for i in range(piece):
            h=1
        pass

class Game:
    shapes = {"T_SHAPE": [[0, 1, 0], [1, 1, 1]], "O_SHAPE": [[1, 1], [1, 1]], "J_SHAPE": [[1, 0, 0], [1, 1, 1]]}
    BASIC_DROP_INTERVAL = 0.5
    BASIC_TICK = 60
    def __init__(self,screen):
        self.screen = screen                         # 게임 창
        self.clock = pygame.time.Clock()             # 게임 시간
        self.last_drop_time = time.time()            # 최근 낙하시간
        self.last_move_time = time.time()            # 최근 이동 시간
        self.last_turn_time = time.time()            # 최근 회전 시간
        self.current = self._get_random_shape()      # 현재 바라보고 있는 Tetromino
        self.board = Board(BOARD_WIDTH,BOARD_HEIGHT) # 게임 보드

    def _get_random_shape(self):
        """
        랜덤한 색상과 모양의 Tetromino를 반환
        :return: Tetromino객체
        """
        random_shape_name, random_shape = random.choice(list(self.shapes.items()))
        random_color_name, random_color = random.choice(list(color.items()))
        # print(random_shape_name, random_shape)
        # print(random_color_name,random_color)

        t = Tetromino(4,0, random_shape, random_color)
        return t

    def can_move(self, dx=0, dy=0, shape=None):
        """
        :param dx: int, x의 이동값
        :param dy: int, y의 이동값
        :param shape: list[int],현재 Tetromino의 모양
        :return: True/False, Tetromino가 움질일 수 있는지 없는지를 반환
        """
        shape = shape if shape else self.current.shape
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    nx = self.current.x + c + dx
                    ny = self.current.y + r + dy
                    if nx < 0 or nx >= BOARD_WIDTH:
                        return False
                    if ny < 0 or ny >= BOARD_HEIGHT:
                        return False
        return True


    def try_rotate(self,key):
        """
        :param key:
        :return:
        """
        old_shape = [row[:] for row in self.current.shape]
        self.current.rotate(key)
        if not self.can_move(shape=self.current.shape):
            self.current.shape = old_shape

    def draw_grid(self):
        """
        보드에 격자 그리는 함수
        :return: None
        """
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

    def update(self, DROP_INTERVAL):
        """

        :param DROP_INTERVAL:
        :return:
        """
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN]:
            DROP_INTERVAL = 0.1
        now = time.time()
        if now - self.last_drop_time >= DROP_INTERVAL:
            if self.current.y < BOARD_HEIGHT-len(self.current.shape):
                self.current.y += 1
                self.last_drop_time = now


    def draw(self):
        """
        게임 창에 그리고 반영
        :return: None
        """
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        self.current.draw(self.screen)
        pygame.display.flip()

    def run(self):
        """

        :return:
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.can_move(dx = -1):
                        self.current.x -= 1
                    elif event.key == pygame.K_RIGHT and self.can_move(dx = 1):
                        self.current.x += 1
                    elif event.key == pygame.K_d:
                        self.try_rotate('right')
                    elif event.key == pygame.K_a:
                        self.try_rotate('left')

            if not self.board.if_valid(self.current):
                input("is_valid: True")
            self.update(self.BASIC_DROP_INTERVAL)
            self.draw()
            # self.clock.tick(self.BASIC_TICK)
            self.clock.tick(1)
            print(self.board)

        pygame.quit()
        sys.exit()


# =====================================================reset============================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    game = Game(screen)
    game.run()


if __name__ == "__main__":
    main()