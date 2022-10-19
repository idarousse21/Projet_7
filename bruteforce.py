import csv
from itertools import combinations
import timeit


def get_actions_from_csv():
    actions = []
    with open("data/actions_p7.csv", "r") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        for row in reader:
            if float(row[1]) > 0.0 < float(row[2]):
                action = (
                    row[0],
                    float(row[1]),
                    float((float(row[1]) * float(row[2])) / 100),
                )
                actions.append(action)

    return actions


def generate_combinations():
    actions = get_actions_from_csv()
    for nb_actions in range(1, len(actions) + 1):
        for combination in combinations(actions, nb_actions):
            yield combination


def get_best_combination():
    stock_purchase_budget = 500
    best_combination = None
    max_money = 0
    for combination in generate_combinations():
        total_cost_actions = 0
        total_action_profitability = 0
        for action in combination:
            total_cost_actions += action[1]
            if total_cost_actions > stock_purchase_budget:
                break
            action_profitability = action[2]
            total_action_profitability += action_profitability
        if (
            total_cost_actions <= stock_purchase_budget
            and total_action_profitability > max_money
        ):
            best_combination = combination
            max_money = total_action_profitability
            total_cost_best_action = total_cost_actions
    return best_combination, total_cost_best_action, max_money


result = get_best_combination()
numbers = 10
result_time = timeit.timeit(
    stmt="get_best_combination()",
    setup="from __main__ import get_best_combination",
    number=numbers,
)
times = result_time / numbers

print(f"la meilleur combinaison d'action est:\n{result[0]}\n")
print(f"le prix d'achat de la combinaison est de:\n{result[1]:.2f}€\n")
print(f"le bénéfice pour l'achat de ces actions est de:\n{result[2]:.2f}€\n")
print(f"Le temps de lancemant du programme est de:\n{times:.2f} secondes")
