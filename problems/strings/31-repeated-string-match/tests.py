def visible():
    return [{'in': {'a': 'abcd', 'b': 'cdabcdab'}}, {'in': {'a': 'a', 'b': 'aaab'}}, {'in': {'a': 'a', 'b': 'a'}}]

def hidden():
    return [{'in': {'a': 'abc', 'b': 'cabcab'}}, {'in': {'a': 'abc', 'b': 'ac'}}, {'in': {'a': 'ab', 'b': 'bababa'}}, {'in': {'a': 'xyz', 'b': 'zxyzxy'}}, {'in': {'a': 'abcd', 'b': 'abcdabcd'}}, {'in': {'a': 'a', 'b': 'aaaaa'}}, {'in': {'a': 'abc', 'b': 'bca'}}, {'in': {'a': 'abcd', 'b': 'dabcda'}}]
