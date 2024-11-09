import numpy as np
import random
import pickle
from src.interpreter import game_state, step
from src.constants import LEARNING_RATE, DISCOUNT_RATE, EPSILON, EPSILON_DISCOUNT, MIN_EPSILON

class SnakeAgent():
    def __init__(self, grid_size):
        self.discount_rate = 0.9
        self.learning_rate = 0.1
        self.eps = 0.1
        self.eps_discount = 0.995
        self.min_eps = 0.001
        self.q_table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))
        self.grid_size = grid_size
        self.prev_state = None
        self.score = 0
        self.steps = 0

    def get_score(self):
        return self.score

    def get_steps(self):
        return self.steps

    def get_action(self, state):
        if np.random.rand() < self.eps:
            return np.random.randint(0, 4)
        else:
            return np.argmax(self.q_table[tuple(state)])

    def update_epsilon(self):
        self.eps = max(self.min_eps, self.eps * self.eps_discount)

    def update_q_table(self, current_state, action, reward, next_state):
        current_state_tuple = tuple(current_state)
        next_state_tuple = tuple(next_state)

        max_future_q = np.max(self.q_table[next_state_tuple])

        current_q = self.q_table[current_state_tuple][action]

        self.q_table[current_state_tuple][action] = (1 - self.learning_rate)\
            * current_q + self.learning_rate\
            * (reward + self.discount_rate * max_future_q)

    def update_metrics(self, reward):
        self.score += reward
        self.steps += 1

    def reset(self):
        self.prev_state = None
        self.score = 0
        self.steps = 0

    def set_prev_state(self, state):
        self.prev_state = state

    def load_model(self, model_path):
        self.q_table = np.load(model_path)
