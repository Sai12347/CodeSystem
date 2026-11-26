import solution


def run(inp):
    orig = [int(v) for v in inp["arr"]]
    n = len(orig)
    flips = solution.Solution().pancakeSort(list(orig))
    if not isinstance(flips, list):
        return f"Expected list of ints, got {type(flips).__name__}"
    if len(flips) > 10 * n:
        return f"Too many flips: {len(flips)} exceeds limit {10 * n}"
    sim = list(orig)
    for idx, k in enumerate(flips):
        if isinstance(k, bool) or not isinstance(k, int):
            return f"Flip #{idx} is not an integer: {k!r}"
        if k < 1 or k > n:
            return f"Flip #{idx} value {k} out of range [1, {n}]"
        sim[:k] = reversed(sim[:k])
    if sim != sorted(orig):
        return f"Array is not sorted after applying flips: got {sim[:20]}"
    return True
