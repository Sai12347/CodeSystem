import solution


def run(inp):
    orig = [int(v) for v in inp["nums"]]
    n = len(orig)
    idx = solution.Solution().findPeakElement(list(orig))
    if isinstance(idx, bool) or not isinstance(idx, int):
        return f"Expected integer index, got {type(idx).__name__}"
    if idx < 0 or idx >= n:
        return f"Index {idx} out of range [0, {n - 1}]"
    left_ok = idx == 0 or orig[idx] > orig[idx - 1]
    right_ok = idx == n - 1 or orig[idx] > orig[idx + 1]
    if not (left_ok and right_ok):
        return f"Index {idx} (value {orig[idx]}) is not a peak"
    return True
