import argparse

from src.Render import Render
from src.Grid import Grid
from src.game import main_loop, train_agent
from src.constants import DEFAULT_SIZE, EPOCHS, DEFAULT_VISUAL
from src.SnakeAgent import SnakeAgent


def main(size=DEFAULT_SIZE, epochs=EPOCHS, visual_mode=DEFAULT_VISUAL,
         model=None, train=True, verbose=False, step_by_step=False):

    grid = Grid(size)
    agent = SnakeAgent(grid.get_grid_size(), train, model)
    # agent.load_model(model)
    if visual_mode is False:
        train_agent(agent, grid, None, epochs, visual_mode, verbose)
    else:
        render = Render(size)
        main_loop(render, grid, epochs,
                  agent, visual_mode, verbose, step_by_step)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--size', '-s', type=int, default=DEFAULT_SIZE)
    argparser.add_argument('--epochs', '-e', type=int, default=EPOCHS)
    argparser.add_argument('--model', '-m', type=str, default=None)
    argparser.add_argument('--train', default=True,
                           action=argparse.BooleanOptionalAction)
    argparser.add_argument('--verbose', default=False,
                           action=argparse.BooleanOptionalAction)
    argparser.add_argument('--visual', default=True,
                           action=argparse.BooleanOptionalAction)
    argparser.add_argument('--step_by_step', default=False,
                           action=argparse.BooleanOptionalAction)

    try:
        args = argparser.parse_args()

        main(args.size, args.epochs, args.visual,
             args.model, args.train, args.verbose, args.step_by_step)
    except Exception as e:
        print('Error:', e)
