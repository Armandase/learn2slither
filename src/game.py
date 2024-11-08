import pygame

from src.utils import handle_keys, analyse_scores, display_learning_curve
from src.constants import GAME_SPEED
from src.SnakeAgent import SnakeAgent
from src.interpreter import game_state, step


# for epoch in range(epochs):
#     self.reset()
#     grid.reset_grid()
#     self.state = game_state(grid)
#     done = False
#     while not done:
#         action = self.get_action(self.state, self.q_table)
#         reward, done = step(action, grid)
#         next_state = game_state(grid)
#         # self.update_q_table(state, action, reward, next_state)
#         self.update_q_table(self.state, action, reward, next_state)
#         self.state = next_state
#     self.update_epsilon()

def main_loop(render, grid, epochs, agent):
    clock = pygame.time.Clock()
    running = True

    while running:
        scores = []
        for epoch in range(epochs):
            agent.reset()
            grid.reset_grid()
            agent.set_prev_state(game_state(grid))
            done = False
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # running = False
                        display_learning_curve(scores)
                        exit()
                action = agent.get_action(agent.prev_state, agent.q_table)
                reward, done = step(action, grid)
                state = game_state(grid)
                agent.update_q_table(agent.prev_state, action, reward, state)
                agent.set_prev_state(state)
                # print("State:", state)
                # print("q_table:", agent.q_table)

                score = grid.get_snake_len()

                render.draw_grid(grid.board)
                render.display_toolbar(score, grid.get_grid_size())

                keys = pygame.key.get_pressed()
                if handle_keys(keys, grid) is False:
                    display_learning_curve(scores)
                    exit()

                clock.tick(GAME_SPEED + score // 3)

                pygame.display.flip()
            agent.update_epsilon()
            print(f"Epoch {epoch + 1}/{epochs}")
            print(f"Score: {agent.score}")
            scores.append(agent.score)
            print(f"Steps: {agent.steps}")
            print(f"Epsilon: {agent.eps}")
            print()

