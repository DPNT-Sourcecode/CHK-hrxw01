from collections import Counter


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    table = {"A": 50, "B": 30, "C": 20, "D": 15}

    counter = Counter(skus.split(","))

    # 3A is 130
    total_a = (counter["A"] // 3) * 130 + (counter["A"] % 3) * table["A"]

    # 2B is 45
    total_b = (counter["B"] // 2) * 45 + (counter["B"] % 2) * table["B"]

    total = total_a + total_b + counter["C"] * table["C"] + counter["D"] * table["D"]

    return total


