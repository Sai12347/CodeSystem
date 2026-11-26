class NumArray:
    def __init__(self, nums: List[int]):
        self.values = nums[:]
        self.bit = [0] * (len(nums) + 1)
        for i, value in enumerate(nums):
            self._add(i + 1, value)

    def _add(self, i: int, delta: int) -> None:
        while i < len(self.bit):
            self.bit[i] += delta
            i += i & -i

    def _prefix(self, i: int) -> int:
        total = 0
        while i:
            total += self.bit[i]
            i -= i & -i
        return total

    def update(self, index: int, value: int) -> None:
        delta = value - self.values[index]
        self.values[index] = value
        self._add(index + 1, delta)

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix(right + 1) - self._prefix(left)
