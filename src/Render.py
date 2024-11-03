import pygame
from src.constants import W_WIDTH, W_HEIGHT, DEFAULT_SIZE, TITLE, \
    TAIL, HEAD, GREEN_APPLE, RED_APPLE, \
    COLORS_RED_APPLE, COLORS_GREEN_APPLE, COLORS_SNAKE, \
    COLORS_EMPTY, COLORS_LINES, COLORS_TOOLBAR, COLORS_SNAKE_HEAD, \
    IMAGE_PATH


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
        self.font = None
        self.toolbar_width = self.window_width - self.window_height
        self.load_image()


    def __del__(self):
        pygame.quit()

    def load_image(self, path=IMAGE_PATH):
        self.img_snake_head = pygame.image.load(f'{IMAGE_PATH}/snake_head.png')
        self.img_snake_tail = pygame.image.load(f'{IMAGE_PATH}/snake_tail.png')
        self.img_red_apple = pygame.image.load(f'{IMAGE_PATH}/red_apple.png')
        self.img_green_apple = pygame.image.load(f'{IMAGE_PATH}/green_apple.png')

        # Redimensionne les images à la taille des cases de la grille
        self.img_snake_head = pygame.transform.scale(self.img_snake_head, (self.ratio, self.ratio))
        self.img_snake_tail = pygame.transform.scale(self.img_snake_tail, (self.ratio, self.ratio))
        self.img_red_apple = pygame.transform.scale(self.img_red_apple, (self.ratio, self.ratio))
        self.img_green_apple = pygame.transform.scale(self.img_green_apple, (self.ratio, self.ratio))


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
                # if grid[row, col] == HEAD:
                #     color = COLORS_SNAKE_HEAD
                # elif grid[row, col] == TAIL:
                #     color = COLORS_SNAKE
                # elif grid[row, col] == RED_APPLE:
                #     color = COLORS_RED_APPLE
                # elif grid[row, col] == GREEN_APPLE:
                #     color = COLORS_GREEN_APPLE
                # else:
                #     color = COLORS_EMPTY

                # rect = pygame.Rect(
                #     col * self.ratio, row * self.ratio,
                #     self.ratio, self.ratio
                # )

                # pygame.draw.rect(self.screen, color, rect)
                # pygame.draw.rect(self.screen, COLORS_LINES, rect, 1)
                x, y = col * self.ratio, row * self.ratio

                if grid[row, col] == HEAD:
                    self.screen.blit(self.img_snake_head, (x, y))
                elif grid[row, col] == TAIL:
                    self.screen.blit(self.img_snake_tail, (x, y))
                elif grid[row, col] == RED_APPLE:
                    self.screen.blit(self.img_red_apple, (x, y))
                elif grid[row, col] == GREEN_APPLE:
                    self.screen.blit(self.img_green_apple, (x, y))
                else:
                    rect = pygame.Rect(x, y, self.ratio, self.ratio)
                    pygame.draw.rect(self.screen, COLORS_EMPTY, rect)

                pygame.draw.rect(self.screen, COLORS_LINES, pygame.Rect(x, y, self.ratio, self.ratio), 1)


    def display_toolbar(self, score, grid_size):
        rect = pygame.Rect(
                    self.window_height, 0,
                    self.toolbar_width, self.window_height
                )
        pygame.draw.rect(self.screen, COLORS_LINES, rect)
        self.display_score(score, grid_size)

    def display_score(self, score, grid_size):
        # achievement = 'noob'
        # if score > grid_size:
        #     achievement = 'monkey'
        # elif score > grid_size * 2:
        #     achievement = 'mid'
        # elif score > grid_size * 4:
        #     achievement = 'pro'
        # elif score > grid_size * 6:
        #     achievement = 'god'
        # elif score > grid_size * 7:
        #     achievement = 'baka'
        score_str = f'Score: {score}'

        if self.font is None:
            self.font = pygame.font.Font(None, self.toolbar_width // len(score_str) * 2)
        score_text = self.font.render(score_str, True, COLORS_EMPTY, COLORS_LINES)

        self.screen.blit(score_text, (self.window_height + 10, 10))
