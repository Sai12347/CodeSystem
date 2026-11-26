def visible():
    return [{'in': {'s': 'lee(t(c)o)de)'}}, {'in': {'s': 'a)b(c)d'}}, {'in': {'s': '))('}}]

def hidden():
    return [{'in': {'s': '(a(b(c)d)'}}, {'in': {'s': 'abc'}}, {'in': {'s': '((a))'}}, {'in': {'s': 'a((b)c))'}}, {'in': {'s': '(()'}}, {'in': {'s': '())()(('}}, {'in': {'s': 'x(y)z'}}, {'in': {'s': '(((('}}]
