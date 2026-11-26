class Solution:
    def pancakeSort(self, arr: List[int]) -> List[int]:
        res = []
        n = len(arr)
        for val in range(n, 1, -1):
            idx = arr.index(val)
            if idx == val - 1:
                continue
            if idx > 0:
                arr[:idx + 1] = reversed(arr[:idx + 1])
                res.append(idx + 1)
            arr[:val] = reversed(arr[:val])
            res.append(val)
        return res
