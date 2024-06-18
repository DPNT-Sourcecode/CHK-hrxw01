from collections import Counter


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    table = {"A": 50, "B": 30, "C": 20, "D": 15}

    multi = {"A": [(5, 200), (3, 130)], "B": [(2, 45)]}

    # ..yep
    print(skus)
    counter = Counter([*skus])

    # keys of counter should be a subset of table
    if not set(counter.keys()).issubset(set(table.keys())):
        return -1

    # first process free items
    # for every 2 E, get a B free
    counter["B"] -= counter["E"] // 2

    # now process the multi-prices
    # to work out a price for a letter with deals, apply the deal price with highest number of items
    # then apply the deal price with the next highest number of items, and so on

    total = 0
    for sku, count in counter.items():
        if sku not in multi:
            total += count * table[sku]
            continue

        for deal_count, deal_price in multi[sku]:
            while count >= deal_count:
                count -= deal_count
                total += deal_price

        if count > 0:
            total += count * table[sku]

    return total




