
import time
import csv
from itertools import combinations


def get_actions_from_csv():
    actions = []
    with open("data/actions_p7.csv", "r") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        for row in reader:
            action = (row[0], float(row[1]), float(row[2]))
            actions.append(action)
    return actions


def generate_combinations():
    actions = get_actions_from_csv()
    for nb_actions in range(1, len(actions) + 1):
        for combination in combinations(actions, nb_actions):
            yield combination


def get_best_combination():
    best_combination = None
    max_money = 0
    total_cost_actions = 0
    total_action_profitability = 0
    for combination in generate_combinations():
        for action in combination:
            total_cost_actions = total_cost_actions + action[1]
            action_profitability = action[1] * action[2] / 100
            total_action_profitability = (
                total_action_profitability + action_profitability
            )
            if total_cost_actions <= 500 and action == combination[-1]:
                total_cost_actions = 0
                if total_action_profitability > max_money:
                    best_combination = combination
                    max_money = total_action_profitability
                    total_action_profitability = 0
                else:
                    total_action_profitability = 0
            elif total_cost_actions >= 500 and action == combination[-1]:
                total_cost_actions = 0
                total_action_profitability = 0
        pass
    end_time = time.time() - start_time
    print(f"La meilleure combinaison est: {best_combination} ")
    print(f"La rentabilité de cette combinaison est: {round(max_money,2)} €")
    print(f"le temps d'exectution du code est de: {round(end_time,2)} secondes")
    return best_combination, max_money


start_time = time.time()
get_best_combination()
