import random


def _stress_shared_prefix(num_strs: int, prefix_len: int, total_len: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    prefix = "".join(chr(ord("a") + rng.randrange(26)) for _ in range(prefix_len))
    out = []
    for idx in range(num_strs):
        if prefix_len == total_len:
            out.append(prefix)
        else:
            first_diff = chr(ord("a") + (idx % 26))
            tail = "".join(
                chr(ord("a") + rng.randrange(26))
                for _ in range(total_len - prefix_len - 1)
            )
            out.append(prefix + first_diff + tail)
    return out


def visible():
    return [
        {"in": {"strs": ["flower", "flow", "flight"]}},
        {"in": {"strs": ["dog", "racecar", "car"]}},
        {"in": {"strs": ["interspecies", "interstellar", "interstate"]}},
    ]


def hidden():
    return [
        {"in": {"strs": ["alone"]}},
        {"in": {"strs": [""]}},
        {"in": {"strs": ["abc", "", "ab"]}},
        {"in": {"strs": ["same", "same", "same", "same"]}},
        {"in": {"strs": ["prefixlonger", "prefixlong", "pre"]}},
        {"in": {"strs": ["a", "ab", "abc", "abcd"]}},
        {"in": {"strs": ["abcdefg", "abcdefg", "abcdefh"]}},
        {"in": {"strs": ["apple", "apricot", "ant"]}},
        {"in": {"strs": _stress_shared_prefix(200, 180, 200, seed=14)}},
        {"in": {"strs": _stress_shared_prefix(200, 150, 150, seed=15)}},
    ]
