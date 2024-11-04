import numpy as np
from src.interpreter import game_state, step

class SnakeAgent():
    def __init__(self):
        self.discount_rate = 0.95
        self.learning_rate = 0.1
        self.eps = 1.0
        self.eps_discount = 0.9992
        self.min_eps = 0.001
        self.q_table = np.zeros((11, 11, 4))
        self.prev_state = None
        self.prev_action = None
        self.score = 0
        self.steps = 0

    def get_action(self, state, q_table):
        # exploration
        if np.random.rand() < self.eps:
            return np.random.randint(0, 4)
        else:
            # exploitation
            return np.argmax(q_table[np.astype(state, np.int32)])

    def update_epsilon(self):
        self.eps = max(self.min_eps, self.eps * self.eps_discount)

    def update_q_table(self, current_state, action, reward, next_state):
        # if self.prev_state is not None:
        #     cumulative_reward = self.discount_rate * np.max(self.q_table[np.astype(next_state, np.int32)])
        #     calcul = self.learning_rate * (
        #         reward + cumulative_reward - self.q_table[np.astype(self.prev_state, np.int32), self.prev_action]
        #     )
        #     self.q_table[np.astype(self.prev_state, np.int32), self.prev_action] += calcul
        # self.prev_state = state
        self.q_table[current_state][action] = (1 - self.learning_rate)\
                            * self.q_table[np.astype(current_state, np.int32)][action] + self.learning_rate\
                            * (reward + self.discount_rate * max(self.q_table[np.astype(next_state, np.int32)]))
        self.prev_action = action
        self.score += reward
        self.steps += 1

    def reset(self):
        self.prev_state = None
        self.prev_action = None

    def train(self, epochs, grid):
        for epoch in range(epochs):
            self.reset()
            grid.reset_grid()
            self.state = game_state(grid)
            done = False
            while not done:
                action = self.get_action(self.state, self.q_table)
                reward, done = step(action, grid)
                next_state = game_state(grid)
                # self.update_q_table(state, action, reward, next_state)
                self.update_q_table(self.state, action, reward, next_state)
                self.state = next_state
            self.update_epsilon()
            print(f"Epoch {epoch + 1}/{epochs}")
            print(f"Score: {self.score}")
            print(f"Steps: {self.steps}")
            print(f"Epsilon: {self.eps}")
            print()
        print("Training finished.")
        print()

    def test(self, epochs, grid):
        for epoch in range(epochs):
            state = grid.reset_grid()
            self.reset()
            done = False
            while not done:
                action = self.get_action(state)
                _, done = step(action, grid)
                next_state = game_state(grid)
                state = next_state
            print(f"Epoch {epoch + 1}/{epochs}")
            print(f"Score: {self.get_score()}")
            print(f"Steps: {self.get_steps()}")
            print()
        print("Testing finished.")
        print()
