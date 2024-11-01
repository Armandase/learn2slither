import argparse

from Render import Render
from Grid import Grid
from game import main_loop
from constants import DEFAULT_SIZE, WINDOW_SIZE


def main(size=DEFAULT_SIZE, window_size=WINDOW_SIZE):
    grid = Grid(size)
    render = Render(window_size)

    main_loop(render, grid)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--size', '-s', type=int, default=DEFAULT_SIZE)
    argparser.add_argument('--window_size', '-ws',
                           type=int, default=WINDOW_SIZE)
    args = argparser.parse_args()
    # try:
    main(args.size, args.window_size)
    # except Exception as e:
        # print('Error:', e)
