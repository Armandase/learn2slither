import pygame
from src.constants import W_WIDTH, W_HEIGHT, DEFAULT_SIZE, TITLE, \
    TAIL, HEAD, GREEN_APPLE, RED_APPLE, WALL, \
    COLORS_EMPTY, COLORS_LINES, COLORS_WALL, \
    IMAGE_PATH, GAME_SPEED


class Render():
    def __init__(self,
                 grid_size=DEFAULT_SIZE,
                 w_width=W_WIDTH, w_height=W_HEIGHT):
        pygame.init()
        self.screen = pygame.display.set_mode((w_width, w_height))
        pygame.display.set_caption(TITLE)
        self.window_width = w_width
        self.window_height = w_height
        self.ratio = w_height / (grid_size + 2)
        self.font = None
        self.toolbar_width = self.window_width - self.window_height
        self.button_height = self.window_height // 25
        self.load_image()

    def __del__(self):
        pygame.quit()

    def load_image(self, path=IMAGE_PATH):
        self.img_snake_head = pygame.image.load(f'{IMAGE_PATH}/snake_head.png')
        self.img_snake_tail = pygame.image.load(f'{IMAGE_PATH}/snake_tail.png')
        self.img_red_apple = pygame.image.load(f'{IMAGE_PATH}/red_apple.png')
        self.img_green_apple = pygame.image.load(
            f'{IMAGE_PATH}/green_apple.png')
        self.img_play_game = pygame.image.load(f'{IMAGE_PATH}/play_game.jpg')
        self.img_game_over = pygame.image.load(f'{IMAGE_PATH}/game_over.jpg')

        # Redimensionne les images à la taille des cases de la grille
        self.img_snake_head = pygame.transform.scale(
            self.img_snake_head, (self.ratio, self.ratio))
        self.img_snake_tail = pygame.transform.scale(
            self.img_snake_tail, (self.ratio, self.ratio))
        self.img_red_apple = pygame.transform.scale(
            self.img_red_apple, (self.ratio, self.ratio))
        self.img_green_apple = pygame.transform.scale(
            self.img_green_apple, (self.ratio, self.ratio))
        self.img_play_game = pygame.transform.scale(
            self.img_play_game, (self.window_width, self.window_height))
        self.img_game_over = pygame.transform.scale(
            self.img_game_over, (self.window_width, self.window_height))

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
                x, y = col * self.ratio, row * self.ratio

                if grid[row, col] == HEAD:
                    self.screen.blit(self.img_snake_head, (x, y))
                elif grid[row, col] == TAIL:
                    self.screen.blit(self.img_snake_tail, (x, y))
                elif grid[row, col] == RED_APPLE:
                    self.screen.blit(self.img_red_apple, (x, y))
                elif grid[row, col] == GREEN_APPLE:
                    self.screen.blit(self.img_green_apple, (x, y))
                elif grid[row, col] == WALL:
                    rect = pygame.Rect(x, y, self.ratio, self.ratio)
                    pygame.draw.rect(self.screen, COLORS_WALL, rect)
                else:
                    rect = pygame.Rect(x, y, self.ratio, self.ratio)
                    pygame.draw.rect(self.screen, COLORS_EMPTY, rect)

                pygame.draw.rect(self.screen, COLORS_LINES,
                                 pygame.Rect(x, y, self.ratio, self.ratio), 1)

    def display_toolbar(self, score, epoch=None, epochs=None):
        rect = pygame.Rect(
                    self.window_height, 0,
                    self.toolbar_width, self.window_height
                )
        pygame.draw.rect(self.screen, COLORS_LINES, rect)

        score_str = f'Score: {score}'
        self.display_text(score_str, (self.window_height + 10, 10))

        speed_str = f"Speed: {GAME_SPEED}"
        self.display_text(speed_str, (
            self.window_height + 10, self.button_height * 2))

        if epoch is not None and epochs is not None:
            epoch_str = f"Epoch: {epoch + 1}/{epochs}"
            self.display_text(epoch_str, (
                self.window_height + 10, self.button_height * 3))

    def display_text(self, text, coords):
        if self.font is None:
            self.font = pygame.font.Font(None, int(self.button_height * 1.25))

        speed_txt = self.font.render(text,
                                     True, COLORS_EMPTY, COLORS_LINES)

        self.screen.blit(speed_txt,
                         coords)

    def display_curve(self, scores):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.backends.backend_agg as agg
        import pylab

        fig = pylab.figure(figsize=[4, 4], dpi=self.button_height * 2,)
        ax = fig.gca()

        ax.plot(scores)
        ax.set_title("Scores over epochs")
        ax.set_xlabel("Epochs")
        ax.set_ylabel("Scores")

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.screen.blit(surf, (self.window_height + 20,
                                self.button_height * 6))
        matplotlib.pyplot.close()

    def display_begin(self):
        self.screen.blit(self.img_play_game, (0, 0))
        pygame.display.flip()

    def display_game_over(self):
        self.screen.blit(self.img_game_over, (0, 0))
        pygame.display.flip()
