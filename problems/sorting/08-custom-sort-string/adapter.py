import solution


def run(inp):
    order = inp["order"]
    s = inp["s"]
    res = solution.Solution().customSortString(order, s)
    if not isinstance(res, str):
        return f"Expected str, got {type(res).__name__}"
    if len(res) != len(s) or sorted(res) != sorted(s):
        return f"Output '{res}' is not a permutation of '{s}'"
    rank = {c: i for i, c in enumerate(order)}
    prev = -1
    for c in res:
        if c in rank:
            if rank[c] < prev:
                return f"Character '{c}' violates custom order '{order}'"
            prev = rank[c]
    return True
