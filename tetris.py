import pygame
import random
# import os
# os.environ['SDL_AUDIODRIVER'] = 'dummy'


# =====================
# 기본 설정
# =====================
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 600
BLOCK_SIZE = 30
GAME_WIDTH = 300
COLS, ROWS = GAME_WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE
BOARD_X = 120

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# =====================
# 배경 음악
# =====================
pygame.mixer.music.load("tetris_bgm.mp3")
pygame.mixer.music.play(-1)

# =====================
# 색상
# =====================
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)

COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (128, 0, 128)
]

# =====================
# 블록 정의
# =====================
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]


class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))


# =====================
# 게임 상태
# =====================
board = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
current = Tetromino()
next_block = Tetromino()
score = 0
game_over = False


def valid_position(block, dx=0, dy=0):
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                nx = block.x + x + dx
                ny = block.y + y + dy
                if nx < 0 or nx >= COLS or ny >= ROWS:
                    return False
                if ny >= 0 and board[ny][nx] != BLACK:
                    return False
    return True


def lock_block(block):
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                board[block.y + y][block.x + x] = block.color


def clear_lines():
    global board, score
    lines = 0
    new_board = []
    for row in board:
        if BLACK not in row:
            lines += 1
        else:
            new_board.append(row)

    while len(new_board) < ROWS:
        new_board.insert(0, [BLACK for _ in range(COLS)])

    board = new_board
    score += lines * 100


def draw_board():
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(
                screen,
                board[y][x],
                (BOARD_X + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                screen,
                GRAY,
                (BOARD_X + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1
            )


def draw_block(block, offset_x=0, offset_y=0):
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    block.color,
                    (BOARD_X + (block.x + x) * BLOCK_SIZE + offset_x,
                     (block.y + y) * BLOCK_SIZE + offset_y,
                     BLOCK_SIZE, BLOCK_SIZE)
                )


def draw_next_block():
    text = font.render("NEXT", True, WHITE)
    screen.blit(text, (20, 10))

    for y, row in enumerate(next_block.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    next_block.color,
                    (20 + x * BLOCK_SIZE,
                     40 + y * BLOCK_SIZE,
                     BLOCK_SIZE, BLOCK_SIZE)
                )
                pygame.draw.rect(
                    screen,
                    GRAY,
                    (20 + x * BLOCK_SIZE,
                     40 + y * BLOCK_SIZE,
                     BLOCK_SIZE, BLOCK_SIZE),
                    1
                )


def draw_score():
    text = font.render(f"SCORE: {score}", True, WHITE)
    x = WIDTH - text.get_width() - 20
    screen.blit(text, (x, 10))


# =====================
# 메인 루프
# =====================
fall_time = 0
running = True

while running:
    screen.fill(BLACK)
    fall_time += clock.get_rawtime()
    clock.tick(60)

    if fall_time > 500:
        if valid_position(current, dy=1):
            current.y += 1
        else:
            lock_block(current)
            clear_lines()
            current = next_block
            next_block = Tetromino()
            # 게임 오버: 새로 생성한 블록이 유효한 위치에 있지 않으면 상단 충돌로 간주
            if not valid_position(current):
                game_over = True
                # 화면에 Game Over를 표시하고 종료 대기
                text = font.render("GAME OVER", True, WHITE)
                while True:
                    screen.fill(BLACK)
                    draw_board()
                    draw_block(current)
                    draw_next_block()
                    draw_score()
                    x = WIDTH // 2 - text.get_width() // 2
                    y = HEIGHT // 2 - text.get_height() // 2
                    screen.blit(text, (x, y))
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            raise SystemExit
                        if event.type == pygame.KEYDOWN:
                            pygame.quit()
                            raise SystemExit
                    clock.tick(10)
        fall_time = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and valid_position(current, dx=-1):
                current.x -= 1
            elif event.key == pygame.K_RIGHT and valid_position(current, dx=1):
                current.x += 1
            elif event.key == pygame.K_DOWN and valid_position(current, dy=1):
                current.y += 1
            elif event.key == pygame.K_UP:
                original = current.shape
                current.rotate()
                if not valid_position(current):
                    current.shape = original
            elif event.key == pygame.K_SPACE:
                while valid_position(current, dy=1):
                    current.y += 1

    draw_board()
    draw_block(current)
    draw_next_block()
    draw_score()

    pygame.display.flip()

pygame.quit()
