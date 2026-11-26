def visible():
    return [{'in': {'s1': 'aabcc', 's2': 'dbbca', 's3': 'aadbbcbcac'}}, {'in': {'s1': 'aabcc', 's2': 'dbbca', 's3': 'aadbbbaccc'}}, {'in': {'s1': '', 's2': '', 's3': ''}}]

def hidden():
    return [{'in': {'s1': 'a', 's2': '', 's3': 'a'}}, {'in': {'s1': '', 's2': 'b', 's3': 'b'}}, {'in': {'s1': 'ab', 's2': 'cd', 's3': 'acbd'}}, {'in': {'s1': 'ab', 's2': 'cd', 's3': 'abcd'}}, {'in': {'s1': 'aa', 's2': 'ab', 's3': 'aaba'}}, {'in': {'s1': 'a', 's2': 'b', 's3': 'ba'}}, {'in': {'s1': 'abc', 's2': 'def', 's3': 'adbcef'}}, {'in': {'s1': 'abc', 's2': 'def', 's3': 'abdecf'}}]
