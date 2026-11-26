import random


def visible():
    return [
        {"in": {"path": "/home/"}},
        {"in": {"path": "/home//foo/"}},
        {"in": {"path": "/home/user/Documents/../Pictures"}},
    ]


def hidden():
    rng = random.Random(71)
    names = ["usr", "bin", "lib", "var", "opt", "dir_1", "a", "b2", "...", ".cfg", "..file"]
    parts = [""]
    total_len = 0
    while total_len < 2700:
        r = rng.random()
        if r < 0.2:
            seg = ".."
        elif r < 0.35:
            seg = "."
        elif r < 0.45:
            seg = ""
        else:
            seg = rng.choice(names)
        if total_len + len(seg) + 1 > 2900:
            break
        parts.append(seg)
        total_len += len(seg) + 1
    stress_random = "/".join(parts)

    # Push 350 directories then pop 349 -> length ~2800 (<= 3000)
    push_pop = "/" + "/".join(f"d{i}" for i in range(350)) + "/" + "/".join([".."] * 349)

    return [
        {"in": {"path": "/"}},
        {"in": {"path": "/////"}},
        {"in": {"path": "/../"}},
        {"in": {"path": "/../../../.."}},
        {"in": {"path": "/.../a/../b/c/../d/./"}},
        {"in": {"path": "/.hidden/..file/a..b/_dir/./.."}},
        {"in": {"path": "/a/b/c/../../../"}},
        {"in": {"path": "/a/./b/../../c/"}},
        {"in": {"path": "/usr/local/bin/python3"}},
        {"in": {"path": stress_random}},
        {"in": {"path": push_pop}},
    ]
