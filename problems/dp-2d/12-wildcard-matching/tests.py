def visible():
    return [{'in': {'s': 'adceb', 'p': '*a*b'}}, {'in': {'s': 'aa', 'p': 'a'}}, {'in': {'s': 'aa', 'p': '*'}}]

def hidden():
    return [{'in': {'s': '', 'p': ''}}, {'in': {'s': '', 'p': '*'}}, {'in': {'s': 'a', 'p': '?'}}, {'in': {'s': 'cb', 'p': '?a'}}, {'in': {'s': 'abc', 'p': 'a*c'}}, {'in': {'s': 'abc', 'p': '***'}}, {'in': {'s': 'mississippi', 'p': 'm*si*?i*pi'}}, {'in': {'s': 'abcdef', 'p': 'a*d?f'}}]
