import re
from collections import Counter

TABLE = """
+------+-------+---------------------------------+
| Item | Price | Special offers                  |
+------+-------+---------------------------------+
| A    | 50    | 3A for 130, 5A for 200          |
| B    | 30    | 2B for 45                       |
| C    | 20    |                                 |
| D    | 15    |                                 |
| E    | 40    | 2E get one B free               |
| F    | 10    | 2F get one F free               |
| G    | 20    |                                 |
| H    | 10    | 5H for 45, 10H for 80           |
| I    | 35    |                                 |
| J    | 60    |                                 |
| K    | 70    | 2K for 120                      |
| L    | 90    |                                 |
| M    | 15    |                                 |
| N    | 40    | 3N get one M free               |
| O    | 10    |                                 |
| P    | 50    | 5P for 200                      |
| Q    | 30    | 3Q for 80                       |
| R    | 50    | 3R get one Q free               |
| S    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
| T    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
| U    | 40    | 3U get one U free               |
| V    | 50    | 2V for 90, 3V for 130           |
| W    | 20    |                                 |
| X    | 17    | buy any 3 of (S,T,X,Y,Z) for 45 |
| Y    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
| Z    | 21    | buy any 3 of (S,T,X,Y,Z) for 45 |
+------+-------+---------------------------------+
"""

PATTERN = re.compile(r"\|\s+([A-Z])\s+\|\s+(\d+)\s+\|(.+)")
MULTI_DEAL_PATTERN = re.compile(r"(\d)([A-Z]) for (\d+)")


def get_tables(s: str):
    lines = s.strip().split("\n")

    out = []
    for line in lines:
        m = PATTERN.match(line)
        if m:
            out.append(
                {
                    "sku": m.group(1),
                    "price": int(m.group(2)),
                    "deal": m.group(3).strip(),
                }
            )

    multi = {}
    for x in out:
        if x["deal"]:
            deals = x["deal"].split(",")
            for deal in deals:
                if m := MULTI_DEAL_PATTERN.match(deal.strip()):
                    if x["sku"] not in multi:
                        multi[x["sku"]] = []
                    multi[x["sku"]].append((int(m.group(1)), int(m.group(3))))

    table = {x["sku"]: x["price"] for x in out}
    print(multi)

    # todo maybe parse the deal out later
    return table, multi


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    table, multi = get_tables(TABLE)

    # multi = {
    #     "A": [(5, 200), (3, 130)],
    #     "B": [(2, 45)],
    #     "H": [(10, 80), (5, 45)],
    #     "K": [(2, 150)],
    #     "P": [(5, 200)],
    #     "Q": [(3, 80)],
    #     "V": [(3, 130), (2, 90)],
    # }

    counter = Counter([*skus])

    # validate skus
    if not set(counter.keys()).issubset(set(table.keys())):
        return -1

    # first process free items
    # for every 2 E, get a B free
    counter["B"] -= counter.get("E", 0) // 2

    # for every 3 N, get an M free
    counter["M"] -= counter.get("N", 0) // 3

    # for every 3 R, get a Q free
    counter["Q"] -= counter.get("R", 0) // 3

    # for every 2 F, get an F free
    counter["F"] -= counter.get("F", 0) // 3

    # for every 3 U, get a U free
    counter["U"] -= counter.get("U", 0) // 4

    # now process the multi-prices
    # to work out a price for a letter with deals, apply the deal price with highest number of items
    # then apply the deal price with the next highest number of items, and so on

    total = 0
    for sku, count in counter.items():
        if count <= 0:
            continue

        if sku not in multi:
            total += count * table.get(sku, 0)
            continue

        for deal_count, deal_price in multi[sku]:
            while count >= deal_count:
                count -= deal_count
                total += deal_price

        if count > 0:
            total += count * table[sku]

    return total


