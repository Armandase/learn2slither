import pygame

from src.utils import handle_keys
from src.constants import GAME_SPEED
from src.SnakeAgent import SnakeAgent
from src.interpreter import game_state, step


def main_loop(render, grid, epochs, agent):
    clock = pygame.time.Clock()
    running = True

    while running:
        for epoch in range(epochs):
            agent.reset()
            grid.reset_grid()
            agent.state = game_state(grid)
            done = False
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                action = agent.get_action(agent.state, agent.q_table)
                reward, done = step(action, grid)
                next_state = game_state(grid)
                # self.update_q_table(state, action, reward, next_state)
                agent.update_q_table(agent.state, action, reward, next_state)
                agent.state = next_state

                score = grid.get_snake_len()

                render.draw_grid(grid.board)
                render.display_toolbar(score, grid.get_grid_size())

                # keys = pygame.key.get_pressed()
                # if handle_keys(keys, grid) is False:
                    # running = False

                clock.tick(GAME_SPEED + score // 3)

                pygame.display.flip()
            agent.update_epsilon()
            print(f"Epoch {epoch + 1}/{epochs}")
            print(f"Score: {agent.score}")
            print(f"Steps: {agent.steps}")
            print(f"Epsilon: {agent.eps}")
            print()

