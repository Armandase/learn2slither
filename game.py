import pygame

from src.utils import handle_keys
from src.constants import GAME_SPEED
from src.Interpreter import snake_vision, print_snake_vision


def main_loop(render, grid):
    clock = pygame.time.Clock()
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        score = grid.get_snake_len()

        render.draw_grid(grid.board)
        render.display_toolbar(score, grid.get_grid_size())

        state = snake_vision(grid)
        print_snake_vision(state, grid)
        
        keys = pygame.key.get_pressed()
        if handle_keys(keys, grid) is False:
            running = False

        clock.tick(GAME_SPEED + score // 3)

        pygame.display.flip()

