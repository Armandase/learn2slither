import pygame
from src.constants import W_WIDTH, W_HEIGHT, DEFAULT_SIZE, TITLE, \
    TAIL, HEAD, GREEN_APPLE, RED_APPLE, WALL, \
    COLORS_RED_APPLE, COLORS_GREEN_APPLE, COLORS_SNAKE, COLORS_WALL, \
    COLORS_EMPTY, COLORS_LINES, COLORS_TOOLBAR, COLORS_SNAKE_HEAD, \
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

        # Redimensionne les images à la taille des cases de la grille
        self.img_snake_head = pygame.transform.scale(
            self.img_snake_head, (self.ratio, self.ratio))
        self.img_snake_tail = pygame.transform.scale(
            self.img_snake_tail, (self.ratio, self.ratio))
        self.img_red_apple = pygame.transform.scale(
            self.img_red_apple, (self.ratio, self.ratio))
        self.img_green_apple = pygame.transform.scale(
            self.img_green_apple, (self.ratio, self.ratio))

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
        self.display_text(speed_str, (self.window_height + 10, self.button_height * 2))
        
        if epoch is not None and epochs is not None:
            epoch_str = f"Epoch: {epoch + 1}/{epochs}"
            self.display_text(epoch_str, (self.window_height + 10, self.button_height * 3))        

    def display_text(self, text, coords ):
        if self.font is None:
            self.font = pygame.font.Font(None, int(self.button_height * 1.25))

        speed_txt = self.font.render(text, True,
                                        COLORS_EMPTY, COLORS_LINES)

        self.screen.blit(speed_txt,
                         coords)

    def mean_scores(self, scores):
        length_block = len(scores) // 10
        complement = len(scores) % 10

        avg_scores = []

        for i in range(10):
            if i < complement:
                avg_scores.append(sum(scores[
                    (i * length_block) + i:((i + 1) * length_block) + i]))
            else:
                avg_scores.append(sum(
                    scores[i * length_block:(i + 1) * length_block]))
        return avg_scores

    def display_curve(self, scores):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.backends.backend_agg as agg
        import pylab

        fig = pylab.figure(figsize=[4, 4], dpi=self.button_height,)
        ax = fig.gca()
        # if len(scores) > 10:
            # ax.plot(self.mean_scores(scores))
        # else:
        ax.plot(scores)
        ax.set_title("Mobile average")

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.screen.blit(surf, (self.window_height + 20,
                                self.window_height - self.button_height * 4))
        matplotlib.pyplot.close()
