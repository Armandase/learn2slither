import argparse

from src.Render import Render
from src.Grid import Grid
from src.game import main_loop, train_agent
from src.constants import DEFAULT_SIZE, W_HEIGHT, W_WIDTH, EPOCHS, DEFAULT_VISUAL
from src.SnakeAgent import SnakeAgent


def main(size=DEFAULT_SIZE, window_width=W_HEIGHT,
         window_height=W_WIDTH, epochs=EPOCHS, visual_mode=DEFAULT_VISUAL):
    if window_height > window_width:
        raise Exception("Window height should inferior than width")
    if window_width - window_height < window_width * 0.1:
        raise Exception("The minimal ratio between window width and height isn't respected")

    grid = Grid(size)
    agent = SnakeAgent(grid.get_grid_size())

    if visual_mode is False:
        train_agent(agent, grid, None, epochs, visual_mode)
        return

    render = Render(window_width, window_height, size)
    main_loop(render, grid, epochs, agent, visual_mode)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--size', '-s', type=int, default=DEFAULT_SIZE)
    argparser.add_argument('--visual', '-v', type=str, default="yes")
    argparser.add_argument('--epochs', '-e', type=int, default=EPOCHS)
    argparser.add_argument('--window_width', '-ww',
                           type=int, default=W_WIDTH)
    argparser.add_argument('--window_height', '-wh',
                           type=int, default=W_HEIGHT)
    args = argparser.parse_args()
    # try:
    visual_mode = DEFAULT_VISUAL
    if args.visual == "yes":
        visual_mode = True
    elif args.visual == "no":
        visual_mode = False
    else:
        print("Visual modal should be yes(enable) or no (disable)")
        exit(1)

    main(args.size, args.window_width, args.window_height, args.epochs, visual_mode)
    # except Exception as e:
        # print('Error:', e)
