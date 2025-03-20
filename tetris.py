import pygame
import random

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS, ROWS = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
CYAN = (0, 200, 200)
MAGENTA = (200, 0, 200)
YELLOW = (200, 200, 0)
ORANGE = (255, 165, 0)
COLORS = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 1], [1, 0, 0]]   # L
]

class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x, self.y = COLUMNS // 2 - len(self.shape[0]) // 2, 0

    def rotate(self):
        """Rotates the shape clockwise if possible."""
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]
        return rotated_shape

class Tetris:
    def __init__(self):
        self.grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.tetrimino = Tetrimino()
        self.running = True

    def valid_move(self, dx=0, dy=0, shape=None):
        """Checks if the tetrimino can move to the given position."""
        if shape is None:
            shape = self.tetrimino.shape

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = self.tetrimino.x + x + dx, self.tetrimino.y + y + dy
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        return False
        return True

    def merge_tetrimino(self):
        """Merges the current tetrimino into the grid."""
        for y, row in enumerate(self.tetrimino.shape):
            for x, cell in enumerate(row):
                if cell and self.tetrimino.y + y >= 0:
                    self.grid[self.tetrimino.y + y][self.tetrimino.x + x] = self.tetrimino.color

    def remove_lines(self):
        """Removes full lines from the grid."""
        new_grid = [row for row in self.grid if BLACK in row]
        lines_cleared = ROWS - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [BLACK] * COLUMNS)
        self.grid = new_grid

    def update(self):
        """Updates the game state by moving the tetrimino down."""
        if self.valid_move(dy=1):
            self.tetrimino.y += 1
        else:
            self.merge_tetrimino()
            self.remove_lines()
            self.tetrimino = Tetrimino()
            if not self.valid_move():
                self.running = False  # Game Over

    def draw(self, screen):
        """Draws the grid and tetrimino on the screen."""
        screen.fill(BLACK)
        # Draw grid blocks
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color != BLACK:
                    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Draw current tetrimino
        for y, row in enumerate(self.tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.tetrimino.color,
                                     ((self.tetrimino.x + x) * BLOCK_SIZE, (self.tetrimino.y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)

# Main game loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Tetris()

    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.valid_move(dx=-1):
                    game.tetrimino.x -= 1
                if event.key == pygame.K_RIGHT and game.valid_move(dx=1):
                    game.tetrimino.x += 1
                if event.key == pygame.K_DOWN:
                    game.update()
                if event.key == pygame.K_UP:
                    rotated_shape = game.tetrimino.rotate()
                    if game.valid_move(shape=rotated_shape):
                        game.tetrimino.shape = rotated_shape

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()
