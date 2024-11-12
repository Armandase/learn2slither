import numpy as np
from collections import deque
from src.constants import DEFAULT_SIZE, HEAD, TAIL, GREEN_APPLE, \
    RED_APPLE, EMPTY, DEAD, WALL
from src.utils import dir_to_point


class Grid():
    def __init__(self, size=DEFAULT_SIZE):
        # self.grid_size = size
        self.total_grid_size = size + 2
        self.current_dir = None

        self.board = np.zeros((self.total_grid_size, self.total_grid_size))

        self.snake = deque()
        self.init_board()

    def fill_border(self):
        self.board[0, :] = WALL
        self.board[-1, :] = WALL
        self.board[:, 0] = WALL
        self.board[:, -1] = WALL

    def init_board(self):
        self.fill_border()
        self.head_pos = self.generate_empty_pos()
        self.board[tuple(self.head_pos)] = HEAD
        body = self.generate_around(self.head_pos)
        if body is None:
            self.reset_grid()
            return
        self.board[tuple(body)] = TAIL
        tail = self.generate_around(body)
        if tail is None:
            self.reset_grid()
            return
        self.board[tuple(tail)] = TAIL
        self.snake.append(tail)
        self.snake.append(body)
        self.snake.append(self.head_pos)

        self.board[tuple(self.generate_empty_pos())] = GREEN_APPLE
        self.board[tuple(self.generate_empty_pos())] = GREEN_APPLE
        self.board[tuple(self.generate_empty_pos())] = RED_APPLE

    def generate_around(self, in_pos):
        pos = in_pos.copy()
        available_pos = []
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        for dx, dy in directions:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if 1 <= new_x < self.get_grid_size() - 1 \
                    and 1 <= new_y < self.get_grid_size() - 1 \
                    and self.board[(new_x, new_y)] == EMPTY:
                available_pos.append([new_x, new_y])

        if available_pos:
            pos = available_pos[np.random.choice(len(available_pos))]
        else:
            return None

        return pos

    def generate_empty_pos(self):
        empty_pos = np.argwhere(self.board == EMPTY)
        if empty_pos.size > 0:
            random_empty_position = empty_pos[np.random.choice(len(empty_pos))]
            return random_empty_position
        else:
            print("No empty positions available.")
        return None

    def get_grid_size(self):
        return (self.total_grid_size)

    def get_current_dir(self):
        return (self.current_dir)

    def get_board(self):
        return (self.board)

    def get_head_pos(self):
        return (self.head_pos)

    def update_board(self, next_dir):
        new_pos = dir_to_point(next_dir)
        # if self.current_dir is None \
        #   and (self.snake[-1] + new_pos == self.snake[-2]).all():
        #     return EMPTY

        self.head_pos = self.snake[-1] + new_pos
        checked_pos = self.check_move(self.head_pos)
        if checked_pos == DEAD:
            return DEAD

        if next_dir is None:
            return EMPTY

        self.board[tuple(self.head_pos)] = HEAD
        self.board[tuple(self.snake[-1])] = TAIL
        if checked_pos == EMPTY:
            self.remove_tip_tail()
        elif checked_pos == GREEN_APPLE:
            self.board[tuple(self.generate_empty_pos())] = GREEN_APPLE
        elif checked_pos == RED_APPLE:
            if len(self.snake) <= 1:
                return DEAD
            self.remove_tip_tail()
            self.remove_tip_tail()
            self.board[tuple(self.generate_empty_pos())] = RED_APPLE

        self.snake.append(self.head_pos)
        self.current_dir = next_dir
        return checked_pos

    def check_move(self, new_pos):
        # Check if the new position is out of bounds
        value_pos = self.board[tuple(new_pos)]
        if not (0 <= new_pos).all() \
            or not (new_pos < self.get_grid_size()).all() \
                or value_pos == WALL or value_pos == TAIL:
            return DEAD
        return value_pos

    def reset_grid(self):
        self.board = np.zeros((self.total_grid_size, self.total_grid_size))

        self.snake = deque()
        self.head_pos = None
        self.init_board()

        self.current_dir = None

    def remove_tip_tail(self):
        self.board[tuple(self.snake[0])] = EMPTY
        self.snake.popleft()

    def get_snake_len(self):
        return (len(self.snake))

    def get_snake(self):
        return (self.snake)
