import argparse

from Render import Render
from Grid import Grid
from game import main_loop
from constants import DEFAULT_SIZE, W_HEIGHT, W_WIDTH, EPOCHS


def main(size=DEFAULT_SIZE, window_width=W_HEIGHT, window_height=W_WIDTH, epochs=EPOCHS):
    if window_height > window_width:
        raise Exception("Window height should inferior than width")
    if window_width - window_height < window_width * 0.1:
        raise Exception("The minimal ratio between window width and height isn't respected")
    grid = Grid(size)
    render = Render(window_width, window_height, size)

    main_loop(render, grid)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--size', '-s', type=int, default=DEFAULT_SIZE)
    argparser.add_argument('--epochs', '-e', type=int, default=EPOCHS)
    argparser.add_argument('--window_width', '-ww',
                           type=int, default=W_WIDTH)
    argparser.add_argument('--window_height', '-wh',
                           type=int, default=W_HEIGHT)
    args = argparser.parse_args()
    # try:
    main(args.size, args.window_width, args.window_height, args.epochs)
    # except Exception as e:
        # print('Error:', e)
