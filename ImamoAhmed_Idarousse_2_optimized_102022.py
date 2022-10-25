import csv
import timeit


def get_actions_from_csv(file_csv):
    actions = []
    with open(file_csv, "r") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        for row in reader:
            if float(row[1]) > 0.0 < float(row[2]):
                action = (
                    row[0],
                    float(row[1]),
                    float(row[2]),
                    round(float((float(row[1]) * float(row[2])) / 100), 2),
                )
                actions.append(action)

    return actions


def get_best_combination(file_csv):
    stock_purchase_budget = 500
    list_best_combination = []
    actions = get_actions_from_csv(file_csv)
    matrix_table = [
        [0 for budget_line in range(stock_purchase_budget + 1)]
        for action_line in range(len(actions) + 1)
    ]
    for browse_stocks in range(1, len(actions) + 1):
        for brows_budget in range(1, stock_purchase_budget + 1):
            if actions[browse_stocks - 1][1] <= brows_budget:
                matrix_table[browse_stocks][brows_budget] = max(
                    actions[browse_stocks - 1][3]
                    + float(
                        matrix_table[browse_stocks - 1][
                            round(brows_budget - actions[browse_stocks - 1][1])
                        ]
                    ),
                    matrix_table[browse_stocks - 1][round(brows_budget)],
                )

            else:
                matrix_table[browse_stocks][round(brows_budget)] = round(
                    matrix_table[browse_stocks - 1][round(brows_budget)]
                )

    numbers_actions = len(actions)

    while stock_purchase_budget >= 0 and numbers_actions >= 0:
        action = actions[numbers_actions - 1]

        if (
            matrix_table[numbers_actions][round(stock_purchase_budget)]
            == matrix_table[numbers_actions - 1][
                round(stock_purchase_budget - action[1])
            ]
            + action[3]
        ):
            list_best_combination.append(action)
            stock_purchase_budget -= action[1]
        numbers_actions -= 1

    return (list_best_combination, matrix_table[-1][-1], 500 - stock_purchase_budget)


def display_result(file_csv):

    results = get_best_combination(file_csv)
    numbers = 20
    result_time = timeit.timeit(
        stmt=f"get_best_combination('{file_csv}')",
        setup="from __main__ import get_best_combination",
        number=numbers,
    )
    times = result_time / numbers
    print(f"la meilleur combinaison d'action est:\n{results[0]}\n")
    print(f"le prix d'achat de la combinaison est de:\n{results[2]:.2f}€\n")
    print(f"le bénéfice pour l'achat de ces actions est de:\n{results[1]:.2f}€\n")
    print(f"Le temps de lancemant du programme est de:\n{times:.2f} secondes\n")


display_result("data/actions_p7.csv")
display_result("data/dataset1_Python+P7.csv")
display_result("data/dataset2_Python+P7.csv")
