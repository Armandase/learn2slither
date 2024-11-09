import numpy as np
from prettytable import PrettyTable
from src.constants import MODELS_PATH


def display_training_info(epochs, epoch, every_length, every_reward):
    if epoch % 25 != 0:
        return
    mean_length = sum(every_length) / len(every_length)
    mean_reward = sum(every_reward) / len(every_reward)
    table = PrettyTable()
    table.title = f"Epochs {epoch}/{epochs}"
    table.field_names = ["Length", "Reward"]
    table.add_row([mean_length, mean_reward])
    every_length.clear()
    every_reward.clear()
    print(table)


def save_q_table(q_table, nb_epoch, scores, path=MODELS_PATH):
    path = f"{path}/q_table_e{nb_epoch}.npy"
    np.save(path, q_table)
    print(f"Q-table saved at {path}")
