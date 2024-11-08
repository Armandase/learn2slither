import numpy as np
from src.interpreter import game_state, step

class SnakeAgent():
    def __init__(self, grid_size):
        self.discount_rate = 0.95
        self.learning_rate = 0.01
        self.eps = 1.0
        self.eps_discount = 0.995
        self.min_eps = 0.001
        self.q_table = np.zeros((grid_size, 4))
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
            return np.argmax(q_table[np.argmax(state)])

    def update_epsilon(self):
        self.eps = max(self.min_eps, self.eps * self.eps_discount)
    # np.astype(next_state, np.int32)
    def update_q_table(self, current_state, action, reward, next_state):
        # current_state_idx = tuple(current_state.astype(np.int32))
        current_state_idx = np.max(current_state).astype(np.int32)
        # next_state_idx = tuple(next_state.astype(np.int32))
        next_state_idx = np.max(next_state).astype(np.int32)
        max_future_q = np.max(self.q_table[next_state_idx])
        # Bellman Equation Update
        self.q_table[current_state_idx][action] = (1 - self.learning_rate)\
            * self.q_table[current_state_idx][action] + self.learning_rate\
            * (reward + self.discount_rate * max_future_q)
        self.score += reward
        self.steps += 1
    def reset(self):
        self.prev_state = None
        self.prev_action = None
        self.score = 0
        self.steps = 0
    
    def set_prev_state(self, state):
        self.prev_state = state

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
            # print("SHAPE!:", next_state.shape)
            # print(f"Epoch {epoch + 1}/{epochs}")
            # print(f"Score: {self.score}")
            # print(f"Steps: {self.steps}")
            # print(f"Epsilon: {self.eps}")
            print()
        print("Training finished.")
        print()

    def test(self, epochs, grid):
        for epoch in range(epochs):
            self.reset()
            grid.reset_grid()
            self.state = game_state(grid)
            done = False
            while not done:
                action = self.get_action(self.state, self.q_table)
                reward, done = step(action, grid)
                next_state = game_state(grid)
                self.state = next_state
            print(f"Epoch {epoch + 1}/{epochs}")
            print(f"Score: {self.score}")
            print(f"Steps: {self.steps}")
            print()
