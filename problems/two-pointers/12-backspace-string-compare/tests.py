import random


def _build_noisy(rng, target, max_len=200):
    out = []
    n = len(target)
    for idx, ch in enumerate(target):
        out.append(ch)
        rem = n - idx - 1
        noise_len = rng.randint(1, 3)
        if len(out) + 2 * noise_len + rem <= max_len and rng.random() < 0.65:
            for _ in range(noise_len):
                out.append(chr(ord('a') + rng.randint(0, 25)))
            for _ in range(noise_len):
                out.append('#')
    return "".join(out)


def visible():
    return [
        {"in": {"s": "ab#c", "t": "ad#c"}},
        {"in": {"s": "ab##", "t": "c#d#"}},
        {"in": {"s": "a#c", "t": "b"}},
    ]


def hidden():
    rng = random.Random(844)
    base = "".join(chr(ord('a') + rng.randint(0, 25)) for _ in range(45))
    # Build two distinct length<=200 encodings of the same base string
    long_eq_s = "###" + _build_noisy(rng, base, 197)
    long_eq_t = _build_noisy(rng, base, 200)

    # Differ only at the very first surviving character
    alt_first = 'b' if base[0] == 'a' else 'a'
    diff_base = alt_first + base[1:]
    long_neq_s = _build_noisy(rng, base, 200)
    long_neq_t = _build_noisy(rng, diff_base, 200)

    return [
        {"in": {"s": "a", "t": "a"}},
        {"in": {"s": "a", "t": "b"}},
        {"in": {"s": "#", "t": "####"}},
        {"in": {"s": "###a", "t": "a"}},
        {"in": {"s": "bxj##tw", "t": "bxo#j##tw"}},
        {"in": {"s": "bxj##tw", "t": "bxj###tw"}},
        {"in": {"s": "nzp#o#g", "t": "b#nzp#o#g"}},
        {"in": {"s": "y#fo##f", "t": "y#f#o##f"}},
        {"in": {"s": long_eq_s, "t": long_eq_t}},
        {"in": {"s": long_neq_s, "t": long_neq_t}},
    ]
