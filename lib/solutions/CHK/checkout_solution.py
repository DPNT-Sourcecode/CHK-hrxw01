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
GET_ONE_PATTERN = re.compile(r"(\d)([A-Z]) get one ([A-Z]) free")
GROUP_DISCOUNT_PATTERN = re.compile(r"buy any 3 of \(S,T,X,Y,Z\) for 45")


def get_tables(s: str):
    lines = s.strip().split("\n")

    parsed_table = []
    for line in lines:
        m = PATTERN.match(line)
        if m:
            parsed_table.append(
                {
                    "sku": m.group(1),
                    "price": int(m.group(2)),
                    "deal": m.group(3).strip(),
                }
            )

    # parse the deals
    multi = {}
    get_one = []
    for x in parsed_table:
        if x["deal"]:
            deals = x["deal"].split(",")
            for deal in deals:
                if x["sku"] == "H":
                    print(deals)
                if m := MULTI_DEAL_PATTERN.match(deal.strip()):
                    if x["sku"] not in multi:
                        multi[x["sku"]] = []
                    multi[x["sku"]].append((int(m.group(1)), int(m.group(3))))
                if m := GET_ONE_PATTERN.match(deal.strip()):
                    source = m.group(2)
                    target = m.group(3)
                    quantity = int(m.group(1)) + int(source == target)
                    get_one.append(
                        {
                            "source": source,
                            "target": target,
                            "quantity": quantity,
                        }
                    )
    # reorder the multi deals so that the highest count is first
    for k, v in multi.items():
        multi[k] = sorted(v, key=lambda x: x[0], reverse=True)

    print(multi["H"])

    table = {x["sku"]: x["price"] for x in parsed_table}

    # todo maybe parse the deal out later
    return table, multi, get_one


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    price_table, multi, get_one = get_tables(TABLE)

    counter = Counter([*skus])

    # validate skus
    if not set(counter.keys()).issubset(set(price_table.keys())):
        return -1

    # apply get_one deals
    for x in get_one:
        counter[x["target"]] -= counter.get(x["source"], 0) // x["quantity"]

    # to apply a group discount i can get all the skus in the group out
    # order the skus by price
    # apply the discount to groups of 3 until there are no more groups of 3
    # then count the remaining skus
    # add it all to the total

    total = 0

    group_discounts = [{"count": 3, "skus": ["S", "T", "X", "Y", "Z"], "price": 45}]

    for group in group_discounts:
        present_skus = [sku for gsku in group["skus"] for sku in gsku * counter[gsku]]
        present_skus = sorted(present_skus, key=lambda x: price_table[x], reverse=True)

        num_groups = len(present_skus) // group["count"]
        total += num_groups * group["price"]

        # remove the skus that were used in the group discount
        for sku in present_skus[: num_groups * group["count"]]:
            counter[sku] -= 1

    # now process the multi-prices
    # to work out a price for a letter with deals, apply the deal price with highest number of items
    # then apply the deal price with the next highest number of items, and so on

    for sku, count in counter.items():
        if count <= 0:
            continue

        if sku not in multi:
            total += count * price_table.get(sku, 0)
            continue

        for deal_count, deal_price in multi[sku]:
            while count >= deal_count:
                count -= deal_count
                total += deal_price

        if count > 0:
            total += count * price_table[sku]

    return total

    # # first process free items
    # # for every 2 E, get a B free
    # counter["B"] -= counter.get("E", 0) // 2

    # # for every 3 N, get an M free
    # counter["M"] -= counter.get("N", 0) // 3

    # # for every 3 R, get a Q free
    # counter["Q"] -= counter.get("R", 0) // 3

    # # for every 2 F, get an F free
    # counter["F"] -= counter.get("F", 0) // 3

    # # for every 3 U, get a U free
    # counter["U"] -= counter.get("U", 0) // 4


