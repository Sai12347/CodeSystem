from collections import Counter
import solution


def run(inp):
    s = inp["s"]
    res = solution.Solution().reorganizeString(s)
    if not isinstance(res, str):
        return f"Expected str, got {type(res).__name__}"
    counts = Counter(s)
    possible = max(counts.values()) <= (len(s) + 1) // 2
    if not possible:
        if res == "":
            return True
        return f"Expected empty string for impossible input, got '{res[:50]}'"
    if len(res) != len(s) or Counter(res) != counts:
        return "Output is not a permutation of the input string"
    for i in range(1, len(res)):
        if res[i] == res[i - 1]:
            return f"Adjacent duplicate character '{res[i]}' at indices {i - 1} and {i}"
    return True
