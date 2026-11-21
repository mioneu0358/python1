import os
from PIL import Image, ImageDraw, ImageFilter
from themes import THEMES

TILE_SIZE = 64
BG_WIDTH = 1024
BG_HEIGHT = 640


def add_neon_layer(base_img: Image.Image, draw_func, color, blur_radius=5):
    """네온 글로우(빛 번짐) + 밝은 중심선을 base_img에 합성"""
    glow = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    draw_func(g_draw, color + (255,), width=5)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # 글로우 2회 중첩으로 발광감 강화
    base_img.alpha_composite(glow)
    base_img.alpha_composite(glow)

    # 중심부 밝은 코어 라인
    core_draw = ImageDraw.Draw(base_img)
    core_color = tuple(min(255, c + 120) for c in color) + (255,)
    draw_func(core_draw, core_color, width=2)


def create_theme_assets(theme_name: str, t: dict):
    out_dir = os.path.join("assets", theme_name)
    os.makedirs(out_dir, exist_ok=True)

    # 1. 사이버펑크 배경 (1024x640, 좌우 무한 반복 가능)
    bg = Image.new("RGBA", (BG_WIDTH, BG_HEIGHT))
    bg_draw = ImageDraw.Draw(bg)
    r1, g1, b1 = t["bg_top"]
    r2, g2, b2 = t["bg_bottom"]

    # 세로 그라데이션
    for y in range(BG_HEIGHT):
        ratio = y / BG_HEIGHT
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        bg_draw.line([(0, y), (BG_WIDTH, y)], fill=(r, g, b, 255))

    # 사이버 그리드 레이어
    grid_layer = Image.new("RGBA", (BG_WIDTH, BG_HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grid_layer)
    step = 64
    for x in range(0, BG_WIDTH, step):
        g_draw.line([(x, 0), (x, BG_HEIGHT)], fill=t["grid_color"], width=1)
    for y in range(0, BG_HEIGHT, step):
        g_draw.line([(0, y), (BG_WIDTH, y)], fill=t["grid_color"], width=1)

    # 하단 수평 네온 지평선 강조
    horizon_y = int(BG_HEIGHT * 0.75)
    g_draw.line([(0, horizon_y), (BG_WIDTH, horizon_y)], fill=t["block_neon"] + (130,), width=3)

    # 배경에 장식용 사이버 사각형(빌딩 실루엣 느낌)
    for bx, bw, bh in [(80, 90, 220), (260, 130, 300), (520, 100, 190), (740, 150, 260)]:
        rect = [bx, horizon_y - bh, bx + bw, horizon_y]
        g_draw.rectangle(rect, fill=(10, 10, 25, 110), outline=t["block_neon"] + (70,), width=2)

    bg.alpha_composite(grid_layer)
    bg.save(os.path.join(out_dir, "bg.png"))

    # 2. 플레이어 큐브 (64x64 네온 코어 디자인)
    player = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(player)
    p_draw.rectangle([4, 4, TILE_SIZE - 5, TILE_SIZE - 5], fill=t["player_core"] + (255,))

    # 외곽 네온 + 내부 기하학 눈/코어
    add_neon_layer(
        player,
        lambda d, c, width: d.rectangle([4, 4, TILE_SIZE - 5, TILE_SIZE - 5], outline=c, width=width),
        t["player_neon"],
        blur_radius=4,
    )
    add_neon_layer(
        player,
        lambda d, c, width: (
            d.rectangle([15, 16, 25, 26], outline=c, width=width),
            d.rectangle([38, 16, 48, 26], outline=c, width=width),
            d.line([(16, 44), (48, 44)], fill=c, width=width),
        ),
        t["player_neon"],
        blur_radius=3,
    )
    player.save(os.path.join(out_dir, "player.png"))

    # 3. 타일셋 (가로 3칸: 1=블록, 2=가시, 3=골인 포털)
    tileset = Image.new("RGBA", (TILE_SIZE * 3, TILE_SIZE), (0, 0, 0, 0))
    ts_draw = ImageDraw.Draw(tileset)

    # [Tile 1] 사이버 네온 블록
    ts_draw.rectangle([2, 2, TILE_SIZE - 3, TILE_SIZE - 3], fill=t["block_fill"] + (255,))
    # 내부 회로 십자 패턴
    ts_draw.rectangle([14, 14, TILE_SIZE - 15, TILE_SIZE - 15], outline=t["block_neon"] + (90,), width=2)
    add_neon_layer(
        tileset,
        lambda d, c, width: d.rectangle([3, 3, TILE_SIZE - 4, TILE_SIZE - 4], outline=c, width=width),
        t["block_neon"],
        blur_radius=4,
    )

    # [Tile 2] 네온 가시 (강렬한 대비)
    ox = TILE_SIZE
    spike_pts = [(ox + TILE_SIZE // 2, 6), (ox + 6, TILE_SIZE - 3), (ox + TILE_SIZE - 6, TILE_SIZE - 3)]
    ts_draw.polygon(spike_pts, fill=t["spike_fill"] + (255,))
    add_neon_layer(
        tileset,
        lambda d, c, width: d.polygon(spike_pts, outline=c, width=width),
        t["spike_neon"],
        blur_radius=4,
    )

    # [Tile 3] 골인 에너지 포털
    ox = TILE_SIZE * 2
    ts_draw.rectangle([ox + 16, 0, ox + TILE_SIZE - 16, TILE_SIZE - 1], fill=t["goal_neon"] + (70,))
    add_neon_layer(
        tileset,
        lambda d, c, width: d.rectangle([ox + 14, 2, ox + TILE_SIZE - 14, TILE_SIZE - 3], outline=c, width=width),
        t["goal_neon"],
        blur_radius=5,
    )

    tileset.save(os.path.join(out_dir, "tileset.png"))
    print(f"[완료] assets/{theme_name}/ 에셋 생성 완료")


def create_stage1_tmx():
    os.makedirs("maps", exist_ok=True)
    width, height = 50, 10

    blocks = [[0] * width for _ in range(height)]
    spikes = [[0] * width for _ in range(height)]
    goal = [[0] * width for _ in range(height)]

    for x in range(width):
        blocks[9][x] = 1

    spikes[8][10] = 2
    spikes[8][16] = 2
    spikes[8][17] = 2

    blocks[8][23] = 1
    blocks[8][24] = 1
    blocks[7][27] = 1
    blocks[7][28] = 1
    spikes[8][27] = 2
    spikes[8][28] = 2

    spikes[8][34] = 2
    spikes[8][39] = 2

    goal[8][46] = 3
    goal[7][46] = 3
    goal[6][46] = 3

    def to_csv(grid):
        return ",\n".join(",".join(map(str, row)) for row in grid)

    tmx_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" tiledversion="1.10.2" orientation="orthogonal" renderorder="right-down" width="{width}" height="{height}" tilewidth="{TILE_SIZE}" tileheight="{TILE_SIZE}" infinite="0" nextlayerid="4" nextobjectid="1">
 <tileset firstgid="1" name="gd_tiles" tilewidth="{TILE_SIZE}" tileheight="{TILE_SIZE}" tilecount="3" columns="3">
  <image source="../assets/cyber_neon/tileset.png" width="{TILE_SIZE * 3}" height="{TILE_SIZE}"/>
 </tileset>
 <layer id="1" name="Blocks" width="{width}" height="{height}">
  <data encoding="csv">
{to_csv(blocks)}
  </data>
 </layer>
 <layer id="2" name="Spikes" width="{width}" height="{height}">
  <data encoding="csv">
{to_csv(spikes)}
  </data>
 </layer>
 <layer id="3" name="Goal" width="{width}" height="{height}">
  <data encoding="csv">
{to_csv(goal)}
  </data>
 </layer>
</map>
"""
    with open("maps/stage1.tmx", "w", encoding="utf-8") as f:
        f.write(tmx_content)
    print("[완료] maps/stage1.tmx 생성 완료 (cyber_neon 타일셋 연결)")


if __name__ == "__main__":
    for name, palette in THEMES.items():
        create_theme_assets(name, palette)
    create_stage1_tmx()