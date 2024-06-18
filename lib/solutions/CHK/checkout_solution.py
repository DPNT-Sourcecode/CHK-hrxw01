from collections import Counter


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    table = {"A": 50, "B": 30, "C": 20, "D": 15}

    # ..yep
    print(skus)
    counter = Counter([*skus])

    # keys of counter should be a subset of table
    if not set(counter.keys()).issubset(set(table.keys())):
        return -1

    # first process free items
    # for every 2 E, get a B free
    counter["B"] -= counter["E"] // 2

    # 3A is 130
    total_a = (counter["A"] // 3) * 130 + (counter["A"] % 3) * table["A"]

    # 2B is 45
    total_b = (counter["B"] // 2) * 45 + (counter["B"] % 2) * table["B"]

    total = total_a + total_b + counter["C"] * table["C"] + counter["D"] * table["D"]

    return total

