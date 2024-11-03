import pygame

from src.utils import handle_keys
from src.constants import GAME_SPEED
from src.SnakeAgent import SnakeAgent


def main_loop(render, grid, epochs):
    clock = pygame.time.Clock()
    running = True
    agent = SnakeAgent()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        score = grid.get_snake_len()

        render.draw_grid(grid.board)
        render.display_toolbar(score, grid.get_grid_size())
        agent.train(epochs, grid)

        keys = pygame.key.get_pressed()
        if handle_keys(keys, grid) is False:
            running = False

        clock.tick(GAME_SPEED + score // 3)

        pygame.display.flip()

