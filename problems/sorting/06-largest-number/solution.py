from functools import cmp_to_key


class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        strs = [str(x) for x in nums]

        def cmp(a: str, b: str) -> int:
            ab, ba = a + b, b + a
            if ab > ba:
                return -1
            if ab < ba:
                return 1
            return 0

        strs.sort(key=cmp_to_key(cmp))
        if strs[0] == "0":
            return "0"
        return "".join(strs)
