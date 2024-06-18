from collections import Counter


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    table = {"A": 50, "B": 30, "C": 20, "D": 15}

    counter = Counter(skus.split(","))

    raise NotImplementedError()

