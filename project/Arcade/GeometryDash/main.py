import arcade
from save_manager import load_save_data, save_stage_clear, get_stage_record

# 화면 및 물리 상수
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Geometry Dash Clone (Arcade + Tiled)"

TILE_SIZE = 64
MOVE_SPEED = 420.0      # 초당 이동 픽셀
GRAVITY = 2800.0        # 중력 가속도
JUMP_SPEED = 860.0      # 고정 점프 초기 속도
ROTATION_SPEED = 360.0  # 공중 회전 속도 (도/초)

# 스테이지 목록 (클리어 기록은 saves/save_data.json에서 관리)
STAGES = [
    {"id": 1, "name": "Stage 1", "map_path": "maps/stage1.tmx", "theme": "cyber_neon"},
    {"id": 2, "name": "Stage 2", "map_path": None, "theme": "synth_sunset"},
    {"id": 3, "name": "Stage 3", "map_path": None, "theme": "crimson_core"},
]


class IntroView(arcade.View):
    """인트로 페이지: 게임 모드 선택"""
    def __init__(self):
        super().__init__()
        self.title_text = arcade.Text(
            "GEOMETRY DASH CLONE", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.72,
            arcade.color.CYAN, font_size=40, anchor_x="center", bold=True
        )
        self.mode1_text = arcade.Text(
            "[1] 큐브 모드 (기본 점프) - ENTER 또는 1번 키",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.48,
            arcade.color.WHITE, font_size=20, anchor_x="center"
        )
        self.mode2_text = arcade.Text(
            "[2] 비행 모드 (준비 중)",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.38,
            arcade.color.GRAY, font_size=18, anchor_x="center"
        )

    def on_show_view(self):
        self.window.background_color = (15, 20, 40)

    def on_draw(self):
        self.clear()
        self.title_text.draw()
        self.mode1_text.draw()
        self.mode2_text.draw()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.KEY_1, arcade.key.ENTER, arcade.key.SPACE):
            self.window.show_view(StageSelectView(mode="cube"))


class StageSelectView(arcade.View):
    """스테이지 선택 페이지 (박스 UI + 방향키 이동)"""
    def __init__(self, mode="cube", selected_index=0):
        super().__init__()
        self.mode = mode
        self.selected_index = selected_index
        self.save_data = load_save_data()

        self.header_text = arcade.Text(
            f"STAGE SELECT ({mode.upper()} MODE)", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.80,
            arcade.color.YELLOW, font_size=32, anchor_x="center", bold=True
        )
        self.guide_text = arcade.Text(
            "← / → : 스테이지 이동   |   ENTER : 시작   |   ESC : 모드 선택",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.15,
            arcade.color.LIGHT_GRAY, font_size=15, anchor_x="center"
        )
        self.notice_text = arcade.Text(
            "", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.23,
            arcade.color.ORANGE_RED, font_size=15, anchor_x="center"
        )

        # 박스 레이아웃 계산 및 텍스트 객체 미리 생성 (최적화)
        self.box_size = 150
        self.box_gap = 60
        total_width = len(STAGES) * self.box_size + (len(STAGES) - 1) * self.box_gap
        start_x = (SCREEN_WIDTH - total_width) / 2 + self.box_size / 2
        self.box_y = SCREEN_HEIGHT * 0.52

        self.box_positions = []
        self.stage_labels = []
        self.status_labels = []

        for i, stage in enumerate(STAGES):
            cx = start_x + i * (self.box_size + self.box_gap)
            self.box_positions.append((cx, self.box_y))

            # 박스 하단 스테이지 번호 텍스트
            self.stage_labels.append(
                arcade.Text(
                    f"Stage {stage['id']}", cx, self.box_y - self.box_size / 2 - 32,
                    arcade.color.WHITE, font_size=18, anchor_x="center", bold=True
                )
            )

            # 세이브 파일에서 클리어 기록 조회
            record = get_stage_record(self.save_data, self.mode, stage["id"])
            if record["cleared"]:
                status_str = f"클리어\n({record['clear_count']}회)\n최소 {record['best_attempts']}시도"
            else:
                status_str = "" if stage["map_path"] else "준비 중"

            self.status_labels.append(
                arcade.Text(
                    status_str, cx, self.box_y,
                    arcade.color.WHITE, font_size=15, anchor_x="center", anchor_y="center",
                    multiline=True, width=self.box_size - 16, align="center", bold=True
                )
            )

    def on_show_view(self):
        self.window.background_color = (20, 25, 50)

    def on_draw(self):
        self.clear()
        self.header_text.draw()
        self.guide_text.draw()
        self.notice_text.draw()

        half = self.box_size / 2
        for i, stage in enumerate(STAGES):
            cx, cy = self.box_positions[i]
            left, right = cx - half, cx + half
            bottom, top = cy - half, cy + half

            # 세이브 데이터 기준 클리어 여부에 따른 박스 색상 (초록 / 빨강)
            record = get_stage_record(self.save_data, self.mode, stage["id"])
            fill_color = (40, 170, 75) if record["cleared"] else (190, 50, 55)
            arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, fill_color)

            # 선택된 스테이지 강조 테두리
            if i == self.selected_index:
                arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.YELLOW, border_width=5)
            else:
                arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.WHITE, border_width=2)

            self.status_labels[i].draw()
            self.stage_labels[i].draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.selected_index = (self.selected_index - 1) % len(STAGES)
            self.notice_text.text = ""
        elif key == arcade.key.RIGHT:
            self.selected_index = (self.selected_index + 1) % len(STAGES)
            self.notice_text.text = ""
        elif key in (arcade.key.ENTER, arcade.key.SPACE):
            stage = STAGES[self.selected_index]
            if stage["map_path"]:
                game_view = GameView(stage_index=self.selected_index, mode=self.mode)
                game_view.setup()
                self.window.show_view(game_view)
            else:
                self.notice_text.text = f"Stage {stage['id']} 맵 파일이 아직 준비되지 않았습니다."
        elif key == arcade.key.ESCAPE:
            self.window.show_view(IntroView())


