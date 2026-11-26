def visible():
    return [{'in': {'haystack': 'sadbutsad', 'needle': 'sad'}}, {'in': {'haystack': 'leetcode', 'needle': 'leeto'}}, {'in': {'haystack': 'aaaaa', 'needle': 'bba'}}]

def hidden():
    return [{'in': {'haystack': 'abc', 'needle': ''}}, {'in': {'haystack': 'mississippi', 'needle': 'issip'}}, {'in': {'haystack': 'ababababca', 'needle': 'abababca'}}, {'in': {'haystack': 'a', 'needle': 'a'}}, {'in': {'haystack': '', 'needle': 'a'}}, {'in': {'haystack': 'abcabcabcd', 'needle': 'abcabcd'}}, {'in': {'haystack': 'aaaaaaab', 'needle': 'aaaab'}}, {'in': {'haystack': 'xyz', 'needle': 'xyzq'}}]
