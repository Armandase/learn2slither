import pygame

from utils import handle_keys
from constants import GAME_SPEED


def main_loop(render, grid):
    clock = pygame.time.Clock()
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        score = grid.get_snake_len()

        render.draw_grid(grid.board)
        render.display_score(score)

        keys = pygame.key.get_pressed()
        if handle_keys(keys, grid) is False:
            running = False

        pygame.display.flip()

        clock.tick(GAME_SPEED + score // 3)
