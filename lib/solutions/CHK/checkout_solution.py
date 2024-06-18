import re
from collections import Counter

TABLE = """
+------+-------+------------------------+
| Item | Price | Special offers         |
+------+-------+------------------------+
| A    | 50    | 3A for 130, 5A for 200 |
| B    | 30    | 2B for 45              |
| C    | 20    |                        |
| D    | 15    |                        |
| E    | 40    | 2E get one B free      |
| F    | 10    | 2F get one F free      |
| G    | 20    |                        |
| H    | 10    | 5H for 45, 10H for 80  |
| I    | 35    |                        |
| J    | 60    |                        |
| K    | 80    | 2K for 150             |
| L    | 90    |                        |
| M    | 15    |                        |
| N    | 40    | 3N get one M free      |
| O    | 10    |                        |
| P    | 50    | 5P for 200             |
| Q    | 30    | 3Q for 80              |
| R    | 50    | 3R get one Q free      |
| S    | 30    |                        |
| T    | 20    |                        |
| U    | 40    | 3U get one U free      |
| V    | 50    | 2V for 90, 3V for 130  |
| W    | 20    |                        |
| X    | 90    |                        |
| Y    | 10    |                        |
| Z    | 50    |                        |
+------+-------+------------------------+
"""


def get_tables(s: str):
    pattern = re.compile(r"([A-Z])\s+\|\s+(\d+)\s+\|(.+)")
    lines = s.strip().split("\n")

    out = []
    for line in lines:
        m = pattern.match(line)
        if m:
            out.append(
                {
                    "sku": m.group(1),
                    "price": int(m.group(2)),
                    "deal": m.group(3).strip(),
                }
            )

    return out


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    t = get_tables(TABLE)

    table = [{x["sku"]: x["price"]} for x in t]

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

    # for every 2 F, get an F free
    counter["F"] -= counter["F"] // 3

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
