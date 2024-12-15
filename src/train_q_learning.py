import torch #pytorch
import numpy as np #numpy
from deep_q_learning import Linear_QNet, QTrainer #importing the neural net from step 2

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001 #learning rate


def get_model():
    n_games = 0
    epsilon = 0  # randomness
    gamma = 0.9  # discount rate
    model = Linear_QNet(11, 256, 3) #input size, hidden size, output size
    trainer = QTrainer(model, lr=LR, gamma=gamma)

def get_action(self, state):
    if np.random.rand() < self.eps:
        return np.random.randint(0, 4)
    else:
        return np.argmax(self.q_table[tuple(state)])

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)