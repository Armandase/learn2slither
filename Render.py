import pygame
from constants import W_WIDTH, W_HEIGHT, DEFAULT_SIZE, TITLE, \
    TAIL, HEAD, GREEN_APPLE, RED_APPLE, \
    COLORS_RED_APPLE, COLORS_GREEN_APPLE, COLORS_SNAKE, \
    COLORS_EMPTY, COLORS_LINES


class Render():
    def __init__(self,
                 w_width=W_WIDTH, w_height=W_HEIGHT,
                 grid_size=DEFAULT_SIZE):
        pygame.init()
        self.screen = pygame.display.set_mode((w_width, w_height))
        pygame.display.set_caption(TITLE)
        self.window_width = w_width
        self.window_height = w_height
        self.ratio = w_height / grid_size

    def __del__(self):
        pygame.quit()

    def get_screen(self):
        return self.screen

    def set_screen(self, screen: pygame.Surface):
        self.screen = screen

    def display_background(self):
        self.screen.fill("black")

    def draw_grid(self, grid):
        rows, cols = grid.shape

        for row in range(rows):
            for col in range(cols):
                if grid[row, col] == HEAD or grid[row, col] == TAIL:
                    color = COLORS_SNAKE
                elif grid[row, col] == RED_APPLE:
                    color = COLORS_RED_APPLE
                elif grid[row, col] == GREEN_APPLE:
                    color = COLORS_GREEN_APPLE
                else:
                    color = COLORS_EMPTY

                rect = pygame.Rect(
                    col * self.ratio, row * self.ratio,
                    self.ratio, self.ratio
                )

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, COLORS_LINES, rect, 1)

    def display_score(self, score):
        font = pygame.font.Font(None, 36)

        score_text = font.render(f'Score: {score}', True, COLORS_LINES)
        self.screen.blit(score_text, (10, 10))
