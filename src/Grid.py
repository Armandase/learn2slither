import numpy as np
from collections import deque
from src.constants import DEFAULT_SIZE, HEAD, TAIL, GREEN_APPLE, RED_APPLE, EMPTY, DEAD
from src.utils import dir_to_point


class Grid():
    def __init__(self, size=DEFAULT_SIZE):
        self.grid_size = size
        self.current_dir = None

        self.board = np.zeros((size, size))

        self.snake = deque()
        self.init_board()

    def init_board(self):
        self.head_pos = np.random.randint(self.grid_size, size=2)
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
            if 0 <= new_x < 10 and 0 <= new_y < 10 and self.board[(new_x, new_y)] == EMPTY:
                available_pos.append([new_x, new_y])

        if available_pos:
            pos = available_pos[np.random.choice(len(available_pos))]
        else:
            return None

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

    def get_board(self):
        return (self.board)

    def get_head_pos(self):
        return (self.head_pos)

    def update_board(self, next_dir):
        new_pos = dir_to_point(next_dir)
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
        if not (0 <= new_pos).all() or not (new_pos < self.grid_size).all() \
            or self.board[tuple(new_pos)] == TAIL:
            return DEAD
        return self.board[tuple(new_pos)]
        # elif self.board[tuple(new_pos)] == GREEN_APPLE:
        #     return GREEN_APPLE
        # elif self.board[tuple(new_pos)] == RED_APPLE:
        #     return RED_APPLE
        # return EMPTY

    def reset_grid(self):
        self.board = np.zeros((self.grid_size, self.grid_size))

        self.snake = deque()
        self.init_board()

        self.current_dir = None

    def remove_tip_tail(self):
        self.board[tuple(self.snake[0])] = EMPTY
        self.snake.popleft()

    def get_snake_len(self):
        return (len(self.snake))

    def get_snake(self):
        return (self.snake)