class GameView(arcade.View):
    """게임 진행 페이지"""
    def __init__(self, stage_index: int, mode: str = "cube"):
        super().__init__()
        self.stage_index = stage_index
        self.mode = mode
        self.stage_info = STAGES[stage_index]
        self.map_path = self.stage_info["map_path"]

        self.scene = None
        self.player = None
        self.player_list = None

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.theme_name = self.stage_info.get("theme", "cyber_neon")
        self.bg_list = None
        self.bg_scroll_x = 0.0

        self.attempts = 1
        self.on_ground = False
        self.jump_held = False
        self.spawn_x = TILE_SIZE * 2
        self.spawn_y = TILE_SIZE * 2

        self.attempt_text = arcade.Text(
            "Attempt 1", 20, SCREEN_HEIGHT - 40,
            arcade.color.WHITE, font_size=20, bold=True
        )
        self.guide_text = arcade.Text(
            "SPACE/UP: 점프 (꾹 누르면 연속 점프) | ESC: 포기",
            20, SCREEN_HEIGHT - 70,
            arcade.color.LIGHT_GRAY, font_size=13
        )

    def setup(self):
        self.window.background_color = (5, 8, 20)

        # 패럴랙스 배경 (동일 이미지 2장을 이어 붙여 무한 스크롤)
        self.bg_list = arcade.SpriteList()
        bg_path = f"assets/{self.theme_name}/bg.png"
        for i in range(2):
            bg_sprite = arcade.Sprite(bg_path, scale=1.0)
            bg_sprite.left = i * SCREEN_WIDTH
            bg_sprite.bottom = 0
            self.bg_list.append(bg_sprite)

        layer_options = {
            "Blocks": {"use_spatial_hash": True},
            "Spikes": {"use_spatial_hash": True},
            "Goal": {"use_spatial_hash": True},
        }
        tile_map = arcade.load_tilemap(self.map_path, scaling=1.0, layer_options=layer_options)
        self.scene = arcade.Scene.from_tilemap(tile_map)

        self.player_list = arcade.SpriteList()
        self.player = arcade.Sprite(f"assets/{self.theme_name}/player.png", scale=1.0)
        self.player_list.append(self.player)

        self.reset_player()

    def reset_player(self):
        self.player.center_x = self.spawn_x
        self.player.center_y = self.spawn_y
        self.player.change_y = 0
        self.player.angle = 0
        self.on_ground = False
        self.attempt_text.text = f"Attempt {self.attempts}"

    def trigger_death(self):
        self.attempts += 1
        self.reset_player()

    def on_draw(self):
        self.clear()

        # 1. 패럴랙스 배경 (화면 좌표계)
        self.gui_camera.use()
        self.bg_list.draw()

        # 2. 월드 (카메라 이동 적용)
        self.camera.use()
        self.scene.draw()
        self.player_list.draw()

        # 3. UI (화면 고정)
        self.gui_camera.use()
        self.attempt_text.draw()
        self.guide_text.draw()

    def on_update(self, delta_time: float):
        dt = min(delta_time, 1 / 30)

        # 1. 연속 점프 처리
        if self.jump_held and self.on_ground:
            self.player.change_y = JUMP_SPEED
            self.on_ground = False

        # 2. X축 이동 및 벽(옆면) 충돌 판정
        self.player.center_x += MOVE_SPEED * dt
        block_hits_x = arcade.check_for_collision_with_list(self.player, self.scene["Blocks"])
        for block in block_hits_x:
            if self.player.bottom < block.top - 8:
                self.trigger_death()
                return

        # 3. Y축 이동 (중력) 및 바닥/천장 충돌 판정
        self.player.change_y -= GRAVITY * dt
        self.player.center_y += self.player.change_y * dt
        self.on_ground = False

        block_hits_y = arcade.check_for_collision_with_list(self.player, self.scene["Blocks"])
        for block in block_hits_y:
            if self.player.change_y <= 0:  # 낙하 중 바닥 착지
                self.player.angle = round(self.player.angle / 90) * 90
                self.player.bottom = block.top
                self.player.change_y = 0
                self.on_ground = True
            elif self.player.change_y > 0:  # 천장 충돌 -> 사망
                self.trigger_death()
                return

        # 4. 공중 회전 애니메이션
        if not self.on_ground:
            self.player.angle += ROTATION_SPEED * dt

        # 5. 가시 충돌 판정
        if arcade.check_for_collision_with_list(self.player, self.scene["Spikes"]):
            self.trigger_death()
            return

        # 6. 낙사 판정
        if self.player.center_y < -100:
            self.trigger_death()
            return

        # 7. 골인 지점 도달 판정 -> 세이브 파일 저장
        if arcade.check_for_collision_with_list(self.player, self.scene["Goal"]):
            save_stage_clear(self.mode, self.stage_info["id"], self.attempts)
            self.window.show_view(
                GameClearView(stage_index=self.stage_index, mode=self.mode, attempts=self.attempts)
            )
            return

        # 8. 카메라 추적
        cam_x = self.player.center_x + SCREEN_WIDTH * 0.25
        cam_y = SCREEN_HEIGHT / 2
        self.camera.position = (cam_x, cam_y)
        offset = (self.player.center_x * 0.2) % SCREEN_WIDTH
        self.bg_list[0].left = -offset
        self.bg_list[1].left = SCREEN_WIDTH - offset

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.UP, arcade.key.W):
            self.jump_held = True
        elif key == arcade.key.ESCAPE:
            self.window.show_view(StageSelectView(mode=self.mode, selected_index=self.stage_index))

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.UP, arcade.key.W):
            self.jump_held = False


