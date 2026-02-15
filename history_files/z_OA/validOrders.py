# [p1, p2, d1, d2] - 4
# [p1, p1, d1, d1] - 2 [p1, d1]
# [p1, p1, d1]
# orders = ["p1", "p2", "d1", "d2"]
# orders = ["p1", "p1", "d1", "d1"]
# orders = ["p1", "p1", "d1", "d2"]
# orders = ["p1", "p2", "d1", "d3"]
# orders = ["d1", "p1", "d1"]
# orders = ["p1", "p1", "d1"]
# orders = ['p1', 'd1', 'p1', 'p2', 'p3', 'd1', 'd2', 'd3']

orders_list = []
orders_list.append(["p1", "p2", "d1", "d2"])
orders_list.append(["d1", "p1", "d1"])
orders_list.append(["p1", "p1", "d1", "d1"])
orders_list.append(['p1', 'd1', 'p1', 'p2', 'p3', 'd1', 'd2', 'd3'])

def validOrder(orders:list) -> list:
    picked = set()
    delivered = set()
    for order in orders:
        status, v = order[0], order[1]

        if status == "d":  # need to know if it's picked up or not?
            if v in picked and v not in delivered:
                # have already picked, and not delivered before
                delivered.add(v)  # 记录order编号
        else:  # pick order
            if v not in picked:
                picked.add(v)

    res = []
    delivered = sorted(delivered) # 不需要先list再sort

    for i in delivered:
        res.append("p" + i)

    for i in delivered:
        res.append("d" + i)
    return res

for orders in orders_list:
    print(validOrder(orders))

# if need to preserve pick/delivery order
# visited = set()
# for order in orders:
#     if order[1] in delivered and order not in visited:
#         res.append(order)
#         visited.add(order)