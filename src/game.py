import pygame

from src.utils import dir_from_keys, analyse_scores, display_learning_curve, last_trained_model
from src.constants import GAME_SPEED, DEAD, WALL, TAIL
from src.SnakeAgent import SnakeAgent
from src.Grid import Grid
from src.interpreter import game_state, step
from src.callbacks import display_training_info, save_q_table


def train_agent(agent, grid, render, epochs):
    print("Training agent...")
    scores = []
    avg_length = []
    avg_reward = []
    epoch = 0
    running = False
    agent.load_model(last_trained_model())
    while epoch < epochs and not running:
        agent.reset()
        grid.reset_grid()
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

            # agent.update_q_table(current_state, action, reward, next_state)
            agent.update_metrics(reward)
            current_state = next_state
            length = grid.get_snake_len()

            render.draw_grid(grid.board)
            render.display_toolbar(length, grid.get_grid_size())

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                # running = False
                display_learning_curve(scores)
                exit()

            clock.tick(GAME_SPEED + length // 3)
            pygame.display.flip()
        avg_length.append(grid.get_snake_len())
        avg_reward.append(agent.score)
        display_training_info(epochs, epoch, avg_length, avg_reward)
        if epoch % 500 == 0:
            save_q_table(agent.q_table, epoch, scores)
        scores.append(agent.score)
        epoch += 1
    analyse_scores(scores)
    display_learning_curve(scores)


def main_loop(render, grid, epochs, agent):
    global clock
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

