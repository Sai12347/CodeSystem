def visible():
    return [{'in': {'s': 'ab', 'goal': 'ba'}}, {'in': {'s': 'ab', 'goal': 'ab'}}, {'in': {'s': 'aa', 'goal': 'aa'}}]

def hidden():
    return [{'in': {'s': 'aaaaaaabc', 'goal': 'aaaaaaacb'}}, {'in': {'s': 'abc', 'goal': 'acb'}}, {'in': {'s': 'abc', 'goal': 'abc'}}, {'in': {'s': '', 'goal': ''}}, {'in': {'s': 'ab', 'goal': 'ca'}}, {'in': {'s': 'aab', 'goal': 'aba'}}, {'in': {'s': 'abcd', 'goal': 'badc'}}, {'in': {'s': 'abc', 'goal': 'ab'}}]
