import pygame

from src.utils import dir_from_keys, analyse_scores, display_learning_curve
from src.constants import GAME_SPEED, DEAD, WALL, TAIL
from src.SnakeAgent import SnakeAgent
from src.Grid import Grid
from src.interpreter import game_state, step


def train_agent(agent, grid, render, epochs):
    scores = []
    epoch = 0
    running = False
    while epoch < epochs and not running:
        agent.reset()
        grid.reset_grid()
        # agent.set_prev_stat(game_state(grid))
        current_state = game_state(grid)
        agent.update_epsilon()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display_learning_curve(scores)
                    exit()
            action = agent.get_action(current_state)
            reward, done = step(action, grid)
            next_state = game_state(grid)

            # self.update_q_table(state, action, reward, next_state)
            agent.update_q_table(current_state, action, reward, next_state)
            current_state = next_state
            length = grid.get_snake_len()

            render.draw_grid(grid.board)
            render.display_toolbar(length, grid.get_grid_size())

            keys = pygame.key.get_pressed()
            if handle_keys(keys, grid) is False:
                # running = False
                display_learning_curve(scores)
                exit()

            clock.tick(GAME_SPEED + length // 3)

            pygame.display.flip()
        epoch += 1
        scores.append(agent.score)
        print(f"Epoch {epoch + 1}/{epochs}")
        print(f"Score: {agent.score}")
        print(f"Steps: {agent.steps}")
        print(f"Epsilon: {agent.eps}")
        print()
    analyse_scores(scores)
    display_learning_curve(scores)


def main_loop(render, grid, epochs, agent):
    # global clock
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        # train_agent(agent, grid, render, epochs)
        if keys[pygame.K_SPACE]:
            train_agent(agent, grid, render, epochs)
        if keys[pygame.K_ESCAPE]:
            running = False

        next_dir = dir_from_keys(keys, grid)
        new_case = grid.update_board(next_dir)

        if new_case == DEAD or new_case == WALL or new_case == TAIL:
            print("Game over")
            running = False
        
        render.draw_grid(grid.board)
        render.display_toolbar(grid.get_snake_len(), grid.get_grid_size())

        clock.tick(GAME_SPEED + (grid.get_snake_len() // 3))
        pygame.display.flip()

