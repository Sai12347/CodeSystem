import solution


class MountainArray:
    def __init__(self, arr):
        self._arr = arr
        self._calls = 0

    def get(self, index: int) -> int:
        self._calls += 1
        if index < 0 or index >= len(self._arr):
            raise IndexError(f"Index {index} out of bounds for length {len(self._arr)}")
        return self._arr[index]

    def length(self) -> int:
        return len(self._arr)


def run(inp):
    arr = [int(v) for v in inp["mountainArr"]]
    target = int(inp["target"])
    ma = MountainArray(arr)
    solution.MountainArray = MountainArray
    res = solution.Solution().findInMountainArray(target, ma)
    if ma._calls > 100:
        return f"Exceeded maximum of 100 calls to MountainArray.get() (made {ma._calls} calls)"
    return None if res is None else int(res)
