import random


def visible():
    return [
        {"in": {"s": "tree"}},
        {"in": {"s": "cccaaa"}},
        {"in": {"s": "Aabb"}},
    ]


def hidden():
    rng1 = random.Random(45101)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    stress1 = "".join(rng1.choices(alphabet, k=4000))

    rng2 = random.Random(45102)
    chunks = []
    for i, ch in enumerate(alphabet[:30]):
        chunks.append(ch * (i + 1))
    chars2 = list("".join(chunks))
    rng2.shuffle(chars2)
    stress2 = "".join(chars2)

    return [
        {"in": {"s": "z"}},
        {"in": {"s": "aaaaaa"}},
        {"in": {"s": "abcdef"}},
        {"in": {"s": "0123456789001112222"}},
        {"in": {"s": "AaBbCcAaBbA"}},
        {"in": {"s": "2a554442f544asfasssffffasss"}},
        {"in": {"s": "Z9z9Z9a0a0"}},
        {"in": {"s": "mississippi"}},
        {"in": {"s": stress1}},
        {"in": {"s": stress2}},
    ]
