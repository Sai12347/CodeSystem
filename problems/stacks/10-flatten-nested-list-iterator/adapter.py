import solution


class NestedInteger:
    def __init__(self, value):
        if isinstance(value, int) and not isinstance(value, bool):
            self._int = value
            self._list = None
        else:
            self._int = None
            self._list = [NestedInteger(x) for x in value]

    def isInteger(self) -> bool:
        return self._int is not None

    def getInteger(self) -> int:
        return self._int

    def getList(self):
        return self._list


def run(inp):
    nested_list = [NestedInteger(x) for x in inp["nestedList"]]
    solution.NestedInteger = NestedInteger
    it = solution.NestedIterator(nested_list)
    res = []
    limit = 100000
    while it.hasNext():
        if len(res) >= limit:
            return "Exceeded maximum output length (possible infinite loop in hasNext/next)"
        if not it.hasNext():
            return "hasNext() is not idempotent"
        res.append(int(it.next()))
    if it.hasNext():
        return "hasNext() returned True after iterator was exhausted"
    return res
