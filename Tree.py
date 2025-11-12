import os, time, random, sys
os.system('')  # 윈도우 ANSI 컬러 활성화

# ANSI 색상
leaf_colors = ["\033[92m","\033[32m","\033[93m","\033[96m","\033[95m"]
trunk_color = "\033[38;5;94m"
snow_color = "\033[97m"
reset = "\033[0m"

# 트리
tree = [
    "         *         ",
    "        ***        ",
    "       *****       ",
    "      *******      ",
    "     *********     ",
    "    ***********    ",
    "   *************   ",
    "        |||        "
]

# 눈사람
snowman = [
    "    ___ ",
    "  \\(o o)/ ",
    "   ( : ) ",
    "  ''''''' "
]

# 눈송이 및 눈 더미
snowflakes = []
snow_pile = {}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_scene():
    width = 60
    height = 14  # 바닥 높이

    # 눈송이 떨어짐
    new_snowflakes = []
    for (x, y) in snowflakes:
        pile_height = snow_pile.get(x, 0)
        if y < height - pile_height - 1:
            new_snowflakes.append((x, y + 1))
        else:
            # 최대 2층까지만 쌓이도록 제한
            if snow_pile.get(x, 0) < 2:
                snow_pile[x] = snow_pile.get(x, 0) + 1
    snowflakes[:] = new_snowflakes

    # 새 눈 생성
    if random.random() < 0.9:
        snowflakes.append((random.randint(0, width - 1), 0))

    # 바닥 눈 녹음 (5% 확률)
    for x in list(snow_pile.keys()):
        if random.random() < 0.05:
            snow_pile[x] -= 1
            if snow_pile[x] <= 0:
                del snow_pile[x]

    # 화면 버퍼
    buffer = [[" "] * width for _ in range(height)]

    # 쌓인 눈 표시
    for x, pile_height in snow_pile.items():
        for y in range(height - 1, height - pile_height - 1, -1):
            if 0 <= x < width and 0 <= y < height:
                buffer[y][x] = snow_color + "*" + reset

    # 떨어지는 눈 표시
    for (x, y) in snowflakes:
        if 0 <= x < width and 0 <= y < height:
            buffer[y][x] = snow_color + "*" + reset

    # 트리 표시
    start_y = 3
    for i, line in enumerate(tree):
        if start_y + i < height:
            for j, ch in enumerate(line):
                if ch == "*":
                    buffer[start_y + i][10 + j] = random.choice(leaf_colors) + "*" + reset
                elif ch == "|":
                    buffer[start_y + i][10 + j] = trunk_color + "|" + reset

    # 눈사람 표시 (바닥 바로 위)
    start_y_snowman = height - len(snowman) -2
    for i, line in enumerate(snowman):
        if start_y_snowman + i < height:
            for j, ch in enumerate(line):
                if ch != " ":
                    buffer[start_y_snowman + i][38 + j] = snow_color + ch + reset

    # 화면 출력
    for row in buffer:
        print("".join(row))

try:
    while True:
        clear()
        show_scene()
        time.sleep(0.12)
except KeyboardInterrupt:
    clear()
    sys.exit()
