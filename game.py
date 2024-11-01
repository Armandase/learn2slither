import pygame

from constants import FPS
from utils import handle_keys


def main_loop(render, grid):
    clock = pygame.time.Clock()
    running = True
    dt = 0
    # head_pos = pygame.Vector2(tuple(grid.get_head_pos()))

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        render.draw_grid(grid.board)

        keys = pygame.key.get_pressed()
        if handle_keys(keys, grid) is False:
            running = False

        pygame.display.flip()

        # clock.tick(10 + score // 5) 
        clock.tick(7) 

