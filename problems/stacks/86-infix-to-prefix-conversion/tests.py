def visible():
    return [{'in': {'s': '(a + b) * c'}}, {'in': {'s': 'a - b - c'}}, {'in': {'s': 'a + b * c - d'}}]

def hidden():
    return [{'in': {'s': 'x'}}, {'in': {'s': '((a))'}}, {'in': {'s': 'a * b / c'}}, {'in': {'s': 'a - (b - c)'}}, {'in': {'s': '(a + b) * (c - d)'}}, {'in': {'s': 'a + b + c + d'}}, {'in': {'s': 'a * (b + c * (d - e)) / f'}}, {'in': {'s': '((a / b) + (c * d)) - e'}}, {'in': {'s': 'i - g / w * j / (g / m + l) - p * (b * (v / e / a + f) * j / (p + x * j + w - (h * n))) / (s + e + u + (h - k / w) - ((s / t) * m) * c)'}}]
