import time
import pygame as pg
import sys, os
import random

# ================================================GAME============================================================
class Game:
    BG_COLOR = (0, 0, 0)
    GRID_COLOR = (70, 70, 70)
    CURR_PATH = os.path.curdir
    STATIC_PATH = os.path.join(CURR_PATH,'static')

    def __init__(self):
        pg.init()
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 800
        pg.display.set_caption("MY TETRIS 2026")
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.BASIC_TICK = 60  # 게임 기본 틱
        self.CLOCK = pg.time.Clock()  # 게임 시간
        self.BLOCK_SIZE = 40
        self.BOARD_WIDTH = 10
        self.BOARD_HEIGHT = 20

        PAGES = [self._intro, self._run_tetris, self._ending]
        self.PAGE = 0  # 게임 페이지
        while True:
            PAGES[self.PAGE]()


    def _intro(self):
        bg_intro_path = os.path.join(self.STATIC_PATH, 'BG_INTRO.png')
        bg_img = pg.image.load(bg_intro_path)
        bg_rect = bg_img.get_rect()
        bg_rect = bg_rect.move(self.SCREEN_WIDTH // 2 - bg_rect.width//2,self.SCREEN_HEIGHT//2 - bg_rect.height//2)

        blink = True
        last_blink_time = pg.time.get_ticks()  # 마지막 깜빡임 시간 기록
        blink_interval = 500  # 깜빡임 간격 (밀리초 단위, 500ms = 0.5초)
        while True:
            player_current_time = pg.time.get_ticks()
            if player_current_time - last_blink_time > blink_interval:
                blink = not blink
                last_blink_time = player_current_time
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    self.PAGE += 1
                    return

            self.screen.fill((0, 0, 0))  # 배경 검정색
            self.screen.blit(bg_img,bg_rect)
            if blink:
                font = pg.font.SysFont(None, 48)
                text = font.render("Press any key to start", True, (255, 255, 255))
                self.screen.blit(text, (self.SCREEN_WIDTH//2 - text.get_rect().width//2 , bg_rect.y+bg_rect.height))
            pg.display.flip()
            self.CLOCK.tick(60)

    def _run_tetris(self):
        """
        게임 진행 함수
        :return:
        """
        return

    def _reset(self):
        pass

    def _ending(self):
        pg.quit()
        sys.exit()



# ================================================TETROMINO============================================================

class Tetromino:
    COLORS = {                                          # 블록 색상표
        'PUPPLE': (163, 73, 164), 'BLUE': (0, 0, 255),
         'RED': (255, 0, 0), 'WHITE': (200, 200, 200),
         'CYAN': (0, 230, 230)
    }
    SHAPES = {                                         # 블록 모양
        "T_SHAPE": [[0, 1, 0], [1, 1, 1]],
        "O_SHAPE": [[1, 1], [1, 1]],
        "J_SHAPE": [[1, 0, 0], [1, 1, 1]]
    }
    BASIC_DROP_INTERVAL = 0.5                          # 블록 낙하 시간

    move_interval = 0.05
    spint_interval = 0.3
    # 초기화: 랜덤한 모양과 색상을 가진 Tetromino 객체 반환
    def __init__(self, x, y):
        self.x = x                                             # 블록 좌상단 좌표
        self.y = y                                             # 블록 좌상단 좌표
        self.shape = random.choice(list(self.SHAPES.values())) # 랜덤 모양
        self.COLOR = random.choice(list(self.COLORS.values())) # 랜덤 색상

    # Tetromino 움직이는 함수
    def move(self):
        pass
    # Tetromino 회전하는 함수
    def rotate(self):
        pass
    # Tetromino 충돌 처리 함수
    def _is_collide(self):
        return


if __name__ == "__main__":
    game = Game()