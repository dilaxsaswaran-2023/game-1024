import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 400, 400
TILE_SIZE = WIDTH // 4
FONT = pygame.font.SysFont("comicsansms", 40)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

WHITE = (250, 248, 239)
BLACK = (119, 110, 101)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

grid = [[0] * 4 for _ in range(4)]

def add_tile():
    empty = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        grid[r][c] = 2 if random.random() < 0.9 else 4

def draw_grid():
    screen.fill(WHITE)
    for r in range(4):
        for c in range(4):
            val = grid[r][c]
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, TILE_COLORS.get(val, (60, 58, 50)), rect)
            if val:
                text = FONT.render(str(val), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    pygame.display.update()

def compress(row):
    new_row = [num for num in row if num != 0]
    new_row += [0] * (4 - len(new_row))
    return new_row

def merge(row):
    for i in range(3):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0
    return row

def move_left():
    moved = False
    for i in range(4):
        row = compress(grid[i])
        merged = merge(row)
        new_row = compress(merged)
        if grid[i] != new_row:
            moved = True
            grid[i] = new_row
    return moved

def move_right():
    moved = False
    for i in range(4):
        row = list(reversed(grid[i]))
        row = compress(row)
        merged = merge(row)
        new_row = list(reversed(compress(merged)))
        if grid[i] != new_row:
            moved = True
            grid[i] = new_row
    return moved

def move_up():
    moved = False
    for c in range(4):
        col = [grid[r][c] for r in range(4)]
        col = compress(col)
        col = merge(col)
        col = compress(col)
        for r in range(4):
            if grid[r][c] != col[r]:
                moved = True
                grid[r][c] = col[r]
    return moved

def move_down():
    moved = False
    for c in range(4):
        col = [grid[r][c] for r in range(4)]
        col = list(reversed(col))
        col = compress(col)
        col = merge(col)
        col = compress(col)
        col = list(reversed(col))
        for r in range(4):
            if grid[r][c] != col[r]:
                moved = True
                grid[r][c] = col[r]
    return moved

def game_over():
    for r in range(4):
        for c in range(4):
            if grid[r][c] == 0:
                return False
            if c < 3 and grid[r][c] == grid[r][c + 1]:
                return False
            if r < 3 and grid[r][c] == grid[r + 1][c]:
                return False
    return True

def show_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    over_text = FONT.render("Game Over", True, WHITE)
    screen.blit(over_text, over_text.get_rect(center=(WIDTH//2, HEIGHT//2)))
    pygame.display.update()

def main():
    add_tile()
    add_tile()
    running = True
    clock = pygame.time.Clock()

    while running:
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_LEFT:
                    moved = move_left()
                elif event.key == pygame.K_RIGHT:
                    moved = move_right()
                elif event.key == pygame.K_UP:
                    moved = move_up()
                elif event.key == pygame.K_DOWN:
                    moved = move_down()

                if moved:
                    add_tile()
                    draw_grid()
                    if game_over():
                        show_game_over()
                        pygame.time.wait(2000)
                        running = False

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
