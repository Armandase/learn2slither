import numpy as np
from prettytable import PrettyTable
from src.constants import MODELS_PATH, METRICS_CALLBACK


def display_training_info(epochs, epoch, sum_length, sum_reward):
    sum_length /= METRICS_CALLBACK
    sum_reward /= METRICS_CALLBACK
    table = PrettyTable()
    table.title = f"Epochs {epoch}/{epochs}"
    table.field_names = ["Length", "Reward"]
    table.add_row([sum_length, sum_reward])
    print(table)


def save_q_table(q_table, nb_epoch, path=MODELS_PATH):
    path = f"{path}q_table_e{nb_epoch}.npy"
    np.save(path, q_table)
    # print(f"Q-table saved at {path}")


def save_best_model(agent, score, path=MODELS_PATH):
    if agent.check_best_score(score) is False:
        return
    path = f"{path}/q_table_best_model.npy"
    np.save(path, agent.q_table)
    # print("New best models has been saved")
