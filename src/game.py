import pygame

from src.utils import dir_from_keys, analyse_scores, \
    display_learning_curve, print_snake_vision
from src.constants import GAME_SPEED, DEAD, WALL, TAIL, \
    DEFAULT_VISUAL, DIR_MAP, METRICS_CALLBACK, SAVING_MODEL_STEP
from src.interpreter import game_state, step
from src.callbacks import display_training_info, save_q_table, save_best_model
from src.SnakeAgent import SnakeAgent
from src.Grid import Grid
from src.Render import Render
import time


def game_started(keys):
    return keys[pygame.K_UP] or keys[pygame.K_DOWN] or\
        keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]


def train_agent(agent: SnakeAgent, grid: Grid,
                render: Render, epochs: int,
                visual_mode=DEFAULT_VISUAL, verbose=False,
                step_by_step=False):
    scores = []
    sum_reward = 0
    sum_length = 0
    epoch = 0
    running = False
    step_trigger = False
    while epoch < epochs and not running:
        agent.reset()
        grid.reset_grid()
        current_state = game_state(grid)
        agent.update_epsilon()
        done = False
        while not done:
            if visual_mode is True:
                step_trigger = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        display_learning_curve(scores)
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            display_learning_curve(scores)
                            exit()
                        elif event.key == pygame.K_f and step_by_step:
                            step_trigger = True
                if step_by_step is True and step_trigger is False:
                    continue
            action = agent.get_action(current_state)
            if verbose is True:
                print(DIR_MAP[action])
                print_snake_vision(grid)
            reward, done = step(action, grid)
            next_state = game_state(grid)

            agent.update_q_table(current_state, action, reward, next_state)
            agent.update_metrics(reward)
            current_state = next_state
            length = grid.get_snake_len()

            if visual_mode is False:
                continue

            render.draw_grid(grid.board)
            render.display_toolbar(length, epoch, epochs)
            render.display_curve(scores)

            clock.tick(GAME_SPEED + length // 3)
            pygame.display.flip()

        sum_length += grid.get_snake_len()
        sum_reward += agent.score
        if epoch % METRICS_CALLBACK == 0:
            display_training_info(epochs, epoch, sum_length, sum_reward)
            sum_length = 0
            sum_reward = 0
        save_best_model(agent, agent.score)
        if epoch % SAVING_MODEL_STEP == 0:
            save_q_table(agent.q_table, epoch)
        scores.append(agent.score)
        epoch += 1
    analyse_scores(scores)
    display_learning_curve(scores)


def test_agent(agent: SnakeAgent, grid: Grid, render: Render,
               visual_mode=DEFAULT_VISUAL, verbose=False):
    agent.reset()
    grid.reset_grid()
    current_state = game_state(grid)
    done = False
    while not done:
        action = agent.get_true_action(current_state)
        if verbose is True:
            print(DIR_MAP[action])
            print_snake_vision(grid)
        _, done = step(action, grid)
        next_state = game_state(grid)

        current_state = next_state
        length = grid.get_snake_len()

        if visual_mode is False:
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        render.draw_grid(grid.board)
        render.display_toolbar(length, grid.get_grid_size())

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        clock.tick(GAME_SPEED + length // 3)
        pygame.display.flip()
    print("Final score:", agent.score)
    print("Final length:", grid.get_snake_len())
    print("Game over")
    agent.reset()
    grid.reset_grid()


def main_loop(render: Render, grid: Grid, epochs, agent: SnakeAgent,
              visual=DEFAULT_VISUAL, verbose=False, step_by_step=False):
    global clock
    clock = pygame.time.Clock()
    running = True

    started = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if game_started(keys):
            render.draw_grid(grid.board)
            render.display_toolbar(grid.get_snake_len())
            started = True

        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_SPACE] and agent.train_agent is True:
            started = True
            print('Training agent')
            train_agent(agent, grid, render, epochs,
                        visual, verbose, step_by_step)
        if keys[pygame.K_SPACE] and agent.train_agent is False:
            started = True
            print('Testing agent')
            test_agent(agent, grid, render, visual, verbose)

        if started is False:
            render.display_begin()
            continue
        if verbose is True:
            print_snake_vision(grid)
        next_dir = dir_from_keys(keys, grid)
        new_case = grid.update_board(next_dir)
        if new_case == DEAD or new_case == WALL or new_case == TAIL:
            render.display_game_over()
            print("Final score:", grid.get_snake_len())
            print("Game over")
            running = False
            time.sleep(1)
            break

        render.draw_grid(grid.board)
        render.display_toolbar(grid.get_snake_len())
        clock.tick(GAME_SPEED + (grid.get_snake_len() // 3))
        pygame.display.flip()
