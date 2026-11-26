import solution


def run(inp):
    ops = inp["ops"]
    args = inp["args"]
    if not ops or ops[0] != "RandomizedSet":
        return "First operation must be RandomizedSet"
    obj = solution.RandomizedSet()
    ref = set()
    streak = 0
    seen_in_streak = set()

    for i in range(1, len(ops)):
        op = ops[i]
        a = args[i]
        if op == "insert":
            val = int(a[0])
            expected = val not in ref
            if expected:
                ref.add(val)
            got = obj.insert(val)
            if not isinstance(got, bool) or got != expected:
                return f"Op {i} insert({val}): expected {expected}, got {got}"
            streak = 0
            seen_in_streak.clear()
        elif op == "remove":
            val = int(a[0])
            expected = val in ref
            if expected:
                ref.remove(val)
            got = obj.remove(val)
            if not isinstance(got, bool) or got != expected:
                return f"Op {i} remove({val}): expected {expected}, got {got}"
            streak = 0
            seen_in_streak.clear()
        elif op == "getRandom":
            got = obj.getRandom()
            if isinstance(got, bool) or not isinstance(got, int):
                return f"Op {i} getRandom(): expected int, got {type(got).__name__}"
            if got not in ref:
                return f"Op {i} getRandom(): returned {got}, which is not in the set"
            if len(ref) >= 2:
                streak += 1
                seen_in_streak.add(got)
                if streak >= 100 and len(seen_in_streak) < 2:
                    return f"Op {i} getRandom(): returned only {seen_in_streak} across {streak} draws from {len(ref)} elements"
        else:
            return f"Unknown operation {op}"
    return True
