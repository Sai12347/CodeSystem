import random


def _gen_accounts(num_people: int, num_accounts: int, seed: int) -> list[list[str]]:
    rng = random.Random(seed)
    names = ["Alice", "Bob", "Carol", "David", "Emma", "Frank", "Grace", "Henry"]
    people_names = [names[i % len(names)] for i in range(num_people)]
    people_emails = [
        [f"p{i}e{j}@m.co" for j in range(rng.randint(2, 6))]
        for i in range(num_people)
    ]
    accounts = []
    for _ in range(num_accounts):
        p = rng.randrange(num_people)
        pool = people_emails[p]
        k = rng.randint(1, min(4, len(pool)))
        chosen = [rng.choice(pool) for _ in range(k)]
        accounts.append([people_names[p]] + chosen)
    rng.shuffle(accounts)
    return accounts


def visible():
    return [
        {
            "in": {
                "accounts": [
                    ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
                    ["John", "johnsmith@mail.com", "john00@mail.com"],
                    ["Mary", "mary@mail.com"],
                    ["John", "johnnybravo@mail.com"],
                ]
            }
        },
        {
            "in": {
                "accounts": [
                    ["Gabe", "Gabe0@m.co", "Gabe3@m.co", "Gabe1@m.co"],
                    ["Kevin", "Kevin3@m.co", "Kevin5@m.co", "Kevin0@m.co"],
                    ["Ethan", "Ethan5@m.co", "Ethan4@m.co", "Ethan0@m.co"],
                    ["Hanzo", "Hanzo3@m.co", "Hanzo1@m.co", "Hanzo0@m.co"],
                    ["Fern", "Fern5@m.co", "Fern1@m.co", "Fern0@m.co"],
                ]
            }
        },
    ]


def hidden():
    # 1. Single account with single email
    t1 = [["Alice", "a@x.com"]]
    # 2. Duplicate emails inside the same account
    t2 = [["Bob", "b@x.com", "a@x.com", "b@x.com", "a@x.com"]]
    # 3. Transitive chain merged only when the final bridging accounts arrive
    t3 = [
        ["David", "e1@m.co", "e2@m.co"],
        ["David", "e3@m.co", "e4@m.co"],
        ["David", "e5@m.co", "e6@m.co"],
        ["David", "e2@m.co", "e3@m.co"],
        ["David", "e4@m.co", "e5@m.co"],
    ]
    # 4. Same name, completely disjoint people
    t4 = [
        ["Alex", "a1@m.co"],
        ["Alex", "a2@m.co"],
        ["Alex", "a3@m.co"],
        ["Alex", "a4@m.co"],
    ]
    # 5. Repeated identical accounts
    t5 = [
        ["Sam", "z@m.co", "a@m.co"],
        ["Sam", "a@m.co", "z@m.co"],
        ["Sam", "z@m.co", "a@m.co"],
    ]
    # 6. ASCII lexicographical order (digits, uppercase, underscore, lowercase)
    t6 = [
        ["Mix", "a@m.co", "Z@m.co", "0@m.co"],
        ["Mix", "Z@m.co", "_@m.co", "A@m.co", "9@m.co"],
    ]
    # 7. Star merge: 10 accounts all sharing one hub email
    t7 = [["Hub", "hub@m.co", f"leaf{i}@m.co"] for i in range(10)]
    # 8. Three distinct "David" clusters mixed together
    t8 = [
        ["David", "d1a@m.co", "d1b@m.co"],
        ["David", "d2a@m.co", "d2b@m.co"],
        ["David", "d3a@m.co", "d3b@m.co"],
        ["David", "d1b@m.co", "d1c@m.co"],
        ["David", "d2b@m.co", "d2c@m.co"],
        ["David", "d3c@m.co", "d3a@m.co"],
    ]
    # 9. Medium random accounts
    t9 = _gen_accounts(40, 120, 7211)
    # 10. Larger stress test
    t10 = _gen_accounts(120, 400, 7212)

    return [{"in": {"accounts": t}} for t in (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10)]
