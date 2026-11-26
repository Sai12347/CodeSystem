def visible():
    return [
        {"in": {"amount": 5, "coins": [1, 2, 5]}},
        {"in": {"amount": 3, "coins": [2]}},
        {"in": {"amount": 10, "coins": [10]}},
    ]


def hidden():
    return [
        {"in": {"amount": 0, "coins": [1, 2, 5]}},
        {"in": {"amount": 0, "coins": [7]}},
        {"in": {"amount": 12, "coins": [3]}},
        {"in": {"amount": 4, "coins": [5, 10, 20]}},
        {"in": {"amount": 7, "coins": [5, 1, 2]}},
        {"in": {"amount": 99, "coins": [2, 4, 6, 8]}},
        {"in": {"amount": 100, "coins": [1, 5, 10, 25]}},
        {"in": {"amount": 200, "coins": [3, 5, 7, 8, 9, 10, 11]}},
        {"in": {"amount": 5000, "coins": [100, 200, 500, 1000, 2000, 5000]}},
        {"in": {"amount": 5000, "coins": [50, 75, 125, 200, 350, 500, 750, 1000, 1500, 2500]}},
        {"in": {"amount": 1000, "coins": list(range(200, 300))}},
    ]
