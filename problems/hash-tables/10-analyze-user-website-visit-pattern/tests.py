import random


def visible():
    return [
        {"in": {
            "username": ["joe", "joe", "joe", "james", "james", "james", "james", "mary", "mary", "mary"],
            "timestamp": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "website": ["home", "about", "career", "home", "cart", "maps", "home", "home", "about", "career"]
        }},
        {"in": {
            "username": ["ua", "ua", "ua", "ub", "ub", "ub"],
            "timestamp": [1, 2, 3, 4, 5, 6],
            "website": ["a", "b", "a", "a", "b", "c"]
        }},
    ]


def hidden():
    rng = random.Random(1152)

    # Max-size test (n = 50) with unsorted timestamps across 5 users
    users_pool = ["alice", "bob", "carol", "dave", "erin"]
    sites_pool = ["home", "login", "cart", "pay", "help", "blog"]
    records = []
    used_ts = {u: set() for u in users_pool}
    for _ in range(50):
        u = rng.choice(users_pool)
        t = rng.randint(1, 10**9)
        while t in used_ts[u]:
            t = rng.randint(1, 10**9)
        used_ts[u].add(t)
        w = rng.choice(sites_pool)
        records.append((u, t, w))
    rng.shuffle(records)

    # Single user with 12 visits (stress combinations for one user + lexicographical tie-break)
    single_u = ["solo"] * 12
    single_t = [120, 10, 90, 30, 110, 50, 70, 20, 100, 40, 80, 60]
    single_w = ["z", "d", "b", "c", "a", "b", "c", "a", "d", "a", "b", "c"]

    return [
        # Minimum size n = 3 with unsorted timestamps
        {"in": {
            "username": ["u", "u", "u"],
            "timestamp": [300, 100, 200],
            "website": ["third", "first", "second"]
        }},
        # Same user repeats pattern many times (must count as 1, losing to pattern seen by 2 users!)
        {"in": {
            "username": ["a", "a", "a", "a", "a", "a", "b", "b", "b", "c", "c", "c"],
            "timestamp": [1, 2, 3, 4, 5, 6, 1, 2, 3, 1, 2, 3],
            "website": ["x", "x", "x", "x", "x", "x", "z", "y", "w", "z", "y", "w"]
        }},
        # Unsorted timestamps across multiple users
        {"in": {
            "username": ["ua", "ub", "ua", "ub", "ua", "ub"],
            "timestamp": [30, 10, 10, 30, 20, 20],
            "website": ["c", "a", "a", "c", "b", "b"]
        }},
        # Users with < 3 visits ignored
        {"in": {
            "username": ["a", "a", "b", "c", "c", "c", "d", "d"],
            "timestamp": [1, 2, 1, 10, 20, 30, 5, 6],
            "website": ["home", "home", "home", "shop", "cart", "pay", "shop", "cart"]
        }},
        # Lexicographical tie-break with prefix strings ("a", "aa", "b" vs "a", "ab", "a")
        {"in": {
            "username": ["ua", "ua", "ua", "ub", "ub", "ub"],
            "timestamp": [1, 2, 3, 1, 2, 3],
            "website": ["a", "ab", "a", "a", "aa", "b"]
        }},
        # Repeated website names in winning pattern
        {"in": {
            "username": ["ua", "ua", "ua", "ub", "ub", "ub"],
            "timestamp": [5, 1, 9, 1000000000, 500000000, 1],
            "website": ["home", "home", "home", "home", "home", "home"]
        }},
        # Tie between two patterns with score 2 -> pick lexicographically smaller
        {"in": {
            "username": ["a", "a", "a", "b", "b", "b", "c", "c", "c", "d", "d", "d"],
            "timestamp": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
            "website": ["beta", "alpha", "gamma", "beta", "alpha", "gamma", "alpha", "zeta", "omega", "alpha", "zeta", "omega"]
        }},
        # Classic LC 1152 unsorted timestamp example
        {"in": {
            "username": ["zkiikgv", "zkiikgv", "zkiikgv", "zkiikgv"],
            "timestamp": [436363475, 710406388, 386655081, 797150921],
            "website": ["wnaaxbfhxp", "mryxsjc", "oz", "wlarkzzqht"]
        }},
        # Single user with 12 unsorted visits
        {"in": {
            "username": single_u,
            "timestamp": single_t,
            "website": single_w
        }},
        # Max-size 50 records randomized stress test
        {"in": {
            "username": [r[0] for r in records],
            "timestamp": [r[1] for r in records],
            "website": [r[2] for r in records]
        }},
    ]
