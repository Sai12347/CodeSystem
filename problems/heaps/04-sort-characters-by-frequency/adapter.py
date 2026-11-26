from collections import Counter
import solution


def run(inp):
    s = inp["s"]
    res = solution.Solution().frequencySort(s)
    if not isinstance(res, str):
        return f"Expected str, got {type(res).__name__}"
    if len(res) != len(s) or Counter(res) != Counter(s):
        return "Output is not a permutation of the input string"
    seen = set()
    prev_run = len(s) + 1
    i = 0
    n = len(res)
    while i < n:
        ch = res[i]
        if ch in seen:
            return f"Character '{ch}' is not grouped contiguously"
        seen.add(ch)
        j = i
        while j < n and res[j] == ch:
            j += 1
        run_len = j - i
        if run_len > prev_run:
            return f"Frequencies are not in non-increasing order at character '{ch}'"
        prev_run = run_len
        i = j
    return True
