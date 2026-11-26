import random


def _gen_equations(n: int, contradict: bool, seed: int) -> list[str]:
    rng = random.Random(seed)
    letters = [chr(ord("a") + i) for i in range(26)]
    # Partition 26 letters into 4 groups so equality edges stay within groups
    groups = [i % 4 for i in range(26)]
    eqs = []
    target = n - 1 if contradict else n
    while len(eqs) < target:
        x = rng.randrange(26)
        y = rng.randrange(26)
        if groups[x] == groups[y]:
            eqs.append(f"{letters[x]}=={letters[y]}")
        else:
            eqs.append(f"{letters[x]}!={letters[y]}")
    if contradict:
        # Force a transitive contradiction inside group 0 (0, 4, 8, 12, ...)
        eqs[0] = "a==e"
        eqs[1] = "e==i"
        eqs[2] = "i==m"
        eqs.append("a!=m")
    rng.shuffle(eqs)
    return eqs


def visible():
    return [
        {"in": {"equations": ["a==b", "b!=a"]}},
        {"in": {"equations": ["b==a", "a==b"]}},
    ]


def hidden():
    # 1. Self-inequality
    t1 = ["a!=a"]
    # 2. Self-equality
    t2 = ["z==z"]
    # 3. Inequality appears before the transitive equality chain
    t3 = ["a!=d", "a==b", "b==c", "c==d"]
    # 4. Full 26-letter equality chain contradicted by a!=z
    t4 = [f"{chr(97 + i)}=={chr(98 + i)}" for i in range(25)] + ["a!=z"]
    # 5. Full 26-letter equality chain with consistent redundant equality
    t5 = [f"{chr(97 + i)}=={chr(98 + i)}" for i in range(25)] + ["z==a"]
    # 6. Two disjoint equality components with cross-inequalities only
    t6 = ["a==b", "b==c", "d==e", "e==f", "a!=d", "b!=e", "c!=f"]
    # 7. Complete inequality graph on 10 distinct letters (always satisfiable)
    t7 = [f"{chr(97 + i)}!={chr(97 + j)}" for i in range(10) for j in range(i + 1, 10)]
    # 8. Mixed duplicates with late bridging equality creating contradiction
    t8 = ["a==b", "b==a", "c==d", "b!=c", "c!=b", "e==f", "d==a"]
    # 9. Medium random satisfiable system (n = 200)
    t9 = _gen_equations(200, False, 9901)
    # 10. Max-size stress test (n = 500) with subtle transitive contradiction
    t10 = _gen_equations(500, True, 9902)

    return [{"in": {"equations": t}} for t in (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10)]
