import numpy as np
import random
from src.interpreter import game_state, step
from src.constants import LEARNING_RATE, DISCOUNT_RATE, EPSILON, EPSILON_DISCOUNT, MIN_EPSILON

class SnakeAgent():
    def __init__(self, grid_size):
        self.discount_rate = 0.9
        self.learning_rate = 0.1
        self.eps = 1.0
        self.eps_discount = 0.995
        self.min_eps = 0.001
        # self.q_table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))
        # self.q_table = np.zeros((2**16, 4))
        self.q_table = np.zeros((3, 3, 4))
        self.grid_size = grid_size
        self.prev_state = None
        self.score = 0
        self.steps = 0

    def get_score(self):
        return self.score

    def get_steps(self):
        return self.steps

    def get_action(self, state):
        # exploration
        if np.random.rand() < self.eps:
            return random.randint(0, 3)
        else:
            return np.argmax(self.q_table[state[0][0]][state[1][1]][state[2][0]])
            # exploitation
            # return np.argmax(self.q_table[state])

    def update_epsilon(self):
        self.eps = max(self.min_eps, self.eps * self.eps_discount)

    # def update_q_table(self, current_state, action, reward, next_state):
    #     max_future_q = np.max(self.q_table[next_state])
    #     self.q_table[current_state][action] = (1 - self.learning_rate)\
    #         * self.q_table[current_state][action] + self.learning_rate\
    #         * (reward + self.discount_rate * max_future_q)

    #     self.score += reward
    #     self.steps += 1

    def update_q_table(self, state, action, reward, next_state):
        current_q = self.q_table[state[0][0]][state[1][1]][action]
        best_next_q = np.max(self.q_table[next_state[0][0]][next_state[1][1]])
        new_q = current_q + LEARNING_RATE * (reward + DISCOUNT_RATE * best_next_q - current_q)
        self.q_table[state[0][0]][state[1][1]][action] = new_q
        self.score += reward
        self.steps += 1


    def reset(self):
        self.prev_state = None
        self.score = 0
        self.steps = 0

    def set_prev_state(self, state):
        self.prev_state = state