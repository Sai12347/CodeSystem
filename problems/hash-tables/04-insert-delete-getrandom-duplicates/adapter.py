import solution


def run(inp):
    ops = inp["ops"]
    args = inp["args"]
    if not ops or ops[0] != "RandomizedCollection":
        return "First operation must be RandomizedCollection"
    obj = solution.RandomizedCollection()
    counts = {}
    total = 0
    streak = 0
    streak_counts = {}

    def check_streak():
        nonlocal streak
        if streak >= 100 and len(counts) >= 2:
            if len(streak_counts) < 2:
                return f"getRandom() returned only {list(streak_counts.keys())} across {streak} draws from {len(counts)} distinct values"
            if streak >= 400:
                max_val, max_cnt = max(counts.items(), key=lambda kv: kv[1])
                if max_cnt * 100 >= 85 * total:
                    got_cnt = streak_counts.get(max_val, 0)
                    if got_cnt * 100 < 70 * streak:
                        return (
                            f"getRandom() distribution appears unweighted: value {max_val} has "
                            f"{max_cnt}/{total} copies but appeared only {got_cnt}/{streak} times"
                        )
        return None

    for i in range(1, len(ops)):
        op = ops[i]
        a = args[i]
        if op == "insert":
            err = check_streak()
            if err:
                return err
            streak = 0
            streak_counts.clear()
            val = int(a[0])
            expected = counts.get(val, 0) == 0
            counts[val] = counts.get(val, 0) + 1
            total += 1
            got = obj.insert(val)
            if not isinstance(got, bool) or got != expected:
                return f"Op {i} insert({val}): expected {expected}, got {got}"
        elif op == "remove":
            err = check_streak()
            if err:
                return err
            streak = 0
            streak_counts.clear()
            val = int(a[0])
            expected = counts.get(val, 0) > 0
            if expected:
                counts[val] -= 1
                total -= 1
                if counts[val] == 0:
                    del counts[val]
            got = obj.remove(val)
            if not isinstance(got, bool) or got != expected:
                return f"Op {i} remove({val}): expected {expected}, got {got}"
        elif op == "getRandom":
            got = obj.getRandom()
            if isinstance(got, bool) or not isinstance(got, int):
                return f"Op {i} getRandom(): expected int, got {type(got).__name__}"
            if counts.get(got, 0) <= 0:
                return f"Op {i} getRandom(): returned {got}, which is not in the collection"
            if len(counts) >= 2:
                streak += 1
                streak_counts[got] = streak_counts.get(got, 0) + 1
        else:
            return f"Unknown operation {op}"

    err = check_streak()
    if err:
        return err
    return True
