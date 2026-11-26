import math
import solution


def run(inp):
    w = [int(x) for x in inp["w"]]
    trials = int(inp["trials"])
    n = len(w)
    sol = solution.Solution(list(w))
    counts = [0] * n
    for _ in range(trials):
        idx = sol.pickIndex()
        if not isinstance(idx, int) or isinstance(idx, bool):
            return f"pickIndex() must return an int, got {type(idx).__name__}"
        if idx < 0 or idx >= n:
            return f"pickIndex() returned out-of-range index {idx} for length {n}"
        counts[idx] += 1

    total = sum(w)
    for i in range(n):
        p = w[i] / total
        obs = counts[i] / trials
        tol = max(0.035, 6.5 * math.sqrt(p * (1.0 - p) / trials))
        if abs(obs - p) > tol:
            return f"Distribution mismatch at index {i}: expected {p:.4f}, got {obs:.4f}"

    if n > 10:
        blocks = 4
        for b in range(blocks):
            lo = (b * n) // blocks
            hi = ((b + 1) * n) // blocks
            p = sum(w[lo:hi]) / total
            obs = sum(counts[lo:hi]) / trials
            tol = max(0.035, 6.5 * math.sqrt(p * (1.0 - p) / trials))
            if abs(obs - p) > tol:
                return f"Distribution mismatch in block [{lo}, {hi}): expected {p:.4f}, got {obs:.4f}"

    return True