class GameClearView(arcade.View):
    """게임 종료(클리어) 페이지"""
    def __init__(self, stage_index: int, mode: str, attempts: int):
        super().__init__()
        self.stage_index = stage_index
        self.mode = mode
        self.clear_text = arcade.Text(
            f"STAGE {STAGES[stage_index]['id']} CLEAR!", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.65,
            arcade.color.GOLD, font_size=44, anchor_x="center", bold=True
        )
        self.stat_text = arcade.Text(
            f"총 시도 횟수: {attempts}번", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.5,
            arcade.color.WHITE, font_size=24, anchor_x="center"
        )
        self.guide_text = arcade.Text(
            "ENTER: 스테이지 선택으로 | ESC: 인트로로",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.35,
            arcade.color.LIGHT_GRAY, font_size=16, anchor_x="center"
        )

    def on_show_view(self):
        self.window.background_color = (15, 35, 25)

    def on_draw(self):
        self.clear()
        self.clear_text.draw()
        self.stat_text.draw()
        self.guide_text.draw()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ENTER, arcade.key.SPACE):
            self.window.show_view(StageSelectView(mode=self.mode, selected_index=self.stage_index))
        elif key == arcade.key.ESCAPE:
            self.window.show_view(IntroView())


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, vsync=True)
    window.show_view(IntroView())
    arcade.run()


if __name__ == "__main__":
    main()