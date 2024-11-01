import numpy as np
import random
from collections import deque
from constants import DEFAULT_SIZE, HEAD, TAIL, GREEN_APPLE, RED_APPLE, EMPTY
from constants import UP, DOWN, LEFT, RIGHT
from utils import dir_to_point


class Grid():
    def __init__(self, size=DEFAULT_SIZE):
        self.grid_size = size
        self.current_dir = None

        self.board = np.zeros((size, size))

        self.snake = deque()
        self.init_snake()

        self.board[tuple(self.generate_empty_pos())] = GREEN_APPLE
        self.board[tuple(self.generate_empty_pos())] = GREEN_APPLE
        self.board[tuple(self.generate_empty_pos())] = RED_APPLE

    def init_snake(self):
        self.head_pos = np.random.randint(self.grid_size, size=2)
        self.board[tuple(self.head_pos)] = HEAD
        body = self.generate_around(self.head_pos)
        self.board[tuple(body)] = TAIL
        tail = self.generate_around(body)
        self.board[tuple(tail)] = TAIL
        self.snake.append(tail)
        self.snake.append(body)
        self.snake.append(self.head_pos)

    def generate_around(self, in_pos):
        def get_direction(value, limit):
            if value <= 0:
                return 1
            elif value >= limit - 1:
                return -1
            else:
                return random.choice([-1, 1])
        pos = in_pos.copy()
        if random.choice([0, 1]) == 0:
            pos[0] += get_direction(pos[0], self.grid_size)
        else:
            pos[1] += get_direction(pos[1], self.grid_size)
        return pos

    def generate_empty_pos(self):
        empty_pos = np.argwhere(self.board == 0)

        if empty_pos.size > 0:
            random_empty_position = empty_pos[np.random.choice(len(empty_pos))]
            return random_empty_position
        else:
            print("No empty positions available.")
        return None

    def get_grid_size(self):
        return (self.grid_size)

    def get_current_dir(self):
        return (self.current_dir)

    def update_board(self, next_dir):
        new_pos = dir_to_point(next_dir)
        self.head_pos = self.snake[-1] + new_pos

        checked_pos = self.check_move(self.head_pos)
        if checked_pos == -1:
            self.reset_grid()
            return

        if next_dir is None:
            return
        
        self.board[tuple(self.head_pos)] = HEAD
        self.board[tuple(self.snake[-1])] = TAIL
        if checked_pos == EMPTY:
            self.remove_tip_tail()
        elif checked_pos == GREEN_APPLE:
            # score ++
            self.board[tuple(self.generate_empty_pos())] = GREEN_APPLE
            pass
        elif checked_pos == RED_APPLE:
            self.remove_tip_tail()
            self.remove_tip_tail()
            self.board[tuple(self.generate_empty_pos())] = RED_APPLE

        self.snake.append(self.head_pos)
        self.current_dir = next_dir

    def check_move(self, new_pos):
        if new_pos[0] < 0 or new_pos[0] >= self.grid_size \
                or new_pos[1] < 0 or new_pos[1] >= self.grid_size:
            return -1
        # if not (0 <= new_pos).all() or not (new_pos < self.grid_size).all():

        if self.board[tuple(new_pos)] == TAIL:
            return -1
        elif self.board[tuple(new_pos)] == GREEN_APPLE:
            return GREEN_APPLE
        elif self.board[tuple(new_pos)] == RED_APPLE:
            return RED_APPLE
        return EMPTY

    def reset_grid(self):
        self.board = np.zeros((self.grid_size, self.grid_size))

        self.snake = deque()
        self.init_snake()

        self.board[tuple(self.generate_empty_pos())] = GREEN_APPLE
        self.board[tuple(self.generate_empty_pos())] = GREEN_APPLE
        self.board[tuple(self.generate_empty_pos())] = RED_APPLE
        self.current_dir = None

    def remove_tip_tail(self):
        self.board[tuple(self.snake[0])] = EMPTY
        self.snake.popleft()
